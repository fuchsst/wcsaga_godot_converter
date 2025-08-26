# Wing Commander Saga to Godot Data Converter Specifications

## Overview
This document provides comprehensive specifications for converting Wing Commander Saga assets from their original formats to Godot-compatible formats, following Godot's feature-based organization principles as defined in the directory_structure.md and Godot_Project_Structure_Refinement.md. It consolidates requirements, technical standards, and implementation guidelines for all asset types, ensuring compliance with the hybrid organizational model that groups all files related to a single conceptual feature into a single, self-contained directory within `/features/`, while maintaining truly global assets in `/assets/` and using `/_shared/` directories for semi-global assets specific to feature categories.

## Complete Asset Conversion Pipeline

### 1. Foundation Data (.tbl/.tbm → .tres)
**Purpose**: Establish core game data definitions following the "Global Litmus Test" principle
**Process**:
- Parse custom TBL format with modular TBM support
- Convert to Godot Resource properties using data-driven design
- Organize in hybrid directory structure with feature-based co-location and global assets in `/assets/`
- Maintain cross-references between related entities using Godot's resource system

**Output**: Data-driven resources organized according to the hybrid model:
- ShipClass definitions co-located with ship entities in `/features/fighters/{faction}_{ship_name}/`
- WeaponClass specifications co-located with weapon entities in `/features/weapons/{weapon_name}/`
- AI profiles with tactical behaviors in `/assets/data/ai/profiles/` (passes Global Litmus Test)
- Species and IFF relationship definitions in `/assets/data/species/` and `/assets/data/iff/` (passes Global Litmus Test)
- Armor type damage modifiers in `/assets/data/armor/` (passes Global Litmus Test)
- Effect system parameters co-located with effect entities in `/features/effects/{effect_name}/`

### 2. Visual Assets (POF/PCX/DDS → glTF/WebP)
**Purpose**: Convert 3D models and textures to modern formats following feature-based organization
**Process**:
- Parse POF geometry and convert to glTF 2.0 preserving model hierarchy
- Extract hardpoint and subsystem metadata for gameplay systems
- Convert PCX/DDS paletted/images to RGB/RGBA with transparency
- Generate optimized textures with mipmaps for performance
- Create sprite sheets for animations with timing data

**Output**: Media assets organized according to feature-based principles:
- 3D models (.glb) co-located with entity scenes in `/features/{category}/{entity_name}/`
- Textures (.webp) optimized for use in feature directories and `/assets/textures/` for shared assets
- Sprite sheets with animation data in `/assets/animations/` for globally shared animations

### 3. Audio Assets (WAV/OGG → Ogg Vorbis)
**Purpose**: Convert sound effects and music to efficient format following the hybrid model
**Process**:
- Convert WAV files to Ogg Vorbis with appropriate settings for platform compatibility
- Standardize sample rates and bit depths for consistent audio quality
- Preserve loop points and 3D positioning data for spatial audio
- Organize by content type and usage context following the Global Litmus Test

**Output**: Audio files (.ogg) organized according to the hybrid model:
- Feature-specific sounds co-located in `/features/{category}/{entity_name}/assets/sounds/`
- Shared audio assets in `/assets/audio/` directories for assets that pass the Global Litmus Test
- UI sounds in `/assets/audio/sfx/ui/` (passes Global Litmus Test)
- Generic SFX in `/assets/audio/sfx/` (passes Global Litmus Test)
- Music tracks in `/assets/audio/music/` (passes Global Litmus Test)

### 4. Animation Assets (ANI → Sprite Sheets/Animation Resources)
**Purpose**: Convert sprite-based animations to efficient format following feature-based organization
**Process**:
- Extract animation frame sequences from ANI files preserving timing data
- Generate optimized sprite sheet textures with efficient packing
- Create Godot Animation resources with frame timing and sequence information
- Organize by animation type and usage context following the hybrid model

**Output**: Animation resources organized according to the hybrid model:
- Feature-specific animations co-located in `/features/{category}/{entity_name}/` directories
- Shared animations in `/assets/animations/` for assets that pass the Global Litmus Test
- UI animations in `/assets/animations/ui/` (passes Global Litmus Test)
- Effect animations in `/assets/animations/effects/` (passes Global Litmus Test)

### 5. Text Assets (TXT → BBCode)
**Purpose**: Convert narrative and technical text to displayable format following campaign-centric organization
**Process**:
- Parse custom formatting codes in TXT files preserving narrative structure
- Convert to BBCode for Godot RichTextLabel compatibility with formatting preservation
- Structure content for navigation and search with metadata generation
- Organize by campaign and mission following campaign-centric principles

