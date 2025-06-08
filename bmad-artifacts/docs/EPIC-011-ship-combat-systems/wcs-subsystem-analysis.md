# WCS Ship Subsystem Management Analysis

## Overview

Based on analysis of the WCS source code, the subsystem management system is a sophisticated hierarchical damage and functionality system that manages ship components and their effects on ship performance.

## Core Data Structures

### 1. ship_subsys Structure (ship.h:235-314)

The main subsystem instance structure contains:

```cpp
typedef struct ship_subsys {
    struct ship_subsys* next,*prev;          // Linked list pointers
    model_subsystem* system_info;            // Pointer to static subsystem data
    
    char sub_name[NAME_LENGTH];              // Instance-specific name override
    float current_hits;                      // Current damage state
    float max_hits;                          // Maximum health
    
    int flags;                               // Subsystem state flags
    int subsys_guardian_threshold;           // Protection threshold
    int armor_type_idx;                      // Armor type for damage calculation
    
    // Turret-specific data
    int turret_best_weapon;                  // Optimal weapon for current target
    vec3d turret_last_fire_direction;        // Last firing direction
    int turret_next_enemy_check_stamp;       // Next targeting update time
    int turret_next_fire_stamp;              // Next fire time
    int turret_enemy_objnum;                 // Current target object
    int turret_enemy_sig;                    // Target object signature
    int turret_next_fire_pos;                // Gun position cycling counter
    float turret_time_enemy_in_range;        // Accuracy improvement timer
    int turret_targeting_order[NUM_TURRET_ORDER_TYPES]; // Target prioritization
    float optimum_range;                     // Preferred engagement range
    float favor_current_facing;              // Facing preference factor
    ship_subsys* targeted_subsys;            // Targeted enemy subsystem
    
    // Weapon management
    ship_weapon weapons;                     // Weapon bank configuration
    
    // Rendering and animation
    submodel_instance_info submodel_info_1;  // Main turret instance data
    submodel_instance_info submodel_info_2;  // Gun barrel instance data
    
    // Status effects
    int disruption_timestamp;                // EMP/disruption recovery time
    
    // Cargo and misc
    int subsys_cargo_name;                   // Cargo subsystem identifier
    fix time_subsys_cargo_revealed;          // Cargo scan timestamp
    
    // Animation and rotation
    triggered_rotation trigger;              // Animation state
    float points_to_target;                  // Targeting precision
    float base_rotation_rate_pct;            // Base rotation speed modifier
    float gun_rotation_rate_pct;             // Gun rotation speed modifier
    
    // Audio
    int subsys_snd_flags;                    // Sound state flags
    int rotation_timestamp;                  // Rotation sound timing
    matrix world_to_turret_matrix;           // Turret coordinate transform
    
    // Target prioritization
    int target_priority[32];                 // Priority weights
    int num_target_priorities;               // Number of priority entries
} ship_subsys;
```

### 2. model_subsystem Structure (model.h:134-200+)

The static subsystem definition contains:

