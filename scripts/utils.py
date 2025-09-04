import subprocess

def run_fab_command(command: str):

    """
    Runs a Fabric CLI command and returns the output.
    
    Parameters:
        command (str): The Fabric CLI command to run.
    Returns:
        None
    """

    # Run Fabric CLI command
    result = subprocess.run(
        ["fab", "-c", command], capture_output=True, text=True
    )
    
    return result.stdout.strip()

def get_id(workspace_name: str, artifact_name: str, type: str) -> str:
    """
    Retrieves the artifact ID.
    
    Parameters:
        workspace_name (str): The name of the workspace.
        artifact_name (str): The name of the artifact.
        type (str): The type of the artifact (e.g., Workspace, SQLDatabase, Lakehouse).
    Returns:
        str: The ID of the artifact.
    """
    
    # Get artifact ID
    id = run_fab_command(f"get /{workspace_name}.Workspace/{artifact_name} -q id")
    return id

def add_users_to_artifact(
        artifact_name: str,
        artifact_type: str,
        upns: list,
        role: str,
        command_prefix: str = ""
):
    """
    Adds users to an artifact with a specified role.
    
    Parameters:
        artifact_name (str): The name of the artifact.
        artifact_type (str): The type of the artifact (e.g., Workspace, Connection).
        upns (list): A list of user principal names (UPNs) to add.
        role (str): The role to assign to the users (e.g., admin).
        command_prefix (str, optional): Extra information to run the command.
    Returns:
        None
    """

    # Add users to artifact
    if len(upns) > 0:
        
        print(f"*INFO*: ▶️ Adding users to artifact '{artifact_name}'.")
        
        for upn in upns:
            run_fab_command(
                f"acl set -f {command_prefix}/{artifact_name}.{artifact_type} -I {upn} -R {role}"
            )
        print(f"*INFO*: ✅ Added '{upns}' as '{role}' users to artifact '{artifact_name}'.")


def create_workspace(workspace_name: str, capacity_name: str, upns: list = None) -> str:
    """
    Creates a new Fabric workspace.
    
    Parameters:
        workspace_name (str): The name of the workspace to create.
        capacity_name (str): The name of the capacity to associate with the workspace.
    Returns:
        None
    """

    # Check if workspace already exists
    exists = run_fab_command(f"exists {workspace_name}.Workspace")
    print(f"*INFO*: ▶️ The workspace '{workspace_name}' exists: {exists}.")
    
    if exists == "* false":

        # Create workspace
        print(f"*INFO*: ▶️ Creating workspace '{workspace_name} in the capacity '{capacity_name}'.")

        run_fab_command(
            f"create /{workspace_name}.Workspace -P capacityName={capacity_name}"
        )

        print(f"*INFO*: ✅ Workspace '{workspace_name}' created with ID: {workspace_id}")

        # Add users to workspace
        if upns:

            add_users_to_artifact(
                artifact_name=workspace_name,
                artifact_type="Workspace",
                upns=upns,
                role="admin"
            )
        
        # Get workspace ID
        workspace_id = run_fab_command(
            f"get /{workspace_name}.Workspace -q id"
        )
        
        return workspace_id