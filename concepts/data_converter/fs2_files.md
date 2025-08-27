# FS2 Files Conversion Requirements

## Overview
FS2 (Mission) files contain complete mission definitions including briefing data, initial ship placements, AI directives, and event scripting. These complex binary files need to be parsed and converted to Godot's native formats (.tscn/.tres) as part of the migration process, following Godot's feature-based organization principles as defined in the directory_structure.md and Godot_Project_Structure_Refinement.md. The conversion follows a campaign-centric mission organization where all mission data is stored with the mission scenes in campaign-specific directories, transforming the legacy binary format into data-driven Godot resources.

## File Structure and Components

### Mission Header Information
**Purpose**: Basic mission identification and properties
**Conversion Requirements**:
- Extract mission name and description
- Parse author and version information
- Convert mission type (single player, multiplayer) to Godot enums
- Map skybox and ambient lighting settings to Environment resources
- Extract music and audio environment settings to AudioStreamPlayer nodes

### Briefing Data
**Purpose**: Mission introduction and objectives presentation
**Conversion Requirements**:
- Parse briefing text with formatting codes and convert to BBCode
- Extract voice acting references and map to AudioStream files
- Convert objective definitions to Godot MissionObjective resources (.tres)
- Map briefing cutscene references to VideoStream files or Animation resources
- Maintain briefing UI layout information as Control node properties

### Initial State Definitions
**Purpose**: Starting conditions and entity placements
**Conversion Requirements**:
- Parse initial ship placements with positions and orientations (convert to Godot coordinate system)
- Convert wing formations and assignments to Formation resources (.tres)
- Map starting weapon loadouts to WeaponData resources (.tres)
- Extract initial AI directives and goals to AI behavior resources (.tres)
- Handle player ship positioning and setup with PlayerStart nodes

### Event Scripting
**Purpose**: Dynamic mission flow and conditional triggers
**Conversion Requirements**:
- Parse event conditions and triggers and convert to Godot signal connections
- Convert event actions and consequences to AnimationPlayer keyframes or script methods
- Map timeline-based events to Godot's timeline system with frame accuracy
- Handle variable and flag references through exported Resource properties
- Convert sexp (symbolic expression) logic to Godot equivalent using AnimationPlayer and custom script functions

### Message System
**Purpose**: In-mission communications and notifications
**Conversion Requirements**:
- Parse message definitions with sender/receiver information and convert to Message resources (.tres)
- Convert message triggers and conditions to Godot signal-based events
- Map audio references for voice acting to converted AudioStream files (.ogg)
- Handle message priority and grouping through MessageQueue resources (.tres)
- Maintain message history and display properties with persistent data structures

### AI Profiles and Behaviors
**Purpose**: Specific AI directives for mission entities
**Conversion Requirements**:
- Parse AI class assignments for ships referencing AI profiles in `/assets/data/ai/profiles/`
- Convert tactical overrides and special behaviors to LimboAI behavior trees (.lbt)
- Map reinforcement schedules and conditions to mission event timelines (AnimationPlayer)
- Handle support ship behavior (rearm/repair) through mission service systems
- Maintain wing commander and formation assignments with FormationData resources (.tres)

## Conversion Process

### 1. Binary Parsing Phase
- Read FS2 file header and validate format with checksum verification
- Parse mission data chunks using chunk-based structure with error handling
- Extract briefing and fiction text segments preserving narrative context and formatting
- Handle variable length data sections with proper buffer management
- Validate checksums and file integrity with recovery mechanisms for corrupted data

### 2. Data Extraction Phase
- Create intermediate mission data structures following Godot Resource patterns
- Parse entity placements and properties with coordinate system conversion (left-handed to right-handed)
- Extract event graph and conditional logic maintaining branching structures and timing
- Convert briefing objectives to structured format with BBCode formatting and localization support
- Map all cross-references and dependencies through ResourceLoader system with path resolution

### 3. Native Format Generation Phase
- Generate Godot scene structure (.tscn) for mission environment following campaign-centric organization
- Create Godot resource files (.tres) for mission data, objectives, events, and messages
- Convert entity placements to Node3D instances with proper transform properties
- Generate AnimationPlayer resources for event timelines with keyframe sequences
- Create MessageQueue resources for communication systems with priority handling

### 4. Resource Integration Phase
- Link converted table data (ships, weapons, etc.) from feature directories using exported Resource properties
- Integrate converted 3D models and textures from `/features/` directories through MeshInstance3D nodes
- Connect audio references to converted sound files from `/assets/audio/` directories with AudioStreamPlayer3D nodes
- Map animation references to converted animations from `/assets/animations/` directories with Animation resources
- Validate all asset connections using Godot's resource system with comprehensive error reporting

