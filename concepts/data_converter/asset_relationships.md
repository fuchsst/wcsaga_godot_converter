# Closely Related Assets and Directory Organization

## Overview
This document identifies closely related assets in Wing Commander Saga and specifies how they should be organized in the same directories to maintain gameplay relationships and facilitate efficient development and maintenance.

## Asset Relationship Groups

### 1. Ship Entities
**Primary Directory**: `/entities/fighters/{faction}/{ship_name}/`

**Closely Related Assets**:
- ShipClass data resource (.tres) from `/data/ships/{faction}/{type}/{ship_name}.tres`
- 3D model (.glb) converted from .pof file
- Ship textures (.webp) converted from .pcx files
- Engine sound effects (.ogg) converted from .wav files
- Weapon hardpoint metadata from .pof conversion
- Thruster effect animations from `/animations/effects/engine/`
- Damage effect textures from `/textures/effects/`
- Cockpit UI graphics from `/textures/ui/cockpit/`

**Integration Example**:
```
/entities/fighters/confed_rapier/
├── rapier.tscn              # Ship entity scene
├── rapier.gd                # Ship script
├── rapier.tres              # ShipClass resource (links to /data/ships/terran/fighters/)
├── rapier.glb               # 3D model (converted from rapier.pof)
├── rapier_diffuse.webp      # Diffuse texture (converted from rapier.pcx)
├── rapier_normal.webp       # Normal map (converted from rapier_normals.pcx)
├── rapier_engine.ogg        # Engine sound (converted from engine.wav)
├── rapier_muzzle_flash.png  # Muzzle flash effect (converted from muzzle.ani)
└── rapier_trail.webp        # Engine trail (converted from trail.ani)
```

### 2. Weapon Entities
**Primary Directory**: `/entities/weapons/{weapon_name}/`

**Closely Related Assets**:
- WeaponClass data resource (.tres) from `/data/weapons/{faction}/{weapon_name}.tres`
- Weapon 3D model (.glb) converted from .pof file
- Firing sound effects (.ogg) converted from .wav files
- Muzzle flash animations from `/animations/weapons/{weapon_type}/`
- Projectile textures from `/textures/particles/weapons/`
- Impact effect animations from `/animations/explosions/`
- Impact sound effects (.ogg) from `/audio/sfx/explosions/`

**Integration Example**:
```
/entities/weapons/laser_cannon/
├── laser_cannon.tscn        # Weapon entity scene
├── laser_cannon.gd          # Weapon script
├── laser_cannon.tres        # WeaponClass resource (links to /data/weapons/terran/)
├── laser_cannon.glb         # 3D model (converted from laser_cannon.pof)
├── laser_fire.ogg           # Firing sound (converted from fire.wav)
├── laser_muzzle.png         # Muzzle flash (converted from laser_muzzle.ani)
└── laser_bolt/              # Projectile subdirectory
    ├── laser_bolt.tscn      # Projectile scene
    ├── laser_bolt.tres      # Projectile resource
    ├── laser_bolt.webp      # Projectile texture
    └── laser_trail.webp     # Projectile trail
```

### 3. Mission Packages
**Primary Directory**: `/missions/{campaign}/{mission_name}/`

**Closely Related Assets**:
- Mission data resource (.tres) from `/data/missions/{campaign}/{mission_name}.tres`
- Mission scene (.tscn) converted from .fs2 file
- Briefing text (.txt) converted from .txt file
- Fiction text (.txt) converted from .txt file
- Mission objectives (.tres) from mission parsing
- Event definitions (.tres) from mission parsing
- Initial ship placements from .fs2 parsing
- Entity references to `/entities/` directories

**Integration Example**:
```
/campaigns/hermes/missions/m01_hermes/
├── mission.tscn             # Mission scene (converted from m01_hermes.fs2)
├── mission.tres             # Mission data (converted from m01_hermes.fs2)
├── briefing.txt             # Briefing text (converted from briefing.txt)
├── fiction.txt              # Fiction text (converted from m01fiction.txt)
├── objectives.tres          # Mission objectives
├── events.tres              # Mission events
├── messages.tres            # Mission messages
└── entities/                # Mission-specific entity instances
    ├── player_ship.tscn
    ├── enemy_wing.tscn
    └── waypoints.tscn
```

