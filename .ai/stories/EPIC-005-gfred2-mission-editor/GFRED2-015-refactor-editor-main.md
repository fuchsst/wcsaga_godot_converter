# User Story: Refactor editor_main.gd to Reduce Complexity

**Epic**: EPIC-005 - GFRED2 Mission Editor  
**Story ID**: GFRED2-015  
**Created**: June 7, 2025  
**Status**: Ready  
**Priority**: High

## Story Definition
**As a**: Developer working on the GFRED2 codebase  
**I want**: The `editor_main.gd` script to be refactored, delegating its responsibilities to more focused classes/scenes  
**So that**: The main editor script is less complex, easier to maintain, and follows SOLID principles better.

## Acceptance Criteria
- [ ] **AC1**: Responsibilities like menu handling, dialog management, viewport control, and gizmo management are extracted from `editor_main.gd` into separate, dedicated components (scripts and/or scenes).
- [ ] **AC2**: `editor_main.gd` primarily acts as an orchestrator, coordinating between these new focused components.
- [ ] **AC3**: The overall functionality of the editor remains unchanged or is improved after the refactoring.
- [ ] **AC4**: The new components follow the scene-based UI architecture where applicable (e.g., UI-related managers should be scenes).
- [ ] **AC5**: Code complexity of `editor_main.gd` (e.g., lines of code, cyclomatic complexity) is significantly reduced.

## Technical Requirements
- **Architecture Reference**: .ai/docs/epic-005-gfred2-mission-editor/architecture.md (especially regarding scene-based UI and manager responsibilities).
- **Refactoring Target**: `target/addons/gfred2/editor_main.gd` and `editor_main.tscn`.
- **New Components**: New GDScript classes and potentially new scenes will be created (e.g., `ViewportManager.gd`, `EditorDialogManager.gd`, `GizmoController.gd`). These should reside in appropriate directories (e.g., `managers/`, `ui/controllers/`, or within `scenes/` if they are UI scenes).
- **Design Principles**: Adhere to Single Responsibility Principle. Use signals for communication between components where appropriate.

## Implementation Notes
- **Architectural Improvement**: This is a key refactoring to improve the long-term maintainability and scalability of GFRED2.
- **Phased Approach**: This refactoring can be done incrementally, extracting one responsibility at a time.
- **Impact**: Will touch many parts of the editor's core logic.

## Dependencies
- **Prerequisites**: A stable base of other managers (like `MissionObjectManager`, `GFRED2ShortcutManager`) is beneficial. Completion of GFRED2-011 (Scene-based UI) is important for new UI components.
- **Blockers**: None.
- **Related Stories**: This refactoring will make implementing other stories easier by providing clearer points of integration.

## Definition of Done
- [ ] `editor_main.gd` has been significantly simplified.
- [ ] New focused classes/scenes for delegated responsibilities are created and functional.
- [ ] All editor functionality previously handled by `editor_main.gd` is now correctly managed by the new components.
- [ ] The editor is fully functional and passes all existing tests.
- [ ] The new structure is documented (e.g., in `CLAUDE.md` for `gfred2` or architecture documents).

## Estimation
- **Complexity**: High
- **Effort**: 3-5 days (depending on the extent of refactoring for each responsibility)
- **Risk Level**: Medium (risk of breaking existing functionality if not done carefully)
- **Confidence**: Medium

## Implementation Tasks
- [ ] **Task 1**: Identify distinct responsibilities currently handled by `editor_main.gd` (e.g., menu bar logic, viewport input handling, camera control, gizmo lifecycle, dialog invocation).
- [ ] **Task 2**: For each identified responsibility, design and create a new class/scene (e.g., `EditorMenuManager`, `ViewportInputController`, `EditorCameraManager`).
- [ ] **Task 3**: Incrementally move logic from `editor_main.gd` to these new components.
- [ ] **Task 4**: Update `editor_main.gd` to instantiate and coordinate these new components.
- [ ] **Task 5**: Refactor signal connections to ensure proper communication between `editor_main.tscn` and the new components.
- [ ] **Task 6**: Ensure new UI-related components adhere to the scene-based architecture (GFRED2-011).
- [ ] **Task 7**: Test each refactored piece of functionality thoroughly.

## Testing Strategy
- **Regression Testing**: Perform full regression testing of all editor features after each major piece of logic is extracted.
- **Component Testing**: Test the new focused components in isolation if possible.
- **Code Review**: Due to the complexity, peer review of the refactored structure is highly recommended.

## Notes and Comments
This refactoring addresses the "God Object" concern for `editor_main.gd`. It will make the editor's core logic more modular, testable, and easier to understand.

---

## Approval Checklist
- [x] Story follows template structure completely
- [x] All acceptance criteria are specific and testable
- [x] Technical requirements are clear.
- [x] Dependencies are identified and documented
- [x] Story size is appropriate
- [x] Definition of Done is complete and realistic

**Approved by**: SallySM (Story Manager) **Date**: June 7, 2025  
**Role**: Story Manager
