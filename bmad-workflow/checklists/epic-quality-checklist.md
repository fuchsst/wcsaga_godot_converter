# Epic Quality Checklist

## Purpose
This checklist ensures that WCS Epics are well-defined, strategically aligned, and provide a solid foundation for subsequent architecture design and story breakdown before being marked as "Defined" or "Approved".

## Reviewer: Curly (Conversion Manager), with input from Larry (WCS Analyst) & Mo (Godot Architect)
**Usage**: Run this checklist before approving an Epic definition created using `bmad-workflow/templates/wcs-epic-template.md`.

## Epic Foundation & Strategic Alignment

### Clarity and Purpose
- [ ] **Epic Name & ID**: Clear, descriptive name and unique ID (e.g., EPIC-001) are present.
- [ ] **Description**: A concise overview explains the epic's purpose and the value it delivers.
- [ ] **Strategic Alignment**: Clearly articulates how the epic supports overall conversion goals and PRD(s).
- [ ] **PRD Reference**: Links to relevant, approved PRD(s) are included.

### Value Proposition
- [ ] **Primary Benefit**: The main value to the project/players is clearly stated and significant.
- [ ] **Key Outcomes**: Measurable outcomes expected from the epic's completion are defined.
- [ ] **Solves a Problem**: Addresses a clear user/stakeholder need or conversion challenge.

## Scope Definition

### Boundaries
- [ ] **In Scope**: Major features/functionalities are explicitly listed and are substantial enough for an epic.
- [ ] **Out of Scope**: Exclusions are clearly listed, preventing ambiguity.
- [ ] **Epic-Level Scope**: Scope is appropriately high-level, not delving into story-level details.
- [ ] **Manageable Size**: Epic is large enough to be significant but not so vast it becomes unmanageable or loses focus.

### Technical Grounding (Input from Larry & Mo)
- [ ] **WCS Component Alignment**: "In Scope" items align with identifiable WCS systems/modules (Larry's input).
- [ ] **Godot Feasibility**: High-level technical feasibility in Godot has been considered (Mo's input).
- [ ] **Logical Grouping**: Features/functionalities grouped within the epic are logically related.

## Requirements & Criteria

### High-Level Requirements
- [ ] **User Outcomes**: High-level requirements are framed as user outcomes or major capabilities.
- [ ] **Sufficient Detail**: Provides enough detail to guide architecture without being overly prescriptive.
- [ ] **Traceability**: High-level requirements can be traced back to PRD objectives.

### High-Level Acceptance Criteria
- [ ] **Overall Success Indicators**: Criteria define what success looks like for the *entire epic*.
- [ ] **Measurable/Observable**: Criteria are broad but still observable or measurable at an epic scale.
- [ ] **Covers Key Aspects**: Criteria address functionality, integration, performance (high-level), and value delivery.

## Dependencies & Risks

### Dependencies
- [ ] **Preceding/Succeeding Epics**: Major dependencies on other epics are identified.
- [ ] **External Dependencies**: Key external factors (tools, other projects) are noted.
- [ ] **Impact Understood**: The impact of these dependencies is considered.

### Risks
- [ ] **High-Level Risks Identified**: Major potential risks (technical, scope, resource) are listed.
- [ ] **Initial Mitigation Ideas**: Brief, high-level mitigation thoughts are included.
- [ ] **Realism**: Risks identified are realistic for an undertaking of this epic's scale.

## Stakeholder & Collaboration

### Stakeholder Identification
- [ ] **Key Stakeholders Listed**: Product Owner, Technical Leads, and other relevant stakeholders are identified.
- [ ] **User Input Considered**: Evidence that user/stakeholder input (from `define-epics-list` or other interactions) has been incorporated.

### Collaboration
- [ ] **Technical Input**: Evidence of input from WCS Analyst (Larry) and Godot Architect (Mo) in scoping.
- [ ] **User/Stakeholder Feedback**: Epic definition reflects user/stakeholder discussions and priorities.

## Documentation & Workflow

### Template Compliance
- [ ] **Template Used**: Epic definition follows the structure of `bmad-workflow/templates/wcs-epic-template.md`.
- [ ] **All Sections Addressed**: All relevant sections of the template are completed appropriately for the epic's current state.

### Status & Next Steps
- [ ] **Current Status**: Epic status (e.g., "To Do", "Defined") is correctly set.
- [ ] **Next Steps Clear**: Implied or stated next steps align with BMAD workflow (e.g., if "Defined", next is prioritization for "In Progress" & Architecture).

## Final Validation

### Overall Quality
- [ ] **Clarity**: The epic is easy to understand for all stakeholders.
- [ ] **Completeness**: Contains sufficient information for high-level planning and to initiate architecture.
- [ ] **Consistency**: Consistent with PRDs and overall project direction.
- [ ] **Actionability**: Provides a clear basis for the next steps in the BMAD workflow (e.g., architectural design, story breakdown).

## Checklist Completion

**Reviewer (Curly)**: _________________ **Date**: _________________
**Technical Input (Larry)**: [ ] Confirmed / [ ] N/A
**Technical Input (Mo)**: [ ] Confirmed / [ ] N/A

**Epic ID**: _________________ **Epic Name**: _________________

**Review Result**:
- [ ] **APPROVED / DEFINED**: Epic meets quality standards and is ready for prioritization / architectural design.
- [ ] **NEEDS REVISION**: Specific issues identified that must be addressed before approval.
- [ ] **REJECTED / ON HOLD**: Fundamental problems or strategic misalignment; requires significant rework or reconsideration.

**Critical Issues** (if any):
_List any critical issues that must be addressed before approval_

**Recommendations**:
_Document any recommendations for improvement or clarification_

---
**Critical Reminder**: Well-defined Epics are crucial for breaking down large conversion efforts into manageable, value-driven segments. This checklist ensures Epics provide a solid strategic foundation.