**Output**: Text resources organized according to campaign-centric principles:
- Mission fiction co-located with missions in `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/`
- Technical database entries in `/features/ui/tech_database/`
- Interface text in feature directories
- Campaign text in `/campaigns/{campaign}/` directories

### 6. Mission Integration (FS2/FC2 → Godot Scenes/Resources)
**Purpose**: Assemble all converted assets into playable missions following campaign-centric organization
**Process**:
- Parse binary FS2 mission format extracting briefing, placement, and event data
- Parse FC2 campaign files for mission sequencing and progression data
- Generate Godot scenes with entity references using instance() calls
- Create event timeline using Godot's animation system with timeline sequences
- Link to all converted data and media assets through exported variables

**Output**: Complete mission scenes organized according to campaign-centric principles:
- Mission scenes with integrated entity instances in `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/`
- Campaign definitions in `/campaigns/{campaign}/campaign.tres`
- Event timelines with gameplay logic using Godot's AnimationPlayer
- Objective tracking and message systems with persistent data

## Filetype Conversion Requirements Specification

### TBL/TBM Files (.tbl/.tbm → .tres)

#### Technical Requirements
- **Format Parsing**: Custom table parser for WCS TBL format with modular TBM support
- **Data Mapping**: Convert legacy data structures to Godot Resource properties with type safety
- **Merge Processing**: Handle TBM override files with base TBL data using inheritance
- **Validation**: Ensure data integrity and range constraints with error reporting
- **Cross-References**: Maintain links between related table entries through ResourceLoader

#### Quality Standards
- **Data Accuracy**: Preserve all gameplay-relevant values with precision
- **Consistency**: Maintain consistent property naming conventions following snake_case
- **Documentation**: Include comments for complex data relationships with clear descriptions
- **Validation**: Implement range checking for numerical values with boundary tests
- **Error Handling**: Graceful degradation for invalid data with fallback values

#### Target Format Specifications
- **File Extension**: .tres (Godot Resource) for data-driven design
- **Encoding**: UTF-8 for cross-platform compatibility
- **Structure**: Godot's native resource serialization with human-readable sections
- **Compression**: Text sections remain human-readable for version control
- **Size Limits**: No hard limit, but recommended < 100MB for performance

#### Integration Points
- **Entity Scenes**: `/features/` directories reference data resources through exported variables
- **Mission Scenes**: `/campaigns/` reference entity and data resources via instance() calls
- **System Components**: Reference configuration resources in `/assets/data/` 
- **UI Components**: Reference display data resources through theme properties

#### Directory Organization
Following the hybrid model and Global Litmus Test:
- **Ship Data**: Co-located in `/features/fighters/{faction}_{ship_name}/{ship_name}.tres`
- **Weapon Data**: Co-located in `/features/weapons/{weapon_name}/{weapon_name}.tres`
- **AI Profiles**: `/assets/data/ai/profiles/{profile_name}.tres` (passes Global Litmus Test)
- **Species Data**: `/assets/data/species/{species_name}.tres` (passes Global Litmus Test)
- **IFF Data**: `/assets/data/iff/{iff_name}.tres` (passes Global Litmus Test)
- **Armor Data**: `/assets/data/armor/{armor_type}.tres` (passes Global Litmus Test)
- **Effect Data**: Co-located in `/features/effects/{effect_name}/{effect_name}.tres`

### FS2/FC2 Files (.fs2/.fc2 → .tscn/.tres)

#### Technical Requirements
- **Binary Parsing**: Custom FS2 format parser with mission data extraction
- **Campaign Parsing**: Custom FC2 format parser with sequencing data extraction
- **Event Translation**: Convert sexp logic to Godot animation system with timeline sequences
- **Entity Placement**: Parse initial ship positions and orientations with precision
- **Script Integration**: Map mission events to Godot timeline with AnimationPlayer
- **Cross-Reference Resolution**: Link to converted table and model data through ResourceLoader

#### Quality Standards
- **Event Fidelity**: Preserve all mission event logic with accurate translation
- **Placement Accuracy**: Maintain precise entity positioning with coordinate systems
- **Timing Consistency**: Preserve mission pacing and flow with frame-accurate timing
- **Objective Tracking**: Accurate primary/secondary objective handling with state management
- **Message System**: Complete communication event preservation with dialogue systems

#### Target Format Specifications
- **Scene Files**: .tscn (Godot Scene) for mission composition
- **Data Files**: .tres (Godot Resource) for mission configuration
- **Timeline System**: Godot's AnimationPlayer for event sequencing with keyframes
- **Entity References**: Resource paths to converted entities with instance() calls
- **Event Structure**: Hierarchical event organization with nested timelines

