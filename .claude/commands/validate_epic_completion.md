Guide the quality assurance validation of a completed WCS-Godot conversion Epic.

You are initiating QA validation for the Epic: $ARGUMENTS

## Validation Process

### 1. Load BMAD Framework
- Load the QA Specialist persona (QA) from `.bmad/personas/qa-specialist.md`.
- Reference the completed Epic definition (`.ai/epics/[epic-name].md`).
- Review all constituent story files and their `[story-id]-review.md` documents.
- Review the original WCS system analysis and architecture documents relevant to the Epic.

### 2. Prerequisites Check (CRITICAL - MUST FOLLOW)
Before starting Epic validation, verify:
- [ ] The Epic (identified by $ARGUMENTS) is defined and marked as "Implementation Complete" or "Ready for Epic Validation".
- [ ] All user stories within this Epic are marked as "Complete" (implemented and passed individual code reviews).
- [ ] For each story in the Epic, a `[story-id]-review.md` document exists in `.ai/reviews/[epic-name]/`.
- [ ] All critical and major issues identified in these story-level review documents have been addressed, or have new user stories/tasks created and prioritized.
- [ ] The Epic's high-level acceptance criteria are clearly defined in its definition file.

**VIOLATION CHECK**: If any prerequisite is missing, STOP. The Epic is not ready for final validation. Address outstanding story-level issues or complete necessary reviews first.

### 3. Validation Framework
Follow QA's comprehensive testing approach:

1. **Feature Parity Validation**
   - Behavioral Comparison: Does the Godot version behave like WCS?
   - Visual Comparison: Do graphics and effects match the original feel?
   - Audio Comparison: Are sound effects and music properly integrated?
   - Performance Comparison: Does it run as well as or better than WCS?
   - Control Comparison: Do input responses feel authentic to WCS?

2. **Performance Testing**
   - Frame Rate: Maintain target FPS under normal and stress conditions
   - Memory Usage: Stay within acceptable memory footprint limits
   - Loading Times: Asset loading and scene transitions within targets
   - CPU Usage: Efficient processing without unnecessary overhead
   - GPU Usage: Optimal rendering performance for target hardware

3. **Epic-Level Validation Focus**
   - **Integration Testing**: Verify all stories within the Epic function correctly together.
   - **End-to-End Feature Parity**: Ensure the complete feature set delivered by the Epic matches WCS behavior and feel.
   - **Epic Acceptance Criteria**: Validate against the high-level acceptance criteria defined in the Epic document.
   - **Overall Performance**: Test the performance of the integrated Epic against defined benchmarks.
   - **WCS-Specific Quality Criteria**: Assess the overall gameplay impact and user experience of the completed Epic.

### 4. Testing Procedures

#### Epic Validation Process
1.  **Review Epic Definition**: Understand the Epic's scope, value proposition, and high-level acceptance criteria from `.ai/epics/[epic-name].md`.
2.  **Confirm Story Completion & Review Resolution**:
    *   Verify all associated user stories are complete.
    *   Review all `[story-id]-review.md` documents for the Epic's stories.
    *   Confirm that critical/major issues from these reviews have been addressed or have follow-up stories/tasks.
3.  **Holistic Feature Parity Testing**:
    *   Test the Epic's complete functionality against original WCS behavior and expectations.
    *   Focus on end-to-end user flows and interactions encompassed by the Epic.
4.  **Integration Testing**:
    *   Verify seamless interaction between all components/stories developed as part of the Epic.
    *   Test integration points with other Epics or existing systems if applicable.
5.  **Epic-Level Acceptance Criteria Validation**: Systematically test each high-level acceptance criterion for the Epic.
6.  **Edge Case & Stress Testing (Epic Scope)**: Test boundary conditions and error scenarios relevant to the Epic as a whole.

#### Performance Testing Process (Epic Scope)
1. **Baseline Measurement**: Establish performance benchmarks for the Epic's functionality.
2. **Load Testing**: Test under various stress conditions
3. **Optimization Validation**: Verify performance improvements
4. **Regression Testing**: Ensure changes don't degrade performance
5. **Target Validation**: Confirm all performance targets are met

