# Task: Plan Conversion Milestone

## Objective
To define a clear and achievable conversion milestone by grouping a set of prioritized features and epics into a logical package of work with a defined goal and timeline.

## Prerequisites
- A prioritized feature and epic backlog, as produced by the `Prioritize WCS Features` task.
- A high-level understanding of the effort and dependencies involved for the features being considered.

## Input Requirements
- **Prioritized Backlog**: The list of features and epics to be planned.
- **Milestone Goal**: A clear objective for what the milestone should achieve (e.g., "Implement core player ship mechanics," "First playable combat loop").
- **Resource Constraints**: Awareness of team capacity and any time constraints.

## Planning Process

### 1. Select Features for Milestone
- From the prioritized backlog, select a coherent set of features and epics that align with the milestone goal.
- Ensure that all technical dependencies for the selected features are either already met or are included within the milestone.

### 2. Define Milestone Scope
- Clearly document which epics and features are included in the milestone.
- Explicitly state what is considered "out of scope" for this milestone to manage expectations.

### 3. High-Level Estimation
- Consult with the technical personas (Larry, Mo, Dev) to get high-level effort estimates for the included work.
- Use these estimates to create a realistic timeline for the milestone.

### 4. Define Milestone Deliverables
- List the concrete outcomes of the milestone. This should include:
    - Implemented features.
    - Completed epics.
    - A playable build or demo, if applicable.
    - Completed documentation (PRDs, Architecture, Reviews).

### 5. Document the Plan
- Create a milestone plan document in `bmad-artifacts/docs/project-overview/milestone-[milestone-name].md`.
- The document should include the goal, scope, timeline, feature list, and deliverables.

## Output Format
- A milestone planning document (e.g., `milestone-1-core-gameplay.md`) in `bmad-artifacts/docs/project-overview/`.
- An updated conversion roadmap reflecting the new milestone.

## Quality Checklist
- [ ] The milestone has a clear and singular goal.
- [ ] The scope is well-defined, with clear inclusions and exclusions.
- [ ] The plan is realistic, considering dependencies and estimated effort.
- [ ] The deliverables are concrete and measurable.
- [ ] The milestone represents a tangible step forward for the project.

## Workflow Integration
- **Input**: A prioritized backlog of features and epics.
- **Output**: A detailed plan for a specific conversion milestone.
- **Next Steps**: The milestone plan guides the team's focus for a specific period. Work on the epics and stories within the milestone begins.
- **Epic Update**: The relevant epic documents should be updated to reflect their inclusion in the milestone.

## Notes for Curly (Conversion Manager)
- A good milestone has a theme or a clear goal. Avoid just grabbing a random collection of features.
- Be realistic. It's better to deliver a smaller, successful milestone than to fail at an overly ambitious one.
- Communication is key. Ensure the whole team understands and agrees with the milestone plan.
- This plan provides focus. Once the milestone is set, the team should primarily work on tasks within that milestone.
