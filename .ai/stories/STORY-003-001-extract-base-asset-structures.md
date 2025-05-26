# STORY-003-001: Extract Base Asset Data Structures

## Story Overview
**Story ID**: STORY-003-001  
**Epic**: EPIC-003 Asset Structures and Management Addon  
**Story Name**: Extract Base Asset Data Structures  
**Story Owner**: Larry (WCS Analyst)  
**Priority**: High  
**Status**: Created  
**Created**: 2025-01-26  

## User Story
**As a** developer working on both the main game and FRED2 editor  
**I want** centralized asset data structures in a shared addon  
**So that** I can avoid code duplication and maintain consistency across projects  

## Story Description
Extract the existing asset data structures (ShipData, WeaponData, ArmorData) from the main game into the core addon framework. This includes creating the base asset interface and establishing the foundation for all future asset types.

## Current State Analysis
Based on analysis of `/target/scripts/resources/ship_weapon/`:

### Existing Structures to Extract
1. **ShipData.gd** - 847 lines, 100+ properties
   - Ship specifications, physics, rendering, weapons
   - Faithful conversion of WCS ship_info structure
2. **WeaponData.gd** - Comprehensive weapon definitions
   - Physics properties, rendering data, combat specs
3. **ArmorData.gd** - Armor and shielding specifications
4. **Related utilities** - Validation and helper functions

### Extraction Strategy
- Move structures to addon preserving all functionality
- Create base class hierarchy for shared properties
- Maintain backward compatibility during transition
- Establish clear interfaces for game integration

## Acceptance Criteria

### AC1: Base Asset Interface Created
**Given** the need for consistent asset structure  
**When** I create the base asset interface  
**Then** it should provide:
- Common properties (name, id, description, file_path)
- Validation interface with `is_valid()` method
- Serialization support for `.tres` files
- Type identification system
- Standard metadata handling

**Implementation Requirements:**
```gdscript
class_name BaseAssetData
extends Resource

@export var asset_name: String = ""
@export var asset_id: String = ""
@export var description: String = ""
@export var file_path: String = ""
@export var asset_type: AssetTypes.Type = AssetTypes.Type.UNKNOWN
@export var metadata: Dictionary = {}

func is_valid() -> bool
func get_asset_type() -> AssetTypes.Type
func serialize_to_dict() -> Dictionary
func deserialize_from_dict(data: Dictionary) -> void
```

### AC2: Ship Data Structure Extracted
**Given** the existing ShipData.gd in the main game  
**When** I extract it to the addon  
**Then** it should:
- Preserve all 100+ existing properties
- Extend BaseAssetData properly
- Maintain static typing for all properties
- Include comprehensive validation logic
- Support backward compatibility with existing usage

**Key Properties to Preserve:**
- Basic info (name, tech_description, ship_class_name)
- Physical specs (max_speed, afterburner_max_speed, mass)
- Combat data (max_shield_strength, max_hull_strength)
- Rendering (pof_file, detail_distance, cockpit_pof_file)
- All other properties from current implementation

### AC3: Weapon Data Structure Extracted
**Given** the existing WeaponData.gd in the main game  
**When** I extract it to the addon  
**Then** it should:
- Preserve all weapon specification properties
- Extend BaseAssetData with weapon-specific interface
- Include physics calculations and rendering data
- Maintain compatibility with existing weapon systems
- Support proper validation and error handling

### AC4: Armor Data Structure Extracted
**Given** the existing ArmorData.gd  
**When** I extract it to the addon  
**Then** it should:
- Preserve armor and shielding specifications
- Follow the same pattern as ship and weapon data
- Include proper validation and type checking
- Maintain integration with existing systems

### AC5: Addon Plugin Structure Created
**Given** the extracted asset structures  
**When** I create the addon plugin framework  
**Then** it should:
- Have proper plugin.cfg configuration
- Include main plugin class with initialization
- Provide autoload registration for asset types
- Include proper folder structure for organization
- Support easy integration into existing projects

**Required Plugin Structure:**
```
addons/wcs_asset_core/
├── plugin.cfg
├── AssetCorePlugin.gd
├── structures/
│   ├── base_asset_data.gd
│   ├── ship_data.gd
│   ├── weapon_data.gd
│   └── armor_data.gd
├── constants/
│   └── asset_types.gd
└── README.md
```

