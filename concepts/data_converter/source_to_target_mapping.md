# Source Assets to Target Structure Mapping

## Overview
This document maps specific source assets from the Wing Commander Saga Hermes campaign to their corresponding target locations and formats in the Godot implementation, providing a clear reference for the conversion process. The mapping follows the feature-based organizational approach and hybrid model defined in `directory_structure.md` and `Godot_Project_Structure_Refinement.md`.

## Ship Assets Mapping

### Terran Confederation Ships

#### F-27B Arrow Fighter
**Source Assets**:
- `ships.tbl` - Ship class definition
- `arrow.pof` - 3D model
- `arrow.pcx` - Diffuse texture
- `arrow_normals.pcx` - Normal map
- `engine.wav` - Engine sound
- `weapon_mounts.ani` - Weapon effects

**Target Structure**:
Following the feature-based organization principle where "this is a self-contained 'thing' that can be placed in the game world":
```
/features/fighters/confed_arrow/
├── arrow.tscn                                     # Ship scene
├── arrow.gd                                       # Ship script
├── arrow.tres                                     # Ship instance data (converted from ships.tbl)
├── arrow.glb                                     # 3D model (converted from arrow.pof)
├── arrow_diffuse.webp                            # Diffuse texture (converted from arrow.pcx)
├── arrow_normal.webp                             # Normal map (converted from arrow_normals.pcx)
├── assets/                                        # Feature-specific assets
│   ├── sounds/                                    # Ship-specific sounds
│   │   ├── engine_loop.ogg                       # Engine sound (converted from engine.wav)
│   │   ├── maneuver.ogg                          # Maneuvering thrusters
│   │   └── afterburner.ogg                        # Afterburner sound
│   └── effects/                                   # Ship-specific visual effects
│       ├── thruster_particles.tscn                # Thruster particle effect
│       └── shield_effect.png                      # Shield visual effect
└── arrow_icon.png                                 # UI icon (converted from bicon-arrow.ani)
```

### Kilrathi Ships

#### Dralthi Fighter
**Source Assets**:
- `ships.tbl` - Ship class definition
- `dralthi.pof` - 3D model
- `dralthi.pcx` - Diffuse texture
- `dralthi_engine.wav` - Engine sound
- `dralthi_weapons.ani` - Weapon effects

**Target Structure**:
Following the feature-based organization principle:
```
/features/fighters/kilrathi_dralthi/
├── dralthi.tscn                                   # Ship scene
├── dralthi.gd                                     # Ship script
├── dralthi.tres                                   # Ship instance data (converted from ships.tbl)
├── dralthi.glb                                    # 3D model (converted from dralthi.pof)
├── dralthi_diffuse.webp                          # Diffuse texture (converted from dralthi.pcx)
├── assets/                                        # Feature-specific assets
│   ├── sounds/                                    # Ship-specific sounds
│   │   ├── engine_loop.ogg                       # Engine sound (converted from dralthi_engine.wav)
│   │   ├── maneuver.ogg                          # Maneuvering thrusters
│   │   └── afterburner.ogg                        # Afterburner sound
│   └── effects/                                   # Ship-specific visual effects
│       ├── thruster_particles.tscn                # Thruster particle effect
│       └── shield_effect.png                     # Shield visual effect
└── dralthi_icon.png                              # UI icon
```

## Weapon Assets Mapping

### Laser Weapons

#### Mk.II Laser Cannon
**Source Assets**:
- `weapons.tbl` - Weapon class definition
- `laser_cannon.pof` - 3D model (for projectiles)
- `laser_cannon.pcx` - Texture
- `laser_fire.wav` - Firing sound
- `laser_impact.wav` - Impact sound
- `laser_muzzle.ani` - Muzzle effect
- `laser_bolt.ani` - Projectile effect

