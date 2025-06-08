# WCS Shield and Energy Systems Analysis

**Date**: 2025-06-08  
**Analyst**: Larry (WCS Analyst)  
**Epic**: EPIC-011-ship-combat-systems  
**Source Files Analyzed**:
- `/source/code/hud/hudets.cpp` - ETS management and UI
- `/source/code/ship/ship.cpp` - Ship processing and power integration
- `/source/code/object/objectshield.cpp` - Shield mechanics and regeneration
- `/source/code/ship/afterburner.cpp` - Afterburner power consumption
- `/source/code/weapon/emp.cpp` - EMP effects and power disruption
- `/source/code/ship/subsysdamage.h` - Subsystem damage thresholds

## Executive Summary

The WCS power management system is a sophisticated tri-system energy distribution network that governs ship performance through dynamic power allocation between engines, shields, and weapons. The Energy Transfer System (ETS) allows both players and AI to redistribute power in real-time, creating tactical depth through resource management trade-offs. This analysis reveals the core algorithms and mechanics required for authentic power management in the Godot conversion.

## 1. Energy Transfer System (ETS) Core Mechanics

### 1.1 Energy Distribution Architecture

**Power Allocation Indices**:
```cpp
// 13 discrete power levels (0-12 indices)
float Energy_levels[NUM_ENERGY_LEVELS] = {
    0.0f,     // 0  - No power
    0.0833f,  // 1  - 8.33%
    0.167f,   // 2  - 16.7%
    0.25f,    // 3  - 25%
    0.333f,   // 4  - 33.3% (Default)
    0.417f,   // 5  - 41.7%
    0.5f,     // 6  - 50%
    0.583f,   // 7  - 58.3%
    0.667f,   // 8  - 66.7%
    0.75f,    // 9  - 75%
    0.833f,   // 10 - 83.3%
    0.9167f,  // 11 - 91.67%
    1.0f      // 12 - Maximum (100%)
};
```

**Default Configuration**:
- Initial Shield Recharge Index: 4 (33.3%)
- Initial Weapon Recharge Index: 4 (33.3%)
- Initial Engine Recharge Index: 4 (33.3%)
- Total: 99.9% (allows for slight power reserve)

### 1.2 Power Transfer Algorithms

**Zero-Sum Power Distribution**:
When decreasing power to one system, the energy is redistributed to the other two systems using priority-based allocation:

```cpp
void decrease_recharge_rate(object* obj, SYSTEM_TYPE ship_system)
{
    // 1. Identify losing system and gaining systems
    // 2. Check available energy to transfer (minimum 2 units)
    // 3. Prioritize gains based on current need (lowest index first)
    // 4. Distribute energy while respecting MAX_ENERGY_INDEX limits
    
    int count = MIN(2, *lose_index);
    *lose_index -= count;
    
    // Smart distribution: fill lowest system first
    while (count > 0) {
        if (gain_index1 && *gain_index1 < MAX_ENERGY_INDEX) {
            *gain_index1 += 1;
            count--;
        }
        if (count > 0 && gain_index2 && *gain_index2 < MAX_ENERGY_INDEX) {
            *gain_index2 += 1;
            count--;
        }
    }
}
```

**Direct Energy Transfer**:
The system also supports direct shield-to-weapon and weapon-to-shield transfers:

```cpp
#define ENERGY_DIVERT_DELTA 0.2f  // 20% transfer per operation

// Transfers 20% of source energy to destination
delta = from_field * ENERGY_DIVERT_DELTA * scale;
*to_delta += delta;
*from_delta -= delta;
```

## 2. Shield Regeneration System

### 2.1 Core Regeneration Algorithm

**Frame-Based Regeneration**:
```cpp
void update_ets(object* objp, float fl_frametime)
{
    // Calculate maximum possible shield regeneration this frame
    max_new_shield_energy = fl_frametime * 
                           sinfo_p->max_shield_regen_per_second * 
                           max_shield_strength;
    
    // Apply ETS scaling and skill level modifiers
    if (objp->flags & OF_PLAYER_SHIP) {
        shield_delta = Energy_levels[ship_p->shield_recharge_index] * 
                      max_new_shield_energy * 
                      mission_ai_profile->shield_energy_scale[Game_skill_level];
    } else {
        shield_delta = Energy_levels[ship_p->shield_recharge_index] * 
                      max_new_shield_energy;
    }
    
    shield_add_strength(objp, shield_delta);
}
```

