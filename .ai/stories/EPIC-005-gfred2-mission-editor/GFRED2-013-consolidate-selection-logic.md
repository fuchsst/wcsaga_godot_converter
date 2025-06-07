# User Story: Consolidate Selection Logic into MissionObjectManager

**Epic**: EPIC-005 - GFRED2 Mission Editor  
**Story ID**: GFRED2-013  
**Created**: June 7, 2025  
**Status**: Ready  
**Priority**: Critical

## Story Definition
**As a**: Developer maintaining the GFRED2 codebase  
**I want**: All object selection logic to be handled by the `MissionObjectManager`  
**So that**: The dependency on the missing `selection_manager.gd` is removed and the architecture is cleaner.

## Acceptance Criteria
- [ ] **AC1**: All references to `selection_manager` in `editor_main.gd` are removed.
- [ ] **AC2**: All selection-related functionality (single select, box select, group select, transform, delete) is now handled by `MissionObjectManager`.
- [ ] **AC3**: The line `selection_manager = preload("res://addons/gfred2/selection_manager.gd").new()` is removed from `editor_main.gd`.
- [ ] **AC4**: The editor's selection functionality works correctly after the refactor.
- [ ] **AC5**: The `MissionObjectManager` now exposes the necessary properties and methods for selection management (e.g., `selected_objects`, `get_selection_center`, `clear_selection`).

## Technical Requirements
- **Architecture Reference**: .ai/docs/epic-005-gfred2-mission-editor/architecture.md
- **Refactoring Target**: `target/addons/gfred2/editor_main.gd`
- **Consolidation Target**: `target/addons/gfred2/object_management/mission_object_manager.gd`
- **Goal**: Remove all dependencies on the non-existent `selection_manager.gd` by migrating its responsibilities to `MissionObjectManager`.

## Implementation Notes
- **Critical Fix**: This addresses a P0 (Critical) issue where the editor attempts to load a missing file, which would cause a runtime crash.
- **Architectural Improvement**: Consolidates selection logic into the most appropriate manager class, reducing redundancy and clarifying responsibilities.

## Dependencies
- **Prerequisites**: `editor_main.gd` and `mission_object_manager.gd` must exist.
- **Blockers**: None.
- **Related Stories**: This refactoring will impact any story that involves object selection or manipulation.

## Definition of Done
- [ ] All code referencing `selection_manager` in `editor_main.gd` has been successfully refactored to use `mission_object_manager`.
- [ ] The `selection_manager.gd` file is no longer referenced anywhere in the project.
- [ ] All selection-related features of the editor are fully functional.
- [ ] The code is cleaner and the responsibility for selection is clearly defined in `MissionObjectManager`.

## Estimation
- **Complexity**: Medium
- **Effort**: 2 days
- **Risk Level**: Medium (due to the number of touchpoints in `editor_main.gd`)
- **Confidence**: High

## Implementation Tasks
- [ ] **Task 1**: Add selection management properties (e.g., `selected_objects`, `box_selecting`) to `mission_object_manager.gd`.
- [ ] **Task 2**: Implement selection management methods (e.g., `clear_selection`, `get_selection_center`, `start_box_selection`, etc.) in `mission_object_manager.gd`.
- [ ] **Task 3**: Go through `editor_main.gd` method-by-method and replace every call to `selection_manager` with the equivalent call to `mission_object_manager`.
- [ ] **Task 4**: Remove the instantiation of `selection_manager` from `editor_main.gd`.
- [ ] **Task 5**: Create a test scene or instructions to manually test all selection-related functionality to ensure the refactor was successful.

## Testing Strategy
- **Manual Testing**: Thoroughly test all selection modes in the editor:
  - Single click selection.
  - Shift-click multi-selection.
  - Box selection (with and without shift).
  - Selection groups (store and recall).
  - Deleting selected objects.
  - Applying gizmo transformations to selected objects.
  - Camera controls that depend on selection.
- **Regression Testing**: Ensure no other editor functionality was broken by the change.

## Notes and Comments
This is a critical refactoring to fix a startup crash and improve the architectural integrity of the editor.

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
