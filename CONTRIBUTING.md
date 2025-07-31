# Contributing to AlgoKit Templates

First off, thank you for considering contributing to AlgoKit Templates! It's people like you that make the Algorand developer community great. This document provides guidelines for contributing to this repository.

For information on getting started with the repository and understanding its structure, please see the main [README.md](README.md).

## Making Contributions

We welcome contributions of all kinds, from fixing typos to adding new features.

## Code Contributions

* **Fork and Clone**: Follow the instructions in the "Getting Started" section of the [README.md](README.md).
* **Branching**: Create a new branch for your changes. Use the following branching naming conventions:
* **Feature branches**: `feature/description-of-feature` such as a new template or example
* **Bug fixes**: `fix/description-of-fix`
* **Documentation**: `docs/description-of-update`
* **Example branches**: `examples/example-id` (the prefix is reserved and auto-generated. DON'T MANUALLY CREATE A BRANCH WITH THE `examples/` PREFIX)
* **Temporary branches**: `tmp/example-id` (for codespaces)

    ```bash
    git checkout -b feature/your-feature-name
    ```

* **Coding Standards**: Please adhere to the coding style of the existing codebase. For Python, we follow PEP 8.
* **Pre-commit Hooks**: This project uses [pre-commit](https://pre-commit.com/) to ensure code quality. After setting up your development environment, install the pre-commit hooks:

    ```bash
    pre-commit install  # Auto-invoke hooks on each commit
    ```

    You can also run pre-commit manually on all files:

    ```bash
    pre-commit run --all-files  # Run manually on all files
    ```

* **Commit Messages**: We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification. This helps in maintaining a clear and automated commit history.
* **Testing**: Before submitting a pull request, please ensure your changes are well-tested. If you modify a template, regenerate the corresponding example(s) and verify that they are correct and functional.

    ```bash
    make generate-new-examples id=<your-changed-example-id>
    # Manually inspect and test the output in examples/<your-changed-example-id>
    ```

    Also run the validation script:

    ```bash
    make validate-example-configuration
    ```

* **Pull Request**: Once you are ready, push your branch to your fork and open a pull request against the `main` branch of the original repository. Provide a clear description of your changes in the PR.

## Updating Documentation

Documentation is just as important as code.

* **When to Update**: If you are adding a new feature, changing the behavior of an existing one, or deprecating something, please update the documentation.
* **Style**: Write in a clear and concise manner. Use Markdown for formatting.
* **Previewing**: You can use any standard Markdown preview tool to check your changes before committing.
* **Which Files to Update**:
  * For changes to the contribution process, update this file (`CONTRIBUTING.md`).
  * For changes to the overall project, update the main `README.md`.
  * If you are adding or modifying a template, consider adding or updating a `README.md` within that template directory.

## Releases

This repository uses automated releases with semantic versioning:

* **Beta Releases**: Automatically created when changes are merged to the `main` branch. These include a `-beta` suffix for testing and development.
* **Stable Releases**: Manually triggered by maintainers by running the "Release" workflow from the GitHub Actions tab, which creates production-ready releases without the beta suffix.

The release process uses [Python Semantic Release](https://python-semantic-release.readthedocs.io/) with [Conventional Commits](https://www.conventionalcommits.org/), so following the commit message format mentioned above ensures proper version bumping and changelog generation.

As a contributor, you don't need to worry about releases - they are handled automatically by the CI/CD pipeline.

Thank you for contributing!