**Target Structure**:
Following the feature-based organization principle:
```
/features/weapons/laser_cannon/
├── laser_cannon.tscn                              # Weapon scene
├── laser_cannon.gd                                # Weapon script
├── laser_cannon.tres                              # Weapon instance data (converted from weapons.tbl)
├── assets/                                        # Feature-specific assets
│   ├── sounds/                                    # Weapon-specific sounds
│   │   ├── fire_sound.ogg                        # Firing sound (converted from laser_fire.wav)
│   │   └── impact_sound.ogg                       # Impact sound (converted from laser_impact.wav)
│   └── effects/                                   # Weapon-specific effects
│       ├── muzzle_flash.png                       # Muzzle flash (converted from laser_muzzle.ani)
│       └── impact_effect/                          # Impact effect directory
└── laser_bolt/                                    # Projectile directory
    ├── laser_bolt.tscn                           # Projectile scene
    ├── laser_bolt.gd                             # Projectile script
    ├── laser_bolt.tres                           # Projectile data
    ├── laser_bolt.glb                            # 3D model (converted from laser_cannon.pof)
    ├── laser_bolt.webp                           # Projectile texture (converted from laser_cannon.pcx)
    └── laser_bolt_trail.webp                     # Projectile trail texture
```

### Missile Weapons

#### SRM-1 Missile
**Source Assets**:
- `weapons.tbl` - Weapon class definition
- `srm1.pof` - 3D model
- `srm1.pcx` - Texture
- `missile_launch.wav` - Launch sound
- `missile_engine.wav` - Engine sound
- `missile_explosion.wav` - Explosion sound
- `missile_launch.ani` - Launch effect
- `missile_engine.ani` - Engine effect
- `missile_explosion.ani` - Explosion effect

**Target Structure**:
Following the feature-based organization principle:
```
/features/weapons/srm1/
├── srm1.tscn                                      # Weapon scene
├── srm1.gd                                        # Weapon script
├── srm1.tres                                      # Weapon instance data (converted from weapons.tbl)
├── assets/                                        # Feature-specific assets
│   ├── sounds/                                    # Weapon-specific sounds
│   │   ├── launch_sound.ogg                       # Launch sound (converted from missile_launch.wav)
│   │   ├── engine_sound.ogg                      # Engine sound (converted from missile_engine.wav)
│   │   └── explosion_sound.ogg                   # Explosion sound (converted from missile_explosion.wav)
│   └── effects/                                   # Weapon-specific effects
│       ├── launch_effect.png                     # Launch effect (converted from missile_launch.ani)
│       ├── engine_effect.png                      # Engine effect (converted from missile_engine.ani)
│       └── explosion_effect/                      # Explosion effect directory
│           ├── explosion.tscn                    # Explosion scene
│           ├── explosion.gd                      # Explosion script
│           ├── explosion.tres                    # Explosion data
│           ├── fire_texture.webp                 # Fire texture (converted from fire.pcx)
│           ├── smoke_texture.webp                # Smoke texture (converted from smoke.pcx)
│           └── sparks_texture.webp                # Sparks texture (converted from sparks.pcx)
└── missile_projectile/                            # Projectile directory
    ├── missile.tscn                              # Projectile scene
    ├── missile.gd                                # Projectile script
    ├── missile.tres                              # Projectile data
    ├── missile.glb                              # 3D model (converted from srm1.pof)
    └── missile.webp                             # Projectile texture (converted from srm1.pcx)
```

## Mission Assets Mapping

### Hermes Campaign Mission 1

**Source Assets**:
- `m01_hermes.fs2` - Mission file
- `m1fiction.txt` - Fiction text
- `m1briefing.txt` - Briefing text
- Various ship and weapon references

**Target Structure**:
Following the campaign-centric mission organization principle where "this file defines 'what' happens in a mission, rather than 'how' a game mechanic works":
```
/campaigns/hermes/missions/m01_hermes/
├── mission.tscn                                   # Main mission scene (converted from M01-BG-Hermes.fs2)
├── mission_data.tres                              # Mission configuration (converted from .fs2)
├── briefing.txt                                   # Briefing text (converted from m1briefing.txt)
├── fiction.txt                                    # Fiction text (converted from m1fiction.txt)
├── objectives.tres                                # Mission objectives (converted from .fs2)
├── events.tres                                    # Mission events (converted from .fs2)
├── messages.tres                                  # Mission messages (converted from .fs2)
└── assets/                                        # Mission-specific assets
    ├── audio/                                     # Mission audio
    │   ├── briefing_voice.ogg                     # Briefing voice audio
    │   ├── music.ogg                              # Mission background music
    │   └── ambient.ogg                           # Ambient mission sounds
    └── visuals/                                   # Mission visuals
        └── cutscene_frames/                       # Cutscene animation frames
```

