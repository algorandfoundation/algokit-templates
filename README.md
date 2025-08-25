# Smart Contract Example

Welcome to your new AlgoKit project! This is an example of a Smart Contract.

### Pre-requisites

These pre-requisites already come configured in the Github codespace, but you must have a github account to launch a codespace.

- [Python 3.12](https://www.python.org/downloads/) or later
- [Docker](https://www.docker.com/) (required for LocalNet)
- [AlgoKit CLI](https://github.com/algorandfoundation/algokit-cli#install) (2.0.0 or later)
- [Poetry](https://python-poetry.org/docs/#installation) (1.2 or later)

### Initial Setup

1. **Open the example in a Github Codespace**

   Click the **CodeSpace** button above to launch the project in a Codespace. This will launch a VM using your Github profile. This will automatically install the latest Algokit and run Localnet. The example comes pre-configured with a `.env` file that points to Localnet.

2. **Bootstrap Environment**
   You needs to install all the dependencies in order to launch the example. The Algokit CLI comes equipped with a command that installs the dependencies in each of your projects.

   ```bash
   # Install dependencies for contracts and frontend projects
   algokit project bootstrap all
   # Install dependencies for projects that use npm
   algokit project bootstrap npm
   # Install dependencies for projects that use python via poetry
   algokit project bootstrap poetry
   ```

### Development Workflow

#### Command Line

- **Build Contracts**: `algokit project run build`
- **Deploy**: `algokit project deploy localnet`

## Project Features

### Smart Contract Generation

- Use `algokit generate smart-contract` to create new contracts
- Contracts are placed in the `smart_contracts` directory
- Each contract has its own deployment configuration

### Debugging Support

- Integrated with AlgoKit AVM Debugger
- VSCode launch configurations included
- Interactive TEAL debugging available

## Tools & Technologies

- **Algorand**: Layer 1 Blockchain platform
- **AlgoKit**: Development toolkit for Algorand
- **Algorand Python**: Smart contract development in Python
- **AlgoKit Utils**: Core Algorand utilities
- **Poetry**: Python dependency management

## Project Structure

The workspace uses a `projects` directory as the default location for new projects. Each sub-project contains its own README with specific setup instructions.

## Additional Resources

- [AlgoKit Documentation](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/algokit.md)
- [Algorand Developer Portal](https://dev.algorand.co/)
- [Puya Documentation](https://algorandfoundation.github.io/puya/)
