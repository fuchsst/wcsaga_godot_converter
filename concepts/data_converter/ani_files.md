# ANI Files Conversion Requirements

## Overview
ANI files contain animation sequences for effects, UI elements, and sprite-based animations in Wing Commander Saga. These custom format files need to be converted to Godot's animation system using sprite sheets and animation resources, following Godot's feature-based organization principles as defined in the project's directory structure and integration plan.

The conversion process will transform approximately 544 ANI files from the WCS Hermes campaign into Godot-compatible assets, organized according to the hybrid model that groups truly global assets in `/assets/` and feature-specific assets within their respective `/features/` directories.

## File Types and Conversion Requirements

### Sprite-Based Animations
**Purpose**: Explosions, weapon effects, and visual feedback
**Source Format**: ANI format with frame sequences
**Target Format**: Sprite sheet textures with animation data
**Conversion Requirements**:
- Extract individual animation frames preserving original timing
- Convert frames to WebP sprite sheet format for optimal performance
- Generate timing and frame sequence data as Godot Animation resources
- Handle loop properties and playback modes according to original behavior
- Maintain transparency and blending modes for visual fidelity

### User Interface Animations
**Purpose**: Animated menu elements and HUD effects (prefixed with "2_" in source)
**Source Format**: ANI format with UI-specific properties
**Target Format**: Animated texture resources with UI properties
**Conversion Requirements**:
- Preserve exact pixel positioning and sizing for pixel-perfect UI
- Convert UI-specific timing and triggers to match original interactions
- Handle different UI states and transitions with proper event integration
- Maintain crisp edges for interface clarity using appropriate filtering
- Integrate with Godot's UI animation system through AnimationPlayer nodes

### Particle Effect Animations
**Purpose**: Animated textures for particle systems (explosions, engine effects)
**Source Format**: ANI format with particle properties
**Target Format**: Animated texture atlases for particle systems
**Conversion Requirements**:
- Convert to efficient texture atlas format optimized for GPU rendering
- Generate particle emission timing data synchronized with visual effects
- Handle additive and blend mode properties for correct visual compositing
- Maintain frame rate compatibility with particle systems for smooth playback
- Optimize for real-time particle rendering with appropriate compression

### Character Animation Sequences
**Purpose**: Pilot portraits and character expressions (prefixed with "Head-" in source)
**Source Format**: ANI format with character-specific data
**Target Format**: Sprite sheet with character animation data
**Conversion Requirements**:
- Extract character-specific animation frames maintaining facial details
- Convert facial expression sequences preserving emotional context
- Generate timing data for dialogue synchronization in cutscenes
- Handle different character states and emotions with appropriate transitions
- Maintain consistent sizing and positioning for UI integration

### Engine Animations
**Purpose**: Thruster and engine glow effects (prefixed with "thruster" in source)
**Source Format**: ANI format with engine-specific properties
**Target Format**: Animated texture resources for engine effects
**Conversion Requirements**:
- Extract engine glow and particle effects maintaining visual intensity
- Convert thruster animations to match ship-specific engine characteristics
- Generate timing data synchronized with engine audio
- Handle different engine states (idle, acceleration, afterburner)
- Maintain proper scaling for different ship classes

## Conversion Process

### 1. Format Analysis Phase
- Validate ANI file structure and headers for data integrity
- Extract animation properties and metadata including frame dimensions
- Identify frame count and sequence information for timing calculations
- Determine animation type and intended use based on naming conventions
- Check for special properties or effects like additive blending

### 2. Frame Extraction Phase
- Parse individual animation frames preserving original palette information
- Extract frame timing and sequence data for accurate playback
- Handle frame compression and encoding maintaining visual quality
- Convert palette and color information to RGBA format
- Maintain transparency and special effects like glow maps

### 3. Sprite Sheet Generation Phase
- Combine frames into efficient sprite sheets minimizing texture memory usage
- Generate texture atlas metadata for frame lookup in Godot
- Apply appropriate compression and quality settings (WebP format)
- Handle different frame sizes and layouts with proper padding
- Optimize for GPU texture memory usage with power-of-two dimensions

### 4. Animation Data Generation Phase
- Create Godot Animation resources (.tres) with frame sequence data
- Generate frame sequence and timing data matching original playback
- Handle loop and playback properties according to source behavior
- Integrate with Godot's animation system using AnimationPlayer nodes
- Create material definitions for special effects like additive blending

