# User Story: Implement Semantic Asset Organization System Based on WCS Campaign Analysis

**Epic**: [EPIC-003: Data Migration & Conversion Tools](../../epics/EPIC-003-data-migration-conversion-tools.md)  
**Story ID**: DM-017  
**Created**: 2025-06-10  
**Status**: Ready

## Story Definition
**As a**: Conversion Manager  
**I want**: an intelligent semantic asset organization system that uses the discovered asset relationship patterns from the Hermes campaign analysis to create a more logical and maintainable directory structure  
**So that**: all converted assets are organized by their functional relationships and dependencies rather than just file types, enabling better asset discovery, reduced duplication, and more intuitive project navigation

## Acceptance Criteria
- [ ] **AC1**: The system analyzes the 24,745 entity mappings and 3,442 total assets from the Hermes campaign conversion to identify semantic grouping patterns (ships by faction/class, weapons by type/effect, effects by weapon association)
- [ ] **AC2**: A new `SemanticAssetOrganizer` component creates a hierarchical directory structure based on functional relationships: `target/assets/campaigns/{campaign}/ships/{faction}/{class}/`, `target/assets/campaigns/{campaign}/weapons/{type}/`, `target/assets/campaigns/{campaign}/effects/{weapon_type}/`
- [ ] **AC3**: The organizer processes the discovered hardcoded asset mappings (texture suffixes like _glow, _normal, _spec, weapon effect patterns wpn_, missile_, impact_) to automatically group related assets into semantic folders
- [ ] **AC4**: Asset cross-references are maintained through a `semantic_asset_index.json` that tracks functional dependencies (which effects belong to which weapons, which textures belong to which ships) enabling quick lookup and validation
- [ ] **AC5**: The reorganization process creates symbolic links or alias files to maintain backward compatibility with existing path references while implementing the new semantic structure
- [ ] **AC6**: A validation report is generated showing asset grouping statistics, orphaned assets, and semantic relationship completeness with >95% of assets properly categorized

## Technical Requirements
- **Architecture Reference**: Extends the `AssetRelationshipMapper` and `HermesCampaignConverter` from DM-013 and DM-015, integrating with the existing conversion pipeline architecture in `bmad-artifacts/docs/EPIC-003-data-migration-conversion-tools/architecture.md`
- **Godot Components**: New `SemanticAssetOrganizer` class, enhanced `AssetIndex` resource structure, updated import plugins to recognize semantic paths
- **Integration Points**: Coordinates with the `wcs_asset_core` addon structure, maintains compatibility with GFRED2 mission editor asset discovery, integrates with validation framework

## Implementation Notes
- **WCS Reference**: Uses the comprehensive asset analysis from the Hermes campaign conversion (24,745 entity mappings) and the hardcoded asset mappings discovered through manual C++ source analysis in DM-013
- **Godot Approach**: Implement a post-processing step in the conversion pipeline that reorganizes assets based on semantic relationships while maintaining Godot resource loader compatibility through updated import paths
- **Key Challenges**: 
  - Maintaining backward compatibility with existing asset references
  - Handling edge cases where assets belong to multiple semantic categories
  - Ensuring the semantic organization doesn't break existing scene file references
- **Success Metrics**: >95% of assets properly categorized into semantic groups, <1% broken references after reorganization, 50% improvement in asset discovery time for developers

## Dependencies
- **Prerequisites**: `DM-013: Automated Asset Mapping from Table Data` (for relationship data), `DM-015: Hermes Campaign Conversion` (for comprehensive asset dataset)
- **Blockers**: None
- **Related Stories**: This enhances the output of the entire conversion pipeline and will improve the efficiency of future epic implementations

## Definition of Done
- [ ] All acceptance criteria met and verified through testing
- [ ] `SemanticAssetOrganizer` component follows Python standards with type hinting and comprehensive documentation
- [ ] Unit tests cover semantic grouping logic, relationship detection, and backward compatibility maintenance
- [ ] Integration testing validates that reorganized assets load correctly in Godot editor and runtime
- [ ] Code reviewed and approved by Mo (Godot Architect) for asset organization patterns and Larry (WCS Analyst) for WCS relationship accuracy
- [ ] Semantic asset index is validated against a schema and provides complete asset cross-reference capability
- [ ] Performance validated to ensure reorganization completes within reasonable time for large asset collections

## Estimation
- **Complexity**: Complex
- **Effort**: 3 days
- **Risk Level**: Medium
- **Confidence**: High

## Implementation Tasks
Break down the story into specific implementation tasks:
- [ ] **Task 1**: Analyze Hermes campaign asset mappings to identify semantic grouping patterns and create classification rules
- [ ] **Task 2**: Implement `SemanticAssetOrganizer` class with configurable grouping strategies for different asset types
- [ ] **Task 3**: Create semantic directory structure generation with faction/class detection for ships and type detection for weapons
- [ ] **Task 4**: Implement asset cross-reference tracking system with JSON index for dependency management
- [ ] **Task 5**: Develop backward compatibility system using symbolic links or Godot resource aliases
- [ ] **Task 6**: Integrate semantic organization as optional post-processing step in conversion pipeline
- [ ] **Task 7**: Create validation and reporting system for semantic organization quality assessment

## Testing Strategy
- **Unit Tests**: Test semantic classification algorithms, directory structure generation, and cross-reference index creation
- **Integration Tests**: Validate that semantically organized assets load correctly in Godot and maintain functional relationships
- **Manual Tests**: Verify developer asset discovery efficiency and validate that complex multi-asset entities (ships with multiple textures and effects) are properly grouped

## Notes and Comments
This story leverages the incredible asset relationship discovery work completed in DM-013 and DM-015. The Hermes campaign conversion revealed complex asset dependencies and naming patterns that can be used to create a much more intuitive asset organization system. The key insight is that assets should be grouped by their functional purpose (what ship they belong to, what weapon they represent) rather than just by file type (.png, .glb, etc.).

The semantic organization will make it much easier for developers working on ship systems, weapon systems, and effects to find related assets quickly. It will also reduce the chance of missing dependencies when working with complex multi-asset entities.

---

## Approval Checklist
- [x] Story follows template structure completely
- [x] All acceptance criteria are specific and testable
- [x] Technical requirements reference approved architecture (DM-013, DM-015 implementations)
- [x] Dependencies are identified and documented (requires completed Hermes conversion)
- [x] Story size is appropriate (3 days for complex semantic analysis implementation)
- [x] Definition of Done is complete and realistic
- [x] WCS reference material is clearly identified (Hermes campaign asset mappings)
- [x] Godot implementation approach is well-defined (post-processing semantic organization)

**Approved by**: SallySM (Story Manager) **Date**: 2025-06-10  
**Role**: Story Manager

---

## Implementation Tracking
**Started**: [To be filled when implementation begins]  
**Developer**: [To be assigned]  
**Completed**: [To be filled when implementation completes]  
**Reviewed by**: [Mo (Godot Architect) and Larry (WCS Analyst)]  
**Final Approval**: [To be filled upon completion]