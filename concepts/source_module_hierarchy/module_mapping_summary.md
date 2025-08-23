# Module Hierarchy Summary

## Overview
This document provides an overview of the module hierarchy for converting the Wing Commander Saga codebase to Godot. The modules are organized based on their dependencies and functionality, showing how they interconnect to form a complete game engine.

## Module Dependencies Diagram

```
                    +------------------+
                    |   Game State     |
                    |   Module         |
                    +------------------+
                             |
         +-------------------+-------------------+
         |                   |                   |
+----------------+  +-----------------+  +----------------+
| Core Entity    |  | Mission         |  | UI             |
| Module         |  | Module          |  | Module         |
+----------------+  +-----------------+  +----------------+
         |                   |                   |
         |         +-----------------+           |
         |         | Visual Effects  |           |
         |         | Module          |           |
         |         +-----------------+           |
         |                   |                   |
+----------------+           |          +----------------+
| Ship Module    |-----------+----------| Audio          |
+----------------+           |          | Module         |
         |                   |          +----------------+
         |          +-----------------+         |
         |          | Physics         |         |
         |          | Module          |         |
         |          +-----------------+         |
         |                   |                  |
         |          +-----------------+         |
         |          | AI              |         |
         |          | Module          |         |
         |          +-----------------+         |
         |                   |                  |
+----------------+           |          +----------------+
| Weapon         |-----------+----------| Game State     |
| Module         |                      | Module         |
+----------------+                      +----------------+
```

## Module Relationships

### 1. Core Dependencies
- **Core Entity Module** is the foundation for all other modules
- **Physics Module** depends on Core Entity Module for entity physics properties
- **Game State Module** depends on all major modules for state transitions

### 2. Ship System Dependencies
- **Ship Module** depends on:
  - Core Entity Module (ships are entities)
  - Physics Module (ship movement)
  - Weapon Module (ship weapons)
  - AI Module (ship behavior)
  - Visual Effects Module (ship visuals)
  - Audio Module (ship sounds)

### 3. Combat System Dependencies
- **Weapon Module** depends on:
  - Core Entity Module (weapons are entities)
  - Ship Module (weapons are fired by ships)
  - Physics Module (projectile movement)
  - Visual Effects Module (weapon effects)
  - Audio Module (weapon sounds)

### 4. Mission Flow Dependencies
- **Mission Module** depends on:
  - Core Entity Module (mission entities)
  - Ship Module (mission ships)
  - Weapon Module (mission weapons)
  - AI Module (mission AI)
  - UI Module (briefing/debriefing)
  - Game State Module (mission state management)

### 5. Presentation Layer Dependencies
- **UI Module** depends on:
  - Core Entity Module (entity information)
  - Ship Module (ship status)
  - Weapon Module (weapon status)
  - Mission Module (mission data)
  - Game State Module (screen management)
  
- **Visual Effects Module** depends on:
  - Core Entity Module (effect entities)
  - Graphics Module (rendering)
  - Physics Module (particle physics)
  
- **Audio Module** depends on:
  - Core Entity Module (3D positioning)
  - Ship Module (ship sounds)
  - Weapon Module (weapon sounds)
  - Mission Module (mission audio)

### 6. AI System Dependencies
- **AI Module** depends on:
  - Core Entity Module (AI entities)
  - Ship Module (ship-specific AI)
  - Weapon Module (weapon selection)
  - Physics Module (movement calculations)
  - Mission Module (mission objectives)

## Data Flow Patterns

### 1. Initialization Flow
```
Game State Module → Config Loading → Subsystem Initialization
                              ↓
                   Mission Module → Entity Creation
                              ↓
        Ship/Weapon/AI/Physics Modules → Component Attachment
```

### 2. Runtime Update Flow
```
Game State Module → Input Processing
              ↓
     Mission Module → Event Processing
              ↓
  AI/Physics/Entity Modules → Component Updates
              ↓
Visual Effects/Audio Modules → Feedback Generation
              ↓
        UI Module → Display Updates
```

### 3. Event Flow
```
Input/UI Events → Game State Module
            ↓
      Event Queue → System Processing
            ↓
  Mission/Ships/Weapons/AI → State Changes
            ↓
    Visual/Audio Feedback → Player
```

## Integration Points

### 1. Entity Component System
All gameplay modules integrate through the Core Entity Module using a component-based approach:
- Ships have PhysicsController, WeaponSystem, AIController components
- Weapons have PhysicsController, ParticleSystem components
- Effects have ParticleSystem, AudioEmitter components

### 2. Resource System Integration
All modules use Godot's resource system for data-driven configuration:
- Ship classes as ShipClass resources
- Weapon types as WeaponClass resources
- Sound effects as SoundDefinition resources
- Mission data as Mission resources

### 3. Signal-Based Communication
Modules communicate through Godot's signal system:
- GameStateManager signals for state changes
- EntityManager signals for entity events
- MissionManager signals for mission events
- UIManager signals for UI interactions

### 4. Scene Composition
Complex game objects are composed using Godot scenes:
- Ships as scenes with model, components, and scripts
- Weapons as scenes with effects and behavior
- UI screens as scenes with controls and logic
- Missions as scenes with environment and entities

## Conversion Strategy

### 1. Direct Mapping
- **Physics Module**: Direct port of movement calculations
- **AI Module**: Behavior trees replacing goal-based system
- **Weapon Module**: Similar functionality with Godot integration
- **Game State Module**: State machine pattern preserved

### 2. Engine Replacement
- **Graphics**: Replaced with Godot renderer
- **Audio**: Replaced with Godot audio system
- **Input**: Replaced with Godot input handling
- **UI**: Replaced with Godot UI system

### 3. Hybrid Approaches
- **Mission System**: Logic ported, presentation in Godot scenes
- **Model System**: POF files converted to Godot-compatible formats
- **Particle System**: Replaced with Godot particle systems
- **Animation System**: Replaced with Godot animation system

## Implementation Priority

### Phase 1: Foundation (Core + Game State)
1. Core Entity Module
2. Game State Module
3. Basic UI Module

### Phase 2: Gameplay Systems
4. Physics Module
5. Ship Module
6. Weapon Module

### Phase 3: Intelligence and Content
7. AI Module
8. Mission Module
9. Visual Effects Module

### Phase 4: Polish and Polish
10. Audio Module
11. Advanced UI Features
12. Final Integration

This hierarchy provides a clear roadmap for converting the Wing Commander Saga codebase to Godot while preserving the core gameplay functionality and extending it with modern engine capabilities.