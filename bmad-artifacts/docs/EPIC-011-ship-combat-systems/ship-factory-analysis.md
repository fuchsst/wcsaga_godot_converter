# WCS System Analysis: Ship Class Definitions and Ship Factory Systems

## Executive Summary

The WCS ship system represents one of the most sophisticated object-oriented ship management systems in classic space combat games. At its core, it implements a comprehensive factory pattern that separates ship class definitions (`ship_info`) from ship instances (`ship`), supported by a complex subsystem architecture, weapons management, and asset integration. This system handles everything from ship spawning and configuration to real-time simulation of hundreds of ships with full subsystem damage models.

**Key Findings:**
- **Ship Factory Pattern**: Clean separation between ship templates (`Ship_info[]`), runtime instances (`Ships[]`), and asset management (`model_num`, `weapon arrays`)
- **Configuration-Driven Design**: Ship definitions loaded from `ships.tbl` with template inheritance and variant support  
- **Complex Subsystem Architecture**: Each ship instance manages dynamic lists of subsystems with individual damage states and AI behavior
- **Asset Pipeline Integration**: Ships tie together 3D models (POF files), textures, weapons, AI profiles, and audio resources
- **Performance-Optimized**: Object pooling, flyweight patterns, and efficient collision/physics integration

## System Overview

### Purpose
The ship system serves as the central object management framework for all space vehicles in WCS, handling:
- Ship class definitions and template instantiation
- Real-time ship lifecycle management (spawn, update, destroy)
- Subsystem damage modeling and repair mechanics  
- Weapon loadout configuration and firing control
- AI behavior attachment and state management
- Asset integration (models, textures, sounds, physics)

### Scope
- **Ship Creation**: `ship_create()` factory function for instantiating any ship type
- **Ship Classes**: `Ship_info[]` array containing 200+ ship class definitions
- **Ship Templates**: `Ship_templates[]` for modular inheritance and variants
- **Runtime Management**: `Ships[]` array for active ship instances (max 400)
- **Subsystem Framework**: Dynamic subsystem management with damage states
- **Asset Integration**: Model loading, texture management, weapon assignment

### Key Files
- `source/code/ship/ship.h` - Core ship structures and factory interface (1794 lines)
- `source/code/ship/ship.cpp` - Ship factory implementation and lifecycle management (15000+ lines)
- `source/code/ship/subsysdamage.h` - Subsystem damage modeling
- `source/code/model/model.h` - 3D model and subsystem definitions
- `source/code/weapon/weapon.h` - Weapon system integration

### Dependencies
- **Object System**: Ships are specialized objects in the main object array
- **Model System**: 3D geometry, collision meshes, subsystem definitions  
- **Weapon System**: Primary/secondary weapon loadouts and firing control
- **AI System**: Behavior trees, goal management, targeting logic
- **Physics System**: Movement, collision detection, damage application
- **Asset Management**: POF models, textures, sounds, particle effects

## Architecture Analysis

### Class Structure

The ship system implements a sophisticated multi-level architecture:

```cpp
// Master ship class template (loaded from ships.tbl)
struct ship_info {
    char name[NAME_LENGTH];                    // Ship class name (e.g. "GTF Apollo")
    int model_num;                            // 3D model reference
    int num_primary_banks;                    // Number of primary weapon hardpoints  
    int primary_bank_weapons[MAX_SHIP_PRIMARY_BANKS];  // Default weapon loadout
    float max_hull_strength;                  // Base hull hitpoints
    float max_shield_strength;                // Base shield strength
    model_subsystem* subsystems;             // Subsystem templates
    int n_subsystems;                         // Number of subsystems
    // ... 200+ more fields for physics, AI, assets, etc.
};

// Runtime ship instance
struct ship {
    int objnum;                               // Link to object array
    int ship_info_index;                      // Reference to ship_info template
    char ship_name[NAME_LENGTH];              // Individual ship name
    ship_subsys subsys_list;                  // Dynamic subsystem instances
    ship_weapon weapons;                      // Current weapon state
    float ship_max_hull_strength;             // Modified hull strength
    float ship_max_shield_strength;           // Modified shield strength  
    uint flags;                               // Runtime state flags
    // ... 200+ more runtime fields
};

// Dynamic subsystem instance
struct ship_subsys {
    ship_subsys* next, *prev;                 // Linked list navigation
    model_subsystem* system_info;            // Reference to template
    float current_hits;                       // Current damage state
    float max_hits;                           // Maximum hitpoints
    ship_weapon weapons;                      // Turret weapons (if applicable)
    // ... turret AI, animation state, etc.
};
```

