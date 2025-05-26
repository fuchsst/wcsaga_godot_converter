# EPIC-002: Asset Structures & Management Addon - Godot Files

**Epic**: EPIC-002 - Asset Structures & Management Addon  
**Architect**: Mo (Godot Architect)  
**Version**: 2.0 (Based on source code analysis and circular dependency solution)  
**Date**: 2025-01-27  

## Overview

Comprehensive asset management system implemented as a Godot addon, providing Resource-based data structures, efficient loading systems, and component architecture for all WCS assets.

**Architectural Revolution**: Analysis of 21 WCS asset files (~50,000+ lines) revealed complex interdependencies, particularly circular references between ship.h ↔ weapon.h. Godot's Resource system provides an elegant solution using Resource paths instead of direct object references.

**Key Innovation**: Circular dependency resolution through Resource path references, eliminating the need for complex dependency management while maintaining clean asset relationships.

## Addon Structure

### `res://addons/wcs_assets/`

#### Plugin Configuration
- `plugin.cfg`: Addon metadata and activation configuration
- `plugin.gd`: Main addon plugin class (extends EditorPlugin)

## Core Resource Definitions (WCS Data Structures)

### Base Asset System

#### `res://addons/wcs_assets/resources/base/`
- `base_asset_data.gd`: Base class for all WCS assets (extends Resource)
- `asset_types.gd`: Asset type enumerations and constants
- `asset_validator.gd`: Validation utilities for asset integrity

```gdscript
# base_asset_data.gd - Foundation for all assets
class_name BaseAssetData
extends Resource

@export var asset_name: String
@export var asset_id: String  
@export var description: String
@export var asset_type: AssetTypes.Type
@export var metadata: Dictionary = {}

func is_valid() -> bool
func get_validation_errors() -> Array[String]
```

### Ship Asset System (Complex Dependency Resolution)

#### `res://addons/wcs_assets/resources/ships/`
- `ship_data.gd`: Ship class definitions with weapon mount system
- `weapon_slot_data.gd`: Weapon mounting configuration (breaks circular dependency)
- `ship_subsystem_data.gd`: Ship component system definitions
- `shield_data.gd`: Shield system specifications

```gdscript
# ship_data.gd - Circular Dependency Solution
class_name ShipData
extends BaseAssetData

# Ship properties (100+ properties from WCS analysis)
@export var max_speed: float
@export var afterburner_max_speed: float
@export var mass: float
@export var max_hull_strength: float

# SOLUTION: Weapon references by path, not object
@export var weapon_slots: Array[WeaponSlotData] = []

# weapon_slot_data.gd - Breaks ship↔weapon circular dependency
class_name WeaponSlotData
extends Resource

@export var weapon_resource_path: String  # "res://weapons/laser_cannon.tres"
@export var mount_position: Vector3
@export var mount_type: String
@export var mount_flags: int

# Weapon loaded on-demand, breaking circular dependency
func get_weapon() -> WeaponData:
    return load(weapon_resource_path) as WeaponData
```

### Weapon Asset System  

#### `res://addons/wcs_assets/resources/weapons/`
- `weapon_data.gd`: Weapon definitions and behavior specifications
- `weapon_behavior_data.gd`: Weapon behavior flags and configuration
- `projectile_data.gd`: Projectile physics and visual specifications

```gdscript
# weapon_data.gd - Independent weapon definitions
class_name WeaponData
extends BaseAssetData

# Weapon properties (from WCS weapon.h analysis)
@export var damage: float
@export var energy_consumed: float
@export var projectile_speed: float
@export var rate_of_fire: float
@export var weapon_behavior_flags: int

# Compatible ship classes by path reference (no circular dependency)
@export var compatible_ship_paths: Array[String] = []
```

### 3D Model Asset System

#### `res://addons/wcs_assets/resources/models/`
- `model_data.gd`: 3D model specifications and LOD configuration
- `submodel_data.gd`: Hierarchical model component system
- `attachment_point_data.gd`: Weapon/component mounting points

```gdscript
# model_data.gd - POF model conversion data
class_name ModelData
extends BaseAssetData

@export var model_scene_path: String  # "res://models/ships/fighter.tscn"
@export var collision_shape_path: String
@export var submodels: Array[SubmodelData] = []
@export var attachment_points: Array[AttachmentPointData] = []
@export var bounding_radius: float
```

### Texture Asset System

#### `res://addons/wcs_assets/resources/textures/`
- `texture_data.gd`: Texture specifications and format information
- `texture_set_data.gd`: Grouped texture collections for models

```gdscript
# texture_data.gd - Simplified texture management
class_name TextureData
extends BaseAssetData

@export var texture_path: String  # "res://textures/ships/fighter_hull.png"
@export var original_format: String  # "PCX", "TGA", etc.
@export var resolution: Vector2
@export var has_transparency: bool
```

## Asset Management System

### Core Management

#### `res://addons/wcs_assets/scripts/management/`
- `asset_loader.gd`: Core asset loading functionality (uses ResourceLoader)
- `asset_registry.gd`: Asset discovery and cataloging system
- `asset_cache_manager.gd`: Memory management (minimal - Godot handles most caching)

