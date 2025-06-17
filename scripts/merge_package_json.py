import json
from pathlib import Path
import fire  # type: ignore[import-untyped]
from typing import Dict


def merge_json_dependencies(
    source: Dict, destination: Dict, overwrite_existing_only: bool = False
) -> Dict:
    """
    Merge dependencies and scripts from source into destination package.json,
    preserving all destination fields and structure.
    Source entries take precedence over destination entries.

    Args:
        source: Source dictionary
        destination: Destination dictionary
        overwrite_existing_only: If True, only overwrite entries that already exist in destination
    """
    result = destination.copy()

    # Merge dependencies and devDependencies
    for dep_type in ["dependencies", "devDependencies"]:
        if dep_type in source and dep_type in result:
            source_deps = source[dep_type]
            for dep_name, dep_version in source_deps.items():
                if not overwrite_existing_only or dep_name in result[dep_type]:
                    result[dep_type][dep_name] = dep_version
        elif dep_type in source and not overwrite_existing_only:
            # Only add new dep_type if overwrite_existing_only is False
            result[dep_type] = source[dep_type].copy()

    # Merge scripts
    if "scripts" in source:
        if "scripts" not in result:
            result["scripts"] = {}
        source_scripts = source["scripts"]
        for script_name, script_command in source_scripts.items():
            if not overwrite_existing_only or script_name in result["scripts"]:
                result["scripts"][script_name] = script_command

    return result


def merge_package_json(
    source: str = ".", destination: str = ".", overwrite_existing_only: bool = False
) -> None:
    """
    Merge dependencies from source package.json to destination package.json.

    Args:
        source: Path to source directory containing package.json
        destination: Path to destination directory containing package.json
        overwrite_existing_only: If True, only overwrite dependencies that already exist in destination
    """
    source_path = Path(source)
    dest_path = Path(destination)
    print(f"Merging package.json dependencies from {source_path} to {dest_path}")

    # Ensure source exists and is a directory
    if not source_path.exists():
        raise ValueError(f"Source directory '{source}' does not exist")
    if not source_path.is_dir():
        raise ValueError(f"Source path '{source}' is not a directory")

    # Create destination if it doesn't exist
    dest_path.mkdir(parents=True, exist_ok=True)

    # Handle package.json
    source_package = source_path / "package.json"
    dest_package = dest_path / "package.json"

    if source_package.exists():
        source_deps = json.loads(source_package.read_text())
        if dest_package.exists():
            dest_deps = json.loads(dest_package.read_text())
            print(f"Merging dependencies from {source_package} to {dest_package}")
            merged_deps = merge_json_dependencies(
                source_deps, dest_deps, overwrite_existing_only
            )
            dest_package.write_text(json.dumps(merged_deps, indent=2))
        else:
            if not overwrite_existing_only:
                print(f"Creating new package.json at {dest_package}")
                dest_package.write_text(json.dumps(source_deps, indent=2))
            else:
                print(
                    "Destination package.json doesn't exist and overwrite_existing_only is True. Skipping."
                )
    else:
        print(f"Source package.json not found at {source_package}")


if __name__ == "__main__":
    fire.Fire(merge_package_json)
