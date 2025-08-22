# Orchestrator Agent

This directory contains the implementation of the Orchestrator agent, which serves as the project manager.

Based on the "Agentic Migration with CLI Agents" document, this agent is powered by the **DeepSeek V3.1** model and follows these principles:

## Responsibilities
- Ingest the migration plan
- Shard tasks into atomic units
- Manage the task queue
- Orchestrate the workflow between other agents
- Dynamically select workflow models (sequential or hierarchical) based on task complexity
- Use DeepSeek V3.1 model for advanced reasoning and planning

## Key Components

- `main.py` - Main orchestrator implementation
- `langgraph_orchestrator.py` - LangGraph orchestrator with state machine workflow
- `state_machine/` - Custom state machine implementation for deterministic bolt cycles
  - `core.py` - Core state machine orchestrator
  - `task_queue.py` - Task queue management
  - `bolt_executor.py` - Bolt execution implementation

## Workflow Process

The orchestrator operates with a robust workflow:

1. **Dependency Analysis**: Uses the graph system to analyze codebase dependencies
2. **Migration Planning**: Creates migration sequence based on dependency analysis
3. **Task Execution**: Executes tasks in deterministic bolt cycles
4. **Quality Validation**: Validates results with quality gates
5. **HITL Review**: Requests human review for critical components

## Integration with Other Systems

The orchestrator integrates with several systems:

- **Graph System**: Uses the dependency graph for intelligent task ordering
- **Validation System**: Incorporates test quality gates for rigorous validation
- **HITL System**: Implements human oversight for critical decisions