### 2.2 Smart Shield Management

**AI Priority Repair System**:
```cpp
// AIPF_SMART_SHIELD_MANAGEMENT flag enables intelligent quadrant repair
while (delta > 0.0f) {
    // Find weakest shield quadrant
    for (int i = 0; i < MAX_SHIELD_SECTIONS; i++) {
        float quad = shield_get_quad(objp, i);
        if (quad < weakest) {
            weakest = quad;
            weakest_idx = i;
        }
    }
    
    // Focus all available power on weakest quadrant
    float xfer_amount = MIN(delta, section_max - weakest);
    shield_add_quad(objp, weakest_idx, xfer_amount);
    delta -= xfer_amount;
}
```

**Quadrant-Based Architecture**:
- 4 shield sections (MAX_SHIELD_SECTIONS = 4)
- Each quadrant can be independently damaged and repaired
- Equal distribution for non-AI ships
- Smart repair prioritizes damaged sections for AI ships

### 2.3 Shield Generator Subsystem Effects

**Performance Scaling**:
```cpp
// Shield effectiveness based on generator health
float generator_fraction = subsystem_current_hits / subsystem_total_hits;

if (generator_fraction > 0.5f) {
    // Full effectiveness above 50%
    return objp->shield_quadrant[quadrant_num];
} else if (generator_fraction > 0.3f) {
    // Logarithmic scaling between 30-50%
    return scale_quad(generator_fraction, shield_strength);
} else {
    // Random flickering below 30%
    float rand_chance = sqrt(generator_fraction);
    if (random() < rand_chance) {
        return scale_quad(generator_fraction, shield_strength);
    } else {
        return 0.0f;  // Shield flickers off
    }
}
```

## 3. Weapon Energy Management

### 3.1 Energy Consumption Model

**Regeneration Algorithm**:
```cpp
max_new_weapon_energy = fl_frametime * 
                       sinfo_p->max_weapon_regen_per_second * 
                       max_weapon_reserve;

weapon_energy += Energy_levels[weapon_recharge_index] * 
                max_new_weapon_energy * 
                skill_level_modifier;

// Clamp to maximum
if (weapon_energy > max_weapon_reserve) {
    weapon_energy = max_weapon_reserve;
}
```

**Key Parameters**:
- `max_weapon_regen_per_second`: Base regeneration rate per ship class
- `max_weapon_reserve`: Maximum weapon energy capacity
- `weapon_recharge_index`: ETS allocation level (0-12)
- Skill level modifiers affect player regeneration rates

### 3.2 Weapon Firing Constraints

**Subsystem Damage Effects** (from `subsysdamage.h`):
```cpp
#define SUBSYS_WEAPONS_STR_FIRE_OK    0.7f  // 70%+ strength: normal firing
#define SUBSYS_WEAPONS_STR_FIRE_FAIL  0.2f  // <20% strength: weapons offline
```

Between 20-70% weapon subsystem strength, firing becomes probabilistic based on damage level.

## 4. Engine Power and Performance

### 4.1 Speed Calculation Algorithm

**Dynamic Speed Scaling**:
```cpp
float y = Energy_levels[engine_recharge_index];

if (y < Energy_levels[INITIAL_ENGINE_INDEX]) {
    // Below default: linear scale from 50% to 100% base speed
    current_max_speed = 0.5f * max_speed + 
                       (y - Energy_levels[0]) * 
                       (max_speed - 0.5f * max_speed) / 
                       (Energy_levels[INITIAL_INDEX] - Energy_levels[0]);
} else {
    // Above default: linear scale from 100% to overclocked speed
    current_max_speed = max_speed + 
                       (y - Energy_levels[INITIAL_INDEX]) * 
                       (max_overclocked_speed - max_speed) / 
                       (Energy_levels[MAX_INDEX] - Energy_levels[INITIAL_INDEX]);
}
```