#### Integration Points
- **Entity Library**: Reference converted entities from `/features/` via instance() calls
- **Data Resources**: Link to entity data co-located in `/features/` through exported variables
- **Text Resources**: Connect to fiction in campaign directories with file references
- **Audio Resources**: Integrate sounds from `/assets/audio/` with AudioStreamPlayer nodes

#### Directory Organization
Following campaign-centric organization principles:
- **Campaign Definitions**: `/campaigns/{campaign}/campaign.tres`
- **Mission Scenes**: `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/mission.tscn`
- **Mission Data**: `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/mission_data.tres`
- **Briefing Text**: `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/briefing.txt`
- **Fiction Text**: `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/fiction.txt`

### POF Files (.pof → .glb/.gltf)

#### Technical Requirements
- **Geometry Conversion**: BSP tree to mesh conversion preserving polygon accuracy
- **Texture Mapping**: UV coordinate preservation with material assignment
- **Hardpoint Extraction**: Weapon/attachment point metadata with coordinate systems
- **LOD Processing**: Multiple detail level generation with vertex reduction
- **Animation Support**: Subobject hierarchy preservation with bone structures

#### Quality Standards
- **Visual Fidelity**: Accurate polygon representation with normal preservation
- **Texture Accuracy**: Proper UV mapping and material assignment with PBR support
- **Hardpoint Precision**: Exact weapon/emitter positioning with attachment points
- **LOD Consistency**: Seamless detail level transitions with distance-based switching
- **Metadata Preservation**: Gameplay-relevant information retention with custom properties

#### Target Format Specifications
- **Primary Format**: .glb (glTF Binary) for single-file distribution
- **Alternative Format**: .gltf (glTF JSON) for editable workflows
- **Compatibility**: glTF 2.0 specification compliance with extension support
- **Embedded Data**: Textures and metadata in single file with binary buffers
- **Size Optimization**: Efficient vertex and index storage with compression

#### Integration Points
- **Entity Models**: Direct use in `/features/` scenes with MeshInstance3D nodes
- **Hardpoint Systems**: Weapon mounting in ship entities with attachment points
- **Subsystem Damage**: Hit detection in gameplay systems with subobject metadata
- **Visual Effects**: Attachment points for engine/weapon effects with empty nodes

#### Directory Organization
Following feature-based co-location:
- **Entity Models**: Co-located in `/features/{category}/{entity_name}/{entity_name}.glb`
- **Shared Models**: In feature category `_shared` directories for semi-global assets
- **Template Models**: In `/features/{category}/templates/` for reusable components

### PCX/DDS Files (.pcx/.dds → WebP/PNG)

#### Technical Requirements
- **Palette Conversion**: 256-color to RGB/RGBA conversion with color accuracy
- **Transparency Handling**: Color key to alpha channel with clean edges
- **Mipmap Generation**: Automatic LOD texture creation with proper filtering
- **Compression Optimization**: Format-specific quality settings with size balancing
- **Resolution Scaling**: Power-of-2 dimension adjustment with aspect ratio preservation

#### Quality Standards
- **Color Accuracy**: Faithful palette reproduction with gamma correction
- **Transparency Clarity**: Clean alpha channel edges with anti-aliasing
- **Compression Balance**: Quality vs. file size optimization with visual testing
- **Mipmap Quality**: Proper filtering for different LODs with distance accuracy
- **Format Appropriateness**: WebP for textures, PNG for UI with appropriate codecs

#### Target Format Specifications
- **Textures**: WebP (lossy compression) for optimal performance/quality ratio
- **UI Graphics**: PNG (lossless compression) for crisp interface elements
- **Color Depth**: 24-bit RGB + 8-bit alpha with sRGB color space
- **Dimensions**: Power-of-2 for optimal GPU usage with hardware compatibility
- **Metadata**: Embedded color profile information with texture settings

#### Integration Points
- **3D Models**: Material textures in entity models with StandardMaterial3D
- **UI Elements**: Interface graphics in `/features/ui/` scenes with TextureRect
- **Particle Systems**: Effect textures in animations with ParticleProcessMaterial
- **Fonts**: Character set graphics for text rendering with DynamicFont

#### Directory Organization
Following the hybrid model:
- **Feature Textures**: Co-located in `/features/{category}/{entity_name}/` directories
- **Shared Textures**: In `/assets/textures/` for assets passing Global Litmus Test
- **UI Textures**: In `/assets/textures/ui/` (passes Global Litmus Test)
- **Effect Textures**: In `/assets/textures/effects/` (passes Global Litmus Test)

