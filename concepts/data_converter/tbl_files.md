# TBL Files Conversion Requirements

## Overview
TBL (Table) files contain structured data definitions for various game elements in Wing Commander Saga. These files need to be converted to Godot's resource format (.tres) to maintain the data-driven design approach, following Godot's feature-based organization principles and the hybrid model defined in our project structure.

The TBL files found in the source assets include:
- `ships.tbl` - Ship class definitions with physics, weapons, and visual properties
- `weapons.tbl` - Weapon definitions with damage, firing rates, and effects
- `ai.tbl` - AI behavior characteristics and combat parameters
- `ai_profiles.tbl` - AI behavior profiles with difficulty scaling parameters
- `Species.tbl` - Species definitions and relationships
- `Species_defs.tbl` - Species definitions with thruster animations and debris behavior
- `iff_defs.tbl` - IFF (Identification Friend or Foe) relationship definitions
- `fireball.tbl` - Fireball/explosion effect definitions
- `weapon_expl.tbl` - Weapon impact explosion definitions
- `medals.tbl` - Medal definitions with visual representations
- `rank.tbl` - Military rank definitions with promotion requirements
- `sounds.tbl` - Sound effect definitions with file references
- `music.tbl` - Music track definitions for campaign events
- `cutscenes.tbl` - Cutscene definitions with audio file references
- `asteroid.tbl` - Asteroid field definitions and properties
- `autopilot.tbl` - Autopilot navigation and behavior settings
- `credits.tbl` - Credits sequence definitions and timing
- `fonts.tbl` - Font definitions and character mappings
- `help.tbl` - In-game help system definitions
- `hud_gauges.tbl` - HUD gauge definitions and visual properties
- `icons.tbl` - Icon definitions for radar and interface
- `launchhelp.tbl` - Launch sequence help definitions
- `lightning.tbl` - Lightning/electrical effect definitions
- `mainhall.tbl` - Main menu/hall interface definitions
- `menu.tbl` - Menu system definitions and layouts
- `messages.tbl` - Message system definitions and templates
- `mflash.tbl` - Muzzle flash effect definitions
- `nebula.tbl` - Nebula cloud definitions and properties
- `pixels.tbl` - Pixel shader effect definitions
- `scripting.tbl` - Scripting system definitions and hooks
- `ssm.tbl` - Subspace missile definitions and behaviors
- `stars.tbl` - Starfield and background definitions
- `strings.tbl` - String table and localization definitions
- `tips.tbl` - Loading screen tips and hints
- `traitor.tbl` - Traitor/defection event definitions
- `tstrings.tbl` - Technical string definitions

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
- Map to `/features/fighters/{faction}/{ship_name}/{ship_name}.tres` for fighters
- Map to `/features/capital_ships/{faction}/{ship_name}/{ship_name}.tres` for capital ships

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
- Map to `/features/weapons/{weapon_name}/{weapon_name}.tres` for self-contained weapon features

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
- Reference related assets in `/assets/audio/sfx/` and `/assets/audio/voice/`

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
- Map to `/features/fighters/_shared/species/{species_name}.tres` for species-specific assets
- Reference related animations in `/features/fighters/_shared/effects/` and textures in `/features/fighters/_shared/textures/`

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
- Map to `/features/ui/hud/_shared/iff/{iff_name}.tres` for HUD display elements
- Reference related UI assets in `/features/ui/hud/_shared/radar/` and `/features/ui/hud/_shared/iff/`

### Fireball Effects (fireball.tbl)
**Purpose**: Defines fireball/explosion effect properties and behaviors
**Source Format**: Custom TBL format with effect sections
**Target Format**: Effect resources (.tres)
**Conversion Requirements**:
- Parse effect names and descriptions
- Extract effect properties (LOD settings)
- Map to visual assets for conversion
- Map to `/features/effects/{effect_name}/{effect_name}.tres` for self-contained effect features
- Reference related assets in `/features/effects/_shared/` for shared effect components

### Weapon Impact Effects (weapon_expl.tbl)
**Purpose**: Defines weapon impact explosion effects
**Source Format**: Custom TBL format with explosion effect sections
**Target Format**: Effect resources (.tres)
**Conversion Requirements**:
- Parse effect names and descriptions
- Extract effect properties
- Map to visual assets for conversion
- Map to `/features/weapons/_shared/impact_effects/{effect_name}.tres` for shared impact effects
- Reference related assets in `/features/effects/` for effect implementations

### Medals (medals.tbl)
**Purpose**: Defines military decoration and award definitions
**Source Format**: Custom TBL format with medal sections
**Target Format**: Medal resources (.tres)
**Conversion Requirements**:
- Parse medal names and descriptions
- Extract visual representation references (bitmap files)
- Map number of modifications/variations
- Map to `/features/ui/debriefing/_shared/medals/{medal_name}.tres` for debriefing screen elements
- Reference related assets in `/features/ui/debriefing/_shared/icons/`

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
- Map to `/features/ui/debriefing/_shared/ranks/{rank_name}.tres` for debriefing screen elements
- Reference related assets in `/features/ui/debriefing/_shared/insignia/`

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

