# User Story: Implement Mission Object Duplication

**Epic**: EPIC-005 - GFRED2 Mission Editor  
**Story ID**: GFRED2-012  
**Created**: June 7, 2025  
**Status**: Ready  
**Priority**: Critical

## Story Definition
**As a**: Mission designer  
**I want**: To duplicate objects within the editor  
**So that**: I can efficiently create copies of ships, wings, and other mission elements.

## Acceptance Criteria
- [ ] **AC1**: A `duplicate_data(deep: bool = true) -> MissionObject` method is implemented on the `MissionObject` class.
- [ ] **AC2**: The `ObjectFactory`'s `duplicate_object` method successfully uses this new method to create a copy of a `MissionObject`.
- [ ] **AC3**: The duplicated object is a deep copy, meaning all its nested data (like properties, SEXP variables, etc.) are also copied and not just referenced.
- [ ] **AC4**: The duplicated object is assigned a new, unique ID by the `MissionObjectManager`.
- [ ] **AC5**: The duplication process is integrated with the editor's Undo/Redo manager.

## Technical Requirements
- **Architecture Reference**: bmad-artifacts/docs/epic-005-gfred2-mission-editor/architecture.md
- **Implementation File**: `target/addons/gfred2/mission/mission_object.gd`
- **Integration Point**: `target/addons/gfred2/object_management/object_factory.gd`
- **Method Signature**: `func duplicate_data(deep: bool = true) -> MissionObject:`
- **Deep Copy**: The implementation must perform a deep copy of the object's data. Godot's `duplicate(true)` method on resources should be leveraged.

## Implementation Notes
- **Critical Fix**: This addresses a P0 (Critical) issue identified during code analysis where a call to a non-existent method was causing object duplication to fail.
- **Core Functionality**: Duplication is a fundamental feature for any editor.

## Dependencies
- **Prerequisites**: `MissionObject` and `ObjectFactory` classes must be defined.
- **Blockers**: None.
- **Related Stories**: This enables features in any story that involves creating or managing objects.

## Definition of Done
- [ ] The `duplicate_data` method is implemented in `mission_object.gd`.
- [ ] The `ObjectFactory` is updated to correctly call this method.
- [ ] Unit tests are created to verify that deep copies are created correctly.
- [ ] The "Duplicate" action in the GFRED2 editor UI works as expected.

## Estimation
- **Complexity**: Low
- **Effort**: 1 day
- **Risk Level**: Low
- **Confidence**: High

## Implementation Tasks
- [ ] **Task 1**: Add the `duplicate_data(deep: bool = true) -> MissionObject` function to `mission_object.gd`.
- [ ] **Task 2**: Implement the deep copy logic within the new function, using `self.duplicate(true)`.
- [ ] **Task 3**: Modify `object_factory.gd` to call `source_object.duplicate_data()` in its `duplicate_object` method.
- [ ] **Task 4**: Ensure the duplicated object is registered with the `MissionObjectManager` to receive a new unique ID.
- [ ] **Task 5**: Add a unit test to `tests/unit/mission/test_mission_object.gd` to verify the duplication logic.

## Testing Strategy
- **Unit Tests**: Verify that `duplicate_data` creates a true deep copy and not a reference.
- **Integration Tests**: Test the full duplication workflow from the editor UI, including undo/redo.

## Notes and Comments
This story addresses a critical bug preventing a core editor feature from working.

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
