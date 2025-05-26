# EPIC-002: Asset Structures and Management Addon - Architecture

**Document Version**: 1.0  
**Date**: 2025-01-26  
**Architect**: Mo (Godot Architect)  
**Epic**: EPIC-002 - Asset Structures and Management Addon  
**System**: Shared asset data structures, loading system, registry  
**Approval Status**: PENDING (SallySM)  

---

## Architecture Philosophy (Mo's Principles)

> **"Shared code is clean code - one source of truth for all asset operations."**
> 
> This addon architecture creates a centralized, reusable foundation for asset management that eliminates code duplication between the main game and FRED2 editor while providing type-safe, performant asset operations.

### Core Design Principles

1. **Single Source of Truth**: All asset definitions exist in one place
2. **Type Safety First**: Static typing throughout with Resource-based architecture
3. **Performance Optimized**: Efficient loading, caching, and memory management
4. **Plugin Architecture**: Clean addon structure with minimal external dependencies
5. **Extensible Design**: Easy addition of new asset types and validation rules
6. **Developer Experience**: Intuitive APIs with comprehensive error handling

## System Architecture Overview

```
WCS Asset Core Addon
├── Plugin Framework                    # Godot addon integration
│   ├── AssetCorePlugin.gd             # Main plugin class
│   └── plugin.cfg                     # Addon configuration
├── Asset Data Structures              # Type-safe asset definitions
│   ├── BaseAssetData (Resource)       # Common asset interface
│   ├── ShipData (Resource)            # Ship specifications
│   ├── WeaponData (Resource)          # Weapon definitions
│   └── ArmorData (Resource)           # Armor and shield specs
├── Asset Loading System               # Resource loading and caching
│   ├── AssetLoader                    # Core loading functionality
│   ├── RegistryManager               # Asset discovery and cataloging
│   └── ValidationManager             # Asset integrity checking
├── Constants & Utilities              # Shared definitions
│   ├── AssetTypes                     # Asset type enumerations
│   ├── FolderPaths                    # Standardized paths
│   └── AssetUtils                     # Helper functions
└── Integration Layer                   # External system integration
    ├── GameIntegration                # Main game integration
    └── EditorIntegration              # FRED2 editor integration
```

## Detailed Component Architecture

### Asset Data Structure Hierarchy

```gdscript
# Base Asset Interface
class_name BaseAssetData
extends Resource

@export var asset_name: String
@export var asset_id: String  
@export var description: String
@export var file_path: String
@export var asset_type: AssetTypes.Type
@export var metadata: Dictionary = {}

# Validation interface
func is_valid() -> bool
func get_validation_errors() -> Array[String]
func get_asset_type() -> AssetTypes.Type

# Ship Asset Extension
class_name ShipData
extends BaseAssetData

# 100+ ship properties from existing implementation
@export var max_speed: float
@export var afterburner_max_speed: float
@export var mass: float
@export var max_shield_strength: float
@export var max_hull_strength: float
# ... (all existing ship properties preserved)

# Weapon Asset Extension  
class_name WeaponData
extends BaseAssetData

# Weapon specifications from existing implementation
@export var damage: float
@export var energy_consumed: float
@export var projectile_speed: float
@export var rate_of_fire: float
# ... (all existing weapon properties preserved)
```

### Asset Loading Architecture

```gdscript
# Core Asset Loader
class_name AssetLoader
extends RefCounted

# Singleton pattern for global access
static var instance: AssetLoader

# Loading interface
func load_asset(asset_path: String) -> BaseAssetData
func load_assets_by_type(asset_type: AssetTypes.Type) -> Array[BaseAssetData]
func preload_asset_group(group_name: String) -> void

# Caching system
var _asset_cache: Dictionary = {}
var _type_caches: Dictionary = {}

# Registry Manager for Asset Discovery
class_name RegistryManager
extends RefCounted

# Asset discovery and cataloging
func scan_asset_directories() -> void
func register_asset(asset: BaseAssetData) -> void
func get_assets_by_type(asset_type: AssetTypes.Type) -> Array[BaseAssetData]
func search_assets(query: String) -> Array[BaseAssetData]

# Asset registry storage
var _asset_registry: Dictionary = {}
var _type_indices: Dictionary = {}
var _search_index: Dictionary = {}
```

### Plugin Integration Architecture

```gdscript
# Main Plugin Class
@tool
class_name AssetCorePlugin
extends EditorPlugin

# Plugin lifecycle
func _enter_tree() -> void:
    _initialize_asset_system()
    _register_custom_types()
    _setup_autoloads()

func _exit_tree() -> void:
    _cleanup_asset_system()
    _unregister_custom_types()

# Asset system initialization
func _initialize_asset_system() -> void:
    AssetLoader.initialize()
    RegistryManager.scan_directories()
    ValidationManager.setup_validators()

# Custom type registration
func _register_custom_types() -> void:
    add_custom_type("BaseAssetData", "Resource", 
                   preload("structures/base_asset_data.gd"), 
                   preload("icons/asset_icon.svg"))
    add_custom_type("ShipData", "BaseAssetData",
                   preload("structures/ship_data.gd"),
                   preload("icons/ship_icon.svg"))
```

