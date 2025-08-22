# Test Generator

This directory contains the implementation of the Test Generator component, which creates unit tests.

## Responsibilities

- Receive newly generated Godot files and analyst's report
- Write comprehensive suite of unit tests using gdUnit4 framework
- Ensure comprehensive test coverage for public methods and signals
- Use qwen-code CLI agent for all test generation tasks

## Key Components

- `test_generator.py` - Main implementation of the Test Generator component

## Integration with Other Systems

The Test Generator integrates with several systems:

- **Validation System**: Works closely with the Validation Engineer for test quality gates
- **Refactoring Specialist**: Receives newly generated code for test creation
- **Quality Assurance**: Provides tests for validation and quality assurance processes