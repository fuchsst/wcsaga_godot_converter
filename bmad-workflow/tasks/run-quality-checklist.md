# Task: Run Quality Checklist

## Objective
To formally run one of the project's predefined quality checklists against a specific artifact (e.g., a PRD, an architecture document, a user story) to ensure it meets the required quality standards before proceeding to the next stage of the workflow.

## Prerequisites
- An artifact (document, story, etc.) that is ready for a quality gate review.
- The relevant checklist exists in `bmad-workflow/checklists/`.

## Input Requirements
- **Checklist Name**: The filename of the checklist to be used (e.g., `conversion-prd-quality-checklist.md`).
- **Artifact Path**: The path to the document or artifact being reviewed.
- **Epic Name**: The epic associated with the artifact.

## Process

### 1. Select the Correct Checklist
- Identify the appropriate checklist from the `bmad-workflow/checklists/` directory based on the artifact being reviewed.

### 2. Systematically Review the Artifact
- Go through the checklist item by item.
- For each item, carefully examine the artifact to determine if it meets the criterion.
- Mark each item as passed or failed.

### 3. Document the Results
- Create a new review document in `bmad-artifacts/reviews/[epic-name]/` named `[artifact-name]-[checklist-name]-review.md`.
- In this document, embed the checklist and its results.
- For any failed items, provide a clear explanation of why it failed and what needs to be done to address the issue.

### 4. Determine the Outcome
- Based on the checklist results, determine if the artifact passes the quality gate.
- The artifact is only considered "approved" if all checklist items are passed.

## Output Format
- A review document in `bmad-artifacts/reviews/[epic-name]/` that contains the completed checklist and any notes.
- A clear pass/fail status for the artifact.

## Quality Checklist
- [ ] The correct checklist was used for the artifact.
- [ ] Every item on the checklist was evaluated.
- [ ] All failures are clearly documented with actionable feedback.
- [ ] The final pass/fail decision is unambiguous.

## Workflow Integration
- **Input**: An artifact requiring a quality check.
- **Output**: A formal quality review document and an approval status.
- **Next Steps**: A "pass" status unblocks the next stage of the BMAD workflow. A "fail" status sends the artifact back to its creator for revision.
- **Epic Update**: Update the parent epic to reflect the outcome of the quality check.

## Notes for SallySM (Story Manager)
- Your role here is to be the guardian of the process.
- Be meticulous. A missed item on a checklist can lead to problems later.
- The goal is not to be a blocker, but to ensure quality is maintained at every step.
- Ensure the feedback for failed items is constructive and helps the owner of the artifact to improve it.
