# Task: Define WCS Epic

## Objective
Define a high-level Epic `bmad-artifacts/docs/epic-structure-definition.md` for the WCS-Godot conversion project, outlining a significant body of work that delivers substantial value. Epics will serve as large user stories that can be broken down into smaller, manageable user stories for implementation.

## Prerequisites
- Approved Conversion PRD for the relevant WCS system(s) or overall project.
- Understanding of the overall conversion goals and strategic priorities.
- Input from WCS Analyst (Larry) regarding system complexity and scope.
- Input from Godot Architect (Mo) regarding high-level technical feasibility.

## Input Requirements
- **PRD Reference**: Link to the approved Product Requirements Document(s).
- **Strategic Goals**: Key objectives the epic aims to achieve.
- **Scope Idea**: Initial thoughts on the boundaries of the epic.
- **User/Stakeholder Needs**: High-level requirements or problems the epic addresses.

## Epic Definition Process

### 1. Epic Identification
- Review PRD and strategic goals to identify potential epics.
- Brainstorm with stakeholders (including user interaction) to list potential large features or areas of work.
- Group related requirements or features into logical epic candidates.

### 2. Scope Definition
- Clearly define the boundaries of the epic: what is included and what is not.
- Identify key functionalities and deliverables within the epic.
- Consult with WCS Analyst and Godot Architect for scope refinement based on technical insights.

### 3. Value Proposition
- Articulate the primary benefit and value the epic delivers to the project or end-users.
- Define how the epic contributes to the overall conversion success.

### 4. High-Level Requirements
- List the major requirements or user outcomes associated with the epic.
- These are not detailed user stories yet but provide a summary of what needs to be achieved.

### 5. Dependencies and Risks
- Identify any major dependencies on other epics, systems, or external factors.
- Outline potential high-level risks associated with the epic.

### 6. Naming and Identification
- Assign a clear, concise, and descriptive name to the epic.
- Assign a unique identifier (e.g., EPIC-001).

## Output Format

Create an epic definition document in `bmad-artifacts/epics/` using the `wcs-epic-template.md` from `bmad-workflow/templates/wcs-epic-template.md`. The filename should be, for example, `bmad-artifacts/epics/EPIC-001-player-ship-core-system-conversion.md`.

The template includes sections for:
```markdown
# Epic: [EPIC-ID]: [Epic Name]

## 1. Description
[Brief overview of the epic, its purpose, and the problem it solves or value it delivers.]

## 2. Strategic Alignment
[How this epic aligns with the overall WCS-Godot conversion goals and PRD.]

## 3. Scope
### In Scope:
- [List of major features/functionalities included]
### Out of Scope:
- [List of related features/functionalities explicitly excluded]

## 4. Value Proposition
[Primary benefits and value delivered by completing this epic.]

## 5. High-Level Requirements / User Outcomes
- [Outcome 1]
- [Outcome 2]
- [...]

## 6. Key Stakeholders
- [List of stakeholders interested in this epic]

## 7. Dependencies
- [Other epics, systems, or prerequisites]

## 8. Potential Risks
- [High-level risks identified]

## 9. Acceptance Criteria (High-Level)
[Broad conditions that will indicate the epic's objectives have been met. These are not story-level ACs.]
- [Criterion 1]
- [Criterion 2]

## 10. Estimated Size/Complexity (Optional)
[T-shirt size (S, M, L, XL) or rough estimate if useful at this stage.]
```

## Quality Checklist
- [ ] Epic has a clear, descriptive name and unique ID.
- [ ] Scope is well-defined (inclusions and exclusions).
- [ ] Value proposition is clearly articulated.
- [ ] High-level requirements are captured.
- [ ] Major dependencies and risks are identified.
- [ ] Epic is aligned with the PRD and strategic goals.
- [ ] Stakeholders have been consulted/informed.
- [ ] Epic is large enough to be significant but not too large to be unmanageable.
- [ ] **Quality Check**: The defined Epic passes the criteria in `bmad-workflow/checklists/epic-quality-checklist.md`.

## Workflow Integration
- **Input**: Approved PRD, strategic goals, user feedback.
- **Template**: `bmad-workflow/templates/wcs-epic-template.md`
- **Checklist**: `bmad-workflow/checklists/epic-quality-checklist.md`
- **Process**: Defined by Conversion Manager (Curly), with input from WCS Analyst (Larry) and Godot Architect (Mo), and interaction with the user.
- **Output**: Defined epic document stored in `bmad-artifacts/epics/[epic-name].md`.
- **Next Steps**: Defined epics are prioritized and then handed over to Story Manager (SallySM) for breakdown into user stories.
- **Interaction**: Requires interaction with the user to confirm and prioritize the list of epics.

## Success Criteria
- Epic definition provides a clear, high-level understanding of a significant piece of work.
- Enables effective prioritization and planning.
- Serves as a stable container for a set of related user stories.
- Facilitates communication with stakeholders about major deliverables.

## Notes for Curly (Conversion Manager)
- Focus on defining epics that deliver tangible value and align with strategic priorities.
- Collaborate with Larry and Mo to ensure epics are technically grounded.
- Engage with the user/stakeholders to validate and prioritize epics.
- Keep epics at a high level; avoid getting into detailed story-level requirements.
- Ensure a manageable number of active epics at any given time (ideally one, as per BMAD rules for "in progress").
