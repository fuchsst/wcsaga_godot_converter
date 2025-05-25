# BMAD Workflow Enforcement Configuration

## Purpose
This configuration file defines how Claude should enforce BMAD workflow rules and integrate with the project's quality gates, templates, and checklists.

## Enforcement Hierarchy

### Level 1: Critical Rules (Cannot be bypassed)
1. **Sequential Phase Progression**: PRD → Architecture → Stories → Implementation → Validation
2. **Version Control Compliance**: All artifacts committed after each phase
3. **Template Compliance**: All documents use specified templates
4. **Quality Gate Compliance**: All checklists completed before proceeding

### Level 2: Quality Standards (Enforced with warnings)
1. **Code Quality Standards**: Static typing, documentation, naming conventions
2. **Architecture Standards**: Godot-native patterns, performance considerations
3. **Documentation Standards**: Completeness, clarity, consistency

### Level 3: Best Practices (Recommended with guidance)
1. **Performance Optimization**: Efficient algorithms and resource usage
2. **Maintainability**: Clean code, modular design, clear interfaces
3. **Testing**: Comprehensive test coverage and validation

## Workflow State Tracking

### Phase States
- **Not Started**: No artifacts exist
- **In Progress**: Artifacts being created but not complete
- **Complete**: All artifacts created and quality gates passed
- **Approved**: Formal approval received, ready for next phase

### Epic States
- **Planned**: Epic defined but not started
- **In Progress**: Currently active epic (only one allowed)
- **Complete**: All stories completed and validated
- **Cancelled**: Epic cancelled or deprioritized

### Story States
- **Draft**: Story created but not ready for implementation
- **Ready**: Story approved and ready for implementation
- **In Progress**: Implementation started
- **Complete**: All acceptance criteria met
- **Validated**: QA approved

## Template Enforcement Matrix

| Phase | Required Template | Checklist | Output Location |
|-------|------------------|-----------|-----------------|
| Analysis | `wcs-conversion-brief-template.md` | N/A | `.ai/docs/[system]-analysis.md` |
| PRD | `conversion-prd-template.md` | `conversion-prd-quality-checklist.md` | `.ai/docs/[system]-prd.md` |
| Architecture | `godot-architecture-template.md` | `godot-architecture-checklist.md` | `.ai/docs/[system]-architecture.md` |
| Stories | `wcs-story-template.md` | `story-readiness-checklist.md` | `.ai/stories/[story-name].md` |
| Implementation | Package docs | `story-definition-of-done-checklist.md` | `target/` + `CLAUDE.md` |
| Validation | Review reports | All applicable checklists | `.ai/reviews/[feature]-validation.md` |

## Persona Enforcement Rules

### Larry (WCS Analyst)
```yaml
required_inputs:
  - source_code: "source/" submodule
  - system_focus: Specific WCS system to analyze
mandatory_outputs:
  - analysis_document: ".ai/docs/[system]-analysis.md"
  - conversion_brief: Uses "wcs-conversion-brief-template.md"
quality_gates:
  - technical_accuracy: Must reference actual source code
  - completeness: All major system aspects covered
  - clarity: Understandable by other team members
```

### Curly (Conversion Manager)
```yaml
required_inputs:
  - analysis_document: From Larry
  - business_requirements: Stakeholder input
mandatory_outputs:
  - prd_document: ".ai/docs/[system]-prd.md"
  - project_brief: Uses "wcs-conversion-brief-template.md"
quality_gates:
  - checklist: "conversion-prd-quality-checklist.md"
  - scope_clarity: Clear in/out of scope definitions
  - success_criteria: Measurable objectives defined
```

### Mo (Godot Architect)
```yaml
required_inputs:
  - prd_document: From Curly (approved)
  - technical_constraints: Godot capabilities and limitations
mandatory_outputs:
  - architecture_document: ".ai/docs/[system]-architecture.md"
  - technical_specifications: Detailed implementation guidance
quality_gates:
  - checklist: "godot-architecture-checklist.md"
  - godot_native: Leverages Godot strengths
  - performance: Meets performance requirements
```

### SallySM (Story Manager)
```yaml
required_inputs:
  - architecture_document: From Mo (approved)
  - epic_definition: High-level feature grouping
mandatory_outputs:
  - user_stories: ".ai/stories/[story-name].md"
  - epic_breakdown: Complete story mapping
quality_gates:
  - checklist: "story-readiness-checklist.md"
  - acceptance_criteria: Clear and testable
  - dependencies: Properly mapped and managed
```

