# EPIC-002: Asset Structures & Management Addon - WCS Source Dependencies

**Epic**: EPIC-002 - Asset Structures & Management Addon  
**Analyst**: Larry (WCS Analyst)  
**Analysis Date**: 2025-01-27  
**WCS Source**: /mnt/d/projects/wcsaga_godot_converter/source/code/  

## Executive Summary

This document maps the critical dependencies between WCS C++ source files that comprise the asset structures and management systems for EPIC-002. Understanding these relationships is essential for proper conversion sequencing and maintaining system integrity during the Godot implementation.

**Dependency Analysis Focus**:
- Core asset definition interdependencies
- Table data parsing dependencies
- Asset loading and caching relationships
- Cross-system references and shared structures

## Critical Foundation Dependencies

### 1. Core Asset Structure Dependencies

#### `ship/ship.h` → Foundation Dependencies
```cpp
// Primary EPIC-001 Dependencies (Critical)
#include "globalincs/pstypes.h"        // Base types and definitions
#include "globalincs/globals.h"        // Global constants and enums
#include "math/vecmat.h"               // Vector and matrix mathematics
#include "cfile/cfile.h"               // File I/O for ship data loading
#include "parse/parselo.h"             // Table parsing infrastructure

// Asset Structure Dependencies (EPIC-002)
#include "model/model.h"               // 3D model integration
#include "weapon/weapon.h"             // Weapon mount definitions
#include "species_defs/species_defs.h" // Species classification
#include "iff_defs/iff_defs.h"         // Faction system integration
```

**Dependency Impact**: ship.h is the central hub requiring 9+ core dependencies
**Conversion Priority**: Must ensure all foundation systems (EPIC-001) are stable first

#### `weapon/weapon.h` → Foundation Dependencies
```cpp
// Primary EPIC-001 Dependencies
#include "globalincs/pstypes.h"        // Base types
#include "math/vecmat.h"               // Projectile physics calculations
#include "parse/parselo.h"             // Weapons.tbl parsing

// Asset Integration Dependencies
#include "model/model.h"               // Weapon 3D models
#include "ship/ship.h"                 // Ship mount points (circular!)
```

**Circular Dependency Alert**: ship.h ↔ weapon.h creates interdependency
**Conversion Strategy**: Implement base structures first, then cross-references

### 2. 3D Model System Dependencies

#### `model/model.h` → Core Dependencies
```cpp
// Foundation Dependencies (EPIC-001)
#include "globalincs/pstypes.h"        // Basic types
#include "math/vecmat.h"               // 3D mathematics
#include "cfile/cfile.h"               // POF file loading

// Graphics Dependencies (Future EPIC-009)
#include "graphics/2d.h"               // Texture references
#include "bmpman/bmpman.h"             // Texture management
```

**Usage By**: 15+ files depend on model.h
- ship/ship.h (ship 3D models)
- weapon/weapon.h (weapon models)
- asteroid/asteroid.h (debris models)
- fireball/fireballs.h (effect models)

#### `model/modelread.cpp` → Heavy Dependencies
```cpp
// File Format Dependencies
#include "model/model.h"               // Model structures
#include "cfile/cfile.h"               // POF file reading
#include "parse/parselo.h"             // Data parsing utilities

// Memory Management
#include "globalincs/pstypes.h"        // Memory allocation types
```

**Critical Path**: POF loading is essential for all 3D assets
**Performance Impact**: Model cache affects loading times significantly

### 3. Texture Management Dependencies

#### `bmpman/bmpman.h` → Format Support Dependencies
```cpp
// Core Dependencies (EPIC-001)
#include "globalincs/pstypes.h"        // Base types
#include "cfile/cfile.h"               // Image file loading

// Format-Specific Dependencies
#include "pcxutils/pcxutils.h"         // PCX format support
#include "tgautils/tgautils.h"         // TGA format support
#include "jpgutils/jpgutils.h"         // JPEG format support
#include "pngutils/pngutils.h"         // PNG format support
#include "ddsutils/ddsutils.h"         // DDS format support
```

**Usage Pattern**: Referenced by 50+ files across all visual systems
**Cache Dependency**: 4,750-slot texture cache is performance-critical

#### `bmpman/bmpman.cpp` → Implementation Dependencies
```cpp
// Graphics System Integration
#include "graphics/gropengl.h"         // OpenGL texture upload
#include "graphics/grinternal.h"       // Graphics internal functions

// Memory Management
#include "globalincs/systemvars.h"     // System configuration
```

## Asset Loading Pipeline Dependencies

### 4. VP Archive System Dependencies

#### `cfile/cfilearchive.h` → Archive Infrastructure
```cpp
// Foundation Dependencies
#include "cfile/cfile.h"               // Basic file operations
#include "globalincs/pstypes.h"        // Standard types
```

**Usage Impact**: All asset loading depends on VP archive access
**Files Using VP System**: 
- model/modelread.cpp (POF model loading)
- bmpman/bmpman.cpp (texture loading)
- ship/ship.cpp (ships.tbl loading)
- weapon/weapons.cpp (weapons.tbl loading)

### 5. Table Data Parsing Dependencies

#### Ships.tbl Parsing Chain
```
ship/ship.cpp::parse_ship()
  ↓ depends on
parse/parselo.h::required_string()
  ↓ depends on  
cfile/cfile.h::cfread_string()
  ↓ depends on
globalincs/pstypes.h::basic types
```

#### Weapons.tbl Parsing Chain
```
weapon/weapons.cpp::parse_weapon()
  ↓ depends on
parse/parselo.h::stuff_float()
  ↓ depends on
cfile/cfile.h::cf_get_file_list()
  ↓ depends on
cfile/cfilearchive.h::VP file access
```

