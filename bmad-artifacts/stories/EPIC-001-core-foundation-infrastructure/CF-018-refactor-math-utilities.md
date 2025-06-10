# Story ID: CF-016 - Refactor Custom Math Utilities to Use Godot Native Functions

- **Epic**: [EPIC-001: Core Foundation & Infrastructure](../../../epics/EPIC-001-core-foundation-infrastructure.md)
- **Story Owner**: Mo (Godot Architect)
- **Developer**: Dev
- **QA**: QA
- **Story Point Estimate**: 3
- **Priority**: Medium
- **Status**: Ready for Implementation
- **Created**: 2025-06-10
- **Updated**: 2025-06-10

## User Story

As a developer, I want to replace custom mathematical wrapper functions with direct calls to Godot's native math APIs so that the codebase is simplified, performance is improved, and maintenance overhead is reduced.

## Description

The current implementation includes custom math utility scripts like `wcs_vector_math.gd`. While potentially useful during initial porting, these wrappers add an unnecessary layer of abstraction over Godot's highly optimized, C++-based math libraries (`Vector3`, `Basis`, etc.).

This story involves auditing these utility files, identifying functions that are redundant, and replacing their usage throughout the codebase with direct calls to the equivalent native Godot functions. This aligns with the core architectural principle of "Godot-Native First" and reduces technical debt.

## Acceptance Criteria

1.  **Audit Complete**: `scripts/core/foundation/wcs_vector_math.gd` and any other custom math files have been fully audited.
2.  **Redundant Wrappers Removed**: All functions that have a direct 1-to-1 equivalent in Godot's native API (`Vector3`, `Basis`, `Transform3D`, `@GDScript` functions) are removed.
3.  **Codebase Refactored**: All call sites that used the removed wrapper functions are updated to use the direct Godot API calls.
4.  **Special Cases Consolidated**: Any remaining functions that implement a unique WCS algorithm (not present in Godot) are consolidated into a single `WCSMathUtils.gd` helper class.
5.  **Clear Documentation**: Each remaining custom function in `WCSMathUtils.gd` is documented with a comment explaining why it is a special case that cannot be replaced by a native function.
6.  **Tests Pass**: All existing unit and integration tests related to physics, movement, and mathematics must pass after the refactor.
7.  **Gameplay Parity**: There is no observable change in ship movement, physics, or any other math-dependent game behavior. Gameplay feel must be identical to the pre-refactor state.

## Technical Implementation Notes

-   **Target Files for Audit**:
    -   `scripts/core/foundation/wcs_vector_math.gd`
    -   `scripts/core/foundation/wcs_physics.gd`
    -   `scripts/core/foundation/wcs_splines.gd`
-   **Common Replacements**:
    -   Custom `vec_add()` -> `Vector3.operator+()`
    -   Custom `vec_normalize()` -> `Vector3.normalized()`
    -   Custom `vec_dot()` -> `Vector3.dot()`
    -   Custom `vec_cross()` -> `Vector3.cross()`
-   A global search for function names will be required to find all call sites.
-   Pay close attention to physics calculations in `scripts/ships/` and `scripts/ai/` as they are the most sensitive to mathematical changes.

## Dependencies

-   None. This is a self-contained refactoring task.

## Risks

-   **Behavioral Changes**: A subtle difference between the custom implementation and Godot's native function could lead to minor but noticeable changes in gameplay feel.
    -   **Mitigation**: Extensive playtesting and side-by-side comparison with a pre-refactor build. Automated tests for key physics calculations are essential.
- Make sure to maintain custom logic (e.g. curves, and lookups) that define the original gameplay feeling.

## Quality Assurance Checklist

-   [ ] **Code Review**: All changes reviewed by Mo to ensure correctness and adherence to Godot best practices.
-   [ ] **Automated Tests**: All relevant unit tests pass.
-   [ ] **Gameplay Validation**: QA confirms that ship flight, AI movement, and weapon targeting feel identical to the previous version.
-   [ ] **Performance Check**: No performance regressions are introduced. A minor performance *improvement* is expected.
-   [ ] **Documentation**: All remaining custom functions are clearly documented as per acceptance criteria.
