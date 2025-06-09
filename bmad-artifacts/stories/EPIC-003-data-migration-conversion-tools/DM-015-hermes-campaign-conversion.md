# User Story: Convert Hermes Campaign Assets via Automated Mapping

**Epic**: [EPIC-003: Data Migration & Conversion Tools](bmad-artifacts/epics/EPIC-003-data-migration-conversion-tools.md)  
**Story ID**: DM-015  
**Created**: 2025-06-09  
**Status**: Draft

## Story Definition
**As a**: Conversion Manager,  
**I want to**: execute the full, automated conversion pipeline for the WCS Hermes campaign assets,  
**So that**: all necessary models, textures, and data for the campaign are correctly converted and integrated into the Godot project.

## Acceptance Criteria
- [ ] **AC1**: The `AssetMapper` (from DM-013) is successfully run on the `source_assets/wcs_hermes_campaign` directory and its associated table files.
- [ ] **AC2**: The generated `hermes_campaign_mapping.json` is used as the input for a full conversion run.
- [ ] **AC3**: The conversion process, including duplicate detection (from DM-014), completes with a success rate of over 98% for all assets in the mapping.
- [ ] **AC4**: A final validation report is generated, confirming the integrity of all converted assets and detailing any duplicates found.

## Technical Requirements
- **Architecture Reference**: This story utilizes the entire conversion pipeline as defined in `bmad-artifacts/docs/EPIC-003-data-migration-conversion-tools/architecture.md`, orchestrated by `migration_manager.py`.
- **Godot Components**: The final converted assets will be organized in the `target/assets/campaigns/hermes` directory, following the semantic structure from the mapping.
- **Integration Points**: This story is the practical application and integration test for stories `DM-013` and `DM-014`.

## Implementation Notes
- **WCS Reference**: `source_assets/wcs_hermes_campaign` directory and all relevant `.tbl` files.
- **Godot Approach**: This involves running the main Python conversion script (`migration_manager.py`) with the correct arguments to trigger the automated mapping, conversion, and validation for the Hermes campaign.
- **Key Challenges**: Handling any unforeseen edge cases or asset types specific to the Hermes campaign that were not accounted for in the mapping logic.
- **Success Metrics**: A functional Godot project containing all necessary Hermes campaign assets, correctly imported, organized, and validated.

## Dependencies
- **Prerequisites**: `DM-013: Automated Asset Mapping from Table Data`, `DM-014: Duplicate Asset Detection and Handling`.
- **Blockers**: None.
- **Related Stories**: This story serves as the capstone for the Hermes campaign conversion effort within this epic.

## Definition of Done
- [ ] All acceptance criteria are met.
- [ ] The Hermes campaign assets are successfully converted and can be loaded in the Godot editor without errors.
- [ ] The final conversion log and validation report are archived as artifacts for review.
- [ ] The process is documented as a guide for converting other campaigns.
- [ ] The results are reviewed and approved by the project stakeholders.

## Estimation
- **Complexity**: Medium
- **Effort**: 2 days
- **Risk Level**: Medium
- **Confidence**: High
