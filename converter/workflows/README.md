# Workflows

This directory contains the process definitions for orchestrating the migration.

The system supports two workflow models:

## Current Implementation

- `sequential_workflow.py` - Sequential workflow implementation for atomic coding tasks
- `hierarchical_workflow.py` - Hierarchical workflow implementation for managing overall migration

## Key Components

- `sequential_workflow.py` - Sequential workflow processor for atomic tasks
- `hierarchical_workflow.py` - Hierarchical workflow processor for complex tasks

## Integration with Other Systems

The workflow system integrates with several systems:

- **Orchestrator**: Core workflow execution engine
- **Graph System**: Uses dependency graph for intelligent task ordering
- **Validation System**: Incorporates test quality gates for rigorous validation
- **HITL System**: Implements human oversight for critical decisions