# Code Review Checklist

## Reviewers: QA Specialist (QA), Godot Architect (Mo)
**Story ID**: [Story Being Reviewed]
**Date**: [Date]
**Commit/Branch**: [Link or ID]

### 1. Story & Requirements Adherence
- [ ] All Acceptance Criteria (ACs) from the story are verifiably met.
- [ ] The implementation fulfills the overall goal and intent of the user story.
- [ ] Functionality matches the story description and technical requirements.
- [ ] Any deviations from the story are documented and justified.

### 2. Architecture & Design (Godot Architect Focus)
- [ ] Adherence to the approved system architecture document.
- [ ] Correct use of Godot-specific patterns (nodes, scenes, signals, resources).
- [ ] Scene structure is logical, efficient, and follows best practices (e.g., composition over inheritance).
- [ ] Node hierarchy is appropriate, not overly complex, and uses correct node types.
- [ ] Signals are used effectively for decoupling; parameters are typed and documented.
- [ ] Data flow and state management are clear, robust, and follow architectural guidelines.
- [ ] Code is modular, and components are reusable where appropriate.
- [ ] No unnecessary deviations from established design patterns or architectural principles.
- [ ] File and directory structure for new/modified code aligns with Godot and project conventions.

### 3. Code Quality & GDScript Best Practices (QA Specialist & Architect)
- [ ] **Static Typing**: 100% static typing is enforced (variables, function parameters, return types). No `Variant` types unless explicitly justified.
- [ ] **Naming Conventions**: Adherence to GDScript naming conventions (PascalCase for classes/nodes/`class_name`, snake_case for functions/variables/signals).
- [ ] `class_name` used for all reusable classes/scripts, and is globally unique.
- [ ] **Readability**: Code is clear, concise, and easy to understand. Avoid overly complex expressions or logic.
- [ ] **Comments & Docstrings**:
    - Public functions, signals, and classes have clear, informative docstrings explaining purpose, parameters, and return values.
    - Complex or non-obvious logic is adequately explained with inline comments.
    - Comments are up-to-date, accurate, and add value (not just restating the code).
- [ ] **SOLID Principles**: Code generally adheres to SOLID principles where applicable.
- [ ] **DRY Principle**: "Don't Repeat Yourself" - code duplication is minimized through functions, classes, or components.
- [ ] **Error Handling**:
    - Potential errors (e.g., null references, failed operations, invalid input) are identified and handled gracefully.
    - Error messages are informative and user-friendly where appropriate.
    - No silent failures; issues are logged or reported.
- [ ] **Resource Management**: Proper use of `preload`, `load`; resources are freed/cleaned up if necessary (e.g., manual `free()` for non-Node objects if not managed by parent, disconnecting signals).
- [ ] **Magic Numbers/Strings**: Minimized; constants or exported variables used instead.

### 4. Performance
- [ ] No obvious performance bottlenecks (e.g., large loops in `_process`, inefficient algorithms, excessive node creation/deletion).
- [ ] Memory usage seems reasonable; no obvious memory leaks or excessive allocations.
- [ ] Optimizations are applied where necessary without sacrificing clarity; premature optimization is avoided.
- [ ] Resource loading/unloading is handled efficiently (e.g., background loading for large assets if needed).

### 5. Testability & Unit Tests
- [ ] Code is structured in a way that facilitates unit testing (e.g., dependencies injectable or mockable).
- [ ] Unit tests (gdUnit4) are present for key logic and cover acceptance criteria.
- [ ] Project compiles and all tests pass
- [ ] Test scripts follow the same folder structure in the `target/tests/` folder as the the tested script (e.g. the test script for `target/scripts/ships/core/base_ship.gd` is placed in `target/tests/ships/core/base_ship.gd`)
- [ ] Unit tests are passing and provide meaningful assertions.
- [ ] Test coverage is adequate for the complexity and criticality of the code.
- [ ] Tests are easy to understand and maintain.

### 6. Maintainability & Extensibility
- [ ] Code is easy to modify and extend without major refactoring.
- [ ] Configuration is separated from logic (e.g., using exported variables, `Resource` files, configuration singletons).
- [ ] Code is organized logically within scripts and across the project structure.
- [ ] Dependencies are managed clearly.

### 7. WCS-Godot Specifics
- [ ] Preserves essential WCS gameplay feel and mechanics (if applicable to the story).
- [ ] Adheres to any project-specific coding standards, helper functions, or global systems.
- [ ] Integration with other converted systems (if any) is correct, robust, and uses defined interfaces.

### 8. Security (if applicable, e.g., for networking, file I/O)
- [ ] No obvious security vulnerabilities (e.g., related to input validation, data handling).

### Overall Assessment
- [ ] **Clarity**: Is the code's purpose and logic clear?
- [ ] **Correctness**: Does the code do what it's supposed to do, correctly and reliably?
- [ ] **Robustness**: Is the code resilient to errors, invalid inputs, and edge cases?
- [ ] **Efficiency**: Is the code reasonably performant for its context?
- [ ] **Maintainability**: Will this code be easy to understand, debug, and update in the future?

**Summary of Key Findings / Action Items**:
-
-

**Recommendation**:
- [ ] Approve - Ready for merge/next step.
- [ ] Approve with minor revisions (list below, Dev to address).
- [ ] Requires major revisions (list below, potentially new stories/tasks needed).
