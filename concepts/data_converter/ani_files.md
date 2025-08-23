# ANI Files Conversion Requirements

## Overview
ANI files contain animation sequences for effects, UI elements, and sprite-based animations in Wing Commander Saga. These custom format files need to be converted to Godot's animation system using sprite sheets and animation resources, following Godot's feature-based organization principles.

## File Types and Conversion Requirements

### Sprite-Based Animations
**Purpose**: Explosions, weapon effects, and visual feedback
**Source Format**: ANI format with frame sequences
**Target Format**: Sprite sheet textures with animation data
**Conversion Requirements**:
- Extract individual animation frames
- Convert frames to sprite sheet format
- Generate timing and frame sequence data
- Handle loop properties and playback modes
- Maintain transparency and blending modes

### User Interface Animations
**Purpose**: Animated menu elements and HUD effects
**Source Format**: ANI format with UI-specific properties
**Target Format**: Animated texture resources with UI properties
**Conversion Requirements**:
- Preserve exact pixel positioning and sizing
- Convert UI-specific timing and triggers
- Handle different UI states and transitions
- Maintain crisp edges for interface clarity
- Integrate with Godot's UI animation system

### Particle Effect Animations
**Purpose**: Animated textures for particle systems
**Source Format**: ANI format with particle properties
**Target Format**: Animated texture atlases for particle systems
**Conversion Requirements**:
- Convert to efficient texture atlas format
- Generate particle emission timing data
- Handle additive and blend mode properties
- Maintain frame rate compatibility with particle systems
- Optimize for real-time particle rendering

### Character Animation Sequences
**Purpose**: Pilot portraits and character expressions
**Source Format**: ANI format with character-specific data
**Target Format**: Sprite sheet with character animation data
**Conversion Requirements**:
- Extract character-specific animation frames
- Convert facial expression sequences
- Generate timing data for dialogue synchronization
- Handle different character states and emotions
- Maintain consistent sizing and positioning

## Conversion Process

### 1. Format Analysis Phase
- Validate ANI file structure and headers
- Extract animation properties and metadata
- Identify frame count and sequence information
- Determine animation type and intended use
- Check for special properties or effects

### 2. Frame Extraction Phase
- Parse individual animation frames
- Extract frame timing and sequence data
- Handle frame compression and encoding
- Convert palette and color information
- Maintain transparency and special effects

### 3. Sprite Sheet Generation Phase
- Combine frames into efficient sprite sheets
- Generate texture atlas metadata
- Apply appropriate compression and quality settings
- Handle different frame sizes and layouts
- Optimize for GPU texture memory usage

### 4. Animation Data Generation Phase
- Create Godot Animation resources
- Generate frame sequence and timing data
- Handle loop and playback properties
- Integrate with Godot's animation system
- Create material definitions for special effects

## Feature-Based Directory Structure
Following Godot's recommended directory structure:
```
/animations/
├── effects/               # Effect animations
│   ├── explosions/        # Explosion animations
│   │   ├── small/
│   │   ├── medium/
│   │   └── large/
│   ├── weapons/            # Weapon effect animations
│   │   ├── lasers/
│   │   ├── missiles/
│   │   └── beams/
│   └── engine/             # Engine animations
│       ├── thrusters/
│       ├── afterburners/
│       └── glides/
├── ui/                    # UI animations
│   ├── menus/             # Menu animations
│   │   ├── transitions/
│   │   ├── buttons/
│   │   └── sliders/
│   ├── hud/                # HUD animations
│   │   ├── gauges/
│   │   ├── indicators/
│   │   └── alerts/
│   └── transitions/        # UI transition animations
│       ├── fades/
│       ├── slides/
│       └── wipes/
├── characters/            # Character animations
│   ├── portraits/          # Pilot portraits
│   │   ├── blair/
│   │   ├── manor/
│   │   └── angel/
│   └── expressions/        # Character expressions
│       ├── happy/
│       ├── sad/
│       └── angry/
└── particles/             # Particle animations
    ├── explosions/        # Particle explosion effects
    ├── weapons/            # Particle weapon effects
    └── environment/       # Environmental particle effects
```

## Entity Integration
Animations integrate with entity scenes in `/entities/` directories:
- Effect entities reference animations from `/animations/effects/`
- Weapon entities reference animations from `/animations/weapons/`
- Ship entities reference engine animations from `/animations/engine/`
- UI components reference animations from `/animations/ui/`

## System Integration
Animations integrate with Godot systems in `/systems/` directories:
- `/systems/graphics/` - Visual effect animations
- `/systems/weapon_control/` - Weapon effect animations
- `/systems/audio/` - Audio-synchronized animations
- `/systems/ai/` - AI behavior animations
- `/systems/mission_control/` - Mission-specific animations

## UI Integration
Animations integrate with UI components in `/ui/` directories:
- `/ui/main_menu/` - Menu transition animations
- `/ui/hud/` - HUD element animations
- `/ui/briefing/` - Briefing transition animations
- `/ui/debriefing/` - Debriefing feedback animations

## Closely Related Assets
- Particle effect definitions that use animated textures from `/data/effects/`
- Mission events that trigger specific animations from `/missions/{campaign}/{mission}/`
- UI layout files that reference animated elements from `/ui/{component}/`
- Sound files that synchronize with animation timing from `/audio/`

## Entity Asset Organization
Each entity in `/entities/` contains references to relevant animations:
- Effect entities reference textures from `/animations/effects/`
- Weapon entities reference textures from `/animations/weapons/`
- Ship entities reference engine animations from `/animations/engine/`
- UI components reference animations from `/animations/ui/`

## Common Shared Assets
- Standard explosion and impact effect animations from `/animations/effects/explosions/`
- Common UI transition and feedback animations from `/animations/ui/transitions/`
- Shared engine glow and thruster animations from `/animations/engine/thrusters/`
- Standard weapon firing and impact effects from `/animations/weapons/`
- Common HUD element animations for status feedback from `/animations/ui/hud/`
- Shared debris animations for destruction effects from `/animations/particles/explosions/`
- Standard shield and hull damage animations from `/animations/effects/`
- Common cockpit and interior animations from `/animations/characters/portraits/`