### WAV/OGG Files (.wav/.ogg → Ogg Vorbis)

#### Technical Requirements
- **Format Conversion**: WAV to Ogg Vorbis encoding with quality preservation
- **Sample Rate Adjustment**: Standardization to target rates with resampling
- **Channel Management**: Mono/stereo preservation with channel mapping
- **Loop Point Preservation**: Seamless playback markers with loop metadata
- **3D Positioning Data**: Spatial audio metadata with distance parameters

#### Quality Standards
- **Audio Fidelity**: Minimal quality loss in conversion with bit-perfect processing
- **Consistent Levels**: Normalized volume across asset types with RMS matching
- **Loop Seamlessness**: Invisible transition points with crossfading
- **Spatial Accuracy**: Proper 3D positioning characteristics with HRTF support
- **Format Compatibility**: Broad codec support with fallback options

#### Target Format Specifications
- **Container**: Ogg container format with Vorbis codec for compression
- **Codec**: Vorbis audio codec with variable bit rate encoding
- **Bit Rate**: Variable based on content type with quality presets
- **Sample Rates**: 22.05kHz (voice), 44.1kHz (SFX/music) with appropriate settings
- **Metadata**: Embedded loop and positioning information with custom tags

#### Integration Points
- **Entity Audio**: Engine/weapon sounds in entity scenes with AudioStreamPlayer3D
- **UI Feedback**: Interface sounds in `/features/ui/` components with AudioStreamPlayer
- **Mission Audio**: Voice acting and ambient sounds with 3D positioning
- **Effect Systems**: Impact and environmental audio with spatial effects

#### Directory Organization
Following the hybrid model and Global Litmus Test:
- **Feature Sounds**: Co-located in `/features/{category}/{entity_name}/assets/sounds/`
- **Shared Audio**: In `/assets/audio/` directories for assets passing Global Litmus Test
- **UI Sounds**: In `/assets/audio/sfx/ui/` (passes Global Litmus Test)
- **SFX**: In `/assets/audio/sfx/` (passes Global Litmus Test)
- **Music**: In `/assets/audio/music/` (passes Global Litmus Test)

### ANI Files (.ani → Sprite Sheets/Animation Resources)

#### Technical Requirements
- **Frame Extraction**: Individual animation frame parsing with timing preservation
- **Sprite Atlas Creation**: Efficient texture packing with minimal waste
- **Timing Data**: Frame duration and sequence information with keyframe timing
- **Playback Control**: Loop and transition properties with animation states
- **Effect Integration**: Particle and visual effect data with emitter parameters

#### Quality Standards
- **Frame Accuracy**: Precise animation sequence preservation with no frame loss
- **Atlas Efficiency**: Minimal texture space waste with optimal packing
- **Timing Precision**: Accurate frame rate reproduction with vsync compatibility
- **Playback Smoothness**: Seamless animation transitions with interpolation
- **Effect Quality**: Proper visual effect implementation with particle systems

#### Target Format Specifications
- **Texture Format**: PNG sprite sheets for lossless quality with alpha support
- **Animation Data**: Godot Animation resources with keyframe interpolation
- **Metadata**: Frame timing and sequence information with custom properties
- **Compression**: Lossless for UI, appropriate for effects with quality settings
- **Organization**: Atlas with coordinate mapping for efficient rendering

#### Integration Points
- **Visual Effects**: Particle and impact effects with GPU particles
- **UI Animation**: Interface element animations in `/features/ui/` with AnimationPlayer
- **Entity Effects**: Ship/engine visual feedback with sprite animations
- **Weapon Effects**: Firing and impact animations with effect systems

#### Directory Organization
Following the hybrid model:
- **Feature Animations**: Co-located in `/features/{category}/{entity_name}/` directories
- **Shared Animations**: In `/assets/animations/` for assets passing Global Litmus Test
- **UI Animations**: In `/assets/animations/ui/` (passes Global Litmus Test)
- **Effect Animations**: In `/assets/animations/effects/` (passes Global Litmus Test)

### TXT Files (.txt → BBCode Text)

#### Technical Requirements
- **Markup Parsing**: Custom formatting code interpretation with tag mapping
- **Text Conversion**: Legacy codes to BBCode with formatting preservation
- **Structure Preservation**: Paragraph and section organization with hierarchy
- **Cross-Reference Handling**: Link and navigation support with internal anchors
- **Metadata Generation**: Search and categorization data with indexing tags

