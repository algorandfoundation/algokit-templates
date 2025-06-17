import json
import tomli
import tomli_w
from pathlib import Path
import fire  # type: ignore[import-untyped]
from typing import Dict


def merge_json_dependencies(
    source: Dict, destination: Dict, overwrite_existing_only: bool = False
) -> Dict:
    """
    Merge dependencies from source into destination package.json,
    preserving all destination fields and structure.
    Source dependencies take precedence over destination dependencies.

    Args:
        source: Source dependency dictionary
        destination: Destination dependency dictionary
        overwrite_existing_only: If True, only overwrite dependencies that already exist in destination
    """
    result = destination.copy()

    for dep_type in ["dependencies", "devDependencies"]:
        if dep_type in source and dep_type in result:
            source_deps = source[dep_type]
            for dep_name, dep_version in source_deps.items():
                if not overwrite_existing_only or dep_name in result[dep_type]:
                    result[dep_type][dep_name] = dep_version
        elif dep_type in source and not overwrite_existing_only:
            # Only add new dep_type if overwrite_existing_only is False
            result[dep_type] = source[dep_type].copy()

    return result


def merge_pyproject_dependencies(
    source: Dict, destination: Dict, overwrite_existing_only: bool = False
) -> Dict:
    """
    Merge dependencies from source into destination pyproject.toml dependencies.
    Source dependencies will overwrite matching dependencies in destination.
    Assumes Poetry-style pyproject.toml format.

    Args:
        source: Source dependency dictionary
        destination: Destination dependency dictionary
        overwrite_existing_only: If True, only merge dependencies that already exist in destination
    """
    result = destination.copy()

    if "tool" in source and "poetry" in source["tool"]:
        source_poetry = source["tool"]["poetry"]
        if "tool" not in result:
            result["tool"] = {}
        if "poetry" not in result["tool"]:
            result["tool"]["poetry"] = {}

        # Handle main dependencies
        if "dependencies" in source_poetry:
            dest_deps = result["tool"]["poetry"].setdefault("dependencies", {})
            for dep_name, dep_version in source_poetry["dependencies"].items():
                if not overwrite_existing_only or dep_name in dest_deps:
                    dest_deps[dep_name] = dep_version

        # Handle dependency groups
        if "group" in source_poetry:
            dest_groups = result["tool"]["poetry"].setdefault("group", {})
            for group_name, group_data in source_poetry["group"].items():
                if "dependencies" in group_data:
                    if group_name not in dest_groups and not overwrite_existing_only:
                        dest_groups[group_name] = {"dependencies": {}}
                    elif group_name in dest_groups:
                        dest_group_deps = dest_groups[group_name].setdefault(
                            "dependencies", {}
                        )
                        for dep_name, dep_version in group_data["dependencies"].items():
                            if (
                                not overwrite_existing_only
                                or dep_name in dest_group_deps
                            ):
                                dest_group_deps[dep_name] = dep_version

    return result


def merge_dependencies(
    source: str = ".", destination: str = ".", overwrite_existing_only: bool = False
) -> None:
    """
    Merge dependencies from source package.json/pyproject.toml to destination files.

    Args:
        source: Path to source directory containing dependency files
        destination: Path to destination directory containing dependency files
        overwrite_existing_only: If True, only overwrite dependencies that already exist in destination
    """
    source_path = Path(source)
    dest_path = Path(destination)
    print(f"Merging dependencies from {source_path} to {dest_path}")

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
            print(f"Merging dependencies from {source_deps} to {dest_deps}")
            merged_deps = merge_json_dependencies(
                source_deps, dest_deps, overwrite_existing_only
            )
            dest_package.write_text(json.dumps(merged_deps, indent=2))

    # Handle pyproject.toml
    source_pyproject = source_path / "pyproject.toml"
    dest_pyproject = dest_path / "pyproject.toml"

    if source_pyproject.exists():
        source_deps = tomli.loads(source_pyproject.read_text())
        if dest_pyproject.exists():
            dest_deps = tomli.loads(dest_pyproject.read_text())
            merged_deps = merge_pyproject_dependencies(
                source_deps, dest_deps, overwrite_existing_only
            )
        else:
            merged_deps = source_deps if not overwrite_existing_only else {}
        dest_pyproject.write_text(tomli_w.dumps(merged_deps))


if __name__ == "__main__":
    fire.Fire(merge_dependencies)
