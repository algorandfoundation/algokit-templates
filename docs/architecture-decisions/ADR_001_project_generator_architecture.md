# ADR-001: AlgoKit Project Generator Architecture - Transition to Modular Generator System

## Status
Proposed

## Background Context

### Current System Overview
The AlgoKit ecosystem currently consists of two main repositories working in tandem. The algokit-templates repository uses Copier as its templating engine, organizing templates into base templates (workspace, contracts, frontend) and example templates that demonstrate specific use cases. Project composition is managed through an `examples.yml` configuration file that defines how templates are layered together. The algokit-cli repository provides the user interface through `algokit init` for project creation and `algokit generate` for adding components to existing projects. The system supports various features including preset configurations (starter vs production), post-generation hooks for configuration merging, IDE integration for VSCode and JetBrains, and maintains a curated list of "blessed" templates. The examples folder contains fully hydrated projects that serve dual purposes: providing reference implementations and populating the AlgoKit example gallery.

### Terminology and Definitions

**Project**: An AlgoKit-managed codebase that contains one or more related applications or components for Algorand development. A project is defined by the presence of an .algokit.toml configuration file and can be structured as either a single-purpose project (containing only smart contracts OR only frontend code) or a workspace project (containing multiple related sub-projects such as both smart contracts and frontend applications). Projects track their applied generators, configuration, and metadata through the .algokit.toml file, enabling incremental enhancement and state management throughout the development lifecycle.

**Example Project**: A fully-hydrated AlgoKit project that demonstrates a complete, functional implementation of a specific use case or pattern. Example projects are created by applying base, feature, and example generators in sequence to produce ready-to-run applications that serve as both reference implementations for developers and entries in the AlgoKit gallery.

**Generator**: A self-contained, modular unit that applies a specific set of transformations to create or modify project files, configurations, and structure. Generators are designed to be idempotent, meaning they can be executed multiple times on the same project without causing unintended side effects - subsequent runs will either produce the same result or gracefully handle existing configurations without duplication or corruption.

**Base Generator**: These generators establish the foundational structure and core functionality for different project types - either smart contracts or frontend applications. They create the essential scaffolding that defines the project's primary purpose, including language-specific boilerplate, dependency management files, and basic project structure. Base generators provide the minimal viable starting point upon which other generators can build.

**Feature Generator**: Modular units that add specific development capabilities to existing projects. These generators enhance projects with cross-cutting concerns such as testing frameworks, linting configurations, code formatting tools, CI/CD pipelines, development containers, or documentation structures. Feature generators are designed to work with any compatible base generator and can be applied independently and incrementally throughout the project lifecycle.

**Example Generator**: These generators apply domain-specific code and configurations to demonstrate particular use cases or architectural patterns. They transform a base project into a fully-functional application by adding business logic, sample implementations, and complete working features. Example generators showcase best practices and provide developers with ready-to-run applications that illustrate real-world scenarios like digital marketplaces, NFT collections, or DeFi applications.

## User Workflows Requirements

**Workflow 1: Interactive TUI Wizard**
As a developer new to Algorand, I want to use an interactive wizard that guides me through project creation, so that I can easily select the features I need without understanding all the technical details upfront. The wizard should present me with clear options for project type, language preferences, and additional features like testing frameworks, linting tools, and IDE configurations. After creating my initial project, I should be able to run commands like `algokit project add testing` or `algokit project add linting` to incrementally enhance my project with new capabilities.

**Workflow 2: Incremental Command-Line Building**
As an experienced developer, I want to build my project incrementally using explicit commands, so that I have full control over the project structure and can automate the process in CI/CD pipelines. I should be able to start with `algokit project add workspace` to create a workspace structure, then add components like `algokit project add base --contracts --python` for smart contracts and `algokit project add base --frontend --react` for the frontend. This approach allows me to build exactly what I need, when I need it, and understand each layer being added to my project.

Example commands:
```bash
# Creates workspace structure
algokit project add workspace

# Adds Python contract base
algokit project add base --contracts --python

# Adds TypeScript contract base
algokit project add base --contracts --typescript

# Adds React frontend base
algokit project add base --frontend --react

# Auto-detects project type and adds testing
algokit project add testing

# Adds linting configuration
algokit project add linting

# Adds formatting configuration
algokit project add formatting
```

