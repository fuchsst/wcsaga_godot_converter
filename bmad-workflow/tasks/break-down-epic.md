# Task: Break Down Epic

## Objective
To break down a large, approved epic into a backlog of small, well-defined, and implementable user stories. This process ensures that a large body of work is decomposed into manageable chunks for the development team.

## Prerequisites
- An approved epic document in `bmad-artifacts/epics/`.
- Approved PRD and Architecture documents relevant to the epic.

## Input Requirements
- **Epic ID**: The identifier of the epic to be broken down.
- **Epic Document**: The full epic document.
- **Supporting Documents**: The PRD and Architecture documents that provide the necessary detail.

## Decomposition Process

### 1. Understand the Epic
- Thoroughly review the epic document, its scope, high-level requirements, and value proposition.
- Review the associated PRD and architecture documents to understand the detailed functional and technical requirements.

### 2. Identify Story Candidates
- Brainstorm a list of all the individual pieces of functionality required to fulfill the epic.
- Group related functionalities into potential user stories.
- Think vertically: each story should ideally represent a thin slice of end-to-end functionality, even if it's very small.

### 3. Draft User Stories
- For each identified story candidate, create a draft user story.
- Use the `Create WCS User Story` task as a guide for the structure and level of detail required for each story.
- Focus on defining the "what" and "why," with clear acceptance criteria.

### 4. Refine and Size Stories
- Review the drafted stories to ensure they are well-defined and appropriately sized (1-3 days of work).
- If a story is too large, break it down further.
- If a story is too small, consider merging it with another closely related story.
- Add high-level estimates (e.g., complexity points) to each story.

### 5. Map Dependencies
- For the newly created stories, identify and document the dependencies between them.
- This will create a logical sequence for implementation.

## Output Format
- A backlog of new user story files (`[STORY-ID]-[story-name].md`) located in `bmad-artifacts/stories/[epic-name]/`.
- An updated epic document in `bmad-artifacts/epics/[epic-name].md` with links to the newly created stories and a status update.

## Quality Checklist
- [ ] The entire scope of the epic is covered by the created user stories.
- [ ] All created stories are small, independent, and testable.
- [ ] Each story has clear acceptance criteria.
- [ ] Dependencies between stories are clearly mapped out.
- [ ] The resulting story backlog represents a clear and actionable plan for implementing the epic.

## Workflow Integration
- **Input**: An approved epic.
- **Output**: A backlog of user stories for that epic.
- **Next Steps**: The created stories can be prioritized and assigned for implementation.
- **Epic Update**: The epic document is updated to become a central hub for tracking the progress of its stories.

## Notes for SallySM (Story Manager)
- Your technical expertise is crucial here. You need to understand the architecture to break it down logically.
- Collaborate with Mo (Godot Architect) and Dev (GDScript Developer) if you are unsure about the technical details or effort required.
- The goal is to create a "ready" backlog that the development team can start working on without significant further clarification.
- A well-decomposed epic is the key to a smooth and predictable development flow.
