# WCS System: Ship Class Definitions and Ship Factory Systems - Source Dependencies (Used By)

## File: `source/code/ship/ship.h` included/used by:
- `source/code/ship/ship.cpp` - Main implementation file for ship factory and management
- `source/code/ship/afterburner.cpp` - Accesses ship structures for afterburner fuel management
- `source/code/ship/awacs.cpp` - Uses ship subsystem structures for AWACS functionality  
- `source/code/ship/shield.cpp` - Accesses ship shield data and damage states
- `source/code/ship/shipcontrails.cpp` - Uses ship structures for contrail positioning
- `source/code/ship/shipfx.cpp` - Accesses ship data for visual effects and explosions
- `source/code/ship/shiphit.cpp` - Uses ship structures for collision and damage processing
- `source/code/ai/ai.cpp` - Accesses ship AI data and behavior states
- `source/code/ai/aicode.cpp` - Uses ship movement and targeting data
- `source/code/ai/aigoals.cpp` - Accesses ship goal and objective systems
- `source/code/ai/aiturret.cpp` - Uses ship subsystem data for turret control
- `source/code/weapon/weapons.cpp` - Accesses ship weapon loadouts and firing systems
- `source/code/weapon/beam.cpp` - Uses ship turret data for beam weapon targeting
- `source/code/mission/missionparse.cpp` - Creates ships during mission loading
- `source/code/object/object.cpp` - Manages ship objects in main object array
- `source/code/physics/physics.cpp` - Applies physics simulation to ship movement
- `source/code/hud/hudtarget.cpp` - Displays ship information on HUD
- `source/code/hud/hudtargetbox.cpp` - Shows ship subsystem data in targeting display
- `source/code/hud/hudshield.cpp` - Renders ship shield status indicators
- `source/code/network/multimsgs.cpp` - Synchronizes ship state in multiplayer
- `source/code/fred2/shipeditordlg.cpp` - Mission editor ship property interface
- `source/code/freespace2/freespace.cpp` - Main game loop ship processing

## File: `source/code/ship/ship.cpp` included/used by:
- `source/code/freespace2/freespace.cpp` - Calls ship_init() and ship_level_init()
- `source/code/mission/missionparse.cpp` - Uses ship_create() for spawning ships
- `source/code/ai/ai.cpp` - Calls ship lifecycle functions for AI ship management
- `source/code/object/object.cpp` - Uses ship_delete() for cleanup when objects are destroyed
- `source/code/network/multimsgs.cpp` - Calls ship creation functions for multiplayer synchronization
- `source/code/fred2/freddoc.cpp` - Uses ship factory functions for mission editor operations
- `source/code/gamesequence/gamesequence.cpp` - Calls ship initialization during level transitions

## File: `source/code/model/model.h` included/used by:
- `source/code/ship/ship.h` - Uses model_subsystem structures for subsystem templates
- `source/code/ship/ship.cpp` - Accesses model data for ship creation and rendering
- `source/code/model/modelinterp.cpp` - Ship rendering and model interpolation
- `source/code/model/modelcollide.cpp` - Ship collision detection using model geometry
- `source/code/model/modelread.cpp` - Loading POF models for ship classes
- `source/code/render/3d.cpp` - 3D rendering of ship models
- `source/code/ai/aiturret.cpp` - Uses model subsystem data for turret positioning
- `source/code/weapon/weapons.cpp` - Accesses model weapon hardpoints for firing
- `source/code/hud/hudtargetbox.cpp` - Uses model data for subsystem targeting display

## File: `source/code/weapon/weapon.h` included/used by:
- `source/code/ship/ship.h` - Defines ship_weapon structures and weapon bank arrays
- `source/code/ship/ship.cpp` - Implements weapon loadout initialization and management
- `source/code/weapon/weapons.cpp` - Main weapon implementation using ship weapon data
- `source/code/ai/aiturret.cpp` - Turret AI uses weapon definitions for targeting
- `source/code/ai/aicode.cpp` - AI weapon selection and firing decisions
- `source/code/hud/hudtarget.cpp` - Displays ship weapon information on HUD
- `source/code/mission/missionparse.cpp` - Parses mission weapon loadouts for ships
- `source/code/network/multimsgs.cpp` - Synchronizes weapon states in multiplayer

