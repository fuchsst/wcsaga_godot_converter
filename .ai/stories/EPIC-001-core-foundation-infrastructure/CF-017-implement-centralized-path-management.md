# User Story: Implement Centralized Path Management System

**Epic**: EPIC-001 - Core Foundation & Infrastructure
**Story ID**: CF-017
**Created**: June 7, 2025
**Status**: Ready
**Priority**: High

## Story Definition
**As a**: Developer
**I want**: A centralized path management singleton (`Paths.gd`) to resolve all file and directory paths within the project
**So that**: Hardcoded `res://` strings are eliminated, making the codebase more resilient to future changes in the project's directory structure and reducing maintenance overhead.

## Acceptance Criteria
- [ ] **AC1**: A new autoload singleton named `Paths` is created at `target/autoload/paths.gd`.
- [ ] **AC2**: The `Paths` singleton provides methods for resolving paths to key project directories (e.g., `get_missions_dir()`, `get_assets_dir()`, `get_ships_dir()`).
- [ ] **AC3**: The `Paths` singleton provides methods for constructing full paths to specific assets (e.g., `get_ship_model_path(ship_class_name)`).
- [ ] **AC4**: At least 10 major instances of hardcoded paths in the existing codebase (e.g., in `gfred2` or `wcs_asset_core`) are refactored to use the new `Paths` singleton.
- [ ] **AC5**: The system remains fully functional after the refactoring, with all tests passing.

## Technical Requirements
- **Architecture Reference**: This story supports the architectural goal of creating a maintainable and robust core foundation. It aligns with the principles laid out in `.ai/docs/EPIC-001-core-foundation-infrastructure/architecture.md`.
- **Implementation**: Create a new script `target/autoload/paths.gd` and register it as an autoload singleton in `project.godot`.
- **Design Principles**: The `Paths` singleton should be lightweight and consist primarily of static or const strings and simple helper functions. It should not have complex logic or dependencies on other managers.

## Implementation Notes
- **Impact**: This is a cross-cutting concern that will touch many parts of the codebase over time. This story focuses on creating the system and refactoring a few key areas to establish the pattern.
- **Future Work**: Subsequent stories in other epics should be updated to use this new `Paths` singleton.

## Dependencies
- **Prerequisites**: None. This is a foundational story.
- **Blockers**: None.
- **Related Stories**: Will be related to almost all future stories that involve file access.

## Definition of Done
- [ ] `paths.gd` is created and implemented as an autoload singleton.
- [ ] The singleton provides clear, well-documented methods for path resolution.
- [ ] At least 10 key areas of the codebase are refactored to use the `Paths` singleton.
- [ ] All existing tests pass after the refactoring.
- [ ] The new `Paths` singleton is documented in the core infrastructure's `CLAUDE.md`.

## Estimation
- **Complexity**: Medium
- **Effort**: 2-3 days
- **Risk Level**: Low
- **Confidence**: High

## Implementation Tasks
- [ ] **Task 1**: Create `target/autoload/paths.gd`.
- [ ] **Task 2**: Define and implement the core path resolution methods.
- [ ] **Task 3**: Register `Paths.gd` as an autoload singleton in `project.godot`.
- [ ] **Task 4**: Identify 10-15 high-impact areas where hardcoded paths are used.
- [ ] **Task 5**: Refactor these areas to use the new `Paths` singleton.
- [ ] **Task 6**: Run all tests to ensure no regressions were introduced.
- [ ] **Task 7**: Document the `Paths` singleton.

## Testing Strategy
- **Unit Testing**: Create a unit test for the `Paths` singleton to verify its methods return correct paths.
- **Regression Testing**: Run the full test suite to ensure the refactoring did not break existing functionality.

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
