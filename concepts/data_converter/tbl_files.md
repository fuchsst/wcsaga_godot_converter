# TBL Files Conversion Requirements

## Overview
TBL (Table) files contain structured data definitions for various game elements in Wing Commander Saga. These files need to be converted to Godot's resource format (.tres) to maintain the data-driven design approach, following Godot's feature-based organization principles and the hybrid model defined in our project structure.

The TBL files found in the source assets include:
- `ships.tbl` - Ship class definitions with physics, weapons, and visual properties
- `weapons.tbl` - Weapon definitions with damage, firing rates, and effects
- `ai_profiles.tbl` - AI behavior profiles with difficulty scaling parameters
- `Species_defs.tbl` - Species definitions with thruster animations and debris behavior
- `iff_defs.tbl` - IFF (Identification Friend or Foe) relationship definitions
- `fireball.tbl` - Fireball/explosion effect definitions
- `weapon_expl.tbl` - Weapon impact explosion definitions
- `medals.tbl` - Medal definitions with visual representations
- `rank.tbl` - Military rank definitions with promotion requirements
- `sounds.tbl` - Sound effect definitions with file references
- `music.tbl` - Music track definitions for campaign events
- `cutscenes.tbl` - Cutscene definitions with audio file references

## File Types and Conversion Requirements

### Ship Definitions (ships.tbl)
**Purpose**: Defines all playable and AI ship classes with their properties
**Source Format**: Custom TBL format with sections for each ship class
**Target Format**: ShipClass resources (.tres)
**Conversion Requirements**:
- Parse ship names, descriptions, and classifications
- Extract physics properties (mass, max velocity, acceleration)
- Convert weapon hardpoints and subsystem locations
- Map damage characteristics and armor values
- Preserve IFF (Identification Friend or Foe) settings
- Maintain 3D model references for later POF conversion
- Handle modular TBM overrides
- Map to `/assets/data/ships/{ship_name}.tres` following the Global Litmus Test

### Weapon Definitions (weapons.tbl)
**Purpose**: Defines all weapon types with their characteristics
**Source Format**: Custom TBL format with weapon sections
**Target Format**: WeaponClass resources (.tres)
**Conversion Requirements**:
- Parse weapon names, descriptions, and types (laser, missile, etc.)
- Extract damage values, fire rates, and ranges
- Convert homing characteristics for missiles
- Map special effects (EMP, electronics, spawn weapons)
- Preserve 3D model references for later POF conversion
- Handle beam weapon properties (duration, width)
- Maintain audio references for firing/impact sounds
- Map to `/assets/data/weapons/{weapon_name}.tres` following the Global Litmus Test

### AI Profiles (ai_profiles.tbl)
**Purpose**: Defines AI behavior characteristics and difficulty settings
**Source Format**: Custom TBL format with AI profile sections
**Target Format**: AIProfile resources (.tres)
**Conversion Requirements**:
- Parse profile names and descriptions
- Extract behavior parameters (aggression, courage, accuracy)
- Convert tactical preferences (strafing, evasion patterns)
- Map weapon selection preferences
- Maintain difficulty scaling factors
- Map to `/assets/data/ai/profiles/{profile_name}.tres` following the Global Litmus Test
- Reference related assets in `/assets/audio/sfx/ai/` and `/assets/audio/voice/ai/`

### Species Definitions (species_defs.tbl)
**Purpose**: Defines alien species properties and characteristics
**Source Format**: Custom TBL format with species sections
**Target Format**: Species resources (.tres)
**Conversion Requirements**:
- Parse species names and descriptions
- Extract thruster animation references
- Convert debris behavior properties
- Map species-specific visual effects
- Maintain IFF relationship mappings
- Map to `/assets/data/species/{species_name}.tres` following the Global Litmus Test
- Reference related animations in `/assets/animations/effects/` and textures in `/assets/textures/effects/`

### IFF Definitions (iff_defs.tbl)
**Purpose**: Defines faction relationships and identification properties
**Source Format**: Custom TBL format with IFF sections
**Target Format**: IFF resources (.tres)
**Conversion Requirements**:
- Parse faction names and descriptions
- Extract color codes for radar/HUD display
- Convert relationship matrices (friendly, hostile, neutral)
- Map species affiliations
- Maintain team assignments
- Map to `/assets/data/iff/{iff_name}.tres` following the Global Litmus Test
- Reference related UI assets in `/assets/textures/ui/hud/radar/` and `/assets/textures/ui/hud/iff/`

### Fireball Effects (fireball.tbl)
**Purpose**: Defines fireball/explosion effect properties and behaviors
**Source Format**: Custom TBL format with effect sections
**Target Format**: Effect resources (.tres)
**Conversion Requirements**:
- Parse effect names and descriptions
- Extract effect properties (LOD settings)
- Map to visual assets for conversion
- Map to `/assets/data/effects/{effect_name}.tres` following the Global Litmus Test
- Reference related assets in `/features/effects/` for feature-specific implementations

