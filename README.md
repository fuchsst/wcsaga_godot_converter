# Wing Commander Saga to Godot Converter

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Agentic migration system for converting the Wing Commander Saga game engine from C++ to Godot/GDScript.

## Overview

This project implements a hierarchical multi-agent framework for migrating the Wing Commander Saga game engine from C++ to Godot. Based on the Agentic Migration Playbook and specifically the "Agentic Migration with CLI Agents" approach, it uses specialized AI agents to automate the complex process of code translation, refactoring, and validation.

## Architecture

The system is organized around five specialized AI agents, all powered by the **DeepSeek V3.1** model for consistent cognitive performance:

1. **MigrationArchitect** - Lead Systems Architect responsible for high-level planning
2. **CodebaseAnalyst** - Senior Software Analyst who analyzes the legacy codebase
3. **TaskDecompositionSpecialist** - Technical Project Manager who breaks down tasks
4. **PromptEngineeringAgent** - AI Communications Specialist who creates precise prompts
5. **QualityAssuranceAgent** - QA Automation Engineer who verifies results

We are standardizing on a single, powerful CLI coding agent: **qwen-code**, which is built upon Alibaba's state-of-the-art Qwen3-Coder models.

## Prerequisites

- Python 3.9 or higher
- [uv](https://github.com/astral-sh/uv) for dependency management
- DeepSeek API key for cognitive agents
- qwen-code CLI agent for code generation tasks

## Development Setup

### Initialize Environment with UV

Initialize a virtual environment and install dependencies:

```bash
make init-env
```

Or manually:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Install Dependencies

Install the package in development mode:

```bash
make install-dev
```

Or manually:

```bash
uv pip install -e ".[dev]"
```

## Development Workflow

This project uses `make` as the primary build tool with `uv` for dependency management. All development tasks should be performed through `make` commands.

### Testing

Run all tests:

```bash
make test
```

Run tests with coverage:

```bash
make test-coverage
```

List available test modules:

```bash
make list-tests
```

### Code Quality

Run all quality checks (formatting, linting, type checking):

```bash
make quality
```

Format code with Black and isort:

```bash
make format
```

Lint code with flake8:

```bash
make lint
```

Type checking with mypy:

```bash
make typecheck
```

### Other Development Tasks

Run environment setup:

```bash
make setup-env
```

Analyze source codebase:

```bash
make analyze
```

Run migration:

```bash
make migrate
```

Clean build artifacts:

```bash
make clean
```

## Project Structure

```
wcsaga_godot_converter/
├── converter/              # Main migration system code
│   ├── agents/             # Agent definitions and configurations
│   ├── analyst/            # Code Analyst agent implementation
│   ├── config/             # Configuration files
│   ├── context/            # Guidance artifacts
│   ├── graph_system/       # Dependency graph system for dynamic memory
│   ├── hitl/               # Human-in-the-loop integration
│   ├── orchestrator/        # Orchestrator agent implementation
│   │   └── state_machine/  # Custom state machine for deterministic bolt cycles
│   ├── prompt_engineering/ # Prompt Engineering agent implementation
│   ├── refactoring/        # Refactoring Specialist agent implementation
│   ├── scripts/            # Utility scripts
│   ├── tasks/              # Task definitions and templates
│   ├── test_generator/    # Test Generator agent implementation
│   ├── tests/             # System tests
│   ├── tools/             # Custom tools for CLI agent control
│   ├── validation/        # Validation Engineer agent implementation
│   │   └── enhanced/       # Enhanced validation with test quality gates
│   └── workflows/         # Process definitions
├── pyproject.toml         # Python project configuration
├── Makefile               # Build and development commands
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
└── run_tests.py           # Test runner script
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Governance

The system includes built-in governance mechanisms:
- Automated feedback loops for self-correction
- Circuit breaker pattern for intractable problems
- Integrated security scanning
- Comprehensive logging and monitoring
- Test quality gates to ensure rigorous validation
- Proactive HITL patterns for critical decision points