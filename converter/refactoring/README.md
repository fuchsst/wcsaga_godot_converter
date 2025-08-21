# Refactoring Specialist Agent

This directory contains the implementation of the Refactoring Specialist agent, which generates Godot files.

Based on the "Agentic Migration with CLI Agents" document, this agent is specifically configured to work with the **qwen-code** CLI agent:

Responsibilities:
- Receive source files and analyst's JSON report
- Generate equivalent idiomatic Godot files (.gd, .tscn, .tres)
- Strictly adhere to guidance artifacts (style guide, templates, gold standards)
- Use qwen-code CLI agent for all code generation tasks