### AI Behavior (ai.tbl)
**Purpose**: Defines general AI behavior characteristics and combat parameters
**Source Format**: Custom TBL format with AI behavior sections
**Target Format**: AIBehavior resources (.tres)
**Conversion Requirements**:
- Parse AI behavior names and combat styles
- Extract combat parameters (attack ranges, evasion patterns)
- Convert weapon usage preferences and tactics
- Map to `/assets/data/ai/behaviors/{behavior_name}.tres` following the Global Litmus Test
- Reference related AI assets in `/assets/data/ai/`

### Species Relationships (Species.tbl)
**Purpose**: Defines species relationships and diplomatic settings
**Source Format**: Custom TBL format with species relationship sections
**Target Format**: SpeciesRelationship resources (.tres)
**Conversion Requirements**:
- Parse species names and diplomatic status
- Extract relationship matrices and alliance settings
- Convert diplomatic event triggers
- Map to `/assets/data/species/relationships/{relationship_name}.tres` following the Global Litmus Test
- Reference related species assets in `/features/fighters/_shared/species/`

### Asteroid Fields (asteroid.tbl)
**Purpose**: Defines asteroid field properties and generation parameters
**Source Format**: Custom TBL format with asteroid field sections
**Target Format**: AsteroidField resources (.tres)
**Conversion Requirements**:
- Parse asteroid field names and descriptions
- Extract generation parameters (density, size ranges)
- Convert movement patterns and rotation speeds
- Map to `/features/environment/asteroid_fields/{field_name}.tres` for environmental features
- Reference related asteroid models in `/features/environment/_shared/asteroids/`

### Autopilot Systems (autopilot.tbl)
**Purpose**: Defines autopilot navigation and behavior settings
**Source Format**: Custom TBL format with autopilot sections
**Target Format**: AutopilotProfile resources (.tres)
**Conversion Requirements**:
- Parse autopilot profile names and descriptions
- Extract navigation parameters (approach distances, docking speeds)
- Convert emergency behavior settings
- Map to `/assets/data/ai/autopilot/{profile_name}.tres` following the Global Litmus Test
- Reference related navigation assets in `/scripts/ai/navigation/`

### Credits Sequence (credits.tbl)
**Purpose**: Defines credits sequence timing and content
**Source Format**: Custom TBL format with credits entries
**Target Format**: CreditsSequence resources (.tres)
**Conversion Requirements**:
- Parse credits timing and scroll speeds
- Extract credit text and formatting
- Convert special effect triggers
- Map to `/assets/data/ui/credits/{sequence_name}.tres` following the Global Litmus Test
- Reference related UI assets in `/features/ui/credits/`

### Font Definitions (fonts.tbl)
**Purpose**: Defines font properties and character mappings
**Source Format**: Custom TBL format with font sections
**Target Format**: FontDefinition resources (.tres)
**Conversion Requirements**:
- Parse font names and character set definitions
- Extract spacing and kerning information
- Convert special character mappings
- Map to `/assets/data/ui/fonts/{font_name}.tres` following the Global Litmus Test
- Reference related font assets in `/features/ui/_shared/fonts/`

### Help System (help.tbl)
**Purpose**: Defines in-game help system content and structure
**Source Format**: Custom TBL format with help entries
**Target Format**: HelpTopic resources (.tres)
**Conversion Requirements**:
- Parse help topic names and categories
- Extract help text and formatting
- Convert cross-reference links
- Map to `/assets/data/ui/help/{topic_name}.tres` following the Global Litmus Test
- Reference related UI assets in `/features/ui/help/`

### HUD Gauges (hud_gauges.tbl)
**Purpose**: Defines HUD gauge visual properties and behaviors
**Source Format**: Custom TBL format with gauge sections
**Target Format**: HUDGauge resources (.tres)
**Conversion Requirements**:
- Parse gauge names and display properties
- Extract visual representation parameters
- Convert animation and behavior settings
- Map to `/features/ui/hud/_shared/gauges/{gauge_name}.tres` for HUD components
- Reference related gauge assets in `/features/ui/hud/_shared/`

### Icons (icons.tbl)
**Purpose**: Defines icon properties for radar and interface
**Source Format**: Custom TBL format with icon entries
**Target Format**: IconDefinition resources (.tres)
**Conversion Requirements**:
- Parse icon names and descriptions
- Extract visual properties and color mappings
- Convert radar display settings
- Map to `/features/ui/hud/_shared/icons/{icon_name}.tres` for HUD components
- Reference related icon assets in `/features/ui/hud/_shared/icons/`

