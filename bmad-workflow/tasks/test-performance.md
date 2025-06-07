# Task: Test Performance

## Objective
To analyze the performance of a newly implemented or converted feature in Godot, ensuring it meets the project's performance targets for frame rate, memory usage, and CPU load.

## Prerequisites
- A feature that is functionally complete and ready for performance testing.
- A playable build of the Godot project.
- Defined performance targets for the project (e.g., target FPS, memory budget).

## Performance Testing Process

### 1. Establish a Baseline
- If possible, measure the performance of the original feature in WCS to establish a benchmark.
- Create a consistent and repeatable test scenario in Godot. This might involve a specific level, a specific number of objects on screen, or a specific sequence of actions.

### 2. Profile the Feature
- Use Godot's built-in profiler to measure key performance indicators:
    - **FPS (Frames Per Second)**: Is the frame rate stable and above the target?
    - **Memory Usage**: How much memory does the feature consume? Are there any memory leaks?
    - **CPU Time**: Which functions are taking the most CPU time?
    - **Draw Calls**: Are there an excessive number of draw calls?

### 3. Stress Testing
- Push the feature to its limits. What happens with a large number of objects? What happens during intense action?
- Identify the conditions under which performance begins to degrade.

### 4. Document Findings
- Create a performance report in `bmad-artifacts/reviews/[epic-name]/[story-id]-performance-report.md`.
- Include screenshots from the profiler, graphs of performance metrics, and a clear summary of the findings.
- Pinpoint specific functions or nodes that are causing performance issues.

### 5. Make Recommendations
- Based on the findings, provide clear recommendations for optimization.
- Suggest specific changes to the code or scene structure that could improve performance.
- If performance is acceptable, document this as well.

## Output Format
- A detailed performance report document.
- Potentially, new user stories or tasks in the backlog specifically for optimization work.

## Quality Checklist
- [ ] The test scenario was consistent and repeatable.
- [ ] Key metrics (FPS, memory, CPU) were measured and documented.
- [ ] The report clearly identifies any performance bottlenecks.
- [ ] Recommendations are specific and actionable.
- [ ] The feature's performance is explicitly compared against the project's targets.

## Workflow Integration
- **Input**: A functionally complete feature.
- **Output**: A performance report and optimization tasks.
- **Next Steps**: If performance is inadequate, optimization stories will be created and prioritized. If performance is acceptable, the feature moves closer to final approval.
- **Epic Update**: Update the parent epic and story with a summary of the performance test results.

## Notes for QA
- Objective data is key. Don't just say "it feels slow." Provide numbers, graphs, and profiler data to back up your assessment.
- Isolate the feature being tested as much as possible to ensure your measurements are accurate.
- A feature is not "done" until it is performant. Do not approve features that fail to meet performance targets.