## File: `source/code/physics/physics.h` included/used by:
- `source/code/ship/ship.cpp` - Initializes ship physics parameters during creation
- `source/code/object/object.cpp` - Applies physics simulation to ship objects
- `source/code/ai/aicode.cpp` - AI movement and navigation using ship physics
- `source/code/ship/afterburner.cpp` - Modifies ship physics for afterburner effects
- `source/code/collision/collision.cpp` - Ship collision response and momentum transfer

## File: `source/code/ai/ai.h` included/used by:
- `source/code/ship/ship.h` - Defines ship AI integration and behavior states
- `source/code/ship/ship.cpp` - Initializes ship AI during creation process
- `source/code/ai/ai.cpp` - Main AI implementation for ship behavior control
- `source/code/ai/aicode.cpp` - Core AI logic and decision making for ships
- `source/code/ai/aigoals.cpp` - AI goal management for ship objectives
- `source/code/mission/missionparse.cpp` - Assigns AI classes to ships during mission loading

## File: `source/code/object/object.h` included/used by:
- `source/code/ship/ship.h` - Ships inherit from base object system
- `source/code/ship/ship.cpp` - Creates ship objects and manages object array slots
- `source/code/object/object.cpp` - Manages ship objects in main simulation loop
- `source/code/physics/physics.cpp` - Physics simulation operates on ship objects
- `source/code/render/3d.cpp` - Rendering system processes ship objects
- `source/code/collision/collision.cpp` - Collision detection between ship objects

## File: `source/code/mission/missionparse.h` included/used by:
- `source/code/ship/ship.cpp` - Uses mission parsing for ship spawning and configuration
- `source/code/mission/missionparse.cpp` - Main mission parsing implementation
- `source/code/freespace2/freespace.cpp` - Mission loading and ship initialization
- `source/code/gamesequence/gamesequence.cpp` - Mission transitions and ship setup
- `source/code/fred2/freddoc.cpp` - Mission editor integration for ship placement

## File: `source/code/globalincs/globals.h` included/used by:
- `source/code/ship/ship.h` - Provides NAME_LENGTH and other global constants
- `source/code/ship/ship.cpp` - Uses global definitions for ship management
- Most other files in the codebase - Central header for global constants and definitions

## File: `source/code/species_defs/species_defs.h` included/used by:
- `source/code/ship/ship.h` - Species definitions for different ship factions
- `source/code/ship/ship.cpp` - Species-specific ship characteristics and behaviors
- `source/code/ai/ai.cpp` - AI behavior variations based on ship species
- `source/code/iff_defs/iff_defs.cpp` - IFF system integration with species data

## File: `source/code/parse/parselo.h` included/used by:
- `source/code/ship/ship.cpp` - Table parsing for ships.tbl configuration files
- `source/code/weapon/weapons.cpp` - Weapon table parsing using same infrastructure
- `source/code/ai/ai_profiles.cpp` - AI configuration table parsing
- Most table-driven systems throughout the codebase

## File: `source/code/sound/sound.h` included/used by:
- `source/code/ship/ship.cpp` - Ship engine sounds and audio management
- `source/code/ship/afterburner.cpp` - Afterburner sound effects
- `source/code/weapon/weapons.cpp` - Weapon firing sounds
- `source/code/ai/aiturret.cpp` - Turret rotation and firing sounds

## File: `source/code/bmpman/bmpman.h` included/used by:
- `source/code/ship/ship.cpp` - Ship texture loading and management
- `source/code/ship/shipfx.cpp` - Explosion and effect texture loading
- `source/code/model/modelinterp.cpp` - Model texture application and rendering
- Most graphics and rendering systems throughout the codebase