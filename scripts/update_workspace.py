import json
from pathlib import Path


def update_workspace(workspace_path: str, folder_path: str) -> None:
    """
    Update VS Code workspace file by adding a new folder to it.

    Args:
        workspace_path (str): Absolute path to the workspace file
        destination_path (str): Absolute path to the folder to be added
    """
    # Convert paths to Path objects and resolve to absolute paths
    workspace_file = Path(workspace_path).resolve()

    # Verify workspace file exists
    if not workspace_file.exists():
        raise FileNotFoundError(f"Workspace file not found: {workspace_file}")

    # Load the workspace file
    with open(workspace_file, "r") as f:
        workspace_data = json.load(f)

    # Add folder if it doesn't exist
    # if not any(folder.get("path") == str(rel_path) for folder in workspace_data["folders"]):
    workspace_data["folders"].append({"path": str(folder_path)})

    # Write back the updated workspace file
    with open(workspace_file, "w") as f:
        json.dump(workspace_data, f, indent=2)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print(
            "Usage: python update_workspace.py <workspace_file_path> <destination_folder_path>"
        )
        sys.exit(1)

    update_workspace(sys.argv[1], sys.argv[2])