## Effect Assets Mapping

### Explosion Effects

**Source Assets**:
- `explosion.ani` - Explosion animation
- `fire.pcx` - Fire texture
- `smoke.pcx` - Smoke texture
- `sparks.pcx` - Sparks texture
- `explosion.wav` - Explosion sound

**Target Structure**:
Following the feature-based organization principle:
```
/features/effects/explosion/
├── explosion.tscn                                 # Effect scene
├── explosion.gd                                   # Effect script
├── explosion.tres                                 # Effect instance data
├── assets/                                        # Feature-specific assets
│   ├── textures/                                  # Effect-specific textures
│   │   ├── fire_texture.webp                      # Fire texture (converted from fire.pcx)
│   │   ├── smoke_texture.webp                     # Smoke texture (converted from smoke.pcx)
│   │   └── sparks_texture.webp                 # Sparks texture (converted from sparks.pcx)
│   └── sounds/                                    # Effect-specific sounds
│       ├── fire_sound.ogg                        # Fire sound (converted from explosion.wav)
│       └── blast_sound.ogg                        # Blast sound
└── explosion_icon.png                             # UI icon
```

## UI Assets Mapping

### HUD Components

**Source Assets**:
- `hud.pcx` - HUD background
- `gauges.pcx` - Instrument gauges
- `hud_click.wav` - Interface click sound
- `hud_font.pcx` - Interface font

**Target Structure**:
Following the feature-based organization principle:
```
/features/ui/hud/
├── player_hud.tscn                                # HUD scene
├── player_hud.gd                                  # HUD script
├── gauges/                                        # HUD gauge graphics
│   ├── speed/                                     # Speed gauge
│   ├── shields/                                   # Shield gauge
│   ├── weapons/                                   # Weapon gauge
│   └── fuel/                                      # Fuel gauge
├── indicators/                                    # HUD indicator graphics
│   ├── targets/                                   # Target indicators
│   ├── warnings/                                  # Warning indicators
│   └── status/                                    # Status indicators
├── animations/                                    # HUD animations
│   ├── warnings/                                 # Warning animations
│   └── status/                                    # Status animations
├── assets/                                        # Feature-specific assets
│   ├── sounds/                                   # HUD sounds
│   │   ├── warning.ogg                          # Warning sound (converted from hud_click.wav)
│   │   ├── target_acquired.ogg                   # Target acquired sound
│   │   └── system_status.ogg                     # System status sound
│   ├── backgrounds/                              # HUD backgrounds
│   │   └── hud_background.png                     # Background texture (converted from hud.pcx)
│   ├── gauges/                                   # HUD gauge graphics
│   │   └── hud_gauges.png                         # Gauge textures (converted from gauges.pcx)
│   └── themes/                                   # UI themes
│       ├── hud_fonts.tres                        # Font resources (converted from hud_font.pcx)
│       └── hud_theme.tres                        # UI theme
└── player_hud_icon.png                            # UI icon
```

## Audio Assets Mapping

### Music Tracks

**Source Assets**:
- `combat_music.wav` - Combat music
- `briefing_music.wav` - Briefing music
- `menu_music.wav` - Menu music

**Target Structure**:
Following the "Global Litmus Test" principle: "If I delete three random features, is this asset still needed?":
```
/assets/audio/music/
├── combat_theme.ogg                               # Combat music (converted from combat_music.wav)
├── briefing_theme.ogg                            # Briefing music (converted from briefing_music.wav)
└── main_theme.ogg                                # Menu music (converted from menu_music.wav)
```

### Sound Effects

**Source Assets**:
- `laser_fire.wav` - Laser firing sound
- `missile_launch.wav` - Missile launch sound
- `explosion.wav` - Explosion sound
- `engine.wav` - Engine sound

