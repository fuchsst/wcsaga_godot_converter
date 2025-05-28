# EPIC-002: Asset Structures & Management Addon - Godot Dependencies

**Epic**: EPIC-002 - Asset Structures & Management Addon  
**Architect**: Mo (Godot Architect)  
**Version**: 2.0 (Circular dependency solution based on source analysis)  
**Date**: 2025-01-27  

## Overview

Asset management system dependency mapping showing how complex WCS asset interdependencies are resolved using Godot's Resource system. **Key Innovation**: Circular dependency resolution through Resource path references eliminates the ship.h ↔ weapon.h circular reference problem identified in the source code analysis.

**Dependency Philosophy**: Clean one-way dependency flow with Resource path references breaking cycles, leveraging Godot's built-in capabilities instead of complex custom dependency management.

## EPIC-001 Foundation Dependencies

### Required EPIC-001 Components
```gdscript
# Core foundation dependencies from EPIC-001
const WCSTypes = preload("res://scripts/core/constants/wcs_types.gd")
const WCSConstants = preload("res://scripts/core/constants/wcs_constants.gd")
const BaseWCSResource = preload("res://scripts/core/resources/base_wcs_resource.gd")
const MathUtils = preload("res://scripts/core/utils/math_utils.gd")
const FileUtils = preload("res://scripts/core/utils/file_utils.gd")
```

**Foundation Integration**: All EPIC-002 asset classes extend EPIC-001's foundation, ensuring consistent type definitions and utility access.

## Asset Dependency Architecture

### Level 1: Base Asset System (Foundation Dependencies Only)

#### `res://addons/wcs_assets/resources/base/base_asset_data.gd`
```gdscript
# DEPENDENCIES:
extends Resource  # Godot built-in
const WCSTypes = preload("res://scripts/core/constants/wcs_types.gd")  # EPIC-001

# USED BY: All asset classes (ship, weapon, model, texture, etc.)
```

#### `res://addons/wcs_assets/resources/base/asset_types.gd`
```gdscript
# DEPENDENCIES:
const WCSTypes = preload("res://scripts/core/constants/wcs_types.gd")  # EPIC-001

# USED BY: All asset management and resource classes
```

#### `res://addons/wcs_assets/resources/base/asset_validator.gd`
```gdscript
# DEPENDENCIES:
extends RefCounted  # Godot built-in
const WCSTypes = preload("res://scripts/core/constants/wcs_types.gd")  # EPIC-001
const BaseAssetData = preload("res://addons/wcs_assets/resources/base/base_asset_data.gd")

# USED BY: All asset classes for validation
```

### Level 2: Core Asset Resources (Base Dependencies)

#### `res://addons/wcs_assets/resources/ships/weapon_slot_data.gd`
```gdscript
# DEPENDENCIES:
extends Resource  # Godot built-in
const WCSTypes = preload("res://scripts/core/constants/wcs_types.gd")  # EPIC-001

# CRITICAL: NO WEAPON DATA DEPENDENCY - uses path reference instead
@export var weapon_resource_path: String  # "res://weapons/laser_cannon.tres"

# USED BY: ShipData (breaks circular dependency)
# CIRCULAR DEPENDENCY SOLUTION: References weapon by path, not object
```

#### `res://addons/wcs_assets/resources/ships/ship_data.gd`
```gdscript
# DEPENDENCIES:
extends BaseAssetData  # Level 1
const WeaponSlotData = preload("res://addons/wcs_assets/resources/ships/weapon_slot_data.gd")
const MathUtils = preload("res://scripts/core/utils/math_utils.gd")  # EPIC-001

# CRITICAL: NO DIRECT WEAPON DATA DEPENDENCY
# Uses WeaponSlotData which references weapons by path

# USED BY: Game systems, editor, ship instantiation
```

#### `res://addons/wcs_assets/resources/weapons/weapon_data.gd`
```gdscript
# DEPENDENCIES:
extends BaseAssetData  # Level 1
const WCSTypes = preload("res://scripts/core/constants/wcs_types.gd")  # EPIC-001

# CRITICAL: NO DIRECT SHIP DATA DEPENDENCY
# Uses ship paths for compatibility, not direct references
@export var compatible_ship_paths: Array[String] = []

# USED BY: WeaponSlotData.get_weapon() (loaded on-demand)
```

