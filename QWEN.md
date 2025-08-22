# CRUSH.md - WCSAGA Godot Converter

## Build/Lint/Test Commands

**Installation:**
- `make install` - Install production dependencies
- `make install-dev` - Install development dependencies

**Testing:**
- `make test` - Run all tests
- `make test-coverage` - Run tests with coverage
- `uv run run_tests.py [module]` - Run specific test module
- `uv run pytest converter/tests/test_[module].py::TestClass::test_method` - Run single test

**Code Quality:**
- `make format` - Format code with Black and isort
- `make lint` - Lint with flake8
- `make typecheck` - Type checking with mypy
- `make quality` - Run all quality checks

**Project Commands:**
- `make setup-env` - Setup environment
- `make analyze` - Analyze source codebase
- `make migrate` - Run migration

## Code Style Guidelines

**Python (Converter Code):**
- Black formatting (line-length=88)
- Type hints required for all functions
- snake_case for variables/functions
- PascalCase for classes
- CONSTANT_CASE for constants
- Use pytest for testing with `test_` prefix

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

**Testing Patterns:**
- Test classes: `TestClassName`
- Test methods: `test_method_name`
- Use pytest fixtures for setup/teardown
- Mock external dependencies
- Aim for high test coverage on core systems

## Project Structure
- `/converter/` - Main migration system
- `/source/` - Original C++ source code
- `/target/` - Generated Godot project
- `/converter/tests/` - Unit tests
- `/converter/context/` - Style guides & templates

## Key Files
- `pyproject.toml` - Project configuration
- `Makefile` - Development commands
- `converter/context/STYLE_GUIDE.md` - GDScript style guide
- `run_tests.py` - Test runner

## Development Workflow
1. Run `make install-dev`
2. Write tests for new features
3. Implement functionality
4. Run `make quality` to check code
5. Run specific tests: `uv run pytest converter/tests/test_[module].py`
6. Commit changes with descriptive messages