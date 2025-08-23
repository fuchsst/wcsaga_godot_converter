# POF Files Conversion Requirements

## Overview
POF (Parallax Object Format) files contain 3D model data for all ships, weapons, space stations, and other visual elements in Wing Commander Saga. These binary files need to be converted to glTF 2.0 format (.glb/.gltf) for compatibility with Godot's modern renderer, following Godot's feature-based organization principles.

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

## Feature-Based Directory Structure
Following Godot's recommended directory structure:
```
/entities/
├── fighters/              # Fighter ship entities
│   ├── confed_rapier/     # Raptor fighter
│   │   ├── rapier.tscn    # Scene file
│   │   ├── rapier.gd      # Script file
│   │   ├── rapier.tres    # Ship data resource
│   │   ├── rapier.glb     # 3D model
│   │   ├── rapier.png     # Texture
│   │   └── rapier_engine.ogg # Engine sound
│   ├── kilrathi_dralthi/  # Dralthi fighter
│   │   ├── dralthi.tscn
│   │   ├── dralthi.gd
│   │   ├── dralthi.tres
│   │   ├── dralthi.glb
│   │   ├── dralthi.png
│   │   └── dralthi_engine.ogg
│   └── templates/         # Fighter templates
├── capital_ships/         # Capital ship entities
│   ├── tcs_tigers_claw/   # Tigers Claw carrier
│   │   ├── tigers_claw.tscn
│   │   ├── tigers_claw.gd
│   │   ├── tigers_claw.tres
│   │   ├── tigers_claw.glb
│   │   └── tigers_claw.png
│   └── templates/         # Capital ship templates
├── projectiles/           # Projectile entities
│   ├── laser_bolt/        # Laser bolt projectile
│   │   ├── laser_bolt.tscn
│   │   ├── laser_bolt.gd
│   │   └── laser_bolt.tres
│   ├── missile/           # Missile projectile
│   │   ├── missile.tscn
│   │   ├── missile.gd
│   │   └── missile.tres
│   └── templates/         # Projectile templates
├── weapons/               # Weapon entities
│   ├── laser_cannon/      # Laser cannon weapon
│   │   ├── laser_cannon.tscn
│   │   ├── laser_cannon.gd
│   │   └── laser_cannon.tres
│   └── templates/         # Weapon templates
├── effects/               # Effect entities
│   ├── explosion/         # Explosion effect
│   │   ├── explosion.tscn
│   │   ├── explosion.gd
│   │   └── explosion.tres
│   ├── fireball/          # Fireball effect
│   │   ├── fireball.tscn
│   │   ├── fireball.gd
│   │   └── fireball.tres
│   └── templates/         # Effect templates
├── environment/           # Environmental entities
│   ├── asteroid/          # Asteroid object
│   │   ├── asteroid.tscn
│   │   ├── asteroid.gd
│   │   └── asteroid.tres
│   ├── nebula/            # Nebula effect
│   │   ├── nebula.tscn
│   │   ├── nebula.gd
│   │   └── nebula.tres
│   └── templates/         # Environment templates
└── templates/             # Entity templates
```

## Data Integration
Converted POF models integrate with data resources in `/data/` directories:
- ShipClass resources in `/data/ships/{faction}/{type}/` link to model files
- WeaponClass resources in `/data/weapons/{faction}/` link to model files
- Effect resources in `/data/effects/` link to model files

## System Integration
Models integrate with various Godot systems:
- `/systems/physics/` - Physics properties and collision shapes
- `/systems/graphics/` - Rendering materials and shaders
- `/systems/audio/` - Audio emitters for engine sounds
- `/systems/ai/` - Hardpoint data for weapon mounting
- `/systems/weapon_control/` - Weapon hardpoint positioning

## Closely Related Assets
- Texture files (.pcx) referenced in TXTR chunks and converted to `/textures/` directories
- Animation files (.ani) that affect model components and converted to `/animations/` directories
- Particle effect definitions used with model hardpoints from `/data/effects/`
- Sound files (.wav/.ogg) associated with model events and converted to `/audio/` directories

## Entity Asset Organization
Each entity in `/entities/` contains all related assets:
- `.glb` model files with embedded metadata
- Hardpoint information preserved as named nodes
- Subsystem locations maintained for damage modeling
- Thruster positions for engine effects
- Weapon mounting points for armament

## Common Shared Assets
- Standard engine thruster effects used across multiple ship classes from `/entities/effects/engine/`
- Common weapon mounting point configurations shared between similar weapon types
- Shared debris models for destruction effects from `/entities/environment/debris/`
- Standard shield mesh templates for similar ship types from `/data/ships/templates/`
- Common cockpit and interior model components from `/entities/fighters/templates/cockpit/`