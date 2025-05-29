# Code Review Document: [Story ID/Name]

**Story Reviewed**: [Link to Story File]
**Date of Review**: [Date]
**Reviewers**: QA Specialist (QA), Godot Architect (Mo)
**Implementation Commit/Branch**: [Link or ID]

## 1. Executive Summary
[Brief overview of the review findings and overall assessment. Highlight key strengths and critical concerns.]

## 2. Adherence to Story Requirements & Acceptance Criteria
- **Acceptance Criteria Checklist**:
  - [ ] AC1: "[Criterion Text]" - **Status**: [Met / Partially Met / Not Met] - **Comments**: [Detailed observations]
  - [ ] AC2: "[Criterion Text]" - **Status**: [Met / Partially Met / Not Met] - **Comments**: [Detailed observations]
  - ...
- **Overall Story Goal Fulfillment**: [Assess if the core intent of the story was achieved.]

## 3. Architectural Review (Godot Architect Focus)
- **Adherence to Approved Architecture**: [Findings, specific deviations, and impact.]
- **Godot Best Practices & Patterns**: [Compliance level, use of idiomatic Godot, any anti-patterns observed.]
- **Scene/Node Structure & Composition**: [Observations on efficiency, clarity, reusability.]
- **Signal Usage & Decoupling**: [Effectiveness of signal usage, parameter typing, clarity.]
- **Code Reusability & Modularity**: [Assessment of how well components are designed for reuse.]

## 4. Code Quality & Implementation Review (QA Specialist Focus)
- **GDScript Standards Compliance**: (Static Typing, Naming Conventions, `class_name` usage) - [Specific findings.]
- **Readability & Maintainability**: [Overall assessment, suggestions for improvement.]
- **Error Handling & Robustness**: [Effectiveness of error handling, coverage of edge cases.]
- **Performance Considerations**: [Observed or potential performance issues, suggestions for optimization.]
- **Testability & Unit Test Coverage**: [Ease of testing, quality/quantity of existing unit tests (GUT).]
- **Comments & Code Documentation**: [Quality, completeness, and accuracy of inline comments and docstrings.]

## 5. Issues Identified
*(Categorize by severity: Critical, Major, Minor, Suggestion)*

| ID    | Severity   | Description                                      | File(s) & Line(s)      | Suggested Action                                   | Assigned (Persona) | Status      |
|-------|------------|--------------------------------------------------|------------------------|----------------------------------------------------|--------------------|-------------|
| R-001 | Major      | Example: Untyped variable in core player logic.  | `player_controller.gd:42` | Refactor to include static type. Create new Story. | Dev                | Open        |
| R-002 | Minor      | Example: Typo in a comment.                      | `utility_functions.gd:10`| Fix typo directly.                                 | Dev                | Open        |
| R-003 | Suggestion | Example: Consider using a signal for X event.    | `hud_manager.gd:75`    | Discuss with Dev, potentially refactor.            | Dev                | Open        |
| ...   | ...        | ...                                              | ...                    | ...                                                | ...                | ...         |

## 6. Actionable Items & Recommendations

### New User Stories Proposed:
*(To address Critical/Major issues requiring significant work)*
- **[STORY-ID-NEW-XXX]**: [Title: e.g., "Refactor Player State Management for Type Safety"]
  - **Description**: [Brief description of the new story.]
  - **Rationale**: [Based on Issue ID(s) from section 5, e.g., "Addresses R-001 regarding untyped variables."].
  - **Estimated Complexity**: [Simple/Medium/Complex]
- ...

### Modifications to Existing Stories / Tasks for Current Story:
*(For Major/Minor issues that can be handled within current or slightly modified scope)*
- **Story [STORY-ID-CURRENT]**:
  - **Task**: [Describe modification or task, e.g., "Fix comment typo in `utility_functions.gd:10` (R-002)"].
  - **Rationale**: [Based on Issue ID(s)].
- ...

### General Feedback & Hints:
- [General observations, positive feedback, or broader suggestions for the development team or future work.]

## 7. Overall Assessment & Recommendation
- [ ] **Approved**: Implementation is of high quality. Any minor issues can be addressed directly by Dev without new stories.
- [ ] **Approved with Conditions**: Implementation is largely good, but specific Major issues (listed above, to be tracked as new stories/tasks) must be resolved before final validation.
- [ ] **Requires Major Rework**: Significant issues found. Implementation needs substantial revision. Key issues must be addressed, potentially requiring re-evaluation of the story/approach.

**Sign-off**:
- QA Specialist (QA):
- Godot Architect (Mo):
