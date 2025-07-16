# Jupyter Notebook for AlgoKit Utils Python

This directory contains template files for creating Python-based Algorand scripts using AlgoKit.

## Contents

- **algokit.toml.jinja**: Configuration template for AlgoKit projects
- **pyproject.toml**: Python project dependencies and configuration
- **poetry.toml**: Poetry configuration (uses in-project virtualenvs)
- **algokit-utils.ipynb**: Jupyter notebook example demonstrating AlgoKit Utils usage


## Requirements

- Python 3.12+
- Poetry (for dependency management)
- AlgoKit CLI v2.0.0+

## Getting Started

This template provides the foundation for creating Python scripts that interact with the Algorand blockchain using AlgoKit Utils. The included Jupyter notebook demonstrates how to configure AlgoKit, load environment variables, and execute transactions.

### Installation and Running

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Start the AlgoKit localnet:
   ```bash
   algokit localnet start
   ```

3. Open the notebook using one of these options:
   - **Option 1**: Run Jupyter Notebook directly
     ```bash
     jupyter notebook
     ```
   - **Option 2**: Open in VS Code with the Jupyter extension
     ```bash
     code .
     ```
     Then open the `.ipynb` file and use the VS Code Jupyter extension to run it.

## Dependencies

- algokit-utils: Core utilities for Algorand development
- jupyter: Support for interactive notebook development
- dotenv: Environment variable management