# Data Converter Concepts

## Overview
This directory contains detailed specifications for converting Wing Commander Saga assets from their original formats to Godot-compatible formats. The documents describe the requirements and processes for converting each asset type, following Godot's feature-based organization principles.

## Consolidated Specification
The complete asset conversion specifications have been consolidated into a single comprehensive document:

- [Consolidated Specifications](consolidated_specifications.md) - Complete specifications for all asset types and conversion processes

## Asset Type Specifications
Individual documents for each asset type:

- [TBL Files](tbl_files.md) - Table data files containing game definitions
- [FS2 Files](fs2_files.md) - Mission files with scripting and placements
- [POF Files](pof_files.md) - 3D model files for ships and objects
- [PCX Files](pcx_files.md) - Texture and UI graphics files
- [WAV Files](wav_files.md) - Audio files for sound effects and music
- [ANI Files](ani_files.md) - Animation sequence files
- [TXT Files](txt_files.md) - Narrative text and documentation
- [TBM Files](tbm_files.md) - Modular table override files

## Conversion Process
Documents covering the overall conversion approach:

- [Scene Assembly](scene_assembly.md) - How assets are combined into complete scenes
- [Asset Relationships](asset_relationships.md) - Closely related assets and directory organization

## Conversion Pipeline

The asset conversion follows this dependency-ordered pipeline:

1. **Data Extraction** - Parse original file formats
   - Table files (.tbl/.tbm) for game definitions
   - Texture files (.pcx) for graphics
   - Audio files (.wav) for sound

2. **Format Conversion** - Convert to Godot-compatible formats
   - Tables → Godot Resource files (.tres) in `/data/`
   - Models → glTF 2.0 (.glb/.gltf) in `/entities/`
   - Textures → WebP/PNG in `/textures/`
   - Audio → Ogg Vorbis in `/audio/`
   - Animations → Sprite sheets in `/animations/`
   - Text → BBCode in `/text/`

3. **Asset Optimization** - Optimize for performance and quality
   - Generate mipmaps for textures
   - Apply appropriate compression settings
   - Optimize 3D models for GPU rendering
   - Create efficient sprite atlases

4. **Integration** - Combine assets into functional game elements
   - Assemble entity scenes in `/entities/`
   - Create mission scenes in `/missions/`
   - Build UI scenes in `/ui/`

5. **Validation** - Verify quality and compatibility
   - Check cross-references between assets
   - Validate scene loading and performance
   - Test gameplay functionality
   - Ensure cross-platform compatibility

## Asset Relationships

Assets in Wing Commander Saga have complex interdependencies that must be maintained during conversion:

### Core Entity Relationships
- **Ships** ←→ Weapons, Models, Textures, Sounds
  - Ship definitions (.tbl) reference weapon hardpoints
  - Ship models (.pof) reference texture files (.pcx)
  - Ship entities integrate engine sounds (.wav)
  - Ship AI behaviors reference AI profiles (.tbl)

- **Weapons** ←→ Effects, Models, Sounds
  - Weapon definitions (.tbl) reference projectile types
  - Weapon models (.pof) reference firing effects (.ani)
  - Weapon entities integrate firing sounds (.wav)
  - Weapon impacts reference explosion effects (.ani/.wav)

- **Missions** ←→ Ships, Weapons, Effects, Text
  - Mission scripts (.fs2) reference ship definitions (.tbl)
  - Mission placements use converted ship models (.pof→.glb)
  - Mission events trigger effects (.ani/.wav)
  - Mission briefings reference fiction text (.txt)

- **Effects** ←→ Textures, Animations, Sounds
  - Particle effects (.ani) reference texture files (.pcx)
  - Visual effects integrate audio feedback (.wav)
  - Animated sequences combine multiple frames (.ani)

- **UI Elements** ←→ Graphics, Fonts, Animations
  - Interface components reference UI graphics (.pcx→.png)
  - Text displays use font resources
  - Animated elements reference animation sequences (.ani)

The conversion process must maintain these relationships while adapting to Godot's resource system and scene composition.

## Feature-Based Organization

All converted assets follow Godot's feature-based organization principles, where each conceptual unit is grouped together in a self-contained directory:

### Data Organization (`/data/`)
Contains all data-driven Resource files (.tres) organized by type:
- `/data/ships/` - Ship data resources organized by faction and type
  - `/data/ships/terran/fighters/`, `/data/ships/kilrathi/capitals/`, etc.
- `/data/weapons/` - Weapon data resources organized by faction
  - `/data/weapons/terran/lasers/`, `/data/weapons/kilrathi/missiles/`, etc.
- `/data/ai/` - AI behavior data and profiles
- `/data/species/` - Species definitions and properties
- `/data/iff/` - IFF (Identification Friend or Foe) relationships
- `/data/armor/` - Armor type definitions and damage modifiers
- `/data/effects/` - Effect data resources

### Entity Organization (`/entities/`)
Contains physical game objects as self-contained scenes with all related assets:
- `/entities/fighters/` - Fighter ship entities with all related assets
  - Example: `/entities/fighters/confed_rapier/rapier.tscn`, `rapier.glb`, `rapier.tres`
- `/entities/capital_ships/` - Capital ship entities
- `/entities/weapons/` - Weapon entities
- `/entities/projectiles/` - Projectile entities
- `/entities/effects/` - Effect entities
- `/entities/environment/` - Environmental entities

### Campaign Organization (`/campaigns/`)
Contains campaign data, progression, and mission scenes organized by campaign:
- `/campaigns/hermes/` - Hermes campaign
  - `/campaigns/hermes/missions/m01_hermes/`, `/campaigns/hermes/fiction/`, etc.
- `/campaigns/brimstone/` - Brimstone campaign
- `/campaigns/training/` - Training campaign

### Media Organization
- `/textures/` - All converted texture files (.webp/.png)
  - `/textures/ships/`, `/textures/ui/`, `/textures/effects/`, etc.
- `/audio/` - All converted audio files (.ogg)
  - `/audio/sfx/`, `/audio/music/`, `/audio/voice/`, etc.
- `/animations/` - All converted animation files
  - `/animations/effects/`, `/animations/ui/`, etc.
- `/text/` - All converted text files (.txt with BBCode)
  - `/text/fiction/`, `/text/technical/`, etc.

This approach ensures that:
1. Related assets are grouped together in self-contained directories
2. Shared assets are placed in common directories with clear cross-references
3. The directory structure reflects gameplay relationships
4. Each feature can be developed, tested, and maintained in isolation

This organization provides maintainability and modularity in the converted Godot project while preserving the relationships between assets from the original Wing Commander Saga.