### 4. Effect Systems
**Primary Directory**: `/entities/effects/{effect_name}/`

**Closely Related Assets**:
- Effect data resource (.tres) from `/data/effects/{effect_type}.tres`
- Effect 3D model (.glb) if applicable
- Particle textures (.webp) converted from .pcx files
- Animation sequences from `/animations/effects/{effect_type}/`
- Sound effects (.ogg) converted from .wav files
- Shader definitions if applicable

**Integration Example**:
```
/entities/effects/explosion/
├── explosion.tscn           # Effect scene
├── explosion.gd             # Effect script
├── explosion.tres           # Effect resource (links to /data/effects/)
├── explosion_particles/     # Particle system directory
│   ├── particles.tscn
│   ├── fire.webp            # Fire texture (converted from fire.pcx)
│   ├── smoke.webp           # Smoke texture (converted from smoke.pcx)
│   └── sparks.webp          # Sparks texture (converted from sparks.pcx)
├── explosion_animations/    # Animation directory
│   ├── fire_ani.tscn        # Fire animation (converted from fire.ani)
│   └── smoke_ani.tscn       # Smoke animation (converted from smoke.ani)
├── explosion_fire.ogg       # Fire sound (converted from fire.wav)
└── explosion_blast.ogg      # Blast sound (converted from blast.wav)
```

### 5. UI Components
**Primary Directory**: `/ui/{component_name}/`

**Closely Related Assets**:
- UI layout scenes (.tscn)
- Interface graphics (.png) converted from .pcx files
- UI animation sequences from `/animations/ui/{component}/`
- Font resources
- Audio feedback (.ogg) converted from .wav files
- Theme resources (.tres)

**Integration Example**:
```
/ui/hud/
├── player_hud.tscn          # HUD scene
├── player_hud.gd            # HUD script
├── hud_background.png       # Background (converted from hud_bg.pcx)
├── hud_gauges.png           # Gauges (converted from gauges.pcx)
├── hud_fonts.tres           # Font resources
├── hud_animations/          # Animation directory
│   ├── gauge_anim.tscn      # Gauge animation (converted from gauge.ani)
│   └── alert_anim.tscn      # Alert animation (converted from alert.ani)
├── hud_click.ogg            # Click sound (converted from click.wav)
└── hud_theme.tres           # UI theme
```

## Shared Asset Organization

### Common Visual Effects
**Directory**: `/animations/effects/explosions/`

**Used By**:
- Ship destruction effects in `/entities/fighters/`
- Weapon impact effects in `/entities/weapons/`
- Projectile explosions in `/entities/projectiles/`
- Environmental effects in `/entities/environment/`

### Common Audio Resources
**Directory**: `/audio/sfx/ui/buttons/`

**Used By**:
- Main menu in `/ui/main_menu/`
- Options menu in `/ui/options/`
- Briefing screens in `/ui/briefing/`
- Debriefing screens in `/ui/debriefing/`

### Common Textures
**Directory**: `/textures/ui/hud/`

**Used By**:
- Player HUD in `/ui/hud/`
- Targeting displays in `/ui/hud/`
- Weapon status in `/ui/hud/`
- System indicators in `/ui/hud/`

## Cross-Reference Management

### Resource-Based References
- Entity scenes reference data resources using Godot's resource system
- Mission scenes reference entity scenes and data resources
- UI components reference font and theme resources
- Effect systems reference particle and animation resources

### Path-Based Organization
- Shared assets are placed in common directories with clear naming
- Cross-references use relative paths within the Godot project structure
- Asset bundles group related resources for efficient loading

## Validation Requirements

### Relationship Integrity
- Verify that all closely related assets are properly linked
- Check that cross-references resolve to valid resources
- Ensure that asset dependencies are correctly ordered

### Directory Structure Compliance
- Confirm that assets are organized according to feature-based principles
- Validate that shared assets are placed in appropriate common directories
- Check that directory naming follows established conventions

This organization ensures that closely related assets are stored together while maintaining clear relationships between different gameplay systems, making the project more maintainable and easier to work with.