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

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd wcsaga_godot_converter
   ```

2. Install dependencies using uv:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

3. For development dependencies:
   ```bash
   uv pip install -e ".[dev]"
   ```

## Usage

### Environment Setup

1. Set up environment variables:
   ```bash
   export DEEPSEEK_API_KEY="your-deepseek-api-key"
   export DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"
   ```

2. Run the setup script:
   ```bash
   python setup_environment.py --full
   ```

### Code Analysis

Analyze the source codebase:
```bash
python analyze_source_codebase.py --source ../source --output analysis.json
```

### Migration Process

Run the migration:
```bash
cd converter
python orchestrator/main.py --source ../source --target ../target
```

Or use the convenience script:
```bash
./run.sh ../source ../target
```

## Development

### Running Tests

Execute the test suite:
```bash
pytest
```

Or with coverage:
```bash
pytest --cov=converter
```

### Code Formatting

Format code with Black:
```bash
black .
```

Sort imports with isort:
```bash
isort .
```

### Linting

Lint code with flake8:
```bash
flake8 .
```

### Type Checking

Run mypy for type checking:
```bash
mypy .
```

## Project Structure

```
wcsaga_godot_converter/
├── converter/              # Main migration system code
│   ├── agents/             # Agent definitions and configurations
│   ├── analyst/            # Code Analyst agent implementation
│   ├── config/             # Configuration files
│   ├── context/            # Guidance artifacts
│   ├── orchestrator/        # Orchestrator agent implementation
│   ├── prompt_engineering/ # Prompt Engineering agent implementation
│   ├── refactoring/        # Refactoring Specialist agent implementation
│   ├── scripts/            # Utility scripts
│   ├── tasks/              # Task definitions and templates
│   ├── test_generator/    # Test Generator agent implementation
│   ├── tests/             # System tests
│   ├── tools/             # Custom tools for CLI agent control
│   ├── validation/        # Validation Engineer agent implementation
│   └── workflows/         # Process definitions
├── pyproject.toml         # Python project configuration
├── README.md              # Project documentation
├── setup_environment.py   # Environment setup script
├── analyze_source_codebase.py # Codebase analysis script
└── requirements.txt       # Legacy requirements file
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