**Target Structure**:
Following the "Global Litmus Test" principle:
```
/assets/audio/sfx/
├── weapons/                                       # Weapon sound effects
│   ├── firing/                                   # Weapon firing sounds
│   │   ├── laser_fire.ogg                        # Laser sound (converted from laser_fire.wav)
│   │   └── missile_launch.ogg                     # Missile sound (converted from missile_launch.wav)
│   ├── impacts/                                   # Weapon impact sounds
│   │   └── explosion.ogg                          # Explosion sound (converted from explosion.wav)
│   └── reloading/                                 # Weapon reload sounds
├── environment/                                   # Environmental sounds
│   └── engine.ogg                                 # Engine sound (converted from engine.wav)
└── ui/                                            # UI sound effects
    ├── button_click.ogg                           # Button click sound
    └── menu_navigation.ogg                       # Menu navigation sound
```

## Text Assets Mapping

### Mission Fiction

**Source Assets**:
- `m1fiction.txt` - Mission 1 fiction
- `m2fiction.txt` - Mission 2 fiction
- `campaign_overview.txt` - Campaign overview

**Target Structure**:
Following the campaign-centric organization principle:
```
/campaigns/hermes/missions/m01_hermes/
├── fiction.txt                                   # Mission fiction (converted from m1fiction.txt)
└── campaign_overview.txt                         # Campaign overview
```

## Integration Points

### Data Converter Output Mapping
- ShipClass resources → Converted to Godot resources (.tres) in `/features/fighters/{faction}_{ship_name}/{ship_name}.tres`
- WeaponClass resources → Converted to Godot resources (.tres) in `/features/weapons/{weapon_name}/{weapon_name}.tres`
- Mission scenes → Converted to Godot scenes (.tscn) in `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/mission.tscn`
- Effect resources → Converted to Godot resources (.tres) in `/features/effects/{effect_name}/{effect_name}.tres`
- UI components → Converted to Godot scenes (.tscn) in `/features/ui/{component}/{component}.tscn`
- 3D models → Converted to glTF (.glb) in `/features/{category}/{entity}/{entity}.glb`
- Textures → Converted to WebP (.webp) in `/features/{category}/{entity}/assets/textures/` or `/assets/textures/`
- Audio → Converted to Ogg Vorbis (.ogg) in `/features/{category}/{entity}/assets/sounds/` or `/assets/audio/`

### Resource References
- **Entity scenes** in `/features/` reference data resources from their own directories
- **Mission scenes** in `/campaigns/` reference entity scenes from `/features/`
- **UI components** in `/features/ui/` reference shared assets from `/features/ui/_shared/`
- **Global assets** in `/assets/` are referenced by multiple features and systems
- **Shared assets** in `/_shared/` directories are referenced by related features within the same category

## Relationship to Other Assets

### Ship-Weapon Integration
- Ships in `/features/fighters/` mount and fire weapons from `/features/weapons/`
- Weapon hardpoints are preserved from POF metadata during conversion
- Weapon mounting is handled through Godot's node hierarchy and exported variables
- AI profiles in `/assets/data/ai/profiles/` influence weapon selection and usage

### Mission-Entity Integration
- Missions in `/campaigns/` create and manage entities from `/features/`
- Entity placement data is parsed from FS2 files during conversion
- Cross-references use Godot's resource system with instance() calls and exported variables
- Mission events in `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/events.tres` trigger entity behaviors

### Effect-Audio Integration
- Visual effects in `/features/effects/` reference audio from `/assets/audio/` and feature-specific directories
- Particle effects reference textures from `/assets/textures/effects/` and feature-specific directories
- Animation timing is preserved from ANI files during conversion to Godot's animation system
- Effect behaviors are controlled by LimboAI behavior trees in `/assets/behavior_trees/ai/`

### UI-Data Integration
- UI components in `/features/ui/` display data from `/assets/data/` and campaign-specific directories
- Tech database entries in `/features/ui/tech_database/` reference ship and weapon data resources
- Briefing screens in `/features/ui/briefing/` reference mission fiction from `/campaigns/{campaign}/missions/`
- HUD elements in `/features/ui/hud/` display real-time data from game state in `/autoload/game_state.gd`

This mapping ensures that all source assets from the Wing Commander Saga Hermes campaign are properly converted and organized in the Godot project structure, maintaining all gameplay relationships and functionality while leveraging modern engine capabilities. The structure follows the hybrid approach where truly global assets are organized in `/assets/` following the "Global Litmus Test" principle, while feature-specific assets are co-located with their respective features in `/features/` directories.