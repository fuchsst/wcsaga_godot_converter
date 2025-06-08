# WCS System: Ship Class Definitions and Ship Factory Systems - Source Files List

## Core Ship System Files

- `source/code/ship/ship.h`: Core ship structures, ship_info definition, ship factory interface, and ship management constants (1794 lines)
- `source/code/ship/ship.cpp`: Main ship factory implementation, ship_create function, lifecycle management, and table parsing (15000+ lines)
- `source/code/ship/afterburner.cpp`: Afterburner fuel management and thrust mechanics
- `source/code/ship/afterburner.h`: Afterburner system definitions and interfaces
- `source/code/ship/awacs.cpp`: AWACS subsystem radar and detection capabilities
- `source/code/ship/awacs.h`: AWACS system structures and function declarations
- `source/code/ship/shield.cpp`: Shield management, quadrant damage, and regeneration logic
- `source/code/ship/shipcontrails.cpp`: Ship engine contrail effects and particle systems
- `source/code/ship/shipcontrails.h`: Contrail system definitions and configuration
- `source/code/ship/shipfx.cpp`: Ship visual effects, explosions, and damage rendering
- `source/code/ship/shipfx.h`: Ship effects system interface and effect definitions
- `source/code/ship/shiphit.cpp`: Ship collision detection and damage application logic
- `source/code/ship/shiphit.h`: Ship collision and damage system interface
- `source/code/ship/subsysdamage.h`: Subsystem damage modeling and state management

## Model and Asset Integration

- `source/code/model/model.h`: 3D model structures, subsystem definitions, and POF format interface
- `source/code/model/modelanim.cpp`: Model animation system for rotating subsystems and turrets
- `source/code/model/modelanim.h`: Model animation structures and control interface
- `source/code/model/modelcollide.cpp`: Model-based collision detection and mesh intersection
- `source/code/model/modelinterp.cpp`: Model rendering and interpolation system
- `source/code/model/modeloctant.cpp`: Spatial partitioning for efficient model collision queries
- `source/code/model/modelread.cpp`: POF file loader and model data parsing
- `source/code/model/modelsinc.h`: Model system includes and shared definitions

## Weapon System Integration

- `source/code/weapon/weapon.h`: Weapon definitions, firing mechanics, and ship weapon integration
- `source/code/weapon/weapons.cpp`: Weapon creation, firing logic, and ballistics management
- `source/code/weapon/beam.cpp`: Beam weapon implementation for ship turrets
- `source/code/weapon/beam.h`: Beam weapon structures and firing interface
- `source/code/weapon/trails.cpp`: Weapon trail effects and particle rendering
- `source/code/weapon/trails.h`: Trail system definitions and configuration
- `source/code/weapon/shockwave.cpp`: Explosion shockwave generation and damage propagation
- `source/code/weapon/shockwave.h`: Shockwave system interface and damage calculations

## Physics and Object Integration

- `source/code/object/object.h`: Base object system that ships inherit from
- `source/code/object/object.cpp`: Object lifecycle management and update loops
- `source/code/physics/physics.cpp`: Ship physics simulation, movement, and collision response
- `source/code/physics/physics.h`: Physics system interface and ship physics parameters

## Mission and Spawning System

- `source/code/mission/missionparse.h`: Mission file parsing and ship spawning definitions
- `source/code/mission/missionparse.cpp`: Mission ship creation, wing management, and spawn logic
- `source/code/mission/missionload.cpp`: Mission loading and ship initialization sequences
- `source/code/mission/missionload.h`: Mission loading system interface

## AI and Behavior Integration

- `source/code/ai/ai.h`: AI system structures and ship AI behavior interface
- `source/code/ai/ai.cpp`: AI decision making and ship behavior control
- `source/code/ai/aigoals.cpp`: AI goal system for ship objectives and tactics
- `source/code/ai/aigoals.h`: AI goal definitions and ship behavior goals
- `source/code/ai/aicode.cpp`: Core AI logic for ship movement and combat
- `source/code/ai/aiturret.cpp`: Turret AI targeting and firing control

## Asset and Resource Management

- `source/code/bmpman/bmpman.cpp`: Texture loading and management for ship materials
- `source/code/bmpman/bmpman.h`: Bitmap manager interface and texture handling
- `source/code/cfile/cfile.cpp`: File system interface for loading ship assets
- `source/code/cfile/cfile.h`: File loading system definitions
- `source/code/sound/sound.cpp`: Audio system for ship engine and weapon sounds
- `source/code/sound/sound.h`: Sound system interface and audio management

## Global Systems and Utilities

- `source/code/globalincs/globals.h`: Global constants and definitions used by ship system
- `source/code/globalincs/pstypes.h`: Platform-specific type definitions for ship structures
- `source/code/math/vecmat.cpp`: Vector and matrix mathematics for ship positioning and rotation
- `source/code/math/vecmat.h`: Mathematical utilities for ship coordinate systems
- `source/code/parse/parselo.cpp`: Low-level table parsing for ships.tbl file format
- `source/code/parse/parselo.h`: Table parsing system interface

## Species and Configuration

- `source/code/species_defs/species_defs.cpp`: Species-specific ship characteristics and behaviors
- `source/code/species_defs/species_defs.h`: Species system definitions for different ship factions
- `source/code/iff_defs/iff_defs.cpp`: IFF (Identify Friend or Foe) system for ship identification
- `source/code/iff_defs/iff_defs.h`: IFF system interface and team definitions

## Editor Integration (FRED2)

- `source/code/fred2/ship_select.cpp`: Ship selection interface for mission editor
- `source/code/fred2/ship_select.h`: Ship selection dialog definitions
- `source/code/fred2/shipeditordlg.cpp`: Ship property editor for mission creation
- `source/code/fred2/shipeditordlg.h`: Ship editor dialog interface
- `source/code/fred2/shipclasseditordlg.cpp`: Ship class modification interface
- `source/code/fred2/shipclasseditordlg.h`: Ship class editor definitions