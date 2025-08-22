# State Machine Orchestrator

This directory contains the custom state machine implementation for deterministic bolt cycles in the migration process.

## Overview

The state machine system implements a custom state machine-based orchestrator for deterministic bolt cycles. It provides:

1. **Deterministic Execution**: Explicit state transitions for predictable execution
2. **Bolt Management**: Manage individual bolt cycles with proper state tracking
3. **Error Handling**: Handle errors with retry and escalation mechanisms
4. **Task Queue Management**: Manage task queues with proper status tracking

## Key Components

- `core.py` - Core state machine orchestrator implementation
- `task_queue.py` - Task queue management with persistence
- `bolt_executor.py` - Bolt execution implementation

## Integration with Other Systems

The state machine system integrates with several other systems:

- **Orchestrator**: Core execution engine for the migration process
- **Graph System**: Use dependency graph for task ordering
- **Validation System**: Integrate validation results into state transitions
- **HITL System**: Request human input at critical decision points