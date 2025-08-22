# Refactoring Specialist Agent

This directory contains the implementation of the Refactoring Specialist agent, which generates Godot files.

Based on the "Agentic Migration with CLI Agents" document, this agent is specifically configured to work with the **qwen-code** CLI agent:

## Responsibilities
- Receive source files and analyst's JSON report
- Generate equivalent idiomatic Godot files (.gd, .tscn, .tres)
- Strictly adhere to guidance artifacts (style guide, templates, gold standards)
- Use qwen-code CLI agent for all code generation tasks

## Key Components

- `refactoring_specialist.py` - Main implementation of the Refactoring Specialist agent

## Integration with Other Systems

The Refactoring Specialist integrates with several systems:

- **Prompt Engineering**: Receives precisely formatted prompts from the Prompt Engineering Agent
- **Validation System**: Incorporates feedback from the Validation Engineer for iterative improvements
- **Context Engineering**: Strictly adheres to guidance artifacts for consistent output quality