#### Quality Standards
- **Content Accuracy**: Exact text preservation with character encoding
- **Formatting Consistency**: Proper BBCode implementation with style mapping
- **Navigation Support**: Clear section boundaries with heading structure
- **Searchability**: Proper metadata for indexing with keyword extraction
- **Presentation Quality**: Readable and well-formatted with responsive layout

#### Target Format Specifications
- **Format**: Plain text with BBCode markup for rich text display
- **Encoding**: UTF-8 for international character support
- **Structure**: Section and paragraph organization with semantic markup
- **Metadata**: Embedded categorization tags for search and filtering
- **Size Limits**: No hard limits, but recommended < 1MB per file for performance

#### Integration Points
- **Briefing Screens**: Mission introduction text in `/features/ui/briefing/` with RichTextLabel
- **Tech Database**: Ship/weapon specification display in `/features/ui/tech_database/` with navigation
- **Fiction Reader**: Narrative content presentation with scrolling views
- **UI Text**: Interface labels and descriptions in `/features/ui/` with localization

#### Directory Organization
Following campaign-centric and feature-based organization:
- **Mission Fiction**: Co-located in `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/fiction.txt`
- **Briefing Text**: Co-located in `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/briefing.txt`
- **Technical Entries**: In `/features/ui/tech_database/` with entity references
- **Campaign Text**: In `/campaigns/{campaign}/` directories with progression data

## Hybrid Directory Structure

All converted assets follow Godot's hybrid organizational model combining feature-based co-location with global asset management:

### Core Organization
```
wcsaga_godot/
├── addons/                # Third-party plugins and extensions (managed by Godot)
├── assets/                # Global asset library (truly shared assets passing Global Litmus Test)
├── autoload/              # Singleton scripts (auto-loaded following Global State principle)
├── campaigns/             # Campaign data and mission scenes (campaign-centric organization)
├── features/              # Self-contained game features with co-located data (feature-based)
├── scripts/               # Reusable GDScript code and custom resources (abstract logic only)
├── project.godot          # Godot project file
└── README.md             # Project README
```

### Assets Directory Structure
Following the "Global Litmus Test" principle for truly shared assets:
```
/assets/                  # Global asset library (truly shared assets)
├── audio/                # Shared audio files (assets needed even if 3 random features deleted)
│   ├── sfx/              # Generic sound effects
│   │   ├── weapons/      # Weapon sound effects
│   │   ├── explosions/   # Explosion sound effects
│   │   ├── environment/  # Environmental sound effects
│   │   └── ui/           # UI sound effects (passes Global Litmus Test)
│   ├── music/            # Background music tracks (passes Global Litmus Test)
│   └── voice/            # Voice acting files (passes Global Litmus Test)
├── behavior_trees/       # Shared LimboAI behavior trees (passes Global Litmus Test)
│   ├── ai/               # AI behavior trees
│   └── mission/          # Mission-specific behavior trees
├── data/                 # Shared data resources (passes Global Litmus Test)
│   ├── ai/               # AI data resources
│   │   └── profiles/     # AI profile definitions
│   ├── species/          # Species data resources (passes Global Litmus Test)
│   ├── iff/              # IFF data resources (passes Global Litmus Test)
│   ├── armor/            # Armor type data (passes Global Litmus Test)
│   └── mission/          # Mission data resources
├── textures/             # Shared texture files (assets needed even if 3 random features deleted)
│   ├── ui/               # Generic UI elements (passes Global Litmus Test)
│   ├── effects/          # Particle textures used by multiple effects (passes Global Litmus Test)
│   └── fonts/            # Font textures (passes Global Litmus Test)
└── animations/           # Shared animation files (assets needed even if 3 random features deleted)
    ├── ui/               # UI animations (passes Global Litmus Test)
    └── effects/          # Generic effect animations (passes Global Litmus Test)
```

### Autoload Directory Structure
Following the "Is this state or service truly global and required everywhere?" principle:
```
/autoload/                # Singleton scripts (auto-loaded)
├── game_state.gd         # Current game state (truly global)
├── event_bus.gd          # Global event system (truly global)
├── resource_loader.gd    # Resource loading utilities (truly global)
├── audio_manager.gd      # Audio management (truly global)
└── save_manager.gd       # Save/load system (truly global)
```

