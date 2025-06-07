# BMAD Workflow Enforcement Rules for Claude

## Purpose
These rules ensure that Claude AI assistant strictly follows the BMAD methodology when working on the WCS-Godot conversion project. These rules are automatically enforced and cannot be bypassed.

## Critical Enforcement Rules

### Rule 1: Sequential Phase Progression (MANDATORY)
**REQUIREMENT**: Must follow PRD → Epic Definition → Architecture → Stories → Implementation → Code Review → Validation

#### Before Epic Definition
- [ ] **STOP**: Verify PRD exists in `bmad-artifacts/docs/[system]-prd.md` (or an overall project PRD).
- [ ] **STOP**: Verify PRD has been approved.
- [ ] **STOP**: Run `bmad-workflow/checklists/conversion-prd-quality-checklist.md` (as applicable to the PRD).
- [ ] **VIOLATION**: If any check fails, REFUSE to proceed with Epic definition.
- [ ] **NOTE**: Epic definition involves using `define-epics-list.md` (interactive with user, Larry, Mo) and then `create-epic.md` for individual epics.

#### Before Architecture Design (for an Epic's scope)
- [ ] **STOP**: Verify the parent Epic is defined in `bmad-artifacts/epics/[epic-name].md` and is approved/active.
- [ ] **STOP**: Verify PRD (that the Epic aligns with) exists and is approved.
- [ ] **VIOLATION**: If any check fails, REFUSE to proceed with architecture for that Epic's scope.

#### Before Story Creation (for an Epic)
- [ ] **STOP**: Verify the parent Epic is defined, approved, and "In Progress".
- [ ] **STOP**: Verify architecture for the Epic's scope exists in `bmad-artifacts/docs/[epic-scope]-architecture.md` and is approved.
- [ ] **STOP**: Run `bmad-workflow/checklists/godot-architecture-checklist.md` for the relevant architecture.
- [ ] **VIOLATION**: If any check fails, REFUSE to proceed with stories for that Epic.

#### Before Implementation
- [ ] **STOP**: Verify stories exist in `bmad-artifacts/stories/`
- [ ] **STOP**: Verify stories have clear acceptance criteria
- [ ] **STOP**: Run `bmad-workflow/checklists/story-readiness-checklist.md`
- [ ] **VIOLATION**: If any check fails, REFUSE to proceed with implementation

#### Before Feature Completion
- [ ] **STOP**: Verify all acceptance criteria met
- [ ] **STOP**: Run `bmad-workflow/checklists/story-definition-of-done-checklist.md`
- [ ] **VIOLATION**: If any check fails, REFUSE to mark feature complete

#### Before Code Review
- [ ] **STOP**: Verify implementation is complete for the story.
- [ ] **STOP**: Verify the story has passed its Definition of Done checklist (`bmad-workflow/checklists/story-definition-of-done-checklist.md`), signed off by Dev.
- [ ] **VIOLATION**: If any check fails, REFUSE to proceed with Code Review. Implementation needs to be finalized first.

#### Before Validation
- [ ] **STOP**: Verify a code review has been conducted by QA and Godot Architect for the implemented story.
- [ ] **STOP**: Check for the existence of a corresponding review document in `bmad-artifacts/reviews/[epic-name]/[story-id]-review.md`.
- [ ] **STOP**: Verify all critical/major issues identified in the code review document have either been addressed or have new user stories/tasks created and prioritized for them.
- [ ] **VIOLATION**: If any check fails, REFUSE to proceed with final feature validation until code review feedback is appropriately handled.

### Rule 2: Version Control Compliance (MANDATORY)
**REQUIREMENT**: All artifacts must be committed after each phase

