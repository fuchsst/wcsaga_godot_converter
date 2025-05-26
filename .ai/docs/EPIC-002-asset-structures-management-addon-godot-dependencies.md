# EPIC-002: Asset Structures & Management Addon - Godot Dependencies

## Overview
Asset management system dependency mapping showing integration with core infrastructure and providing services to all content systems. This addon serves as the central hub for all WCS asset operations.

## Core Dependencies (EPIC-001 Requirements)

### Required Autoloads from EPIC-001:
- `CoreManager` - System registration and error handling
- `FileSystemManager` - VP archive access and file operations
- `VPArchiveManager` - WCS asset file extraction
- `MathUtilities` - Unit conversion and scaling operations

### Required Core Scripts from EPIC-001:
- `res://systems/core/parsing/config_parser.gd` - For asset definition parsing
- `res://systems/core/utilities/error_handler.gd` - For asset loading error management
- `res://systems/core/file_system/file_validator.gd` - For asset integrity checking

## Asset Manager Singleton Dependencies

### Script: `res://addons/wcs_assets/asset_manager.gd`
**Autoload Registration**: Registered with `CoreManager` as "AssetManager"
**Initialization Priority**: After EPIC-001 core systems

**Signals Connected To**:
- `CoreManager.core_systems_initialized.connect(_on_core_ready)`
- `FileSystemManager.vp_archives_mounted.connect(_on_archives_ready)`
- `VPArchiveManager.vp_archive_mounted.connect(_refresh_asset_catalog)`

**References/Uses**:
- `FileSystemManager.load_from_vp(archive: String, file_path: String) -> PackedByteArray`
- `VPArchiveManager.get_file_listing(archive: String) -> Array[String]`
- `res://addons/wcs_assets/asset_registry.gd`
- `res://addons/wcs_assets/asset_cache.gd`
- `res://addons/wcs_assets/loaders/loader_registry.gd`

**Signals Emitted**:
- `asset_loaded(asset_name: String, asset: Resource)`
- `asset_load_failed(asset_name: String, error: String)`
- `asset_cache_updated(cache_size: int, memory_usage: int)`
- `asset_system_ready()`

**Functions Called By Other Systems**:
- `AssetManager.load_ship_class(class_name: String) -> ShipClass`
- `AssetManager.load_weapon_definition(weapon_name: String) -> WeaponDefinition`
- `AssetManager.get_mission_template(mission_name: String) -> MissionTemplate`
- `AssetManager.preload_asset_category(category: String)`
- `AssetManager.get_asset_dependencies(asset_name: String) -> Array[String]`

## Resource Loading Dependencies

### Script: `res://addons/wcs_assets/loaders/ship_loader.gd`
**Attached To**: Used by AssetManager for ship asset loading
**References/Uses**:
- `res://addons/wcs_assets/resources/ship_class.gd` (Resource definition)
- `res://addons/wcs_assets/loaders/base_loader.gd` (inheritance)
- `FileSystemManager` for model and texture file loading
- `MathUtilities.convert_wcs_units()` for scale conversion

**Signals Connected To**:
- `AssetManager.asset_load_requested.connect(_handle_ship_load_request)`

**Signals Emitted**:
- `ship_model_loaded(ship_name: String, model: PackedScene)`
- `ship_textures_loaded(ship_name: String, textures: Dictionary)`
- `ship_definition_validated(ship_name: String, is_valid: bool)`

### Script: `res://addons/wcs_assets/loaders/weapon_loader.gd`
**References/Uses**:
- `res://addons/wcs_assets/resources/weapon_definition.gd`
- `res://addons/wcs_assets/conversion/wcs_data_converter.gd`
- `res://addons/wcs_assets/validation/asset_validator.gd`

**Functions Called By AssetManager**:
- `load_weapon_from_table(weapon_name: String, table_data: Dictionary) -> WeaponDefinition`
- `validate_weapon_definition(weapon_def: WeaponDefinition) -> bool`

### Script: `res://addons/wcs_assets/loaders/mission_loader.gd`
**References/Uses**:
- `res://addons/wcs_assets/resources/mission_template.gd`
- `res://systems/core/parsing/config_parser.gd` for mission file parsing
- SEXP System integration (when available)

**Signals Connected To**:
- `SexpManager.expression_validated.connect(_on_sexp_validated)` (if EPIC-004 loaded)

## Resource Definition Dependencies

### Resource: `res://addons/wcs_assets/resources/ship_class.gd`
**Script Type**: `ShipClass` (extends Resource)
**Used By**: Ship Loader, Ship Manager, AI System, Combat System

**Property Dependencies**:
```gdscript
class_name ShipClass
extends Resource

@export var class_name: String
@export var display_name: String
@export var model_path: String
@export var texture_paths: Dictionary
@export var technical_specifications: ShipTechnicalSpecs
@export var weapon_hardpoints: Array[WeaponMount]
@export var engine_specifications: EngineSpecs
```

**References Other Resources**:
- `WeaponMount` resources for weapon mounting points
- `ShipTechnicalSpecs` for performance characteristics
- `EngineSpecs` for propulsion properties

### Resource: `res://addons/wcs_assets/resources/weapon_definition.gd`
**Script Type**: `WeaponDefinition` (extends Resource)
**Used By**: Weapon Loader, Combat System, Ship Loadout System

**Property Dependencies**:
```gdscript
class_name WeaponDefinition
extends Resource

@export var weapon_name: String
@export var weapon_type: WeaponType
@export var damage_properties: DamageProperties
@export var ballistics: BallisticsData
@export var visual_effects: WeaponEffects
@export var audio_effects: AudioEffects
```

