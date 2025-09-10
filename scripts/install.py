import os
from utils import *

def main():
    # Read required environment variables
    capacity_name = os.getenv("FAB_CAPACITY").strip()
    workspace_name = os.getenv("WORKSPACE_NAME").strip()
    fab_admin_upns = os.getenv("FAB_ADMIN_UPNS").strip()

    # Validate required variables
    if not capacity_name:
        raise ValueError("*ERROR*: ❌ FAB_CAPACITY environment variable is not set.")
    if not workspace_name:
        raise ValueError("*ERROR*: ❌ PRO_WORKSPACE_NAME environment variable is not set.")
    
    # Define workspace names
    dev_workspace_name = f"{workspace_name}_DEV"
    pro_workspace_name = f"{workspace_name}_PRO"
    
    # Prepare list of UPNs if provided
    upns = None
    if fab_admin_upns:
        upns = [upn.strip() for upn in fab_admin_upns.split(",")]

    # Get DEV workspace ID
    dev_workspace_id = run_fab_command(f"get /{dev_workspace_name}.Workspace -q id")
    print(f"*INFO*: ℹ️ DEV Workspace ID: {dev_workspace_id}")

    # Set the DEV workspace ID as an environment variable for GitHub Actions
    echo_statement = f"echo \"DEV_WORKSPACE_ID={dev_workspace_id}\" >> $GITHUB_ENV"
    os.system(echo_statement)

    # Create PRO workspace
    pro_workspace_id = create_workspace(
        workspace_name=pro_workspace_name,
        capacity_name=capacity_name,
        upns=upns
    )

    # Set the PRO workspace ID as an environment variable for GitHub Actions
    echo_statement = f"echo \"PRO_WORKSPACE_ID={pro_workspace_id}\" >> $GITHUB_ENV"
    os.system(echo_statement)

if __name__ == "__main__":
    main()