### Data Flow

The ship factory follows a sophisticated multi-stage creation process:

1. **Class Definition Loading** (`ship_init()`):
   - Parse `ships.tbl` into `Ship_info[]` array
   - Load 3D models and extract subsystem templates
   - Build weapon compatibility matrices
   - Initialize AI class assignments

2. **Template Resolution** (`ship_template_lookup()`):
   - Support inheritance from base ship classes
   - Apply modular ship variants (e.g., "GTF Apollo#Advanced")
   - Resolve template dependencies and overrides

3. **Instance Creation** (`ship_create()`):
   - Allocate slot in `Ships[]` array
   - Create corresponding `object` in main object system
   - Clone subsystems from ship_info template to dynamic list
   - Initialize weapons from default loadout
   - Set up physics simulation parameters
   - Initialize AI behavior state

4. **Runtime Management**:
   - Update ship physics and AI each frame
   - Process subsystem damage and repair
   - Handle weapon firing and reloading
   - Manage special effects and animations

### Key Algorithms

**Ship Factory Pattern**:
```cpp
int ship_create(matrix* orient, vec3d* pos, int ship_type, char* ship_name) {
    // 1. Validate ship type and find free slot
    Assert((ship_type >= 0) && (ship_type < Num_ship_classes));
    ship_info* sip = &(Ship_info[ship_type]);
    
    // 2. Create base object in main object system
    objnum = obj_create(OBJ_SHIP, ship_index, ship_type, orient, pos, sip->model_num);
    
    // 3. Initialize ship instance from template
    ship* shipp = &Ships[ship_index];
    shipp->ship_info_index = ship_type;
    shipp->objnum = objnum;
    
    // 4. Clone subsystems from template
    subsys_set(objnum);  // Creates dynamic subsystem instances
    
    // 5. Initialize weapons, physics, AI
    ship_set_default_weapons(shipp, sip);
    physics_ship_init(&Objects[objnum]);
    
    return objnum;
}
```

**Template Lookup with Inheritance**:
```cpp
int ship_info_lookup(char* token) {
    // 1. Direct class name lookup
    idx = ship_info_lookup_sub(token);
    if (idx >= 0) return idx;
    
    // 2. Check for variant notation (e.g., "GTF Apollo#Advanced")
    char* p = get_pointer_to_first_hash_symbol(token);
    if (p != NULL) {
        // Parse variant and apply inheritance
        return resolve_ship_variant(token);
    }
    
    return -1;
}
```

## Implementation Details

### Core Functions

**Ship Factory Interface**:
- `ship_create(matrix* orient, vec3d* pos, int ship_type, char* ship_name)` - Main factory function
- `ship_info_lookup(char* name)` - Resolve ship class name to index with variant support
- `ship_template_lookup(char* name)` - Find ship template for inheritance
- `ship_set_default_weapons(ship* shipp, ship_info* sip)` - Initialize weapon loadout
- `subsys_set(int objnum)` - Create dynamic subsystem instances

**Lifecycle Management**:
- `ship_init()` - Load ship classes from tables at game startup
- `ship_level_init()` - Initialize ship system for new mission
- `ship_delete(object* objp)` - Clean up ship instance and subsystems
- `ship_cleanup(int shipnum, int cleanup_mode)` - Handle ship departure/destruction

