# Option 1 Implementation Details

This document contains detailed implementation specifications for the "Flat Generator Architecture with State in .algokit.toml" option.

## Functionality Distribution

| Functionality | CLI Repo | Templates Repo | Copier | Generator Post-Processing | Notes |
|--------------|----------|----------------|--------|---------------------------|-------|
| TUI Wizard Interface | ✓ | | | | Interactive UI for project initialization |
| CLI Command Parsing | ✓ | | | | Parse and validate user commands |
| Generator Discovery | ✓ | | | | Query available generators from templates |
| Generator Metadata | | ✓ | | | Dependencies, compatibility, descriptions |
| Template File Generation | | | ✓ | | Core file generation and templating |
| Jinja2 Template Processing | | | ✓ | | Variable substitution and conditionals |
| File Merging Strategy | | | ✓ | | Conflict resolution during file copying |
| Generator Implementation | | ✓ | | | Copier template definitions and structure |
| Post-Generation Hooks | | | | ✓ | Scripts run after template application |
| Configuration Merging | | | | ✓ | Merge configs (package.json, pyproject.toml) |
| Workflow Orchestration | ✓ | | | | Sequential application of generators |
| State Management | ✓ | | | | Track applied generators in .algokit.toml |
| Project Type Detection | ✓ | | | | Analyze existing project structure |
| Configuration Parsing | ✓ | | | | Parse YAML/TOML configuration files |
| Compatibility Checking | ✓ | | | | Validate generator combinations |
| Example Configurations | | ✓ | | | YAML files defining example projects |
| Hydrated Examples | | ✓ | | | Full example projects for app gallery |
| Dry run mode | ✓ | | | | Show changes before applying |
| Conflict Resolution UI | ✓ | | | | Handle file conflicts during generation |
| Version Management | ✓ | | | | Track generator versions in .algokit.toml |

## Repository Structure

Templates Repository:

```text
algokit-templates/
├── generators/                           # All generators (flat structure)
│   ├── workspace/                       # Creates workspace structure
│   ├── base-contracts-python/           # Python contract base
│   ├── base-contracts-typescript/       # TypeScript contract base
│   ├── base-frontend-react/             # React frontend base
│   ├── create-smart-contract/           # Create new smart contract
│   ├── testing/                         # Add testing (auto-detects type)
│   ├── linting/                         # Add linting configuration
│   ├── formatting/                      # Add code formatting
│   ├── devcontainer/                    # Add devcontainer support
│   ├── ci-cd/                           # Add CI/CD workflows
│   ├── env-file/                        # Create environment files
│   ├── example-digital-marketplace/     # Digital marketplace delta
│   └── example-hello-world/             # Hello world delta
├── examples/                            # Fully hydrated examples
│   ├── examples.yml                     # Configuration for generating examples
│   ├── python-smart-contract/           # Complete project for app gallery
│   └── digital-marketplace/             # Complete project for app gallery
└── scripts/
    └── generate-examples.py             # Build examples from configurations
```

CLI Repository:

```text
algokit-cli/
└── src/
    └── algokit/
        ├── cli/
        │   ├── project/
        │   │   ├── __init__.py
        │   │   ├── init.py              # TUI wizard implementation
        │   │   ├── add.py               # Incremental commands
        │   │   └── generate.py          # Configuration-based generation
        │   └── ...
        └── core/
            ├── project/
            │   ├── __init__.py
            │   ├── generator_registry.py # Discover available generators
            │   ├── state_manager.py      # Manage state in .algokit.toml
            │   └── compatibility.py      # Check generator compatibility
            └── ...
```

## Workflow Implementation Flows

### Workflow 1: Interactive Wizard (TUI)

There is a spike for this TUI [on GitHub](https://github.com/lempira/template-gallery-spike). Look at the end for a video of the TUI.

```text
CLI Repo                          Templates Repo
--------                          --------------
TUI Wizard -----------------> Query generators/*/copier.yaml
    |                              |
Present feature choices            v
    |                         Return generator metadata
    v                              |
User selects features              |
    |                              |
Validate selections <--------------+
    |
Apply generators sequentially --> Execute each generator
    |                              |
Update .algokit.toml               v
    |                         Apply template files
    v
Complete project
```

### Workflow 2: Incremental CLI Commands

Command to Generator Mapping:

| Command | Generator Name |
|---------|---------------|
| `add workspace` | `workspace` |
| `add base-contracts-python` | `base-contracts-python` |
| `add base-contracts-typescript` | `base-contracts-typescript` |
| `add base-frontend-react` | `base-frontend-react` |
| `add testing` | `testing` |
| `add linting` | `linting` |
| `add formatting` | `formatting` |

### Workflow 3: Configuration-Based Generation Example

```yaml
project:
  id: python-fullstack-marketplace
  name: "Digital Marketplace"
  # Additional metadata that can be used for any purpose e.g. example gallery
  
  # Generators applied in order
  # This is the only config that is needed to build a project
  # Each generator can run no data because of defaults but can be overridden with the data config.    
  generators:
    - name: workspace
      
    - name: base-contracts-python
      
    - name: create-smart-contract
      data:
        language: python
        contract_name: digital_marketplace
        
    - name: example-digital-marketplace
      
    - name: base-frontend-react
      
    - name: testing
      
    - name: linting
      
    - name: formatting
```
