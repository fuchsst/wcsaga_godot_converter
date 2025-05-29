# WCS System Analysis Quality Checklist

## Purpose
This checklist ensures that the analysis of a Wing Commander Saga (WCS) C++ system, performed by the WCS Analyst (Larry), is comprehensive, accurate, and provides a solid foundation for subsequent PRD creation and Godot architecture design.

## Reviewer: Larry (WCS Analyst) before handoff, potentially peer-reviewed by Mo (Godot Architect) or Curly (Conversion Manager) for clarity and completeness from their perspectives.
**Usage**: Run this checklist before marking a WCS system analysis as complete and ready for the next BMAD phase.

## I. Foundation & Scope
- [ ] **System Name & Scope**: Clearly defined in all output documents (`-analysis.md`, `-source-files.md`, `-source-dependencies.md`).
- [ ] **Analysis Depth**: Analysis matches the required depth (overview, detailed, deep-dive).
- [ ] **Prerequisites Met**: Access to source code confirmed, basic understanding demonstrated.

## II. Main Analysis Document (`[system-name]-analysis.md`)

### A. System Overview & Executive Summary
- [ ] **Executive Summary**: Provides a concise overview of the system and key findings.
- [ ] **Purpose**: Clearly states what the system does.
- [ ] **Scope**: Boundaries and responsibilities of the system are well-defined.
- [ ] **Key Files (Summary)**: Mentions the primary source files analyzed (detailed list in supplementary doc).
- [ ] **Dependencies (Summary)**: Briefly lists other major WCS systems this system depends on or interacts with.

### B. Architecture Analysis
- [ ] **Class Structure**: Key classes and their relationships (inheritance, composition) documented.
- [ ] **Data Flow**: Describes how data moves through the system.
- [ ] **Key Algorithms**: Important algorithms and computational approaches detailed.

### C. Implementation Details
- [ ] **Core Functions**: Critical functions documented with signatures and purposes.
- [ ] **State Management**: How system state is maintained and updated is explained.
- [ ] **Performance Characteristics**: Notes on memory usage, computational complexity, potential bottlenecks.
- [ ] **Error Handling**: How the system handles edge cases and failures is described.
- [ ] **Design Patterns**: Common C++ design patterns used are identified.
- [ ] **Memory Management**: Notes on object creation, management, and destruction.
- [ ] **Threading/Concurrency**: Any multi-threading aspects are noted.
- [ ] **Resource Management**: How assets/resources are handled is described.

### D. Game-Specific Considerations
- [ ] **Gameplay Impact**: How the system affects player experience is analyzed.
- [ ] **Performance Requirements**: Original real-time constraints and optimization needs identified.
- [ ] **Integration Points**: How it connects with other game systems is detailed.
- [ ] **Configuration**: Any data-driven or configurable aspects are documented.

### E. Conversion Considerations
- [ ] **Godot Mapping Opportunities**: Potential ways to map WCS concepts to Godot systems are suggested.
- [ ] **Potential Challenges**: Difficult aspects for conversion are highlighted.
- [ ] **Preservation Requirements**: What must be maintained for gameplay fidelity is specified.

### F. Recommendations & References
- [ ] **Architecture Approach (Initial Thoughts)**: Tentative suggestions for Godot architecture.
- [ ] **Implementation Priority (Initial Thoughts)**: Ideas on what to implement first.
- [ ] **Risk Assessment (Initial Thoughts)**: Potential issues for conversion.
- [ ] **Source Files Referenced**: Main document appropriately refers to the detailed list in `-source-files.md`.
- [ ] **Key Functions Listed**: Important function signatures are included or referenced.
- [ ] **External Documentation**: Any relevant WCS documentation used is cited.

## III. Supplementary Document 1 (`[system-name]-source-files.md`)
- [ ] **Completeness**: All source files (.cpp, .h) relevant to the analyzed system's scope are listed.
- [ ] **Accuracy**: File paths are correct relative to the `source/` directory.
- [ ] **Descriptions**: Each file has a brief, accurate description of its purpose/content.
- [ ] **Organization**: Files are logically grouped (e.g., core system, utilities) if applicable.

## IV. Supplementary Document 2 (`[system-name]-source-dependencies.md`)
- [ ] **Key Files Covered**: The most important files of the system are analyzed for their "used by" dependencies.
- [ ] **"Used By" Information**: For each key file, lists other files that include it or call its functions/classes.
- [ ] **Clarity**: Dependency information is presented in a clear and understandable format.
- [ ] **Scope of Dependencies**: Focuses on dependencies within the system and key interactions with other major WCS systems.
- [ ] **Accuracy**: "Used by" information is accurate to the best of Larry's ability using available tools (grep, IDE, manual tracing).

## V. Overall Quality & Process
- [ ] **Thoroughness**: Analysis reflects a deep dive appropriate to the defined scope and depth.
- [ ] **Clarity & Readability**: All documents are well-written and easy to understand by other team members (Mo, Curly, Dev).
- [ ] **Actionability**: The analysis provides a solid, actionable basis for PRD creation and Godot architecture design.
- [ ] **Command-Line Tools**: Evidence or notes suggest effective use of command-line tools for exploration where appropriate.
- [ ] **Code Snippet Readiness**: Larry is prepared to provide specific code snippets to Mo if requested.
- [ ] **File Naming**: The output documents `analysis.md`, `source-files.md`, and `source-dependencies.md` in `.ai/docs/[epic-name]/`.
- [ ] **Epic Update**: Parent epic document in `.ai/epics/[epic-name].md` updated with analysis status and key findings summary.

## Checklist Completion

**WCS Analyst (Larry)**: _________________ **Date**: _________________
**System Analyzed**: ____________________________________

**Review Result**:
- [ ] **ANALYSIS COMPLETE & APPROVED**: All checklist items satisfied. Ready for handoff to Godot Architect and Conversion Manager.
- [ ] **NEEDS REVISION**: Specific issues identified below must be addressed.

**Critical Issues / Areas for Revision**:
1.  _______________________________________________________________________________
2.  _______________________________________________________________________________
3.  _______________________________________________________________________________

**Recommendations for Future Analyses**:
___________________________________________________________________________________
___________________________________________________________________________________

---
**Critical Reminder**: A thorough and accurate WCS system analysis is the bedrock of a successful conversion. Errors or omissions here can propagate through the entire BMAD workflow.
