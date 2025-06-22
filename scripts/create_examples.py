import os
import fire  # type: ignore[import-untyped]
import yaml
from pathlib import Path
from copier import run_copy
import json
from typing import Dict, Optional, Any
from update_workspace import update_workspace
from bootstrap_examples import bootstrap_example

BACKEND_TEMPLATES_NAME = "contracts"
FRONTEND_TEMPLATES_NAME = "frontend"


def load_examples_config() -> Dict[str, Any]:
    file_path = Path(__file__).parent.parent / "examples" / "examples.yml"
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def get_template_type(path: Path) -> Optional[str]:
    template_type = "example"
    path_str = str(path)
    if path_str.startswith("templates/base/workspace"):
        template_type = "workspace"
    elif path_str.startswith(f"templates/base/{BACKEND_TEMPLATES_NAME}"):
        template_type = BACKEND_TEMPLATES_NAME
    elif path_str.startswith(f"templates/base/{FRONTEND_TEMPLATES_NAME}"):
        template_type = FRONTEND_TEMPLATES_NAME
    return template_type


def read_workspace_config(workspace_file: Path | None) -> Dict[str, Any]:
    """
    Read the workspace file and extract configuration values.

    Args:
        workspace_file (Path): Path to the workspace file

    Returns:
        dict: Dictionary containing workspace configuration values including:
            - projects_root_path: Base path for projects
            - projects: Dictionary mapping project names to their paths
    """
    config: Dict[str, Any] = {"projects_root_path": None, "projects": {}}

    if workspace_file and workspace_file.exists():
        with open(workspace_file, "r") as f:
            workspace_data = json.loads(f.read())
            files_exclude = workspace_data.get("settings", {}).get("files.exclude", {})
            # Get the first key that ends with '/'
            projects_root_path = next(
                (path for path in files_exclude.keys() if path.endswith("/")), None
            )
            if projects_root_path:
                config["projects_root_path"] = projects_root_path.rstrip("/")

            # Extract project folders from workspace folders
            if "folders" in workspace_data:
                for folder in workspace_data["folders"]:
                    if "path" in folder:
                        if folder["path"].endswith(BACKEND_TEMPLATES_NAME):
                            config["projects"][BACKEND_TEMPLATES_NAME] = folder["path"]
                        elif folder["path"].endswith(FRONTEND_TEMPLATES_NAME):
                            config["projects"][FRONTEND_TEMPLATES_NAME] = folder["path"]
                        else:
                            config["projects"]["root"] = folder["path"]

    return config


def has_workspace(base_path: Path) -> tuple[bool, Optional[Path]]:
    """
    Check if a workspace file exists in the given path and return it.

    Args:
        base_path (Path): Path to search for workspace files

    Returns:
        tuple: (is_workspace, workspace_file) where:
            - is_workspace (bool): True if a workspace file exists
            - workspace_file (Optional[Path]): Path to the workspace file if found, None otherwise
    """
    workspace_file = next(base_path.glob("*.code-workspace"), None)
    is_workspace = bool(workspace_file)
    return is_workspace, workspace_file


def update_base_template_data(
    template: Dict[str, Any],
    base_destination_path: Path,
    project_name: str,
    project_type: str,
) -> Dict[str, Any]:
    template["destination"] = base_destination_path
    use_workspace, workspace_file = has_workspace(base_destination_path)

    # Manually add data to template data for the copier answers
    template_data = template.get("data", {})
    template_data["use_workspace"] = use_workspace
    if not template_data.get("project_name"):
        template_data["project_name"] = project_name
    template["data"] = template_data

    if use_workspace and project_type in [
        BACKEND_TEMPLATES_NAME,
        FRONTEND_TEMPLATES_NAME,
    ]:
        workspace_config = read_workspace_config(workspace_file)
        projects_root_path = workspace_config["projects_root_path"]
        project_dir_name = f"{project_name}-{project_type}"
        template["destination"] = (
            base_destination_path / projects_root_path / project_dir_name
        )
        projects_path = os.path.join(projects_root_path, project_dir_name)
        # Update workspace file with the new project folder
        update_workspace(str(workspace_file), str(projects_path))

    return template


