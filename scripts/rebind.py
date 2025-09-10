import os
import json
import time
import requests
import base64
import pandas as pd

def get_bearer_token(client_id: str, tenant_id: str, fed_token: str) -> str:
    """
    Get Bearer token using client credentials and federated token

    Parameters:
        client_id (str): The Azure AD application (client) ID.
        tenant_id (str): The Azure tenant ID.
        fed_token (str): The federated token.
    Returns:
        str: The Bearer token.
    """
    
    token_endpoint = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_params = f"\
        grant_type=client_credentials&\
        client_id={client_id}&\
        scope=https://api.fabric.microsoft.com/.default&\
        client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer&\
        client_assertion={fed_token}"
    token_headers = {'Content-Type': 'application/x-www-form-urlencoded'} 
    response = requests.post(token_endpoint, headers=token_headers, data=token_params)

    if response.status_code != 200:
        raise ValueError(f"*ERROR*: ❌ Error obtaining Bearer token. Status code: {response.status_code}, Message: {response.text}")
    
    return response.json()['access_token']

def get_workspace_items(endpoint: str, headers: dict) -> pd.DataFrame:
    """
    Get items from a Fabric workspace

    Parameters:
        endpoint (str): The Fabric API endpoint for the request.
        headers (dict): The headers to be used in the API call.
    Returns:
        pd.DataFrame: DataFrame containing the items in the workspace.
    """

    response = requests.get(endpoint, headers=headers)

    if response.status_code != 200:
        raise ValueError(f"*ERROR*: ❌ Error retrieving items from workspace. Status code: {response.status_code}, Message: {response.text}")
    
    return pd.DataFrame(response.json()['value'])

