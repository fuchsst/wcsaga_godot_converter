# PCX Files Conversion Requirements

## Overview
PCX (PC Paintbrush) files contain textures and UI graphics used throughout Wing Commander Saga. These legacy image files need to be converted to modern formats compatible with Godot (WebP for textures, PNG for UI elements), following Godot's feature-based organization principles and the hybrid model defined in our project structure.

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

## Directory Structure Alignment
Following the Godot project structure defined in directory_structure.md and the hybrid organizational model:

### Assets Directory Structure (Global Assets)
Global texture assets that follow the "Global Litmus Test" principle: "If I delete three random features, is this asset still needed?"

```
assets/
├── textures/              # Shared texture files
│   ├── ui/                # Generic UI elements
│   │   ├── hud/           # HUD elements
│   │   ├── menus/         # Menu backgrounds
│   │   └── icons/         # UI icons
│   ├── effects/           # Particle textures used by multiple effects
│   │   ├── explosions/    # Explosion effects
│   │   ├── fireballs/     # Fireball effects
│   │   └── energy/        # Energy effects
│   ├── particles/         # Particle textures
│   │   ├── engine/        # Engine trails
│   │   ├── weapons/       # Weapon effects
│   │   └── debris/        # Debris effects
│   └── fonts/             # Font textures
│       ├── interface/     # Interface fonts
│       └── mission/       # Mission briefing fonts
└── animations/            # Shared animation files
    ├── ui/                # UI animations
    └── effects/           # Generic effect animations
```

### Features Directory Structure (Feature-Specific Assets)
Feature-specific textures that are closely tied to particular features and follow the co-location principle:

```
features/
├── fighters/              # Fighter ship entities
│   ├── confed_rapier/     # Raptor fighter - all files together
│   │   ├── rapier_diffuse.webp    # Diffuse texture
│   │   ├── rapier_normal.webp     # Normal map
│   │   └── rapier_specular.webp   # Specular map
│   └── kilrathi_dralthi/  # Dralthi fighter
│       ├── dralthi_diffuse.webp   # Diffuse texture
│       ├── dralthi_normal.webp    # Normal map
│       └── dralthi_specular.webp  # Specular map
├── weapons/               # Weapon entities
│   ├── ion_cannon/        # Ion cannon weapon
│   │   ├── ion_cannon.webp        # Weapon texture
│   │   ├── ion_muzzle.webp        # Muzzle flash texture
│   │   └── ion_trail.webp         # Projectile trail texture
│   └── javelin_missile/   # Javelin missile weapon
│       ├── javelin_missile.webp   # Weapon texture
│       └── javelin_trail.webp     # Projectile trail texture
├── effects/               # Effect entities
│   ├── explosion/         # Explosion effect
│   │   ├── explosion_fire.webp    # Fire texture
│   │   └── explosion_smoke.webp   # Smoke texture
│   └── fireball/          # Fireball effect
│       ├── fireball_texture.webp  # Fireball texture
│       └── fireball_glow.webp     # Glow texture
├── environment/           # Environmental objects
│   ├── asteroid/          # Asteroid object
│   │   └── asteroid_diffuse.webp  # Diffuse texture
│   └── nebula/            # Nebula effect
│       └── nebula_texture.webp    # Nebula texture
└── ui/                    # UI feature elements
    ├── main_menu/         # Main menu interface
    │   ├── background.png         # Background graphic
    │   └── buttons/               # Button graphics
    │       ├── normal.png         # Normal button state
    │       ├── hover.png          # Hover button state
    │       └── pressed.png        # Pressed button state
    ├── hud/               # Heads-up display
    │   ├── gauges/                # HUD gauges
    │   │   ├── speed_gauge.png    # Speed gauge
    │   │   └── shield_gauge.png   # Shield gauge
    │   └── indicators/            # HUD indicators
    │       ├── target_box.png     # Target box
    │       └── warning_icon.png   # Warning icon
    └── tech_database/     # Technical database
        ├── ship_entries/          # Ship entry graphics
        └── weapon_entries/        # Weapon entry graphics
```

## Integration Points

### Data Converter Output Mapping
- Ship textures → Converted to WebP and placed in `/features/fighters/{ship}/` or `/assets/textures/ships/` based on usage
- UI graphics → Converted to PNG and placed in `/features/ui/{component}/` or `/assets/textures/ui/` based on usage
- Effect textures → Converted to WebP/PNG and placed in `/features/effects/{effect}/` or `/assets/textures/effects/` based on usage
- Particle textures → Converted to WebP/PNG and placed in `/features/{category}/` or `/assets/textures/particles/` based on usage
- Font graphics → Converted to appropriate formats and placed in `/features/ui/_shared/fonts/` or `/assets/textures/fonts/`

### Resource References
- **Feature-specific textures** are referenced directly by entity scenes in `/features/`
- **Global textures** are referenced by multiple features and UI components
- **Material definitions** reference texture paths for proper rendering
- **Particle systems** reference particle textures for visual effects
- **UI components** reference UI graphics for interface rendering

## Relationship to Other Assets

### Closely Related Assets
- POF model files that reference these textures and are converted to `/features/{category}/{entity}/{entity}.glb`
- Animation sequence files (.ani) that use texture frames and are converted to sprite sheets in `/assets/animations/` or `/features/{category}/{entity}/`
- Particle effect definitions that specify texture usage from `/assets/data/effects/`
- UI layout files that reference specific graphics from `/features/ui/{component}/`

### Entity Asset Organization
Each entity in `/features/` contains references to relevant textures:
- 3D models reference textures from their own feature directory or `/assets/textures/` for shared assets
- Weapon entities reference textures from `/features/weapons/{weapon}/` or shared directories
- Effect entities reference textures from `/features/effects/{effect}/` or shared directories
- UI components reference textures from `/features/ui/{component}/` or `/assets/textures/ui/`

### Common Shared Assets
- Standard HUD element graphics used across different UI screens from `/assets/textures/ui/hud/`
- Common explosion and impact effect textures from `/assets/textures/effects/explosions/`
- Shared UI button and control graphics from `/assets/textures/ui/icons/`
- Standard font graphics for consistent text rendering from `/assets/textures/fonts/interface/`
- Common engine glow and thruster effect textures from `/assets/textures/particles/engine/`
- Shared debris models for destruction effects from `/assets/textures/particles/debris/`

This structure follows the hybrid approach where truly global, context-agnostic assets are organized in `/assets/`, while feature-specific assets are co-located with their respective features in `/features/`. The guiding principle is: "If I delete three random features, is this asset still needed?" If yes, it belongs in `/assets/`; if only needed by specific features, it belongs in those feature directories.