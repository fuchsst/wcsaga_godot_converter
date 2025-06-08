# WCS Weapon Targeting and Lock-On Systems Analysis

**Date:** 2025-06-08  
**Epic:** EPIC-011 Ship Combat Systems  
**Analyst:** Larry (WCS Analyst)  
**Status:** Complete  

## Executive Summary

The Wing Commander Saga weapon targeting and lock-on systems represent a sophisticated multi-layered targeting architecture with distinct systems for player targeting, AI targeting, homing missile guidance, and turret targeting. The system integrates tightly with the HUD, physics simulation, and AI behavior systems to provide comprehensive targeting functionality.

## Core Targeting System Architecture

### 1. Player Targeting Interface (HUD Layer)

**Primary Files:**
- `source/code/hud/hudtarget.cpp` - Main player targeting interface
- `source/code/hud/hudlock.cpp` - Missile lock-on mechanics
- `source/code/hud/hudreticle.cpp` - Targeting reticle management

**Key Components:**

#### Target Selection Algorithm
```cpp
// From hudtarget.cpp:51-52
int TARGET_SHIP_IGNORE_FLAGS = (SF_EXPLODED | SF_DEPART_WARP | SF_DYING | 
                                SF_ARRIVING_STAGE_1 | SF_HIDDEN_FROM_SENSORS);
```

The player targeting system cycles through valid targets using:
- **Target cycling functions:** `hud_target_next()`, `hud_target_prev()`
- **Team filtering:** Filters targets by team affiliation masks
- **Range validation:** Eliminates targets beyond sensor range
- **Status filtering:** Ignores destroyed, warping, or hidden ships

#### Subsystem Targeting
- **Function:** `hud_target_subobject_common()`
- **Navigation:** `hud_target_next_subobject()`, `hud_target_prev_subobject()`
- **Integration:** Tight coupling with subsystem damage and shield systems

#### Hotkey Target Management
- **Storage:** Up to 10 hotkey target groups (0-9)
- **Functions:** `hud_target_hotkey_add_remove()`, `hud_target_hotkey_select()`
- **Persistence:** Hotkey assignments persist across target changes

### 2. Missile Lock-On System

**Primary File:** `source/code/hud/hudlock.cpp`

#### Aspect Lock Mechanics
The lock-on system implements sophisticated aspect-based targeting:

```cpp
// Lock parameters from hudlock.cpp:40-48
static float Lock_start_dist;
int Lock_target_box_width[GR_NUM_RESOLUTIONS] = {19, 30};
int Lock_target_box_height[GR_NUM_RESOLUTIONS] = {19, 30};
```

**Lock Acquisition Process:**
1. **Initial Detection:** Target must be within reticle area
2. **Lock Timing:** Minimum lock time based on weapon type (`min_lock_time`)
3. **Movement Tolerance:** Lock broken if target moves too fast (`lock_pixels_per_sec`)
4. **Aspect Validation:** Maintains lock based on relative facing angle

#### Lock State Management
- **Lock Indicator:** Visual feedback system with rotating triangles
- **Audio Cues:** Distinct sounds for lock acquisition and missile tracking
- **Range Validation:** Continuous range checking during lock process

### 3. Weapon Homing and Guidance

**Primary File:** `source/code/weapon/weapons.cpp`

#### Homing Algorithm Core
The weapon homing system provides multiple guidance modes:

```cpp
// From weapon_home() function
void weapon_home(object* obj, int num, float frame_time)
{
    weapon* wp = &Weapons[num];
    weapon_info* wip = &Weapon_info[wp->weapon_info_index];
    object* hobjp = Weapons[num].homing_object;
    
    // Free flight time before homing activates
    if (f2fl(Missiontime - wp->creation_time) < wip->free_flight_time)
        return;
}
```

#### Homing Types

**Heat-Seeking (WIF_HOMING_HEAT):**
- Targets engine signatures and heat sources
- Can retarget during flight if original target lost
- Vulnerable to countermeasures

**Aspect Lock (WIF_LOCKED_HOMING):**
- Locks onto specific target signature at launch
- Cannot retarget once fired
- More reliable against countermeasures

**Javelin Heat-Seeking (WIF_HOMING_JAVELIN):**
- Specialized anti-ship homing
- Specifically targets engine subsystems
- Advanced guidance algorithms

#### Target Validation
```cpp
// Aspect lock validation
if (wp->target_sig > 0) {
    if (wp->homing_object->signature != wp->target_sig) {
        wp->homing_object = &obj_used_list;  // Lose lock
        return;
    }
}
```

### 4. AI Targeting System

**Primary Files:**
- `source/code/ai/aicode.cpp` - Core AI targeting logic
- `source/code/ai/ai.h` - AI structures and definitions

#### AI Target Priority System
The AI uses a sophisticated priority-based targeting system:

**Target Evaluation Factors:**
- **Threat Level:** Based on weapon loadout and ship class
- **Range:** Distance-based priority scaling
- **Angle:** Firing solution viability
- **Target Health:** Preference for damaged targets
- **Mission Priority:** Goal-specific target weighting

