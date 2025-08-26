# Weapons Asset Mapping

## Overview
This document maps the weapon definitions from weapons.tbl and weapon_expl.tbl to their corresponding media assets in the Wing Commander Saga Hermes campaign, organized according to the Godot feature-based directory structure. The mapping follows the hybrid model where truly global weapon assets are organized in the `/assets/` directory, while feature-specific weapon elements are co-located with their respective features.

## Asset Types

### 3D Models (.pof)
Weapons.tbl references POF files for projectile models:
- tcm_javelin.pof - Javelin projectile model
- tcm_dart.pof - Dart projectile model
- tcm_spiculum.pof - Spiculum projectile model
- tcm_lance.pof - Lance projectile model
- tcm_warhammer.pof - Warhammer projectile model
- misc_ghostmissile.pof - Ghost missile model

### Textures (.pcx/.dds)
Weapon textures referenced by POF models and weapon effects:
- Projectile-specific textures for visual appearance (e.g., tcm_javelin.dds, tcm_javelin-shine.dds)
- Glow and effect textures for weapon trails (e.g., Ion_Glow.DDS)
- Muzzle flash effects (e.g., Ion_Bitmap.DDS)
- Weapon icon textures (e.g., IconIon_0000.dds)

### Sounds (.wav)
Weapons.tbl references various audio files through sound indices:
- Firing sounds for each weapon type (referenced by $LaunchSnd index)
- Impact sounds for weapon hits (referenced by $ImpactSnd index)
- Flyby sounds for projectiles (referenced by $FlyBySnd index)
- Explosion sounds for warheads
- Reload/charging sounds
- Special effect sounds (e.g., EMP discharge)

### Animations (.ani)
Animated effects for weapons:
- Muzzle flash animations
- Projectile trail effects
- Impact explosion animations (e.g., Mekhu_Impact.ani, explode1.ani)
- Charging/arming sequences
- Technology database animations (e.g., 2_tech_javelin.ani, 2_tech_ion.ani)
- Loadout screen animations (e.g., 2_LoadoutIon.ani)

### Explosion Definitions (.tbl)
Weapon_expl.tbl defines named explosion effects that map to animation files:
- Mekhu_Impact - Ion cannon impact explosion
- Subach_Impact - Subach cannon impact explosion
- ExpMissileHit1 - Generic missile hit explosion
- exp20 - Flak explosion
- Various other named explosion effects for different weapon types

## Format Conversion Process

### Legacy Formats to Godot Formats

**POF Files (.pof)**
- Legacy 3D model format for projectile models
- Will be converted to glTF format preserving model hierarchy
- Subobject structure and animation points maintained
- Converted textures to Godot-supported formats (WebP)

**DDS/PCX Files (.dds/.pcx)**
- Legacy texture formats for weapon visuals
- Will be converted to WebP format for better compression and Godot compatibility
- Mipmaps and compression settings preserved during conversion
- Alpha channels maintained for transparency effects

**ANI Files (.ani)**
- Legacy animation format for weapon effects
- Will be converted to sprite sheet animations or particle effects in Godot
- Animation frame sequences preserved during conversion
- Timing and looping properties maintained where appropriate

**TBL Files (.tbl)**
- Legacy configuration format for weapon definitions
- Will be converted to Godot resource files (.tres) for data-driven design
- Property mappings preserved with appropriate Godot data types
- Weapon statistics and behavior data maintained for gameplay systems

## Target Structure
Following the Godot project structure defined in directory_structure.md and the hybrid organizational model, weapon assets are organized as follows:

### Assets Directory Structure
Generic weapon assets that are shared across multiple features are organized in the global `/assets/` directory, following the "Global Litmus Test" principle: "If I delete three random features, is this asset still needed?"

```
assets/
├── audio/                         # Shared audio files
│   └── sfx/                       # Generic sound effects
│       ├── weapons/               # Weapon sound effects
│       │   ├── firing/            # Weapon firing sounds
│       │   ├── impacts/           # Weapon impact sounds
│       │   ├── explosions/        # Explosion sounds
│       │   └── flyby/             # Projectile flyby sounds
│       └── ui/                    # UI sound effects
├── textures/                      # Shared texture files
│   └── effects/                   # Particle textures used by multiple effects
│       ├── weapons/               # Generic weapon effect textures
│       │   ├── muzzle_flashes/    # Muzzle flash textures
│       │   ├── trails/            # Projectile trail textures
│       │   └── explosions/        # Explosion effect textures
│       └── ui/                    # Generic UI elements
└── animations/                    # Shared animation files
    └── effects/                   # Generic effect animations
        ├── weapons/               # Weapon effect animations
        │   ├── muzzle_flashes/    # Muzzle flash animations
        │   ├── trails/            # Projectile trail animations
        │   └── explosions/        # Explosion animations
        └── ui/                    # UI animations
```

