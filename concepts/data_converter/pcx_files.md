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
│   │   ├── backgrounds/   # Background graphics
│   │   ├── buttons/       # Button graphics
│   │   ├── gauges/        # Gauge graphics
│   │   ├── indicators/    # Indicator graphics
│   │   ├── icons/         # Icon graphics
│   │   ├── fonts/         # Font graphics
│   │   ├── cursors/       # Cursor graphics
│   │   └── animations/    # UI animation frames
│   └── effects/           # Particle textures used by multiple effects
│       ├── weapons/       # Generic weapon effect textures
│       │   ├── muzzle_flashes/    # Muzzle flash textures
│       │   ├── trails/            # Projectile trail textures
│       │   └── explosions/        # Explosion effect textures
│       └── particles/     # Generic particle textures
│           ├── engine/    # Engine trail effects
│           ├── debris/    # Debris effects
│           └── energy/    # Energy effects
└── animations/            # Shared animation files
    ├── ui/                # UI animations
    │   ├── transitions/   # Screen transitions
    │   ├── buttons/       # Button animations
    │   ├── gauges/        # Gauge animations
    │   ├── indicators/    # Indicator animations
    │   └── menus/         # Menu animations
    └── effects/           # Generic effect animations
        └── weapons/       # Weapon effect animations
            ├── muzzle_flashes/    # Muzzle flash animations
            ├── trails/            # Projectile trail animations
            └── explosions/        # Explosion animations
```

### Features Directory Structure (Feature-Specific Assets)
Feature-specific textures that are closely tied to particular features and follow the co-location principle:

```
features/
├── fighters/              # Fighter ship entities
│   ├── confed_arrow/      # F-27B Arrow fighter - all files together
│   │   ├── arrow_diffuse.webp     # Diffuse texture
│   │   ├── arrow_normal.webp      # Normal map
│   │   └── arrow_specular.webp    # Specular map
│   ├── confed_rapier/     # F-44B Rapier fighter
│   │   ├── rapier_diffuse.webp    # Diffuse texture
│   │   ├── rapier_normal.webp     # Normal map
│   │   └── rapier_specular.webp   # Specular map
│   ├── kilrathi_dralthi/  # Dralthi fighter
│   │   ├── dralthi_diffuse.webp   # Diffuse texture
│   │   ├── dralthi_normal.webp    # Normal map
│   │   └── dralthi_specular.webp  # Specular map
│   └── _shared/           # Shared fighter assets
│       ├── cockpits/      # Shared cockpit textures
│       └── effects/       # Shared fighter effects
│           ├── engine_trail.webp
│           └── shield_effect.webp
├── capital_ships/         # Capital ship entities
│   ├── tcs_behemoth/      # TCS Behemoth capital ship
│   │   ├── behemoth_diffuse.webp  # Diffuse texture
│   │   ├── behemoth_normal.webp   # Normal map
│   │   └── behemoth_specular.webp # Specular map
│   └── _shared/           # Shared capital ship assets
│       ├── bridge_models/ # Shared bridge textures
│       └── turret_models/ # Shared turret textures
├── weapons/               # Weapon entities
│   ├── ion_cannon/        # Ion cannon weapon
│   │   ├── ion_cannon.webp        # Weapon texture
│   │   ├── ion_muzzle.webp        # Muzzle flash texture
│   │   └── ion_trail.webp         # Projectile trail texture
│   ├── javelin_missile/   # Javelin missile weapon
│   │   ├── javelin_missile.webp   # Weapon texture
│   │   └── javelin_trail.webp     # Projectile trail texture
│   └── _shared/           # Shared weapon assets
│       ├── muzzle_flashes/        # Shared muzzle flash effects
│       ├── impact_effects/        # Shared impact effects
│       └── explosion_effects/     # Shared explosion effects
├── effects/               # Effect entities
│   ├── explosion/         # Explosion effect
│   │   ├── explosion_fire.webp    # Fire texture
│   │   └── explosion_smoke.webp   # Smoke texture
│   ├── fireball/          # Fireball effect
│   │   ├── fireball_texture.webp  # Fireball texture
│   │   └── fireball_glow.webp     # Glow texture
│   └── _shared/           # Shared effect assets
│       ├── particle_textures/     # Shared particle effects
│       └── shader_effects/        # Shared shader effects
├── environment/           # Environmental objects
│   ├── asteroid/          # Asteroid object
│   │   └── asteroid_diffuse.webp  # Diffuse texture
│   ├── nebula/            # Nebula effect
│   │   └── nebula_texture.webp    # Nebula texture
│   └── _shared/           # Shared environment assets
│       ├── debris/        # Space debris textures
│       └── environment/   # Environmental textures
└── ui/                    # UI feature elements
    ├── main_menu/         # Main menu interface
    │   ├── background.png         # Background graphic
    │   └── buttons/               # Button graphics
    │       ├── normal.png         # Normal button state
    │       ├── hover.png          # Hover button state
    │       └── pressed.png        # Pressed button state
    ├── hud/               # Heads-up display
    │   ├── gauges/                # HUD gauges
    │   │   ├── speed/             # Speed gauge elements
    │   │   ├── shields/           # Shield gauge elements
    │   │   ├── weapons/           # Weapon gauge elements
    │   │   └── fuel/              # Fuel gauge elements
    │   └── indicators/            # HUD indicators
    │       ├── targets/           # Target indicators
    │       ├── warnings/          # Warning indicators
    │       └── status/            # Status indicators
    ├── briefing/          # Briefing interface
    │   ├── background.png         # Background graphic
    │   ├── text_display/          # Text display area
    │   └── mission_map/           # Mission map area
    ├── debriefing/        # Debriefing interface
    │   ├── background.png         # Background graphic
    │   ├── results_display/       # Results display area
    │   └── statistics/            # Statistics display
    ├── tech_database/     # Technical database
    │   ├── backgrounds/           # Background graphics
    │   ├── ship_entries/          # Ship entry graphics
    │   └── weapon_entries/        # Weapon entry graphics
    └── _shared/           # Shared UI assets
        ├── fonts/         # UI fonts
        ├── icons/         # UI icons
        ├── themes/        # UI themes
        ├── cursors/       # Cursor graphics
        └── components/    # Reusable UI components
            ├── buttons/   # Button components
            ├── sliders/   # Slider components
            ├── checkboxes/# Checkbox components
            ├── dropdowns/ # Dropdown components
            ├── text_fields/# Text field components
            └── lists/     # List components
