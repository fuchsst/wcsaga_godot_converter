# Centurion Agentic Migration System - Wing Commander Saga to Godot Converter

ALWAYS use `uv` or `make` to run build tooling like liner, tests, formater etc.!!!
You MUST use `uv run`  to run any Python code!!!

If the user asks for refinements, ALWAYS look for existing files that cover that purpose. Edit the file. Do NOT create new a "enhanced" or "refined" version of the file!

## Build/Lint/Test Commands

**Installation:**
- `make install` - Install production dependencies using uv
- `make install-dev` - Install development dependencies using uv

**Testing:**
- `make test` - Run all tests with pytest via uv
- `make test-coverage` - Run tests with coverage reporting via uv
- `uv run python run_tests.py [module]` - Run specific test module
- `uv run pytest converter/tests/test_[module].py::TestClass::test_method` - Run single test

**Code Quality:**
- `make format` - Format code with Black and isort via uv
- `make lint` - Lint with flake8 via uv
- `make typecheck` - Type checking with mypy via uv
- `make quality` - Run all quality checks (format, lint, typecheck) via uv

**Project Commands:**
- `make setup-env` - Setup development environment with uv
- `make analyze` - Analyze source codebase
- `make migrate` - Run LangGraph-based migration

## Architecture Overview

The Centurion system uses LangGraph as the core orchestrator, providing a deterministic, reliable, and observable workflow for the complex code migration process. The system implements a state machine approach with specialized components working together in "bolt" cycles.

### Core Components

1. **LangGraph Orchestrator** - Deterministic state machine for migration workflow
2. **Unified Tool Framework** - Standardized interface for all external tools
3. **Test Quality Gate** - Automated validation of AI-generated tests with JUnit XML parsing
4. **Proactive HITL Patterns** - Human-in-the-loop integration for critical decisions

### Workflow Process

The system operates in "bolts" - intense work cycles that follow this sequence:
1. **Targeting** - Select atomic task from backlog using LangGraph state machine
2. **Analysis** - Code Analyst examines source files and parses legacy formats
3. **Generation** - Refactoring Specialist creates Godot files using qwen-code
4. **Testing** - Test Generator creates unit tests with gdUnit4
5. **Validation** - Validation Engineer runs tests with quality gates and JUnit XML parsing
6. **Review** - Successful tasks are packaged for human review with HITL patterns

## Code Style Guidelines

**Python (Converter Code):**
- Black formatting (line-length=88)
- Type hints required for all functions
- snake_case for variables/functions
- PascalCase for classes
- CONSTANT_CASE for constants
- Use pytest for testing with `test_` prefix
- Follow LangGraph patterns for state machine workflows

**GDScript (Generated Code):**
- PascalCase for classes/nodes
- snake_case for variables/methods
- CONSTANT_CASE for constants
- Use Godot signals for communication
- Follow component-based design patterns
- Document public methods with docstrings

**Imports:**
- Standard library imports first
- Third-party imports second
- Local imports last
- Use absolute imports
- Sort imports with isort

**Error Handling:**
- Use specific exception types
- Include context in error messages
- Handle errors gracefully in user-facing code
- Use logging for non-critical errors
- Implement circuit breaker patterns for resilience

**Testing Patterns:**
- Test classes: `TestClassName`
- Test methods: `test_method_name`
- Use pytest fixtures for setup/teardown
- Mock external dependencies
- Aim for high test coverage on core systems
- Include integration tests for LangGraph workflows

## LangGraph Architecture Guidelines

**State Machine Design:**
- Use TypedDict for defining LangGraph state schemas
- Implement deterministic state transitions
- Use conditional edges for workflow control flow
- Store all workflow context in the central state

**Node Implementation:**
- Each node should be a pure function receiving state and returning updates
- Nodes should have single responsibilities
- Handle errors gracefully within nodes
- Use structured outputs for consistency

**Tool Integration:**
- Wrap all external CLI tools with standardized CommandLineTool wrappers
- Parse tool outputs into structured data
- Implement timeouts and error handling for all tools
- Use subprocess.Popen for fine-grained control

**Human-in-the-Loop Patterns:**
- Implement "Interrupt & Resume" for critical path validations using LangGraph interrupts
- Use "Human-as-a-Tool" for ambiguity resolution with confidence scoring
- Tag tasks requiring human approval in task definitions
- Provide structured context for human reviewers
- Handle human responses through Command resumption patterns

## Project Structure
- `/converter/` - Main migration system
- `/source/` - Original C++ source code
- `/target/` - Generated Godot project
- `/converter/tests/` - Unit and integration tests
- `/converter/context/` - Style guides & templates
- `/converter/orchestrator/` - LangGraph state machine orchestrator
- `/converter/graph_system/` - Dependency graph system
- `/converter/hitl/` - Human-in-the-loop integration
- `/converter/tools/` - CLI agent tool wrappers
- `/converter/validation/` - Test quality gates and validation

## Key Files
- `pyproject.toml` - Project configuration with uv
- `uv.lock` - Locked dependencies for reproducible environments
- `Makefile` - Development commands using uv
- `converter/context/STYLE_GUIDE.md` - GDScript style guide
- `run_tests.py` - Test runner
- `converter/orchestrator/langgraph_orchestrator.py` - Core LangGraph orchestrator

## Development Workflow
1. Run `make install-dev` to setup environment with uv
2. Write tests for new features following pytest and LangGraph patterns
3. Implement functionality with LangGraph state machine nodes
4. Run `make quality` to check code quality
5. Run specific tests: `uv run pytest converter/tests/test_[module].py`
6. Verify LangGraph workflows with integration tests
7. Commit changes with descriptive messages

ALWAYS use `uv`to run python scripts.
You MUST use `uv`to run python scripts.