### Validation System Architecture

```gdscript
# Asset Validation Manager
class_name ValidationManager
extends RefCounted

# Validation interface
func validate_asset(asset: BaseAssetData) -> ValidationResult
func validate_asset_group(assets: Array[BaseAssetData]) -> Array[ValidationResult]

# Validation rules registration
var _validators: Dictionary = {}

func register_validator(asset_type: AssetTypes.Type, validator: AssetValidator) -> void
func get_validator(asset_type: AssetTypes.Type) -> AssetValidator

# Validation result structure
class_name ValidationResult
extends RefCounted

var is_valid: bool
var errors: Array[String] = []
var warnings: Array[String] = []
var suggestions: Array[String] = []
```

## Integration Patterns

### Main Game Integration

```gdscript
# Main game accesses addon through autoload
func _ready() -> void:
    # Access ship data
    var ship_data = AssetLoader.load_asset("ships/terran/colossus.tres")
    if ship_data and ship_data is ShipData:
        _configure_ship(ship_data)
    
    # Get all weapons of a type
    var primary_weapons = AssetLoader.load_assets_by_type(AssetTypes.Type.PRIMARY_WEAPON)
    _populate_weapon_selection(primary_weapons)

# Asset change notifications
func _on_asset_reloaded(asset_path: String) -> void:
    # Handle hot reloading during development
    _refresh_asset_dependent_systems()
```

### FRED2 Editor Integration

```gdscript
# Editor asset browser integration
class_name AssetBrowserDock
extends Control

@onready var asset_tree: Tree = $AssetTree
@onready var preview_panel: AssetPreviewPanel = $PreviewPanel

func _ready() -> void:
    _populate_asset_tree()
    
func _populate_asset_tree() -> void:
    # Use registry to populate tree structure
    var ships = RegistryManager.get_assets_by_type(AssetTypes.Type.SHIP)
    var weapons = RegistryManager.get_assets_by_type(AssetTypes.Type.WEAPON)
    
    _create_tree_section("Ships", ships)
    _create_tree_section("Weapons", weapons)

func _on_asset_selected(asset: BaseAssetData) -> void:
    preview_panel.display_asset(asset)
    asset_selected.emit(asset)

signal asset_selected(asset: BaseAssetData)
```

## Directory Structure

```
addons/wcs_asset_core/
├── plugin.cfg                         # Addon configuration
├── AssetCorePlugin.gd                 # Main plugin class
├── structures/                        # Asset data structures
│   ├── base_asset_data.gd            # Base asset interface
│   ├── ship_data.gd                  # Ship specifications
│   ├── weapon_data.gd                # Weapon definitions
│   └── armor_data.gd                 # Armor specifications
├── loaders/                           # Asset loading systems
│   ├── asset_loader.gd               # Core loading functionality
│   ├── registry_manager.gd           # Asset discovery
│   └── validation_manager.gd         # Asset validation
├── constants/                         # Shared constants
│   ├── asset_types.gd                # Asset type definitions
│   └── folder_paths.gd               # Standardized paths
├── utils/                            # Utility functions
│   ├── asset_utils.gd               # Helper functions
│   └── path_utils.gd                # Path management
├── icons/                            # Asset type icons
│   ├── asset_icon.svg               # Base asset icon
│   ├── ship_icon.svg                # Ship asset icon
│   └── weapon_icon.svg              # Weapon asset icon
└── README.md                         # Addon documentation
```

## Performance Considerations

### Memory Management

```gdscript
# Efficient asset caching with memory limits
class_name AssetCache
extends RefCounted

const MAX_CACHE_SIZE_MB: int = 100
const CACHE_CLEANUP_THRESHOLD: float = 0.8

var _cached_assets: Dictionary = {}
var _cache_size_bytes: int = 0
var _access_times: Dictionary = {}

func cache_asset(asset_path: String, asset: BaseAssetData) -> void:
    if _should_cache_asset(asset):
        _ensure_cache_space(asset.get_memory_size())
        _cached_assets[asset_path] = asset
        _cache_size_bytes += asset.get_memory_size()
        _access_times[asset_path] = Time.get_ticks_msec()

func _cleanup_cache() -> void:
    # LRU eviction strategy
    var sorted_by_access = _access_times.keys()
    sorted_by_access.sort_custom(_compare_access_times)
    
    var target_size = MAX_CACHE_SIZE_MB * 1024 * 1024 * CACHE_CLEANUP_THRESHOLD
    while _cache_size_bytes > target_size and sorted_by_access.size() > 0:
        var evict_path = sorted_by_access.pop_front()
        _evict_asset(evict_path)
```

### Loading Optimization

