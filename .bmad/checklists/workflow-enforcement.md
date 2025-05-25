# BMAD Workflow Enforcement Checklist

## Purpose
This checklist ensures that the BMAD workflow is followed correctly and that no critical steps are skipped in the WCS-Godot conversion process. It serves as a quality gate to maintain project standards and prevent workflow violations.

## Critical Workflow Rules

### Rule 1: Sequential Phase Progression
**REQUIREMENT**: Must follow PRD → Architecture → Stories → Implementation → Validation

#### Before Architecture Design
- [ ] **PRD Exists**: A completed PRD document exists in `.ai/docs/`
- [ ] **PRD Approved**: PRD has been reviewed and approved by stakeholders
- [ ] **Requirements Clear**: All functional and technical requirements are clearly defined
- [ ] **Scope Defined**: In-scope and out-of-scope items are explicitly listed
- [ ] **Success Criteria**: Measurable success criteria are established

**VIOLATION CHECK**: If any item is unchecked, STOP and complete PRD phase first.

#### Before Story Creation
- [ ] **Architecture Exists**: A completed architecture document exists in `.ai/docs/`
- [ ] **Architecture Approved**: Architecture has been reviewed and approved
- [ ] **Technical Specs Complete**: All technical specifications are detailed and actionable
- [ ] **Integration Points Defined**: System interfaces and communication patterns are specified
- [ ] **Implementation Roadmap**: Clear phases and dependencies are documented

**VIOLATION CHECK**: If any item is unchecked, STOP and complete Architecture phase first.

#### Before Implementation
- [ ] **Stories Exist**: User stories exist in `.ai/stories/` directory
- [ ] **Stories Approved**: All stories have been reviewed and approved
- [ ] **Acceptance Criteria**: Each story has clear, testable acceptance criteria
- [ ] **Dependencies Resolved**: All story dependencies are identified and planned
- [ ] **Architecture Reference**: Stories reference specific architecture components

**VIOLATION CHECK**: If any item is unchecked, STOP and complete Story phase first.

#### Before Feature Completion
- [ ] **Implementation Complete**: All story acceptance criteria have been met
- [ ] **Code Quality**: Code meets all quality standards (static typing, documentation, etc.)
- [ ] **Tests Written**: Unit tests exist and are passing
- [ ] **Performance Validated**: Performance requirements have been verified
- [ ] **Integration Tested**: System integration has been validated

**VIOLATION CHECK**: If any item is unchecked, STOP and complete Implementation phase first.

### Rule 2: Version Control Compliance
**REQUIREMENT**: All artifacts and code must be committed after each major phase completion

#### Git Workflow Requirements
- [ ] **After Analysis**: Commit `.ai/docs/[system]-analysis.md` and related documents
- [ ] **After PRD**: Commit `.ai/docs/[system]-prd.md` and project briefs  
- [ ] **After Architecture**: Commit `.ai/docs/[system]-architecture.md` and specifications
- [ ] **After Stories**: Commit `.ai/stories/[story-files].md` and epic updates
- [ ] **After Implementation**: Commit `target/` submodule code + `CLAUDE.md` package docs
- [ ] **After Validation**: Commit `.ai/reviews/[validation-reports].md` and approvals

**VIOLATION CHECK**: If phase artifacts are not committed, STOP and commit before proceeding.

### Rule 3: Single Epic Focus
**REQUIREMENT**: Only one epic can be in progress at a time

#### Epic Management
- [ ] **Current Epic Identified**: There is exactly one epic marked as "In Progress"
- [ ] **Previous Epic Complete**: Any previous epic is marked as "Complete" or "Cancelled"
- [ ] **Epic Scope Clear**: Current epic boundaries and deliverables are well-defined
- [ ] **Epic Dependencies**: Dependencies between epics are documented and managed

**VIOLATION CHECK**: If multiple epics are in progress, STOP and focus on one epic.

### Rule 4: Quality Gate Compliance
**REQUIREMENT**: All quality gates must be passed before proceeding

#### Documentation Quality
- [ ] **Complete Documentation**: All required documents exist and are complete
- [ ] **Consistent Formatting**: Documents follow established templates and standards
- [ ] **Clear Language**: Documentation is clear, unambiguous, and actionable
- [ ] **Proper References**: All references to source code, files, and systems are accurate
- [ ] **Version Control**: Documents are properly versioned and tracked