**Subsystem Damage Integration**:
```cpp
#define SHIP_MIN_ENGINES_FOR_FULL_SPEED 0.5f

float strength = ship_get_subsystem_strength(ship, SUBSYSTEM_ENGINE);
if (strength < SHIP_MIN_ENGINES_FOR_FULL_SPEED) {
    current_max_speed *= sqrt(strength);
}
```

### 4.2 Engine Power Allocation Effects

**Power Level Mapping**:
- Index 0 (0%): 50% maximum speed
- Index 4 (33.3%): 100% base speed (default)
- Index 12 (100%): Maximum overclocked speed
- Linear interpolation between these points

## 5. Afterburner System

### 5.1 Fuel Consumption Model

**Minimum Fuel Requirements**:
```cpp
#define MIN_AFTERBURNER_FUEL_TO_ENGAGE 10  // Minimum fuel to start
```

**Consumption Rate**:
- Fuel depletes over time during afterburner use
- Rate varies by ship class (`afterburner_fuel_capacity`)
- No direct power system integration (uses separate fuel reservoir)

### 5.2 Afterburner Constraints

**Engine Subsystem Dependency**:
Afterburners require functional engines and are affected by:
- Engine subsystem damage
- Power allocation to engines
- Ship-specific afterburner capabilities (`SIF_AFTERBURNER` flag)

## 6. EMP Effects and Power Disruption

### 6.1 EMP Intensity System

**Disruption Mechanics**:
```cpp
float Emp_intensity = -1.0f;    // Current EMP effect strength
float Emp_decr = 0.0f;          // Decay rate per second

#define MAX_TURRET_DISRUPT_TIME 7500  // Maximum turret offline time (ms)
```

**System Effects**:
- Weapons systems: Firing disruption and targeting interference
- Shields: Regeneration penalties and random failures
- Engines: Power fluctuations and control instability
- HUD: Display corruption and targeting errors

### 6.2 EMP Recovery Timeline

**Progressive Recovery**:
EMP effects decay over time, with systems gradually returning to normal operation. The intensity decreases linearly, allowing partial functionality before complete recovery.

## 7. AI Power Management

### 7.1 Automated ETS Logic

**AI Decision Constants**:
```cpp
#define SHIELDS_MIN_LEVEL_PERCENT   0.3f   // 30% minimum
#define WEAPONS_MIN_LEVEL_PERCENT   0.3f   // 30% minimum
#define SHIELDS_MAX_LEVEL_PERCENT   0.8f   // 80% maximum
#define WEAPONS_MAX_LEVEL_PERCENT   0.8f   // 80% maximum
#define SHIELDS_EMERG_LEVEL_PERCENT 0.10f  // 10% emergency
#define WEAPONS_EMERG_LEVEL_PERCENT 0.05f  // 5% emergency
#define MIN_ENGINE_RECHARGE_INDEX   3      // Prevent engine power elimination
```

### 7.2 AI ETS Algorithm

**Priority System**:
```cpp
void ai_manage_ets(object* obj) {
    float shield_percent = get_shield_pct(obj);
    float weapon_percent = weapon_energy / max_weapon_reserve;
    
    // 1. Maximum level check: reduce power if at 100%
    if (weapon_percent == 1.0f) decrease_recharge_rate(obj, WEAPONS);
    if (shield_percent == 1.0f) decrease_recharge_rate(obj, SHIELDS);
    
    // 2. Minimum level check: increase power if too low
    if (shield_percent < SHIELDS_MIN_LEVEL_PERCENT) {
        if (weapon_percent > WEAPONS_MIN_LEVEL_PERCENT) {
            // Transfer from weapons to shields
        }
    }
    
    // 3. Emergency protocols for critical situations
    // 4. Combat situation adjustments
    // 5. Efficiency optimizations
}
```

**Update Frequency**:
- AI manages ETS every 500ms (`AI_MODIFY_ETS_INTERVAL`)
- Players can adjust ETS instantaneously
- Changes are subject to system constraints and damage effects

## 8. Player ETS Controls and Interface

### 8.1 Input Mapping

**Control Scheme**:
- Increase/Decrease Shield Power
- Increase/Decrease Weapon Power  
- Increase/Decrease Engine Power
- Shield-to-Weapon Transfer
- Weapon-to-Shield Transfer
- Reset to Default Distribution

### 8.2 Audio Feedback

