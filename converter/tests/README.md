# Converter Test Suite

This directory contains the comprehensive test suite for the Wing Commander Saga to Godot converter system.

## Test Organization

The tests are organized by component:

- `test_qwen_code_execution_tool.py` - Tests for the QwenCodeExecutionTool
- `test_qwen_code_wrapper.py` - Tests for the QwenCodeWrapper
- `test_prompt_engineering_agent.py` - Tests for the PromptEngineeringAgent
- `test_workflows.py` - Tests for SequentialWorkflow and HierarchicalWorkflow
- `test_example.py` - Example tests to verify setup

## Running Tests

### Run All Tests

To run all tests in the suite:

```bash
# From the converter directory
./test.sh
```

Or directly with pytest:

```bash
# Activate virtual environment first
source .venv/bin/activate
pytest tests/
```

### Run Tests for a Specific Module

To run tests for a specific module:

```bash
./test.sh qwen_code_execution_tool
```

Or directly with pytest:

```bash
# Activate virtual environment first
source .venv/bin/activate
pytest tests/test_qwen_code_execution_tool.py
```

### List Available Test Modules

To see a list of all available test modules:

```bash
./test.sh --list
```

### Verbose Output

To enable verbose output:

```bash
./test.sh --verbose
```

Or directly with pytest:

```bash
# Activate virtual environment first
source .venv/bin/activate
pytest tests/ -v
```

## Test Categories

The test suite provides comprehensive coverage of all major components:

1. **Tool Tests** - Validate the CLI execution tools
2. **Agent Tests** - Verify agent functionality
3. **Workflow Tests** - Ensure workflow orchestration works correctly
4. **Integration Tests** - Test component interactions
5. **Quality Gate Tests** - Validate test quality gates
6. **HITL Integration Tests** - Test human-in-the-loop integration
7. **Graph System Tests** - Validate dependency graph functionality

## Writing New Tests

When adding new functionality to the converter system, corresponding tests should be added to the appropriate test file. Follow these guidelines:

1. Use descriptive test method names that clearly indicate what is being tested
2. Include both positive and negative test cases
3. Use mocking where appropriate to isolate units under test
4. Test edge cases and error conditions
5. Keep tests focused and independent
6. Include tests for quality gates

## Continuous Integration

The test suite is designed to be run as part of a continuous integration pipeline to ensure code quality and prevent regressions.