### Features Directory Structure
Following feature-based organization with co-location principle:
```
/features/                # Self-contained game features organized by category
├── fighters/             # Fighter ship entities (primary player and AI ships)
│   ├── confed_rapier/    # Raptor fighter - all files together
│   │   ├── rapier.tscn   # Scene file
│   │   ├── rapier.gd     # Script file
│   │   ├── rapier.tres   # Ship data resource
│   │   ├── rapier.glb    # 3D model
│   │   ├── assets/       # Feature-specific assets
│   │   │   ├── textures/ # Textures specific to this fighter
│   │   │   └── sounds/   # Sounds specific to this fighter
│   │   └── rapier_icon.png # UI icon
│   ├── _shared/          # Shared fighter assets
│   │   ├── cockpits/     # Shared cockpit models
│   │   └── effects/      # Shared fighter effects
│   └── templates/        # Fighter templates
├── weapons/              # Weapon entities (self-contained)
│   ├── laser_cannon/     # Laser cannon
│   │   ├── laser_cannon.tscn   # Scene
│   │   ├── laser_cannon.gd     # Script
│   │   ├── laser_cannon.tres   # Weapon data
│   │   ├── assets/       # Feature-specific assets
│   │   │   ├── textures/ # Textures specific to this weapon
│   │   │   └── sounds/   # Sounds specific to this weapon
│   │   └── laser_cannon_icon.png # UI icon
│   ├── _shared/          # Shared weapon assets
│   │   ├── muzzle_flashes/ # Shared muzzle flash effects
│   │   └── impact_effects/ # Shared impact effects
│   └── templates/        # Weapon templates
├── effects/              # Effect entities
│   ├── explosion/        # Explosion effect
│   │   ├── explosion.tscn      # Scene file
│   │   ├── explosion.gd        # Script file
│   │   ├── explosion.tres      # Effect data resource
│   │   ├── assets/       # Feature-specific assets
│   │   │   ├── textures/ # Textures specific to this effect
│   │   │   └── sounds/   # Sounds specific to this effect
│   │   └── explosion_icon.png  # UI icon
│   ├── _shared/          # Shared effect assets
│   │   ├── particle_textures/  # Shared particle effects
│   │   └── shader_effects/     # Shared shader effects
│   └── templates/        # Effect templates
├── ui/                   # UI feature elements
│   ├── main_menu/        # Main menu interface
│   │   ├── main_menu.tscn      # Scene file
│   │   ├── main_menu.gd        # Script file
│   │   ├── assets/       # Feature-specific assets
│   │   │   ├── textures/ # Textures specific to this UI
│   │   │   ├── sounds/   # Sounds specific to this UI
│   │   │   └── fonts/    # Fonts specific to this UI
│   │   └── main_menu_icon.png  # UI icon
│   ├── _shared/          # Shared UI assets
│   │   ├── fonts/        # UI fonts (passes Global Litmus Test)
│   │   ├── icons/        # UI icons
│   │   ├── themes/       # UI themes
│   │   └── components/   # Reusable UI components
│   └── templates/        # UI templates
└── templates/            # Feature templates
```

### Campaigns Directory Structure
Following campaign-centric mission organization:
```
/campaigns/               # Campaign data and mission scenes
├── hermes/               # Hermes campaign (self-contained)
│   ├── campaign.tres     # Campaign definition
│   ├── progression.tres  # Campaign progression data
│   ├── pilot_data.tres   # Pilot progression data
│   └── missions/         # Mission scenes with integrated data
│       ├── m01_hermes/   # Mission 1 - all files together
│       │   ├── mission.tscn      # Main mission scene
│       │   ├── mission_data.tres # Mission configuration
│       │   ├── briefing.txt      # Briefing text
│       │   ├── fiction.txt       # Fiction text
│       │   └── objectives.tres   # Mission objectives
│       └── templates/    # Mission templates
└── templates/            # Campaign templates
```

### Scripts Directory Structure
Following separation of concerns principle (no instantiable game objects):
```
/scripts/                 # Reusable GDScript code and custom resources
├── entities/             # Base entity scripts
│   ├── base_fighter.gd   # Base fighter controller
│   └── base_weapon.gd    # Base weapon controller
├── ai/                   # AI behavior scripts
│   ├── ai_behavior.gd    # Base AI behavior class
│   └── combat_tactics.gd # Combat behavior logic
├── mission/              # Mission system scripts
│   ├── mission_manager.gd # Mission orchestration
│   └── event_system.gd   # Mission event handling
└── utilities/            # Utility functions and helpers
    ├── resource_loader.gd # Resource loading utilities
    └── object_pool.gd    # Generic object pooling system
```

## Asset Relationships and Dependencies