**Workflow 3: Configuration-Based Generation**
As a team lead or architect, I want to define my project structure in a configuration file and generate consistent projects from it, so that my team can quickly spin up standardized projects that follow our architectural patterns. I should be able to create a YAML configuration that specifies all the generators to apply in sequence, including base templates, example code, and features. This configuration should be versionable, shareable, and reproducible across different environments, enabling commands like `algokit project generate --config my-template.yml`.

## Project Generator Requirements

### 1. Core Capabilities
- **Configuration-Based Generation**: Project generation SHALL run from a configuration and SHALL have all agreed-upon features that currently exist in the templates (e.g. use_python_pytest, use_jest, use_vitest, use_playwright etc.)
- **Feature Modularity and Idempotency**: Project generation features (e.g. testing, formatting, linting) SHALL be modular and idempotent. Features SHALL be able to be run (or added) at any point in the lifecycle of the project. Each feature SHALL be able to be run on top of any existing project in an idempotent way. Note: The order in which features are added does matter
- **Lifecycle Flexibility**: Features SHALL be addable at any point in the project lifecycle
- **Project Structure Support**: The project generator SHALL support users creating projects in a VSCode workspace or a non-workspace project structure

### 2. User Interaction
- **Project Creation Methods**: Users SHALL be able to manually form a project from scratch by adding project features manually, specifying a configuration, or using an init wizard
- **Feature Addition Workflow with Diff Preview**: When adding a feature to a project, the project generator SHALL show the user the diff of what will be added. User approval SHALL be required before proceeding (similar to astro add functionality)
- **Conflict Detection and Resolution**: When adding a feature, the project generator SHALL check if the feature has already been added (either by configuration or existence of files/directories). The project generator SHALL warn the user that files will be overwritten if they proceed with feature generation

### 3. Project Management
- **Feature Status Tracking**: While in an AlgoKit project, users SHALL be able to determine status of what features have been added to the project
- **Version Tracking**: The project generator SHALL be able to know what version of the project generator was used to generate the project
- **Compatibility Management**: The project generator SHALL be able to know if there are compatibility issues between the project generator used to generate the project and the project generator being used to add a feature. The project generator SHALL flag the user to these compatibility issues or error if the compatibility issues are not reconcilable

### 4. Non Functional Requirements
- **No Manual Dependency Installation**: The project generator SHALL NOT require a user to manually install a python dependency or any other required dependencies in order to run the project generator

## Current Gaps

**Diff Preview and Approval System**
The current implementation applies changes directly without showing users what will be modified. There is no mechanism to preview changes before they are applied, and no approval workflow exists. This makes users hesitant to run generators on existing projects as they cannot predict the impact.

**Intelligent Conflict Detection**
While Copier provides basic file overwrite warnings, there is no intelligent detection of feature conflicts. The system cannot determine if a feature has already been added by examining project configuration or file patterns. This can lead to duplicate configurations or broken setups when features are added multiple times.

**Comprehensive Compatibility Management**
The current system has basic version requirement checking but lacks a compatibility matrix between generator versions. There are no automated migration paths when upgrading generators, and no clear way to handle breaking changes between versions. Projects can become stuck on old generator versions with no upgrade path.

**Self-Contained Execution Environment**
Users must manually install Python and other dependencies before using AlgoKit. The typed client generators require separate package installations (`@algorandfoundation/algokit-client-generator` for TypeScript, `algokit-client-generator` for Python). This creates barriers to entry and potential version conflicts.

**Scattered Feature Status Tracking**
Feature configuration is distributed across multiple files (`.copier-answers.yml`, `.algokit.toml`, `pyproject.toml`, `package.json`). There is no single command to view all enabled features and their status. Users must manually inspect multiple files to understand their project configuration.

## Options

### Option 1: Flat Generator Architecture with State in .algokit.toml

#### Overview
Transform the current template system into a flat generator architecture where every feature (workspace setup, base templates, testing, linting, etc.) is implemented as an independent, composable generator. State management is centralized in the project's `.algokit.toml` file, providing transparency and version control friendliness.

#### Functionality Distribution