```gdscript
# asset_loader.gd - Simplified asset loading
class_name AssetLoader
extends RefCounted

# Uses Godot's built-in ResourceLoader - no custom caching needed
static func load_asset(asset_path: String) -> BaseAssetData:
    return ResourceLoader.load(asset_path) as BaseAssetData

static func load_assets_by_type(asset_type: AssetTypes.Type) -> Array[BaseAssetData]:
    # Use Godot's ResourceLoader with type filtering
    pass
```

### Asset Discovery

#### `res://addons/wcs_assets/scripts/discovery/`
- `asset_scanner.gd`: Directory scanning for asset discovery
- `asset_indexer.gd`: Asset metadata indexing for search
- `asset_validator.gd`: Asset integrity validation

## Specialized Asset Types

### Mission Assets

#### `res://addons/wcs_assets/resources/missions/`
- `mission_data.gd`: Mission configuration and metadata
- `objective_data.gd`: Mission objective definitions
- `waypoint_data.gd`: Navigation waypoint system

### Effect Assets

#### `res://addons/wcs_assets/resources/effects/`
- `effect_data.gd`: Visual effect specifications
- `fireball_data.gd`: Explosion effect definitions
- `trail_data.gd`: Engine trail configurations

### Species and Faction Assets

#### `res://addons/wcs_assets/resources/factions/`
- `species_data.gd`: Species-specific configurations
- `iff_data.gd`: Identification Friend/Foe system
- `faction_data.gd`: Faction relationships and properties

## Addon Integration System

### Editor Integration

#### `res://addons/wcs_assets/editor/`
- `asset_inspector.gd`: Custom inspector for WCS assets
- `asset_dock.gd`: Asset browser dock for editor
- `asset_importer.gd`: Import pipeline integration

### Runtime Integration

#### `res://addons/wcs_assets/runtime/`
- `asset_preloader.gd`: Runtime asset preloading system
- `asset_query.gd`: Runtime asset search and filtering
- `asset_factory.gd`: Asset instantiation utilities

## Testing Infrastructure

#### `res://addons/wcs_assets/tests/`
- `test_asset_loading.gd`: Asset loading validation tests
- `test_circular_dependencies.gd`: Circular dependency prevention tests
- `test_resource_integrity.gd`: Resource data integrity tests
- `test_performance.gd`: Asset loading performance benchmarks

## Configuration and Data Files

### Asset Definitions

#### `res://addons/wcs_assets/data/`
- `asset_registry.json`: Master asset registry (generated)
- `asset_paths.json`: Standard asset path definitions
- `validation_rules.json`: Asset validation configuration

### Template Resources

#### `res://addons/wcs_assets/templates/`
- `ship_template.tres`: Default ship data template
- `weapon_template.tres`: Default weapon data template
- `model_template.tres`: Default model data template

## File Count Summary

**Total Implementation Files**: ~25-30 files (for 50,000+ lines of WCS complexity)
- **Resource Classes**: 12-15 files
- **Management Scripts**: 6-8 files  
- **Editor Integration**: 3-4 files
- **Testing**: 4-5 files
- **Configuration**: 3-4 files

## Implementation Priority

### Phase 1: Core Resources (Week 1)
1. `base_asset_data.gd` - Foundation class
2. `asset_types.gd` - Type definitions
3. `ship_data.gd` - Ship definitions
4. `weapon_slot_data.gd` - Circular dependency solution

### Phase 2: Asset Management (Week 2)
1. `weapon_data.gd` - Weapon definitions
2. `model_data.gd` - 3D model integration
3. `asset_loader.gd` - Loading system
4. `asset_registry.gd` - Discovery system

### Phase 3: Specialized Assets (Week 3)
1. `texture_data.gd` - Texture management
2. `species_data.gd` - Faction system
3. `effect_data.gd` - Visual effects
4. Editor integration components

### Phase 4: Integration & Testing (Week 4)
1. Runtime integration systems
2. Testing infrastructure
3. Performance optimization
4. Documentation and validation

## Mo's Architectural Notes

**Circular Dependency Solution**:
- **Problem**: WCS ship.h ↔ weapon.h circular references
- **Solution**: Resource path strings instead of direct object references
- **Benefit**: Clean dependencies, Godot-native approach, maintainable code

**Resource System Advantages**:
- **Built-in Caching**: No need for custom 4,750-slot texture cache
- **Automatic Loading**: ResourceLoader handles dependencies automatically
- **Editor Integration**: @export properties work seamlessly in editor
- **Type Safety**: Strong typing with Resource subclasses

**Performance Confidence**:
- **15+ Year Old Game**: No performance concerns with modern hardware
- **Godot Efficiency**: Built-in Resource system is highly optimized
- **Minimal Overhead**: Clean architecture reduces complexity overhead

**Quality Standards**:
- 100% static typing with Resource subclasses
- Every Resource class documented with usage examples
- Comprehensive test coverage for circular dependency prevention
- Editor integration for asset browsing and validation

---

**Implementation Confidence**: This addon architecture elegantly solves WCS's complex asset interdependencies while leveraging Godot's Resource system strengths. Achievable in 4 weeks with robust, maintainable results.