# Weapon System Analysis

## Purpose
The weapon system handles all projectile and beam-based weapons in FreeSpace, including their properties, behavior, firing logic, and effects. It supports multiple weapon types with different characteristics and special behaviors.

## Main Public Interfaces
- `weapon_info` - Structure defining weapon class properties (damage, speed, effects)
- `weapon` - Structure representing individual weapon instances
- `weapon_create()` - Creates a new weapon instance
- `weapon_process_pre()` / `weapon_process_post()` - Per-frame weapon processing
- `weapon_delete()` - Removes a weapon from the game
- `weapon_hit()` - Handles weapon impact and damage application
- `weapon_info_lookup()` - Finds weapon class by name
- `weapon_fire_primary()` / `weapon_fire_secondary()` - Firing functions

## Key Components
- **Weapon Types**: Lasers, missiles, beams, and countermeasures
- **Homing Systems**: Heat-seeking, aspect-lock, and javelin-style targeting
- **Special Effects**: Trails, particles, EMP, electronics effects
- **Damage Modeling**: Hull/shield damage with armor factors and multipliers
- **Ammunition Management**: Ammo tracking for ballistic weapons
- **Spawn Weapons**: Weapons that create other weapons on detonation
- **Beam Weapons**: Continuous energy weapons with special rendering
- **Countermeasures**: Chaff and other defensive systems

## Dependencies
- `object.h` - Weapons are object instances with specific properties
- `ship.h` - Weapons are fired by ships and affect ships
- `model.h` - Weapon models and firing point positioning
- `physics.h` - Weapon movement and trajectory
- `ai.h` - AI targeting and weapon selection

## Game Logic Integration
The weapon system is central to combat gameplay:
- Implements all player and AI offensive capabilities
- Handles damage application and destruction effects
- Supports tactical variety through different weapon types
- Integrates with AI for target selection and firing decisions
- Manages multiplayer weapon synchronization
- Controls balance through weapon statistics and properties