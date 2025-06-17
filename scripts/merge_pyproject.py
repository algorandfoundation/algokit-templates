import tomli
import tomli_w
from pathlib import Path
import fire  # type: ignore[import-untyped]
from typing import Dict


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


def merge_pyproject(
    source: str = ".", destination: str = ".", overwrite_existing_only: bool = False
) -> None:
    """
    Merge dependencies from source pyproject.toml to destination pyproject.toml.

    Args:
        source: Path to source directory containing pyproject.toml
        destination: Path to destination directory containing pyproject.toml
        overwrite_existing_only: If True, only overwrite dependencies that already exist in destination
    """
    source_path = Path(source)
    dest_path = Path(destination)
    print(f"Merging pyproject.toml dependencies from {source_path} to {dest_path}")

    # Ensure source exists and is a directory
    if not source_path.exists():
        raise ValueError(f"Source directory '{source}' does not exist")
    if not source_path.is_dir():
        raise ValueError(f"Source path '{source}' is not a directory")

    # Create destination if it doesn't exist
    dest_path.mkdir(parents=True, exist_ok=True)

    # Handle pyproject.toml
    source_pyproject = source_path / "pyproject.toml"
    dest_pyproject = dest_path / "pyproject.toml"

    if source_pyproject.exists():
        source_deps = tomli.loads(source_pyproject.read_text())
        if dest_pyproject.exists():
            dest_deps = tomli.loads(dest_pyproject.read_text())
            print(f"Merging dependencies from {source_pyproject} to {dest_pyproject}")
            merged_deps = merge_pyproject_dependencies(
                source_deps, dest_deps, overwrite_existing_only
            )
            dest_pyproject.write_text(tomli_w.dumps(merged_deps))
        else:
            if not overwrite_existing_only:
                print(f"Creating new pyproject.toml at {dest_pyproject}")
                dest_pyproject.write_text(tomli_w.dumps(source_deps))
            else:
                print(
                    "Destination pyproject.toml doesn't exist and overwrite_existing_only is True. Skipping."
                )
    else:
        print(f"Source pyproject.toml not found at {source_pyproject}")


if __name__ == "__main__":
    fire.Fire(merge_pyproject)
