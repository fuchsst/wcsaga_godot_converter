# Godot Integration Mapping for Converted Assets

## Overview
This document provides a clear mapping between converted assets from the data converter and their integration into the Godot project structure, ensuring seamless transition from legacy formats to modern Godot implementation.

## Asset Type Integration Mapping

### 1. Table Data Files (.tbl/.tbm → .tres)
**Data Converter Output**: `/data/{type}/{faction}/{subtype}/{entity}.tres`
**Godot Target Structure**: `/data/{type}/{faction}/{subtype}/{entity}.tres`

**Integration Points**:
- ShipClass resources → `/entities/fighters/{faction}/{ship}/` entity scenes
- WeaponClass resources → `/entities/weapons/{weapon}/` entity scenes
- AIProfile resources → `/systems/ai/profiles/` behavior definitions
- Mission data resources → `/missions/{campaign}/{mission}/` scene resources

### 2. Model Files (.pof → .glb/.gltf)
**Data Converter Output**: `/entities/{type}/{entity}/{entity}.glb`
**Godot Target Structure**: `/entities/{type}/{entity}/{entity}.glb`

**Integration Points**:
- 3D models with hardpoint metadata → Entity scenes in `/entities/`
- Subsystem positions → Damage modeling in ship entities
- Thruster locations → Engine effects in ship entities
- Weapon hardpoints → Weapon mounting in ship entities

### 3. Texture Files (.pcx → WebP/PNG)
**Data Converter Output**: `/textures/{type}/{subtype}/{texture}.{webp|png}`
**Godot Target Structure**: `/textures/{type}/{subtype}/{texture}.{webp|png}`

**Integration Points**:
- Ship textures → 3D model materials in `/entities/fighters/`
- UI graphics → Interface elements in `/ui/`
- Effect textures → Particle systems in `/animations/`
- Font graphics → Text rendering in `/ui/`

### 4. Audio Files (.wav → Ogg Vorbis)
**Data Converter Output**: `/audio/{type}/{subtype}/{sound}.ogg`
**Godot Target Structure**: `/audio/{type}/{subtype}/{sound}.ogg`

**Integration Points**:
- Engine sounds → Ship entities in `/entities/fighters/`
- Weapon sounds → Weapon entities in `/entities/weapons/`
- Explosion sounds → Effect entities in `/entities/effects/`
- Voice acting → Mission scenes in `/missions/`
- Music tracks → Campaign and mission scenes

### 5. Animation Files (.ani → Sprite Sheets)
**Data Converter Output**: `/animations/{type}/{subtype}/{animation}/`
**Godot Target Structure**: `/animations/{type}/{subtype}/{animation}/`

**Integration Points**:
- Explosion effects → Effect entities in `/entities/effects/`
- UI animations → Interface elements in `/ui/`
- Weapon effects → Weapon entities in `/entities/weapons/`
- Particle effects → Visual systems in `/systems/graphics/`

### 6. Mission Files (.fs2 → .tscn/.tres)
**Data Converter Output**: `/missions/{campaign}/{mission}/{mission}.tscn`
**Godot Target Structure**: `/missions/{campaign}/{mission}/{mission}.tscn`

**Integration Points**:
- Mission scenes → Gameplay execution in `/missions/`
- Event timelines → Mission control in `/systems/mission_control/`
- Entity placements → Scene composition using converted entities
- Scripting logic → Mission behavior using Godot's animation system

### 7. Text Files (.txt → BBCode)
**Data Converter Output**: `/text/{type}/{subtype}/{content}.txt`
**Godot Target Structure**: `/text/{type}/{subtype}/{content}.txt`

**Integration Points**:
- Fiction text → Briefing screens in `/ui/briefing/`
- Technical entries → Tech database in `/ui/tech_database/`
- Credits → Credits display in `/ui/`
- Documentation → Help systems in `/ui/`

## Cross-Reference Integration

### Resource References
- **Data Resources** (.tres) are referenced by:
  - Entity scenes in `/entities/`
  - Mission scenes in `/missions/`
  - UI components in `/ui/`
  - System components in `/systems/`

### Asset References
- **Media Assets** are referenced by:
  - 3D models (.glb) in entity scenes
  - Materials in visual effects
  - Audio players in entity and UI scenes
  - Animation players in effect and UI scenes

## Directory Structure Alignment

| Data Converter Output | Godot Target Structure | Purpose |
|----------------------|------------------------|---------|
| `/data/` | `/data/` | Game data definitions |
| `/entities/` | `/entities/` | Physical game objects |
| `/textures/` | `/textures/` | Texture and UI graphics |
| `/audio/` | `/audio/` | Audio files |
| `/animations/` | `/animations/` | Animation sequences |
| `/missions/` | `/missions/` | Mission scenes and data |
| `/text/` | `/text/` | Narrative text and documentation |

## Validation Integration Points

### Asset Validation
- **Format Compliance**: Verify converted assets match Godot format specifications
- **Cross-Reference Integrity**: Ensure all resource references resolve correctly
- **Performance Metrics**: Validate asset sizes and loading times
- **Platform Compatibility**: Test assets on target platforms

### Gameplay Validation
- **Entity Behavior**: Verify entity scenes function with converted data
- **Mission Flow**: Test mission scenes with integrated assets
- **UI Presentation**: Validate text and graphics display correctly
- **Audio-Visual Sync**: Confirm audio and visual effects align properly

## Migration Workflow

### Phase 1: Data Foundation
1. Convert .tbl/.tbm files to .tres resources
2. Place in `/data/` directory structure
3. Validate cross-references and data integrity

### Phase 2: Media Assets
1. Convert .pof files to .glb/.gltf models
2. Convert .pcx files to WebP/PNG textures
3. Convert .wav files to Ogg Vorbis audio
4. Convert .ani files to sprite sheet animations
5. Place in respective directory structures

### Phase 3: Content Integration
1. Convert .txt files to BBCode text resources
2. Convert .fs2 files to Godot mission scenes
3. Integrate all assets into entity and mission scenes
4. Validate gameplay functionality

### Phase 4: Quality Assurance
1. Test cross-reference integrity
2. Verify performance metrics
3. Validate platform compatibility
4. Confirm gameplay balance and presentation

This mapping ensures a smooth transition from legacy asset formats to the modern Godot implementation while maintaining all gameplay relationships and functionality.