### Launch Help (launchhelp.tbl)
**Purpose**: Defines launch sequence help content and timing
**Source Format**: Custom TBL format with launch help entries
**Target Format**: LaunchHelp resources (.tres)
**Conversion Requirements**:
- Parse help message timing and triggers
- Extract help text and formatting
- Convert sequence step dependencies
- Map to `/assets/data/ui/launch_help/{help_name}.tres` following the Global Litmus Test
- Reference related UI assets in `/features/ui/hud/`

### Lightning Effects (lightning.tbl)
**Purpose**: Defines lightning/electrical effect properties
**Source Format**: Custom TBL format with lightning effect sections
**Target Format**: LightningEffect resources (.tres)
**Conversion Requirements**:
- Parse effect names and descriptions
- Extract electrical properties and damage values
- Convert visual effect parameters
- Map to `/features/effects/lightning/{effect_name}.tres` for electrical effects
- Reference related effect assets in `/features/effects/_shared/`

### Main Menu (mainhall.tbl)
**Purpose**: Defines main menu/hall interface properties
**Source Format**: Custom TBL format with menu sections
**Target Format**: MainMenuDefinition resources (.tres)
**Conversion Requirements**:
- Parse menu layout and navigation settings
- Extract background and theme properties
- Convert menu item definitions
- Map to `/features/ui/main_menu/_shared/menu_definition.tres` for menu components
- Reference related UI assets in `/features/ui/main_menu/`

### Menu System (menu.tbl)
**Purpose**: Defines menu system layouts and behaviors
**Source Format**: Custom TBL format with menu system sections
**Target Format**: MenuSystem resources (.tres)
**Conversion Requirements**:
- Parse menu system structure and hierarchy
- Extract navigation flow and state transitions
- Convert input handling settings
- Map to `/assets/data/ui/menus/{system_name}.tres` following the Global Litmus Test
- Reference related UI assets in `/features/ui/`

### Message System (messages.tbl)
**Purpose**: Defines message system templates and delivery rules
**Source Format**: Custom TBL format with message entries
**Target Format**: MessageTemplate resources (.tres)
**Conversion Requirements**:
- Parse message templates and formatting
- Extract delivery conditions and priorities
- Convert voice acting references
- Map to `/assets/data/communications/messages/{template_name}.tres` following the Global Litmus Test
- Reference related audio assets in `/assets/audio/voice/`

### Muzzle Flash Effects (mflash.tbl)
**Purpose**: Defines muzzle flash effect properties
**Source Format**: Custom TBL format with muzzle flash sections
**Target Format**: MuzzleFlashEffect resources (.tres)
**Conversion Requirements**:
- Parse effect names and descriptions
- Extract visual properties and timing
- Convert weapon association mappings
- Map to `/features/weapons/_shared/muzzle_flashes/{effect_name}.tres` for shared weapon effects
- Reference related effect assets in `/features/effects/`

### Nebula Clouds (nebula.tbl)
**Purpose**: Defines nebula cloud properties and effects
**Source Format**: Custom TBL format with nebula sections
**Target Format**: NebulaCloud resources (.tres)
**Conversion Requirements**:
- Parse nebula names and descriptions
- Extract visual properties and density settings
- Convert environmental effects (sensor interference, damage)
- Map to `/features/environment/nebulas/{nebula_name}.tres` for environmental features
- Reference related effect assets in `/features/environment/_shared/`

### Pixel Shaders (pixels.tbl)
**Purpose**: Defines pixel shader effect properties
**Source Format**: Custom TBL format with shader sections
**Target Format**: PixelShader resources (.tres)
**Conversion Requirements**:
- Parse shader names and descriptions
- Extract shader parameters and uniforms
- Convert performance optimization settings
- Map to `/assets/data/shaders/pixel/{shader_name}.tres` following the Global Litmus Test
- Reference related shader assets in `/assets/shaders/`

### Scripting System (scripting.tbl)
**Purpose**: Defines scripting system hooks and event handlers
**Source Format**: Custom TBL format with scripting sections
**Target Format**: ScriptingHook resources (.tres)
**Conversion Requirements**:
- Parse script hook names and event types
- Extract parameter definitions and return types
- Convert event handler mappings
- Map to `/assets/data/scripting/hooks/{hook_name}.tres` following the Global Litmus Test
- Reference related script assets in `/scripts/mission/`

### Subspace Missiles (ssm.tbl)
**Purpose**: Defines subspace missile properties and behaviors
**Source Format**: Custom TBL format with missile sections
**Target Format**: SubspaceMissile resources (.tres)
**Conversion Requirements**:
- Parse missile names and descriptions
- Extract subspace travel properties
- Convert damage and effect parameters
- Map to `/features/weapons/subspace_missiles/{missile_name}.tres` for specialized weapons
- Reference related weapon assets in `/features/weapons/_shared/`

