# Ships Asset Mapping

## Overview
This document maps the ship definitions from ships.tbl to their corresponding media assets in the Wing Commander Saga Hermes campaign, organized according to the Godot feature-based directory structure. The mapping follows the self-contained feature organization principle where all files related to a single ship are grouped together in a dedicated directory.

## Asset Types

### 3D Models (.pof)
Ships.tbl references POF files that contain the 3D geometry for each ship class:
- tcf_arrow.pof - F-27B Arrow fighter
- tcf_ferret.pof - F-32B Ferret fighter
- tcf_hellcat_v.pof - F-86C Hellcat V fighter
- tcf_rapier.pof - F-44B Raptor fighter
- tcb_thunderbolt_vii.pof - F-72B Thunderbolt VII fighter
- tcs_behemoth.pof - TCS Behemoth capital ship
- tcs_prowler_d.pof - TCS Prowler-D capital ship
- tcs_venture.pof - TCS Venture capital ship
- kb_starbase.pof - Kilrathi starbase
- kim_paw.pof - Kilrathi Imperial-class PAKT
- And many others...

### Textures (.pcx/.dds)
Ship textures are typically stored in separate PCX or DDS files referenced by the POF models:
- Ship-specific diffuse textures (e.g., arrow.pcx for the Arrow fighter)
- Normal map textures (e.g., arrow_normals.pcx)
- Detail textures and other material maps
- DDS format textures for higher quality (e.g., tcf_arrow_2-shine.dds)

### Sounds (.wav/.ogg)
Ship-related sounds include:
- Engine sounds for each ship class
- Weapon firing sounds specific to ship-mounted weapons
- Explosion sounds for ship destruction
- Thruster and maneuvering sounds

### Animations (.ani)
Ship-related animations:
- Thruster effects (thruster03.ani, thruster02.ani)
- Special visual effects for ships
- HUD icons and interface elements (bicon-arrow.ani, icon_arrowmk1.ani)

## Format Conversion Process

### Legacy Formats to Godot Formats

**POF Files (.pof)**
- Legacy 3D model format containing ship geometry and subobject hierarchy
- Will be converted to glTF format (.glb) preserving model hierarchy
- Subobject structure and animation points (thrusters, weapons, subsystems) preserved
- Converted using custom POF to glTF conversion tool

**PCX/DDS Files (.pcx/.dds)**
- Legacy texture formats for ship diffuse, normal, and detail maps
- Will be converted to WebP format for better compression and Godot compatibility
- Mipmaps and compression maintained for performance
- Normal maps converted to Godot format

**WAV/OGG Files (.wav/.ogg)**
- Legacy audio formats for engine sounds, weapons, and effects
- Will be maintained in Ogg Vorbis format as it's already Godot-compatible
- Metadata and audio characteristics preserved
- 3D positioning support added where appropriate

**ANI Files (.ani)**
- Legacy animation format for visual effects and UI elements
- Will be converted to PNG sequences for particle effects or video format
- Animation timing and frame data preserved in conversion

## Target Structure
Following the Godot project structure defined in directory_structure.md and the feature-based organization principle, ship assets are organized as follows:

### Features Directory Structure
Ships are implemented as self-contained features in `/features/fighters/` for fighter craft and `/features/capital_ships/` for larger vessels, following the principle that "this is a self-contained 'thing' that can be placed in the game world."

