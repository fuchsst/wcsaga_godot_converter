# Task: Review Godot Architecture

## Objective
To conduct a formal review of a proposed Godot architecture, ensuring it is robust, scalable, maintainable, and aligns with Godot best practices before it is approved for implementation.

## Prerequisites
- A complete set of architecture documents (`architecture.md`, `godot-files.md`, `godot-dependencies.md`) has been created.
- The architecture is ready for formal review.

## Input Requirements
- **Epic Name**: The epic to which the architecture belongs.
- **Architecture Documents**: The full set of documents to be reviewed.

## Review Process

### 1. Comprehensive Checklist Review
- Systematically go through the `bmad-workflow/checklists/godot-architecture-checklist.md`.
- If the system involves significant UI components, also use the `bmad-workflow/checklists/godot-ui-architecture-checklist.md`.
- Verify that every item on the checklist is met by the proposed architecture.

### 2. Critical Analysis
- **Scalability**: Assess whether the architecture can accommodate future features and complexity.
- **Performance**: Scrutinize the design for potential performance bottlenecks.
- **Maintainability**: Evaluate how easy the system will be to understand, modify, and debug.
- **Godot-Native Principles**: Challenge any design choice that doesn't feel "Godot-native." Is it using signals effectively? Is the node composition logical?

### 3. Document Findings
- Create a review document in `bmad-artifacts/reviews/[epic-name]/` named `architecture-review.md`.
- Clearly articulate any identified issues, concerns, or required changes.
- For each issue, provide a clear rationale and a suggested alternative or improvement.
- Also, document what is good about the architecture and why.

### 4. Approve or Request Revisions
- Based on the review, make a clear decision:
    - **Approved**: The architecture is sound and can proceed to story creation.
    - **Approved with Conditions**: Minor revisions are required but do not need a full re-review.
    - **Requires Major Rework**: The architecture has significant flaws and must be revised and re-reviewed.

## Output Format
- A formal review document: `bmad-artifacts/reviews/[epic-name]/architecture-review.md`.
- A clear status update on the architecture (Approved, Needs Rework, etc.).

## Quality Checklist
- [ ] The review was thorough and referenced the official checklists.
- [ ] All identified issues are documented with clear, actionable feedback.
- [ ] The final decision is unambiguous.
- [ ] The review provides constructive feedback to improve the architecture.

## Workflow Integration
- **Input**: A set of proposed architecture documents.
- **Output**: A formal review document and an approval status.
- **Next Steps**: An approved architecture is the prerequisite for the `Create WCS User Story` task. If the architecture requires rework, it goes back to the `Design Godot Architecture` task.
- **Epic Update**: Update the parent epic in `bmad-artifacts/epics/[epic-name].md` with the outcome of the architecture review and a link to the review document.

## Notes for Mo (Godot Architect)
- This is your quality gate. Be ruthless. Do not let a suboptimal architecture pass.
- Your standards define the quality of the entire project. Uphold them.
- Justify your decisions with principles from Godot's official documentation and established best practices.
- The goal is not just to find flaws, but to ensure the final architecture is as strong as possible.