#### Git Workflow Enforcement
- [ ] **STOP**: After analysis, verify `bmad-artifacts/docs/[system]-analysis.md` is committed.
- [ ] **STOP**: After PRD, verify `bmad-artifacts/docs/[system]-prd.md` is committed.
- [ ] **STOP**: After Epic Definition (both list and individual epics), verify `bmad-artifacts/epics/` files are committed.
- [ ] **STOP**: After architecture, verify `bmad-artifacts/docs/[system]-architecture.md` (or `[epic-scope]-architecture.md`) is committed.
- [ ] **STOP**: After stories, verify `bmad-artifacts/stories/` files are committed.
- [ ] **STOP**: After implementation, verify `target/` submodule is committed.
- [ ] **VIOLATION**: If artifacts not committed, REFUSE to proceed to next phase.

### Rule 3: Template Compliance (MANDATORY)
**REQUIREMENT**: All documents must use specified templates

#### Template Enforcement
- [ ] **PRD Creation**: MUST use `bmad-workflow/templates/conversion-prd-template.md`.
- [ ] **Epic Definition**: MUST use `bmad-workflow/templates/wcs-epic-template.md`.
- [ ] **Architecture Design**: MUST use `bmad-workflow/templates/godot-architecture-template.md`.
- [ ] **Story Creation**: MUST use `bmad-workflow/templates/wcs-story-template.md`.
- [ ] **Project Briefs**: MUST use `bmad-workflow/templates/wcs-conversion-brief-template.md`.
- [ ] **VIOLATION**: If wrong template used, REFUSE to proceed.

### Rule 4: Quality Gate Compliance (MANDATORY)
**REQUIREMENT**: All quality checklists must be completed

