# Code Analyst Component

This directory contains the implementation of the Code Analyst component, which operates as a node in the LangGraph workflow to analyze the source codebase.

## Responsibilities

- Receive a task from the LangGraph state (e.g., "GTC Fenris")
- Analyze all related source files from the state
- Produce a structured JSON report classifying components
- Identify dependencies and architectural patterns
- Update the LangGraph state with analysis results

## Key Components

- `codebase_analyst.py` - Main implementation of the Codebase Analyst component as a LangGraph node
- `__init__.py` - Package initialization file
- `example_usage.py` - Example usage of the Codebase Analyst
- `test_codebase_analyst.py` - Unit tests for the Codebase Analyst

## Implementation Details

The Codebase Analyst is designed to handle the specific file formats used in the Wing Commander Saga project:

1. **Table Files (.tbl, .tbm)** - Parse entity data and properties
2. **Model Files (.pof)** - Extract 3D model metadata including subsystems and hardpoints
3. **Source Files (.cpp, .h)** - Analyze C++ classes, methods, and dependencies
4. **Mission Files (.fs2)** - Parse SEXP expressions for mission logic

The component produces a structured JSON report that categorizes components according to the Architectural Mapping Table:
- **Data** - Table files and other data definitions
- **Behavior** - Source code and mission logic
- **Visuals** - 3D model files
- **Physics** - Physical properties and behaviors

## LangGraph Integration

The component operates as a node in the LangGraph workflow:

1. Receives source_code_content from the graph state
2. Performs analysis on the source files
3. Returns analysis_report to update the graph state
4. Can trigger HITL interventions for ambiguous code through interrupts

## Usage

The component is typically invoked by the LangGraph orchestrator as part of the migration workflow:

```python
from converter.analyst import CodebaseAnalyst

analyst = CodebaseAnalyst()
analysis_report = analyst.analyze_entity("GTC Fenris", [
    "source/tables/ships.tbl",
    "source/models/fenris.pof", 
    "source/code/ship.cpp"
])
```