## Campaign-Centric Directory Structure
Following the campaign-centric mission organization principle where "this file defines 'what' happens in a mission, rather than 'how' a game mechanic works":

```
campaigns/
├── hermes/                          # Hermes campaign (main campaign)
│   ├── campaign.tres                # Campaign definition
│   ├── progression.tres             # Campaign progression data
│   ├── pilot_data.tres              # Pilot progression data
│   ├── campaign_intro.tscn          # Campaign intro cutscene scene
│   ├── campaign_credits.tscn        # Campaign end credits scene
│   └── missions/                    # Mission scenes with integrated data
│       ├── m01_hermes/              # Mission 1 - all files together
│       │   ├── mission.tscn         # Main mission scene
│       │   ├── mission_data.tres    # Mission configuration
│       │   ├── briefing.txt         # Briefing text
│       │   ├── fiction.txt          # Fiction text
│       │   ├── objectives.tres      # Mission objectives
│       │   ├── events.tres          # Mission events
│       │   ├── messages.tres        # Mission messages
│       │   ├── cutscenes/           # Mission-specific cutscenes
│       │   │   ├── intro.tscn       # Intro cutscene scene
│       │   │   └── outro.tscn       # Outro cutscene scene
│       │   └── assets/              # Mission-specific assets
│       │       ├── audio/           # Mission audio
│       │       │   ├── briefing.ogg # Briefing voice audio
│       │       │   ├── music.ogg    # Mission background music
│       │       │   └── ambient.ogg  # Ambient mission sounds
│       │       └── visuals/         # Mission visuals
│       │           ├── cutscene_frames/ # Cutscene animation frames
│       │           └── briefing_background.png # Briefing background
│       ├── m02_hermes/              # Mission 2
│       │   ├── mission.tscn
│       │   ├── mission_data.tres
│       │   ├── briefing.txt
│       │   ├── fiction.txt
│       │   ├── objectives.tres
│       │   ├── events.tres
│       │   ├── messages.tres
│       │   ├── cutscenes/
│       │   │   ├── intro.tscn
│       │   │   └── outro.tscn
│       │   └── assets/
│       │       ├── audio/
│       │       └── visuals/
│       └── templates/               # Mission templates
├── brimstone/                       # Brimstone campaign
│   ├── campaign.tres                # Campaign definition
│   ├── progression.tres             # Campaign progression data
│   ├── pilot_data.tres              # Pilot progression data
│   └── missions/                    # Mission scenes
│       ├── m01_brimstone/           # Mission 1
│       │   ├── mission.tscn
│       │   ├── mission_data.tres
│       │   ├── briefing.txt
│       │   ├── fiction.txt
│       │   └── objectives.tres
│       └── templates/               # Mission templates
├── training/                        # Training campaign
│   ├── campaign.tres                # Campaign definition
│   ├── tutorials.tres               # Tutorial definitions
│   └── missions/                    # Training missions
│       ├── intro_training/          # Introduction training
│       │   ├── mission.tscn
│       │   ├── mission_data.tres
│       │   ├── briefing.txt
│       │   └── objectives.tres
│       └── advanced_training/       # Advanced training
│           ├── mission.tscn
│           ├── mission_data.tres
│           ├── briefing.txt
│           └── objectives.tres
└── multiplayer/                     # Multiplayer campaigns
    ├── coop.tres                    # Cooperative campaign
    ├── teams.tres                   # Team vs team campaign
    └── dogfight.tres                # Dogfight campaign
```

## System Integration
FS2 missions are converted to native Godot formats and integrate with various Godot systems following the separation of concerns principle. The migration process transforms legacy binary data into data-driven Godot resources that leverage the engine's native capabilities:

### Mission Management Systems
- `/autoload/mission_manager.gd` - Mission orchestration and state management following the "Is this state or service truly global and required everywhere?" principle
- `/autoload/event_bus.gd` - Global event system for mission events using Godot's signal system
- `/autoload/save_manager.gd` - Save/load system for mission progression with persistent data storage

### Script Systems
- `/scripts/mission/mission_parser.gd` - FS2 file parser with chunk-based structure handling for data extraction
- `/scripts/mission/mission_manager.gd` - Mission orchestration logic with state management using Godot's node system
- `/scripts/mission/event_system.gd` - Mission event handling with AnimationPlayer integration for timeline sequences
- `/scripts/mission/objective_tracker.gd` - Objective tracking with persistent data using Resource serialization

