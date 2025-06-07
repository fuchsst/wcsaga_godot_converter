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

Create an epic definition document in `bmad-artifacts/epics/` using the `bmad-workflow/templates/wcs-epic-template.md`. The filename should follow the convention `EPIC-XXX-epic-name.md`.

## Quality Checklist
- [ ] The epic must pass all criteria in the `bmad-workflow/checklists/epic-quality-checklist.md`.
- [ ] The epic has a clear, descriptive name and unique ID.
- [ ] The scope is well-defined with clear inclusions and exclusions.
- [ ] The value proposition is clearly articulated.
- [ ] The epic is aligned with the project's strategic goals and PRDs.

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