```
features/
├── fighters/                      # Fighter ship entities
│   ├── confed_arrow/              # F-27B Arrow fighter - all files together
│   │   ├── arrow.tscn             # Ship scene file
│   │   ├── arrow.gd               # Ship controller script
│   │   ├── arrow.tres             # Ship data resource (converted from .tbl)
│   │   ├── arrow.glb              # Converted 3D model (from tcf_arrow.pof)
│   │   ├── arrow_diffuse.webp     # Diffuse texture (from arrow.pcx)
│   │   ├── arrow_normal.webp      # Normal map (from arrow_normals.pcx)
│   │   ├── arrow_engine.ogg       # Engine sound
│   │   ├── arrow_muzzle.png       # Muzzle flash effect
│   │   └── assets/                # Feature-specific assets
│   │       ├── sounds/            # Ship-specific sounds
│   │       │   ├── engine_loop.ogg # Engine loop sound
│   │       │   ├── maneuver.ogg    # Maneuvering thrusters
│   │       │   └── afterburner.ogg # Afterburner sound
│   │       └── effects/           # Ship-specific visual effects
│   │           ├── thruster_particles.tscn # Thruster particle effect
│   │           └── shield_effect.png       # Shield visual effect
│   ├── confed_rapier/             # F-44B Raptor fighter
│   │   ├── rapier.tscn            # Scene file
│   │   ├── rapier.gd              # Script file
│   │   ├── rapier.tres            # Ship data resource
│   │   ├── rapier.glb             # 3D model
│   │   ├── rapier.png             # Texture
│   │   └── rapier_engine.ogg      # Engine sound
│   ├── kilrathi_dralthi/          # Dralthi fighter
│   │   ├── dralthi.tscn
│   │   ├── dralthi.gd
│   │   ├── dralthi.tres
│   │   ├── dralthi.glb
│   │   ├── dralthi.png
│   │   └── dralthi_engine.ogg
│   ├── _shared/                   # Shared fighter assets
│   │   ├── cockpits/              # Shared cockpit models
│   │   │   ├── standard_cockpit.glb
│   │   │   └── standard_cockpit_material.tres
│   │   └── effects/               # Shared fighter effects
│   │       ├── engine_trail.png
│   │       └── shield_effect.png
│   └── templates/                 # Fighter templates
├── capital_ships/                 # Capital ship entities
│   ├── tcs_behemoth/              # TCS Behemoth capital ship
│   │   ├── behemoth.tscn          # Ship scene file
│   │   ├── behemoth.gd            # Ship controller script
│   │   ├── behemoth.tres          # Ship data resource (converted from .tbl)
│   │   ├── behemoth.glb           # Converted 3D model (from tcs_behemoth.pof)
│   │   ├── behemoth_diffuse.webp  # Diffuse texture
│   │   ├── behemoth_normal.webp   # Normal map
│   │   ├── behemoth_engine.ogg    # Engine sound
│   │   └── assets/                # Feature-specific assets
│   │       ├── sounds/            # Ship-specific sounds
│   │       └── effects/           # Ship-specific visual effects
│   ├── _shared/                   # Shared capital ship assets
│   │   ├── bridge_models/         # Shared bridge components
│   │   └── turret_models/         # Shared turret models
│   └── templates/                 # Capital ship templates
└── templates/                     # Feature templates
```

### Assets Directory Structure
Generic audio assets that are shared across multiple ships are organized in the global `/assets/` directory, following the "Global Litmus Test" principle: "If I delete three random features, is this asset still needed?"

```
assets/
├── audio/                         # Shared audio files
│   ├── sfx/                       # Generic sound effects
│   │   ├── ship_explosions/       # Shared explosion sounds
│   │   │   ├── small_explosion.ogg
│   │   │   ├── medium_explosion.ogg
│   │   │   └── large_explosion.ogg
│   │   ├── ship_effects/          # Shared ship effects
│   │   │   ├── shield_hit.ogg
│   │   │   ├── hull_damage.ogg
│   │   │   └── subsystem_destroyed.ogg
│   │   └── ui/                    # UI sound effects
│   │       ├── ship_select.ogg
│   │       ├── ship_deselect.ogg
│   │       └── target_lock.ogg
│   └── music/                     # Background music tracks
├── textures/                      # Shared texture files
│   ├── effects/                   # Particle textures used by multiple effects
│   │   ├── explosion_fire.png
│   │   ├── explosion_smoke.png
│   │   └── energy_glow.png
│   └── fonts/                     # Font textures
└── animations/                    # Shared animation files
    └── ui/                        # UI animations
        ├── ship_selection/
        └── target_acquisition/
```

### Scripts Directory Structure
Reusable ship system scripts are organized in the `/scripts/entities/` directory, following the separation of concerns principle where nothing in this folder should be a complete, instantiable game object.

```
scripts/
├── entities/                      # Base entity scripts
│   ├── base_fighter.gd            # Base fighter controller
│   ├── base_capital_ship.gd       # Base capital ship controller
│   └── ship_systems/              # Ship subsystem components
│       ├── weapon_system.gd       # Weapon system management
│       ├── subsystem.gd           # Subsystem component
│       ├── subsystem_template.gd  # Subsystem template resource
│       └── physics_controller.gd  # Physics system controller
├── ai/                            # AI behavior scripts
│   ├── ai_behavior.gd             # Base AI behavior class
│   ├── combat_tactics.gd          # Combat behavior logic
│   └── navigation.gd              # Navigation and pathfinding
└── utilities/                     # Utility functions and helpers
    ├── resource_loader.gd         # Resource loading utilities
    └── object_pool.gd             # Generic object pooling system
```

### Autoload Directory Structure
Ship management systems are implemented as autoload singletons, following the "Is this state or service truly global and required everywhere?" principle.

```
autoload/
├── ship_manager.gd                # Ship creation and management system
├── entity_manager.gd              # Generic entity management with pooling
├── event_bus.gd                   # Global event system for ship events
└── resource_loader.gd             # Resource loading utilities
```

## Data Conversion Strategy

### Configuration Files (.tbl)
Convert to Godot resources (.tres) organized by feature:
- Ship definitions to ShipData resources in `/features/{ship_type}/{ship_name}/{ship_name}.tres`
- Weapon definitions to WeaponData resources in `/assets/data/weapons/`
- AI profiles to AIProfile resources in `/assets/data/ai/`
- Species and IFF relationship definitions in `/assets/data/species/` and `/assets/data/iff/`
- Armor type damage modifiers in `/assets/data/armor/`
- Effect system parameters in `/assets/data/effects/`
- Use Godot's resource system for data-driven design with centralized management

