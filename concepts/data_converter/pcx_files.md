# PCX Files Conversion Requirements

## Overview
PCX (PC Paintbrush) files contain textures and UI graphics used throughout Wing Commander Saga. These legacy image files need to be converted to modern formats compatible with Godot (WebP for textures, PNG for UI elements), following Godot's feature-based organization principles.

## File Types and Conversion Requirements

### Ship Textures
**Purpose**: Surface materials for 3D models
**Source Format**: PCX format with 8-bit palette
**Target Format**: WebP (lossy) with embedded mipmaps
**Conversion Requirements**:
- Convert 256-color palette to 24-bit RGB
- Generate mipmaps for different LOD levels
- Apply appropriate compression settings for performance
- Handle texture wrapping modes (repeat, clamp)
- Maintain aspect ratios and UV mapping compatibility

### User Interface Graphics
**Purpose**: HUD elements, menu backgrounds, and UI components
**Source Format**: PCX format with transparency
**Target Format**: PNG with alpha channel
**Conversion Requirements**:
- Preserve exact pixel colors for UI consistency
- Convert transparency using color key or alpha channel
- Maintain crisp edges for text and icons
- Handle different UI scaling factors
- Organize into texture atlases where appropriate

### Particle Effects
**Purpose**: Visual effects like explosions, engine trails, and weapon impacts
**Source Format**: PCX format with special effects properties
**Target Format**: WebP (lossy) or PNG based on requirements
**Conversion Requirements**:
- Convert additive blend properties to material settings
- Handle animation frame sequences
- Maintain transparency and blending modes
- Optimize for real-time particle systems
- Preserve special lighting properties

### Animation Frames
**Purpose**: Sprites for animated sequences
**Source Format**: Multiple PCX files forming animation sequences
**Target Format**: Atlas textures with animation data
**Conversion Requirements**:
- Combine frames into efficient texture atlases
- Generate animation metadata for frame timing
- Handle different frame rates and loop behaviors
- Maintain consistent sizing and positioning
- Optimize for Godot's animation system

### Font Graphics
**Purpose**: In-game text rendering
**Source Format**: Specialized PCX font files
**Target Format**: Font resources or texture atlases
**Conversion Requirements**:
- Parse character mappings and spacing information
- Convert to Godot's dynamic font system
- Maintain kerning and line spacing properties
- Handle multiple font sizes and styles
- Preserve anti-aliasing and readability

## Conversion Process

### 1. Format Analysis Phase
- Validate PCX file headers and structure
- Extract palette and image dimensions
- Identify transparency methods (color key vs. alpha)
- Determine intended use (texture, UI, effect)
- Check for special properties or metadata

### 2. Color Conversion Phase
- Convert paletted images to RGB/RGBA
- Handle color key transparency to alpha channel
- Apply gamma correction if needed
- Optimize color depth for target format
- Preserve important visual details

### 3. Optimization Phase
- Generate appropriate mipmaps for textures
- Apply compression based on image content
- Optimize for GPU texture memory layout
- Handle different quality requirements
- Batch process related image sets

### 4. Format Export Phase
- Export to WebP for 3D textures with appropriate settings
- Export to PNG for UI elements with full quality
- Generate texture atlas metadata where applicable
- Create material definitions for special effects
- Validate exported files for quality and compatibility

## Feature-Based Directory Structure
Following Godot's recommended directory structure:
```
/textures/
├── ships/                 # Ship textures
│   ├── terran/            # Terran ship textures
│   │   ├── fighter/
│   │   ├── bomber/
│   │   └── capital/
│   ├── kilrathi/          # Kilrathi ship textures
│   │   ├── fighter/
│   │   ├── bomber/
│   │   └── capital/
│   └── pirate/            # Pirate ship textures
│       ├── fighter/
│       └── capital/
├── ui/                    # UI graphics
│   ├── hud/               # HUD elements
│   │   ├── gauges/
│   │   ├── indicators/
│   │   └── displays/
│   ├── menus/             # Menu backgrounds
│   │   ├── main/
│   │   ├── options/
│   │   └── campaign/
│   └── icons/             # UI icons
│       ├── weapons/
│       ├── ships/
│       └── systems/
├── effects/               # Effect textures
│   ├── explosions/         # Explosion effects
│   ├── fireballs/         # Fireball effects
│   └── energy/            # Energy effects
├── particles/             # Particle textures
│   ├── engine/            # Engine trails
│   ├── weapons/            # Weapon effects
│   └── debris/            # Debris effects
├── animations/           # Animation frames
│   ├── ui/                # UI animations
│   └── effects/           # Effect animations
└── fonts/                 # Font graphics
    ├── interface/          # Interface fonts
    └── mission/            # Mission briefing fonts
```

## Entity Integration
Textures integrate with entity scenes in `/entities/` directories:
- Ship textures link to `/entities/fighters/{faction}/{ship_name}/` directories
- Weapon textures link to `/entities/weapons/{weapon_name}/` directories
- Effect textures link to `/entities/effects/{effect_name}/` directories
- UI textures link to `/ui/{component}/` directories

## System Integration
Textures integrate with various Godot systems:
- `/systems/graphics/` - Rendering materials and shaders
- `/systems/particle/` - Particle effect textures
- `/systems/weapon_control/` - Weapon effect textures
- `/ui/` - UI element graphics
- `/entities/` - Entity surface materials

## Closely Related Assets
- POF model files that reference these textures and are converted to `/entities/` directories
- Animation sequence files (.ani) that use texture frames and are converted to `/animations/` directories
- Particle effect definitions that specify texture usage from `/data/effects/`
- UI layout files that reference specific graphics from `/ui/` directories

## Entity Asset Organization
Each entity in `/entities/` contains references to relevant textures:
- 3D models reference textures from `/textures/ships/` directories
- Weapon entities reference textures from `/textures/weapons/` directories
- Effect entities reference textures from `/textures/effects/` and `/textures/particles/` directories
- UI components reference textures from `/textures/ui/` directories

## Common Shared Assets
- Standard HUD element graphics used across different UI screens from `/textures/ui/hud/`
- Common explosion and impact effect textures from `/textures/effects/explosions/`
- Shared UI button and control graphics from `/textures/ui/icons/`
- Standard font graphics for consistent text rendering from `/textures/fonts/interface/`
- Common engine glow and thruster effect textures from `/textures/particles/engine/`
- Shared debris models for destruction effects from `/textures/particles/debris/`
- Standard shield mesh templates for similar ship types from `/data/ships/templates/`
- Common cockpit and interior model components from `/entities/fighters/templates/cockpit/`