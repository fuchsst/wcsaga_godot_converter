# Wing Commander Saga System Architecture

## Overview
This document provides a high-level view of how the different systems in Wing Commander Saga interact with each other, showing the relationships and data flow between components.

## Core Engine Architecture

```
                    +------------------+
                    |   Main Loop      |
                    |  (freespace2/)   |
                    +------------------+
                             |
         +-------------------+-------------------+
         |                   |                   |
+----------------+  +-----------------+  +----------------+
| Game Sequence  |  | Object System   |  | Rendering      |
| (gamesequence/)|  |   (object/)     |  |  Pipeline      |
+----------------+  +-----------------+  +----------------+
         |                   |           |        |
+----------------+  +-----------------+  |  +-------------+
| Mission System |  | Physics System  |  |  | Graphics    |
|  (mission/)    |  |  (physics/)     |  |  | (graphics/) |
+----------------+  +-----------------+  |  +-------------+
         |                   |           |        |
+----------------+           |           |  +-------------+
| AI System      |           |           |  | Models      |
|   (ai/)        |           |           |  |  (model/)   |
+----------------+           |           |  +-------------+
         |                   |           |        |
+----------------+  +-----------------+  |  +-------------+
| Ship System    |  | Weapons System  |  |  | Textures    |
|   (ship/)      |  |   (weapon/)     |  |  | (bmpman/)   |
+----------------+  +-----------------+  |  +-------------+
                                        |        |
                                +----------------------+
                                | Special Effects      |
                                | (particle/, fireball/)|
                                +----------------------+
```

## Data Flow Architecture

### 1. Initialization Phase
```
cmdline/ → parse/ → [System Initialization] → mission/ → object/
```

### 2. Runtime Loop
```
io/ → controlconfig/ → [Player Input Processing]
    ↓
gamesequence/ → [State Management]
    ↓
object/ → physics/ → [Movement Updates]
    ↓
ai/ → [AI Decision Making]
    ↓
ship/ ↔ weapon/ → [Combat Processing]
    ↓
graphics/ → model/ → bmpman/ → [Rendering]
    ↓
hud/ → [Player Feedback]
```

## System Dependencies

### High-Level Dependencies
- **Everything** → `object/` (base entity system)
- **Everything** → `math/` (mathematical operations)
- **Rendering systems** → `graphics/` (rendering pipeline)
- **Gameplay systems** → `physics/` (movement and collision)

### Mission Flow Dependencies
```
mission/ → ship/ → weapon/ → ai/
    ↓        ↓       ↓       ↓
object/  object/ object/ object/
    ↓        ↓       ↓       ↓
physics/ physics/ physics/ physics/
```

### UI Dependencies
```
ui/ → menuui/ → playerman/
  ↓       ↓         ↓
graphics/ mission/  stats/
```

## Key Integration Patterns

### 1. Component-Based Architecture
Most game entities use a component-based approach:
- `object/` provides the base component
- `ship/`, `weapon/`, `asteroid/` extend object with specialized data
- `physics/` provides movement component for all objects
- `ai/` provides behavior component for ships

### 2. Data-Driven Design
- Configuration files parsed by `parse/`
- Game data defined in external tables
- Runtime behavior controlled by data rather than code

### 3. Event-Driven Systems
- `gamesequence/` manages state transitions through events
- `mission/` uses scripted events to drive mission flow
- `ui/` responds to input events

### 4. Pipeline Processing
- Assets flow through loading pipeline: file → parse → load → cache
- Frame updates flow through processing pipeline: input → update → render
- Special effects flow through: create → update → render → destroy

## Multiplayer Architecture

```
network/ ←→ object/ synchronization
    ↓
mm/ (matchmaking) ←→ playerman/
    ↓
observer/ ←→ camera/
```

## Editor Architecture (FRED2)

```
fred2/ ←→ mission/
    ↓         ↓
ui/ ←→ ship/ ↔ ai/
    ↓         ↓
graphics/ ←→ weapon/
```

## Performance Considerations

### Caching Systems
- `bmpman/` caches textures
- `model/` caches loaded models
- `sound/` caches audio files
- `anim/` caches animations

### Level of Detail
- `model/` provides multiple detail levels
- `graphics/` implements LOD switching
- `particle/` adjusts effect complexity

### Streaming
- `mission/` loads/unloads content dynamically
- `bmpman/` streams textures on demand
- `sound/` manages audio memory

This architecture shows how the systems are interconnected to create a cohesive game engine while maintaining modularity and separation of concerns.