**Asset Integration**:
- `ship_page_in_textures(int ship_index)` - Load ship textures for current mission
- `ship_model_start(object* objp)` - Setup model instance data for rendering
- `ship_assign_sound(ship* sp)` - Attach engine and ambient sounds

### State Management

**Ship Instance State**:
- **Creation**: Ships start with full hull/shields and default weapon loadout
- **Combat**: Real-time subsystem damage affects ship capabilities
- **Repair**: Support ships can restore hull, shields, and subsystems
- **Destruction**: Multi-stage death sequence with debris and explosion effects

**Subsystem State**:
- **Functional**: Subsystem operates at full capacity  
- **Damaged**: Reduced effectiveness based on current_hits/max_hits ratio
- **Destroyed**: Subsystem offline, affects ship capabilities
- **Repaired**: Support ships can restore destroyed subsystems

### Performance Characteristics

**Memory Usage**:
- `Ship_info[]`: ~500KB for 200 ship classes (2.5KB per class)
- `Ships[]`: ~2MB for 400 ship instances (5KB per instance)
- Subsystem pools: ~1MB for 4000 subsystem instances (dynamic allocation)

**Computational Complexity**:
- Ship creation: O(n) where n = number of subsystems to clone
- Ship lookup: O(1) with pre-computed hash maps for name resolution
- Subsystem damage: O(1) per subsystem hit with linked list traversal

**Bottlenecks**:
- String-based ship name lookups can be expensive in large missions
- Subsystem linked list traversal for damage calculations
- Template inheritance resolution during ship creation

## Conversion Considerations

### Godot Mapping Opportunities

**Resource System Integration**:
- Convert `ship_info` to Godot Resource classes for memory efficiency
- Use Godot's ResourceLoader for ship class definitions
- Implement ship variants as Resource inheritance hierarchy

**Node-Based Architecture**:
- Ship instances as CharacterBody3D nodes with specialized components
- Subsystems as child Area3D nodes with collision and health components
- Weapon hardpoints as Marker3D nodes with weapon controller scripts

**Factory Pattern Implementation**:
```gdscript
class_name ShipFactory
extends Node

static var ship_registry: Dictionary = {}

static func create_ship(ship_class_name: String, position: Vector3, rotation: Vector3) -> Ship:
    var ship_data = ship_registry.get(ship_class_name)
    if not ship_data:
        push_error("Unknown ship class: " + ship_class_name)
        return null
    
    var ship_scene = ship_data.scene.instantiate()
    ship_scene.position = position
    ship_scene.rotation = rotation
    
    # Initialize subsystems from template
    ship_scene.setup_subsystems(ship_data.subsystems)
    ship_scene.setup_weapons(ship_data.default_weapons)
    
    return ship_scene
```

### Potential Challenges

**Complex Subsystem Interactions**:
- WCS subsystems have intricate interdependencies (engines affect speed, weapons affect targeting)
- Godot's component system requires careful design to maintain these relationships
- Consider using composition pattern with clear interfaces

