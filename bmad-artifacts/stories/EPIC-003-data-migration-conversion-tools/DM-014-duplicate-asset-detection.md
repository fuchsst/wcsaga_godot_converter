# User Story: Duplicate Asset Detection and Handling

**Epic**: [EPIC-003: Data Migration & Conversion Tools](bmad-artifacts/epics/EPIC-003-data-migration-conversion-tools.md)  
**Story ID**: DM-014  
**Created**: 2025-06-09  
**Status**: Draft

## Story Definition
**As a**: Game Developer,  
**I want**: the conversion tool to detect and handle duplicate assets (files with identical content) during the conversion process,  
**So that**: we can reduce the final game's size, minimize redundant data, and improve loading times.

## Acceptance Criteria
- [ ] **AC1**: The `ConversionManager` calculates a SHA256 hash for each source file's content before adding it to a conversion job.
- [ ] **AC2**: A manifest of file hashes and their corresponding converted target paths is maintained throughout the conversion process.
- [ ] **AC3**: If a file with an identical hash is encountered, the conversion for that file is skipped, and the existing converted asset is used instead.
- [ ] **AC4**: The conversion log clearly reports any detected duplicate files and indicates that they were skipped, referencing the original asset (e.g., "SKIPPED: Duplicate of 'assets/textures/shared/icon.png'").

## Technical Requirements
- **Architecture Reference**: This functionality will be integrated into the `ConversionManager.execute_conversion_plan` method in `bmad-artifacts/docs/EPIC-003-data-migration-conversion-tools/architecture.md`.
- **Godot Components**: N/A. This is a pure Python implementation within the conversion tool.
- **Integration Points**: Hooks into the main job execution loop of the `ConversionManager`.

## Implementation Notes
- **WCS Reference**: N/A
- **Godot Approach**: Use Python's `hashlib` library for efficient SHA256 calculation. The hash manifest can be a simple Python dictionary for fast lookups during the conversion run.
- **Key Challenges**: Ensuring the hashing process is performant and does not become a bottleneck for large numbers of assets.
- **Success Metrics**: A measurable reduction in the total size of converted assets for the Hermes campaign (target >5%).

## Dependencies
- **Prerequisites**: None.
- **Blockers**: None.
- **Related Stories**: This can be implemented in parallel with `DM-013`.

## Definition of Done
- [ ] All acceptance criteria are met and verified.
- [ ] The implementation follows Python best practices.
- [ ] Unit tests are created for the hashing and duplicate detection logic, achieving >90% coverage.
- [ ] The performance impact of the hashing mechanism is measured and confirmed to be within acceptable limits (e.g., less than a 10% increase in total conversion time).
- [ ] Code is reviewed and approved by the development team.

## Estimation
- **Complexity**: Medium
- **Effort**: 2 days
- **Risk Level**: Low
- **Confidence**: High
