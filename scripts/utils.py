import subprocess

def run_fab_command(command: str, skip_errors: bool = False):
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

    if not (skip_errors) and (result.returncode > 0 or result.stderr):
        raise Exception(
            f"*ERROR*: ❌ Error running fab command. exit_code: '{result.returncode}'; stderr: '{result.stderr}'"
        )
    
    return result.stdout.strip().split("\n")[-1]

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
            f"create /{workspace_name}.Workspace -P capacityName={capacity_name}",
            skip_errors=True
        )
        
    # Get workspace ID
    workspace_id = run_fab_command(
        f"get /{workspace_name}.Workspace -q id"
    )
    print(f"*INFO*: ✅ Workspace '{workspace_name}' created with ID: {workspace_id}")

    if upns is not None:

        upns = [x for x in upns if x.strip()]

        if len(upns) > 0:
            print(f"*INFO*: ▶️ Adding users to workspace '{workspace_name}'.")

            for upn in upns:
                run_fab_command(
                    f"acl set -f /{workspace_name}.Workspace -I {upn} -R admin", 
                    skip_errors=True
                )
            print(f"*INFO*: ✅ Added users as 'admin' users to workspace '{workspace_name}'.")

    return workspace_id