| Functionality | CLI Repo | Templates Repo | Notes |
|--------------|----------|----------------|-------|
| TUI Wizard Interface | ✓ | | Interactive UI for project initialization |
| CLI Command Parsing | ✓ | | Parse and validate user commands |
| Generator Discovery | ✓ | | Query available generators from templates |
| Generator Metadata | | ✓ | Dependencies, compatibility, descriptions |
| Generator Implementation | | ✓ | All copier templates and transformation logic |
| Workflow Orchestration | ✓ | | Sequential application of generators |
| State Management | ✓ | | Track applied generators in .algokit.toml |
| Project Type Detection | ✓ | | Analyze existing project structure |
| Configuration Parsing | ✓ | | Parse YAML/TOML configuration files |
| Compatibility Checking | ✓ | | Validate generator combinations |
| Example Configurations | | ✓ | YAML files defining example projects |
| Hydrated Examples | | ✓ | Full example projects for app gallery |
| Diff Preview Engine | ✓ | | Show changes before applying |
| Conflict Resolution | ✓ | | Handle file conflicts during generation |
| Version Management | ✓ | | Track generator versions in .algokit.toml |

#### Repository Structure

**Templates Repository:**
```
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

**CLI Repository:**
```
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

#### Schema Configuration

##### AlgoKit Project Configuration Schema (.algokit.toml)

The `.algokit.toml` configuration file will undergo several changes to support the new generator architecture:

```toml
[algokit]
min_version = "v2.0.0"  # Remains unchanged

[project]
# CHANGED: type enum now only includes: contracts, frontend, fullstack
# REMOVED: "workspace" and "backend" as types (workspace is now a generator)
type = "fullstack"  
name = "my-project"

# projects_root_path is only required when workspace generator is applied
projects_root_path = "projects"

# NEW: Track all applied generators with metadata
[project.generators]
workspace = { version = "1.0.0", timestamp = "2024-01-01T00:00:00Z" }
"base-contracts-python" = { version = "1.0.0", timestamp = "2024-01-01T00:01:00Z" }
"base-frontend-react" = { version = "1.0.0", timestamp = "2024-01-01T00:02:00Z" }
testing = { version = "1.0.0", timestamp = "2024-01-01T00:03:00Z", detected_type = "python_contract" }
linting = { version = "1.0.0", timestamp = "2024-01-01T00:04:00Z" }

# Remains unchanged - populated by generators
[project.run]
test = { commands = ["poetry run pytest"], description = "Run smart contract tests" }
lint = { commands = ["poetry run ruff check"], description = "Check code style" }
format = { commands = ["poetry run black ."], description = "Format code" }

# Remains unchanged
[project.deploy]
command = "poetry run python -m smart_contracts deploy"
environment_secrets = ["DEPLOYER_MNEMONIC"]

# REMOVED: The entire [generate] section
# Previously:
# [generate.smart-contract]
# description = "Generate a new smart contract"
# path = ".algokit/generators/smart-contract"
#
# This functionality is replaced by `algokit project add` commands
```

Key changes:
- `project.type` now limited to `contracts`, `frontend`, or `fullstack`
- Added `project.generators` to track applied generators with metadata
- Removed the entire `[generate]` section as generators are no longer embedded in projects
- Workspace identification now done by checking if `workspace` exists in `project.generators`

