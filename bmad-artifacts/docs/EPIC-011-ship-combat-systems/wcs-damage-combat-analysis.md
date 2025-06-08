# WCS Damage Processing and Combat Mechanics Analysis

**Analysis Date:** 2025-06-08  
**Analyst:** Larry (WCS Analyst)  
**Epic:** EPIC-011-ship-combat-systems  

## Executive Summary

This analysis examines the WCS damage processing and combat mechanics system, one of the most complex and critical components of the Wing Commander Saga gameplay experience. The system features sophisticated multi-layered damage processing, realistic shield quadrant mechanics, comprehensive subsystem functionality tracking, and advanced armor/resistance calculations.

## System Overview

The WCS damage system is architected as a layered damage processing pipeline that handles multiple types of incoming damage sources (weapons, beams, shockwaves, collisions) and applies them through:

1. **Damage Source Classification & Scaling**
2. **Shield Quadrant Processing & Armor**
3. **Subsystem Hit Detection & Damage Distribution**
4. **Hull Armor Processing**
5. **Death Sequence & Visual Effects**

## Core Damage Processing Architecture

### 1. Primary Damage Entry Points

The system provides two main damage application interfaces:

#### `ship_apply_local_damage()` - Point-Specific Damage
```cpp
void ship_apply_local_damage(object* ship_obj, object* other_obj, vec3d* hitpos, 
                             float damage, int quadrant, bool create_spark=true, 
                             int submodel_num=-1, vec3d* hit_normal=NULL)
```

**Purpose:** Applies damage at a specific hit location with known shield quadrant  
**Used For:** Direct weapon hits, beam weapons, collision impacts  
**Key Features:**
- Precise hit location tracking
- Spark generation for visual feedback
- Submodel-specific damage application
- Team-based friendly fire prevention

#### `ship_apply_global_damage()` - Area/Directional Damage
```cpp
void ship_apply_global_damage(object* ship_obj, object* other_obj, 
                              vec3d* force_center, float damage)
```

**Purpose:** Applies damage from a directional force or area effect  
**Used For:** Shockwaves, explosions, area-of-effect weapons  
**Key Features:**
- Automatic shield quadrant calculation
- Force center-based damage direction
- Distributed damage across all quadrants if no center specified

### 2. Core Damage Processing Function

All damage flows through the central `ship_do_damage()` function:

#### Damage Processing Pipeline:
1. **Damage Source Analysis** - Identifies weapon/beam/shockwave/collision type
2. **Skill Level Scaling** - Applies difficulty modifiers for player ships
3. **Shield Processing** - Applies shield armor, piercing, and absorption
4. **Subsystem Processing** - Calculates subsystem hit detection and damage
5. **Hull Processing** - Applies hull armor and final damage
6. **Death Processing** - Handles ship destruction sequences

## Shield System Mechanics

### Shield Quadrant System

WCS uses a 4-quadrant shield system:
- **FRONT_QUAD (1)** - Forward-facing shield
- **REAR_QUAD (2)** - Aft-facing shield  
- **LEFT_QUAD (3)** - Port-side shield
- **RIGHT_QUAD (0)** - Starboard-side shield

### Shield Damage Processing

#### Key Function: `shield_apply_damage()`
```cpp
float shield_apply_damage(object* objp, int quadrant_num, float damage)
{
    float remaining_damage = damage - shield_get_quad(objp, quadrant_num);
    if (remaining_damage > 0.0f) {
        shield_set_quad(objp, quadrant_num, 0.0f);
        return remaining_damage;  // Penetrates to hull
    } else {
        shield_add_quad(objp, quadrant_num, -damage);
        return 0.0f;  // Fully absorbed
    }
}
```

#### Shield Features:
- **Quadrant-Based Absorption** - Each quadrant absorbs damage independently
- **Overflow Damage** - Excess damage penetrates to hull and subsystems
- **Shield Factors** - Weapons have shield-specific damage multipliers
- **Smart Recharge** - AI ships prioritize weakest quadrants for repair
- **Shield Armor** - Separate armor type for shield resistance calculations

### Shield State Management

