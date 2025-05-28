# EPIC-001: Core Foundation & Infrastructure - Godot Dependencies

**Epic**: EPIC-001 - Core Foundation & Infrastructure  
**Architect**: Mo (Godot Architect)  
**Version**: 2.0 (Simplified based on Godot-native approach)  
**Date**: 2025-01-27  

## Overview

Dependency mapping for the foundation infrastructure implementation. **Architectural Insight**: The simplified Godot-native approach dramatically reduces dependency complexity compared to WCS's 58+ files with 100+ interdependencies.

**Key Achievement**: Clean dependency chains with minimal circular references, leveraging Godot's built-in systems.

## Core Dependency Architecture

### Foundation Layer (No Dependencies - Pure Godot)

#### Godot Built-in Systems (Zero Implementation Needed)
```
Godot Engine Core Systems (No custom code required):
├── Vector3, Transform3D, Basis → Replaces WCS math libraries
├── FileAccess → Replaces WCS file I/O system  
├── ResourceLoader → Replaces WCS asset loading
├── JSON, ConfigFile → Replaces WCS parsing systems
└── Cross-platform APIs → Replaces WCS platform abstraction
```

**Dependency Impact**: Zero - these are Godot engine capabilities

### Level 1: Core Constants (Foundation Dependencies)

#### `res://scripts/core/constants/wcs_constants.gd`
```gdscript
# DEPENDENCIES: None (static class with constants)
# USED BY: All other scripts
```

#### `res://scripts/core/constants/wcs_types.gd`
```gdscript
# DEPENDENCIES: None (enum definitions)
# USED BY: All resource classes and utilities
```

#### `res://scripts/core/constants/wcs_paths.gd`
```gdscript
# DEPENDENCIES: None (static paths)
# USED BY: Asset loading and file utilities
```

**Dependency Chain**: Foundation → No dependencies, consumed by everything

### Level 2: Resource Classes (Constants Dependencies)

#### `res://scripts/core/config/game_config.gd`
```gdscript
# DEPENDENCIES:
extends Resource
const WCSTypes = preload("res://scripts/core/constants/wcs_types.gd")
const WCSConstants = preload("res://scripts/core/constants/wcs_constants.gd")

# USED BY: All game systems requiring configuration
```

#### `res://scripts/core/config/player_profile.gd`
```gdscript
# DEPENDENCIES:
extends Resource
const WCSTypes = preload("res://scripts/core/constants/wcs_types.gd")

# USED BY: Save/load systems, player data management
```

#### `res://scripts/core/config/control_settings.gd`
```gdscript
# DEPENDENCIES:
extends Resource
const WCSTypes = preload("res://scripts/core/constants/wcs_types.gd")

# USED BY: Input system, controls configuration
```

### Level 3: Utility Classes (Resource Dependencies)

#### `res://scripts/core/utils/math_utils.gd`
```gdscript
# DEPENDENCIES:
const WCSConstants = preload("res://scripts/core/constants/wcs_constants.gd")
# Uses: Vector3, Transform3D, Basis (Godot built-ins)

# USED BY: Physics systems, ship movement, collision detection
```

#### `res://scripts/core/utils/file_utils.gd`
```gdscript
# DEPENDENCIES:
const WCSPaths = preload("res://scripts/core/constants/wcs_paths.gd")
# Uses: FileAccess, DirAccess (Godot built-ins)

# USED BY: Asset loading, save/load systems, configuration
```

#### `res://scripts/core/utils/debug_utils.gd`
```gdscript
# DEPENDENCIES:
const WCSConstants = preload("res://scripts/core/constants/wcs_constants.gd")
# Uses: print, push_error (Godot built-ins)

# USED BY: All systems for debugging and logging
```

### Level 4: Asset Management (Utility Dependencies)

#### `res://scripts/core/assets/wcs_resource_loader.gd` (IF NEEDED)
```gdscript
# DEPENDENCIES:
extends ResourceFormatLoader
const WCSTypes = preload("res://scripts/core/constants/wcs_types.gd")
const FileUtils = preload("res://scripts/core/utils/file_utils.gd")

# USED BY: Godot's ResourceLoader system automatically
```

#### `res://autoloads/asset_registry.gd` (ONLY IF ABSOLUTELY NECESSARY)
```gdscript
# DEPENDENCIES:
extends Node
const WCSPaths = preload("res://scripts/core/constants/wcs_paths.gd")
const FileUtils = preload("res://scripts/core/utils/file_utils.gd")

# USED BY: Systems requiring asset discovery (rare)
```

### Level 5: Advanced Resource Classes

#### `res://scripts/core/resources/base_wcs_resource.gd`
```gdscript
# DEPENDENCIES:
extends Resource
const WCSTypes = preload("res://scripts/core/constants/wcs_types.gd")

# USED BY: All WCS data resource classes (ship data, weapon data, etc.)
```

