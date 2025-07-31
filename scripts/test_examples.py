import subprocess
import logging
from pathlib import Path

import pytest

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("test_examples.log")],
)
logger = logging.getLogger(__name__)

BOOTSTRAP_TIMEOUT = 180
COMMAND_TIMEOUT = 300
COMMANDS = ["build", "lint", "test"]


def get_example_folders() -> list[str]:
    """Return directory names from the examples folder."""
    examples_dir = Path(__file__).parent.parent / "examples"
    logger.info(f"Scanning examples directory: {examples_dir}")

    folders = [
        folder.name
        for folder in examples_dir.iterdir()
        if folder.is_dir() and not folder.name.startswith(".")
    ]

    logger.info(f"Found {len(folders)} example folders: {folders}")
    return folders


def _run_command(
    cmd: list[str],
    cwd: Path,
    timeout: int,
    env_overrides: dict[str, str] | None = None,
    env_removals: list[str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run subprocess command with error handling and comprehensive logging."""
    cmd_str = " ".join(cmd)
    logger.info(f"Executing command: {cmd_str} in directory: {cwd}")

    # Prepare environment variables
    import os

    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)
    if env_removals:
        for key in env_removals:
            env.pop(key, None)

    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            env=env,
        )

        # Log command completion details
        logger.info(f"Command completed with return code: {result.returncode}")

        # Always log stdout and stderr for debugging purposes
        if result.stdout:
            logger.debug(f"STDOUT for '{cmd_str}':\n{result.stdout}")
        if result.stderr:
            logger.debug(f"STDERR for '{cmd_str}':\n{result.stderr}")

        # Log warning if command failed but didn't raise exception
        if result.returncode != 0:
            logger.warning(
                f"Command '{cmd_str}' failed with return code {result.returncode}"
            )

        return result

    except subprocess.TimeoutExpired as e:
        logger.error(
            f"Command '{cmd_str}' timed out after {timeout} seconds in {cwd.name}"
        )
        logger.error(f"Timeout details: {e}")
        pytest.fail(f"Command {cmd_str} timed out in {cwd.name}")
    except FileNotFoundError as e:
        logger.error(f"Command not found: {cmd_str}")
        logger.error(f"FileNotFoundError details: {e}")
        pytest.fail(
            "algokit command not found. Ensure algokit is installed and in PATH."
        )
    except Exception as e:
        logger.error(f"Unexpected error running command '{cmd_str}': {e}")
        logger.error(f"Exception type: {type(e).__name__}")
        raise


@pytest.mark.parametrize("example_folder", get_example_folders())
def test_example_commands(example_folder: str) -> None:
    """Test algokit commands run successfully in example folders."""
    logger.info(f"Starting test for example folder: {example_folder}")

    examples_dir = Path(__file__).parent.parent / "examples"
    example_path = examples_dir / example_folder

    assert example_path.exists() and example_path.is_dir()
    logger.debug(f"Confirmed example path exists: {example_path}")

    # Bootstrap command
    logger.info(f"Running bootstrap command for {example_folder}")
    bootstrap_result = _run_command(
        ["algokit", "-v", "project", "bootstrap", "all"],
        example_path,
        BOOTSTRAP_TIMEOUT,
        env_removals=["CI"],
    )

    if bootstrap_result.returncode != 0:
        error_msg = (
            f"Command 'algokit project bootstrap all' failed in {example_folder}\n"
            f"Return code: {bootstrap_result.returncode}\n"
            f"STDOUT: {bootstrap_result.stdout}\n"
            f"STDERR: {bootstrap_result.stderr}"
        )
        logger.error(error_msg)
        pytest.fail(error_msg)
    else:
        logger.info(f"Bootstrap completed successfully for {example_folder}")

    # Test individual commands
    for command in COMMANDS:
        logger.info(f"Running '{command}' command for {example_folder}")
        result = _run_command(
            ["algokit", "-v", "project", "run", command], example_path, COMMAND_TIMEOUT
        )

        if "No such command" in result.stderr:
            logger.info(
                f"Command 'algokit project run {command}' not found in {example_folder}, skipping..."
            )
            print(
                f"Command 'algokit project run {command}' not found in {example_folder}, skipping..."
            )
            continue

        if result.returncode != 0:
            error_msg = (
                f"Command 'algokit project run {command}' failed in {example_folder}\n"
                f"Return code: {result.returncode}\n"
                f"STDOUT: {result.stdout}\n"
                f"STDERR: {result.stderr}"
            )
            logger.error(error_msg)
            pytest.fail(error_msg)
        else:
            logger.info(
                f"Command '{command}' completed successfully for {example_folder}"
            )

    logger.info(f"All tests completed successfully for {example_folder}")


if __name__ == "__main__":
    logger.info("Starting example folder tests")
    folders = get_example_folders()
    print(f"Found {len(folders)} example folders to test:")
    for folder in folders:
        print(f"  - {folder}")
    logger.info("Example folder discovery completed")