### Primary Relationships Following Hybrid Model
- **Ships**: Connect .pof models, .tbl properties, .pcx/.dds textures, and .wav/.ogg sounds all co-located in `/features/fighters/{faction}_{ship_name}/` with shared assets in `/features/fighters/_shared/` and global assets in `/assets/` that pass the Global Litmus Test
- **Weapons**: Connect .pof models, .tbl properties, .ani effects, and .wav/.ogg sounds all co-located in `/features/weapons/{weapon_name}/` with shared assets in `/features/weapons/_shared/` and global assets in `/assets/` that pass the Global Litmus Test
- **Missions**: Reference entity data co-located in `/features/`, .fs2/.fc2 scripting in `/campaigns/{campaign}/missions/`, and .txt fiction co-located with missions following campaign-centric organization
- **Effects**: Combine .ani animations, .pcx/.dds textures, and .wav/.ogg sounds all co-located in `/features/effects/{effect_name}/` with shared assets in `/features/effects/_shared/` and global assets in `/assets/` that pass the Global Litmus Test
- **UI**: Use .pcx/.dds graphics in `/assets/textures/ui/` (passes Global Litmus Test), .ani animations in `/assets/animations/ui/` (passes Global Litmus Test), and .txt content co-located with UI features

### Conversion Pipeline Dependencies Following Hybrid Model
1. **Data Files** (.tbl/.tbm) - Foundation data definitions co-located in `/features/` directories with global data in `/assets/data/` (passes Global Litmus Test)
2. **Texture Files** (.pcx/.dds) - Visual assets for models co-located in feature directories with shared textures in `/assets/textures/` (passes Global Litmus Test)
3. **Model Files** (.pof) - 3D geometry with texture references co-located in `/features/` directories with shared models in feature `_shared` directories
4. **Audio Files** (.wav/.ogg) - Sound assets co-located in feature directories with shared audio in `/assets/audio/` (passes Global Litmus Test)
5. **Animation Files** (.ani) - Animated visual effects co-located in feature directories with shared animations in `/assets/animations/` (passes Global Litmus Test)
6. **Text Files** (.txt) - Narrative and documentation content co-located with features or campaigns following campaign-centric organization
7. **Mission Files** (.fs2/.fc2) - Integration of all assets into gameplay co-located in `/campaigns/` directories following campaign-centric organization

## Technical File Format Standards

### Godot Resource Files (.tres)
**Specifications**:
- UTF-8 encoding for text sections with cross-platform compatibility
- Godot's native resource serialization format with version control support
- Support for custom resource types with inheritance
- Cross-platform compatibility with consistent behavior
- Version control friendly with human-readable text sections

**Size Limits**:
- Individual files: No hard limit, but recommended < 100MB for performance
- Resource properties: Limited by available memory with graceful degradation
- String properties: Limited by available memory with streaming support

### glTF 2.0 Files (.glb/.gltf)
**Specifications**:
- Compliance with glTF 2.0 specification with extension support
- Embedded or external texture support with efficient compression
- PBR material definitions with metallic/roughness workflow
- Node hierarchy preservation with transform accuracy
- Animation channel support with keyframe interpolation

**Model Restrictions**:
- Vertex count: Limited by GPU capabilities (recommended < 1M vertices per mesh)
- Texture size: Maximum 8192x8192 pixels with hardware compatibility
- Bone count: Maximum 256 bones per skeleton with skinning support
- Mesh count: Limited by scene complexity with batching optimization

### Image Files (WebP/PNG)
**WebP Textures**:
- Lossy compression for optimal size/performance with quality settings
- Quality setting: 80-95 for most textures with visual testing
- Mipmap generation for all textures with proper filtering
- Color space: sRGB for diffuse textures with gamma correction
- Alpha channel support for transparency with premultiplied alpha

**PNG UI Graphics**:
- Lossless compression for perfect quality with file size consideration
- Indexed color for simple graphics (256 colors) with palette optimization
- Direct color for complex graphics (24-bit RGB + 8-bit alpha) with full range
- Interlacing disabled for faster loading with progressive rendering

**Size Recommendations**:
- UI elements: Powers of 2 dimensions (32, 64, 128, etc.) with aspect ratios
- Textures: Powers of 2 dimensions, maximum 8192x8192 with hardware limits
- Sprite sheets: Efficient packing with minimal waste and atlas optimization

### Audio Files (Ogg Vorbis)
**Specifications**:
- Ogg Vorbis container format with Vorbis codec for compression
- Vorbis audio codec with variable bit rate encoding for quality
- Variable bit rate encoding with adaptive compression
- Support for 3D positioning metadata with spatial audio
- Loop point specification with seamless transitions

