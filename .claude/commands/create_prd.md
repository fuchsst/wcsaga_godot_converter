Guide the creation of a Product Requirements Document (PRD) for converting a WCS system to Godot.

You are initiating PRD creation for the WCS system: $ARGUMENTS

## PRD Creation Process

### 1. Load BMAD Framework
- Load the Conversion Manager persona (Curly) from `bmad-workflow/personas/conversion-manager.md`
- Reference the PRD template from `bmad-workflow/templates/conversion-prd-template.md`
- Review the PRD creation task from `bmad-workflow/tasks/create-conversion-prd.md`

### 2. Prerequisites Check
Before starting PRD creation, verify:
- [ ] WCS system analysis exists in `bmad-artifacts/docs/[system-name]-analysis.md`
- [ ] System scope and boundaries are understood
- [ ] Stakeholder requirements have been gathered
- [ ] Conversion goals are clearly defined

### 3. PRD Development Steps
Follow the structured approach:

1. **Requirements Gathering**
   - Review WCS system analysis for technical understanding
   - Identify key stakeholders and their requirements
   - Define success criteria and acceptance standards
   - Establish scope boundaries and constraints

2. **Feature Definition**
   - Core Features: Essential functionality that must be preserved
   - Enhanced Features: Improvements possible in Godot implementation
   - Deferred Features: Functionality to be implemented later
   - Excluded Features: Functionality not being converted

3. **Technical Requirements**
   - Performance Requirements: Frame rate, memory, loading time targets
   - Platform Requirements: Target platforms and compatibility needs
   - Integration Requirements: How system connects with other converted systems
   - Quality Requirements: Code standards, testing, and documentation needs

4. **User Experience Requirements**
   - Gameplay Requirements: How conversion affects player experience
   - Visual Requirements: Graphics, effects, and visual fidelity standards
   - Audio Requirements: Sound effects and music integration needs
   - Control Requirements: Input handling and responsiveness standards

### 4. Quality Validation
Use the PM checklist to ensure:
- [ ] All functional requirements clearly defined with acceptance criteria
- [ ] Technical requirements are specific and measurable
- [ ] Success criteria are objective and testable
- [ ] Scope boundaries are clearly established
- [ ] Dependencies and constraints are identified
- [ ] Stakeholder requirements are captured and prioritized
- [ ] Implementation approach is realistic and achievable

### 5. Output Requirements
Create comprehensive PRD document:
- **Location**: `bmad-artifacts/docs/[system-name]-prd.md`
- **Template**: Use `bmad-workflow/templates/conversion-prd-template.md`
- **Content**: Complete all sections with WCS-specific details
- **Approval**: Document must be approved before architecture phase

## Critical Reminders
- Focus on business value and player impact
- Consider resource constraints and timeline realities
- Prioritize features based on conversion goals
- Ensure requirements are specific and testable
- Balance ambition with practical implementation constraints
- Document all prioritization decisions with clear rationale

## BMAD Workflow Compliance
- **Prerequisites**: WCS system analysis must be completed
- **Approval Required**: PRD must be approved before proceeding to architecture
- **Quality Gates**: All checklist items must be satisfied
- **Next Phase**: Architecture design cannot begin without approved PRD

Begin PRD creation for: $ARGUMENTS
