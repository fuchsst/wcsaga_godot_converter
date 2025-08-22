# Human-in-the-Loop (HITL) Integration

This directory contains components for integrating human oversight into the migration process, implementing the proactive HITL patterns recommended in the architectural document.

## Overview

The HITL system implements proactive human-in-the-loop patterns for critical decision points in the migration process. It addresses the overly simplistic and reactive HITL model by implementing sophisticated patterns that prevent errors and resolve ambiguity earlier.

## Key Components

- `hitl_integration.py` - Legacy HITL integration implementation
- `langgraph_hitl.py` - LangGraph-based HITL implementation with native interrupt capabilities

## Proactive HITL Patterns

The system implements several proactive HITL patterns as recommended in the architectural review:

1. **Interrupt & Resume**: Request mandatory human approval gates for critical-path migrations before they can proceed. This pattern is implemented using LangGraph's native interrupt capabilities.

2. **Human-as-a-Tool**: Enable agents to request human expertise when faced with ambiguity. This pattern allows the system to actively request human expertise as a high-precision "tool" callable by the autonomous system.

## LangGraph Implementation Details

The `langgraph_hitl.py` module specifically implements:

- **Interrupt & Resume Pattern**: For critical path validation of foundational C++ modules
  - Tagging critical tasks in task_queue.yaml with `requires_human_approval: true`
  - Creating approval nodes that call `interrupt()` with structured payloads
  - Resuming execution with `Command(resume=True/False)` based on human approval

- **Human-as-a-Tool Pattern**: For ambiguity resolution in the Codebase Analyst node
  - Confidence scoring for complex code constructs like SEXP expressions
  - Conditional interruption when confidence falls below thresholds
  - Resuming with expert data using `Command(resume={'resolved_logic': '...'})`

## Integration with LangGraph Orchestrator

The HITL system integrates directly with the LangGraph orchestrator:

- **Conditional Edges**: Route to human approval nodes based on task flags
- **Node Interruptions**: Pause workflow execution awaiting human input
- **Command Resumption**: Resume workflows with human-provided data
- **Structured Payloads**: Provide rich context for human reviewers

## Migration Scenario Implementation

| Migration Scenario | Proposed HITL Pattern | LangGraph Implementation |
| :---- | :---- | :---- |
| Migrating physics_core.cpp | Interrupt & Resume | Add `requires_human_approval: true` to task. Conditional edge routes to human_approval_gate node after successful validation. This node calls `interrupt()`. Resume with `Command(resume=True)`. |
| Codebase Analyst encounters unknown SEXP | Human-as-a-Tool | Node calculates parsing confidence score. If low, calls `interrupt()` with ambiguous code snippet. Resume with `Command(resume={'...'})`, providing correct logic. |
| Refactoring Specialist needs novel scene structure | Human-as-a-Tool (Architectural Guidance) | Node recognizes deviation from known patterns. Invokes `interrupt()` presenting proposed node hierarchy. Resume with human validation. |

## Integration with Other Systems

The HITL system integrates with several other systems:

- **Orchestrator**: Request human input at critical decision points through LangGraph interrupts
- **Validation System**: Escalate critical validation issues for human review with structured context
- **Codebase Analyst**: Request human expertise for ambiguous code with confidence scoring
- **Quality Assurance**: Request human review of AI-generated outputs before critical merges