### Starfield Backgrounds (stars.tbl)
**Purpose**: Defines starfield and background properties
**Source Format**: Custom TBL format with starfield sections
**Target Format**: StarfieldDefinition resources (.tres)
**Conversion Requirements**:
- Parse starfield names and descriptions
- Extract star density and distribution patterns
- Convert parallax and movement settings
- Map to `/assets/data/environment/starfields/{starfield_name}.tres` following the Global Litmus Test
- Reference related environment assets in `/features/environment/_shared/`

### String Tables (strings.tbl)
**Purpose**: Defines string table for localization and text content
**Source Format**: Custom TBL format with string entries
**Target Format**: StringTable resources (.tres)
**Conversion Requirements**:
- Parse string identifiers and translations
- Extract formatting and placeholder definitions
- Convert language-specific variations
- Map to `/assets/data/localization/strings/{language_code}.tres` following the Global Litmus Test
- Reference related localization assets in `/assets/data/localization/`

### Loading Tips (tips.tbl)
**Purpose**: Defines loading screen tips and hints
**Source Format**: Custom TBL format with tip entries
**Target Format**: LoadingTip resources (.tres)
**Conversion Requirements**:
- Parse tip categories and display conditions
- Extract tip text and formatting
- Convert display timing and rotation settings
- Map to `/assets/data/ui/tips/{category_name}.tres` following the Global Litmus Test
- Reference related UI assets in `/features/ui/loading/`

### Traitor Events (traitor.tbl)
**Purpose**: Defines traitor/defection event conditions and outcomes
**Source Format**: Custom TBL format with traitor event sections
**Target Format**: TraitorEvent resources (.tres)
**Conversion Requirements**:
- Parse event names and trigger conditions
- Extract defection consequences and dialogue
- Convert loyalty check parameters
- Map to `/assets/data/events/traitor/{event_name}.tres` following the Global Litmus Test
- Reference related event assets in `/scripts/mission/events/`

### Technical Strings (tstrings.tbl)
**Purpose**: Defines technical string definitions for system messages
**Source Format**: Custom TBL format with technical string entries
**Target Format**: TechnicalString resources (.tres)
**Conversion Requirements**:
- Parse technical message identifiers
- Extract system-specific formatting
- Convert error code mappings
- Map to `/assets/data/localization/technical/{system_name}.tres` following the Global Litmus Test
- Reference related system assets in `/scripts/utilities/`

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
│   └── music/                     # Background music tracks
├── behavior_trees/                # Shared LimboAI behavior trees
│   ├── ai/                        # AI behavior trees
│   │   ├── combat/                # Combat-related behavior trees
│   │   ├── navigation/            # Navigation behavior trees
│   │   └── tactical/              # Tactical behavior trees
│   └── mission/                   # Mission-specific behavior trees
├── data/                          # Shared data resources
│   ├── ai/                        # AI data resources
│   │   └── profiles/              # AI profile definitions
│   └── mission/                   # Mission data resources
├── textures/                      # Shared texture files
│   ├── ui/                        # Generic UI elements
│   ├── effects/                   # Particle textures used by multiple effects
│   └── fonts/                     # Font textures
└── animations/                    # Shared animation files
    ├── ui/                        # UI animations
    └── effects/                   # Generic effect animations
```

## Integration Points

### Data Converter Output Mapping
- AIProfile resources → `/assets/data/ai/profiles/{profile_name}.tres`
- Sound resources → `/assets/data/audio/sounds/{sound_name}.tres`
- Music resources → `/assets/data/audio/music/{music_name}.tres`
- Cutscene resources → `/assets/data/cutscenes/{cutscene_name}.tres`

### Resource References
- **AI systems** in `/scripts/ai/` reference AIProfile resources from `/assets/data/ai/profiles/`
- **Mission scenes** in `/campaigns/{campaign}/missions/` reference data resources for entity instantiation
- **UI components** in `/features/ui/` reference data resources for display information

## Relationship to Other Assets

### Entity Integration
Converted TBL data integrates with entity scenes following the feature-based organization:
- AIProfile resources are referenced by AI behavior scripts in `/scripts/ai/`

### Common Shared Assets
- Universal AI behavior templates in `/assets/data/ai/profiles/`
- Shared audio assets organized by type in `/assets/audio/`

This structure follows the hybrid approach where truly global, context-agnostic data assets are organized in `/assets/data/`, following the "Global Litmus Test" principle. The structure maintains clear separation of concerns between different data types while ensuring easy access to all data resources needed for game features. Each TBL file type maps to appropriate locations in the target directory structure, maintaining the relationships to other assets as documented in the asset mapping documents.