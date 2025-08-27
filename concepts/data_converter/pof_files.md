# POF Files Conversion Requirements

## Overview
POF (Parallax Object Format) files contain 3D model data for all ships, weapons, space stations, and other visual elements in Wing Commander Saga. These binary files need to be converted to glTF 2.0 format (.glb/.gltf) for compatibility with Godot's modern renderer, following Godot's feature-based organization principles and the hybrid model defined in our project structure.

## File Structure and Components

### Header Information
**Purpose**: File identification and version information
**Conversion Requirements**:
- Parse POF file signature and version
- Extract model name and identification
- Validate file integrity and structure
- Handle version-specific format differences

### Geometry Data (SOBJ Chunks)
**Purpose**: 3D mesh geometry definitions
**Conversion Requirements**:
- Parse vertex positions, normals, and texture coordinates
- Convert face definitions and polygon structures
- Handle BSP (Binary Space Partitioning) tree data
- Triangulate polygons for modern rendering
- Optimize vertex data for GPU rendering

### Texture References (TXTR Chunks)
**Purpose**: Texture mapping and material definitions
**Conversion Requirements**:
- Extract texture filename references
- Map texture coordinates to geometry
- Convert texture wrapping and filtering settings
- Handle multiple texture layers (detail, glow, etc.)
- Maintain texture animation properties

### Hardpoint Definitions
**Purpose**: Attachment points for weapons, engines, and other components
**Conversion Requirements**:
- Parse gun mounting points (GPNT chunks)
- Convert missile hardpoints (MPNT chunks)
- Extract docking points (DOCK chunks)
- Map thruster locations (FUEL chunks)
- Handle subsystem positions (SPCL chunks)

### Shield Mesh Data (SHLD Chunks)
**Purpose**: Collision and damage modeling for shields
**Conversion Requirements**:
- Parse shield mesh geometry
- Convert shield hit detection properties
- Map shield quadrant definitions
- Handle shield regeneration properties

### Model Hierarchy
**Purpose**: Parent-child relationships between model components
**Conversion Requirements**:
- Parse subobject hierarchy and transformations
- Convert relative positioning and rotations
- Handle model detail levels (LOD)
- Maintain animation attachment points
- Preserve subsystem identification

## Conversion Process

### 1. Format Analysis Phase
- Validate POF file structure and version
- Extract metadata and file information
- Identify all chunk types and their locations
- Validate data integrity and consistency

### 2. Geometry Conversion Phase
- Parse vertex and face data from SOBJ chunks
- Triangulate polygon meshes for modern rendering
- Generate normals if not provided
- Optimize vertex data for GPU efficiency
- Handle coordinate system conversion (right-handed to left-handed)

### 3. Material Mapping Phase
- Parse texture references from TXTR chunks
- Create material definitions with PBR properties
- Map texture coordinates to UV sets
- Handle multi-layer texture blending
- Convert texture animation parameters

### 4. Hardpoint Integration Phase
- Extract all hardpoint locations and types
- Create named attachment points in glTF structure
- Map weapon mounting information
- Handle engine thruster positions
- Maintain subsystem location data

### 5. glTF Generation Phase
- Create glTF scene hierarchy from model structure
- Generate mesh primitives with material assignments
- Embed texture data or create external references
- Create named nodes for hardpoints and subsystems
- Export to .glb (binary) or .gltf (JSON) format

## Directory Structure Alignment
Following the Godot project structure defined in directory_structure.md and the hybrid organizational model:

### Features Directory Structure
3D models are organized within feature directories following the co-location principle where all files related to a single feature are grouped together:

```
features/
├── fighters/                      # Fighter ship entities (primary player and AI ships)
│   ├── confed_arrow/              # F-27B Arrow fighter - all files together
│   │   ├── arrow.tscn             # Ship scene file
│   │   ├── arrow.gd               # Ship controller script
│   │   ├── arrow.tres             # Ship data resource
│   │   ├── arrow.glb              # 3D model
│   │   ├── arrow_diffuse.webp     # Diffuse texture
│   │   ├── arrow_normal.webp      # Normal map
│   │   ├── arrow_engine.ogg       # Engine sound
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
│   │   ├── rapier_diffuse.webp    # Diffuse texture
│   │   ├── rapier_normal.webp     # Normal map
│   │   └── rapier_engine.ogg      # Engine sound
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
│   │   ├── behemoth.tres          # Ship data resource
│   │   ├── behemoth.glb           # 3D model
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
│   │   ├── javelin_missile.glb    # 3D model
│   │   ├── javelin_missile.webp   # Weapon texture
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
│   │   │   └── javelin_projectile.glb  # 3D model
│   │   └── templates/             # Projectile templates
│   ├── _shared/                   # Shared weapon assets
│   │   ├── muzzle_flashes/        # Shared muzzle flash effects
│   │   ├── impact_effects/        # Shared impact effects
│   │   └── explosion_effects/     # Shared explosion effects
│   └── templates/                 # Weapon templates
├── effects/                       # Effect entities
│   ├── explosion/                 # Explosion effect
│   │   ├── explosion.tscn         # Effect scene
│   │   ├── explosion.gd           # Effect script
│   │   ├── explosion.tres         # Effect data resource
│   │   ├── explosion_fire.webp    # Fire texture
│   │   └── explosion_sound.ogg    # Explosion sound
│   ├── _shared/                   # Shared effect assets
│   │   ├── particle_textures/     # Shared particle effects
│   │   └── shader_effects/        # Shared shader effects
│   └── templates/                 # Effect templates
├── environment/                   # Environmental objects and props
│   ├── asteroid/                  # Asteroid object
│   │   ├── asteroid.tscn
│   │   ├── asteroid.gd
│   │   ├── asteroid.tres
│   │   ├── asteroid.glb
│   │   └── asteroid.webp
│   ├── nebula/                    # Nebula effect
│   │   ├── nebula.tscn
│   │   ├── nebula.gd
│   │   ├── nebula.tres
│   │   ├── nebula.glb
│   │   └── nebula.webp
│   ├── _shared/                   # Shared environment assets
│   │   ├── debris/                # Space debris models
│   │   └── environment/           # Environmental textures
│   └── templates/                 # Environment templates
└── templates/                     # Feature templates
```

## Integration Points

### Data Converter Output Mapping
- Ship models → Converted to glTF and placed in `/features/fighters/{ship}/` or `/features/capital_ships/{ship}/`
- Weapon models → Converted to glTF and placed in `/features/weapons/{weapon}/`
- Projectile models → Converted to glTF and placed in `/features/weapons/projectiles/{projectile}/`
- Effect models → Converted to glTF and placed in `/features/effects/{effect}/`
- Environment models → Converted to glTF and placed in `/features/environment/{prop}/`

### Resource References
- **Entity scenes** in `/features/` reference their respective .glb model files
- **Data resources** in feature directories reference model paths for instantiation
- **Hardpoint information** is preserved as named nodes in the glTF structure
- **Subsystem locations** are maintained for damage modeling integration

## Relationship to Other Assets

### Closely Related Assets
- Texture files (.pcx/.dds) referenced in TXTR chunks and converted to WebP format in feature directories or `/assets/textures/`
- Animation files (.ani) that affect model components and converted to sprite sheets in feature directories or `/assets/animations/`
- Particle effect definitions used with model hardpoints from feature directories or `/assets/textures/effects/`
- Sound files (.wav/.ogg) associated with model events and converted to Ogg Vorbis in feature directories or `/assets/audio/`

### Entity Asset Organization
Each entity in `/features/` contains all related assets following the co-location principle:
- `.glb` model files with embedded metadata and named hardpoint nodes
- Hardpoint information preserved as named nodes for weapon mounting and effects
- Subsystem locations maintained for damage modeling integration
- Thruster positions for engine effects and audio emitters
- Weapon mounting points for armament attachment

### Common Shared Assets
- Standard engine thruster effects used across multiple ship classes from `/features/fighters/_shared/effects/`
- Common weapon mounting point configurations shared between similar weapon types
- Shared debris models for destruction effects from `/features/environment/_shared/debris/`
- Standard cockpit models shared between fighter classes from `/features/fighters/_shared/cockpits/`
- Shared turret models for capital ships from `/features/capital_ships/_shared/turret_models/`

This organization follows the feature-based approach where each entity is a self-contained feature with all its related assets, while shared assets are properly organized in `_shared` directories within their respective categories following the hybrid model. The structure maintains clear separation of concerns between different systems while ensuring easy access to all assets needed for each feature.