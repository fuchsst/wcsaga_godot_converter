# Module Relationships and Dependencies

## Overview
This document shows how all the modules in the Godot implementation relate to each with their dependencies and integration points, following the directory structure defined in directory_structure.md. Understanding these relationships is crucial for successful conversion and implementation while maintaining proper organization.

## Core Foundation Modules
These modules form the base of the entire system and have minimal dependencies, organized in `/scripts/`:

```
[Core Entity Module] (/scripts/entities/)
    ↑
    |
[Object Module] (/scripts/entities/) ← [Math Module] (/scripts/utilities/)
    ↑                                    ↑
    |                                    |
[Physics Module] (/scripts/physics/) ---+
```

## Gameplay Foundation Modules
These modules build on the core foundation and provide basic gameplay elements, organized in `/features/`:

```
[Core Entity Module] (/scripts/entities/)
    ↑
    |
[Ship Module] (/features/fighters/) ← [Model Module] (/features/environment/) ← [Graphics Module] (/assets/textures/)
    ↑                                   ↑                                        ↑
    |                                   |                                        |
[Weapon Module] (/features/weapons/) --+--[Physics Module] (/scripts/physics/)
    ↑                                   |
    |                                   |
[AI Module] (/scripts/ai/) ------------+
```

## Mission and Campaign Modules
These modules handle mission flow and campaign progression, organized in `/campaigns/` and `/scripts/mission/`:

```
[Mission Module] (/scripts/mission/) ← [Parse Module] (/scripts/utilities/)
    ↑                                    ↑
    |                                    |
[Gamesequence Module] (/scripts/mission/) |
    ↑                                    |
    |                                    |
[Player Module] (/autoload/) -----------+
```

## User Interface Modules
These modules handle all user interaction and display, organized in `/features/ui/`:

```
[UI Module] (/features/ui/) ← [Graphics Module] (/assets/textures/)
    ↑                         ↑
    |                         |
[HUD Module] (/features/ui/hud/) ----+
    ↑
    |
[Radar Module] (/features/ui/hud/)
    ↑
    |
[Menu UI Module] (/features/ui/) ← [Mission UI Module] (/features/ui/briefing/)
```

## Visual and Audio Effects Modules
These modules enhance the sensory experience, organized in `/features/effects/` and `/assets/audio/`:

```
[Visual Effects Module] (/features/effects/) ← [Graphics Module] (/assets/textures/)
    ↑                                           ↑
    |                                           |
[Particle Module] (/features/effects/) --------+
    ↑
    |
[Fireball Module] (/features/effects/fireball/)
    ↑
    |
[Debris Module] (/features/environment/) ← [Asteroid Module] (/features/environment/asteroid/)

[Sound Module] (/autoload/) ← [Audio Module] (/assets/audio/)
    ↑                         ↑
    |                         |
[Gamesnd Module] (/autoload/) --+
```

## Environmental and Special Systems
These modules handle environmental and special gameplay elements, organized in `/features/environment/`:

```
[Nebula Module] (/features/environment/nebula/) ← [Starfield Module] (/features/environment/)
    ↑                                             ↑
    |                                             |
[Jumpnode Module] (/features/environment/) ------+

[Autopilot Module] (/scripts/ai/) ← [AI Module] (/scripts/ai/)
    ↑                               ↑
    |                               |
[CMeasure Module] (/features/weapons/) ---+
```

## Complete Dependency Graph
Here's the full dependency graph showing all relationships with their directory locations:

```
[Math Module] (/scripts/utilities/)
    ↑
    |
[Core Entity Module] (/scripts/entities/) ← [Parse Module] (/scripts/utilities/)
    ↑                                         ↑
    |                                         |
[Object Module] (/scripts/entities/) ← [Physics Module] (/scripts/physics/)
    ↑                                    ↑     ↑
    |                                    |     |
[Ship Module] (/features/fighters/) ← [Model Module] (/features/environment/) ← [Graphics Module] (/assets/textures/)
    ↑                                   ↑              ↑
    |                                   |              |
[Weapon Module] (/features/weapons/) --+--[Physics Module] (/scripts/physics/)
    ↑                                   |     ↑
    |                                   |     |
[AI Module] (/scripts/ai/) ------------+-----+
    ↑                                         |
    |                                         |
[Mission Module] (/scripts/mission/) --------+
    ↑
    |
[Gamesequence Module] (/scripts/mission/) ← [Player Module] (/autoload/)
    ↑
    |
[UI Module] (/features/ui/) ← [Graphics Module] (/assets/textures/)
    ↑                         ↑
    |                         |
[HUD Module] (/features/ui/hud/) ----+
    ↑
    |
[Radar Module] (/features/ui/hud/) ← [IFF Definitions Module] (/features/fighters/_shared/)
    ↑                                  ↑
    |                                  |
[Menu UI Module] (/features/ui/) ------+--[Mission UI Module] (/features/ui/briefing/)
    ↑                                        ↑
    |                                        |
[Visual Effects Module] (/features/effects/) -+
    ↑
    |
[Particle Module] (/features/effects/) ← [Graphics Module] (/assets/textures/)
    ↑                                      ↑
    |                                      |
[Fireball Module] (/features/effects/fireball/) ---+
    ↑
    |
[Debris Module] (/features/environment/) ← [Asteroid Module] (/features/environment/asteroid/)
    ↑                                      ↑
    |                                      |
[Sound Module] (/autoload/) ← [Audio Module] (/assets/audio/)
    ↑                         ↑
    |                         |
[Gamesnd Module] (/autoload/) --+
    ↑
    |
[Nebula Module] (/features/environment/nebula/) ← [Starfield Module] (/features/environment/)
    ↑                                             ↑
    |                                             |
[Jumpnode Module] (/features/environment/) ------+
    ↑
    |
[Autopilot Module] (/scripts/ai/) ← [AI Module] (/scripts/ai/)
    ↑                               ↑
    |                               |
[CMeasure Module] (/features/weapons/) ---+
    ↑
    |
[Species Definitions Module] (/features/fighters/_shared/)
```

## Integration Layers with Directory Structure
The modules integrate in layers from core to presentation, organized according to the directory structure:

### Layer 1: Foundation (/scripts/utilities/, /scripts/entities/)
- Math Module (/scripts/utilities/)
- Core Entity Module (/scripts/entities/)
- Parse Module (/scripts/utilities/)

### Layer 2: Core Systems (/scripts/)
- Object Module (/scripts/entities/)
- Physics Module (/scripts/physics/)
- Model Module (/features/environment/)
- Graphics Module (/assets/textures/)
- Audio Module (/assets/audio/)

### Layer 3: Gameplay Systems (/features/, /scripts/)
- Ship Module (/features/fighters/)
- Weapon Module (/features/weapons/)
- AI Module (/scripts/ai/)
- Sound Module (/autoload/)
- Gamesnd Module (/autoload/)

### Layer 4: Mission Systems (/scripts/mission/, /autoload/, /features/fighters/_shared/)
- Mission Module (/scripts/mission/)
- Player Module (/autoload/)
- Gamesequence Module (/scripts/mission/)
- IFF Definitions Module (/features/fighters/_shared/)
- Species Definitions Module (/features/fighters/_shared/)

### Layer 5: Environmental Systems (/features/environment/, /features/effects/)
- Asteroid Module (/features/environment/asteroid/)
- Debris Module (/features/environment/)
- Fireball Module (/features/effects/fireball/)
- Particle Module (/features/effects/)
- Visual Effects Module (/features/effects/)
- Nebula Module (/features/environment/nebula/)
- Starfield Module (/features/environment/)
- Jumpnode Module (/features/environment/)

### Layer 6: Special Systems (/scripts/ai/, /features/weapons/)
- Autopilot Module (/scripts/ai/)
- CMeasure Module (/features/weapons/)
- Radar Module (/features/ui/hud/)

### Layer 7: User Interface (/features/ui/)
- UI Module (/features/ui/)
- HUD Module (/features/ui/hud/)
- Menu UI Module (/features/ui/)
- Mission UI Module (/features/ui/briefing/)

## Data Flow Patterns with Directory Locations

### 1. Initialization Flow
```
Parse Module (/scripts/utilities/) → Core Entity Module (/scripts/entities/)
                               ↓
                   Object Module (/scripts/entities/) → Ship/Weapon/AI Modules (/features/)
                               ↓
                  Mission Module (/scripts/mission/) → Gamesequence Module (/scripts/mission/)
                               ↓
                       UI Module (/features/ui/)
```

### 2. Runtime Update Flow
```
Gamesequence Module (/scripts/mission/) → Input Processing
                                    ↓
                           AI Module (/scripts/ai/) → Physics Module (/scripts/physics/)
                                    ↓
              Ship/Weapon Modules (/features/) → Collision Detection
                                    ↓
           Visual Effects Module (/features/effects/) → Rendering
                                    ↓
                   HUD Module (/features/ui/hud/) → Display Updates
```

