# Refactoring Specialist

This directory contains the implementation of the Refactoring Specialist component, which generates Godot files.

## Responsibilities

- Receive source files and analyst's JSON report
- Generate equivalent idiomatic Godot files (.gd, .tscn, .tres)
- Strictly adhere to guidance artifacts (style guide, templates, gold standards)
- Use qwen-code CLI agent for all code generation tasks

## Key Components

- `refactoring_specialist.py` - Main implementation of the Refactoring Specialist component

## Integration with Other Systems

The Refactoring Specialist integrates with several systems:

- **Prompt Engineering**: Receives precisely formatted prompts from the Prompt Engineering component
- **Validation System**: Incorporates feedback from the Validation Engineer for iterative improvements
- **Context Engineering**: Strictly adheres to guidance artifacts for consistent output quality