def update_example_template_data(
    template: Dict[str, Any],
    base_destination_path: Path,
    project_name: str,
    project_type: str,
) -> list[Dict[str, Any]]:
    template["destination"] = base_destination_path
    use_workspace, workspace_file = has_workspace(base_destination_path)

    if use_workspace and project_type in [
        BACKEND_TEMPLATES_NAME,
        FRONTEND_TEMPLATES_NAME,
    ]:
        workspace_config = read_workspace_config(workspace_file)
        projects_root_path = workspace_config["projects_root_path"]
        project_dir_name = f"{project_name}-{project_type}"
        template["destination"] = (
            base_destination_path / projects_root_path / project_dir_name
        )
        return [template]
    elif project_type == "fullstack":
        # For fullstack examples, deploy to both contracts and frontend destinations
        use_workspace, workspace_file = has_workspace(base_destination_path)
        workspace_config = (
            read_workspace_config(workspace_file) if use_workspace else {}
        )
        framework_choice = template.get("data", {}).get("framework_choice", "python")

        templates = []
        if BACKEND_TEMPLATES_NAME in workspace_config["projects"]:
            contracts_template = template.copy()
            contracts_folder_path = (
                Path(contracts_template["source"])
                / f"{framework_choice}_template_content"
                / "contracts"
            )

            # If the contracts folder exists, use it as the subdirectory
            # If not, don't run the copier on the contracts template
            if contracts_folder_path.exists():
                relative_contracts_folder_path = contracts_folder_path.relative_to(
                    Path(contracts_template["source"])
                )
                contracts_template["data"]["subdirectory"] = str(
                    relative_contracts_folder_path
                )
                contracts_template["destination"] = (
                    base_destination_path
                    / workspace_config["projects"][BACKEND_TEMPLATES_NAME]
                )
                templates.append(contracts_template)

        if FRONTEND_TEMPLATES_NAME in workspace_config["projects"]:
            frontend_template = template.copy()
            frontend_folder_path = (
                Path(frontend_template["source"])
                / f"{framework_choice}_template_content"
                / "frontend"
            )

            # If the frontend folder exists, use it as the subdirectory
            # If not, don't run the copier on the frontend template
            if frontend_folder_path.exists():
                relative_frontend_folder_path = frontend_folder_path.relative_to(
                    Path(frontend_template["source"])
                )
                frontend_template["data"]["subdirectory"] = str(
                    relative_frontend_folder_path
                )
                frontend_template["destination"] = (
                    base_destination_path
                    / workspace_config["projects"][FRONTEND_TEMPLATES_NAME]
                )
                templates.append(frontend_template)

        return templates
    else:
        return [template]


def update_generator_env_file_template_data(
    template: Dict[str, Any],
    base_destination_path: Path,
) -> list[Dict[str, Any]]:
    template_data = template.get("data", {})
    # Get project type from template data
    project_type = template_data.get("project", "all")
    # Validate project type
    valid_project_types = ["frontend", "contracts", "all"]
    if project_type.lower() not in valid_project_types:
        print(
            f"Warning: Project type '{project_type}' is not one of {valid_project_types}"
        )
        project_type = "all"
    project_type = project_type.lower()
    # Find the destination path for the all project types
    # TODO: Consider the case where the workspace is not used
    use_workspace, workspace_file = has_workspace(base_destination_path)
    workspace_config = read_workspace_config(workspace_file) if use_workspace else {}
    if project_type == "all":
        project_paths = []
        if BACKEND_TEMPLATES_NAME in workspace_config["projects"]:
            project_paths.append(workspace_config["projects"][BACKEND_TEMPLATES_NAME])
        if FRONTEND_TEMPLATES_NAME in workspace_config["projects"]:
            project_paths.append(workspace_config["projects"][FRONTEND_TEMPLATES_NAME])
    else:
        project_paths = [
            workspace_config["projects"][project_type],
        ]
    updated_templates = []
    for project_path in project_paths:
        updated_template = template.copy()
        updated_template["destination"] = base_destination_path / project_path
        updated_templates.append(updated_template)

    return updated_templates


