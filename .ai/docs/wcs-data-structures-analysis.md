# Wing Commander Saga Data Structures Analysis

**Author**: Larry (WCS Analyst)  
**Date**: 2025-01-19  
**Version**: 1.0  

## Executive Summary

This document provides a comprehensive analysis of Wing Commander Saga's data architecture, focusing on how game data is structured, parsed, and managed. The analysis examines the C++ codebase to understand data relationships, formats, and storage patterns critical for the Godot conversion strategy.

## Core Data Architecture Overview

### 1. Table-Driven Design
WCS uses a table-driven architecture where most game data is stored in `.tbl` files with a standardized parsing system:

**Key Table Files:**
- `ships.tbl` - Ship class definitions  
- `weapons.tbl` - Weapon specifications
- `species_defs.tbl` - Species configuration
- `iff_defs.tbl` - IFF (Identification Friend/Foe) settings
- `objecttypes.tbl` - Ship type behaviors
- `ai_profiles.tbl` - AI difficulty settings

**Parser System:** (`parselo.h/cpp`)
- Central text parsing engine with standardized tokens
- Supports multiple data types (strings, floats, vectors, boolean flags)
- Error handling and validation built-in
- Modular table loading for extensions

### 2. Ship Data Structures

#### Ship Class Information (`ship_info` struct)
```cpp
typedef struct ship_info {
    char name[NAME_LENGTH];                    // Ship class name
    char pof_file[MAX_FILENAME_LEN];          // 3D model filename (.pof)
    int model_num;                            // Loaded model index
    float max_vel;                            // Movement characteristics
    float max_hull_strength;                  // Durability
    float max_shield_strength;                // Shield capacity
    int num_primary_banks;                    // Weapon hardpoints
    int primary_bank_weapons[MAX_SHIP_PRIMARY_BANKS];
    int num_secondary_banks;
    int secondary_bank_weapons[MAX_SHIP_SECONDARY_BANKS];
    model_subsystem* subsystems;              // Turrets, engines, etc.
    // ... extensive additional fields
} ship_info;
```

#### Ship Instance Data (`ship` struct)
```cpp
typedef struct ship {
    int objnum;                               // Object system reference
    int ship_info_index;                      // Reference to ship_info
    char ship_name[NAME_LENGTH];              // Instance name
    float ship_max_hull_strength;             // Current max hull
    float ship_max_shield_strength;           // Current max shields
    ship_weapon weapons;                      // Current weapon loadout
    ship_subsys subsys_list;                  // Linked list of subsystems
    // ... physics, AI, status data
} ship;
```

#### Subsystem Architecture (`ship_subsys` struct)
```cpp
typedef struct ship_subsys {
    struct ship_subsys* next, *prev;         // Linked list navigation
    model_subsystem* system_info;            // Static subsystem definition
    float current_hits;                      // Current damage state
    float max_hits;                          // Maximum durability
    ship_weapon weapons;                     // Turret weapons (if applicable)
    // ... turret rotation, targeting data
} ship_subsys;
```

### 3. Weapon Data Structures

#### Weapon Class Information (`weapon_info` struct)
```cpp
typedef struct weapon_info {
    char name[NAME_LENGTH];                   // Weapon name
    int subtype;                             // WP_LASER, WP_MISSILE, WP_BEAM
    int render_type;                         // WRT_LASER, WRT_POF
    char pofbitmap_name[MAX_FILENAME_LEN];   // Model/texture file
    int model_num;                           // 3D model index (if applicable)
    float max_speed;                         // Projectile velocity
    float mass;                              // Physics mass
    float damage;                            // Base damage
    float lifetime;                          // Maximum flight time
    int wi_flags;                            // Behavior flags (WIF_*)
    beam_weapon_info b_info;                 // Beam-specific data
    spawn_weapon_info spawn_info[5];         // Child weapon spawning
    // ... extensive weapon behavior data
} weapon_info;
```

#### Weapon Instance Data (`weapon` struct)
```cpp
typedef struct weapon {
    int weapon_info_index;                   // Reference to weapon_info
    int objnum;                              // Object system reference
    int team;                                // Firing team
    float lifeleft;                          // Remaining lifetime
    vec3d start_pos;                         // Launch position
    int target_num;                          // Homing target
    int weapon_flags;                        // Runtime state flags
    // ... homing, rendering, effects data
} weapon;
```

### 4. 3D Model Architecture

#### Model Data (`polymodel` from model.h)
```cpp
typedef struct bsp_info {
    char name[MAX_NAME_LEN];                 // Submodel name
    int movement_type;                       // Rotation/movement type
    vec3d offset;                            // Position relative to parent
    matrix orientation;                      // Rotation relative to parent
    ubyte* bsp_data;                         // Binary geometry data
    vec3d geometric_center;                  // Bounding sphere center
    float rad;                               // Bounding sphere radius
    // ... submodel hierarchy data
} bsp_info;
```