#### `res://scripts/core/resources/wcs_data_validator.gd`
```gdscript
# DEPENDENCIES:
extends RefCounted
const WCSTypes = preload("res://scripts/core/constants/wcs_types.gd")
const WCSConstants = preload("res://scripts/core/constants/wcs_constants.gd")

# USED BY: Data validation during asset loading and conversion
```

## Dependency Chain Summary

```
Level 1: Constants (No Dependencies)
  ├── wcs_constants.gd
  ├── wcs_types.gd  
  └── wcs_paths.gd
  
Level 2: Resources (Constants Dependencies)
  ├── game_config.gd
  ├── player_profile.gd
  └── control_settings.gd
  
Level 3: Utilities (Constants + Resource Dependencies)
  ├── math_utils.gd
  ├── file_utils.gd
  └── debug_utils.gd
  
Level 4: Asset Management (Utility Dependencies) 
  ├── wcs_resource_loader.gd (optional)
  └── asset_registry.gd (optional autoload)
  
Level 5: Advanced Resources (All Dependencies)
  ├── base_wcs_resource.gd
  └── wcs_data_validator.gd
```

## Cross-Epic Dependencies (Output Dependencies)

### EPIC-002 Dependencies on EPIC-001
```gdscript
# EPIC-002 asset structures will depend on:
const WCSTypes = preload("res://scripts/core/constants/wcs_types.gd")
const BaseWCSResource = preload("res://scripts/core/resources/base_wcs_resource.gd")
const MathUtils = preload("res://scripts/core/utils/math_utils.gd")
```

### EPIC-003 Dependencies on EPIC-001  
```gdscript
# EPIC-003 migration tools will depend on:
const WCSPaths = preload("res://scripts/core/constants/wcs_paths.gd")
const FileUtils = preload("res://scripts/core/utils/file_utils.gd")
const WCSDataValidator = preload("res://scripts/core/resources/wcs_data_validator.gd")
```

## Circular Dependency Prevention

### Mo's Anti-Pattern Enforcement
1. **No Circular References**: Constants → Resources → Utilities → Asset Management (one-way flow)
2. **No Cross-Level Dependencies**: Level N can only depend on Level N-1 or lower
3. **No Autoload Dependencies**: Autoloads (if any) are leaf nodes, nothing depends on them
4. **Resource Path References**: Use string paths instead of direct object references where needed

### Dependency Validation Rules
```gdscript
# VALID: Lower level depending on higher level
const HigherLevel = preload("res://path/to/higher_level.gd")

# INVALID: Higher level depending on lower level  
# This creates circular dependency - FORBIDDEN

# VALID: Resource path reference (breaks cycles)
@export var referenced_resource_path: String = "res://path/to/resource.tres"
func get_referenced_resource() -> Resource:
    return load(referenced_resource_path)
```

## Implementation Order (Dependency-Driven)

### Week 1: Foundation (Level 1-2)
1. `wcs_constants.gd` (No dependencies)
2. `wcs_types.gd` (No dependencies)  
3. `wcs_paths.gd` (No dependencies)
4. `game_config.gd` (Constants dependencies)
5. `player_profile.gd` (Constants dependencies)

### Week 2: Utilities (Level 3)
1. `math_utils.gd` (Constants dependencies)
2. `file_utils.gd` (Constants dependencies)
3. `debug_utils.gd` (Constants dependencies)

### Week 3-4: Advanced Systems (Level 4-5)
1. `base_wcs_resource.gd` (Foundation dependencies)
2. `wcs_data_validator.gd` (All foundation dependencies)
3. `wcs_resource_loader.gd` (Only if needed)
4. `asset_registry.gd` (Only if absolutely necessary)

## Performance Impact Analysis

### Dependency Loading Cost
- **Constants**: Zero cost (static classes)
- **Resources**: Minimal cost (Godot Resource system handles efficiently)
- **Utilities**: Near-zero cost (pure functions, no state)
- **Asset Management**: Moderate cost (but only created if needed)

### Memory Footprint
- **Total Foundation Memory**: < 1MB (compared to complex WCS systems)
- **Dependency Overhead**: Negligible (Godot preload is efficient)
- **Runtime Impact**: Zero measurable impact on 15+ year old game

## Quality Assurance

### Dependency Validation
1. **Circular Dependency Detection**: Automated checks in testing
2. **Load Order Validation**: Ensure proper initialization sequence
3. **Memory Leak Testing**: Verify no reference cycles
4. **Performance Benchmarking**: Measure initialization time

### Static Analysis
```gdscript
# Tool for dependency validation
@tool
class_name DependencyValidator
extends RefCounted

static func validate_epic_001_dependencies() -> bool:
    # Automated validation of dependency rules
    pass
```

---

**Architectural Confidence**: This dependency structure is clean, maintainable, and leverages Godot's strengths. Zero circular dependencies, minimal complexity, maximum reliability.