#### Code Spot-Check & Review Confirmation (Streamlined)
1.  **Consult Story Reviews**: Refer to `[story-id]-review.md` documents for detailed code quality assessments of individual stories.
2.  **Verify Fixes**: Spot-check areas where critical/major issues were reported in story reviews to confirm resolution.
3.  **High-Level Code Scan**: Perform a high-level scan for any obvious regressions or new global issues introduced during integration, but avoid re-doing detailed line-by-line reviews of already-reviewed story code.
4.  **Confirm Standards Adherence**: Ensure overall adherence to GDScript coding standards and architectural principles at the Epic level.

#### Automated Testing Process (Optional - if gdUnit4 tests exist)
1. **gdUnit4 Test Execution**: Run automated test suite if available
   ```bash
   # Execute gdUnit4 tests via command line (if implemented)
   cd target/
   godot --headless --script addons/gdUnit4/bin/GdUnitCmdTool.gd --verbose --coverage --report-html --report-junit
   ```
2. **Test Result Analysis**: Review generated test reports
3. **Coverage Analysis**: Verify test coverage meets quality standards (>90%)
4. **Performance Benchmarks**: Execute performance tests if available
5. **Regression Testing**: Validate no existing functionality is broken

### 5. Quality Gates

#### Pre-Implementation Quality Gate
- [ ] Architecture approved and technically sound
- [ ] Performance requirements clearly defined
- [ ] Test criteria established and measurable
- [ ] Quality standards documented and agreed upon

#### Implementation Quality Gate
- [ ] Code follows all GDScript standards
- [ ] Unit tests written and passing (using gdUnit4 framework)
- [ ] Test coverage >90% for core functionality
- [ ] Performance benchmarks met
- [ ] Integration points tested and working
- [ ] Documentation complete and accurate

#### Final Approval Quality Gate (for the Epic)
- [ ] All constituent stories are complete and have passed their individual code reviews.
- [ ] Critical/major issues from story-level reviews are resolved or have follow-up actions.
- [ ] Epic-level integration testing passed.
- [ ] End-to-end feature parity for the Epic's scope is validated against WCS original.
- [ ] All Epic-level acceptance criteria are met.
- [ ] Overall performance targets for the Epic are achieved.
- [ ] Documentation for the Epic (including updates to the Epic file itself) is complete.

### 6. WCS-Specific Quality Criteria

#### Gameplay Feel Validation
- **Ship Movement**: Does ship handling feel like WCS?
- **Combat Mechanics**: Are weapon behaviors authentic?
- **AI Behavior**: Do enemy ships act like WCS AI?
- **Mission Flow**: Do missions progress like the original?
- **UI Responsiveness**: Does the interface feel responsive and familiar?

#### Technical Quality Standards
- **Godot Integration**: Proper use of Godot engine features
- **Performance Optimization**: Efficient use of system resources
- **Code Maintainability**: Clean, readable, well-documented code
- **Error Resilience**: Graceful handling of unexpected conditions
- **Platform Compatibility**: Works correctly on target platforms

### 7. Output Requirements
Generate a comprehensive Epic validation report:
- **Filename**: `[epic-id]-validation.md` (e.g., `EPIC-001-core-systems-validation.md`).
- **Location**: `.ai/reviews/epics/` (or a similar dedicated directory for Epic-level reviews).
- **Content**: Detailed test results for Epic-level validation, performance metrics, overall quality assessment of the Epic.
- **Decision**: EPIC APPROVED / EPIC NEEDS REVISION / EPIC REJECTED with specific reasons.
- **Recommendations**: Specific improvements if not approved, or suggestions for future related Epics.

## Critical Quality Enforcement (QA's Standards for Epics)
- "The overall Epic functionality [X] does not match WCS behavior in these key areas..."
- "Integration between stories [A] and [B] within this Epic has failed under these conditions..."
- "Performance testing for the complete Epic shows these bottlenecks..."
- "While individual stories were reviewed, the combined Epic fails to meet its high-level acceptance criterion regarding [Y]..."

