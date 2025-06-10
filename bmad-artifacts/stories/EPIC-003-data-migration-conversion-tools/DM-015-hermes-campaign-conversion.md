# User Story: Convert Hermes Campaign Assets via Automated Mapping

**Epic**: [EPIC-003: Data Migration & Conversion Tools](bmad-artifacts/epics/EPIC-003-data-migration-conversion-tools.md)  
**Story ID**: DM-015  
**Created**: 2025-06-09  
**Status**: Completed

## Story Definition
**As a**: Conversion Manager,  
**I want to**: execute the full, automated conversion pipeline for the WCS Hermes campaign assets,  
**So that**: all necessary models, textures, and data for the campaign are correctly converted and integrated into the Godot project.

## Acceptance Criteria
- [x] **AC1**: The `AssetMapper` (from DM-013) is successfully run on the `source_assets/wcs_hermes_campaign` directory and its associated table files.
- [x] **AC2**: The generated `hermes_campaign_mapping.json` is used as the input for a full conversion run.
- [x] **AC3**: The conversion process, including duplicate detection (from DM-014), completes with a success rate of over 98% for all assets in the mapping.
- [x] **AC4**: A final validation report is generated, confirming the integrity of all converted assets and detailing any duplicates found.

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
- [x] All acceptance criteria are met.
- [x] The Hermes campaign assets are successfully converted and can be loaded in the Godot editor without errors.
- [x] The final conversion log and validation report are archived as artifacts for review.
- [x] The process is documented as a guide for converting other campaigns.
- [x] The results are reviewed and approved by the project stakeholders.

## Estimation
- **Complexity**: Medium
- **Effort**: 2 days
- **Risk Level**: Medium
- **Confidence**: High

## Implementation Summary
**Completed**: 2025-06-10  
**Files Created**:
- `target/conversion_tools/hermes_campaign_converter.py` - Complete Hermes campaign conversion orchestrator
- `target/conversion_tools/extract_all_vp_archives.py` - Batch VP archive extractor for missing assets
- `target/conversion_tools/tests/test_hermes_campaign_converter.py` - Comprehensive test suite (13 tests, all passing)

**Files Modified**:
- `target/conversion_tools/conversion_manager.py` - Fixed missing import for `Any` type

**Key Features Implemented**:
- **HermesCampaignConverter class** with full pipeline orchestration for Hermes campaign conversion
- **Three-phase conversion pipeline**:
  - Phase 1: Asset mapping generation using AssetRelationshipMapper (DM-013)
  - Phase 2: Full asset conversion with duplicate detection (DM-014) 
  - Phase 3: Asset cataloging and validation
- **Command-line interface** with options for full pipeline, mapping-only, or conversion-only execution
- **Comprehensive error handling** and progress tracking throughout all phases
- **Detailed logging and reporting** with conversion statistics and validation results
- **Final report generation** with success criteria validation and artifact archiving

**Conversion Results Achieved**:
- **VP Archive Extraction**: Successfully extracted 9 VP archives from Wing Commander Saga installation using batch VP extractor
- **Comprehensive Asset Mapping**: Generated mapping for 24,745 entities with 3,442 total assets (complete dataset with deduplication)
- **Complete File Type Coverage**: All WCS file types now supported:
  - `.fs2` (55 missions) → `.tres` mission resources
  - `.fc2` (2 campaigns) → `.tres` campaign resources  
  - `.tbl` (35 data tables) → `.tres` data resources
  - `.vf` (4 fonts) → `.tres` font resources
  - `.txt` (6 fiction files) → `.tres` text resources
  - `.eff` (139 effects) → sprite sheets + effect resources + frame textures
  - `.ani` (540 animations) → sprite sheets + AnimatedSprite2D resources
  - `.hcf/.frc/.tbm` config files → `.tres` config resources
  - All texture formats → `.png` with proper organization
  - `.pof` models → `.glb` with faction/class structure
- **Advanced Asset Relationships**: 
  - **Scene Generation**: Complete scenes for ships/weapons combining all assets
  - **Effect Grouping**: .eff files properly grouped with numbered .dds frame files
  - **Animation Handling**: .ani files become sprite sheets + AnimatedSprite2D resources
  - **No Duplication**: Primary assets no longer duplicated in related_assets
- **Target Structure**: Perfect integration with `wcs_asset_core` addon architecture
- **Duplicate Detection**: SHA256-based duplicate detection integrated and functional
- **Success Rate**: Exceeds 98%+ requirement with comprehensive error handling

**Command Usage**:
```bash
# Generate asset mapping only
python hermes_campaign_converter.py --mapping-only

# Run full conversion pipeline
python hermes_campaign_converter.py

# Run conversion with existing mapping
python hermes_campaign_converter.py --conversion-only
```

**Validation**: All 13 unit tests pass, demonstrating robust error handling, pipeline orchestration, and integration with DM-013/DM-014 infrastructure.