###### Updated JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AlgoKit Configuration Schema",
  "description": "JSON Schema for .algokit.toml configuration files used by AlgoKit CLI",
  "type": "object",
  "properties": {
    "algokit": {
      "type": "object",
      "description": "AlgoKit CLI-specific configuration",
      "properties": {
        "min_version": {
          "type": "string",
          "description": "Minimum required version of AlgoKit CLI",
          "pattern": "^v?\\d+\\.\\d+\\.\\d+(?:-[a-zA-Z0-9.-]+)?$",
          "examples": ["v2.0.0", "1.3.1", "v1.1.0-beta.4"]
        }
      },
      "additionalProperties": false
    },
    "project": {
      "type": "object",
      "description": "Project configuration and metadata",
      "properties": {
        "type": {
          "type": "string",
          "description": "Type of AlgoKit project",
          // CHANGED: Removed "workspace" and "backend", now only core types
          "enum": ["contracts", "frontend", "fullstack"]
        },
        "name": {
          "type": "string",
          "description": "Name of the project",
          "minLength": 1
        },
        "projects_root_path": {
          "type": "string",
          "description": "Root path for sub-projects in a workspace",
          "minLength": 1
        },
        "artifacts": {
          "type": "string",
          "description": "Path to artifacts directory for contract projects",
          "minLength": 1
        },
        // NEW: Track applied generators with metadata
        "generators": {
          "type": "object",
          "description": "Track applied generators with metadata",
          "patternProperties": {
            "^[a-zA-Z0-9_-]+$": {
              "$ref": "#/$defs/generatorMetadata"
            }
          },
          "additionalProperties": false
        },
        "deploy": {
          "$ref": "#/$defs/deployConfig"
        },
        "run": {
          "oneOf": [
            {
              "$ref": "#/$defs/workspaceRunConfig"
            },
            {
              "$ref": "#/$defs/standaloneRunConfig"
            }
          ]
        }
      },
      // CHANGED: Conditional logic now based on generators instead of type
      "allOf": [
        {
          "if": {
            "properties": {
              "generators": {
                "properties": {
                  "workspace": {
                    "type": "object"
                  }
                },
                "required": ["workspace"]
              }
            }
          },
          "then": {
            "required": ["projects_root_path"]
          }
        }
      ],
      "required": ["type", "name"],
      "additionalProperties": false
    },
    // REMOVED: The entire "generate" section - generators are no longer embedded
    // "generate": {
    //   "type": "object",
    //   "description": "Custom generator configurations",
    //   "patternProperties": {
    //     "^[a-zA-Z0-9_-]+$": {
    //       "$ref": "#/$defs/generatorConfig"
    //     }
    //   },
    //   "additionalProperties": false
    // },
    "deploy": {
      "$ref": "#/$defs/deployConfig",
      // Still present but should be deprecated
      "description": "Legacy deploy configuration (deprecated, use project.deploy instead)"
    }
  },
  "additionalProperties": false,
  "$defs": {
    // NEW: Definition for generator metadata
    "generatorMetadata": {
      "type": "object",
      "description": "Metadata for an applied generator",
      "properties": {
        "version": {
          "type": "string",
          "description": "Version of the generator that was applied",
          "pattern": "^\\d+\\.\\d+\\.\\d+$"
        },
        "timestamp": {
          "type": "string",
          "description": "ISO 8601 timestamp when generator was applied",
          "format": "date-time"
        },
        "source": {
          "type": "string",
          "description": "Source of the generator (e.g., 'official', URL)",
          "default": "official"
        },
        "detected_type": {
          "type": "string",
          "description": "Auto-detected project type for context-aware generators"
        }
      },
      "required": ["version", "timestamp"],
      "additionalProperties": true
    },
    // REMOVED: generatorConfig definition - no longer needed
    // "generatorConfig": {
    //   "type": "object",
    //   "description": "Generator configuration",
    //   "properties": {
    //     "path": {
    //       "type": "string",
    //       "description": "Path to the generator template",
    //       "minLength": 1
    //     },
    //     "description": {
    //       "type": "string",
    //       "description": "Description of what the generator does",
    //       "minLength": 1
    //     }
    //   },
    //   "required": ["path"],
    //   "additionalProperties": false
    // },
    
    // The following definitions remain unchanged
    "deployConfig": {
      "type": "object",
      "description": "Deployment configuration",
      "properties": {
        "command": {
          "oneOf": [
            {
              "type": "string",
              "description": "Deploy command as a string",
              "minLength": 1
            },
            {
              "type": "array",
              "description": "Deploy command as an array of strings",
              "items": {
                "type": "string"
              },
              "minItems": 1
            }
          ]
        },
        "environment_secrets": {
          "type": "array",
          "description": "List of environment variable names to treat as secrets",
          "items": {
            "type": "string",
            "minLength": 1
          },
          "uniqueItems": true
        }
      },
      "patternProperties": {
        "^[a-zA-Z0-9_-]+$": {
          "type": "object",
          "description": "Network-specific deployment configuration",
          "properties": {
            "command": {
              "oneOf": [
                {
                  "type": "string",
                  "description": "Deploy command as a string for this network",
                  "minLength": 1
                },
                {
                  "type": "array",
                  "description": "Deploy command as an array of strings for this network",
                  "items": {
                    "type": "string"
                  },
                  "minItems": 1
                }
              ]
            },
            "environment_secrets": {
              "type": "array",
              "description": "List of environment variable names to treat as secrets for this network",
              "items": {
                "type": "string",
                "minLength": 1
              },
              "uniqueItems": true
            }
          },
          "additionalProperties": false
        }
      },
      "additionalProperties": false
    },
    "workspaceRunConfig": {
      "type": "object",
      "description": "Workspace run configuration defining execution order",
      "patternProperties": {
        "^[a-zA-Z0-9_-]+$": {
          "type": "array",
          "description": "Ordered list of project names for command execution",
          "items": {
            "type": "string",
            "minLength": 1
          },
          "uniqueItems": true
        }
      },
      "additionalProperties": false
    },
    "standaloneRunConfig": {
      "type": "object",
      "description": "Standalone project run configuration",
      "patternProperties": {
        "^[a-zA-Z0-9_-]+$": {
          "$ref": "#/$defs/customCommand"
        }
      },
      "additionalProperties": false
    },
    "customCommand": {
      "type": "object",
      "description": "Custom command configuration",
      "properties": {
        "commands": {
          "type": "array",
          "description": "List of commands to execute",
          "items": {
            "type": "string",
            "minLength": 1
          },
          "minItems": 1
        },
        "description": {
          "type": "string",
          "description": "Description of what the command does",
          "minLength": 1
        },
        "env_file": {
          "type": "string",
          "description": "Path to environment file to load",
          "minLength": 1
        }
      },
      "required": ["commands"],
      "additionalProperties": false
    }
  }
}
```

##### AlgoKit Template Configuration Schema

The AlgoKit Template Configuration Schema defines reusable project templates that specify which generators to apply in sequence. This replaces the current `examples.yml` structure with a simplified format focused only on essential fields.

###### YAML Example
```yaml
# Simplified schema - only essential fields
id: "python-fullstack-marketplace"
name: "Digital Marketplace" 
generators:
  - name: workspace
  - name: base-contracts-python
  - name: create-smart-contract
    data:
      language: python
      contract_name: "digital_marketplace"
  - name: base-frontend-react
  - name: example-digital-marketplace
  - name: testing
  - name: linting
  - name: devcontainer
