# User Story: SEXP System Integration with EPIC-004

**Epic**: EPIC-005 - GFRED2 Mission Editor  
**Story ID**: GFRED2-002  
**Created**: January 30, 2025  
**Status**: 🛑 REQUIRES REWORK
**Updated**: June 7, 2025
**Review Date**: June 7, 2025

### Code Review Summary (June 7, 2025)
**Reviewer**: Cline (QA Specialist)
**Assessment**: 🛑 **REQUIRES MAJOR REWORK**

**Critical Findings**:
1.  **Architectural Violation**: The implementation in `addons/gfred2/sexp_editor/` is a custom, hardcoded placeholder. It **does not** integrate with the core SEXP system from EPIC-004 as required.
2.  **Non-Functional**: The `_create_operator_node` function in `sexp_graph.gd` is static and does not use the `SexpFunctionRegistry`. The `compute_output` method in `sexp_operator_node.gd` is a stub that returns `null`.
3.  **Blocked Functionality**: Due to these issues, no SEXP evaluation, validation, or debugging can occur. All acceptance criteria that depend on a functional SEXP engine are not met.

**Action**: The entire SEXP editor implementation within GFRED2 must be discarded and rebuilt from scratch to correctly integrate with the EPIC-004 SEXP system as per the architecture document.

## Story Definition
**As a**: Mission designer creating complex mission logic  
**I want**: GFRED2 to use the comprehensive EPIC-004 SEXP system for visual scripting  
**So that**: I can create complex mission events with full validation, debugging, and all available functions

## Acceptance Criteria
- [ ] **AC1**: GFRED2 SEXP editor uses `addons/sexp/` system instead of custom implementation
- [ ] **AC2**: Visual SEXP editing provides access to all EPIC-004 functions and operators, populated from the `SexpFunctionRegistry`.
- [ ] **AC3**: SEXP validation and debugging tools are available in mission editor
- [ ] **AC4**: Mission events, goals, and triggers use standardized SEXP expressions
- [ ] **AC5**: Property editors for SEXP fields use core SEXP input controls
- [ ] **AC6**: SEXP expressions can be saved/loaded with mission files correctly
- [ ] **AC7**: SEXP debug features (breakpoints, variable watching) work in mission editor context
- [ ] **AC8**: Migration path preserves existing custom SEXP nodes and expressions
- [ ] **AC9**: AI-powered fix suggestions from EPIC-004 integrated into editor UI
- [ ] **AC10**: Performance maintained for complex SEXP trees (>60 FPS with 100+ nodes)
- [ ] **AC11**: Tests validate integration with complete SEXP system including debug features
- [ ] **AC12**: Variable management UI integrated for creating and monitoring SEXP variables
- [ ] **AC13**: SEXP tools palette with function browser and quick insertion capabilities

## Technical Requirements
**Architecture Reference**: .ai/docs/epic-005-gfred2-mission-editor/architecture.md Section 3 (Scene-Based UI Architecture) **ENHANCED 2025-05-30**

- **Remove**: Basic SEXP implementation from `gfred2/sexp_editor/`
- **Replace**: SEXP graph editor with integration to `addons/sexp/`
- **Migration**: Preserve existing SEXP editor UI while upgrading backend functionality
- **Debug Integration**: Integrate `SexpValidator`, `SexpDebugEvaluator` from EPIC-004 debug framework
- **Performance**: Maintain SEXP editor responsiveness with large expression trees (< 16ms scene instantiation, 60+ FPS UI updates)
- **UI Enhancement**: Add debug panels, variable watch, and AI-powered suggestions using scene-based architecture
- **Variable Management**: Integrate variable creation and monitoring UI from `addons/gfred2/scenes/dialogs/sexp_editor/` (FOUNDATION COMPLETE via GFRED2-011)
- **SEXP Tools**: Add function browser, quick insertion using centralized scene structure from `addons/gfred2/scenes/components/sexp_palette/` (ARCHITECTURE ESTABLISHED)
- **Scene-Based Implementation**: Leverage established scene architecture patterns from UI refactoring

## Implementation Notes
- **Major Integration**: This connects GFRED2 with the complete SEXP system
- **Enhanced Features**: Gains access to debugging, validation, and full function library
- **UI Integration**: SEXP editor becomes more sophisticated with debug capabilities
- **Performance**: Leverage SEXP system's performance optimizations
- **Implementation Gap (June 7, 2025)**: Analysis revealed that `SexpGraph.gd` hardcodes operator creation and does not use the `SexpFunctionRegistry`. Furthermore, `SexpOperatorNode.gd` has a stub `compute_output` method, meaning no actual SEXP logic is evaluated. This story is updated to include these critical implementation tasks.

## Dependencies
- **Prerequisites**: EPIC-004 SEXP Expression System (completed) ✅  
- **Foundation Dependencies**: GFRED2-011 (UI Refactoring) - **COMPLETED** ✅  
- **Blockers**: None - All foundation systems complete with scene-based architecture  
- **Related Stories**: Enables advanced mission scripting workflows  
- **Implementation Ready**: Scene-based UI foundation established for SEXP editor

