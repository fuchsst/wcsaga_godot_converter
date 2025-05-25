# BMAD Workflow Enforcement Rules for Claude

## Purpose
These rules ensure that Claude AI assistant strictly follows the BMAD methodology when working on the WCS-Godot conversion project. These rules are automatically enforced and cannot be bypassed.

## Critical Enforcement Rules

### Rule 1: Sequential Phase Progression (MANDATORY)
**REQUIREMENT**: Must follow PRD → Architecture → Stories → Implementation → Validation

#### Before Architecture Design
- [ ] **STOP**: Verify PRD exists in `.ai/docs/[system]-prd.md`
- [ ] **STOP**: Verify PRD has been approved
- [ ] **STOP**: Run `.bmad/checklists/conversion-prd-quality-checklist.md`
- [ ] **VIOLATION**: If any check fails, REFUSE to proceed with architecture

#### Before Story Creation
- [ ] **STOP**: Verify architecture exists in `.ai/docs/[system]-architecture.md`
- [ ] **STOP**: Verify architecture has been approved
- [ ] **STOP**: Run `.bmad/checklists/godot-architecture-checklist.md`
- [ ] **VIOLATION**: If any check fails, REFUSE to proceed with stories

#### Before Implementation
- [ ] **STOP**: Verify stories exist in `.ai/stories/`
- [ ] **STOP**: Verify stories have clear acceptance criteria
- [ ] **STOP**: Run `.bmad/checklists/story-readiness-checklist.md`
- [ ] **VIOLATION**: If any check fails, REFUSE to proceed with implementation

#### Before Feature Completion
- [ ] **STOP**: Verify all acceptance criteria met
- [ ] **STOP**: Run `.bmad/checklists/story-definition-of-done-checklist.md`
- [ ] **VIOLATION**: If any check fails, REFUSE to mark feature complete

### Rule 2: Version Control Compliance (MANDATORY)
**REQUIREMENT**: All artifacts must be committed after each phase

#### Git Workflow Enforcement
- [ ] **STOP**: After analysis, verify `.ai/docs/[system]-analysis.md` is committed
- [ ] **STOP**: After PRD, verify `.ai/docs/[system]-prd.md` is committed
- [ ] **STOP**: After architecture, verify `.ai/docs/[system]-architecture.md` is committed
- [ ] **STOP**: After stories, verify `.ai/stories/` files are committed
- [ ] **STOP**: After implementation, verify `target/` submodule is committed
- [ ] **VIOLATION**: If artifacts not committed, REFUSE to proceed to next phase

### Rule 3: Template Compliance (MANDATORY)
**REQUIREMENT**: All documents must use specified templates

#### Template Enforcement
- [ ] **PRD Creation**: MUST use `.bmad/templates/conversion-prd-template.md`
- [ ] **Architecture Design**: MUST use `.bmad/templates/godot-architecture-template.md`
- [ ] **Story Creation**: MUST use `.bmad/templates/wcs-story-template.md`
- [ ] **Project Briefs**: MUST use `.bmad/templates/wcs-conversion-brief-template.md`
- [ ] **VIOLATION**: If wrong template used, REFUSE to proceed

### Rule 4: Quality Gate Compliance (MANDATORY)
**REQUIREMENT**: All quality checklists must be completed

#### Checklist Enforcement
- [ ] **Before Architecture**: Run `.bmad/checklists/conversion-prd-quality-checklist.md`
- [ ] **Before Stories**: Run `.bmad/checklists/godot-architecture-checklist.md`
- [ ] **Before Implementation**: Run `.bmad/checklists/story-readiness-checklist.md`
- [ ] **Before Completion**: Run `.bmad/checklists/story-definition-of-done-checklist.md`
- [ ] **For Changes**: Run `.bmad/checklists/change-management-checklist.md`
- [ ] **VIOLATION**: If checklist not completed, REFUSE to proceed

### Rule 5: Single Epic Focus (MANDATORY)
**REQUIREMENT**: Only one epic can be in progress at a time

#### Epic Management Enforcement
- [ ] **STOP**: Verify only one epic is marked "In Progress"
- [ ] **STOP**: Verify previous epic is marked "Complete" or "Cancelled"
- [ ] **VIOLATION**: If multiple epics in progress, REFUSE to start new work

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
- MUST create analysis documents in `.ai/docs/`
- MUST use `.bmad/templates/wcs-conversion-brief-template.md`

### Curly (Conversion Manager)
- MUST use `.bmad/templates/conversion-prd-template.md`
- MUST run `.bmad/checklists/conversion-prd-quality-checklist.md`
- MUST ensure single epic focus

### Mo (Godot Architect)
- MUST use `.bmad/templates/godot-architecture-template.md`
- MUST run `.bmad/checklists/godot-architecture-checklist.md`
- MUST enforce Godot-native design patterns

### SallySM (Story Manager)
- MUST use `.bmad/templates/wcs-story-template.md`
- MUST run `.bmad/checklists/story-readiness-checklist.md`
- MUST enforce workflow compliance

### Dev (GDScript Developer)
- MUST enforce 100% static typing
- MUST create `CLAUDE.md` for code packages
- MUST run `.bmad/checklists/story-definition-of-done-checklist.md`

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