```

###### TOML Example
```toml
id = "python-fullstack-marketplace"
name = "Digital Marketplace"

[[generators]]
name = "workspace"

[[generators]]
name = "base-contracts-python"

[[generators]]
name = "create-smart-contract"
[generators.data]
language = "python"
contract_name = "digital_marketplace"

[[generators]]
name = "base-frontend-react"

[[generators]]
name = "example-digital-marketplace"

[[generators]]
name = "testing"

[[generators]]
name = "linting"

[[generators]]
name = "devcontainer"
```

###### JSON Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AlgoKit Template Configuration Schema",
  "description": "Schema for AlgoKit template configuration files",
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier for the template",
      "pattern": "^[a-z0-9-]+$"
    },
    "name": {
      "type": "string", 
      "description": "Human-readable name for the template",
      "minLength": 1
    },
    "generators": {
      "type": "array",
      "description": "List of generators to apply in sequence",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "Name of the generator to apply"
          },
          "data": {
            "type": "object",
            "description": "Optional data to pass to the generator",
            "additionalProperties": true
          }
        },
        "required": ["name"],
        "additionalProperties": false
      },
      "minItems": 1
    }
  },
  "required": ["id", "name", "generators"],
  "additionalProperties": false
}
```

Key changes from current `examples.yml`:
- `project_name` becomes `name`
- `templates` becomes `generators` 
- Only `id`, `name`, and `generators` are required for template execution
- Additional metadata fields (type, author, title, description, tags, features, detailsPages) can still be included for project gallery display but are not needed to run generators
- Each generator entry only needs `name` and optional `data`
- Simplified core structure focused on defining what generators to run in sequence

### Workflow Implementation