def run_copier_on_template(template: Dict[str, Any]) -> None:
    if "source" not in template:
        raise ValueError("Template source is required")
    if "destination" not in template:
        raise ValueError("Template destination is required")
    if "repo_root" not in template:
        raise ValueError("The repo_root, path to the root of the repo, is required.")
    source = Path(template["source"])
    template_destination = Path(template["destination"])
    # Create the parent directory if it doesn't exist
    template_destination.mkdir(parents=True, exist_ok=True)
    repo_root = template["repo_root"]
    base_destination_path = template["base_destination_path"]
    template_data = {
        **template.get("data", {}),
        "_repo_root": repo_root,
        "_base_destination_path": base_destination_path,
    }
    print(
        f"Running copier on template: {template['source']} with copier file: {source / 'copier.yml'}  "
    )
    run_copy(
        src_path=str(source.absolute()),
        dst_path=str(template_destination.absolute()),
        data=template_data,
        unsafe=True,
        quiet=False,
        overwrite=True,
        defaults=True,
    )


def create_example(example: Dict[str, Any], bootstrap: bool = False) -> None:
    project_name = example["project_name"].lower().replace(" ", "-")
    # Create destination path based on example id
    base_destination_path = Path("examples") / example["id"]

    # Remove destination if it exists
    if base_destination_path.exists():
        import shutil

        shutil.rmtree(base_destination_path)

    # Apply each template in sequence
    for template in example["templates"]:
        if "source" not in template:
            raise ValueError(
                f"Template source is required in for project {project_name}"
            )
        # Repo root is made available to the templates as a metadata field
        template["repo_root"] = str(Path(__file__).parent.parent)
        template["base_destination_path"] = str(base_destination_path.absolute())
        source = Path(template["source"])
        source_parts = list(source.parts)
        generator_type = source_parts.pop(0)

        if generator_type == "templates":
            template_type = source_parts.pop(0)
            if template_type == "base":
                project_type = source_parts.pop(0)
                processed_template = update_base_template_data(
                    template, base_destination_path, project_name, project_type
                )
                run_copier_on_template(processed_template)
            elif template_type == "examples":
                project_type = source_parts.pop(0)
                processed_templates = update_example_template_data(
                    template, base_destination_path, project_name, project_type
                )
                for processed_template in processed_templates:
                    run_copier_on_template(processed_template)
            else:
                raise ValueError(f"Invalid template type: {template_type}")

        elif generator_type == "generators":
            template["destination"] = base_destination_path
            generator_type = source_parts.pop(0)
            if generator_type == "create-devcontainer":
                templates = [template]

            elif generator_type == "create-smart-contract":
                templates = update_generator_env_file_template_data(
                    template, base_destination_path
                )

            elif generator_type == "create-env-file":
                templates = update_generator_env_file_template_data(
                    template, base_destination_path
                )

            else:
                raise ValueError(f"Invalid generator type: {generator_type}")

            for template in templates:
                run_copier_on_template(template)
        else:
            raise ValueError(f"Invalid generator type: {generator_type}")

    # Run bootstrap if flag is set
    if bootstrap:
        bootstrap_example(base_destination_path)


def main(example_id: Optional[str] = None, bootstrap: bool = False) -> None:
    """
    Create examples from templates. If example_id is provided, only that example will be created.

    Args:
        example_id (str, optional): Specific example ID to process. If None, all examples will be processed.
        bootstrap (bool, optional): Whether to run 'algokit project bootstrap all' after creating the example. Defaults to False.
    """
    config = load_examples_config()

    if example_id:
        # Process single example
        example = next(
            (ex for ex in config["examples"] if ex["id"] == example_id), None
        )
        if not example:
            print(f"No example found with ID: {example_id}")
            return
        print(f"\nProcessing example: {example['id']}")
        create_example(example, bootstrap)
        print(f"Completed: {example['id']}")
    else:
        # Process all examples
        for example in config["examples"]:
            print(f"\nProcessing example: {example['id']}")
            create_example(example, bootstrap)
            print(f"Completed: {example['id']}")


if __name__ == "__main__":
    fire.Fire(main)