## Component System Dependencies

### Script: `res://addons/wcs_assets/components/ship_component.gd`
**Attached To**: Ship entity nodes in game scenes
**References/Uses**:
- `AssetManager.load_ship_class()` for ship data loading
- `res://addons/wcs_assets/resources/ship_class.gd`

**Signals Connected To**:
- `AssetManager.asset_loaded.connect(_on_ship_asset_loaded)`

**Signals Emitted**:
- `ship_data_updated(ship_component: ShipComponent)`
- `ship_loadout_changed(new_loadout: ShipLoadout)`

### Script: `res://addons/wcs_assets/components/component_factory.gd`
**References/Uses**:
- All component script files for instantiation
- `res://addons/wcs_assets/components/component_registry.gd`

**Functions Called By Other Systems**:
- `ComponentFactory.create_ship_component(ship_class: ShipClass) -> ShipComponent`
- `ComponentFactory.create_weapon_component(weapon_def: WeaponDefinition) -> WeaponComponent`

## Database and Validation Dependencies

### Script: `res://addons/wcs_assets/database/asset_database.gd`
**References/Uses**:
- `AssetManager` for asset loading coordination
- `res://addons/wcs_assets/database/search_index.gd`
- `res://addons/wcs_assets/database/dependency_tracker.gd`

**Signals Connected To**:
- `AssetManager.asset_loaded.connect(_index_new_asset)`
- `AssetManager.asset_cache_updated.connect(_update_cache_statistics)`

### Script: `res://addons/wcs_assets/validation/asset_validator.gd`
**References/Uses**:
- `res://systems/core/utilities/error_handler.gd` for validation error reporting
- All Resource definition scripts for schema validation

**Functions Called By Loaders**:
- `validate_asset_integrity(asset: Resource) -> ValidationResult`
- `check_asset_references(asset: Resource) -> Array[String]`

## Editor Integration Dependencies

### Script: `res://addons/wcs_assets/editor/wcs_assets_dock.gd`
**Attached To**: `res://addons/wcs_assets/editor/wcs_assets_dock.tscn`
**Editor Context**: Only active in editor mode

**References/Uses**:
- `AssetManager` for asset browsing
- `EditorInterface` for file system integration
- `res://addons/wcs_assets/editor/asset_browser.gd`

**Signals Connected To**:
- `AssetManager.asset_system_ready.connect(_populate_asset_browser)`

## External System Integration Points

### For EPIC-003 (Data Migration Tools):
**Signals Provided**:
- `AssetManager.asset_load_failed` → Conversion validation
- `asset_database.asset_indexed` → Migration progress tracking

**Functions Required by EPIC-003**:
- `AssetManager.register_converted_asset(asset_path: String, asset_type: String)`
- `asset_validator.validate_converted_asset(asset: Resource) -> bool`

### For EPIC-004 (SEXP System):
**Functions Provided**:
- `AssetManager.get_ship_by_name(ship_name: String) -> ShipClass`
- `AssetManager.get_weapon_by_name(weapon_name: String) -> WeaponDefinition`

**Signals Connected From SEXP**:
- `SexpManager.expression_requires_asset.connect(_provide_asset_reference)`

### For EPIC-005 (GFRED2 Mission Editor):
**Functions Provided**:
- `AssetManager.get_available_ship_classes() -> Array[ShipClass]`
- `AssetManager.get_available_weapons() -> Array[WeaponDefinition]`
- `AssetManager.validate_mission_assets(mission: MissionTemplate) -> bool`

### For Gameplay Systems (EPIC-009+):
**Functions Provided**:
- `AssetManager.instantiate_ship_from_class(class_name: String) -> Node3D`
- `ComponentFactory.create_component_for_entity(entity: Node, component_type: String)`

## Performance-Critical Dependencies

### Asset Loading Performance:
```gdscript
# High-frequency asset queries (cached)
AssetManager.get_ship_class_cached(class_name: String) -> ShipClass
AssetManager.get_weapon_definition_cached(weapon_name: String) -> WeaponDefinition

# Batch loading for performance
AssetManager.preload_asset_batch(asset_names: Array[String])
```

### Memory Management:
```gdscript
# Asset cache management (LRU eviction)
asset_cache.set_memory_limit(limit_mb: int)
asset_cache.evict_unused_assets()

# Component pooling for performance
component_factory.pool_component(component: Component)
component_factory.get_pooled_component(component_type: String) -> Component
```

## Signal Flow Architecture

### Asset Loading Flow:
```
1. System requests asset → AssetManager.load_ship_class()
2. AssetManager checks cache → asset_cache.get_cached_asset()
3. If not cached → ship_loader.load_ship_from_table()
4. Ship loader accesses WCS data → FileSystemManager.load_from_vp()
5. Asset validation → asset_validator.validate_asset_integrity()
6. Asset stored in cache → asset_cache.store_asset()
7. Signal emitted → AssetManager.asset_loaded()
```

### Component Creation Flow:
```
1. Game system needs component → ComponentFactory.create_ship_component()
2. Factory loads asset data → AssetManager.load_ship_class()
3. Component instantiated → ship_component.gd instantiation
4. Component configured → ship_component.setup_from_ship_class()
5. Component registered → component_registry.register_component()
```

This asset management system provides a robust, cacheable, and extensible foundation for all WCS asset operations while maintaining optimal performance and clean architectural boundaries.