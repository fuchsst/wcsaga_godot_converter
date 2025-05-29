# Command: Review Code Implementation

## Objective
Guide the QA Specialist (QA), in collaboration with the Godot Architect (Mo), to perform a comprehensive review of an implemented user story. This review ensures adherence to quality standards, architectural guidelines, and story requirements for the WCS-Godot conversion project.

You are initiating a code review for the story: $ARGUMENTS (e.g., "STORY-001-player-movement" or path to story file)

## Review Process

### 1. Load BMAD Framework & Personas
- Activate the **QA Specialist (QA)** persona as defined in `.bmad/personas/qa-specialist.md`.
- Note that QA will collaborate closely with the **Godot Architect (Mo)**, as per their persona definition in `.bmad/personas/godot-architect.md`.
- The primary task to be executed is "Review Code Implementation" detailed in `.bmad/tasks/review_code_implementation.md`.

### 2. Gather Necessary Materials
Before commencing, ensure the following are readily available:
- The **User Story** file (identified by $ARGUMENTS).
- The **Implemented Code** (specific commit or branch in the `target/` submodule).
- The **Approved Architecture Document** for the relevant system/epic.
- The **Code Review Checklist**: `.bmad/checklists/code-review-checklist.md`.
- The **Code Review Document Template**: `.bmad/templates/code-review-document-template.md`.

### 3. Prerequisites Check (QA & Mo to verify)
- [ ] The user story (from $ARGUMENTS) is marked as "Implementation Complete" or "Ready for Review".
- [ ] The specific code version (commit/branch) for review is clearly identified.
- [ ] The story's parent Epic and associated Architecture document are accessible for context.

### 4. Execution Steps (as per `.bmad/tasks/review_code_implementation.md`)
The QA Specialist and Godot Architect will collaboratively:
1.  **Understand Context**: Deeply review the user story, its acceptance criteria, and the relevant sections of the architecture document.
2.  **Systematic Code Examination**:
    *   QA Specialist focuses on: Fulfillment of story ACs, GDScript standards, testability, error handling, code comments, overall code quality, and gameplay feel (if applicable).
    *   Godot Architect focuses on: Adherence to architectural design, Godot best practices, design patterns, scene/node structure, signal usage, and performance implications from a design perspective.
3.  **Utilize Checklist**: Methodically complete the `.bmad/checklists/code-review-checklist.md` for the reviewed code.
4.  **Document Findings**: Record all observations, issues (categorized by severity), and suggestions using the `.bmad/templates/code-review-document-template.md`.
5.  **Define Actionable Items**: Propose new user stories for significant issues or necessary refactoring. Suggest modifications or specific tasks for existing stories if issues are smaller.
6.  **Provide Overall Assessment**: Conclude with a clear recommendation (e.g., Approved, Approved with Conditions, Requires Major Rework).

### 5. Output Requirements
The primary output is a completed code review document:
- **Filename**: `[story-id]-review.md` (e.g., `STORY-001-player-movement-review.md`).
- **Location**: `.ai/reviews/[epic-name]/` (e.g., `.ai/reviews/EPIC-001-core-systems/`).
- **Content**: Must follow the structure of `.bmad/templates/code-review-document-template.md` and include all findings and actionable items.

## Critical Reminders for QA Specialist & Godot Architect
- **Collaboration is Essential**: This is a joint review. Leverage each other's expertise.
- **Constructive Feedback**: Frame feedback to be actionable, specific, and helpful for the developer.
- **Reference Standards**: Consistently refer to the project's checklists, architecture documents, and persona guidelines.
- **Uphold Quality**: Ensure the implementation meets the high-quality standards expected for the WCS-Godot conversion.
- **BMAD Workflow Adherence**: This review is a critical quality gate in the BMAD process.

Begin code review for story: $ARGUMENTS
