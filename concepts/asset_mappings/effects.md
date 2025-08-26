# Effects Asset Mapping

## Overview
This document maps the effect definitions from various TBL files to their corresponding media assets in the Wing Commander Saga Hermes campaign, organized according to the Godot feature-based directory structure. It details how legacy formats will be converted to Godot-compatible formats during the migration process.

## Asset Types

### Fireball Effects
Fireball.tbl and related tables reference animated effects that will be converted to Godot-compatible formats:

**Effect Types:**
- exp04 - Used for the 4 little explosions before a ship explodes and subsystem explosions
- exp05 - Fighter explosion (custom)
- exp06 - Fighter explosion (custom)
- exp07 - Torpedo explosion
- exp08 - Ship explosion 1 (capships)
- exp10 - Ship explosion 2 (capships)
- exp12 - Fighter explosion (custom)
- rockEXP01 - Used when an asteroid explodes
- WarpMap01 - Used for warp in/out effects

**Legacy Format Assets:**
- Animation files (.ani): exp04.ani, exp05.ani, exp06.ani, exp07.ani, exp08.ani, exp10.ani, exp12.ani
- Texture sequences (.dds): exp04_*.dds, exp05_*.dds, exp06_*.dds, exp07_*.dds, exp08_*.dds, exp10_*.dds, exp12_*.dds
- Effect definitions (.eff): exp04.eff, exp05.eff, exp06.eff, exp07.eff, exp08.eff, exp10.eff, exp12.eff

### Weapon Effects
Weapon_expl.tbl references weapon impact effects that will be converted to Godot-compatible formats:

**Effect Types:**
- ExpMissileHit1 - Missile hits
- Subach_Impact
- Mekhu_Impact
- Maxim_Impact
- Vapula_Impact
- Shivan_Impact01, Shivan_Impact02
- Kayser_Impact
- Circe_Impact
- Lamprey_Impact
- Akheton_Impact
- MS_Impact
- Prometheus_Impact

**Legacy Format Assets:**
- Animation files (.ani): ExpMissileHit1.ani, Subach_Impact.ani, Mekhu_Impact.ani, etc.
- Texture sequences (.dds): ExpMissileHit1_*.dds, Subach_Impact_*.dds, Mekhu_Impact_*.dds, etc.
- Effect definitions (.eff): ExpMissileHit1.eff

### Particle Effects
Miscellaneous particle effects that will be converted to Godot-compatible formats:

**Effect Types:**
- ParticleSmoke01 - Particle smoke effects
- ParticleSmoke02 - Particle smoke effects
- shieldhit01a - Shield impact animations
- thruster01, thruster02, thruster03 - Thruster animations

**Legacy Format Assets:**
- Animation files (.ani): ParticleSmoke01.ani, ParticleSmoke02.ani, shieldhit01a.ani, thruster01.ani, etc.
- Texture sequences (.dds): ParticleSmoke01_*.dds, ParticleSmoke02_*.dds, shieldhit01a_*.dds, etc.
- Effect definitions (.eff): ParticleSmoke01.eff, ParticleSmoke02.eff

### Lighting Effects
Corona and sun effects that will be converted to Godot-compatible formats:

**Effect Types:**
- corona*.dds - Corona effects for suns and lights
- Sun*.dds - Sun textures
- Particle glow effects
- Laser/Photon glow effects

**Legacy Format Assets:**
- Textures (.dds): corona*.dds, Sun*.dds, Particle_Glow.dds, Laser_Glow.dds, Photon_Glow.dds

### HUD/Interface Effects
Interface animations that will be converted to Godot-compatible formats:

**Effect Types:**
- 2_*.ani - HUD animations (targeting, weapons, etc.)
- head-*.ani - Pilot head animations
- radar1.ani - Radar display

**Legacy Format Assets:**
- Animation files (.ani): 2_*.ani, head-*.ani, radar1.ani

## Format Conversion Process

### Legacy Formats to Godot Formats

**ANI Files (.ani)**
- Legacy animation format containing frame sequences and timing information
- Will be converted to Godot animation resources (.tres) or texture sequences
- Animation data will be parsed and converted to Godot's AnimationPlayer system
- Frame timing and sequence information preserved in effect data resources

**DDS Files (.dds)**
- Legacy DirectDraw Surface texture format with compression
- Will be converted to WebP format for Godot compatibility
- Mipmaps and compression settings preserved where appropriate
- Normal maps converted to Godot's expected format

**EFF Files (.eff)**
- Legacy effect definition files containing particle system parameters
- Will be converted to Godot effect resources (.tres)
- Parameters mapped to Godot's particle system properties
- Shader effects converted to Godot shader resources

**PCX Files (.pcx)**
- Legacy image format for older textures
- Will be converted to WebP format
- Used primarily for interface elements and some legacy textures

## Target Structure
Following the Godot project structure defined in directory_structure.md, effect assets are organized as follows:

### Features Directory Structure
Effect features are organized within the `/features/effects/` directory, following the feature-based organization principle where each effect is a self-contained entity with all its related assets.

