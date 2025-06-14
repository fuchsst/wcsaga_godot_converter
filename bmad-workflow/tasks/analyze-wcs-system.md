# Task: Analyze WCS System

## Objective
Perform a comprehensive analysis of a specific Wing Commander Saga (WCS) system by examining the C++ source code to understand its functionality, architecture, and implementation details. This analysis will serve as the foundation for designing the equivalent Godot implementation.

Read existing `...-analysis.md` in `.ai\docs\` related to the requested work package before you begin.

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
- Locate relevant source files in `source/code/` directory.
- Identify key classes, functions, and data structures.
- Compile a comprehensive list of all source files (.cpp, .h) constituting the system.
- For each identified file, map out its direct dependencies (files it includes) and identify which other files within the system (or key external systems) include or reference it (i.e., its dependents).
- Document the system's entry points and main interfaces.

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

Create a comprehensive analysis document and two supplementary documents in `bmad-artifacts/docs/[epic-name]/`. The filenames should be `analysis.md`, `source-files.md`, and `source-dependencies.md`.

The main analysis document, `analysis.md`, should follow this structure:

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
- [ ] The analysis passes all criteria in the `bmad-workflow/checklists/wcs-analysis-quality-checklist.md`.
- [ ] All output documents (`analysis.md`, `source-files.md`, `source-dependencies.md`) have been created in the correct epic folder.
- [ ] The analysis is actionable for the PRD and Architecture phases.

### Supplementary Document 1: Source Files

A markdown file named `source-files.md` listing all identified source code files relevant to the analyzed system.

**Format:**
```markdown
# WCS System: [System Name] - Source Files List

- `path/to/file1.cpp`: Short description of file 1
- `path/to/file1.h`: Short description of file 2
- `path/to/another/module/file2.cpp`: Short description of file 3
- `path/to/another/module/file2.h`: Short description of file 4
- ...
```

### Supplementary Document 2: Source Dependencies

A markdown file named `source-dependencies.md` detailing the usage relationships between files. For each key file in the system, list the other files that include or call functions/classes from it.

```markdown
# WCS System: [System Name] - Source Dependencies (Used By)

## File: `path/to/file1.h` included/used by:
- `path/to/dependent_file_A.cpp`
- `path/to/dependent_file_B.h`
- ...

## File: `path/to/file1.cpp` included/used by:
- `path/to/dependent_file_A.cpp`
- ...
```

## Workflow Integration
- **Input**: System identification and scope from user or Conversion Manager
- **Output**: Detailed analysis documents (`analysis.md`, `source-files.md`, `source-dependencies.md`) in `bmad-artifacts/docs/[epic-name]/`
- **Next Steps**: Analysis feeds into Godot Architect for system design
- **Dependencies**: May require additional analysis of related systems
- **Epic Update**: After completing analysis, update the parent epic document in `bmad-artifacts/epics/[epic-name].md` with analysis status and key findings

## Success Criteria
- Analysis provides sufficient detail for architectural design
- All critical functionality is documented and understood
- Conversion challenges and opportunities are clearly identified
- Document serves as reliable reference throughout implementation
- Analysis enables accurate effort estimation for conversion

## Notes for Larry (WCS Analyst)
- Don't just read the code - understand the intent and design decisions.
- Look for comments and documentation within the source code.
- Pay attention to performance-critical sections and optimizations.
- Consider the historical context - some patterns may be legacy.
- Focus on aspects that will impact the Godot conversion.
- When in doubt, dig deeper - surface-level analysis isn't sufficient.
- For the `-source-dependencies.md` file, focus on identifying how key components of the analyzed system are utilized by other parts of the codebase. This 'used by' information is crucial for understanding the impact of changes. Tools like `grep` for include statements or IDE 'find usages' features can be helpful, but manual tracing will likely be needed. Prioritize accuracy for the most critical files of the system under analysis.
