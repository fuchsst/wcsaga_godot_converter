# Godot Integration Mapping for Converted Assets

## Overview
This document provides a clear mapping between converted assets from the data converter and their integration into the Godot project structure, ensuring seamless transition from legacy formats to modern Godot implementation. The mapping follows the feature-based organizational approach and hybrid model defined in our project structure.

## Asset Type Integration Mapping

### 1. Table Data Files (.tbl/.tbm → .tres)
**Data Converter Output**: `/assets/data/{type}/{subtype}/{entity}.tres`
**Godot Target Structure**: `/assets/data/{type}/{subtype}/{entity}.tres`

**Integration Points**:
- ShipClass resources → `/assets/data/ships/{ship_class}.tres` referenced by ship entity scenes
- WeaponClass resources → `/assets/data/weapons/{weapon_class}.tres` referenced by weapon entity scenes
- AIProfile resources → `/assets/data/ai/profiles/{profile_name}.tres` referenced by AI system scripts
- Mission data resources → `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/mission_data.tres`
- Species definitions → `/assets/data/species/{species_name}.tres`
- IFF definitions → `/assets/data/iff/{iff_name}.tres`
- Armor type definitions → `/assets/data/armor/{armor_type}.tres`
- Effect system parameters → `/assets/data/effects/{effect_name}.tres`

### 2. Model Files (.pof → .glb/.gltf)
**Data Converter Output**: `/features/{category}/{entity}/{entity}.glb`
**Godot Target Structure**: `/features/{category}/{entity}/{entity}.glb`

**Integration Points**:
- 3D models with hardpoint metadata → Entity scenes in `/features/fighters/{ship}/` or `/features/capital_ships/{ship}/`
- Subsystem positions → Damage modeling in ship entities
- Thruster locations → Engine effects in ship entities
- Weapon hardpoints → Weapon mounting in ship entities

### 3. Texture Files (.pcx/.dds → WebP)
**Data Converter Output**: `/features/{category}/{entity}/{texture}.webp` or `/assets/textures/{type}/{subtype}/{texture}.webp`
**Godot Target Structure**: 
  - Feature-specific: `/features/{category}/{entity}/{texture}.webp`
  - Global assets: `/assets/textures/{type}/{subtype}/{texture}.webp`

**Integration Points**:
- Ship textures → 3D model materials in `/features/fighters/{ship}/` or `/features/capital_ships/{ship}/`
- UI graphics → Interface elements in `/features/ui/{component}/`
- Effect textures → Particle systems in `/features/effects/{effect}/` or `/assets/textures/effects/`
- Font graphics → Text rendering in `/features/ui/_shared/fonts/` or `/assets/textures/fonts/`

### 4. Audio Files (.wav/.ogg → Ogg Vorbis)
**Data Converter Output**: `/features/{category}/{entity}/{sound}.ogg` or `/assets/audio/{type}/{subtype}/{sound}.ogg`
**Godot Target Structure**: 
  - Feature-specific: `/features/{category}/{entity}/{sound}.ogg`
  - Global assets: `/assets/audio/{type}/{subtype}/{sound}.ogg`

**Integration Points**:
- Engine sounds → Ship entities in `/features/fighters/{ship}/` or `/features/capital_ships/{ship}/`
- Weapon sounds → Weapon entities in `/features/weapons/{weapon}/`
- Explosion sounds → Effect entities in `/features/effects/{effect}/`
- Voice acting → Mission scenes in `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/`
- Music tracks → Campaign and mission scenes
- UI sounds → `/assets/audio/ui/` referenced by UI components

### 5. Animation Files (.ani → Sprite Sheets/WebP)
**Data Converter Output**: `/features/{category}/{entity}/{animation}/` or `/assets/animations/{type}/{subtype}/{animation}/`
**Godot Target Structure**: 
  - Feature-specific: `/features/{category}/{entity}/{animation}/`
  - Global assets: `/assets/animations/{type}/{subtype}/{animation}/`

**Integration Points**:
- Explosion effects → Effect entities in `/features/effects/{effect}/`
- UI animations → Interface elements in `/features/ui/{component}/`
- Weapon effects → Weapon entities in `/features/weapons/{weapon}/`
- Particle effects → Visual systems in game logic

### 6. Mission Files (.fs2 → .tscn/.tres)
**Data Converter Output**: `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/{mission}.tscn`
**Godot Target Structure**: `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/{mission}.tscn`

**Integration Points**:
- Mission scenes → Gameplay execution in `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/`
- Event timelines → Mission control logic using Godot's animation system
- Entity placements → Scene composition using converted entities
- Scripting logic → Mission behavior using Godot's node system

### 7. Text Files (.txt → BBCode/.tres)
**Data Converter Output**: `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/{content}.txt`
**Godot Target Structure**: `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/{content}.txt`

**Integration Points**:
- Fiction text → Mission scenes in `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/`
- Technical entries → Tech database in `/features/ui/tech_database/`
- Credits → Credits display in `/features/ui/`
- Documentation → Help systems in `/features/ui/`

## Cross-Reference Integration

### Resource References
- **Data Resources** (.tres) are referenced by:
  - Entity scenes in `/features/fighters/{ship}/`, `/features/capital_ships/{ship}/`, `/features/weapons/{weapon}/`, `/features/effects/{effect}/`
  - Mission scenes in `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/`
  - UI components in `/features/ui/{component}/`
  - System components in `/scripts/`
  - Autoload systems in `/autoload/`

### Asset References
- **Media Assets** are referenced by:
  - 3D models (.glb) in entity scenes
  - Materials in visual effects
  - Audio players in entity and UI scenes
  - Animation players in effect and UI scenes

