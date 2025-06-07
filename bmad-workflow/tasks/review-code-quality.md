# Task: Review Code Quality

## Objective
To perform a detailed review of implemented GDScript code, focusing specifically on its quality, clarity, maintainability, and adherence to project-wide coding standards.

## Prerequisites
- Implemented code for a user story is available for review.
- The code has already passed initial functional tests.

## Input Requirements
- **Story ID**: The user story associated with the code.
- **Code Location**: A reference to the specific commit or branch containing the code to be reviewed.

## Code Quality Review Process

### 1. Review Against Coding Standards
- Systematically check the code against the GDScript Coding Standards defined in the main `CLAUDE.md`.
- **Static Typing**: Is every variable, parameter, and return type explicitly typed?
- **Naming Conventions**: Does the code use snake_case for variables/functions and PascalCase for classes? Are constants in UPPER_CASE?
- **Class Naming**: Are `class_name` declarations used appropriately for reusable classes?

### 2. Assess Readability and Maintainability
- **Clarity**: Is the code easy to understand? Is the logic straightforward or overly complex?
- **Comments**: Are there comments where necessary to explain complex or non-obvious logic?
- **Docstrings**: Does every public function have a clear docstring explaining its purpose, parameters, and return value?
- **Function Length**: Are functions reasonably short and focused on a single responsibility?

### 3. Verify Error Handling
- Does the code handle potential errors gracefully?
- Are there checks for null or invalid values where appropriate?
- Does the code fail safely without causing crashes?

### 4. Document Findings
- Create a code quality report in `bmad-artifacts/reviews/[epic-name]/[story-id]-code-quality-report.md`.
- Document all identified issues, providing specific examples from the code.
- Categorize issues (e.g., "Style Nitpick," "Maintainability Concern," "Critical Standards Violation").
- Provide concrete suggestions for how to improve the code.

## Output Format
- A code quality report document.
- A list of recommended changes or refactoring tasks for the developer.

## Quality Checklist
- [ ] The code is 100% statically typed.
- [ ] All project naming conventions are followed.
- [ ] Public functions are fully documented with docstrings.
- [ ] The code is clear, readable, and not overly complex.
- [ ] Error handling is present and robust.

## Workflow Integration
- **Input**: Implemented code for a user story.
- **Output**: A code quality report with actionable feedback.
- **Next Steps**: The developer will address the feedback. This review can happen in parallel with other validation tasks.
- **Epic Update**: Update the story to note that a code quality review has been completed and link to the report.

## Notes for QA
- You are the guardian of the project's long-term health. Clean, maintainable code is essential.
- Be consistent in your application of the coding standards.
- The goal is to help the developer improve the code, so ensure your feedback is constructive.
- Don't just point out problems; suggest better alternatives where possible.