**Template Inheritance Complexity**:
- WCS supports sophisticated ship variant inheritance (#notation)
- Godot Resources provide inheritance but may need custom metadata for variant handling
- Ship template resolution logic will need to be reimplemented

**Performance Scaling**:
- WCS handles 400+ ships with thousands of subsystems in large battles
- Godot's node system may need optimization for large ship counts
- Consider object pooling and LOD systems for subsystem management

### Preservation Requirements

**Ship Creation Fidelity**:
- All WCS ship classes must be accurately represented with correct stats
- Subsystem layouts and damage models must match exactly
- Weapon hardpoint configurations must be preserved

**Behavior Preservation**:
- Ship spawning timing and locations must match mission scripts  
- Damage propagation and subsystem interdependencies must be accurate
- Support ship repair behaviors must work identically

**Asset Integration**:
- Original 3D models (POF format) must be converted to Godot scenes
- Ship textures, sounds, and effects must be properly mapped
- Weapon attachment points and firing directions must be exact

## Recommendations

### Architecture Approach

**Resource-Based Ship Classes**:
```gdscript
# Convert ship_info to Godot Resources
class_name ShipClass
extends Resource

@export var ship_name: String
@export var max_hull_strength: float
@export var max_shield_strength: float
@export var model_scene: PackedScene
@export var subsystem_templates: Array[SubsystemTemplate]
@export var default_weapons: Array[WeaponSlot]
@export var physics_params: ShipPhysicsParams
```

**Component-Based Ship Instances**:
```gdscript
# Ship instance as specialized CharacterBody3D
class_name Ship
extends CharacterBody3D

@export var ship_class: ShipClass
var subsystems: Array[ShipSubsystem] = []
var weapons: ShipWeaponManager
var damage_system: ShipDamageSystem

func _ready():
    setup_from_class(ship_class)

func setup_from_class(ship_class: ShipClass):
    # Create subsystems as child nodes
    for template in ship_class.subsystem_templates:
        var subsys = create_subsystem(template)
        add_child(subsys)
        subsystems.append(subsys)
```

**Factory Manager**:
```gdscript
# Central ship factory with registration system
class_name ShipRegistry
extends Node

@export var ship_classes: Array[ShipClass] = []
var _registry: Dictionary = {}

func _ready():
    for ship_class in ship_classes:
        register_ship_class(ship_class)

func register_ship_class(ship_class: ShipClass):
    _registry[ship_class.ship_name] = ship_class

func create_ship(class_name: String, spawn_position: Vector3) -> Ship:
    var ship_class = _registry.get(class_name)
    if not ship_class:
        return null
    
    var ship = ship_class.model_scene.instantiate()
    ship.position = spawn_position
    ship.setup_from_class(ship_class)
    return ship
```

### Implementation Priority

1. **Core Ship Factory** (Week 1-2):
   - Implement ShipClass Resource system
   - Create basic ship instantiation
   - Setup ship registry and lookup

2. **Subsystem Framework** (Week 3-4):
   - Design subsystem component architecture
   - Implement damage propagation system
   - Create subsystem template system

3. **Weapon Integration** (Week 5-6):
   - Connect to weapon system factories
   - Implement hardpoint management
   - Setup weapon slot configurations

4. **Asset Pipeline** (Week 7-8):
   - Convert POF models to Godot scenes
   - Setup texture and material pipeline
   - Integrate audio and particle effects

### Risk Assessment

**High Risk**:
- **Performance**: Godot may struggle with 400+ ships having thousands of subsystems
- **Mitigation**: Implement LOD system, object pooling, and efficient collision layers

**Medium Risk**:
- **Complex Inheritance**: WCS ship variants have sophisticated inheritance patterns
- **Mitigation**: Design clear Resource inheritance hierarchy and validation system

**Low Risk**:
- **Factory Pattern**: Godot's Resource system maps well to WCS ship_info structure
- **API Design**: Ship creation interface can be simplified while preserving functionality

## References

### Source Files
- `source/code/ship/ship.h` - Ship structures and factory interface
- `source/code/ship/ship.cpp` - Core ship factory implementation  
- `source/code/ship/subsysdamage.h` - Subsystem damage modeling
- `source/code/model/model.h` - Model and subsystem templates
- `source/code/weapon/weapon.h` - Weapon system integration
- `source/code/mission/missionparse.h` - Mission ship spawning

### Key Functions
- `int ship_create(matrix* orient, vec3d* pos, int ship_type, char* ship_name)`
- `int ship_info_lookup(char* token)`  
- `int ship_template_lookup(char* token)`
- `void ship_set_default_weapons(ship* shipp, ship_info* sip)`
- `int subsys_set(int objnum, int ignore_subsys_info)`

### External Documentation
- WCS Ship Tables Documentation
- POF Model Format Specification  
- FSOpen Ship Creation Guidelines