#### Checklist Enforcement
- [ ] **Before Epic Definition**: Run `bmad-workflow/checklists/conversion-prd-quality-checklist.md` (for the PRD).
- [ ] **After Epic Definition (Before Approval/Architecture)**: Run `bmad-workflow/checklists/epic-quality-checklist.md`.
- [ ] **Before Architecture Design (for an Epic's scope)**: Ensure parent Epic passed its quality checklist.
- [ ] **Before Story Creation**: Run `bmad-workflow/checklists/godot-architecture-checklist.md` (for the relevant architecture).
- [ ] **Before Implementation**: Run `bmad-workflow/checklists/story-readiness-checklist.md`.
- [ ] **Before Completion (Story)**: Run `bmad-workflow/checklists/story-definition-of-done-checklist.md`.
- [ ] **For Changes**: Run `bmad-workflow/checklists/change-management-checklist.md`.
- [ ] **VIOLATION**: If checklist not completed or failed, REFUSE to proceed.

### Rule 5: Single Epic Focus (MANDATORY)
**REQUIREMENT**: Only one Epic can be "In Progress" at a time for story creation and implementation. Multiple epics can be in a "Defined" or "To Do" state.

#### Epic Management Enforcement
- [ ] **VERIFY**: When creating stories or starting implementation, ensure only one Epic is marked "In Progress".
- [ ] **VERIFY**: Before marking an Epic "In Progress", ensure any previously "In Progress" Epic is now "Complete" or "Cancelled" or "On Hold".
- [ ] **VIOLATION**: If attempting to create stories for an Epic that is not "In Progress", or if multiple Epics are "In Progress" simultaneously for active development, REFUSE to proceed with story creation/implementation for non-active/conflicting Epics.
- [ ] **NOTE**: The `define-epics-list` command can be used to identify and create placeholders for multiple epics. The `create-epic` command can be used to detail multiple epics into a "Defined" state. This rule primarily applies to the transition to "In Progress" for development.

### Rule 6: Code Quality Standards (MANDATORY)
**REQUIREMENT**: All GDScript code must meet quality standards

#### Code Quality Enforcement
- [ ] **Static Typing**: REFUSE any untyped variables or functions
- [ ] **Class Names**: REQUIRE `class_name` declarations for reusable classes
- [ ] **Documentation**: REQUIRE docstrings for all public functions
- [ ] **Package Docs**: REQUIRE `CLAUDE.md` for significant code packages
- [ ] **VIOLATION**: If standards not met, REFUSE to approve code

## Automatic Responses to Violations

### Minor Violations
**Response**: 
```
❌ BMAD WORKFLOW VIOLATION DETECTED
Issue: [Specific violation]
Required Action: [Specific corrective action]
Cannot proceed until violation is resolved.
```

### Major Violations
**Response**:
```
🛑 CRITICAL BMAD WORKFLOW VIOLATION
Issue: [Specific violation]
Impact: [Workflow integrity compromised]
Required Action: Return to [specific phase] and complete all requirements
All work STOPPED until compliance restored.
```

### Critical Violations
**Response**:
```
🚨 SEVERE BMAD WORKFLOW VIOLATION
Issue: [Specific violation]
Impact: Project quality standards compromised
Required Action: Full workflow review and corrective measures
Development HALTED until explicit approval to resume.
```

## Persona-Specific Enforcement

### Larry (WCS Analyst)
- MUST reference specific files in `source/` submodule
- MUST create analysis documents in `bmad-artifacts/docs/`
- MUST use `bmad-workflow/templates/wcs-conversion-brief-template.md`

### Curly (Conversion Manager)
- MUST use `bmad-workflow/templates/conversion-prd-template.md` for PRDs.
- MUST use `bmad-workflow/templates/wcs-epic-template.md` for Epics.
- MUST run `bmad-workflow/checklists/conversion-prd-quality-checklist.md` for PRDs.
- MUST run `bmad-workflow/checklists/epic-quality-checklist.md` for Epics.
- MUST lead Epic definition using `define-epics-list` and `create-epic` commands.
- MUST ensure single epic focus for "In Progress" development.

### Mo (Godot Architect)
- MUST use `bmad-workflow/templates/godot-architecture-template.md`.
- MUST run `bmad-workflow/checklists/godot-architecture-checklist.md`.
- MUST enforce Godot-native design patterns.
- MUST collaborate on Epic definition by providing high-level feasibility.

### SallySM (Story Manager)
- MUST use `bmad-workflow/templates/wcs-story-template.md`.
- MUST run `bmad-workflow/checklists/story-readiness-checklist.md`.
- MUST ensure stories are derived from an approved and active Epic.
- MUST enforce workflow compliance regarding Epic-to-Story flow.

### Dev (GDScript Developer)
- MUST enforce 100% static typing
- MUST create brief `CLAUDE.md` for code packages
- MUST run `bmad-workflow/checklists/story-definition-of-done-checklist.md`

### QA (Quality Assurance)
- MUST validate all quality checklists
- MUST verify feature parity with WCS
- MUST approve only compliant implementations

## Enforcement Commands

### Workflow Validation
```
/bmad:check_workflow - Validate current workflow state
/bmad:validate_phase [phase] - Check specific phase compliance
/bmad:run_checklist [checklist] - Execute quality gate
```

### Violation Reporting
```
/bmad:report_violation [type] [description] - Document violation
/bmad:escalate_violation [violation_id] - Escalate to project leadership
```

### Compliance Restoration
```
/bmad:restore_compliance [phase] - Return to compliant state
/bmad:approve_override [justification] - Request violation override (rare)
```

## Override Conditions (EXTREMELY RARE)

### Emergency Override
Only allowed for:
- Critical production issues
- External dependency failures
- Force majeure circumstances

### Override Process
1. Document emergency justification
2. Escalate to project leadership
3. Implement temporary workaround
4. Schedule compliance restoration
5. Conduct post-incident review

## Continuous Monitoring

### Automated Checks
- Phase progression validation
- Template compliance verification
- Quality gate completion tracking
- Git commit verification
- Code quality standards enforcement

### Violation Tracking
- All violations logged with timestamps
- Violation patterns analyzed for process improvement
- Repeat violations escalated automatically
- Compliance metrics reported regularly

---

**REMEMBER**: These rules are not suggestions - they are mandatory requirements that ensure project success. BMAD workflow violations lead to technical debt, rework, and project failure. No exceptions without explicit override approval.

**CLAUDE DIRECTIVE**: Always check these rules before proceeding with any BMAD workflow action. When in doubt, STOP and verify compliance.
