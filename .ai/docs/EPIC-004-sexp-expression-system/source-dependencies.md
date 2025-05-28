# EPIC-004: SEXP Expression System - WCS Source Dependencies

**Epic**: EPIC-004 - SEXP Expression System  
**Analyst**: Larry (WCS Analyst)  
**Analysis Date**: 2025-01-27  

This document maps the usage relationships between SEXP system files, showing which files depend on (include) core SEXP components and which files are depended upon by the SEXP system.

## Core SEXP Engine Dependencies

### File: `parse/sexp.h` included/used by:
- `parse/sexp.cpp` - Main implementation file
- `mission/missionparse.h` - Mission file structures
- `mission/missionparse.cpp` - Mission loading system
- `mission/missiongoals.h` - Mission objective definitions
- `mission/missiongoals.cpp` - Goal evaluation system
- `mission/missionmessage.cpp` - Message triggering system
- `mission/missiontraining.cpp` - Training system integration
- `mission/missioncampaign.cpp` - Campaign progression logic
- `fred2/sexp_tree.h` - Visual SEXP editor interface
- `fred2/sexp_tree.cpp` - SEXP tree visualization
- `fred2/addvariabledlg.cpp` - Variable creation dialog
- `fred2/modifyvariabledlg.cpp` - Variable editing dialog
- `fred2/briefingeditordlg.cpp` - Briefing editor integration
- `fred2/debriefingeditordlg.cpp` - Debriefing editor
- `fred2/eventeditor.cpp` - Event editor
- `fred2/missiongoalsdlg.cpp` - Mission goals dialog
- `fred2/shipeditordlg.cpp` - Ship editor (AI goals)
- `fred2/campaigntreewnd.cpp` - Campaign tree editor
- `network/multi_sexp.h` - Multiplayer SEXP interface
- `network/multi_sexp.cpp` - Network synchronization
- `ai/aigoals.cpp` - AI behavior system
- `freespace2/freespace.cpp` - Main game loop
- `hud/hudsquadmsg.cpp` - Squadron messaging

### File: `parse/sexp.cpp` included/used by:
- No direct includes (implementation file)
- Linked by all executables using SEXP system

### File: `variables/variables.h` included/used by:
- `variables/variables.cpp` - Implementation file
- `parse/sexp.cpp` - SEXP variable integration
- `fred2/sexp_tree.cpp` - Visual variable editing
- `fred2/addvariabledlg.cpp` - Variable creation
- `fred2/modifyvariabledlg.cpp` - Variable modification

### File: `variables/variables.cpp` included/used by:
- No direct includes (implementation file)
- Linked by SEXP evaluation system

## Mission System Dependencies

### File: `mission/missionparse.h` included/used by:
- `mission/missionparse.cpp` - Implementation
- `mission/missiongoals.cpp` - Goal system access to mission data
- `mission/missionmessage.cpp` - Message system access to mission objects
- `mission/missiontraining.cpp` - Training system mission access
- `mission/missioncampaign.cpp` - Campaign mission management
- `parse/sexp.cpp` - SEXP mission object access
- `fred2/sexp_tree.cpp` - Editor mission object validation
- `fred2/eventeditor.cpp` - Event editor mission integration
- `fred2/shipeditordlg.cpp` - Ship editor mission context
- `ai/aigoals.cpp` - AI goal mission object access
- `network/multi_sexp.cpp` - Multiplayer mission synchronization

### File: `mission/missiongoals.h` included/used by:
- `mission/missiongoals.cpp` - Implementation
- `parse/sexp.cpp` - Goal evaluation integration
- `fred2/missiongoalsdlg.cpp` - Goal editing interface
- `fred2/sexp_tree.cpp` - Goal SEXP visualization
- `mission/missioncampaign.cpp` - Campaign goal tracking

## FRED2 Editor Dependencies

### File: `fred2/sexp_tree.h` included/used by:
- `fred2/sexp_tree.cpp` - Implementation
- `fred2/eventeditor.cpp` - Event SEXP editing
- `fred2/missiongoalsdlg.cpp` - Goal SEXP editing
- `fred2/briefingeditordlg.cpp` - Briefing SEXP integration
- `fred2/debriefingeditordlg.cpp` - Debriefing SEXP integration
- `fred2/shipeditordlg.cpp` - Ship AI goal SEXP editing
- `fred2/campaigntreewnd.cpp` - Campaign SEXP editing

## Network System Dependencies

### File: `network/multi_sexp.h` included/used by:
- `network/multi_sexp.cpp` - Implementation
- `parse/sexp.cpp` - Multiplayer SEXP coordination
- `network/multimsgs.cpp` - Network message integration
- `network/multiutil.cpp` - Multiplayer utilities

## AI System Dependencies

### File: `ai/aigoals.h` included/used by:
- `ai/aigoals.cpp` - Implementation
- `parse/sexp.cpp` - AI goal SEXP evaluation
- `mission/missionparse.cpp` - Mission AI goal assignment
- `fred2/shipeditordlg.cpp` - AI goal editing

