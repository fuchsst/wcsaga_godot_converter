# Task: Create Godot Scene Structure

## Objective
To translate an approved Godot architecture design into a concrete set of scenes, nodes, and script attachments within the Godot project. This task involves creating the foundational `.tscn` files and basic script files as defined in the architecture.

## Prerequisites
- An approved Godot architecture document (`architecture.md`) for the system.
- The supplementary `godot-files.md` and `godot-dependencies.md` documents must be complete and approved.
- Access to the `target/` Godot project.

## Input Requirements
- **Epic Name**: The epic this work belongs to.
- **Architecture Documents**: The full set of approved architecture documents (`architecture.md`, `godot-files.md`, `godot-dependencies.md`).

## Process

### 1. Review Architecture
- Thoroughly review the `architecture.md` to understand the design rationale.
- Use `godot-files.md` as a checklist for all scenes and scripts that need to be created.
- Use `godot-dependencies.md` as a guide for how scenes should be instanced and how scripts should be connected.

### 2. Create Folder Structure
- If not already present, create the necessary subdirectories within `target/scenes/` and `target/scripts/` for the system being implemented.

### 3. Create Scenes (.tscn)
- For each scene defined in `godot-files.md`, create a new `.tscn` file in the appropriate location.
- Build the node hierarchy within each scene exactly as specified in the architecture document.
- Instance child scenes as required by the design.

### 4. Create and Attach Scripts (.gd)
- For each script defined in `godot-files.md`, create a new, empty `.gd` file in the appropriate location.
- Attach these scripts to the corresponding nodes in the scenes you created, as specified in the architecture.
- Add basic boilerplate to each script, such as `class_name` if required, and a brief comment describing its purpose.

### 5. Connect Signals
- Based on the `godot-dependencies.md` document, connect signals between nodes within scenes via the Godot editor's UI where possible.
- For more complex or cross-scene connections, add placeholder comments in the relevant scripts indicating where dynamic signal connections will need to be made in code.

## Output Format
- A set of new or modified `.tscn` and `.gd` files within the `target/` project directory.
- The created files should directly correspond to the blueprints laid out in the architecture documents.

## Quality Checklist
- [ ] All scenes specified in `godot-files.md` have been created.
- [ ] All scripts specified in `godot-files.md` have been created and attached to the correct nodes.
- [ ] Node hierarchies in the `.tscn` files match the architecture document.
- [ ] Folder structure is clean and follows project conventions.
- [ ] Basic signal connections defined in the architecture are implemented.

## Workflow Integration
- **Input**: Approved architecture documents from the `Design Godot Architecture` task.
- **Output**: A foundational structure of scenes and scripts in the Godot project.
- **Next Steps**: This structure serves as the starting point for the `Implement Godot Feature` or `Convert C++ to GDScript` tasks performed by the GDScript Developer (Dev).
- **Epic Update**: Update the parent epic in `bmad-artifacts/epics/[epic-name].md` to reflect that the initial scene structure has been scaffolded.

## Notes for Mo (Godot Architect)
- Your focus here is on precision and fidelity to your own architectural plan.
- This is not about writing the logic, but about creating the skeleton. The structure must be perfect.
- Ensure every node is named correctly and every script is attached properly.
- A clean and accurate scene structure is critical for Dev to be able to work efficiently.