## Definition of Done
- [ ] Custom SEXP parser (`sexp_editor/sexp_graph.gd`) migrated to core system
- [ ] All SEXP operations use core `SexpManager` and evaluation system
- [ ] Visual SEXP editor works with core SEXP tree structures and validation
- [ ] Real-time validation integrated with AI-powered fix suggestions
- [ ] Debug tools (breakpoints, variable watch) accessible from mission editor
- [ ] Migration preserves all existing SEXP expressions and custom nodes
- [ ] Performance benchmarks maintained (>60 FPS with 100+ SEXP nodes)
- [ ] UI integration seamless with existing mission editor workflow
- [ ] Mission save/load preserves SEXP expressions correctly
- [ ] All SEXP editing workflows tested with complex mission scenarios

## Estimation
- **Complexity**: High
- **Effort**: 5 days
- **Risk Level**: Medium
- **Confidence**: High

## Implementation Tasks
- [ ] **Task 1**: Refactor `SexpGraph._create_operator_node` and context menu to be data-driven, dynamically creating nodes based on entries in the `SexpFunctionRegistry` from EPIC-004.
- [ ] **Task 2**: Implement the `SexpOperatorNode.compute_output` method. This method should delegate the actual computation to the appropriate function in the EPIC-004 SEXP evaluation engine.
- [ ] **Task 3**: Ensure `SexpGraph.generate_sexp_code` correctly serializes the graph into a valid SEXP string that can be interpreted by the EPIC-004 `SexpManager`.
- [ ] **Task 4**: Integrate `SexpValidator` from EPIC-004 to provide real-time validation feedback on the graph.
- [ ] **Task 5**: Integrate debug framework (SexpDebugEvaluator) into editor.
- [ ] **Task 6**: Add debug panels for breakpoints, variable watching, and expression testing.
- [ ] **Task 7**: Performance optimization for large SEXP trees using core caching.
- [ ] **Task 8**: UI testing for seamless integration with mission editor workflow.

## Testing Strategy
- **Unit Tests**: Test SEXP editor integration with core system
- **Integration Tests**: Test mission events with SEXP expressions
- **User Experience Tests**: Validate SEXP editing workflow with debug features
- **Performance Tests**: Ensure SEXP evaluation performance in mission context

## Notes and Comments
**FEATURE ENHANCEMENT**: This story significantly upgrades GFRED2's scripting capabilities by integrating with the complete SEXP system that includes debugging, validation, and comprehensive function libraries.

The SEXP system provides advanced features like:
- AI-powered fix suggestions
- Step-through debugging
- Variable watching
- Expression tree visualization
- Performance optimization

Focus on seamless integration while gaining access to all these advanced features.

---

## Approval Checklist
- [x] Story follows template structure completely
- [x] All acceptance criteria are specific and testable
- [x] Technical requirements reference existing architecture
- [x] Dependencies are identified and documented
- [x] Story size is appropriate (3-4 days maximum)
- [x] Definition of Done is complete and realistic
- [x] Implementation approach is well-defined
- [x] Integration points are clearly specified

**Approved by**: SallySM (Story Manager) **Date**: January 30, 2025  
**Role**: Story Manager

---

## Status Update (May 31, 2025)

### Implementation Readiness Assessment
**Updated by**: SallySM (Story Manager)  
**Assessment Date**: May 31, 2025  
**Current Status**: ✅ **READY FOR IMMEDIATE IMPLEMENTATION**

### Foundation Dependencies Satisfied
1. **✅ GFRED2-011 (UI Refactoring) - COMPLETED**: Scene-based architecture foundation established
2. **✅ EPIC-004 (SEXP System) - COMPLETED**: Advanced SEXP system with debugging capabilities ready
3. **✅ All Technical Prerequisites Met**: Scene structure, SEXP integration patterns, UI components ready

### Key Implementation Benefits
- **Advanced SEXP Features Available**: Access to debugging, validation, AI-powered suggestions from EPIC-004
- **Clean Architecture Foundation**: GFRED2-011 provides scene-based UI patterns for SEXP editor implementation
- **Professional Debugging Tools**: Variable watch, breakpoints, step-through debugging capabilities
- **Performance Optimized**: Scene-based SEXP editor will leverage established performance patterns

### Enhanced Capabilities Ready
- **Variable Management UI**: Scene-based variable creation and monitoring components
- **SEXP Tools Palette**: Function browser and quick insertion using established UI patterns
- **Debug Integration**: Advanced debugging features integrated into mission editor workflow
- **Real-time Validation**: AI-powered fix suggestions and comprehensive validation

### Next Steps
1. **Immediate Implementation Possible**: All blocking dependencies resolved
2. **Architecture Compliance**: Follow established scene-based patterns from GFRED2-011
3. **Advanced Features**: Implement enhanced SEXP capabilities using EPIC-004 integration
4. **Professional Workflow**: Deliver IDE-level SEXP debugging within mission editor

**RECOMMENDATION**: ✅ **APPROVED FOR IMMEDIATE IMPLEMENTATION** - All prerequisites satisfied, enhanced SEXP capabilities ready