### Weapon Impact Effects (weapon_expl.tbl)
**Purpose**: Defines weapon impact explosion effects
**Source Format**: Custom TBL format with explosion effect sections
**Target Format**: Effect resources (.tres)
**Conversion Requirements**:
- Parse effect names and descriptions
- Extract effect properties
- Map to visual assets for conversion
- Map to `/assets/data/effects/{effect_name}.tres` following the Global Litmus Test
- Reference related assets in `/features/weapons/_shared/impact_effects/` and `/features/effects/`

### Medals (medals.tbl)
**Purpose**: Defines military decoration and award definitions
**Source Format**: Custom TBL format with medal sections
**Target Format**: Medal resources (.tres)
**Conversion Requirements**:
- Parse medal names and descriptions
- Extract visual representation references (bitmap files)
- Map number of modifications/variations
- Map to `/assets/data/ui/medals/{medal_name}.tres` following the Global Litmus Test
- Reference related assets in `/features/ui/medals_display/assets/icons/`

### Ranks (rank.tbl)
**Purpose**: Defines military rank structure and progression
**Source Format**: Custom TBL format with rank sections
**Target Format**: Rank resources (.tres)
**Conversion Requirements**:
- Parse rank titles and abbreviations
- Extract rank insignia references (bitmap files)
- Map promotion requirements (points)
- Extract promotion voice references
- Map promotion text
- Map to `/assets/data/ui/ranks/{rank_name}.tres` following the Global Litmus Test
- Reference related assets in `/features/ui/rank_display/assets/insignia/`

### Sounds (sounds.tbl)
**Purpose**: Defines sound effect properties and file references
**Source Format**: Custom TBL format with sound entries
**Target Format**: Sound resources (.tres)
**Conversion Requirements**:
- Parse sound signatures and filenames
- Extract pre-loading flags
- Convert default volume settings
- Map 3D sound properties
- Extract attenuation distances for 3D sounds
- Map to `/assets/data/audio/sounds/{sound_name}.tres` following the Global Litmus Test
- Reference related audio assets in `/assets/audio/sfx/` organized by category

### Music (music.tbl)
**Purpose**: Defines music track properties for campaign events
**Source Format**: Custom TBL format with soundtrack entries
**Target Format**: Music resources (.tres)
**Conversion Requirements**:
- Parse soundtrack names and descriptions
- Extract music filenames
- Convert timing information (measures, samples per measure)
- Map to `/assets/data/audio/music/{music_name}.tres` following the Global Litmus Test
- Reference related audio assets in `/assets/audio/music/` organized by category

### Cutscenes (cutscenes.tbl)
**Purpose**: Defines cutscene properties and audio file references
**Source Format**: Custom TBL format with cutscene entries
**Target Format**: Cutscene resources (.tres)
**Conversion Requirements**:
- Parse cutscene filenames and names
- Extract cutscene descriptions
- Map CD location references
- Map to `/assets/data/cutscenes/{cutscene_name}.tres` following the Global Litmus Test
- Reference related audio assets in `/assets/audio/cutscenes/`

## Conversion Process

### 1. Parsing Phase
- Read TBL file line by line
- Identify section headers and data blocks
- Parse key-value pairs within sections
- Handle comments and special directives
- Validate data integrity
- Extract file references for asset conversion pipeline

### 2. Data Transformation Phase
- Map WCS data structures to Godot resource properties
- Convert units and coordinate systems where necessary
- Apply default values for missing data
- Resolve cross-references between table entries
- Handle modular TBM file overrides
- Map asset references to target directory structure

### 3. Resource Generation Phase
- Create Godot Resource objects for each table entry
- Serialize resources to .tres files
- Organize resources in directory structure following Godot conventions and the "Global Litmus Test"
- Generate metadata for relationship mapping
- Validate generated resources

## Directory Structure Alignment
Following the Godot project structure defined in directory_structure.md and the hybrid organizational model:

### Assets Directory Structure (Global Data)
Global data resources that follow the "Global Litmus Test" principle: "If I delete three random features, is this asset still needed?"

