# Source Assets to Target Structure Mapping

## Overview
This document maps specific source assets from the Wing Commander Saga Hermes campaign to their corresponding target locations and formats in the Godot implementation, providing a clear reference for the conversion process.

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
```
/data/ships/terran/fighters/arrow.tres              # ShipClass resource
/entities/fighters/confed_arrow/
├── arrow.tscn                                     # Ship scene
├── arrow.gd                                       # Ship script
├── arrow.tres                                     # Ship instance data
├── arrow.glb                                      # 3D model
├── arrow_diffuse.webp                            # Diffuse texture
├── arrow_normal.webp                             # Normal map
├── arrow_engine.ogg                              # Engine sound
├── arrow_muzzle.png                              # Muzzle flash
└── arrow_trail.webp                              # Engine trail
```

#### Raptor Fighter
**Source Assets**:
- `ships.tbl` - Ship class definition
- `rapier.pof` - 3D model
- `rapier.pcx` - Diffuse texture
- `rapier_engine.wav` - Engine sound
- `rapier_weapons.ani` - Weapon effects

**Target Structure**:
```
/data/ships/terran/fighters/rapier.tres             # ShipClass resource
/entities/fighters/confed_rapier/
├── rapier.tscn                                    # Ship scene
├── rapier.gd                                      # Ship script
├── rapier.tres                                    # Ship instance data
├── rapier.glb                                     # 3D model
├── rapier_diffuse.webp                           # Diffuse texture
├── rapier_engine.ogg                             # Engine sound
├── rapier_muzzle.png                             # Muzzle flash
└── rapier_trail.webp                             # Engine trail
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
```
/data/ships/kilrathi/fighters/dralthi.tres          # ShipClass resource
/entities/fighters/kilrathi_dralthi/
├── dralthi.tscn                                   # Ship scene
├── dralthi.gd                                     # Ship script
├── dralthi.tres                                   # Ship instance data
├── dralthi.glb                                    # 3D model
├── dralthi_diffuse.webp                          # Diffuse texture
├── dralthi_engine.ogg                            # Engine sound
├── dralthi_muzzle.png                            # Muzzle flash
└── dralthi_trail.webp                            # Engine trail
```

## Weapon Assets Mapping

### Laser Weapons

#### Mk.II Laser Cannon
**Source Assets**:
- `weapons.tbl` - Weapon class definition
- `laser_cannon.pof` - 3D model
- `laser_cannon.pcx` - Texture
- `laser_fire.wav` - Firing sound
- `laser_impact.wav` - Impact sound
- `laser_muzzle.ani` - Muzzle effect
- `laser_bolt.ani` - Projectile effect

**Target Structure**:
```
/data/weapons/terran/laser_cannon.tres              # WeaponClass resource
/entities/weapons/laser_cannon/
├── laser_cannon.tscn                              # Weapon scene
├── laser_cannon.gd                                # Weapon script
├── laser_cannon.tres                              # Weapon instance data
├── laser_cannon.glb                               # 3D model
├── laser_cannon.webp                              # Texture
├── laser_fire.ogg                                 # Firing sound
├── laser_impact.ogg                               # Impact sound
├── laser_muzzle.png                               # Muzzle effect
└── laser_bolt/                                    # Projectile directory
    ├── laser_bolt.tscn                           # Projectile scene
    ├── laser_bolt.tres                           # Projectile data
    ├── laser_bolt.webp                           # Projectile texture
    └── laser_bolt_trail.webp                     # Projectile trail
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
```
/data/weapons/terran/srm1.tres                      # WeaponClass resource
/entities/weapons/srm1/
├── srm1.tscn                                      # Weapon scene
├── srm1.gd                                        # Weapon script
├── srm1.tres                                      # Weapon instance data
├── srm1.glb                                       # 3D model
├── srm1.webp                                      # Texture
├── srm1_launch.ogg                                # Launch sound
├── srm1_engine.ogg                                # Engine sound
├── srm1_explosion.ogg                             # Explosion sound
├── srm1_launch.png                                # Launch effect
├── srm1_engine.png                                # Engine effect
└── srm1_explosion/                                # Explosion directory
    ├── explosion.tscn                            # Explosion scene
    ├── explosion.tres                            # Explosion data
    ├── explosion_fire.webp                       # Fire texture
    ├── explosion_smoke.webp                      # Smoke texture
    └── explosion_sparks.webp                     # Sparks texture
```

## Mission Assets Mapping

### Hermes Campaign Mission 1