### AI Systems
- `/scripts/ai/ai_behavior.gd` - Base AI behavior class with LimboAI integration for behavior tree execution
- `/scripts/ai/combat_tactics.gd` - Combat behavior logic with tactical decision making using Godot's navigation system
- `/scripts/ai/navigation.gd` - Navigation and pathfinding with waypoint systems using Godot's navigation mesh

### UI Systems
- `/features/ui/briefing/` - Briefing interface components following feature-based organization with RichTextLabel for text display
- `/features/ui/debriefing/` - Debriefing interface components with mission results using Control nodes
- `/features/ui/hud/` - HUD components with real-time mission information using CanvasLayer and Control nodes

## Closely Related Assets
Missions reference assets organized according to the hybrid model where truly global assets are in `/assets/` and feature-specific assets are co-located:

### Narrative Assets
- Fiction text files (.txt) that accompany missions and are converted to `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/fiction.txt` following campaign-centric organization
- Voice acting files (.wav/.ogg) referenced in briefings and converted to `/assets/audio/voice/{faction}/` (passes Global Litmus Test)
- Cutscene audio files referenced in mission flow and organized in `/assets/audio/cutscenes/{campaign}/` (passes Global Litmus Test)

### Configuration Assets
- Ship and weapon table data (.tbl/.tbm) referenced in entity definitions and converted to feature-specific directories:
  - Ship data in `/features/fighters/{faction}_{ship_name}/{ship_name}.tres`
  - Weapon data in `/features/weapons/{weapon_name}/{weapon_name}.tres`
- AI profile definitions in `/assets/data/ai/profiles/` (passes Global Litmus Test)
- Species and IFF relationship definitions in `/assets/data/species/` and `/assets/data/iff/` (passes Global Litmus Test)

### Media Assets
- Particle effect definitions used in mission events and converted to `/features/effects/{effect_name}/{effect_name}.tres`
- Environmental textures and models organized in `/features/environment/{prop_name}/`
- UI textures and animations in `/assets/textures/ui/` and `/assets/animations/ui/` (passes Global Litmus Test)

## Entity Integration
Missions reference entity scenes from `/features/` directories following feature-based organization where each feature is a self-contained entity:

### Ship Entities
- Fighter entities from `/features/fighters/{faction}_{ship_name}/{ship_name}.tscn`
- Capital ship entities from `/features/capital_ships/{faction}_{ship_name}/{ship_name}.tscn`
- Shared ship assets in `/features/fighters/_shared/` and `/features/capital_ships/_shared/`

### Weapon Entities
- Weapon entities from `/features/weapons/{weapon_name}/{weapon_name}.tscn`
- Projectile entities from `/features/weapons/projectiles/{projectile_name}/{projectile_name}.tscn`
- Shared weapon assets in `/features/weapons/_shared/`

### Effect Entities
- Effect entities from `/features/effects/{effect_name}/{effect_name}.tscn`
- Shared effect assets in `/features/effects/_shared/`

### Environmental Entities
- Environmental entities from `/features/environment/{prop_name}/{prop_name}.tscn`
- Shared environment assets in `/features/environment/_shared/`

## Common Shared Assets
Following the "Global Litmus Test" principle for assets that belong in `/assets/`:

### Audio Assets
- UI sound effects in `/assets/audio/sfx/ui/` (passes Global Litmus Test)
- Generic weapon sounds in `/assets/audio/sfx/weapons/` (passes Global Litmus Test)
- Mission music tracks in `/assets/audio/music/` (passes Global Litmus Test)
- Generic explosion sounds in `/assets/audio/sfx/explosions/` (passes Global Litmus Test)

### Visual Assets
- Generic UI textures in `/assets/textures/ui/` (passes Global Litmus Test)
- Shared particle textures in `/assets/textures/effects/` (passes Global Litmus Test)
- Common font resources in `/assets/textures/fonts/` (passes Global Litmus Test)
- Generic UI animations in `/assets/animations/ui/` (passes Global Litmus Test)

### Data Assets
- AI profiles in `/assets/data/ai/profiles/` (passes Global Litmus Test)
- Species definitions in `/assets/data/species/` (passes Global Litmus Test)
- IFF relationship data in `/assets/data/iff/` (passes Global Litmus Test)
- Common mission templates in `/scripts/mission/templates/` (reusable logic, not instantiable objects)

This structure ensures that FS2 missions are properly migrated to Godot's native formats as part of the conversion process, transforming legacy binary data into data-driven Godot resources (.tscn/.tres) while maintaining the feature-based organization and campaign-centric principles. The migration preserves all gameplay-relevant information while leveraging Godot's modern engine capabilities through native file formats and resource systems.