### Dev (GDScript Developer)
```yaml
required_inputs:
  - user_stories: From SallySM (approved)
  - architecture_specs: Technical implementation guidance
mandatory_outputs:
  - gdscript_code: "target/" submodule
  - package_docs: "CLAUDE.md" for significant modules
  - unit_tests: Comprehensive test coverage
quality_gates:
  - checklist: "story-definition-of-done-checklist.md"
  - static_typing: 100% typed code
  - documentation: All public APIs documented
```

### QA (Quality Assurance)
```yaml
required_inputs:
  - implemented_features: From Dev
  - acceptance_criteria: From user stories
mandatory_outputs:
  - validation_reports: ".ai/reviews/[feature]-validation.md"
  - approval_documentation: Quality gate completion
quality_gates:
  - feature_parity: Matches WCS original behavior
  - performance: Meets specified requirements
  - integration: Works with other systems
```

## Violation Response Protocols

### Automatic Responses
```yaml
minor_violation:
  response: "❌ BMAD WORKFLOW VIOLATION DETECTED"
  action: "Provide specific corrective guidance"
  escalation: "None"

major_violation:
  response: "🛑 CRITICAL BMAD WORKFLOW VIOLATION"
  action: "Stop all work, return to compliant state"
  escalation: "Log violation, require explicit resolution"

critical_violation:
  response: "🚨 SEVERE BMAD WORKFLOW VIOLATION"
  action: "Halt development, escalate to leadership"
  escalation: "Full workflow review required"
```

### Violation Categories
```yaml
phase_skipping:
  severity: "critical"
  description: "Attempting to proceed without completing previous phase"
  
template_non_compliance:
  severity: "major"
  description: "Using wrong template or not following template structure"
  
quality_gate_bypass:
  severity: "major"
  description: "Proceeding without completing required checklists"
  
code_quality_violation:
  severity: "minor"
  description: "Code doesn't meet quality standards"
  
git_workflow_violation:
  severity: "major"
  description: "Artifacts not committed after phase completion"
```

## Integration Points

### File System Monitoring
```yaml
watch_directories:
  - ".ai/docs/": "PRD and architecture documents"
  - ".ai/stories/": "User stories and epic definitions"
  - ".ai/reviews/": "Validation and approval documents"
  - "target/": "Godot project implementation"

required_files:
  - ".bmad/checklists/workflow-enforcement.md": "Master workflow checklist"
  - ".claude/rules/bmad-workflow-rules.md": "Claude enforcement rules"
  - "CLAUDE.md": "Project context and standards"
  - "README.md": "Project documentation"
```

### Quality Gate Integration
```yaml
checklist_execution:
  trigger: "Before phase transition"
  validation: "All items must be checked"
  documentation: "Results logged in .ai/reviews/"
  
template_validation:
  trigger: "Document creation"
  validation: "Must use specified template"
  enforcement: "Refuse non-compliant documents"
  
git_validation:
  trigger: "Phase completion"
  validation: "All artifacts committed"
  enforcement: "Block next phase until committed"
```

## Monitoring and Reporting

### Compliance Metrics
```yaml
phase_completion_rate:
  description: "Percentage of phases completed without violations"
  target: "100%"
  
quality_gate_pass_rate:
  description: "Percentage of quality gates passed on first attempt"
  target: ">95%"
  
template_compliance_rate:
  description: "Percentage of documents using correct templates"
  target: "100%"
  
git_workflow_compliance:
  description: "Percentage of phases with proper commits"
  target: "100%"
```

### Violation Tracking
```yaml
violation_log:
  location: ".ai/reviews/violations.log"
  format: "timestamp | severity | type | description | resolution"
  retention: "Project lifetime"
  
trend_analysis:
  frequency: "Weekly"
  focus: "Recurring violation patterns"
  action: "Process improvement recommendations"
```

## Emergency Procedures

### Override Conditions
```yaml
emergency_override:
  conditions:
    - "Critical production issue"
    - "External dependency failure"
    - "Force majeure circumstances"
  
  process:
    1. "Document emergency justification"
    2. "Escalate to project leadership"
    3. "Implement temporary workaround"
    4. "Schedule compliance restoration"
    5. "Conduct post-incident review"
  
  approval_required: true
  documentation_mandatory: true
```

### Recovery Procedures
```yaml
compliance_restoration:
  trigger: "After violation or override"
  steps:
    1. "Assess current state"
    2. "Identify missing artifacts"
    3. "Complete required quality gates"
    4. "Validate all dependencies"
    5. "Resume normal workflow"
  
  validation: "Full workflow review"
  approval: "QA sign-off required"
```

---

**CONFIGURATION STATUS**: Active and enforced for all BMAD workflow operations.

**LAST UPDATED**: Project initialization

**NEXT REVIEW**: After first epic completion