### TRES Resources Structure
```ini
# Location: /features/fighters/confed_arrow/arrow.tres
[gd_resource type="Resource" load_steps=4 format=2]

[ext_resource path="res://scripts/physics/fighter_physics.tres" type="Resource" id=1]
[ext_resource path="res://scripts/entities/ship_systems/templates/subsystem_template.tres" type="Resource" id=2]
[ext_resource path="res://features/weapons/templates/weapon_hardpoint.tres" type="Resource" id=3]

[resource]
resource_name = "F-27B_Arrow"
name = "F-27B Arrow"
description = "Light Fighter"
manufacturer = "Douglas Aerospace"
ship_type = "FIGHTER"
model_path = "res://features/fighters/confed_arrow/arrow.glb"
icon_path = "res://features/fighters/confed_arrow/arrow_icon.png"
thruster_positions = [Vector3(0, 0, -10), Vector3(2, 0, -5), Vector3(-2, 0, -5)]
max_hull_strength = 280.0
max_shield_strength = 800.0
shield_recharge_rate = 0.04
physics_properties = ExtResource(1)
subsystem_templates = [ExtResource(2)]
weapon_hardpoints = [ExtResource(3)]
destruction_type = "EXPLODE"
default_ai_profile = "CAPTAIN"
```

### TSCN Scenes Structure
```ini
# Location: /features/fighters/confed_arrow/arrow.tscn
[gd_scene load_steps=4 format=2]

[ext_resource path="res://features/fighters/confed_arrow/arrow.gd" type="Script" id=1]
[ext_resource path="res://features/fighters/confed_arrow/arrow.tres" type="Resource" id=2]
[ext_resource path="res://features/fighters/confed_arrow/arrow.glb" type="PackedScene" id=3]

[node name="Arrow" type="Node3D"]
script = ExtResource(1)
ship_class = ExtResource(2)

[node name="Model" type="Node3D" parent="."]
instance = ExtResource(3)

[node name="Thruster1" type="Node3D" parent="."]
position = Vector3(0, 0, -10)

[node name="Thruster2" type="Node3D" parent="."]
position = Vector3(2, 0, -5)

[node name="Thruster3" type="Node3D" parent="."]
position = Vector3(-2, 0, -5)
```

## Example Mapping
For F-27B Arrow fighter:
- tcf_arrow.pof → /features/fighters/confed_arrow/arrow.glb
- arrow.pcx → /features/fighters/confed_arrow/arrow_diffuse.webp
- arrow_normals.pcx → /features/fighters/confed_arrow/arrow_normal.webp
- engine sounds → /features/fighters/confed_arrow/assets/sounds/engine_loop.ogg
- thruster animations → /features/fighters/confed_arrow/assets/effects/thruster_particles.tscn
- ships.tbl entry → /features/fighters/confed_arrow/arrow.tres

For TCS Behemoth capital ship:
- tcs_behemoth.pof → /features/capital_ships/tcs_behemoth/behemoth.glb
- behemoth textures → /features/capital_ships/tcs_behemoth/behemoth_diffuse.webp
- engine sounds → /features/capital_ships/tcs_behemoth/assets/sounds/engine_loop.ogg
- ships.tbl entry → /features/capital_ships/tcs_behemoth/behemoth.tres

## Conversion Pipeline
1. **POF Converter**: Custom tool to convert .pof models to glTF (.glb) format
2. **Texture Converter**: Convert .pcx/.dds textures to WebP format
3. **Audio Converter**: Convert .wav sounds to Ogg Vorbis format
4. **ANI Converter**: Convert .ani animations to PNG sequences or video format
5. **TBL Parser**: Extract ship definitions from ships.tbl
6. **Resource Generator**: Create Godot .tres files with converted ship data
7. **Scene Builder**: Generate Godot scenes (.tscn) for ships with integrated components
8. **Effect System**: Implement visual effects using Godot's particle systems
9. **Validation**: Verify converted ships match original gameplay characteristics

## Relationship to Other Assets
Ships are closely related to:
- **Weapon System**: Ships mount and fire weapons from `/features/weapons/`
- **AI System**: Each ship has associated AI behaviors from `/scripts/ai/`
- **Physics System**: Ships use physics properties from `/scripts/physics/`
- **Visual Effects System**: Ships use effects from `/features/effects/` and `/assets/textures/effects/`
- **Audio System**: Ships use shared sounds from `/assets/audio/` and ship-specific sounds from their feature directories
- **Entity System**: Ships are managed by the entity system in `/autoload/entity_manager.gd`
- **Mission System**: Missions create and manage ships from `/campaigns/` directory
- **UI System**: Ships are displayed in UI elements like the tech database from `/features/ui/tech_database/`

This organization follows the feature-based approach where each ship is a self-contained entity with all its related assets, while shared assets are properly organized in the global `/assets/` directory following the "Global Litmus Test" principle. The structure maintains clear separation of concerns between different systems while ensuring easy access to all assets needed for each ship feature.