```
assets/
├── audio/                         # Shared audio files
│   ├── sfx/                       # Generic sound effects
│   │   ├── weapons/               # Weapon sound effects
│   │   ├── explosions/            # Explosion sound effects
│   │   ├── ui/                    # UI sound effects
│   │   ├── ai/                    # AI sound effects
│   │   └── environment/           # Environmental sound effects
│   ├── music/                     # Background music tracks
│   └── voice/                     # Voice acting files
│       ├── mission_briefings/     # Mission briefing voice files
│       ├── character_dialogue/    # Character dialogue files
│       └── ai/                    # AI voice files
├── behavior_trees/                # Shared LimboAI behavior trees
│   ├── ai/                        # AI behavior trees
│   │   ├── combat/                # Combat-related behavior trees
│   │   ├── navigation/            # Navigation behavior trees
│   │   └── tactical/              # Tactical behavior trees
│   └── mission/                   # Mission-specific behavior trees
├── data/                          # Shared data resources
│   ├── ai/                        # AI data resources
│   │   └── profiles/              # AI profile definitions
│   ├── ships/                     # Ship data resources
│   ├── weapons/                   # Weapon data resources
│   ├── species/                   # Species data resources
│   ├── iff/                       # IFF relationship data
│   ├── effects/                   # Effect data resources
│   ├── ui/                        # UI data resources
│   │   ├── medals/                # Medal definitions
│   │   └── ranks/                 # Rank definitions
│   ├── audio/                     # Audio data resources
│   │   ├── sounds/                # Sound definitions
│   │   └── music/                 # Music definitions
│   └── cutscenes/                 # Cutscene definitions
├── textures/                      # Shared texture files
│   ├── effects/                   # Particle textures used by multiple effects
│   ├── ui/                        # Generic UI elements
│   │   ├── hud/                   # HUD display elements
│   │   │   ├── radar/             # Radar display elements
│   │   │   └── iff/               # IFF-specific HUD elements
│   │   └── medals/                # Medal UI elements
│   └── fonts/                     # Font textures
└── animations/                    # Shared animation files
    ├── effects/                   # Generic effect animations
    │   ├── weapons/               # Weapon effect animations
    │   ├── explosions/            # Explosion animations
    │   └── thrusters/             # Thruster animations
    └── ui/                        # UI animations
```

## Integration Points

### Data Converter Output Mapping
- ShipClass resources → `/assets/data/ships/{ship_name}.tres`
- WeaponClass resources → `/assets/data/weapons/{weapon_name}.tres`
- AIProfile resources → `/assets/data/ai/profiles/{profile_name}.tres`
- Species resources → `/assets/data/species/{species_name}.tres`
- IFF resources → `/assets/data/iff/{iff_name}.tres`
- Effect resources → `/assets/data/effects/{effect_name}.tres`
- Medal resources → `/assets/data/ui/medals/{medal_name}.tres`
- Rank resources → `/assets/data/ui/ranks/{rank_name}.tres`
- Sound resources → `/assets/data/audio/sounds/{sound_name}.tres`
- Music resources → `/assets/data/audio/music/{music_name}.tres`
- Cutscene resources → `/assets/data/cutscenes/{cutscene_name}.tres`

### Resource References
- **Ship entities** in `/features/fighters/{faction}/{ship_name}/` reference ShipClass resources from `/assets/data/ships/`
- **Weapon entities** in `/features/weapons/{weapon_name}/` reference WeaponClass resources from `/assets/data/weapons/`
- **AI systems** in `/scripts/ai/` reference AIProfile resources from `/assets/data/ai/profiles/`
- **Mission scenes** in `/campaigns/{campaign}/missions/` reference data resources for entity instantiation
- **UI components** in `/features/ui/` reference data resources for display information
- **Effect systems** in `/features/effects/` reference Effect resources from `/assets/data/effects/`
- **Medal displays** in `/features/ui/medals_display/` reference Medal resources from `/assets/data/ui/medals/`
- **Rank displays** in `/features/ui/rank_display/` reference Rank resources from `/assets/data/ui/ranks/`

## Relationship to Other Assets

### Entity Integration
Converted TBL data integrates with entity scenes following the feature-based organization:
- ShipClass resources are referenced by ship entity scenes in `/features/fighters/{faction}/{ship_name}/`
- WeaponClass resources are referenced by weapon entity scenes in `/features/weapons/{weapon_name}/`
- AIProfile resources are referenced by AI behavior scripts in `/scripts/ai/`
- Effect resources are used by visual effect entities in `/features/effects/{effect_name}/`
- Medal resources are used by UI components in `/features/ui/medals_display/`
- Rank resources are used by UI components in `/features/ui/rank_display/`

### Common Shared Assets
- Cross-faction weapon definitions (shared between Terran and Kilrathi) in `/assets/data/weapons/`
- Standard particle effects used across multiple systems in `/assets/data/effects/`
- Shared IFF color definitions for radar display in `/assets/data/iff/`
- Universal AI behavior templates in `/assets/data/ai/profiles/`
- Common species properties in `/assets/data/species/`
- Shared UI elements for medals and ranks in `/assets/textures/ui/medals/`
- Shared audio assets organized by type in `/assets/audio/`

This structure follows the hybrid approach where truly global, context-agnostic data assets are organized in `/assets/data/`, following the "Global Litmus Test" principle. The structure maintains clear separation of concerns between different data types while ensuring easy access to all data resources needed for game features. Each TBL file type maps to appropriate locations in the target directory structure, maintaining the relationships to other assets as documented in the asset mapping documents.