#### AI Accuracy System
```cpp
// From aicode.cpp - AI accuracy affects targeting
if (time_enemy_in_range < range_time) {
    // Apply accuracy modifiers based on skill level and time in range
    scale = (1.0f - aip->ai_accuracy) * 4.0f * 
            (1.0f + 4.0f * (1.0f - time_enemy_in_range / (2 * range_time)));
}
```

**Skill-Based Targeting:**
- **Accuracy modifiers** affect leading calculations
- **Time-in-range** improves accuracy over time
- **Weapon-specific** targeting behaviors

### 5. Turret Targeting System

**Primary File:** `source/code/ai/aiturret.cpp`

#### Turret Target Evaluation
```cpp
// Turret evaluation structure
typedef struct eval_enemy_obj_struct {
    int turret_parent_objnum;           // parent of turret
    float weapon_travel_dist;           // max targeting range
    int enemy_team_mask;
    bool big_only_flag;                 // turret fires only at big ships
    bool small_only_flag;               // turret fires only at small ships
    bool tagged_only_flag;              // turret fires only at tagged ships
    bool beam_flag;                     // turret is a beam weapon
    // ... additional targeting parameters
} eval_enemy_obj_struct;
```

#### Turret Targeting Priorities
1. **Bombs:** Highest priority threat assessment
2. **Ships:** Based on ship class and threat level
3. **Asteroids:** Environmental targets

#### Field of View Validation
```cpp
// From aiturret.cpp
int object_in_turret_fov(object* objp, ship_subsys* ss, vec3d* tvec, 
                        vec3d* tpos, float dist)
{
    vec3d v2e;
    float size_mod;
    
    vm_vec_normalized_dir(&v2e, &objp->pos, tpos);
    size_mod = objp->radius / (dist + objp->radius);
    // FOV calculation continues...
}
```

## Leading and Interception Calculations

### Projectile Leading System
WCS implements sophisticated leading calculations for projectile weapons:

**Leading Calculation Factors:**
- **Target velocity** and predicted position
- **Projectile flight time** based on distance and weapon speed
- **Target acceleration** for advanced prediction
- **Evasion patterns** learned by AI over time

### Turret Tracking Behavior
- **Smooth tracking** with realistic angular velocity limits
- **Predictive aiming** for moving targets
- **Range compensation** for ballistic weapons
- **Convergence zones** for multiple turret coordination

## Range and Line-of-Sight Validation

### Sensor Range Limits
```cpp
// Target visibility based on sensor capabilities
if (hud_target_invalid_awacs(objp)) {
    // Target beyond sensor range or blocked
    continue;  // Skip to next target
}
```

### Line-of-Sight Checking
- **Obstacle detection** using ray casting
- **Nebula interference** affecting sensor range
- **Stealth detection** with limited visibility
- **AWACS enhancement** extending sensor coverage

### Range-Based Targeting
- **Weapon-specific ranges** limit engagement distance
- **Optimal engagement zones** for different weapon types
- **Falloff calculations** for accuracy at range

## Integration Points for Godot Conversion

### 1. Node-Based Target Management
**Godot Approach:**
- `TargetingSystem` node managing all targeting logic
- `TargetableObject` interface for valid targets
- Signal-based communication for target state changes

### 2. Physics Integration
**Required Components:**
- Godot's `RayCast3D` for line-of-sight validation
- `Area3D` for proximity detection and sensor ranges
- Custom physics queries for projectile leading calculations

### 3. AI Behavior Trees
**LimboAI Integration:**
- Target selection as behavior tree actions
- Priority evaluation through custom nodes
- Dynamic retargeting based on situation changes

### 4. HUD Integration
**Godot UI System:**
- `Control` nodes for targeting displays
- Custom shaders for lock-on effects
- Audio integration for targeting feedback

## Critical Implementation Considerations

### 1. Performance Optimization
- **Spatial partitioning** for efficient target queries
- **Update frequency scaling** based on importance
- **Level-of-detail** for distant target processing

### 2. Network Synchronization
- **Target state synchronization** in multiplayer
- **Lock-on state** network messages
- **Homing missile** trajectory synchronization

### 3. Accessibility and Feedback
- **Clear visual indicators** for targeting states
- **Audio cues** for lock acquisition and loss
- **Colorblind-friendly** targeting displays

## Conversion Priorities

### High Priority (Core Functionality)
1. **Basic target cycling** and selection
2. **Missile lock-on mechanics**
3. **Homing weapon guidance**
4. **Line-of-sight validation**

### Medium Priority (AI Enhancement)
1. **AI target priority system**
2. **Turret targeting behavior**
3. **Leading calculations**
4. **Range-based accuracy**

### Low Priority (Polish)
1. **Advanced evasion prediction**
2. **Dynamic target prioritization**
3. **Sophisticated counter-targeting**
4. **Multi-target engagement**

## Conclusion

The WCS targeting system represents a mature, feature-rich implementation that balances realism with gameplay. The modular design separates concerns between player interface, AI behavior, weapon guidance, and validation systems. 

For the Godot conversion, the challenge will be maintaining the sophisticated targeting behavior while leveraging Godot's node system and built-in physics capabilities. The signal-based architecture of Godot should actually improve the loose coupling between targeting components.

The system's complexity requires careful attention to performance optimization and clear separation of concerns to maintain the responsive, accurate targeting that defines the WCS combat experience.