### Level 3: Model and Texture Resources (Asset Dependencies)

#### `res://addons/wcs_assets/resources/models/model_data.gd`
```gdscript
# DEPENDENCIES:
extends BaseAssetData  # Level 1
const MathUtils = preload("res://scripts/core/utils/math_utils.gd")  # EPIC-001

# MODEL PATH REFERENCES (no circular dependencies)
@export var model_scene_path: String  # "res://models/ships/fighter.tscn"
@export var collision_shape_path: String

# USED BY: ShipData, WeaponData (via path references)
```

#### `res://addons/wcs_assets/resources/textures/texture_data.gd`
```gdscript
# DEPENDENCIES:
extends BaseAssetData  # Level 1

# TEXTURE PATH REFERENCES (no dependencies on using assets)
@export var texture_path: String  # "res://textures/ships/fighter_hull.png"

# USED BY: ModelData, UI systems (via path references)
```

### Level 4: Asset Management (All Asset Dependencies)

#### `res://addons/wcs_assets/scripts/management/asset_loader.gd`
```gdscript
# DEPENDENCIES:
extends RefCounted  # Godot built-in
const BaseAssetData = preload("res://addons/wcs_assets/resources/base/base_asset_data.gd")
const AssetTypes = preload("res://addons/wcs_assets/resources/base/asset_types.gd")

# Uses ResourceLoader (Godot built-in) - no custom caching dependencies
# USED BY: All systems requiring asset loading
```

#### `res://addons/wcs_assets/scripts/management/asset_registry.gd`
```gdscript
# DEPENDENCIES:
extends RefCounted  # Godot built-in
const AssetLoader = preload("res://addons/wcs_assets/scripts/management/asset_loader.gd")
const FileUtils = preload("res://scripts/core/utils/file_utils.gd")  # EPIC-001

# USED BY: Asset discovery and search systems
```

## Circular Dependency Resolution Strategy

### WCS Problem Analysis
```cpp
// WCS CIRCULAR DEPENDENCY PROBLEM (from source analysis):
// ship.h includes weapon.h (for weapon mounts)
// weapon.h includes ship.h (for ship compatibility)
// Result: Complex build dependencies, fragile system
```

### Godot Solution Implementation
```gdscript
# SOLUTION 1: Resource Path References
# ship_data.gd - NO direct weapon dependency
@export var weapon_slots: Array[WeaponSlotData] = []

# weapon_slot_data.gd - References weapon by path
@export var weapon_resource_path: String = "res://weapons/laser_cannon.tres"
func get_weapon() -> WeaponData:
    return load(weapon_resource_path) as WeaponData  # Loaded on-demand

# SOLUTION 2: Compatibility Arrays  
# weapon_data.gd - NO direct ship dependency
@export var compatible_ship_paths: Array[String] = [
    "res://ships/fighter.tres",
    "res://ships/bomber.tres"
]
```

### Dependency Flow Validation
```
Level 1: Base Assets (No interdependencies)
  ├── base_asset_data.gd
  ├── asset_types.gd
  └── asset_validator.gd

Level 2: Core Assets (Base dependencies only)
  ├── weapon_slot_data.gd → References weapons by PATH
  ├── ship_data.gd → Uses weapon_slot_data (no direct weapon dependency)
  └── weapon_data.gd → References ships by PATH

Level 3: Support Assets (Asset dependencies)
  ├── model_data.gd → References models by PATH
  ├── texture_data.gd → References textures by PATH
  └── effect_data.gd → References effects by PATH

Level 4: Management Systems (All dependencies)
  ├── asset_loader.gd → Loads all asset types
  └── asset_registry.gd → Manages all asset discovery
```

**Dependency Validation**: NO circular references - clean one-way dependency flow

## Cross-Epic Dependencies (Output Dependencies)

