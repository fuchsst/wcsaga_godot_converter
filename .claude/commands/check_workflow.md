Verify BMAD workflow compliance and check for any violations of critical rules.

You are performing a comprehensive BMAD workflow compliance check for the WCS-Godot conversion project.

## Workflow Compliance Verification

### 1. Load Workflow Enforcement Checklist
First, reference the workflow enforcement checklist from `bmad-workflow/checklists/workflow-enforcement.md` to understand all critical rules and requirements.

### 2. Check Sequential Phase Progression
Verify that the project is following the required sequence: PRD → Architecture → Stories → Implementation → Validation

**Check for:**
- Are there any architecture documents without approved PRDs?
- Are there any stories created without approved architecture?
- Is any implementation happening without approved stories?
- Are quality gates being bypassed?

### 3. Validate Single Epic Focus Rule
Ensure only one epic is in progress at a time:
- Check `bmad-artifacts/epics/` directory for multiple "in-progress" epics
- Verify current epic status and scope
- Flag any violations of the single epic rule

### 4. Review Quality Gate Compliance
Check that all quality gates are being properly executed:
- PRD approval documentation
- Architecture approval documentation  
- Story approval and readiness
- Implementation quality standards
- Testing and validation completion

### 5. Verify Documentation Standards
Ensure all BMAD artifacts are properly documented:
- Check `bmad-artifacts/docs/` for required PRD and architecture documents
- Verify `bmad-artifacts/stories/` contains properly formatted user stories
- Confirm `bmad-artifacts/reviews/` has approval documentation
- Validate that all documents follow established templates

### 6. Check Code Quality Standards
If implementation has begun, verify GDScript standards compliance:
- Static typing requirements (no untyped variables/functions)
- Class name declarations for reusable classes
- Documentation requirements (docstrings for public functions)
- Error handling and resource management
- Architecture pattern adherence

## Report Format

Provide a comprehensive compliance report with:

### Compliance Status
- **COMPLIANT**: All rules followed, no violations found
- **MINOR VIOLATIONS**: Small issues that need correction
- **MAJOR VIOLATIONS**: Significant rule violations requiring immediate attention
- **CRITICAL VIOLATIONS**: Workflow breakdown requiring project halt

### Detailed Findings
For each area checked, report:
- Current status
- Any violations found
- Specific corrective actions needed
- Priority level for addressing issues

### Recommendations
- Immediate actions required
- Process improvements suggested
- Preventive measures for future compliance

## Critical Reminders
- BMAD workflow rules are non-negotiable
- Quality gates cannot be bypassed
- Sequential progression must be maintained
- Single epic focus must be enforced
- All violations must be documented and corrected

Generate a detailed compliance report and flag any violations that need immediate attention.
