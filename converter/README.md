# Wing Commander Saga to Godot Converter

This directory contains the agentic migration system for converting the Wing Commander Saga codebase from C++ to Godot/GDScript.

## Project Overview

This system implements a LangGraph-based state machine framework for migrating the Wing Commander Saga game engine from C++ to Godot. It uses a deterministic workflow with specialized components to automate the complex process of code translation, refactoring, and validation.

## Architecture

The system is organized around a LangGraph state machine with specialized components:

1. **Codebase Analysis** - Analyzes the legacy C++ codebase to identify dependencies and patterns
2. **Refactoring Engine** - Converts C++ code to GDScript using advanced transformation rules
3. **Test Generation** - Creates comprehensive unit tests for the migrated code
4. **Validation Engine** - Validates the migrated code against quality gates
5. **Human-in-the-Loop Integration** - Provides strategic human oversight for critical decisions

The system uses **qwen-code** as the primary CLI coding agent, built upon Alibaba's state-of-the-art Qwen3-Coder models.

## Directory Structure

- `analyst/` - Code analysis implementation
- `config/` - Configuration files
- `context/` - Guidance artifacts (style guides, rules, templates, examples)
- `graph_system/` - Dependency graph system for tracking code relationships
- `hitl/` - Human-in-the-loop integration
- `orchestrator/` - LangGraph orchestrator implementation
- `refactoring/` - Refactoring engine implementation
- `scripts/` - Utility scripts
- `tasks/` - Task definitions and templates
- `test_generator/` - Test generation implementation
- `tests/` - System tests
- `tools/` - Custom tools for CLI agent control
- `validation/` - Validation engine implementation

## Key Components

### Context Engineering
The `context/` directory contains essential guidance artifacts:
- `STYLE_GUIDE.md` - Architectural style guide for Godot/GDScript
- `RULES.md` - Virtual constitution with strict principles
- `TEMPLATES/` - Scaffolding templates for common file types
- `GOLD_STANDARDS/` - Curated examples of perfect implementations

### CLI Agent Tools
The `tools/` directory contains wrappers for the qwen-code CLI agent:
- `qwen_code_wrapper.py` - For high-context generation tasks
- `qwen_code_execution_tool.py` - Base tool for shell command execution

### Task Templates
The `tasks/task_templates/` directory contains prompt templates specifically designed for qwen-code:
- `qwen_prompt_templates.py` - Structured templates for different task types

## Workflow

The system operates in "bolts" - intense work cycles that follow this sequence:

1. **Targeting** - Select atomic task from backlog
2. **Analysis** - Code Analyst examines source files
3. **Generation** - Refactoring Specialist creates Godot files using qwen-code
4. **Testing** - Test Generator creates unit tests
5. **Validation** - Validation Engineer runs tests with quality gates
6. **Review** - Successful tasks are packaged for human review

## Human-in-the-Loop

The system is designed with strategic human oversight:
- Upfront strategy and context engineering
- Expert review of AI-generated pull requests
- Edge case intervention for complex problems
- Final authorization for merging changes
- Proactive HITL patterns for critical decision points

## Getting Started

Please refer to the main project README.md at the root of the repository for detailed setup instructions.
The main project uses modern Python tooling including `pyproject.toml`, `uv` for dependency management,
and comprehensive development tools.

To run the migration:

```bash
# From the project root directory
./run.sh ../source ../target
```

Additional arguments can be passed to the migration script:

```bash
./run.sh ../source ../target --verbose --phase analysis
```

## Running Tests

Tests can be run using the project's Makefile from the root directory:

```bash
# Run all tests
make test

# Run tests with coverage
make test-coverage

# List available test modules
make help
```

Or directly with pytest:

```bash
# From the project root directory
pytest converter/tests/
```

## Governance

The system includes built-in governance mechanisms:
- Automated feedback loops for self-correction
- Circuit breaker pattern for intractable problems
- Integrated security scanning
- Comprehensive logging and monitoring
- Test quality gates to ensure rigorous validation
- Proactive HITL patterns for critical decision points

For detailed information about the project structure, development tools, and setup instructions,
please refer to the main README.md file at the root of the project.