## External Dependencies (Files SEXP depends on)

### Core Foundation Dependencies
- `globalincs/pstypes.h` - Basic type definitions (required by all SEXP files)
- `globalincs/linklist.h` - Linked list utilities (used by SEXP nodes)
- `parse/parselo.h` - Text parsing functions (required for SEXP text processing)
- `parse/parselo.cpp` - Parsing implementation

### Game System Dependencies  
SEXP system has extensive dependencies on nearly every WCS subsystem:

#### Ship and Object Systems
- `ship/ship.h` - Ship data structures and functions
- `ship/shiphit.h` - Ship damage and destruction
- `object/object.h` - Game object management
- `object/waypoint.h` - Waypoint system for navigation
- `object/objcollide.h` - Collision detection and events

#### Weapon and Combat Systems
- `weapon/weapon.h` - Weapon data and firing
- `weapon/beam.h` - Beam weapon system
- `weapon/emp.h` - EMP weapon effects
- `weapon/shockwave.h` - Explosive effects

#### Graphics and Rendering
- `graphics/2d.h` - 2D graphics for HUD integration
- `render/3d.h` - 3D rendering for camera control
- `bmpman/bmpman.h` - Texture management

#### Audio System
- `gamesnd/gamesnd.h` - Sound effect triggering
- `gamesnd/eventmusic.h` - Music control
- `sound/audiostr.h` - Audio streaming

#### HUD and User Interface
- `hud/hud.h` - HUD element control
- `hud/hudconfig.h` - HUD configuration
- `hud/hudshield.h` - Shield display
- `hud/hudescort.h` - Escort display
- `hud/hudets.h` - ETS display
- `hud/hudartillery.h` - Artillery display

#### Game Flow and State
- `gamesequence/gamesequence.h` - Game state transitions
- `playerman/player.h` - Player data and progression
- `stats/medals.h` - Award and medal system
- `io/timer.h` - Timing and delays

#### Environment and Effects
- `starfield/starfield.h` - Starfield control
- `starfield/supernova.h` - Supernova effects
- `nebula/neb.h` - Nebula effects
- `nebula/neblightning.h` - Nebula lightning
- `asteroid/asteroid.h` - Asteroid field management
- `fireball/fireballs.h` - Explosion effects

#### Network and Multiplayer
- `network/multi.h` - Multiplayer coordination
- `network/multimsgs.h` - Network messaging
- `network/multiutil.h` - Multiplayer utilities
- `network/multi_team.h` - Team management
- `network/multi_obj.h` - Object synchronization

#### Specialized Systems
- `jumpnode/jumpnode.h` - Jump node control
- `autopilot/autopilot.h` - Autopilot system
- `iff_defs/iff_defs.h` - IFF (Identification Friend/Foe) system
- `camera/camera.h` - Camera control
- `cmdline/cmdline.h` - Command line processing

## Dependency Analysis Summary

### High-Dependency Components (Critical for SEXP)
1. **Mission System**: Core integration point - 8 files depend on SEXP
2. **Ship System**: Essential for status queries - 15+ SEXP operators
3. **Parsing System**: Foundation for SEXP text processing
4. **Object System**: Required for spatial and state queries

### Medium-Dependency Components (Important for SEXP)
1. **AI System**: SEXP-driven behavior trees
2. **HUD System**: Display and user interface integration
3. **Weapon System**: Combat-related SEXP operators
4. **Audio System**: Sound and music control

### Low-Dependency Components (Optional for Core SEXP)
1. **Graphics System**: Advanced visual effects
2. **Network System**: Multiplayer synchronization
3. **Environment Systems**: Visual effects and environment control

### FRED2 Editor Dependencies
The visual SEXP editor has extensive dependencies:
- 12 FRED2 files depend on `sexp_tree.h`
- All mission editing dialogs integrate SEXP functionality
- Visual validation requires access to all game systems

## Conversion Implementation Impact

### Critical Path Dependencies
For Godot conversion, these dependencies must be resolved first:
1. **Parsing System** → Core foundation for SEXP text processing
2. **Mission Data Structures** → Required for SEXP context
3. **Object System** → Essential for SEXP object queries
4. **Ship System** → Required for most SEXP operators

### Parallel Development Opportunities
These systems can be developed in parallel with SEXP:
1. **Audio System** → Mock implementation sufficient initially
2. **Graphics System** → Visual effects can be placeholder
3. **Network System** → Single-player focus initially
4. **Environment Systems** → Can use Godot defaults

### Testing Strategy Implications
The extensive dependencies suggest:
1. **Mock System Architecture** → Create simplified interfaces for testing
2. **Incremental Integration** → Add system dependencies gradually
3. **Compatibility Testing** → Verify each dependency integration
4. **Performance Testing** → Monitor impact of complex dependency chains

---

**Dependency Analysis Complete**: SEXP system has extensive dependencies on virtually every WCS subsystem, requiring careful coordination during Godot conversion. Core dependencies (parsing, mission, object, ship) must be implemented first, followed by incremental integration of additional systems.