#### Code Quality (for Implementation Phase)
- [ ] **Static Typing**: All GDScript code uses static typing (no untyped variables/functions)
- [ ] **Class Names**: All reusable classes have `class_name` declarations
- [ ] **Documentation**: All public functions have docstrings
- [ ] **Naming Conventions**: Code follows established naming conventions
- [ ] **Error Handling**: Proper error checking and graceful failure handling
- [ ] **Resource Management**: Proper use of preload vs load, resource cleanup
- [ ] **Signal Declarations**: Properly typed signal declarations with documentation

#### Architecture Quality
- [ ] **Godot Native**: Architecture leverages Godot's strengths (nodes, signals, scenes)
- [ ] **Performance Conscious**: Performance implications considered and documented
- [ ] **Maintainable**: Architecture is easy to understand and modify
- [ ] **Scalable**: Design can handle growth and additional features
- [ ] **Testable**: Systems are designed for easy testing and validation

### Rule 5: Approval Requirements
**REQUIREMENT**: All major artifacts must be formally approved

#### PRD Approval
- [ ] **Technical Review**: Technical feasibility and approach validated
- [ ] **Scope Review**: Scope is appropriate and achievable
- [ ] **Resource Review**: Required resources and timeline are realistic
- [ ] **Stakeholder Sign-off**: All relevant stakeholders have approved

#### Architecture Approval
- [ ] **Technical Review**: Architecture is sound and follows best practices
- [ ] **Performance Review**: Performance requirements can be met
- [ ] **Integration Review**: Integration with other systems is well-planned
- [ ] **Implementation Review**: Architecture provides clear implementation guidance

#### Story Approval
- [ ] **Clarity Review**: Stories are clear and unambiguous
- [ ] **Testability Review**: Acceptance criteria are testable and measurable
- [ ] **Scope Review**: Story scope is appropriate for implementation
- [ ] **Dependency Review**: Dependencies are identified and managed

## Workflow Violation Responses

### Minor Violations
**Examples**: Missing documentation, incomplete checklists, formatting issues

**Response**:
1. Document the violation
2. Complete the missing requirements
3. Re-run the checklist
4. Proceed when all items are satisfied

### Major Violations
**Examples**: Skipping entire phases, implementing without architecture, multiple epics in progress

**Response**:
1. STOP all work immediately
2. Document the violation and impact
3. Return to the appropriate workflow phase
4. Complete all missing requirements
5. Re-run full workflow validation
6. Proceed only when compliance is restored

### Critical Violations
**Examples**: Deploying untyped code, implementing without PRD, ignoring quality standards

**Response**:
1. HALT all development work
2. Escalate to project leadership
3. Conduct full workflow review
4. Implement corrective measures
5. Establish additional safeguards
6. Resume only with explicit approval

## Checklist Usage Instructions

### For BMAD Personas
- **Run this checklist before starting any new phase**
- **Reference specific sections relevant to your role**
- **Document any violations found and corrective actions taken**
- **Do not proceed if violations exist**

### For Project Management
- **Use this checklist during phase transitions**
- **Validate compliance before approving phase completion**
- **Track violations and trends for process improvement**
- **Ensure all team members understand and follow the workflow**

### For Quality Assurance
- **Validate checklist completion before final approval**
- **Audit workflow compliance regularly**
- **Report violations and recommend process improvements**
- **Ensure quality standards are maintained throughout the project**

## Continuous Improvement

### Checklist Maintenance
- [ ] **Regular Review**: Checklist is reviewed and updated regularly
- [ ] **Feedback Integration**: Team feedback is incorporated into improvements
- [ ] **Process Evolution**: Checklist evolves with project needs and lessons learned
- [ ] **Training Updates**: Team training is updated when checklist changes

### Metrics and Monitoring
- [ ] **Violation Tracking**: All violations are documented and tracked
- [ ] **Trend Analysis**: Violation patterns are analyzed for process improvement
- [ ] **Success Metrics**: Workflow compliance metrics are monitored and reported
- [ ] **Process Effectiveness**: Overall workflow effectiveness is regularly assessed

---

**Remember**: This checklist is not bureaucracy - it's quality assurance. Following the BMAD workflow ensures that we build the right thing, the right way, with the right quality standards. Shortcuts lead to technical debt, rework, and project failure.
