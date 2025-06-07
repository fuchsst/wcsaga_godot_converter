# Command: Create WCS Epic

## Objective
Guide the creation of a high-level Epic for the WCS-Godot conversion project, following the BMAD methodology.

You are initiating the Epic creation process for: $ARGUMENTS (e.g., "Player Ship Core Systems")

## Epic Creation Process

### 1. Load BMAD Framework
- Load the Conversion Manager persona (Curly) from `bmad-workflow/personas/conversion-manager.md`.
- Reference the epic definition task from `bmad-workflow/tasks/define-wcs-epic.md`.
- Note the epic output structure and location as defined in the task (`bmad-artifacts/epics/[epic-name].md`, e.g., `bmad-artifacts/epics/EPIC-001-player-ship-core-system-conversion`).

### 2. Prerequisites Check (CRITICAL)
Before starting Epic creation, Curly must verify:
- [ ] An approved Conversion PRD exists for the relevant WCS system(s) or the overall project. (e.g., in `bmad-artifacts/docs/`)
- [ ] Overall conversion goals and strategic priorities are understood.
- [ ] Input from WCS Analyst (Larry) regarding system complexity and scope is available or can be obtained.
- [ ] Input from Godot Architect (Mo) regarding high-level technical feasibility is available or can be obtained.

**VIOLATION CHECK**: If any prerequisite is missing, Curly must ensure these are addressed before proceeding.

### 3. Epic Development Steps (as per `bmad-workflow/tasks/define-wcs-epic.md`)
Curly will lead the following process, interacting with the user and other personas as needed:

1.  **Epic Identification**:
    *   Review PRD and strategic goals.
    *   Brainstorm with the user/stakeholders for potential epics.
    *   Group related requirements into epic candidates.
2.  **Scope Definition**:
    *   Clearly define "in scope" and "out of scope" items.
    *   Consult Larry (WCS Analyst) and Mo (Godot Architect) for technical refinement.
3.  **Value Proposition**:
    *   Articulate the primary benefit and value.
4.  **High-Level Requirements**:
    *   List major user outcomes.
5.  **Dependencies and Risks**:
    *   Identify major dependencies and high-level risks.
6.  **Naming and Identification**:
    *   Assign a clear name (e.g., "Player Ship Core Systems Conversion").
    *   Assign a unique ID (e.g., "EPIC-001"). The filename should reflect this (e.g., `EPIC-001-player-ship-core-systems-conversion.md`).

### 4. User Interaction
- Curly must interact with the user to:
    - Confirm the list of potential epics.
    - Prioritize the epics.
    - Finalize the details of the current epic being defined.

### 5. Quality Validation (as per Quality Checklist in task)
Curly ensures the defined epic meets criteria such as:
- [ ] Clear name and unique ID.
- [ ] Well-defined scope.
- [ ] Clear value proposition.
- [ ] Alignment with PRD and strategic goals.
- [ ] Stakeholder consultation.

### 6. Output Requirements
Create the epic definition document:
- **Location**: `bmad-artifacts/epics/`
- **Filename**: `[EpicID]-[epic-name-slugified].md` (e.g., `EPIC-001-player-ship-core-systems-conversion.md`)
- **Structure**: Follow the template provided in `bmad-workflow/tasks/define-wcs-epic.md`.
- **Approval**: The epic should be considered for approval by relevant stakeholders.

## Critical Reminders for Curly (Conversion Manager)
- Focus on epics that deliver tangible value and align with strategic priorities.
- Collaborate with Larry and Mo for technical grounding.
- Engage actively with the user/stakeholders for validation and prioritization.
- Keep epics at a high level; avoid story-level details.
- Adhere to the BMAD rule of (ideally) one "in-progress" epic at a time.

## BMAD Workflow Compliance
- **Input**: Approved PRD, strategic goals, user feedback.
- **Process**: Led by Conversion Manager (Curly), with input from WCS Analyst (Larry) & Godot Architect (Mo).
- **Output**: Defined epic document in `bmad-artifacts/epics/`.
- **Next Steps**: Prioritized epics are handed to Story Manager (SallySM) for breakdown.
- **Rule**: Epic definition occurs after PRD definition.

Begin Epic creation for: $ARGUMENTS
