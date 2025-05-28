# Task: Review Code Implementation

## Objective
Conduct a thorough and collaborative review of a specific implemented user story to ensure it meets quality standards, adheres to architectural guidelines, fulfills story requirements, and aligns with Godot best practices.

## Personas Involved
- **Lead**: QA Specialist (QA)
- **Collaborator**: Godot Architect (Mo)

## Prerequisites
- User story marked as "Implementation Complete" or "Ready for Review".
- Access to the implemented code (e.g., specific branch/commit in `target/` submodule).
- Access to the user story file (`.ai/stories/[epic-name]/[story-id].md`).
- Access to the approved architecture document (`.ai/docs/[epic-name]/architecture.md`).

## Input Requirements
- **Story ID / Path**: The identifier or path to the user story file being reviewed.
- **Implemented Code Location**: Reference to the specific commit, branch, or code version to be reviewed.

## Review Process

1.  **Context Gathering (QA & Mo)**:
    *   Thoroughly review the user story, its acceptance criteria, and any associated technical notes.
    *   Review the relevant sections of the approved system architecture document.

2.  **Code Examination & Checklist Application (QA & Mo)**:
    *   Systematically review the implemented code using the `.bmad/checklists/code-review-checklist.md`.
    *   **Godot Architect (Mo) Focus**:
        *   Adherence to approved architecture and design patterns.
        *   Correct and optimal use of Godot nodes, scenes, and signals.
        *   Overall structural integrity and Godot-centric best practices.
        *   Performance implications of the design and implementation.
    *   **QA Specialist (QA) Focus**:
        *   Fulfillment of all story acceptance criteria.
        *   Adherence to GDScript standards (static typing, naming, clarity).
        *   Testability of the code and adequacy of existing unit tests.
        *   Robustness, error handling, and edge case consideration.
        *   Clarity of comments and code documentation.
        *   Overall quality and maintainability.

3.  **Collaborative Documentation (QA & Mo)**:
    *   Jointly fill out the `.bmad/templates/code-review-document-template.md`.
    *   Clearly document all findings, including both positive aspects and areas for improvement.
    *   Categorize issues by severity (e.g., Critical, Major, Minor, Suggestion).

4.  **Actionable Outcome Definition (QA & Mo)**:
    *   For identified issues, propose concrete actions:
        *   Creation of new user stories for significant refactoring or missed requirements.
        *   Modifications or tasks for the original story or related stories.
        *   Direct fixes for minor issues.
    *   Provide an overall assessment (e.g., Approved, Approved with Conditions, Requires Major Rework).

## Output Requirements
- A comprehensive review document named `[story-id]-review.md` (e.g., `STORY-001-player-movement-review.md`).
- This document must be stored in `.ai/reviews/[epic-name]/` (e.g., `.ai/reviews/EPIC-001-core-systems/`).
- The document should clearly list all identified issues and the proposed actionable items (new stories, tasks, etc.).

## Workflow Integration
- This task typically occurs after "Implementation" is complete for a story and before "Final Validation" or as a key part of it.
- The output of this review (especially new stories or required modifications) feeds back into the development cycle.
- Update the parent epic document in `.ai/epics/[epic-name].md` with the review status and link to the review document.

## Success Criteria
- The review is thorough and covers all aspects defined in the checklist.
- Findings are clearly documented and actionable.
- Both QA Specialist and Godot Architect agree on the assessment and recommendations.
- The review document provides a clear path forward for addressing any identified issues.
