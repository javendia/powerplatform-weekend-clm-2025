import os
from utils import *

CAPACITY_NAME = os.getenv("FAB_CAPACITY")
WORKSPACE_NAME = os.getenv("WORKSPACE_NAME")
FAB_ADMIN_UPNS = os.getenv("FAB_ADMIN_UPNS")

if FAB_ADMIN_UPNS:
    FAB_ADMIN_UPNS = [upn.strip() for upn in FAB_ADMIN_UPNS.split(",")]

# Create workspace
workspace_id = create_workspace(
    workspace_name=WORKSPACE_NAME,
    capacity_name=CAPACITY_NAME,
    upns=FAB_ADMIN_UPNS
)

# Set the workspace ID as an environment variable for GitHub Actions
echo_statement="echo \"CONTROL_WORKSPACE_ID=" + workspace_id + "\" >> $GITHUB_ENV"
os.system(echo_statement)