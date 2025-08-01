# Algorand Fullstack Example

This is a full-stack example that demonstrates how to build and deploy Algorand smart contracts with a React frontend. It combines production-ready smart contract development with a modern web interface.

## Features

### Frontend Features

- React web app with TypeScript and Tailwind CSS
- Styled components using DaisyUI
- Wallet integration via use-wallet (supports Pera, Defly, and Exodus)
- Jest unit tests and Playwright E2E tests
- Environment variable support with dotenv
- Local development support with KMD provider for algokit localnet

### Smart Contract Features

- Multiple smart contract language support:
  - Python (via Beaker)
  - TypeScript
  - TealScript
- Automated testing and deployment workflows
- Deploy-time immutability controls

## Prerequisites

- Python 3.12 or later
- Docker (required for LocalNet)
- AlgoKit CLI (2.0.0 or later)
- Poetry (1.2 or later)

## Quick Start

1. **Launch in Github Codespace (Recommended)**

   - Click the **CodeSpace** button to launch the project
   - This automatically sets up AlgoKit and runs Localnet

2. **Local Setup**

   ```bash
   # Install dependencies for all projects
   algokit project bootstrap all

   # Or install specific dependencies:
   algokit project bootstrap npm     # Frontend dependencies
   algokit project bootstrap poetry  # Smart contract dependencies
   ```

## Development Workflow

### Smart Contracts

```bash
# Build contracts
algokit project run build

# Deploy to localnet
algokit project deploy localnet
```

### Frontend

- Development server: `cd frontend && npm run dev`
- Run tests: `npm test`
- Build: `npm run build`