```cpp
typedef struct model_subsystem {
    uint flags;                              // Capability flags (MSS_FLAG_*)
    char name[MAX_NAME_LEN];                // Display name
    char subobj_name[MAX_NAME_LEN];         // Model object matching name
    char alt_sub_name[NAME_LENGTH];         // Override display name
    char alt_dmg_sub_name[NAME_LENGTH];     // Damage popup name
    int subobj_num;                         // Model subobject index
    int model_num;                          // Parent model index
    int type;                               // Subsystem type (SUBSYSTEM_*)
    vec3d pnt;                              // Center position
    float radius;                           // Extent radius
    float max_subsys_strength;              // Maximum health
    int armor_type_idx;                     // Armor type
    
    // Turret-specific static data
    char crewspot[MAX_NAME_LEN];            // AI crew assignment identifier
    vec3d turret_norm;                      // Default facing direction
    matrix turret_matrix;                   // Orientation matrix
    float turret_fov;                       // Field of view (horizontal)
    float turret_max_fov;                   // Maximum elevation FOV
    float turret_y_fov;                     // Vertical FOV
    int turret_num_firing_points;           // Number of gun positions
    vec3d turret_firing_point[MAX_TFP];     // Gun position offsets
    int turret_gun_sobj;                    // Gun subobject reference
    float turret_turning_rate;              // Rotation speed
    int turret_base_rotation_snd;           // Base rotation sound
    float turret_base_rotation_snd_mult;    // Sound volume multiplier
    int turret_gun_rotation_snd;            // Gun rotation sound
    float turret_gun_rotation_snd_mult;     // Gun sound volume multiplier
    
    // Audio
    int alive_snd;                          // Operational sound
    int dead_snd;                           // Destroyed sound
    int rotation_snd;                       // Movement sound
    
    // Engine wash effects
    struct engine_wash_info* engine_wash_pointer;
    
    // Animation
    float turn_rate;                        // Automatic rotation rate
    int weapon_rotation_pbank;              // Weapon-controlled rotation
    stepped_rotation_t* stepped_rotation;   // Stepped rotation configuration
    
    // AWACS
    float awacs_intensity;                  // Sensor strength
    float awacs_radius;                     // Detection range
    
    // Weapons
    int primary_banks[MAX_SHIP_PRIMARY_BANKS];      // Default primary weapons
    int primary_bank_capacity[MAX_SHIP_PRIMARY_BANKS]; // Ammo capacity
    int secondary_banks[MAX_SHIP_SECONDARY_BANKS];   // Default secondary weapons
    int secondary_bank_capacity[MAX_SHIP_SECONDARY_BANKS]; // Missile capacity
    int path_num;                           // Patrol path reference
    
    // Visual effects
    decal_system model_decal_system;        // Damage decals
    
    // Triggered animations
    int n_triggers;                         // Number of animation triggers
    queued_animation* triggers;             // Animation queue
    
    int turret_reset_delay;                 // Reset to idle timing
    int target_priority[32];                // Target type priorities
} model_subsystem;
```

### 3. ship_subsys_info Structure (ship.h:319-324)

Aggregate subsystem information by type:

```cpp
typedef struct ship_subsys_info {
    int num;                    // Total count of this subsystem type
    float total_hits;           // Combined maximum health
    float current_hits;         // Combined current health
} ship_subsys_info;
```

## Subsystem Types (model.h:51-63)

```cpp
#define SUBSYSTEM_NONE          0   // No specific type
#define SUBSYSTEM_ENGINE        1   // Propulsion systems
#define SUBSYSTEM_TURRET        2   // Weapon turrets
#define SUBSYSTEM_RADAR         3   // Sensor arrays
#define SUBSYSTEM_NAVIGATION    4   // Navigation computer
#define SUBSYSTEM_COMMUNICATION 5   // Comm systems
#define SUBSYSTEM_WEAPONS       6   // Weapon systems
#define SUBSYSTEM_SENSORS       7   // General sensors
#define SUBSYSTEM_SOLAR         8   // Solar collectors
#define SUBSYSTEM_GAS_COLLECT   9   // Gas collection
#define SUBSYSTEM_ACTIVATION    10  // Activation systems
#define SUBSYSTEM_UNKNOWN       11  // Unclassified
#define SUBSYSTEM_MAX           12  // Maximum count
```

## Subsystem Management Functions

### Core Access Functions

1. **ship_get_subsys(ship* shipp, char* subsys_name)** - Find subsystem by name
2. **ship_get_indexed_subsys(ship* sp, int index, vec3d* attacker_pos)** - Get subsystem by index
3. **ship_get_subsys_index(ship* sp, char* ss_name, int error_bypass)** - Get index by name
4. **ship_get_closest_subsys_in_sight(ship* sp, int subsys_type, vec3d* attacker_pos)** - Find nearest visible subsystem
5. **ship_get_subsystem_strength(ship* shipp, int type)** - Get aggregate strength by type

### Damage and State Management

1. **ship_subsys_disrupted(ship_subsys* ss)** - Check if subsystem is EMP'd
2. **ship_subsys_set_disrupted(ship_subsys* ss, int time)** - Apply EMP effect
3. **ship_subsys_takes_damage(ship_subsys* ss)** - Check if subsystem can be damaged
4. **do_subobj_destroyed_stuff(ship* ship_p, ship_subsys* subsys, vec3d* hitpos)** - Handle destruction