### EPIC-003 (Migration Tools) Dependencies on EPIC-002
```gdscript
# Migration tools will use asset structures:
const BaseAssetData = preload("res://addons/wcs_assets/resources/base/base_asset_data.gd")
const ShipData = preload("res://addons/wcs_assets/resources/ships/ship_data.gd")
const WeaponData = preload("res://addons/wcs_assets/resources/weapons/weapon_data.gd")
const AssetLoader = preload("res://addons/wcs_assets/scripts/management/asset_loader.gd")
```

### Game Systems Dependencies on EPIC-002
```gdscript
# All game systems will depend on asset structures:
const AssetLoader = preload("res://addons/wcs_assets/scripts/management/asset_loader.gd")
const ShipData = preload("res://addons/wcs_assets/resources/ships/ship_data.gd")
const WeaponData = preload("res://addons/wcs_assets/resources/weapons/weapon_data.gd")
```

## Implementation Order (Dependency-Driven)

### Week 1: Foundation and Base Assets
1. `base_asset_data.gd` (Level 1 - no dependencies)
2. `asset_types.gd` (Level 1 - no dependencies)
3. `asset_validator.gd` (Level 1 - base dependencies only)
4. `weapon_slot_data.gd` (Level 2 - base dependencies only)

### Week 2: Core Asset Classes  
1. `ship_data.gd` (Level 2 - uses weapon_slot_data, no direct weapon dependency)
2. `weapon_data.gd` (Level 2 - no direct ship dependency)
3. `model_data.gd` (Level 3 - asset dependencies)
4. `texture_data.gd` (Level 3 - asset dependencies)

### Week 3: Specialized Assets
1. `effect_data.gd` (Level 3 - asset dependencies)
2. `species_data.gd` (Level 3 - asset dependencies)
3. `mission_data.gd` (Level 3 - asset dependencies)

### Week 4: Management Systems
1. `asset_loader.gd` (Level 4 - all asset dependencies)
2. `asset_registry.gd` (Level 4 - all dependencies)
3. Editor integration systems
4. Testing and validation

## Performance and Memory Analysis

### Dependency Loading Impact
- **Resource Path Loading**: Minimal overhead (Godot ResourceLoader is optimized)
- **On-Demand Loading**: Only loads assets when actually needed
- **Built-in Caching**: Godot automatically caches loaded resources
- **Memory Footprint**: Significantly lower than WCS's 4,750-slot texture cache

### Circular Dependency Prevention Benefits
- **Build Time**: No complex dependency resolution needed
- **Runtime Loading**: Clean loading order, no dependency loops
- **Memory Management**: No reference cycles, proper garbage collection
- **Maintainability**: Clear dependency relationships, easy to debug

## Quality Assurance

### Dependency Validation Tests
```gdscript
# test_circular_dependencies.gd
class_name TestCircularDependencies
extends GutTest

func test_no_circular_dependencies():
    # Validate no circular references in asset system
    var ship_data = ShipData.new()
    var weapon_slot = WeaponSlotData.new()
    weapon_slot.weapon_resource_path = "res://test_weapon.tres"
    
    # Verify weapon can be loaded without creating circular reference
    assert_true(weapon_slot.get_weapon() is WeaponData)
    
func test_dependency_order():
    # Verify assets can be loaded in dependency order
    pass
```

### Static Analysis Tools
```gdscript
# dependency_analyzer.gd - Development tool
@tool
class_name DependencyAnalyzer
extends RefCounted

static func analyze_asset_dependencies() -> Dictionary:
    # Analyze all asset files for dependency violations
    # Report any potential circular references
    pass
```

## Editor Integration Dependencies

### Asset Inspector Integration
```gdscript
# Custom inspector for asset editing
extends EditorInspectorPlugin

func _can_handle(object) -> bool:
    return object is BaseAssetData

func _parse_begin(object):
    # Add custom UI for asset editing
    # Show resolved dependencies in inspector
    pass
```

---

**Architectural Confidence**: This dependency structure elegantly solves WCS's circular dependency problem while maintaining clean, maintainable code. The Resource path approach is Godot-native and provides excellent performance with minimal complexity.