#### Subsystem Definition (`model_subsystem`)
```cpp
typedef struct model_subsystem {
    char name[MAX_NAME_LEN];                 // Subsystem name
    int subobj_num;                          // Submodel index
    int type;                                // SUBSYSTEM_ENGINE, etc.
    vec3d pnt;                               // Center point
    float radius;                            // Extent radius
    float max_subsys_strength;               // Base durability
    // ... turret-specific data
    vec3d turret_norm;                       // Turret facing direction
    float turret_fov;                        // Field of view
    vec3d turret_firing_point[MAX_TFP];      // Weapon muzzles
} model_subsystem;
```

### 5. Mission Data Architecture

#### Mission Structure (`mission` struct)
- Mission metadata (name, description, designer)
- Initial ship placements and loadouts
- Wing formations and AI goals
- Environmental settings (nebula, lighting)
- Event scripting (SEXP - S-Expression system)
- Victory/failure conditions

#### Parse Objects (`p_object`)
- Template definitions for ships before instantiation
- Initial position, orientation, velocity
- Loadout specifications
- AI behavior assignments
- Arrival/departure conditions

## Data Dependencies and Relationships

### 1. Static Data Hierarchy
```
ship_info (class) 
    ├── model_num → polymodel (3D geometry)
    │   ├── submodels (bsp_info)
    │   └── subsystems (model_subsystem)
    ├── weapon arrays → weapon_info (weapon classes)
    ├── species → species_defs (faction data)
    └── ai_class → ai_profiles (behavior)
```

### 2. Runtime Data Flow
```
Parse Mission → p_object instances → ship instances → object system
                                 ↓
                               Physics, AI, Rendering systems
```

### 3. Asset Dependencies
```
Ship Class (ships.tbl)
    ├── 3D Model (.pof file)
    │   ├── Textures (.pcx, .dds files)
    │   └── Hardpoint definitions
    ├── Audio files (.wav)
    │   ├── Engine sounds
    │   └── Death/damage sounds
    └── Effects
        ├── Thruster flames
        ├── Engine glows
        └── Explosion animations
```

## File Format Analysis

### 1. Table File Format (.tbl)
**Structure:**
- Text-based, human-readable
- `$Keyword:` entries for major sections
- `+Subfield:` entries for nested properties  
- `;;` comments supported
- Modular loading (multiple files can extend base tables)

**Example (ships.tbl excerpt):**
```
$Name: CF Longbow
$Short name: Longbow
$Species: Terran
$Type: Bomber
+Tech Title: XSTR("CF-117b Longbow", 1463)
+Tech Description: XSTR("The Longbow...", 1464)
+POF file: fighter03.pof
+Mass: 18.0
+Velocity: 65.0, 130.0, 95.0
+Afterburner: 160.0
+Forward accel: 4.0
+Hitpoints: 280
+Shield Points: 520
+Primary weapon model: subspacerifle.pof
$Subsystem: Engine
    +Type: Engine
    +Flags: ( "carry shockwave" )
+Max hits: 120.0
$Default PBanks: ( "Disruptor" "Disruptor" )
$Default SBanks: ( "Tornado" "Tsunami Bomb" )
$Allowed PBanks: ( "Disruptor" "Pulse Laser" "Ion Cannon" )
$Allowed SBanks: ( "Tornado" "Tsunami Bomb" "Stiletto II" )
#End
```

### 2. 3D Model Format (.pof)
**Binary format containing:**
- Hierarchical submodel structure (BSP tree)
- Vertex data, polygon indices, texture coordinates
- Hardpoint definitions (weapon mounts, docking bays)
- Thruster definitions
- Collision geometry (separate from visual)
- LOD (Level of Detail) data

### 3. Mission Format (.fs2)
**Text-based containing:**
- Mission metadata
- Ship placement data
- Wing formation definitions
- AI goal assignments
- Event scripting (SEXP system)
- Messaging and briefing references

## Data Processing Pipeline

### 1. Initialization Sequence
1. **Table Loading**: Core game data loaded from .tbl files
2. **Asset Registration**: 3D models, textures, sounds indexed
3. **Mission Parsing**: Level-specific data processed
4. **Object Creation**: Runtime instances created from templates
5. **System Activation**: Physics, AI, rendering systems start

### 2. Runtime Data Management
- **Object System**: Unified handling of ships, weapons, effects
- **Memory Management**: Dynamic allocation for subsystems, weapons
- **Update Loops**: Physics, AI, rendering operate on live data
- **State Persistence**: Save/load system preserves runtime state

## Conversion Strategy for Godot

### 1. Static Data Resources (.tres files)
**Ship Classes → ShipClassResource**
```gdscript
class_name ShipClassResource
extends Resource

@export var name: String
@export var model_path: String
@export var max_hull: float
@export var max_shields: float
@export var velocity: Vector3
@export var primary_weapons: Array[WeaponClassResource]
@export var secondary_weapons: Array[WeaponClassResource]
@export var subsystems: Array[SubsystemResource]
```

**Weapon Classes → WeaponClassResource**
```gdscript
class_name WeaponClassResource
extends Resource

@export var name: String
@export var weapon_type: WeaponType
@export var damage: float
@export var speed: float
@export var lifetime: float
@export var model_scene: PackedScene
@export var impact_effect: PackedScene
```

