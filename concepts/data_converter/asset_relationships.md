# Closely Related Assets and Directory Organization

## Overview
This document identifies closely related assets in Wing Commander Saga and specifies how they should be organized according to the Godot project's hybrid organizational model defined in directory_structure.md and following the principles in Godot_Project_Structure_Refinement.md. The approach groups all files related to a single conceptual feature into a single, self-contained directory within `/features/`, while maintaining truly global assets in `/assets/` and using `/_shared/` directories for semi-global assets specific to feature categories.

## Asset Relationship Groups

### 1. Ship Entities
**Primary Directory**: `/features/fighters/{faction}_{ship_name}/`

**Closely Related Assets**:
- ShipClass data resource (.tres) from `/assets/data/ships/{ship_name}.tres`
- 3D model (.glb) converted from .pof file
- Ship textures (.webp) converted from .pcx/.dds files
- Engine sound effects (.ogg) converted from .wav files
- Weapon hardpoint metadata from .pof conversion
- Thruster effect animations from `/assets/animations/effects/particles/`
- Damage effect textures from `/assets/textures/effects/`
- Cockpit UI graphics from `/features/fighters/_shared/cockpits/`

**Integration Example**:
```
/features/fighters/confed_rapier/
├── rapier.tscn              # Ship entity scene
├── rapier.gd                # Ship script
├── rapier.tres              # ShipClass resource (from /assets/data/ships/)
├── rapier.glb               # 3D model (converted from tcf_rapier.pof)
├── rapier_diffuse.webp      # Diffuse texture (converted from rapier.pcx)
├── rapier_normal.webp       # Normal map (converted from rapier_normals.pcx)
├── rapier_engine.ogg        # Engine sound (converted from snd_engine.wav)
├── assets/                  # Feature-specific assets
│   ├── sounds/              # Ship-specific sounds
│   │   ├── engine_loop.ogg  # Engine loop sound
│   │   ├── maneuver.ogg     # Maneuvering thrusters
│   │   └── afterburner.ogg  # Afterburner sound
│   └── effects/             # Ship-specific visual effects
│       ├── thruster_particles.tscn # Thruster particle effect
│       └── shield_effect.png       # Shield visual effect
└── rapier_icon.png          # Ship icon for UI (converted from bicon-rapier.ani)
```

### 2. Weapon Entities
**Primary Directory**: `/features/weapons/{weapon_name}/`

**Closely Related Assets**:
- WeaponClass data resource (.tres) from `/assets/data/weapons/{weapon_name}.tres`
- Weapon 3D model (.glb) converted from .pof file (for projectiles)
- Firing sound effects (.ogg) converted from .wav files
- Muzzle flash animations from `/features/weapons/_shared/muzzle_flashes/`
- Projectile textures from `/assets/textures/effects/particles/`
- Impact effect animations from `/features/weapons/_shared/impact_effects/`
- Impact sound effects (.ogg) from `/assets/audio/sfx/weapons/impacts/`

**Integration Example**:
```
/features/weapons/laser_cannon/
├── laser_cannon.tscn        # Weapon entity scene
├── laser_cannon.gd          # Weapon script
├── laser_cannon.tres        # WeaponClass resource (from /assets/data/weapons/)
├── assets/                  # Feature-specific assets
│   └── sounds/              # Weapon-specific sounds
│       ├── fire_sound.ogg   # Firing sound (converted from snd_weapon_fire.wav)
│       └── impact_sound.ogg # Impact sound (converted from snd_impact.wav)
└── laser_bolt/              # Projectile subdirectory
    ├── laser_bolt.tscn      # Projectile scene
    ├── laser_bolt.gd        # Projectile script
    ├── laser_bolt.tres      # Projectile resource
    └── laser_bolt.glb       # 3D model (converted from tcm_laser.pof)
```

### 3. Mission Packages
**Primary Directory**: `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/`

**Closely Related Assets**:
- Mission data resource (.tres) from `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/mission_data.tres`
- Mission scene (.tscn) converted from .fs2 file
- Briefing text (.txt) converted from .txt file
- Fiction text (.txt) converted from .txt file
- Mission objectives (.tres) from mission parsing
- Event definitions (.tres) from mission parsing
- Initial ship placements from .fs2 parsing
- Entity references to `/features/` directories
- Cutscene definitions (.tres) from `/campaigns/{campaign}/cutscenes/`

**Integration Example**:
```
/campaigns/hermes/missions/m01_hermes/
├── mission.tscn             # Mission scene (converted from M01-BG-Hermes.fs2)
├── mission_data.tres        # Mission configuration
├── briefing.txt             # Briefing text (converted from briefing.txt)
├── fiction.txt              # Fiction text (converted from m1fiction.txt)
├── objectives.tres          # Mission objectives
├── events.tres              # Mission events
├── messages.tres            # Mission messages
├── cutscenes/               # Mission-specific cutscenes
│   ├── intro.tres           # Intro cutscene definition
│   └── outro.tres           # Outro cutscene definition
└── assets/                  # Mission-specific assets
    ├── audio/               # Mission audio
    │   ├── briefing.ogg     # Briefing voice audio
    │   ├── music.ogg        # Mission background music
    │   └── ambient.ogg      # Ambient mission sounds
    └── visuals/             # Mission visuals
        └── cutscene_frames/ # Cutscene animation frames
```

### 4. Effect Systems
**Primary Directory**: `/features/effects/{effect_name}/`

