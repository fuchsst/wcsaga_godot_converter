# Command: Define Epics List

## Objective
Guide the Conversion Manager (Curly) to collaboratively define an initial list of high-level Epics for the WCS-Godot conversion project. This involves identifying major building blocks of the WCS system and creating placeholder files for these epics.

You are initiating the process to define the list of Epics for: $ARGUMENTS (e.g., "Overall WCS Conversion" or a specific major system like "Flight Model and Physics")

## Epic List Definition Process

### 1. Load BMAD Framework
- Load the Conversion Manager persona (Curly) from `.bmad/personas/conversion-manager.md`.
- Curly will also need to interact with:
    - WCS Analyst (Larry) from `.bmad/personas/wcs-analyst.md`
    - Godot Architect (Mo) from `.bmad/personas/godot-architect.md`
- Reference the epic definition task from `.bmad/tasks/define-wcs-epic.md` for understanding what an epic entails.

### 2. Prerequisites Check (CRITICAL)
Before starting, Curly must verify:
- [ ] An approved Conversion PRD exists for the relevant WCS system(s) or the overall project. This PRD provides the strategic context.
- [ ] Access to WCS system analysis (from Larry) is available to understand the system's components.
- [ ] High-level conversion goals and strategic priorities are understood.

**VIOLATION CHECK**: If prerequisites are missing, Curly must ensure these are addressed. This process typically follows PRD definition.

### 3. Collaborative Epic Identification
Curly will lead the following collaborative process:

1.  **Initial Brainstorming with Technical Leads**:
    *   Curly facilitates a discussion with Larry (WCS Analyst) and Mo (Godot Architect).
    *   **Larry's Input**: Identifies major functional areas, modules, and interdependencies from the WCS C++ source.
    *   **Mo's Input**: Provides insights on how these WCS areas might map to logical, large-scale Godot systems or features.
    *   The goal is to break down the overall conversion (or a major system specified in $ARGUMENTS) into significant, high-level "building blocks" or "chunks of value." These are potential epic candidates.

2.  **User Interaction and Refinement (Iterative)**:
    *   Curly presents the initial list of potential epic building blocks to the **user**.
    *   **Crucial Step**: Curly must actively solicit user feedback on this list:
        *   "Does this list of major areas make sense for the conversion?"
        *   "Are there any major components missing?"
        *   "Are any of these too granular or too broad?"
        *   "What are the user's priorities among these areas?"
    *   This interaction should be iterative. Curly refines the list based on user feedback, possibly involving Larry and Mo for further technical clarification if needed.
    *   Curly should **frequently ask the user to help refine the list** until a consensus is reached on the set of epics to define.

3.  **Finalizing the Epic List and Naming**:
    *   Once the user and the team agree on the set of epics, Curly assigns:
        *   A clear, descriptive name for each epic (e.g., "Player Ship Core Systems Conversion," "Main Menu UI Overhaul").
        *   A unique ID for each epic (e.g., "EPIC-001", "EPIC-002").

### 4. Output Requirements

1.  **Formatted List of Identified Epics**:
    *   Curly will present a final, numbered list of the agreed-upon epics with their IDs and names to the user for confirmation.
    Example:
    ```
    Okay, based on our discussions with Larry, Mo, and your valuable input, here is the proposed list of epics:
    1. EPIC-001: Player Ship Core Systems Conversion
    2. EPIC-002: Primary Weapon Systems
    3. EPIC-003: Secondary Weapon Systems
    4. EPIC-004: HUD and Targeting UI
    ...
    ```

2.  **Creation of Placeholder Epic Files**:
    *   For each identified epic in the final list, Curly will instruct the system to create a placeholder markdown file in the `.ai/epics/` directory.
    *   **Filename**: `[EpicID]-[epic-name-slugified].md` (e.g., `EPIC-001-player-ship-core-systems-conversion.md`).
    *   **Content of Placeholder File**: Minimal content, just enough to establish the epic.
        ```markdown
        # Epic: [EpicID]: [Epic Name]

        ## 1. Description
        [Placeholder for detailed description - to be filled out using the 'create-epic' command.]

        ## Status
        To Do
        ```
    *   Curly will confirm with the user once these placeholder files have been (notionally) created.

### 5. Next Steps
- After this command, individual epics from the list can be fully defined using the `create-epic` command (which uses `.bmad/tasks/define-wcs-epic.md`).
- The user can then prioritize which epic to detail first.

## Critical Reminders for Curly (Conversion Manager)
- This is a high-level planning activity. Avoid diving into story-level details for the epics at this stage.
- The collaboration with Larry, Mo, and especially the **user** is key to defining a relevant and agreed-upon set of epics.
- Ensure the identified epics represent significant, valuable chunks of work.

## BMAD Workflow Compliance
- This command facilitates the "Epic Definition" phase, which typically follows "PRD Definition."
- The output (list of epics and placeholder files) sets the stage for detailed definition of each epic.

Begin defining the list of Epics for: $ARGUMENTS, ensuring collaboration with Larry, Mo, and frequent refinement with the user.