### 2. Runtime Classes (GDScript)
**Ship Instance → Ship Node**
```gdscript
class_name Ship
extends CharacterBody3D

@export var ship_class: ShipClassResource
var current_hull: float
var current_shields: float
var weapons: WeaponSystem
var subsystems: Array[Subsystem]
var ai_brain: AIController
```

**Weapon Instance → Weapon Node**
```gdscript
class_name Weapon
extends Area3D

@export var weapon_class: WeaponClassResource
var target: Node3D
var life_remaining: float
var damage_amount: float
```

### 3. Asset Conversion Pipeline

#### 3D Models (.pof → .glb)
- **Tool**: Custom converter or Blender plugin
- **Process**: Extract geometry, materials, hardpoints
- **Output**: Godot scenes with proper node hierarchy
- **Hardpoints**: Convert to Godot Marker3D nodes

#### Data Tables (.tbl → .tres)
- **Tool**: Custom importer script
- **Process**: Parse text, validate data, create resources
- **Output**: Typed Godot resources for each data class
- **Validation**: Ensure data integrity and completeness

#### Missions (.fs2 → .tres + PackedScene)
- **Tool**: Mission converter
- **Process**: Parse mission data, create scene layout
- **Output**: Mission resource + pre-built scene
- **Scripts**: Convert SEXP to GDScript event system

### 4. System Architecture Translation

#### Object System → Node Tree
- WCS objects become Godot nodes
- Object types map to node inheritance
- Object management through scene tree

#### Physics → Godot Physics
- Ship movement → CharacterBody3D
- Weapon collision → Area3D detection
- Damage system → signal-based events

#### AI System → Godot AI
- AI goals → State machines
- Pathfinding → NavigationAgent3D
- Target selection → vision and sensor systems

#### Rendering → Godot 3D
- Model rendering → MeshInstance3D
- Effects → GPUParticles3D + shaders
- HUD → Control nodes + CanvasLayer

## Implementation Recommendations

### 1. Conversion Tools Priority
1. **Table Parser**: Convert .tbl files to .tres resources
2. **Model Converter**: Extract .pof geometry to .glb
3. **Mission Importer**: Parse .fs2 missions to scenes
4. **Asset Validator**: Ensure conversion completeness

### 2. Godot Resource Structure
```
res://
├── data/
│   ├── ships/           # ShipClassResource files
│   ├── weapons/         # WeaponClassResource files
│   ├── missions/        # Mission definition resources
│   └── tables/          # Raw table data backups
├── models/
│   ├── ships/           # Converted 3D ship models
│   ├── weapons/         # Weapon model scenes
│   └── effects/         # Visual effect scenes
├── scenes/
│   ├── ships/           # Complete ship scenes (model + logic)
│   ├── weapons/         # Weapon system scenes
│   └── missions/        # Mission scene templates
└── scripts/
    ├── systems/         # Core game systems
    ├── ai/              # AI behavior classes
    └── ui/              # Interface components
```

### 3. Development Phases
1. **Phase 1**: Core data structures and parsing
2. **Phase 2**: Basic ship and weapon systems
3. **Phase 3**: 3D model integration
4. **Phase 4**: AI and physics systems
5. **Phase 5**: Mission system and scripting
6. **Phase 6**: UI and polish

### 4. Static vs Dynamic Data Decisions

**Static Resources (.tres):**
- Ship class definitions
- Weapon specifications  
- Mission templates
- AI behavior patterns
- Audio/visual asset references

**Dynamic Generation:**
- Ship instances in missions
- Weapon projectiles
- Particle effects
- Runtime state data
- Procedural missions (if applicable)

**Configuration Data (Project Settings):**
- Game balance parameters
- Difficulty settings
- Control mappings
- Display options

## Technical Challenges & Solutions

### 1. Data Volume
**Challenge**: Large number of ship/weapon classes
**Solution**: Lazy loading, resource streaming, LOD systems

### 2. Model Complexity
**Challenge**: Complex .pof format with BSP trees
**Solution**: Simplify to standard meshes, approximate collision

### 3. SEXP Scripting
**Challenge**: Complex S-expression mission scripting
**Solution**: Convert to GDScript state machines and signals

### 4. Physics Accuracy
**Challenge**: WCS has custom physics simulation
**Solution**: Tune Godot physics or implement custom systems

### 5. Performance Scaling
**Challenge**: Large battles with many objects
**Solution**: Object pooling, frustum culling, level-of-detail

## Conclusion

WCS uses a well-structured, data-driven architecture that translates effectively to Godot's resource and node systems. The table-based configuration system maps naturally to Godot's resource files, while the object-oriented runtime structure aligns with Godot's scene/node architecture.

The key conversion strategy involves:
1. **Preserving data relationships** through properly typed Godot resources
2. **Maintaining gameplay fidelity** through accurate system recreation
3. **Leveraging Godot strengths** like scenes, signals, and the physics engine
4. **Creating robust tools** for automated conversion and validation

This approach ensures the converted system maintains WCS's gameplay feel while gaining the benefits of Godot's modern engine capabilities.