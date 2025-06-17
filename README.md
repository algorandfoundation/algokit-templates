# AlgoKit Templates

Templates for initialize algokit projects and examples for the example gallery.

## Getting Started

### Setting up Your Development Environment

To get started with developing and contributing to AlgoKit Templates, you'll need to set up your local development environment. This project uses Python and `uv` for dependency management.****

1. **Prerequisites**:
    * Ensure you have Python 3.12 or higher installed.
    * We use [`uv`](https://github.com/astral-sh/uv) for fast package management. You can install it by following the [official instructions](https://docs.astral.sh/uv/getting-started/installation/).
    * [Git](https://git-scm.com/) for version control.
    * The [GitHub CLI](https://cli.github.com/) (`gh`) is required for some `Makefile` commands like `create-codespace`.

2. **Fork and Clone the Repository**:
    First, fork the repository to your own GitHub account and then clone it to your local machine:

    ```bash
    git clone https://github.com/YOUR_USERNAME/algokit-templates.git
    cd algokit-templates
    ```

3. **Set up Virtual Environment, Install Dependencies, Activate `venv`**:
    Create a virtual environment and install the project dependencies using `uv`.

    ```bash
    uv sync
    ```

    Now you are ready to start making changes!

## Understanding the Repository

### `examples.yml` Configuration File

The `examples/examples.yml` file is the heart of this repository. It defines the composition of each example template that users can generate. Each entry in this file represents a unique example.

Here's a breakdown of the configuration for a single example:

```yaml
- id: python-smart-contract
  project_name: "Python Hello World"
  type: "smart-contract"
  author: "Algorand Foundation"
  title: "Python Hello World"
  description: "..."
  readmeLocation: contracts
  tags:
    - python
    - smart-contract
  features:
    - "String Handling"
  detailsPages:
    smartContract: examples/python-smart-contract/projects/python-hello-world-contracts/smart_contracts/hello_world/contract.py
  templates:
    - source: "templates/base/workspace-setup"
    - source: "templates/base/contracts/python"
    - source: "generators/create-devcontainer"
```

The properties with 🌐 are used in the website [AlgoKit Examples gallery](https://github.com/algorandfoundation/algokit-example-gallery) and not in the generation of the examples themselves.

* 🌐 `id`: A unique identifier for the example. This is used in `Makefile` commands.
* 🌐 `project_name`: The default name for the project generated from this template.
* 🌐 `type`: The type of project (e.g., `smart-contract`, `frontend`, `fullstack`).
* 🌐 `author`: The author of the template.
* 🌐 `title`: A human-readable title for the example.
* 🌐 `description`: A short description of what the example does.
* 🌐 `tags`: A list of tags to categorize the example.
* 🌐 `features`: A list of key features provided by the example.
* 🌐 `detailsPages`: Links to key files within the generated example for easy access. The README will get rendered by default. Additional pages like the locations of the smart contract or notebook to render could be added. This is a key-value pair whose key  in `camelCase` turns into `Camel Case` and the title of the tab in the example details page.
* `templates`: This is a crucial section. It lists the template sources that will be sequentially combined to create the final example. These can be directories within the `templates/` folder or generator scripts from the `generators/` folder. You can also pass data to the templates using a `data` key.

### Repository Structure

The repository is organized into several key directories:

* `.github/`: Contains GitHub Actions workflows for continuous integration and other automation.
* `examples/`: This directory is where generated examples are placed. It also contains `examples.yml`, the main configuration file for all examples. The contents of this directory are git-ignored except for `examples.yml`.
* `scripts/`: Holds Python scripts that are used by the `Makefile` to manage examples. Key scripts include `create_examples.py` and `bootstrap_examples.py`.
* `templates/`: This is where the modular `cookiecutter` templates reside. The structure is as follows:
  * `templates/base/`: Contains foundational templates for different project types (e.g., `contracts/`, `frontend/`).
  * `templates/examples/`: Contains templates specific to certain examples.
* `Makefile`: Provides a convenient set of commands for common tasks like creating, cleaning, and managing examples.
* `pyproject.toml`: The standard Python project file. It defines project metadata and dependencies for the scripts that manage the templates.

### Managing Auto-Generated Examples

The `Makefile` is your primary tool for working with examples. Here are some of the most common commands:

* **Generate a specific example**:
    To generate a single example, use the `create-examples` target with the `id` of the example from `examples.yml`.

    ```bash
    make create-examples id=python-smart-contract
    ```

* **Generate all examples**:

    ```bash
    make create-examples
    ```

* **Clean examples**:
    To remove all generated examples:

    ```bash
    make clean-examples
    ```

    To remove a specific example:

    ```bash
    make clean-examples id=python-smart-contract
    ```

* **Regenerate examples**:
    To clean and then regenerate examples, you can chain the commands or use `generate-new-examples`:

    ```bash
    make generate-new-examples id=python-smart-contract
    ```

These commands automate the process of using the `scripts/create_examples.py` script, which reads `examples.yml` and generates the projects in the `examples/` directory.

### Developing a new example

Creating a new example involves adding a new entry to `examples/examples.yml` and defining the sequence of templates that compose it. This allows for a modular and reusable way to build examples.

The process is as follows:

1. **Define the example in `examples.yml`**: Add a new item to the list in `examples.yml`. Fill in the metadata like `id`, `project_name`, `title`, `description`, etc.

2. **Compose templates**: The `templates` property is a list of sources that are layered on top of each other to create the final project. The order is important. As shown in `examples.yml`, the process is to:
    * **Start with a base template**: Choose one or more foundational templates from the `templates/base/` directory. For instance, `templates/base/workspace-setup` is a good starting point for most projects.
    * **Add an example-specific template**: Add a template from `templates/examples/` that contains the specific logic or files for your example.
    * **Include generators**: Add any necessary generators from the `generators/` directory. These are scripts that can programmatically add or modify files, for example, creating a `.devcontainer` configuration.

3. **Generate and test**: Once you have defined your example, you can generate it using the `Makefile` commands described earlier, for example:

    ```bash
    make generate-new-examples id=<your-example-id>
    ```

#### Testing Your Example

The `Makefile` provides targets to help with testing and sharing your new example.

* **`make push-example`**: This command pushes your generated example to a new branch on GitHub. This is useful for sharing the example or for CI/CD processes. It requires an `id`.

    ```bash
    make push-example id=<your-example-id>
    ```

* **`make create-codespace`**: This command is particularly useful for testing the development container environment for your example. It creates a temporary branch with your example's files at the root and then launches a GitHub Codespace. This allows you to test the dev container and other environment setup without needing to go through the `algokit-examples-gallery`, which is useful for testing container scripts for example.

    ```bash
    make create-codespace id=<your-example-id>
    ```

## Contributing

We welcome contributions to AlgoKit Templates! Please see our [Contributing Guide](CONTRIBUTING.md) for detailed information on how to contribute, including development guidelines, coding standards, and the contribution process.
