# Agent Definitions

This directory contains the base agent definitions for the migration system.

## Overview

The migration system uses a multi-agent approach where each agent has specific responsibilities in the migration process. While the system was initially designed to use the DeepSeek V3.1 model for high-level cognitive tasks, the current implementation focuses on specialized Python components that work together to accomplish the migration.

## Agent Components

The system consists of several specialized agents:

- **Codebase Analyst** - Analyzes the source C++ codebase to identify dependencies, modules, and architectural patterns
- **Prompt Engineering Agent** - Creates precise prompts for the CLI coding agents
- **Refactoring Specialist** - Converts C++ code to GDScript using the qwen-code CLI tool
- **Test Generator** - Creates comprehensive unit tests for the migrated code
- **Validation Engineer** - Validates the migrated code against quality gates

## Implementation

Rather than using separate YAML configuration files for each agent, the agents are implemented as Python classes in their respective modules:

- `analyst/` - Codebase Analyst implementation
- `prompt_engineering/` - Prompt Engineering Agent implementation
- `refactoring/` - Refactoring Specialist implementation
- `test_generator/` - Test Generator implementation
- `validation/` - Validation Engineer implementation

## Integration with Other Systems

The agents integrate with several systems:

- **Orchestrator** - Coordinates the workflow between agents
- **Context Engineering** - Uses guidance artifacts for consistent output quality
- **Validation System** - Provides feedback for iterative improvements
- **HITL System** - Implements human oversight for critical decisions