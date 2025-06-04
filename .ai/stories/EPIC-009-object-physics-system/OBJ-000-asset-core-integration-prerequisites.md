# User Story: Asset Core Integration Prerequisites

## Story Definition
**As a**: WCS-Godot system architect  
**I want**: Object type definitions and constants properly placed in the wcs_asset_core addon (EPIC-002)  
**So that**: Both the main game and FRED2 editor can share common object definitions and maintain architectural consistency

## Acceptance Criteria
- [ ] **AC1**: Create `addons/wcs_asset_core/constants/object_types.gd` with complete WCS object type enumeration
- [ ] **AC2**: Create `addons/wcs_asset_core/constants/collision_layers.gd` with physics collision layer definitions
- [ ] **AC3**: Create `addons/wcs_asset_core/constants/update_frequencies.gd` with LOD and performance constants
- [ ] **AC4**: Move `PhysicsProfile` resource from `scripts/core/objects/types/` to `addons/wcs_asset_core/resources/object/`
- [ ] **AC5**: Create `addons/wcs_asset_core/structures/object_type_data.gd` for object metadata
- [ ] **AC6**: All constants follow existing wcs_asset_core addon patterns and static typing standards
- [ ] **AC7**: Integration with existing `AssetTypes` enum in wcs_asset_core addon
- [ ] **AC8**: Complete documentation following addon standards

## Technical Requirements
- **Architecture Reference**: Mo's corrected architecture.md EPIC-002 integration section
- **EPIC-002 Standards**: Must follow existing wcs_asset_core addon patterns and conventions
- **File Locations**: 
  - Constants go in `addons/wcs_asset_core/constants/`
  - Resources go in `addons/wcs_asset_core/resources/object/`
  - Structures go in `addons/wcs_asset_core/structures/`
- **Integration Points**: Existing AssetTypes, BaseAssetData, and addon loader systems
- **Validation**: All new classes must integrate with existing addon validation framework

## Implementation Notes
- **WCS Reference**: `object/object.cpp`, `object/object.h` - object type definitions and hierarchies
- **Pattern Following**: Study existing `asset_types.gd` for enumeration patterns
- **Addon Consistency**: Follow existing addon file naming and structure conventions
- **Key Challenge**: Mapping WCS object types to Godot-compatible enumeration system
- **Success Metrics**: Clean integration with existing addon, proper type definitions, FRED2 compatibility

## Dependencies
- **Prerequisites**: wcs_asset_core addon enabled and functional (EPIC-002 foundation)
- **Architecture**: Mo's corrected architecture documents must be approved
- **Integration**: Understanding of existing AssetTypes and addon structure
- **Blockers**: None - this is the foundational prerequisite for all other EPIC-009 stories

## Definition of Done
- [ ] All acceptance criteria met and verified through addon integration tests
- [ ] Code follows wcs_asset_core addon standards with full static typing and documentation
- [ ] Integration tests with existing addon systems (AssetLoader, RegistryManager)
- [ ] Object type constants accessible from both main game and FRED2 editor contexts
- [ ] CLAUDE.md documentation updated for addon object integration
- [ ] All existing wcs_asset_core tests still pass after integration
- [ ] Validation that new constants work with existing BaseAssetData structure

## Priority and Sequencing
- **Priority**: CRITICAL - Blocks ALL other EPIC-009 stories
- **Sequence**: MUST be completed before OBJ-001, OBJ-002, OBJ-003, and all other object stories
- **Risk Level**: High (foundation change affects entire object system)
- **Effort**: 1-2 days (asset reorganization and constant definition)

## BMAD Workflow Compliance
- **Epic Status**: ✅ EPIC-009 approved and architecture updated by Mo
- **Architecture Approval**: ✅ Mo has corrected architecture with EPIC-002 integration requirements
- **Story Dependency**: ✅ This story creates prerequisites for all other EPIC-009 implementation stories
- **Quality Gate**: This story must pass ALL acceptance criteria before any object implementation begins

## Related Stories
- **Enables**: OBJ-001, OBJ-002, OBJ-003, and ALL EPIC-009 implementation stories
- **Related Epics**: EPIC-002 (Asset Core foundation), EPIC-001 (ObjectManager integration)
- **FRED2 Impact**: Ensures FRED2 editor can access object type definitions for mission editing