## Directory Structure Alignment
Following the Godot project's hybrid organizational model defined in directory_structure.md:

### Assets Directory Structure
Truly global, context-agnostic animations organized in `/assets/` following the "Global Litmus Test":

```
assets/
├── animations/            # Shared animation files
│   ├── effects/           # Generic effect animations (shared across multiple features)
│   │   ├── explosions/    # Generic explosion animations (explode1.ani, exploAeA.ani, etc.)
│   │   ├── weapons/       # Generic weapon effect animations (lasermine.ani, etc.)
│   │   └── particles/     # Generic particle animations (thrusterparticle.ani, etc.)
│   └── ui/                # Shared UI animations
│       ├── hud/           # Generic HUD animations (2_targhit1.ani, 2_damage1.ani, etc.)
│       ├── menus/         # Generic menu animations (2_weapons1.ani, etc.)
│       └── transitions/   # Generic UI transition animations
└── textures/              # Shared texture files
    └── effects/           # Particle textures used by multiple effects
```

### Features Directory Structure
Feature-specific animations organized within `/features/` directories following the co-location principle:

```
features/
├── effects/               # Effect entities
│   ├── explosion/         # Explosion effect
│   │   ├── explosion.tscn # Main explosion scene
│   │   ├── explosion.gd   # Explosion controller script
│   │   ├── explosion.tres # Explosion data resource
│   │   └── textures/      # Effect-specific textures
│   │       └── {effect_name}_*.webp # Converted animation frames
│   ├── fireball/          # Fireball effect
│   │   ├── fireball.tscn  # Fireball scene
│   │   ├── fireball.gd    # Fireball controller script
│   │   ├── fireball.tres  # Fireball data resource
│   │   └── textures/      # Fireball textures
│   │       └── {effect_name}_*.webp # Converted animation frames
│   ├── weapon_impact/     # Weapon impact effect
│   │   ├── weapon_impact.tscn # Weapon impact scene
│   │   ├── weapon_impact.gd   # Weapon impact controller script
│   │   ├── weapon_impact.tres # Weapon impact data resource
│   │   └── textures/          # Impact textures
│   │       └── {effect_name}_*.webp # Converted animation frames
│   ├── _shared/           # Shared effect assets
│   │   └── particle_textures/ # Shared particle textures
│   │       └── generic_*.webp # Generic particle textures
│   └── templates/         # Effect templates
├── weapons/               # Weapon entities
│   ├── laser_cannon/      # Laser cannon weapon
│   │   ├── laser_cannon.tscn # Weapon scene
│   │   ├── laser_cannon.gd   # Weapon controller script
│   │   ├── laser_cannon.tres # Weapon data resource
│   │   └── textures/         # Weapon-specific textures
│   │       └── {effect_name}_*.webp # Converted animation frames
│   ├── _shared/           # Shared weapon assets
│   │   └── textures/      # Shared weapon textures
│   │       ├── muzzle_flashes/ # Shared muzzle flash animations
│   │       └── impact_effects/ # Shared impact effect animations
│   └── templates/         # Weapon templates
├── fighters/              # Fighter ship entities
│   ├── confed_rapier/     # Rapier fighter
│   │   ├── rapier.tscn    # Fighter scene
│   │   ├── rapier.gd      # Fighter controller script
│   │   ├── rapier.tres    # Fighter data resource
│   │   └── textures/      # Fighter-specific textures
│   │       └── {effect_name}_*.webp # Converted animation frames
│   ├── _shared/           # Shared fighter assets
│   │   └── effects/       # Shared fighter effects
│   │       └── engine/    # Engine animations
│   │           ├── thrusters/ # Thruster animations (thruster01.ani, etc.)
│   │           └── glows/    # Engine glow animations
│   └── templates/         # Fighter templates
└── ui/                    # UI feature elements
    ├── main_menu/         # Main menu interface
    │   ├── main_menu.tscn # Main menu scene
    │   ├── main_menu.gd   # Main menu script
    │   └── animations/    # Menu-specific animations
    │       └── {animation_name}.webp # Converted UI animations
    ├── hud/               # Heads-up display
    │   ├── player_hud.tscn # HUD scene
    │   ├── player_hud.gd   # HUD script
    │   └── animations/     # HUD-specific animations
    │       └── {animation_name}.webp # Converted UI animations
    ├── briefing/          # Briefing interface
    │   ├── briefing_screen.tscn # Briefing scene
    │   ├── briefing_screen.gd   # Briefing script
    │   └── animations/          # Briefing-specific animations
    │       └── {animation_name}.webp # Converted UI animations
    ├── _shared/           # Shared UI assets
    │   └── animations/    # Shared UI animations
    │       └── {animation_name}.webp # Converted shared UI animations
    └── templates/         # UI templates
```