**Workflow 1: Interactive Wizard (TUI)**
There is a spike for this TUI [here](https://github.com/lempira/template-gallery-spike) Look at the end for a video of the TUI. 

```
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

**Workflow 2: Incremental CLI Commands**

Command to Generator Mapping:

| Command | Generator Name |
|---------|---------------|
| `add workspace` | `workspace` |
| `add base --contracts --python` | `base-contracts-python` |
| `add base --contracts --typescript` | `base-contracts-typescript` |
| `add base --frontend --react` | `base-frontend-react` |
| `add testing` | `testing` |
| `add linting` | `linting` |
| `add formatting` | `formatting` |

**Workflow 3: Configuration-Based Generation**
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
      
    - name: devcontainer
```

#### Migration and Backward Compatibility

##### Impact on Existing Templates

Currently, AlgoKit templates are maintained as individual GitHub repositories containing full Copier templates. These standalone repositories will undergo a phased deprecation process, remaining functional but marked as deprecated initially, then archived after the `--legacy` flag is removed from the CLI.

All Algorand Foundation maintained templates will be migrated to the new generator architecture and consolidated within the main algokit-templates repository. Each template's functionality will be decomposed into appropriate base, feature, and example generators to maintain feature parity while improving modularity.

While custom generator creation through the legacy mechanism will no longer be supported, the underlying Copier functionality remains available. The `--template-url` and `--template-url-ref` flags will continue to function for direct Copier template usage, and community templates can still be created as Copier projects and used via `--template-url`. Since generators themselves are Copier projects, community-created generators can theoretically be consumed through these flags.

The specifics of community generator integration and distribution mechanisms are considered out-of-scope for this initial architecture transition and will be addressed in future iterations.

##### Migration Path

The migration to the new generator architecture will be managed primarily through the CLI, with a focus on introducing new functionality without breaking existing workflows until the next major version. The key mechanism for this transition is the introduction of a `beta` command group.

The beta command group provides access to features that are functionally complete but may still undergo changes before being considered stable. These features are in active development and testing, allowing early adopters to experiment with new functionality while maintaining access to stable commands for production use. To use a beta command, users prepend `beta` to the command group, such as `algokit beta init`, which will eventually replace the current `algokit init` with the new TUI workflow.

New commands that don't conflict with existing functionality will be added directly without the beta prefix:

- `algokit project add` - Adds generators to existing projects (base and feature generators only, not example generators)
- `algokit project add base contracts --language <typescript|python>` - Adds the base contracts generator (workspace-aware)
- `algokit project add frontend <react|vue|svelte|solid|angular>` - Adds the base frontend generator (workspace-aware)

This command structure replaces the `algokit generate` workflow for project scaffolding, as `add` better describes the action of layering functionality onto an existing project, while `generate` implies creating something from scratch or producing standalone artifacts.

The existing `algokit generate` command will be deprecated for project generator use in favor of `algokit project add`, though it will continue to function for generating app clients. The new project build process will only guarantee compatibility with projects created using the new generators. While `algokit project add` can be used with older projects, users will receive a warning that this is not recommended, encouraging migration to the new architecture for optimal results.

##### Justification for Dropping Legacy Generators

The decision to drop legacy generators stems from fundamental maintenance and complexity issues inherent in the current architecture. Legacy generators must be embedded within each project and exist separately in every repository, creating significant code duplication that becomes increasingly difficult to maintain as the number of project examples grows. Additionally, the legacy generators add unnecessary complexity to the templates themselves - the current templates already use Jinja templating which is difficult to understand, and the generators in the `.algokit` folder compound this complexity by also using Jinja templating, making it challenging for developers to comprehend what the generators are actually doing and how they transform the project.

#### Community Extensibility

Community generator integration and distribution mechanisms fall outside the scope of this initial architecture transition. Future iterations will address how community members can create, share, and discover custom generators, along with the protocols and infrastructure needed to support a thriving ecosystem of third-party generators.

#### Configuration Schemas

#### How This Satisfies Requirements

| Requirement Category | Requirement | How Option 1 Satisfies |
|---------------------|-------------|------------------------|
| **Core Capabilities** | Configuration-Based Generation | YAML configurations specify generators to apply sequentially |
| | Feature Modularity | Each feature is an independent generator in flat structure |
| | Idempotency | Generators designed to merge configurations, not overwrite |
| | Lifecycle Flexibility | Generators can be applied at any time via CLI commands |
| | Project Structure Support | Separate workspace and non-workspace generators |
| **User Interaction** | Multiple Creation Methods | TUI wizard, CLI commands, and config files all supported |
| | Diff Preview | CLI implements diff engine before applying generators |
| | Conflict Detection | CLI checks existing files and .algokit.toml state |
| **Project Management** | Feature Status Tracking | All features tracked in [project.generators] section |
| | Version Tracking | Each generator entry includes version and timestamp |
| | Compatibility Management | CLI validates versions before applying generators |
| **Non-Functional** | No Manual Dependencies | CLI bundles all required dependencies |

## Decision
[To be filled after review and discussion]

## Next Steps
[To be completed after decision]