```gdscript
# Async loading for large assets
func load_asset_async(asset_path: String, callback: Callable) -> void:
    if _cached_assets.has(asset_path):
        callback.call(_cached_assets[asset_path])
        return
    
    # Use ResourceLoader.load_threaded_request for large assets
    ResourceLoader.load_threaded_request(asset_path)
    _async_loading_queue[asset_path] = callback

func _process_async_loading() -> void:
    for asset_path in _async_loading_queue.keys():
        var status = ResourceLoader.load_threaded_get_status(asset_path)
        if status == ResourceLoader.THREAD_LOAD_LOADED:
            var asset = ResourceLoader.load_threaded_get(asset_path)
            var callback = _async_loading_queue[asset_path]
            _async_loading_queue.erase(asset_path)
            
            cache_asset(asset_path, asset)
            callback.call(asset)
```

## Error Handling & Validation

### Comprehensive Error Management

```gdscript
# Asset loading error handling
enum AssetError {
    NONE,
    FILE_NOT_FOUND,
    INVALID_FORMAT,
    VALIDATION_FAILED,
    DEPENDENCY_MISSING,
    MEMORY_ERROR
}

func load_asset_safe(asset_path: String) -> AssetLoadResult:
    var result = AssetLoadResult.new()
    
    # File existence check
    if not FileAccess.file_exists(asset_path):
        result.error = AssetError.FILE_NOT_FOUND
        result.error_message = "Asset file not found: " + asset_path
        return result
    
    # Resource loading with error handling
    var resource = load(asset_path)
    if not resource:
        result.error = AssetError.INVALID_FORMAT
        result.error_message = "Failed to load resource: " + asset_path
        return result
    
    # Type validation
    if not resource is BaseAssetData:
        result.error = AssetError.INVALID_FORMAT
        result.error_message = "Asset is not a valid BaseAssetData: " + asset_path
        return result
    
    # Asset validation
    var validation_result = ValidationManager.validate_asset(resource)
    if not validation_result.is_valid:
        result.error = AssetError.VALIDATION_FAILED
        result.error_message = "Asset validation failed"
        result.validation_errors = validation_result.errors
        return result
    
    result.asset = resource
    result.error = AssetError.NONE
    return result
```

## Integration Testing Strategy

### Automated Testing Framework

```gdscript
# Asset system integration tests
extends GutTest

func test_asset_loading_lifecycle():
    # Test complete asset loading cycle
    var ship_asset = AssetLoader.load_asset("ships/terran/colossus.tres")
    assert_not_null(ship_asset, "Ship asset should load successfully")
    assert_true(ship_asset is ShipData, "Asset should be correct type")
    assert_true(ship_asset.is_valid(), "Asset should pass validation")

func test_registry_population():
    # Test asset registry functionality
    RegistryManager.scan_asset_directories()
    var ships = RegistryManager.get_assets_by_type(AssetTypes.Type.SHIP)
    assert_gt(ships.size(), 0, "Should find ship assets")

func test_validation_system():
    # Test asset validation
    var invalid_ship = ShipData.new()
    # Leave required fields empty
    var validation = ValidationManager.validate_asset(invalid_ship)
    assert_false(validation.is_valid, "Invalid asset should fail validation")
    assert_gt(validation.errors.size(), 0, "Should have validation errors")

func test_performance_requirements():
    # Test loading performance
    var start_time = Time.get_ticks_msec()
    for i in range(100):
        AssetLoader.load_asset("ships/terran/colossus.tres")
    var end_time = Time.get_ticks_msec()
    var duration_ms = end_time - start_time
    assert_lt(duration_ms, 1000, "100 asset loads should complete in <1 second")
```

## Migration from Existing Systems

### Backward Compatibility

```gdscript
# Migration support for existing asset references
func migrate_legacy_asset_reference(legacy_path: String) -> String:
    # Map old asset paths to new addon structure
    var migration_map = {
        "scripts/resources/ship_weapon/ship_data.gd": "addons/wcs_asset_core/structures/ship_data.gd",
        "scripts/resources/ship_weapon/weapon_data.gd": "addons/wcs_asset_core/structures/weapon_data.gd"
    }
    
    return migration_map.get(legacy_path, legacy_path)

# Gradual migration strategy
func ensure_addon_compatibility() -> void:
    # Check if existing systems need migration
    if _has_legacy_asset_references():
        _prompt_migration_assistant()
        _perform_gradual_migration()
```

## Future Extensibility

### Plugin Extension Points

```gdscript
# Custom asset type registration
func register_custom_asset_type(type_name: String, asset_class: Script) -> void:
    AssetTypes.register_custom_type(type_name, asset_class)
    ValidationManager.register_validator(type_name, _create_default_validator(asset_class))

# Custom validation rules
func add_validation_rule(asset_type: AssetTypes.Type, rule: ValidationRule) -> void:
    ValidationManager.add_custom_rule(asset_type, rule)

# Asset processing pipeline hooks
func register_asset_processor(asset_type: AssetTypes.Type, processor: AssetProcessor) -> void:
    AssetLoader.register_processor(asset_type, processor)
```

---

**Architecture Approval**: PENDING (SallySM)  
**Implementation Ready**: YES  
**Dependencies**: None (foundation addon)  
**Risk Level**: LOW (well-established patterns)

**Next Steps:**
1. SallySM approval of architecture
2. Story breakdown into implementable tasks
3. Dev implementation following architecture
4. Integration testing with existing systems