## Entity Integration
Animations integrate with entity scenes following the feature-based organization:

### Effect Entities
- Reference converted animations from `/assets/animations/effects/` for truly global, shared effects
- Use feature-specific animations from `/features/effects/{effect}/textures/` for effect-specific animations
- Example: Explosion effects reference converted explode1.ani sprite sheets and animation data

### Weapon Entities
- Reference shared animations from `/features/weapons/_shared/textures/` for shared weapon effects
- Use weapon-specific animations from `/features/weapons/{weapon}/textures/` for weapon-specific animations
- Example: Laser weapons reference lasermine.ani converted assets in weapon-specific directories

### Ship Entities
- Reference shared engine animations from `/features/fighters/_shared/effects/engine/` for common engine effects
- Use ship-specific animations from `/features/fighters/{ship}/textures/` for ship-specific animations
- Example: Fighters reference thruster01.ani converted assets for engine effects

### UI Components
- Reference shared UI animations from `/assets/animations/ui/` for truly global UI animations
- Use component-specific animations from `/features/ui/{component}/animations/` for UI-specific animations
- Example: HUD elements reference 2_targhit1.ani and 2_damage1.ani converted assets

## System Integration
Animations integrate with Godot systems in `/scripts/` directories following the separation of concerns:

- `/scripts/entities/base_effect.gd` - Visual effect animation playback
- `/scripts/entities/base_weapon.gd` - Weapon effect animation synchronization
- `/scripts/audio/sound_manager.gd` - Audio-synchronized animation triggering
- `/scripts/mission/event_system.gd` - Mission event-triggered animations
- `/scripts/ui/ui_element.gd` - UI animation control and state management

## Campaign Integration
Animations integrate with campaign content in `/campaigns/` directories:

- Mission-specific cutscene animations stored with mission data
- Campaign intro/outro animations organized by campaign
- Dialogue-synchronized character animations integrated with voice acting

## Closely Related Assets
Animations have dependencies on other asset types requiring coordinated conversion:

- Particle effect definitions that use animated textures from `/assets/textures/effects/`
- Mission events that trigger specific animations from `/campaigns/{campaign}/missions/{mission}/`
- UI layout files that reference animated elements from `/features/ui/{component}/animations/`
- Sound files that synchronize with animation timing from `/assets/audio/sfx/`

## Asset Conversion Categories
Based on analysis of the 544 ANI files in the source assets, animations are categorized as:

### Weapon Effects (~50 files)
- Laser, missile, and projectile impact animations
- Muzzle flash and firing effect animations
- Weapon-specific visual feedback effects

### Explosions (~100 files)
- Ship destruction and damage effect animations
- Projectile impact and detonation effects
- Environmental explosion animations

### Engine Effects (~20 files)
- Thruster animations for different ship classes
- Engine glow and particle effects
- Afterburner and special propulsion effects

### UI Animations (~100 files)
- HUD element animations (targeting, damage indicators)
- Menu transition and feedback animations
- Technical database and loadout screen animations

### Character Portraits (~50 files)
- Pilot head animations for cutscenes
- Character expression and emotion animations
- Dialogue-synchronized facial animations

### Generic Effects (~200 files)
- Shield hit and damage effect animations
- Environmental and atmospheric effects
- Miscellaneous visual feedback animations

## Conversion Pipeline Integration
The ANI conversion process integrates with the overall asset conversion pipeline:

1. **ANI Parser**: Custom parser to extract animation frame sequences and timing
2. **Image Converter**: Convert extracted frames to WebP format maintaining visual quality
3. **Sprite Sheet Generator**: Combine frames into optimized texture atlases
4. **Animation Data Generator**: Create Godot .tres files with converted animation data
5. **Resource Integration**: Link converted animations with appropriate entity features
6. **Validation**: Verify converted animations match original behavior and appearance

## Quality Assurance
Converted animations must maintain fidelity to original source material:

- Frame timing accuracy within 16ms tolerance (1 frame at 60fps)
- Visual quality preservation with proper transparency and blending
- Playback behavior matching original loop and trigger conditions
- Performance optimization for real-time playback on target hardware
- Consistent integration with corresponding audio and gameplay events