```

## Integration Points

### Data Converter Output Mapping
- **Fighter ship textures** → Converted to WebP and placed in `/features/fighters/{ship_name}/` for feature-specific textures or `/features/fighters/_shared/` for shared fighter assets
- **Capital ship textures** → Converted to WebP and placed in `/features/capital_ships/{ship_name}/` for feature-specific textures or `/features/capital_ships/_shared/` for shared capital ship assets
- **Weapon textures** → Converted to WebP and placed in `/features/weapons/{weapon_name}/` for feature-specific textures or `/features/weapons/_shared/` for shared weapon assets
- **UI graphics** → Converted to PNG and placed in `/features/ui/{component}/` for feature-specific UI elements or `/assets/textures/ui/` for truly global UI assets
- **Effect textures** → Converted to WebP/PNG and placed in `/features/effects/{effect_name}/` for feature-specific effects or `/assets/textures/effects/` for global effect assets
- **Particle textures** → Converted to WebP/PNG and placed in appropriate feature directories or `/assets/textures/effects/particles/` for shared particle assets
- **Font graphics** → Converted to appropriate formats and placed in `/features/ui/_shared/fonts/` for UI-specific fonts or `/assets/textures/ui/fonts/` for global font assets

### Resource References
- **Feature-specific textures** are referenced directly by entity scenes in `/features/`
- **Global textures** are referenced by multiple features and UI components
- **Material definitions** reference texture paths for proper rendering
- **Particle systems** reference particle textures for visual effects
- **UI components** reference UI graphics for interface rendering

## Relationship to Other Assets

### Closely Related Assets
- **POF model files** that reference these textures and are converted to:
  - `/features/fighters/{ship_name}/{ship_name}.glb` for fighter ships
  - `/features/capital_ships/{ship_name}/{ship_name}.glb` for capital ships
  - `/features/weapons/projectiles/{projectile_name}/{projectile_name}.glb` for weapon projectiles
- **Animation sequence files (.ani)** that use texture frames and are converted to sprite sheets in:
  - `/assets/animations/` for global animations
  - `/features/{category}/{entity_name}/` for feature-specific animations
- **Particle effect definitions** that specify texture usage from `/assets/textures/effects/` or feature-specific directories
- **UI layout files** that reference specific graphics from `/features/ui/{component}/` or shared UI directories

### Entity Asset Organization
Each entity in `/features/` contains references to relevant textures following the co-location principle:
- **Fighter ships** reference textures from `/features/fighters/{ship_name}/` or `/features/fighters/_shared/` for shared fighter assets
- **Capital ships** reference textures from `/features/capital_ships/{ship_name}/` or `/features/capital_ships/_shared/` for shared capital ship assets
- **Weapon entities** reference textures from `/features/weapons/{weapon_name}/` or `/features/weapons/_shared/` for shared weapon assets
- **Effect entities** reference textures from `/features/effects/{effect_name}/` or `/features/effects/_shared/` for shared effect assets
- **UI components** reference textures from `/features/ui/{component}/` or `/features/ui/_shared/` for shared UI assets
- **Environmental objects** reference textures from `/features/environment/{object_name}/` or `/features/environment/_shared/` for shared environmental assets

### Global Shared Assets (Assets Directory)
Assets that pass the "Global Litmus Test" and are truly context-agnostic:
- **Standard UI elements** used across multiple features from `/assets/textures/ui/`
- **Generic weapon effect textures** used by multiple weapon types from `/assets/textures/effects/weapons/`
- **Common particle textures** used by multiple effects from `/assets/textures/effects/particles/`
- **Global UI animations** used across multiple UI features from `/assets/animations/ui/`
- **Shared effect animations** used by multiple effect features from `/assets/animations/effects/`

### Semi-Global Shared Assets (_shared Directories)
Assets shared within specific feature categories but not globally needed:
- **Shared fighter assets** like cockpit textures in `/features/fighters/_shared/cockpits/`
- **Shared capital ship assets** like bridge components in `/features/capital_ships/_shared/bridge_models/`
- **Shared weapon assets** like muzzle flash effects in `/features/weapons/_shared/muzzle_flashes/`
- **Shared UI components** like button styles in `/features/ui/_shared/components/buttons/`
- **Shared effect assets** like particle textures in `/features/effects/_shared/particle_textures/`

This structure follows the hybrid approach where truly global, context-agnostic assets are organized in `/assets/`, semi-global assets shared within feature categories use `/_shared/` directories, and feature-specific assets are co-located with their respective features in `/features/`. The guiding principle is: "If I delete three random features, is this asset still needed?" If yes, it belongs in `/assets/`; if only needed by a specific feature category, it belongs in that category's `/_shared/` directory; if only needed by specific features, it belongs in those feature directories.