# Task: Convert C++ to GDScript

## Objective
To translate the logic from a specific WCS C++ file or system into a clean, efficient, and statically-typed GDScript implementation, following an approved user story and architectural guidelines.

## Prerequisites
- An approved user story with clear acceptance criteria.
- An approved architecture document for the system.
- The foundational scene and script files have been created in the `target/` project.
- Access to the original WCS C++ source code in `source/`.

## Input Requirements
- **Story ID**: The user story to be implemented.
- **Architecture Documents**: The relevant architecture specifications.
- **WCS Source Files**: The original C++ files to be converted.
- **Target Godot Files**: The `.gd` and `.tscn` files to be implemented.

## Conversion Process

### 1. Understand the Task
- Thoroughly read the user story, focusing on the acceptance criteria.
- Review the architecture document to understand the intended design, node structure, and signal flow.
- Examine the original WCS C++ code to fully grasp the logic that needs to be converted.

### 2. Implement in GDScript
- Write the GDScript code in the target files.
- **ALWAYS use static typing** for all variables, function parameters, and return types.
- Translate the C++ logic into equivalent GDScript, but do not simply do a line-by-line port. Adapt the logic to be "Godot-native."
- Use signals for communication between nodes as defined in the architecture.
- Adhere strictly to the project's GDScript coding standards (naming conventions, documentation, etc.).

### 3. Document the Code
- Write clear docstrings for all public functions, explaining their purpose, parameters, and return values.
- Add comments to explain complex or non-obvious sections of code.
- If you create a significant new class, ensure it has a `class_name` declaration.

### 4. Preliminary Testing
- As you code, perform basic tests to ensure the logic is working as expected.
- Run the relevant scene(s) to check for any immediate errors.

## Output Format
- Modified `.gd` script files in the `target/` project, containing the implemented logic.
- Potentially minor adjustments to `.tscn` files if needed (e.g., assigning a resource).

## Quality Checklist
- [ ] All code is statically typed. No exceptions.
- [ ] The implementation fulfills all acceptance criteria in the user story.
- [ ] The code adheres to the approved architecture.
- [ ] GDScript best practices and project coding standards have been followed.
- [ ] All public functions are documented with docstrings.
- [ ] The code is clean, readable, and maintainable.

## Workflow Integration
- **Input**: An approved user story and architecture.
- **Output**: Implemented GDScript code ready for review and testing.
- **Next Steps**: The implemented story will be reviewed by QA and the Godot Architect. It will also undergo validation and testing.
- **Epic Update**: Update the parent epic in `bmad-artifacts/epics/[epic-name].md` and the story file itself to reflect the implementation status.

## Notes for Dev (GDScript Developer)
- Your primary directive is clean, statically-typed code.
- Do not port C++ architecture. Implement the *Godot* architecture designed by Mo.
- Think about performance. Use Godot's built-in functions and nodes where possible.
- If you encounter an issue where the architecture seems flawed or incomplete, raise the issue immediately. Do not implement a workaround without consultation.
- Your implementation must be testable. Keep functions small and focused.