### 3. Event Flow
```
Input/UI Events → Gamesequence Module (/scripts/mission/)
              ↓
        Event Queue → System Processing
              ↓
Mission/Ships/Weapons/AI (/features/, /scripts/) → State Changes
              ↓
  Visual/Audio Feedback → Player
```

## Cross-Module Communication Patterns with Directory Structure

### 1. Direct Dependencies
Modules that directly depend on others for functionality:
- Ship Module (/features/fighters/) depends on Weapon Module (/features/weapons/) for armament
- Weapon Module (/features/weapons/) depends on Ship Module (/features/fighters/) for mounting points
- AI Module (/scripts/ai/) depends on Ship Module (/features/fighters/) for behavior targets
- Mission Module (/scripts/mission/) depends on all gameplay modules for entity creation

### 2. Signal-Based Communication
Modules that communicate through Godot signals:
- Object Module (/scripts/entities/) emits destruction signals
- Ship Module (/features/fighters/) emits damage signals
- Weapon Module (/features/weapons/) emits firing signals
- Mission Module (/scripts/mission/) emits objective completion signals

### 3. Resource-Based Configuration
Modules that share data through Godot resources:
- Ship/Weapon classes shared between modules (/features/)
- Mission data shared between mission and UI modules (/campaigns/, /features/ui/)
- AI profiles shared between AI and ship modules (/scripts/ai/, /features/fighters/)
- Effect definitions shared between visual effects modules (/features/effects/)

### 4. Singleton Access
Modules accessed through Godot's autoload system (/autoload/):
- Player Module (/autoload/) for player state
- Mission Module (/autoload/ - mission_manager.gd) for mission data
- Gamesequence Module (/autoload/) for game state
- UI Module (/autoload/) for interface elements

## Conversion Order Recommendation with Directory Structure

Based on dependencies and directory organization, modules should be converted in this order:

1. **Foundation Layer**: Math (/scripts/utilities/), Core Entity (/scripts/entities/), Parse (/scripts/utilities/)
2. **Core Systems**: Object (/scripts/entities/), Physics (/scripts/physics/), Model (/features/environment/), Graphics (/assets/), Audio (/assets/)
3. **Gameplay Systems**: Ship (/features/fighters/), Weapon (/features/weapons/), AI (/scripts/ai/), Sound (/autoload/), Gamesnd (/autoload/)
4. **Mission Systems**: Mission (/scripts/mission/), Player (/autoload/), Gamesequence (/scripts/mission/), IFF (/features/fighters/_shared/), Species (/features/fighters/_shared/)
5. **Environmental Systems**: Asteroid (/features/environment/asteroid/), Debris (/features/environment/), Fireball (/features/effects/fireball/), Particle (/features/effects/), Visual Effects (/features/effects/), Nebula (/features/environment/nebula/), Starfield (/features/environment/), Jumpnode (/features/environment/)
6. **Special Systems**: Autopilot (/scripts/ai/), CMeasure (/features/weapons/), Radar (/features/ui/hud/)
7. **User Interface**: UI (/features/ui/), HUD (/features/ui/hud/), Menu UI (/features/ui/), Mission UI (/features/ui/briefing/)

This order ensures that dependent modules are available when needed and minimizes blocking during conversion while following the feature-based organization principles.

## Integration Testing Points with Directory Structure

### Early Integration (Core + Gameplay)
- Object creation and destruction (/scripts/entities/)
- Ship movement and physics (/features/fighters/, /scripts/physics/)
- Basic weapon firing (/features/weapons/)
- Simple AI behavior (/scripts/ai/)

### Mid Integration (Mission + UI)
- Mission loading and entity spawning (/campaigns/, /scripts/mission/)
- HUD display of ship status (/features/ui/hud/)
- Basic mission objectives (/campaigns/)
- Menu navigation (/features/ui/)

### Late Integration (Effects + Environment)
- Visual effects for weapons and explosions (/features/effects/)
- Environmental effects (nebula, starfield) (/features/environment/)
- Full mission flow with briefing/debriefing (/campaigns/, /features/ui/briefing/)
- Complete UI with all elements (/features/ui/)

This dependency analysis provides a roadmap for converting the Wing Commander Saga codebase to Godot while maintaining the same gameplay functionality and ensuring proper integration between all systems, organized according to the feature-based directory structure.