**Quality Settings**:
- Sound effects: 44.1kHz sample rate, 96-128 kbps with transient preservation
- Music: 44.1kHz sample rate, 128-192 kbps with harmonic accuracy
- Voice: 22.05kHz sample rate, 64-96 kbps with speech clarity
- Ambient: 44.1kHz sample rate, 64-128 kbps with atmospheric quality

### Animation Data
**Sprite Sheet Specifications**:
- Power-of-2 dimensions for optimal GPU usage with texture memory
- Efficient frame packing with minimal waste and atlas optimization
- Consistent frame sizes where possible with padding
- Metadata for frame timing and sequences with keyframe data
- Alpha channel support for transparency with edge smoothing

**Animation Resource Format**:
- Godot's native Animation resource format with keyframe interpolation
- Support for property animations with easing functions
- Timeline-based keyframe system with hierarchical tracks
- Loop and playback control properties with state management
- Cross-reference to target nodes with path resolution

## Entity Asset Organization Standards

### Self-Contained Entity Structure Following Feature-Based Principles
Each entity in `/features/` follows these standards:
- Self-contained directory with all related assets following co-location principle
- Related assets grouped together in the same directory with clear hierarchy
- Shared assets placed in common directories with explicit cross-references
- Cross-references maintained through Godot's resource system with exported variables
- Directory structure reflecting gameplay relationships with semantic naming

### Example Entity Organization Following Hybrid Model
```
/features/fighters/confed_rapier/  # Fighter entity directory
├── rapier.tscn                   # Scene file
├── rapier.gd                     # Script file
├── rapier.tres                   # Entity data resource
├── rapier.glb                    # 3D model
├── assets/                       # Feature-specific assets
│   ├── textures/                 # Textures specific to this fighter
│   │   ├── rapier_albedo.webp    # Albedo texture
│   │   ├── rapier_normal.webp    # Normal map
│   │   └── rapier_emission.webp  # Emission map
│   └── sounds/                   # Sounds specific to this fighter
│       ├── engine_loop.ogg       # Engine sound
│       └── afterburner.ogg       # Afterburner sound
└── rapier_icon.png               # UI icon for menus
```

### Shared Asset Organization Following Hybrid Model
```
/features/fighters/_shared/                # Shared fighter assets
├── cockpits/                              # Shared cockpit models
│   ├── standard_cockpit.glb               # Standard cockpit model
│   └── standard_cockpit_material.tres     # Standard cockpit material
└── effects/                               # Shared fighter effects
    ├── engine_trail.png                   # Engine trail texture
    └── shield_effect.png                  # Shield visualization

/assets/audio/sfx/weapons/common/          # Shared weapon sounds (passes Global Litmus Test)
├── laser_fire_01.ogg                      # Common laser firing sound
├── missile_launch_01.ogg                  # Common missile launch sound
└── weapon_reload_01.ogg                   # Common weapon reload sound
```

## Quality Assurance and Validation

### Technical Validation Following Hybrid Model
- **Format Compliance**: Verify converted assets match Godot format specifications with validation tools
- **Cross-Reference Integrity**: Ensure all resource references resolve correctly with ResourceLoader
- **Performance Benchmarks**: Validate asset sizes and loading times with profiling tools
- **Platform Compatibility**: Test assets on target platforms with hardware variation

### Gameplay Validation Following Feature-Based Principles
- **Entity Behavior**: Verify entity scenes function with converted data through gameplay testing
- **Mission Flow**: Test mission scenes with integrated assets using mission flow validation
- **Audio-Visual Sync**: Confirm audio and visual effects align properly with timing tests
- **Balance and Progression**: Validate gameplay balance with converted data through playtesting

## Future Extensibility Following Hybrid Model

### Format Evolution
- **Backward Compatibility**: Maintain with existing assets through version migration
- **Migration Paths**: Clear paths for format updates with automated tools
- **Extension Mechanisms**: Available for new features with modular design
- **Deprecation Policies**: Established for legacy formats with graceful degradation
- **Documentation**: Comprehensive documentation of all format changes with version tracking

### Tool Integration
- **Third-Party Support**: Import pipelines for industry standard formats with plugin architecture
- **Export Capabilities**: For modding community with open formats
- **Plugin Architecture**: For custom workflows with extension points
- **Scriptable Pipelines**: Asset processing automation with batch processing

This consolidated specification ensures consistent and high-quality conversion of all asset types while maintaining the relationships and functionality essential to the Wing Commander Saga gameplay experience, following Godot's best practices for the hybrid organizational model that combines feature-based co-location with global asset management.