### Features Directory Structure
Feature-specific weapon elements that are closely tied to particular weapons are organized within their respective feature directories, following the co-location principle where all files related to a single feature are grouped together.

```
features/
├── weapons/                       # Weapon entities (self-contained)
│   ├── ion_cannon/                # Ion cannon weapon
│   │   ├── ion_cannon.tscn        # Weapon scene
│   │   ├── ion_cannon.gd          # Weapon script
│   │   ├── ion_cannon.tres        # Weapon data resource
│   │   ├── ion_cannon.glb         # 3D model (if applicable)
│   │   ├── ion_cannon.webp        # Weapon texture
│   │   ├── ion_fire.ogg           # Firing sound
│   │   ├── ion_impact.ogg         # Impact sound
│   │   ├── ion_muzzle.webp        # Muzzle flash texture
│   │   └── ion_trail.webp         # Projectile trail texture
│   ├── javelin_missile/           # Javelin missile weapon
│   │   ├── javelin_missile.tscn   # Weapon scene
│   │   ├── javelin_missile.gd     # Weapon script
│   │   ├── javelin_missile.tres   # Weapon data resource
│   │   ├── javelin_missile.glb    # 3D model (converted from tcm_javelin.pof)
│   │   ├── javelin_missile.webp   # Weapon texture (converted from tcm_javelin.dds)
│   │   ├── javelin_fire.ogg       # Firing sound
│   │   ├── javelin_impact.ogg     # Impact sound
│   │   └── javelin_trail.webp     # Projectile trail texture
│   ├── projectiles/               # Projectile entities
│   │   ├── ion_bolt/              # Ion bolt projectile
│   │   │   ├── ion_bolt.tscn      # Projectile scene
│   │   │   ├── ion_bolt.gd        # Projectile script
│   │   │   ├── ion_bolt.tres      # Projectile data resource
│   │   │   └── ion_bolt.webp      # Projectile texture
│   │   ├── javelin_projectile/    # Javelin projectile
│   │   │   ├── javelin_projectile.tscn # Projectile scene
│   │   │   ├── javelin_projectile.gd   # Projectile script
│   │   │   ├── javelin_projectile.tres # Projectile data resource
│   │   │   └── javelin_projectile.glb  # 3D model (converted from tcm_javelin.pof)
│   │   └── templates/             # Projectile templates
│   ├── _shared/                   # Shared weapon assets
│   │   ├── muzzle_flashes/        # Shared muzzle flash effects
│   │   ├── impact_effects/        # Shared impact effects
│   │   └── explosion_effects/     # Shared explosion effects
│   └── templates/                 # Weapon templates
└── effects/                       # Effect entities
    ├── explosion/                 # Explosion effect
    │   ├── explosion.tscn         # Effect scene
    │   ├── explosion.gd           # Effect script
    │   ├── explosion.tres         # Effect data resource
    │   ├── explosion_fire.webp    # Fire texture
    │   └── explosion_sound.ogg    # Explosion sound
    ├── _shared/                   # Shared effect assets
    │   ├── particle_textures/     # Shared particle effects
    │   └── shader_effects/        # Shared shader effects
    └── templates/                 # Effect templates

/scripts/                          # Reusable GDScript code and custom resources
├── entities/                      # Base entity scripts
│   └── base_weapon.gd             # Base weapon controller
└── weapons/                       # Weapon system scripts
    ├── weapon_system.gd           # Weapon management system
    ├── projectile_system.gd       # Projectile management system
    └── explosion_system.gd        # Explosion effect system

/autoload/                         # Singleton scripts (auto-loaded)
├── weapon_manager.gd              # Global weapon management system
└── audio_manager.gd               # Audio management system

/campaigns/                        # Campaign data and mission scenes
├── hermes/                        # Hermes campaign
│   └── weapon_data/               # Campaign-specific weapon data
│       ├── tech_database/         # Technology database entries
│       │   ├── ion_cannon.eff     # Ion cannon tech entry
│       │   └── javelin_missile.eff # Javelin missile tech entry
│       └── loadout_data/          # Loadout screen data
└── brimstone/                     # Brimstone campaign
    └── weapon_data/               # Campaign-specific weapon data
```

### Data Directory Structure
Weapon configuration data converted to Godot resources:

```
assets/
└── data/                          # Shared data resources
    └── weapons/                   # Weapon data resources
        ├── weapon_definitions/    # Weapon definition resources
        │   ├── ion_cannon.tres    # Ion cannon definition
        │   └── javelin_missile.tres # Javelin missile definition
        ├── projectile_data/       # Projectile data resources
        │   ├── ion_bolt.tres      # Ion bolt projectile data
        │   └── javelin_projectile.tres # Javelin projectile data
        └── explosion_data/        # Explosion effect data
            ├── mekhu_impact.tres  # Mekhu impact explosion data
            └── expmissile_hit.tres # Missile hit explosion data
```

## Data Conversion Strategy