**Sound Effects**:
- `SND_ENERGY_TRANS`: Successful power transfer
- `SND_ENERGY_TRANS_FAIL`: Failed transfer attempt
- Volume and 3D positioning for non-player ships

### 8.3 Visual Indicators

**HUD Elements**:
- Three-bar ETS display (G/S/A or E/S/W)
- Numerical percentages for each system
- Color coding for power levels
- Real-time energy level indicators

## 9. Integration Points and Dependencies

### 9.1 Ship Configuration Dependencies

**Required Ship Data**:
```cpp
ship_info {
    float max_weapon_reserve;           // Maximum weapon energy
    float max_weapon_regen_per_second;  // Base weapon regen rate
    float max_shield_regen_per_second;  // Base shield regen rate
    float max_speed;                    // Base maximum speed
    float max_overclocked_speed;        // Overclocked maximum speed
    int power_output;                   // Base power generation
}
```

### 9.2 Mission and Skill Integration

**Difficulty Scaling**:
- Player regeneration rates affected by skill level
- AI behavior constants remain fixed
- Mission-specific power modifiers supported

### 9.3 Subsystem Integration

**Damage Model Integration**:
- Engine damage affects maximum speed
- Weapon subsystem damage affects firing capability
- Shield generator damage affects shield effectiveness
- Communication and sensor damage (separate from power)

## 10. Godot Conversion Recommendations

### 10.1 Core Architecture

**Godot Implementation Strategy**:

1. **PowerManager Component**: Central authority for ship power systems
2. **ETSController**: Handle player input and AI power management
3. **ShieldSystem**: Manage quadrant-based shield regeneration
4. **WeaponEnergySystem**: Handle weapon power and firing constraints
5. **EngineSystem**: Calculate speed based on power allocation

### 10.2 GDScript Structure

**Component Hierarchy**:
```gdscript
class_name ShipPowerManager
extends Node

@export var max_weapon_energy: float = 100.0
@export var max_shield_strength: float = 100.0
@export var base_max_speed: float = 50.0
@export var overclocked_max_speed: float = 75.0

var shield_recharge_index: int = 4
var weapon_recharge_index: int = 4
var engine_recharge_index: int = 4

signal power_levels_changed(shields: float, weapons: float, engines: float)
signal energy_transfer_attempted(success: bool)
```

### 10.3 Performance Considerations

**Frame-Based Updates**:
- Use `_process(delta)` for continuous regeneration
- Cache energy level calculations
- Implement efficient quadrant management for shields
- Use signals for UI updates to minimize coupling

### 10.4 Authenticity Preservation

**Critical Mechanics to Preserve**:
1. 13-level discrete power allocation system
2. Zero-sum power distribution with 2-unit minimum transfers
3. Smart shield repair prioritization for AI
4. Logarithmic shield scaling with subsystem damage
5. Linear speed interpolation with overclocking
6. EMP effect system with progressive recovery
7. AI power management with situation-aware priorities

### 10.5 Testing Strategy

**Key Test Scenarios**:
1. Power transfer accuracy and constraints
2. Shield regeneration under various damage states
3. Speed calculations with different power levels
4. AI ETS decision making in combat scenarios
5. EMP effect duration and recovery curves
6. Subsystem damage integration across all systems

## Conclusion

The WCS power management system represents a sophisticated balance of tactical depth and simulation authenticity. The tri-system energy distribution creates meaningful player choices while maintaining realistic constraints. The Godot conversion must preserve the discrete power level system, frame-based regeneration algorithms, and intelligent AI power management to maintain the authentic WCS experience.

The system's complexity lies not in individual calculations but in the interconnected relationships between power allocation, subsystem damage, environmental effects, and AI decision-making. Successful conversion requires careful attention to these integration points while leveraging Godot's component system for clean, maintainable code architecture.

**Key Success Metrics**:
- Accurate power transfer calculations matching WCS behavior
- Smooth shield regeneration with proper quadrant prioritization  
- Realistic speed/power relationships including overclocking
- Intelligent AI power management that responds to combat situations
- Proper EMP and subsystem damage integration
- Responsive player controls with appropriate audio/visual feedback

This analysis provides the foundation for implementing an authentic and engaging power management system that preserves the tactical depth and feel of the original WCS combat experience.