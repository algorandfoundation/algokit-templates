import subprocess
from pathlib import Path
from typing import Optional
import yaml
import fire  # type: ignore[import-untyped]


def load_examples_config():
    file_path = Path(__file__).parent.parent / "examples" / "examples.yml"
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def bootstrap_example(example_path: Path) -> None:
    """
    Run 'algokit project bootstrap all' in the specified example directory.

    Args:
        example_path (Path): Path to the example directory
    """

    print(f"Bootstrapping example at: {example_path}")
    try:
        subprocess.run(
            ["algokit", "project", "bootstrap", "all"],
            cwd=example_path,
            check=True,
        )
        print(f"Bootstrap completed successfully for: {example_path}")
    except subprocess.CalledProcessError as e:
        print(f"Bootstrap failed for {example_path}: {e}")


def bootstrap_examples(example_id: Optional[str] = None) -> None:
    """
    Bootstrap existing examples without recreating them.

    Args:
        example_id (str, optional): Specific example ID to bootstrap. If None, all examples will be bootstrapped.
    """
    config = load_examples_config()
    examples_dir = Path("examples")

    if example_id:
        # Bootstrap specific example
        example_path = examples_dir / example_id
        if example_path.exists() and example_path.is_dir():
            bootstrap_example(example_path)
        else:
            print(f"Example directory not found: {example_path}")
    else:
        # Bootstrap all examples
        for example in config["examples"]:
            example_path = examples_dir / example["id"]
            if example_path.exists() and example_path.is_dir():
                bootstrap_example(example_path)


if __name__ == "__main__":
    fire.Fire(bootstrap_examples)