### Configuration Files (.tbl)
Convert to Godot resources (.tres) organized appropriately:
- Weapon definitions from weapons.tbl to WeaponData resources
- Explosion definitions from weapon_expl.tbl to ExplosionData resources
- Use Godot's resource system for data-driven design with centralized management
- Preserve weapon statistics and behavior data with appropriate Godot data types

### 3D Models (.pof)
Convert to Godot-compatible formats:
- POF to glTF conversion tool preserving model hierarchy
- Maintain subobject structure and animation points
- Convert textures to Godot-supported formats (WebP)
- Preserve effect points for weapons, trails, and impacts

### Image Conversion Process
1. **DDS/PCX to WebP Converter**: Convert .dds and .pcx image files to WebP format with quality preservation
2. **Palette Preservation**: Maintain color palettes and transparency for accurate display
3. **Resolution Maintenance**: Preserve original resolutions for proper scaling
4. **Resource Generation**: Create Godot .tres files with converted image data
5. **Directory Organization**: Place converted image files in appropriate directories following the structure above
6. **Validation**: Verify converted images maintain original visual quality and properties

### Animation Conversion Process
1. **ANI to Sprite Sheet Converter**: Convert .ani animation files to sprite sheet animations with WebP format
2. **Frame Sequence Preservation**: Maintain animation frame sequences and timing properties
3. **Looping Properties**: Preserve looping and playback characteristics
4. **Resource Generation**: Create Godot .tres files with converted animation data
5. **Directory Organization**: Place converted animation files in appropriate directories following the structure above
6. **Validation**: Verify converted animations maintain original visual characteristics and timing

## Example Mapping

### For Ion Cannon weapon:
- weapons.tbl entry → /assets/data/weapons/weapon_definitions/ion_cannon.tres
- Ion_Bitmap.DDS → /features/weapons/ion_cannon/ion_cannon.webp
- Ion_Glow.DDS → /features/weapons/ion_cannon/ion_glow.webp
- 2_tech_ion.ani → /campaigns/hermes/weapon_data/tech_database/ion_cannon.webp
- LoadoutIon.ani → /campaigns/hermes/weapon_data/loadout_data/ion_cannon.webp
- Mekhu_Impact.ani → /features/weapons/_shared/impact_effects/mekhu_impact.webp
- snd_80.wav (LaunchSnd) → /features/weapons/ion_cannon/ion_fire.ogg
- snd_85.wav (ImpactSnd) → /features/weapons/ion_cannon/ion_impact.ogg
- IconIon_*.dds → /campaigns/hermes/weapon_data/loadout_data/icon_ion.webp

### For Javelin Missile weapon:
- weapons.tbl entry → /assets/data/weapons/weapon_definitions/javelin_missile.tres
- tcm_javelin.pof → /features/weapons/projectiles/javelin_projectile/javelin_projectile.glb
- tcm_javelin.dds → /features/weapons/projectiles/javelin_projectile/javelin_missile.webp
- tcm_javelin-shine.dds → /features/weapons/projectiles/javelin_projectile/javelin_shine.webp
- 2_tech_javelin.ani → /campaigns/hermes/weapon_data/tech_database/javelin_missile.webp
- snd_87.wav (LaunchSnd) → /features/weapons/javelin_missile/javelin_fire.ogg
- snd_88.wav (ImpactSnd) → /features/weapons/javelin_missile/javelin_impact.ogg
- IconJavelin.dds → /campaigns/hermes/weapon_data/loadout_data/icon_javelin.webp

### For Global Weapon Assets:
- explode1.ani → /assets/animations/effects/weapons/explosions/explode1.webp
- snd_ship_explode_1.wav → /assets/audio/sfx/weapons/explosions/ship_explode_1.ogg
- generic muzzle flash textures → /assets/textures/effects/weapons/muzzle_flashes/

## Relationship to Other Assets
Weapon assets are closely related to:
- **Ship System**: Weapons are mounted on and fired by ships, requiring integration with ship subsystems
- **Physics System**: Projectiles use Godot physics for movement and collision detection
- **Audio System**: Weapon sounds are organized by type and managed by the audio manager
- **Effect System**: Weapon effects (muzzle flashes, trails, impacts) use particle systems and animations
- **Game State System**: Weapon availability and ammunition are tracked in game state
- **UI System**: Weapon loadout and technology database screens display weapon information
- **Mission System**: Mission objectives may involve specific weapons or weapon usage
- **Weapon Manager**: Global weapon management system in `/autoload/weapon_manager.gd`
- **Weapon System Scripts**: Reusable weapon components and systems in `/scripts/weapons/`

This organization follows the hybrid approach where truly global weapon assets are organized in the `/assets/` directory following the "Global Litmus Test" principle, while feature-specific weapon elements are co-located with their respective features in the `/features/weapons/` directory. The structure maintains clear separation of concerns between different weapon types while ensuring easy access to all weapon assets needed for game features.