## BMAD Workflow Compliance
- **Prerequisites**: All stories within the Epic must be implemented and have passed their individual `review_code_implementation` task. Critical/major issues from those reviews must be addressed.
- **Quality Standards**: Zero compromise on established criteria
- **Evidence-Based**: All assessments backed by concrete evidence
- **Documentation**: All quality processes and results thoroughly documented
- **Final Authority**: QA has final approval authority for feature completion

## Validation Report Template (for Epics)
```markdown
# Epic Validation Report: [Epic ID]: [Epic Name]

## Executive Summary
- **Epic**: [Epic ID and Name]
- **Validation Date**: [Date]
- **Validator**: QA Specialist (QA)
- **Status**: EPIC APPROVED / EPIC NEEDS REVISION / EPIC REJECTED

## 1. Epic Overview
- **Epic Definition**: [Link to `.ai/epics/[epic-name].md`]
- **Summary of Scope**: [Briefly reiterate the Epic's main goals and deliverables.]

## 2. Story Completion & Review Confirmation
- **Constituent Stories**: [List all stories belonging to this Epic.]
- **Story Review Status**: [Confirmation that all stories passed `review_code_implementation` and critical/major issues were addressed. Reference `[story-id]-review.md` files.]

## 3. Epic-Level Acceptance Criteria Validation
- **Criterion 1**: "[Epic AC Text]" - **Status**: [Met / Partially Met / Not Met] - **Comments**: [Detailed observations]
- **Criterion 2**: "[Epic AC Text]" - **Status**: [Met / Partially Met / Not Met] - **Comments**: [Detailed observations]
- ...

## 4. End-to-End Feature Parity Assessment (Epic Scope)
- **WCS Behavior Match**: [Detailed comparison of the Epic's overall functionality against original WCS behavior.]
- **User Experience (Holistic)**: [Assessment of the combined user experience delivered by the Epic.]

## 5. Integration Testing Results
- **Internal Integration (Story-to-Story)**: [Findings on how well stories within the Epic integrate.]
- **External Integration (Epic-to-Other Systems)**: [Findings on integration with other Epics or core systems, if applicable.]

## 6. Performance Validation (Epic Scope)
- **Overall Frame Rate**: [Target vs. actual performance for the Epic's features.]
- **Overall Memory Usage**: [Resource consumption analysis for the Epic.]
- **Key Loading Times**: [Performance benchmarks for Epic-related loading sequences.]

## 7. Code Quality Spot-Check Summary
- **Confirmation of Story-Level Fixes**: [Verification that major issues from story reviews were resolved.]
- **Overall Architectural Integrity**: [High-level assessment of the Epic's code structure.]
- **New Issues (if any from spot-check)**: [Document any new, overarching issues found during Epic validation.]

## 8. Issues Found (Epic Level)
*(Issues that manifest at the Epic/integration level, or significant unresolved story issues impacting the Epic)*
| ID      | Severity   | Description                                         | Impacted Stories/Components | Suggested Action                                     |
|---------|------------|-----------------------------------------------------|-----------------------------|------------------------------------------------------|
| EV-001  | Critical   | Example: Player data corruption when X and Y interact. | Story-A, Story-B            | Requires immediate fix, potentially new debug story. |
| ...     | ...        | ...                                                 | ...                         | ...                                                  |

## 9. Recommendations
- [Specific actions required for Epic approval, or suggestions for next steps.]

## 10. Final Decision
- **EPIC APPROVED**: The Epic is complete, validated, and meets all quality standards.
- **EPIC NEEDS REVISION**: Specific issues (detailed above) must be addressed. This may involve revisiting specific stories or creating new ones.
- **EPIC REJECTED**: Fundamental problems with the Epic's implementation or integration. Requires significant rework.
```

Begin validation for Epic: $ARGUMENTS

Remember: You're the final guardian of quality. Your meticulous attention to detail and unwavering standards ensure that the WCS-Godot conversion maintains the authentic feel of the original while meeting modern quality standards. Quality is never optional.