def main():

    base_url = "https://api.fabric.microsoft.com/v1"
    client_id = os.getenv("CLIENT_ID").strip()
    tenant_id = os.getenv("TENANT_ID").strip()
    fed_token = os.getenv("FED_TOKEN").strip()
    workspace_name = os.getenv("WORKSPACE_NAME").strip()
    dev_workspace_id = os.getenv("DEV_WORKSPACE_ID").strip()
    pro_workspace_id = os.getenv("PRO_WORKSPACE_ID").strip()

    # Validate required variables
    if not client_id:
        raise ValueError("*ERROR*: ❌ CLIENT_ID environment variable is not set.")
    if not tenant_id:
        raise ValueError("*ERROR*: ❌ TENANT_ID environment variable is not set.")
    if not fed_token:
        raise ValueError("*ERROR*: ❌ FED_TOKEN environment variable is not set.")
    if not workspace_name:
        raise ValueError("*ERROR*: ❌ WORKSPACE_NAME environment variable is not set.")
    if not dev_workspace_id:
        raise ValueError("*ERROR*: ❌ DEV_WORKSPACE_ID environment variable is not set.")
    if not pro_workspace_id:
        raise ValueError("*ERROR*: ❌ PRO_WORKSPACE_ID environment variable is not set.")
    
    # Get Bearer token
    bearer_token = get_bearer_token(client_id, tenant_id, fed_token)
    print(f"*INFO*: ✅ Bearer token acquired.")

    # Set headers to be used in Fabric API calls
    fab_headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}

    # Get items from DEV workspace
    print("*INFO*: ▶️ Retrieving items from DEV workspace...")
    dev_items_df = get_workspace_items(f"{base_url}/workspaces/{dev_workspace_id}/items", fab_headers)
    dev_vl_id = dev_items_df[dev_items_df['type']=='VariableLibrary']['id'].item()
    print(f"*INFO*: ✅ Retrieved items from DEV workspace. Variable Library ID: {dev_vl_id}")

    # Get items from PRO workspace
    print("*INFO*: ▶️ Retrieving items from PRO workspace...")
    pro_items_df = get_workspace_items(f"{base_url}/workspaces/{pro_workspace_id}/items", fab_headers)
    pro_items_df = pro_items_df[pro_items_df['type']!='SQLEndpoint']  # Exclude SQL Endpoints
    pro_vl_id = pro_items_df[pro_items_df['type']=='VariableLibrary']['id'].item()
    print(f"*INFO*: ✅ Retrieved items from PRO workspace. Variable Library ID: {pro_vl_id}")

    # Add workspace item row
    workspace_row = pd.DataFrame({
        "id": [pro_workspace_id],
        "displayName": [workspace_name],
        "description": [""],
        "type": ["Workspace"],
        "workspaceId": [""],
        "folderId": [""]
    })
    pro_items_df = pd.concat([pro_items_df, workspace_row], ignore_index=True)

    # Request the DEV variable library definition
    print(f"*INFO*: ▶️ Requesting variable library definition from DEV workspace...")
    get_vl_request = requests.post(f"{base_url}/workspaces/{dev_workspace_id}/VariableLibraries/{dev_vl_id}/getDefinition", headers=fab_headers)
    
    # Raise error if the request has not been registered
    if get_vl_request.status_code != 202:
        raise ValueError(f"*ERROR*: ❌ Error requesting variable library definition. Status code: {get_vl_request.status_code}, Message: {get_vl_request.text}")
    
    try:
        # Wait for the request to be processed using the Retry-After value
        wait = int(get_vl_request.headers['Retry-After']) + 1
        print (f"*INFO*: Waiting {wait} seconds for the variable library definition request to be processed...")
        time.sleep(wait)
    except Exception as e:
        print(f"*INFO*: ℹ️ No wait time provided.")

    # Get the DEV variable library definition
    dev_vl_definition_request = requests.get(f"{get_vl_request.headers['Location']}/result", headers=fab_headers)

    if dev_vl_definition_request.status_code != 200:
        raise ValueError(f"*ERROR*: ❌ Error retrieving variable library definition. Status code: {dev_vl_definition_request.status_code}, Message: {dev_vl_definition_request.text}")
    
    try:
        # Process the variable library definition
        dev_vl_definition = dev_vl_definition_request.json()
        dev_variables = json.loads(base64.b64decode(dev_vl_definition['definition']['parts'][0]['payload']))['variables']
        print(f"*INFO*: ✅ Retrieved variable library definition from DEV workspace.")
    except Exception as e:
        raise ValueError(f"*ERROR*: ❌ Error processing variable library definition. Message: {str(e)}")

    try:
        # Replace GUIDs in the DEV variable library with the corresponding IDs from the PRO workspace
        print(f"*INFO*: ▶️ Replacing GUIDs in DEV variable library with corresponding IDs from PRO workspace...")

        if len(dev_variables) > 0:
        
            for variable in dev_variables:

                if variable['type'] == "Guid":
                    variable_name = variable['name']
                    print(f"*INFO*: ▶️ Replacing variable '{variable_name}' value with PRO item ID...")

                    values = pro_items_df[pro_items_df['displayName']==variable_name]['id']

                    # If a corresponding item is found in the PRO workspace, update the variable value
                    if values.size > 0:
                        pro_item_id = values.item()
                        variable['value'] = pro_item_id
                        print(f"*INFO*: ✅ Assigned corresponding PRO item ID: {pro_item_id} for variable: {variable_name}")
            
            # Update the base64 encoded payload in the DEV variable library definition using the updated variables
            payload = {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/variableLibrary/definition/variables/1.0.0/schema.json",
                "variables": dev_variables
            }
            
            dev_vl_definition['definition']['parts'][0]['payload'] = base64.b64encode(json.dumps(payload, indent=4).encode('utf-8')).decode('utf-8')
            print(f"*INFO*: ✅ Created new payload.")
    except Exception as e:
         raise ValueError(f"*ERROR*: ❌ Unable to update the payload in the DEV variable library definition. Message: {str(e)}")
    
    # Update the variable library definition in the PRO workspace
    print(f"*INFO*: ▶️ Updating variable library definition in PRO workspace...")

    update_vl_definition = requests.post(f"{base_url}/workspaces/{pro_workspace_id}/VariableLibraries/{pro_vl_id}/updateDefinition?updateMetadata=True", headers=fab_headers, json=dev_vl_definition)

    if update_vl_definition.status_code != 202:
        raise ValueError(f"*ERROR*: ❌ Error updating variable library definition in PRO workspace.")

    print(f"*INFO*: ✅ Updated variable library definition in PRO workspace.")

if __name__ == "__main__":
    main()