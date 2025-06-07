# Command: Analyze WCS Code

## Objective
Guide the WCS Analyst (Larry) to perform a comprehensive analysis of a specific Wing Commander Saga (WCS) system by examining its C++ source code. This analysis will serve as the foundation for designing the equivalent Godot implementation.

You are initiating WCS code analysis for the system: $ARGUMENTS (e.g., "Player Ship Movement", "Weapon Systems")

## Analysis Process

### 1. Load BMAD Framework
- Load the WCS Analyst persona (Larry) from `bmad-workflow/personas/wcs-analyst.md`.
- Reference the WCS system analysis task from `bmad-workflow/tasks/analyze-wcs-system.md`.

### 2. Prerequisites Check
Before starting analysis, Larry must verify:
- [ ] Access to WCS source code in the `source/` submodule is available.
- [ ] The specific **System Name** to analyze has been provided (via $ARGUMENTS).
- [ ] **Scope Definition** (clear boundaries of what aspects to focus on) has been provided or can be clarified with the user/Conversion Manager.
- [ ] **Analysis Depth** (overview, detailed, or deep-dive) has been specified or can be clarified.

### 3. Analysis Steps (as per `bmad-workflow/tasks/analyze-wcs-system.md`)
Larry will follow the structured approach outlined in the task, including:

1.  **System Identification**:
    *   Locate relevant source files in `source/code/`.
    *   Identify key classes, functions, and data structures.
    *   Compile a comprehensive list of all source files (.cpp, .h) for the system.
    *   Map out file dependencies (includes and "used by").
    *   Document entry points and main interfaces.
2.  **Code Structure Analysis**:
    *   Document class hierarchy, key functions, data flow, state management, and external dependencies.
3.  **Functionality Documentation**:
    *   Detail core features, input/output, algorithms, performance characteristics, and error handling.
4.  **Architecture Patterns**:
    *   Identify design patterns, memory management, threading, and resource management.
5.  **Game-Specific Considerations**:
    *   Analyze gameplay impact, performance requirements, integration points, and configuration.
6.  **Utilize Command-Line Tools**:
    *   Employ Bash commands (as detailed in Larry's persona) for efficient code exploration, pattern matching, and dependency tracing within the `source/` C++ codebase.

### 4. Quality Validation
Larry must ensure the analysis meets the criteria in the **WCS System Analysis Quality Checklist** (`bmad-workflow/checklists/wcs-analysis-quality-checklist.md`). This includes verifying:
- [ ] Completeness and accuracy of the main analysis document (`[system-name]-analysis.md`).
- [ ] Completeness and accuracy of the supplementary `[system-name]-source-files.md`.
- [ ] Thoroughness and accuracy of the supplementary `[system-name]-source-dependencies.md`.
- [ ] All sections of the checklist are satisfactorily addressed.

### 5. Output Requirements
Produce three documents in the `bmad-artifacts/docs/` directory:
1.  **Main Analysis Document**: `[system-name]-analysis.md` (following the structure in the task).
2.  **Source Files List**: `[system-name]-source-files.md` (listing relevant .cpp and .h files with brief descriptions).
3.  **Source Dependencies Map**: `[system-name]-source-dependencies.md` (mapping how key files are included/used by others).

## Critical Reminders for Larry (WCS Analyst)
- Don't just read the code; understand the intent and design decisions.
- Utilize your command-line analysis skills (grep, find, etc.) extensively.
- Pay attention to performance-critical sections and legacy patterns.
- Focus on aspects that will directly impact the Godot conversion.
- Be prepared to provide specific C++ code snippets to Mo (Godot Architect) if requested for architectural clarification.
- Ensure the supplementary file lists and dependency maps are thorough for the analyzed system's scope.

## BMAD Workflow Compliance
- **Input**: System Name, Scope Definition, and Analysis Depth from user or Conversion Manager.
- **Process**: Deep C++ code analysis of the specified WCS system within the `source/` submodule.
- **Output**: Three analysis documents (`[system-name]-analysis.md`, `[system-name]-source-files.md`, `[system-name]-source-dependencies.md`) in `bmad-artifacts/docs/`.
- **Next Steps**: The completed analysis package feeds into the Godot Architect (Mo) for system design and the Conversion Manager (Curly) for PRD creation.

Begin WCS code analysis for system: $ARGUMENTS