**Source Assets**:
- `m01_hermes.fs2` - Mission file
- `m1fiction.txt` - Fiction text
- `m1briefing.txt` - Briefing text
- Various ship and weapon references

**Target Structure**:
```
/data/missions/hermes/m01_hermes.tres               # Mission data resource
/missions/hermes/m01_hermes/
├── mission.tscn                                   # Mission scene
├── mission.tres                                   # Mission instance data
├── briefing.txt                                   # Briefing text (converted)
├── fiction.txt                                    # Fiction text (converted)
├── objectives.tres                                # Mission objectives
├── events.tres                                    # Mission events
├── messages.tres                                  # Mission messages
├── entities/                                      # Mission entities
│   ├── player_ship.tscn                          # Player ship instance
│   ├── enemy_wing.tscn                           # Enemy wing instance
│   └── waypoints.tscn                            # Navigation waypoints
└── briefing/                                      # Briefing interface
    ├── briefing.tscn                             # Briefing scene
    ├── briefing.gd                               # Briefing script
    ├── fiction_display.tscn                      # Fiction display
    └── objective_display.tscn                    # Objective display
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
```
/data/effects/explosion.tres                        # Effect data resource
/entities/effects/explosion/
├── explosion.tscn                                 # Effect scene
├── explosion.gd                                   # Effect script
├── explosion.tres                                 # Effect instance data
├── explosion_fire.webp                           # Fire texture
├── explosion_smoke.webp                          # Smoke texture
├── explosion_sparks.webp                         # Sparks texture
├── explosion_fire.ogg                            # Fire sound
└── explosion_blast.ogg                           # Blast sound
```

## UI Assets Mapping

### HUD Components

**Source Assets**:
- `hud.pcx` - HUD background
- `gauges.pcx` - Instrument gauges
- `hud_click.wav` - Interface click sound
- `hud_font.pcx` - Interface font

**Target Structure**:
```
/ui/hud/
├── player_hud.tscn                                # HUD scene
├── player_hud.gd                                  # HUD script
├── hud_background.png                            # Background texture
├── hud_gauges.png                                # Gauge textures
├── hud_click.ogg                                 # Click sound
├── hud_fonts.tres                                # Font resources
└── hud_theme.tres                                # UI theme
```

## Audio Assets Mapping

### Music Tracks

**Source Assets**:
- `combat_music.wav` - Combat music
- `briefing_music.wav` - Briefing music
- `menu_music.wav` - Menu music

**Target Structure**:
```
/audio/music/
├── combat_theme.ogg                               # Combat music
├── briefing_theme.ogg                             # Briefing music
└── main_theme.ogg                                 # Menu music
```

### Sound Effects

**Source Assets**:
- `laser_fire.wav` - Laser firing sound
- `missile_launch.wav` - Missile launch sound
- `explosion.wav` - Explosion sound
- `engine.wav` - Engine sound

**Target Structure**:
```
/audio/sfx/
├── weapons/
│   ├── laser_fire.ogg                            # Laser sound
│   └── missile_launch.ogg                        # Missile sound
├── explosions/
│   └── explosion.ogg                             # Explosion sound
└── environment/
    └── engine.ogg                                # Engine sound
```

## Text Assets Mapping

### Mission Fiction

**Source Assets**:
- `m1fiction.txt` - Mission 1 fiction
- `m2fiction.txt` - Mission 2 fiction
- `campaign_overview.txt` - Campaign overview

**Target Structure**:
```
/text/fiction/hermes/
├── m01_fiction.txt                               # Mission 1 fiction
├── m02_fiction.txt                               # Mission 2 fiction
└── campaign_overview.txt                         # Campaign overview
```

## Cross-Reference Summary

### Ship-Weapon Integration
- Ships in `/entities/fighters/` reference weapons from `/entities/weapons/`
- Weapon hardpoints are preserved from POF metadata
- Weapon mounting is handled through Godot's node hierarchy

### Mission-Entity Integration
- Missions in `/missions/` reference entities from `/entities/`
- Entity placement data is parsed from FS2 files
- Cross-references use Godot's resource system

### Effect-Audio Integration
- Visual effects in `/entities/effects/` reference audio from `/audio/`
- Particle effects reference textures from `/textures/`
- Animation timing is preserved from ANI files

This mapping ensures that all source assets from the Wing Commander Saga Hermes campaign are properly converted and organized in the Godot project structure, maintaining all gameplay relationships and functionality while leveraging modern engine capabilities.