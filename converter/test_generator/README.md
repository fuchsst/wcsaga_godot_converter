# Test Generator Agent

This directory contains the implementation of the Test Generator agent, which creates unit tests.

Based on the "Agentic Migration with CLI Agents" document, this agent is specifically configured to work with the **qwen-code** CLI agent:

## Responsibilities
- Receive newly generated Godot files and analyst's report
- Write comprehensive suite of unit tests using GUT framework
- Ensure 100% test coverage for public methods and signals
- Use qwen-code CLI agent for all test generation tasks

## Key Components

- `test_generator.py` - Main implementation of the Test Generator agent

## Integration with Other Systems

The Test Generator integrates with several systems:

- **Validation System**: Works closely with the Validation Engineer for test quality gates
- **Refactoring Specialist**: Receives newly generated code for test creation
- **Quality Assurance**: Provides tests for validation and quality assurance processes