```
features/
├── effects/                         # Effect feature entities (self-contained)
│   ├── explosion/                  # Explosion effect
│   │   ├── explosion.tscn          # Main explosion scene
│   │   ├── explosion.gd            # Explosion controller script
│   │   ├── explosion.tres          # Explosion data resource (converted from TBL entries)
│   │   └── textures/               # Effect-specific textures (converted from DDS)
│   │       ├── exp04_0000.webp
│   │       ├── exp04_0001.webp
│   │       └── ...                 # Additional explosion textures
│   ├── fireball/                   # Fireball effect
│   │   ├── fireball.tscn           # Fireball scene
│   │   ├── fireball.gd             # Fireball controller script
│   │   ├── fireball.tres           # Fireball data resource
│   │   └── textures/               # Effect-specific textures
│   │       ├── exp05_0000.webp
│   │       ├── exp05_0001.webp
│   │       └── ...                 # Additional fireball textures
│   ├── weapon_impact/              # Weapon impact effect
│   │   ├── weapon_impact.tscn      # Weapon impact scene
│   │   ├── weapon_impact.gd        # Weapon impact controller script
│   │   ├── weapon_impact.tres      # Weapon impact data resource
│   │   └── textures/               # Effect-specific textures
│   │       ├── impact_0000.webp
│   │       ├── impact_0001.webp
│   │       └── ...                 # Additional impact textures
│   ├── muzzle_flash/               # Muzzle flash effect
│   │   ├── muzzle_flash.tscn       # Muzzle flash scene
│   │   ├── muzzle_flash.gd         # Muzzle flash controller script
│   │   ├── muzzle_flash.tres       # Muzzle flash data resource
│   │   └── textures/               # Effect-specific textures
│   │       ├── flash_0000.webp
│   │       ├── flash_0001.webp
│   │       └── ...                 # Additional flash textures
│   ├── engine_trail/               # Engine trail effect
│   │   ├── engine_trail.tscn       # Engine trail scene
│   │   ├── engine_trail.gd         # Engine trail controller script
│   │   ├── engine_trail.tres       # Engine trail data resource
│   │   └── textures/               # Effect-specific textures
│   │       ├── trail_0000.webp
│   │       ├── trail_0001.webp
│   │       └── ...                 # Additional trail textures
│   ├── shield_impact/              # Shield impact effect
│   │   ├── shield_impact.tscn      # Shield impact scene
│   │   ├── shield_impact.gd        # Shield impact controller script
│   │   ├── shield_impact.tres      # Shield impact data resource (from Species_defs.tbl)
│   │   └── textures/               # Effect-specific textures
│   │       ├── shieldhit01a_0000.webp
│   │       ├── shieldhit01a_0001.webp
│   │       └── ...                 # Additional shield textures
│   ├── _shared/                    # Shared effect assets
│   │   ├── particle_textures/      # Shared particle textures
│   │   │   ├── generic_smoke.webp
│   │   │   ├── generic_sparks.webp
│   │   │   └── generic_glow.webp
│   │   └── shader_effects/         # Shared shader effects
│   │       ├── hologram_shader.tres
│   │       ├── energy_shader.tres
│   │       └── distortion_shader.tres
│   └── templates/                  # Effect templates
```

### Assets Directory Structure
Generic effect textures that are shared across multiple effects are organized in the global `/assets/textures/effects/` directory, following the "Global Litmus Test" principle.

```
assets/
├── textures/                        # Shared texture files
│   ├── effects/                    # Particle textures used by multiple effects
│   │   ├── particle_atlases/       # Particle texture atlases
│   │   ├── generic_effects/        # Generic effect textures
│   │   └── shader_materials/       # Shader material textures
│   └── ...                         # Other shared textures
├── animations/                      # Shared animation files
│   ├── effects/                    # Generic effect animations
│   └── ui/                         # UI animations
└── ...                             # Other asset types
```

## Example Mapping
For explosion effect exp04:
- fireball.tbl entry → /features/effects/explosion/explosion.tres (converted data resource)
- exp04.ani → Converted to animation data in /features/effects/explosion/explosion.tres
- exp04_*.dds → Converted to WebP format in /features/effects/explosion/textures/exp04_*.webp
- exp04.eff → Effect parameters integrated into /features/effects/explosion/explosion.tres

For weapon muzzle flash:
- weapon_expl.tbl entry → /features/effects/muzzle_flash/muzzle_flash.tres
- Custom animation data → Integrated into /features/effects/muzzle_flash/muzzle_flash.tres
- Associated textures → Converted to WebP in /features/effects/muzzle_flash/textures/

For generic smoke particle (shared across multiple effects):
- ParticleSmoke01_*.dds → Converted to WebP in /features/effects/_shared/particle_textures/generic_smoke.webp

For shield impact effect:
- Species_defs.tbl entry for Shield_Hit_ani → /features/effects/shield_impact/shield_impact.tres
- shieldhit01a.ani → Converted to animation data in /features/effects/shield_impact/shield_impact.tres
- shieldhit01a_*.dds → Converted to WebP in /features/effects/shield_impact/textures/shieldhit01a_*.webp

## Conversion Pipeline
1. **ANI Parser**: Custom parser to extract animation frame sequences and timing from .ani files
2. **DDS Converter**: Convert DDS textures to WebP format maintaining visual quality
3. **EFF Parser**: Extract particle system parameters from .eff files
4. **Resource Generator**: Create Godot .tres files with converted effect data
5. **Scene Builder**: Generate Godot scenes (.tscn) with appropriate particle systems and animations
6. **Validation**: Verify converted effects match original behavior and appearance