## Directory Structure Alignment

| Data Type | Data Converter Output | Godot Target Structure | Purpose |
|-----------|----------------------|------------------------|---------|
| Table Data | `/assets/data/{type}/` | `/assets/data/{type}/` | Configuration data resources |
| 3D Models | `/features/{category}/{entity}/` | `/features/{category}/{entity}/` | Self-contained game features with models |
| Textures | `/features/{category}/{entity}/` or `/assets/textures/` | `/features/{category}/{entity}/` or `/assets/textures/` | Feature-specific or shared textures |
| Audio | `/features/{category}/{entity}/` or `/assets/audio/` | `/features/{category}/{entity}/` or `/assets/audio/` | Feature-specific or shared audio |
| Animations | `/features/{category}/{entity}/` or `/assets/animations/` | `/features/{category}/{entity}/` or `/assets/animations/` | Feature-specific or shared animations |
| Missions | `/campaigns/{campaign}/missions/` | `/campaigns/{campaign}/missions/` | Campaign data and mission scenes |
| Text | `/campaigns/{campaign}/missions/` | `/campaigns/{campaign}/missions/` | Narrative content and UI text |

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
1. Convert .tbl/.tbm files to .tres resources following the "Global Litmus Test"
2. Place data resources in `/assets/data/` directory structure organized by type
3. Validate cross-references and data integrity
4. Create relationships between data resources and feature entities

### Phase 2: Media Assets
1. Convert .pof files to .glb/.gltf models preserving model hierarchy
2. Convert .pcx/.dds files to WebP textures maintaining visual quality
3. Convert .wav/.ogg files to Ogg Vorbis audio preserving characteristics
4. Convert .ani files to sprite sheet animations or particle effects
5. Place assets in respective directory structures following feature-based organization

### Phase 3: Content Integration
1. Convert .txt files to BBCode text resources preserving formatting
2. Convert .fs2 files to Godot mission scenes in `/campaigns/{campaign}/missions/`
3. Integrate all assets into entity and mission scenes following co-location principle
4. Validate gameplay functionality and cross-references

### Phase 4: Quality Assurance
1. Test cross-reference integrity between all assets and resources
2. Verify performance metrics meet targets
3. Validate platform compatibility across target hardware
4. Confirm gameplay balance and presentation match original experience

## Integration Examples

### Ship Integration Example (F-27B Arrow Fighter)
- **Legacy**: tcf_arrow.pof, arrow.pcx, arrow_normals.pcx, engine sounds
- **Converted**: `/features/fighters/confed_arrow/arrow.glb`, `/features/fighters/confed_arrow/arrow_diffuse.webp`, `/features/fighters/confed_arrow/arrow_normal.webp`, `/features/fighters/confed_arrow/assets/sounds/engine_loop.ogg`
- **Data**: `/assets/data/ships/confed_arrow.tres` (from ships.tbl)
- **Scene**: `/features/fighters/confed_arrow/arrow.tscn`

### Weapon Integration Example (Ion Cannon)
- **Legacy**: weapons.tbl entry, Ion_Bitmap.DDS, Ion_Glow.DDS, snd_80.wav, snd_85.wav
- **Converted**: `/assets/data/weapons/weapon_definitions/ion_cannon.tres`, `/features/weapons/ion_cannon/ion_cannon.webp`, `/features/weapons/ion_cannon/ion_glow.webp`, `/features/weapons/ion_cannon/ion_fire.ogg`, `/features/weapons/ion_cannon/ion_impact.ogg`
- **Scene**: `/features/weapons/ion_cannon/ion_cannon.tscn`

### AI Profile Integration Example (SAGA RETAIL)
- **Legacy**: ai_profiles.tbl entry
- **Converted**: `/assets/data/ai/profiles/saga_retail.tres`
- **Behavior Trees**: `/assets/behavior_trees/ai/combat/bt_attack.lbt`, `/assets/behavior_trees/ai/combat/bt_evade.lbt`

## Shared Directory Integration

### Feature-Specific Shared Assets
- **Fighters**: `/features/fighters/_shared/cockpits/`, `/features/fighters/_shared/effects/`
- **Capital Ships**: `/features/capital_ships/_shared/bridge_models/`, `/features/capital_ships/_shared/turret_models/`
- **Weapons**: `/features/weapons/_shared/muzzle_flashes/`, `/features/weapons/_shared/impact_effects/`
- **Effects**: `/features/effects/_shared/particle_textures/`, `/features/effects/_shared/shader_effects/`
- **UI**: `/features/ui/_shared/fonts/`, `/features/ui/_shared/icons/`, `/features/ui/_shared/themes/`

### Global Shared Assets
- **Audio**: `/assets/audio/sfx/weapons/`, `/assets/audio/sfx/ai/`, `/assets/audio/voice/ai/`
- **Textures**: `/assets/textures/effects/weapons/`, `/assets/textures/fonts/`, `/assets/textures/ui/`
- **Behavior Trees**: `/assets/behavior_trees/ai/combat/`, `/assets/behavior_trees/ai/navigation/`, `/assets/behavior_trees/ai/tactical/`
- **Data**: `/assets/data/ai/profiles/`, `/assets/data/weapons/weapon_definitions/`, `/assets/data/species/`, `/assets/data/iff/`

This mapping ensures a smooth transition from legacy asset formats to the modern Godot implementation while maintaining all gameplay relationships and functionality, following the feature-based organizational approach and hybrid model that combines scalability with a clean repository for generic, reusable assets.