## Technical Requirements

### Code Quality Standards
- **Static Typing**: All variables, parameters, and returns typed
- **Documentation**: Comprehensive docstrings for all public methods
- **Error Handling**: Proper validation and graceful failure handling
- **Performance**: No measurable performance degradation
- **Testing**: Unit tests for all extracted structures

### Godot Best Practices
- Use `class_name` declarations for all asset types
- Proper Resource inheritance for Godot integration
- Signal-based communication where appropriate
- Efficient memory usage with proper cleanup

### Backward Compatibility
- Existing game code continues to work unchanged
- Gradual migration path for dependent systems
- No breaking changes to public APIs
- Clear deprecation notices for old patterns

## Implementation Tasks

### Task 1: Create Addon Framework
- [ ] Create addon directory structure
- [ ] Write plugin.cfg configuration
- [ ] Implement AssetCorePlugin.gd main class
- [ ] Set up autoload registrations

### Task 2: Extract BaseAssetData
- [ ] Create base asset interface
- [ ] Define common properties and methods
- [ ] Implement validation framework
- [ ] Add serialization support

### Task 3: Extract ShipData
- [ ] Move ShipData.gd to addon structure
- [ ] Update to extend BaseAssetData
- [ ] Preserve all existing properties
- [ ] Add enhanced validation logic

### Task 4: Extract WeaponData
- [ ] Move WeaponData.gd to addon structure
- [ ] Update inheritance and typing
- [ ] Preserve weapon specifications
- [ ] Add weapon-specific validation

### Task 5: Extract ArmorData
- [ ] Move ArmorData.gd to addon structure
- [ ] Follow established patterns
- [ ] Preserve armor specifications
- [ ] Implement proper validation

### Task 6: Create Asset Type Constants
- [ ] Define AssetTypes enumeration
- [ ] Create type identification system
- [ ] Add type validation utilities
- [ ] Document type hierarchy

### Task 7: Update Main Game References
- [ ] Update import statements in main game
- [ ] Test backward compatibility
- [ ] Verify all systems still function
- [ ] Add deprecation notices where needed

### Task 8: Testing and Validation
- [ ] Create unit tests for all structures
- [ ] Test addon integration
- [ ] Validate performance impact
- [ ] Ensure no functionality regression

## Dependencies

### Upstream Dependencies
- EPIC-003 analysis completed
- Core Godot Resource system
- Existing asset implementations in main game

### Downstream Dependencies
- STORY-003-002: Addon framework expansion
- STORY-011: Basic Asset Integration (will be updated)
- Future asset loading and registry systems

## Definition of Done

### Technical Completion
- [ ] All asset structures extracted to addon
- [ ] Addon plugin properly configured and functional
- [ ] Main game successfully uses addon structures
- [ ] No regression in existing functionality
- [ ] All acceptance criteria met

### Quality Assurance
- [ ] Code review completed by Dev
- [ ] Unit tests written and passing
- [ ] Performance benchmarks show no degradation
- [ ] Documentation complete and accurate
- [ ] Integration testing passed

### BMAD Compliance
- [ ] Story follows approved architecture
- [ ] Implementation matches technical specifications
- [ ] Quality checklists completed
- [ ] Proper git commits with addon code
- [ ] Ready for next story in epic

## Risks and Mitigation

### Technical Risks
1. **Breaking Existing Code**: Refactoring may break dependencies
   - *Mitigation*: Thorough testing and gradual migration
2. **Performance Impact**: Additional abstraction layers
   - *Mitigation*: Benchmarking and optimization focus

### Timeline Risks
1. **Complex Extraction**: More dependencies than expected
   - *Mitigation*: Break into smaller tasks if needed

## Success Metrics
- Zero regression in existing functionality
- Successful addon integration in both projects
- Clean separation of data structures from game logic
- Foundation ready for asset loading system

---

**Story Created By**: Larry (WCS Analyst)  
**Story Date**: 2025-01-26  
**Ready for Implementation**: Pending architecture approval  
**BMAD Workflow Status**: Analysis → Architecture → Stories → Implementation (Next)