#### Shield Strength Tracking:
- Individual quadrant strength values (0.0 to max_strength)
- Total shield strength calculation across all quadrants
- Maximum shield strength per ship class
- Generator subsystem affects shield effectiveness

#### Shield Regeneration:
- Continuous shield recharge during non-combat periods
- Smart AI shield management prioritizes damaged quadrants
- Shield generator subsystem damage affects recharge rate

## Subsystem Damage System

### Subsystem Hit Detection

The `do_subobj_hit_stuff()` function implements sophisticated subsystem damage:

#### Distance-Based Damage Distribution:
- **0 → 0.5 radius:** 100% subsystem, 0% hull
- **0.5 → 1.0 radius:** 50% subsystem, 50% hull  
- **1.0 → 2.0 radius:** 25% subsystem, 75% hull
- **> 2.0 radius:** 0% subsystem, 100% hull

#### Subsystem Types & Effects:
- **Engines:** Affect speed, maneuverability, and warp capability
- **Weapons:** Control firing rate, accuracy, and availability
- **Sensors:** Impact targeting, radar range, and lock-on time
- **Communications:** Affect wingman commands and messaging
- **Navigation:** Required for warp drive engagement
- **Shields:** Control shield strength and recharge rate

### Subsystem Functionality Degradation

#### Engine System:
```cpp
#define SHIP_MIN_ENGINES_FOR_FULL_SPEED    0.5f  // Below 50% = speed reduction
#define SHIP_MIN_ENGINES_TO_WARP          0.3f  // Below 30% = no warp
#define ENGINE_MIN_STR                    0.15f // Minimum contribution
```

#### Weapon Systems:
```cpp
#define SUBSYS_WEAPONS_STR_FIRE_OK        0.7f  // 70%+ = normal firing
#define SUBSYS_WEAPONS_STR_FIRE_FAIL      0.2f  // <20% = no firing
```

#### Sensor Systems:
```cpp
#define SENSOR_STR_TARGET_NO_EFFECTS      0.3f  // 30%+ = normal targeting
#define MIN_SENSOR_STR_TO_TARGET          0.2f  // <20% = no targeting
#define SENSOR_STR_RADAR_NO_EFFECTS       0.4f  // 40%+ = normal radar
#define MIN_SENSOR_STR_TO_RADAR           0.1f  // <10% = no radar
```

### Subsystem Destruction Effects

When subsystems reach 0 health:
1. **Visual Effects** - Explosion particles and debris
2. **Functional Loss** - Complete system shutdown
3. **Secondary Effects** - May trigger chain reactions
4. **Repair Prevention** - Cannot be repaired until mission end

## Armor and Resistance System

### Armor Type Processing

WCS implements a sophisticated armor system with type-based damage resistance:

#### Armor Application Points:
1. **Shield Armor** - Applied to shield damage before absorption
2. **Hull Armor** - Applied to hull damage after shield penetration  
3. **Subsystem Armor** - Applied to individual subsystem components

#### Damage Type Resistance:
- Each armor type has resistance values against specific damage types
- Weapons, beams, shockwaves, collisions have different damage type indices
- `Armor_types[armor_idx].GetDamage(damage, dmg_type_idx)` calculates final damage

### Weapon-Specific Modifiers

#### Special Weapon Effects:
- **Puncture Weapons** - Damage reduced to 25% against armor (`damage /= 4`)
- **Armor Factor** - Each weapon has an `armor_factor` multiplier
- **Shield Factor** - Separate multiplier for shield damage
- **Piercing Percentage** - Some damage bypasses shields entirely

## Combat State Management

### Ship Vulnerability States

#### Invulnerability Conditions:
- Ships with `OF_INVULNERABLE` flag take no damage
- Player ships during warp-out sequences (PCM_WARPOUT_STAGE2+)
- Ships in arrival sequence (`SF_ARRIVING`)

#### Guardian System:
```cpp
if (shipp->ship_guardian_threshold > 0) {
    float min_hull_strength = 0.01f * shipp->ship_guardian_threshold * shipp->ship_max_hull_strength;
    if ((ship_obj->hull_strength - damage) < min_hull_strength) {
        damage = ship_obj->hull_strength - min_hull_strength;
        damage = MAX(0, damage);
    }
}
```

### Death Sequence Processing