### Naming and Display

1. **ship_subsys_get_name(ship_subsys* ss)** - Get display name
2. **ship_subsys_has_instance_name(ship_subsys* ss)** - Check for custom name
3. **ship_subsys_set_name(ship_subsys* ss, char* n_name)** - Set custom name

## Damage Thresholds (subsysdamage.h)

### Engine Performance
- **SHIP_MIN_ENGINES_FOR_FULL_SPEED (0.5f)** - Below 50%, speed reduction begins
- **SHIP_MIN_ENGINES_TO_WARP (0.3f)** - Below 30%, cannot engage warp
- **ENGINE_MIN_STR (0.15f)** - Minimum contribution when damaged

### Weapon Systems
- **SUBSYS_WEAPONS_STR_FIRE_OK (0.7f)** - Above 70%, weapons always fire
- **SUBSYS_WEAPONS_STR_FIRE_FAIL (0.2f)** - Below 20%, weapons cannot fire

### Sensor Performance
- **SENSOR_STR_TARGET_NO_EFFECTS (0.3f)** - Above 30%, targeting unaffected
- **MIN_SENSOR_STR_TO_TARGET (0.2f)** - Below 20%, targeting disabled
- **SENSOR_STR_RADAR_NO_EFFECTS (0.4f)** - Above 40%, radar unaffected
- **MIN_SENSOR_STR_TO_RADAR (0.1f)** - Below 10%, radar disabled

### Communications
- **MIN_COMM_STR_TO_MESSAGE (0.3f)** - Below 30%, squadron commands disabled

### Navigation
- **SHIP_MIN_NAV_TO_WARP (0.3f)** - Below 30%, warp drive inoperative

### Shields
- **MIN_SHIELDS_FOR_FULL_STRENGTH (0.5f)** - Below 50%, shield effectiveness reduced
- **MIN_SHIELDS_FOR_FULL_COVERAGE (0.3f)** - Below 30%, shield flickers

## Subsystem Effects on Ship Performance

### Engine Damage Effects
- Speed reduction based on engine subsystem health
- Warp capability disabled if engines too damaged
- Maneuverability impact proportional to damage

### Weapon System Damage
- Weapon accuracy degradation
- Fire rate reduction
- Complete weapon failure at critical damage
- Turret rotation speed reduction

### Sensor Damage Effects
- Targeting system accuracy loss
- Radar range reduction
- Lock-on capability degradation
- Stealth detection impairment

### Shield System Damage
- Shield recharge rate reduction
- Shield strength reduction
- Shield coverage gaps (flickering)

## Turret Subsystem Management

### Targeting System
- Multi-priority target selection
- Line-of-sight verification
- Range and angle constraints
- Weapon-specific targeting logic

### Weapon Management
- Multiple weapon bank support
- Ammunition tracking
- Fire rate management
- Weapon cycling and rotation

### AI Behavior
- Autonomous target acquisition
- Firing solution calculation
- Threat assessment
- Coordination with ship AI

## Key Implementation Insights

1. **Hierarchical Damage Model**: Individual subsystems feed into aggregate ship performance
2. **Performance Scaling**: Most systems use threshold-based performance degradation
3. **State Management**: Complex state tracking for targeting, damage, and effects
4. **Modular Design**: Clear separation between static definition and runtime instance data
5. **Audio-Visual Integration**: Subsystems drive sound effects and visual damage states

## Integration with Ship Systems

### Physics Integration
- Engine damage affects thrust and maneuverability
- Subsystem damage impacts ship handling characteristics

### Weapon Integration
- Turret subsystems directly control weapon firing
- Weapon system damage affects all ship armaments

### AI Integration
- Subsystem status influences AI decision making
- Targeting priorities affected by subsystem capabilities

### Visual Integration
- Subsystem damage drives visual effects
- Model animation tied to subsystem state
- Damage decals and sparks based on subsystem health

This analysis reveals that WCS uses a sophisticated subsystem model that directly impacts ship performance, creating authentic damage states and emergent gameplay through system interdependencies.