## Cross-System Asset Dependencies

### 6. Ship-Weapon Integration
```cpp
// ship/ship.h requires weapon definitions
typedef struct ship_weapon {
    int weapon_info_index;             // Index into weapon_info[]
    // ... weapon mount data
} ship_weapon;

// weapon/weapon.h requires ship references  
typedef struct weapon_info {
    int parent_ship_class;             // Ship class restriction
    // ... weapon specifications
} weapon_info;
```

**Circular Reference Resolution**: Use forward declarations and indices
**Loading Order**: Weapons must be loaded before ships for validation

### 7. Model-Texture Integration
```cpp
// model/model.h references textures by index
typedef struct polymodel {
    int n_textures;                    // Number of textures
    int textures[MAX_MODEL_TEXTURES];  // Texture bitmap indices
    // ... model data
} polymodel;

// bmpman/bmpman.h provides texture access
extern int bm_load(char *filename);   // Returns texture index
```

**Integration Pattern**: Models store texture indices, not direct pointers
**Cache Coordination**: Model cache and texture cache must stay synchronized

### 8. Species-Ship Classification
```cpp
// species_defs/species_defs.h defines species data
typedef struct species_info {
    char species_name[NAME_LENGTH];
    // ... species properties
} species_info;

// ship/ship.h links ships to species
typedef struct ship_info {
    int species;                       // Index into species_info[]
    // ... ship data  
} ship_info;
```

**Classification Dependency**: Ships require species definitions for proper setup
**Loading Order**: Species must be loaded before ship classes

## Performance-Critical Dependencies

### 9. Cache Management Dependencies

#### Texture Cache Performance Chain
```
Graphics Rendering Request
  ↓
bmpman/bmpman.cpp::bm_get_info()
  ↓ (cache miss)
bmpman/bmpman.cpp::bm_load_sub_slow()
  ↓
pcxutils/pcxutils.cpp::pcx_read_header()
  ↓
cfile/cfile.cpp::cfread_uint()
  ↓
cfile/cfilearchive.cpp::cf_read_data()
```

**Bottleneck**: VP file decompression is performance-critical
**Cache Strategy**: 4,750 texture slots with LRU eviction

#### Model Cache Performance Chain
```
Ship Rendering Request
  ↓
model/modelinterp.cpp::model_render()
  ↓ (cache miss)
model/modelread.cpp::model_load()
  ↓
cfile/cfile.cpp::cf_open_read_compressed()
  ↓
cfile/cfilearchive.cpp::cf_decompress()
```

**Memory Impact**: Models can be 1MB+ each, cache size is critical
**Loading Strategy**: Preload mission-critical models, stream others

## Conversion Sequencing Recommendations

### 10. Dependency-Driven Implementation Order

#### Phase 1: Foundation Assets (Critical Dependencies)
1. **EPIC-001 Foundation** → All asset systems depend on this
2. **Basic Asset Structures** → ship_info, weapon_info, polymodel
3. **File Loading Infrastructure** → VP archive access, basic parsing

#### Phase 2: Core Asset Systems  
1. **Texture Management** → bmpman system (many dependencies)
2. **3D Model System** → model loading and basic rendering
3. **Ship Class Definitions** → ship_info structure and loading
4. **Weapon Definitions** → weapon_info structure and loading

#### Phase 3: Integration Systems
1. **Species Classification** → species_defs integration
2. **IFF System** → faction management
3. **Animation System** → model animation support
4. **Effect Systems** → fireballs, shields, trails

### 11. Critical Path Analysis

**Longest Dependency Chain**: 
```
VP Archive → File I/O → Parsing → Asset Definition → Asset Loading → Asset Cache → Asset Usage
(7 dependency levels)
```

**Most Referenced Files**:
1. `globalincs/pstypes.h` → 100+ references (foundation)
2. `ship/ship.h` → 45+ references (central asset hub)
3. `model/model.h` → 25+ references (3D asset core)
4. `bmpman/bmpman.h` → 50+ references (texture core)

**Circular Dependencies to Resolve**:
- ship.h ↔ weapon.h (weapon mounts vs ship classes)
- model.h ↔ graphics/grinternal.h (rendering integration)

## Godot Conversion Implications

### 12. Resource System Mapping

#### WCS Index-Based References → Godot Resource Paths
```cpp
// WCS: Index-based asset references
int texture_index = bm_load("ship01.pcx");
int model_index = model_load("fighter.pof");

// Godot: Resource path references  
var texture: Texture2D = preload("res://textures/ships/ship01.png")
var model: PackedScene = preload("res://models/ships/fighter.tscn")
```

#### WCS Cache Management → Godot Resource Caching
```cpp
// WCS: Manual cache with indices
bitmap_entry bitmaps[MAX_BITMAPS];
polymodel models[MAX_MODELS];

// Godot: Automatic resource management
ResourceCache.has("res://path/to/asset.tres")
ResourceLoader.load("res://path/to/asset.tres", "Resource", true)
```

### 13. Critical Conversion Challenges

1. **Index → Path Mapping**: Convert integer indices to string paths
2. **Cache Coordination**: Leverage Godot's built-in resource management  
3. **Circular Dependencies**: Use Resource references instead of direct includes
4. **Table Parsing**: Convert .tbl files to .tres Resource files
5. **VP Archives**: Extract to native Godot asset formats during import

---

**Dependency Analysis Complete**: EPIC-002 dependency relationships mapped and conversion strategy defined