**Closely Related Assets**:
- Effect data resource (.tres) from `/assets/data/effects/{effect_name}.tres`
- Effect 3D model (.glb) if applicable
- Particle textures (.webp) converted from .dds/.pcx files
- Animation sequences from `/assets/animations/effects/{effect_type}/`
- Sound effects (.ogg) converted from .wav files
- Shader definitions if applicable

**Integration Example**:
```
/features/effects/explosion/
├── explosion.tscn           # Effect scene
├── explosion.gd             # Effect script
├── explosion.tres           # Effect resource (from /assets/data/effects/)
├── textures/                # Effect-specific textures
│   ├── exp04_0000.webp      # Frame 0 (converted from exp04_0000.dds)
│   ├── exp04_0001.webp      # Frame 1 (converted from exp04_0001.dds)
│   └── exp04_0002.webp      # Frame 2 (converted from exp04_0002.dds)
└── assets/                  # Feature-specific assets
    └── sounds/              # Effect-specific sounds
        └── explosion_sound.ogg # Explosion sound (converted from snd_explosion.wav)
```

### 5. UI Components
**Primary Directory**: `/features/ui/{component_name}/`

**Closely Related Assets**:
- UI layout scenes (.tscn)
- Interface graphics (.webp) converted from .pcx/.dds files
- UI animation sequences from `/assets/animations/ui/{component}/`
- Font resources from `/features/ui/_shared/fonts/`
- Audio feedback (.ogg) converted from .wav files
- Theme resources (.tres) from `/features/ui/_shared/themes/`

**Integration Example**:
```
/features/ui/hud/
├── player_hud.tscn          # HUD scene
├── player_hud.gd            # HUD script
├── gauges/                  # HUD gauge graphics
│   ├── speed/
│   ├── shields/
│   ├── weapons/
│   └── fuel/
├── indicators/              # HUD indicator graphics
│   ├── targets/
│   ├── warnings/
│   └── status/
├── animations/              # HUD animations
│   ├── warnings/
│   └── status/
├── assets/                  # Feature-specific assets
│   ├── sounds/              # HUD sounds
│   │   ├── warning.ogg      # Warning sound (converted from snd_warning.wav)
│   │   ├── target_acquired.ogg # Target acquired sound
│   │   └── system_status.ogg # System status sound
│   └── backgrounds/         # HUD backgrounds
└── player_hud.tres          # HUD configuration resource
```

## Shared Asset Organization

### Common Visual Effects
**Directory**: `/assets/animations/effects/`

**Used By**:
- Ship destruction effects in `/features/fighters/`
- Weapon impact effects in `/features/weapons/`
- Projectile explosions in `/features/weapons/projectiles/`
- Environmental effects in `/features/environment/`

### Common Audio Resources
**Directory**: `/assets/audio/sfx/ui/`

**Used By**:
- Main menu in `/features/ui/main_menu/`
- Options menu in `/features/ui/options/`
- Briefing screens in `/features/ui/briefing/`
- Debriefing screens in `/features/ui/debriefing/`

### Common Textures
**Directory**: `/assets/textures/ui/`

**Used By**:
- Player HUD in `/features/ui/hud/`
- Targeting displays in `/features/ui/hud/`
- Weapon status in `/features/ui/hud/`
- System indicators in `/features/ui/hud/`

### Shared Fighter Assets
**Directory**: `/features/fighters/_shared/`

**Contains**:
- Shared cockpit models in `/cockpits/`
- Shared effects in `/effects/`
- Shared sounds in `/sounds/`

### Shared Weapon Assets
**Directory**: `/features/weapons/_shared/`

**Contains**:
- Shared muzzle flashes in `/muzzle_flashes/`
- Shared impact effects in `/impact_effects/`

## Cross-Reference Management

### Resource-Based References
- Entity scenes reference data resources using Godot's resource system through exported variables
- Mission scenes reference entity scenes and data resources via instance() calls
- UI components reference font and theme resources through theme properties
- Effect systems reference particle and animation resources through AnimationPlayer nodes

### Path-Based Organization
- Shared assets are placed in common directories following the "Global Litmus Test" principle
- Cross-references use relative paths within the Godot project structure (res://)
- Asset bundles group related resources for efficient loading through ResourceLoader

## Validation Requirements

### Relationship Integrity
- Verify that all closely related assets are properly linked through exported variables
- Check that cross-references resolve to valid resources using ResourceLoader
- Ensure that asset dependencies are correctly ordered in the loading sequence

### Directory Structure Compliance
- Confirm that assets are organized according to feature-based principles with co-location
- Validate that shared assets are placed in appropriate common directories following the hybrid model
- Check that directory naming follows snake_case conventions for files and directories
- Ensure that node names within scenes use PascalCase as per Godot conventions

### Integration with TBL Files
- Ship definitions from ships.tbl map to ShipData resources in `/assets/data/ships/`
- Weapon definitions from weapons.tbl map to WeaponData resources in `/assets/data/weapons/`
- AI profiles from ai_profiles.tbl map to AIProfile resources in `/assets/data/ai/profiles/`
- Species definitions from Species_defs.tbl map to SpeciesData resources in `/assets/data/species/`
- IFF definitions from iff_defs.tbl map to IFFData resources in `/assets/data/iff/`
- Effect definitions from fireball.tbl and weapon_expl.tbl map to EffectData resources in `/assets/data/effects/`

This organization ensures that closely related assets maintain clear relationships between different gameplay systems while following Godot's best practices for feature-based organization and the hybrid model that groups truly global assets in `/assets/` while keeping feature-specific assets co-located within `/features/` directories.