#### Death State Management:
1. **Dying Flag** - `SF_DYING` prevents further damage processing
2. **Death Roll** - Extended destruction sequence for large ships
3. **Deathroll Acceleration** - Excessive damage shortens death animation
4. **Player Pain** - Visual feedback system for player damage

#### Death Sequence Features:
- Large ships (radius > `BIG_SHIP_MIN_RADIUS`) have extended death rolls
- Damage-based death roll shortening for dramatic effect
- Mission log entries for ship destruction
- Multiplayer synchronization of death events

## Collision Damage Mechanics

### Ship-to-Ship Collisions

Collision damage is processed through the same pipeline with:
- Collision-specific damage types
- Mass-based damage calculation
- Relative velocity impact scaling
- Both ships take damage proportional to impact

### Ship-to-Weapon Collisions

Handled by `ship_weapon_do_hit_stuff()`:
1. **Weapon Hit Processing** - `weapon_hit()` handles weapon destruction
2. **Damage Application** - `ship_apply_local_damage()` with weapon damage
3. **Physics Force** - Momentum transfer based on weapon mass and velocity
4. **Visual Effects** - Sparks, decals, and impact effects

## Beam Weapon Damage Processing

### Continuous Beam Damage

Beam weapons use a unique damage application system:
- **Damage Over Time** - Applied in intervals during beam contact
- **Multiple Hit Points** - Beams can hit multiple subsystems simultaneously  
- **Area Effect** - Wide beams affect larger ship areas
- **Collision Tracking** - Maintains collision state between beam and target

### Beam-Specific Features:
- Damage timestamp tracking to prevent excessive damage application
- Multiple collision points along beam path
- Special handling for beam weapon armor factors
- Integration with standard damage pipeline

## Performance and Optimization

### Damage Processing Optimizations:

1. **Collision Caching** - Hit detection results cached between frames
2. **Distance Culling** - Far objects skip detailed collision checks
3. **Damage Batching** - Multiple hits processed in single frame update
4. **Subsystem Culling** - Only nearby subsystems checked for hits

### Multiplayer Considerations:

- **Client-Server Damage** - Only server processes final damage calculations
- **Damage Packets** - Synchronize damage events across clients  
- **Hit Validation** - Prevent client-side damage exploitation
- **Player Pain Packets** - Separate system for player damage feedback

## Key Source Files Analysis

### Primary Files:
- **`ship/shiphit.cpp`** (2,800+ lines) - Core damage processing engine
- **`ship/shiphit.h`** - Damage application interface definitions
- **`object/objectshield.cpp`** - Shield quadrant management system
- **`object/objectshield.h`** - Shield system interface
- **`ship/subsysdamage.h`** - Subsystem functionality thresholds

### Supporting Files:
- **`object/collideshipweapon.cpp`** - Weapon collision detection and handling
- **`weapon/beam.cpp`** - Beam weapon damage application
- **`weapon/weapons.cpp`** - Weapon damage configuration and scaling
- **`ship/shipfx.cpp`** - Combat visual effects and feedback

## Godot Conversion Implications

### Critical Systems for Authentic Combat:

1. **Layered Damage Pipeline** - Must preserve shield→subsystem→hull progression
2. **Quadrant-Based Shields** - Essential for tactical combat positioning
3. **Subsystem Functionality** - Damage must affect ship capabilities realistically
4. **Armor Resistance** - Type-based damage resistance for weapon variety
5. **Death Sequences** - Dramatic ship destruction with proper timing

### Godot Implementation Considerations:

- **Node-Based Architecture** - Damage components as separate nodes
- **Signal-Based Communication** - Damage events propagated via signals
- **Resource-Based Configuration** - Armor types, weapon configs as resources
- **Physics Integration** - Collision detection through Godot physics
- **Visual Effects** - Particle systems for explosions, sparks, debris

### Performance Targets:

- Process damage for 50+ ships simultaneously
- Maintain 60 FPS during intense combat scenarios
- Support multiplayer damage synchronization
- Provide responsive visual feedback for all damage types

This analysis provides the foundation for implementing an authentic WCS combat experience in Godot while leveraging the engine's strengths for modern performance and maintainability.