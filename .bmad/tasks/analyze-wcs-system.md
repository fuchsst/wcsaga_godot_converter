# Task: Analyze WCS System

## Objective
Perform a comprehensive analysis of a specific Wing Commander Saga (WCS) system by examining the C++ source code to understand its functionality, architecture, and implementation details. This analysis will serve as the foundation for designing the equivalent Godot implementation.

## Prerequisites
- Access to WCS source code in `source/` submodule
- Specific system or component identified for analysis
- Basic understanding of C++ and game architecture patterns

## Input Requirements
- **System Name**: The specific WCS system to analyze (e.g., "Player Ship Movement", "Weapon Systems", "AI Behavior")
- **Scope Definition**: Clear boundaries of what aspects to focus on
- **Analysis Depth**: Level of detail required (overview, detailed, or deep-dive)

## Analysis Process

### 1. System Identification
- Locate relevant source files in `source/code/` directory
- Identify key classes, functions, and data structures
- Map out file dependencies and includes
- Document the system's entry points and main interfaces

### 2. Code Structure Analysis
- **Class Hierarchy**: Document inheritance relationships
- **Key Functions**: Identify critical methods and their purposes
- **Data Flow**: Trace how data moves through the system
- **State Management**: Understand how system state is maintained
- **External Dependencies**: Identify connections to other WCS systems

### 3. Functionality Documentation
- **Core Features**: What the system does and how it works
- **Input/Output**: What data the system consumes and produces
- **Algorithms**: Key algorithms and computational approaches used
- **Performance Characteristics**: Memory usage, computational complexity
- **Error Handling**: How the system handles edge cases and failures

### 4. Architecture Patterns
- **Design Patterns**: Identify common patterns used (Observer, Factory, etc.)
- **Memory Management**: How objects are created, managed, and destroyed
- **Threading**: Any multi-threading or concurrency considerations
- **Resource Management**: How assets and resources are handled

### 5. Game-Specific Considerations
- **Gameplay Impact**: How the system affects player experience
- **Performance Requirements**: Real-time constraints and optimization needs
- **Integration Points**: How it connects with other game systems
- **Configuration**: Any data-driven or configurable aspects

## Output Format

Create a comprehensive analysis document in `.ai/docs/` with the following structure:

```markdown
# WCS System Analysis: [System Name]

## Executive Summary
[Brief overview of the system and key findings]

## System Overview
- **Purpose**: What this system does
- **Scope**: Boundaries and responsibilities
- **Key Files**: Primary source files analyzed
- **Dependencies**: Other systems this depends on

## Architecture Analysis
### Class Structure
[Document key classes and their relationships]

### Data Flow
[Describe how data moves through the system]

### Key Algorithms
[Detail important algorithms and approaches]

## Implementation Details
### Core Functions
[Document critical functions with signatures and purposes]

### State Management
[How system state is maintained and updated]

### Performance Characteristics
[Memory usage, computational complexity, bottlenecks]

## Conversion Considerations
### Godot Mapping Opportunities
[How this could map to Godot systems]

### Potential Challenges
[Difficult aspects for conversion]

### Preservation Requirements
[What must be maintained for gameplay fidelity]

## Recommendations
### Architecture Approach
[Suggested Godot architecture patterns]

### Implementation Priority
[What to implement first, dependencies]

### Risk Assessment
[Potential issues and mitigation strategies]

## References
- **Source Files**: List of all files examined
- **Key Functions**: Important function signatures
- **External Documentation**: Any relevant WCS documentation
```

## Quality Checklist
- [ ] All relevant source files identified and examined
- [ ] Key classes and functions documented with file locations
- [ ] Data flow and system interactions clearly described
- [ ] Performance characteristics and constraints identified
- [ ] Godot conversion considerations addressed
- [ ] Specific code examples and function signatures included
- [ ] Analysis is actionable for architecture and implementation phases

## Workflow Integration
- **Input**: System identification and scope from user or Conversion Manager
- **Output**: Detailed analysis document in `.ai/docs/[system-name]-analysis.md`
- **Next Steps**: Analysis feeds into Godot Architect for system design
- **Dependencies**: May require additional analysis of related systems

## Success Criteria
- Analysis provides sufficient detail for architectural design
- All critical functionality is documented and understood
- Conversion challenges and opportunities are clearly identified
- Document serves as reliable reference throughout implementation
- Analysis enables accurate effort estimation for conversion

## Notes for Larry (WCS Analyst)
- Don't just read the code - understand the intent and design decisions
- Look for comments and documentation within the source code
- Pay attention to performance-critical sections and optimizations
- Consider the historical context - some patterns may be legacy
- Focus on aspects that will impact the Godot conversion
- When in doubt, dig deeper - surface-level analysis isn't sufficient
