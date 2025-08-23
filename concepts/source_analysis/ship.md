# Ship System Analysis

## Purpose
The ship system manages all aspects of spacecraft entities in FreeSpace, including ship classes, subsystems, weapons, physics properties, and gameplay characteristics. It handles ship creation, destruction, damage modeling, and all ship-specific behaviors.

## Main Public Interfaces
- `ship_info` - Structure defining ship class properties (weapons, physics, appearance)
- `ship` - Structure representing individual ship instances
- `ship_subsys` - Structure for ship subsystems (engines, weapons, sensors, etc.)
- `ship_create()` - Creates a new ship instance
- `ship_process_pre()` / `ship_process_post()` - Per-frame ship processing
- `ship_delete()` - Removes a ship from the game
- `ship_get_SIF()` - Gets ship class flags
- `ship_info_lookup()` - Finds ship class by name
- `ship_recalc_subsys_strength()` - Recalculates subsystem integrity
- `ship_do_rearm_frame()` - Handles rearm/reload logic

## Key Components
- **Ship Classes**: Defined in `ship_info` with hull strength, weapons, physics characteristics
- **Subsystems**: Damageable components like engines, weapons, sensors with individual health
- **Weapon Management**: Primary/secondary weapon banks with ammo tracking
- **Damage Modeling**: Hull and shield damage with subsystem-specific effects
- **Physics Integration**: Mass, moment of inertia, and physics properties
- **Visual Effects**: Thrusters, afterburners, contrails, and special effects
- **Death Handling**: Multiple death stages with explosions and debris
- **Docking Support**: Ship docking and departure mechanics

## Dependencies
- `object.h` - Ships are object instances with specific properties
- `ai.h` - Each ship has associated AI data
- `weapon.h` - Ship weapons and firing logic
- `model.h` - Ship models and subsystem positioning
- `physics.h` - Ship movement and physics simulation
- `mission.h` - Mission-specific ship properties and behaviors

## Game Logic Integration
The ship system is fundamental to FreeSpace gameplay:
- Defines all flyable and AI-controlled vessels
- Implements damage and destruction mechanics
- Manages weapon loadouts and combat capabilities
- Handles player ship controls and behaviors
- Supports mission objectives through ship properties
- Integrates with AI for tactical behavior
- Manages multiplayer ship instances