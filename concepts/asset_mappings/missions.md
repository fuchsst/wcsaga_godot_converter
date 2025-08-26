# Missions Asset Mapping

## Overview
This document maps the mission definitions from FS2 files to their corresponding media assets in the Wing Commander Saga Hermes campaign, organized according to the Godot feature-based directory structure. The mapping follows the campaign-centric mission organization principle where all mission data is stored with the mission scenes in campaign-specific directories.

## Asset Types

### Mission Files (.fs2)
FS2 files contain complete mission definitions for individual missions:
- M01-BG-Hermes.fs2 - Mission 1 file (Alcor 1)
- M02-BG-Hermes.fs2 - Mission 2 file 
- M31-BG-Hermes.fs2 - Mission 31 file (Alcor 1)
- etc.

Each FS2 file contains:
- Mission briefing data
- Initial ship placements
- AI directives and events
- Scripting logic
- Objectives and goals
- Message sequences
- Viewer position and orientation for briefing
- Game type flags and mission settings

### Campaign Files (.fc2)
FC2 files define campaign structure and progression:
- codename_hermes.fc2 - Main Hermes campaign file
- prologue.fc2 - Campaign prologue file

Each FC2 file contains:
- Campaign name and description
- Campaign type (single/multiplayer)
- Starting ships and weapons
- Mission sequencing
- Intro/end cutscene references
- Campaign flags and settings

### Fiction Text (.txt)
Mission-specific narrative fiction text:
- m1fiction.txt - Mission 1 fiction text
- d1fiction.txt - Demo 1 fiction text
- d2fiction.txt - Demo 2 fiction text
- etc.

Each fiction file contains:
- Mission introduction text
- Shuttle approach descriptions
- Timeline information
- Narrative context for the mission

### Cutscenes (.ani/.ogg)
Mission-specific cutscene animations and audio:
- Various .ani files in hermes_effects/ - Cutscene animation frames
- Various .ogg files in hermes_movies/ - Briefing and cutscene audio
- hermes_intro.ogg - Campaign intro cutscene
- hermes_credits.ogg - Campaign end cutscene

### Music Tracks (.ogg)
Mission-specific background music:
- Various .ogg files in hermes_movies/ - Mission music and ambient tracks

## Format Conversion Process

### Legacy Formats to Godot Formats

**FS2 Files (.fs2)**
- Legacy mission definition format containing all mission data
- Will be converted to Godot scenes (.tscn) with integrated data resources
- Mission events will be implemented using Godot's animation system and signals
- Entity placements will be converted to Godot scene nodes

**FC2 Files (.fc2)**
- Legacy campaign definition format containing mission sequencing
- Will be converted to Godot campaign resources (.tres)
- Campaign progression data will be integrated with save/load system

**ANI Files (.ani)**
- Legacy animation format for cutscenes and UI elements
- Will be converted to PNG sequences for real-time cutscenes or video format
- Animation timing and frame data preserved in conversion

**TXT Files (.txt)**
- Legacy text format with markup for fiction and briefing
- Will be converted to formatted text resources with BBCode
- Preserved formatting for rich text display in Godot's RichTextLabel

**OGG Files (.ogg)**
- Legacy audio format for voice, music, and sound effects
- Will be maintained in Ogg Vorbis format as it's already Godot-compatible
- Metadata and audio characteristics preserved

## Target Structure
Following the Godot project structure defined in directory_structure.md and the campaign-centric mission organization principle, mission assets are organized as follows:

### Campaigns Directory Structure
Campaigns and their missions are organized in the `/campaigns/` directory, following the principle that "this file defines 'what' happens in a mission, rather than 'how' a game mechanic works."

```
campaigns/
├── hermes/                            # Hermes campaign
│   ├── campaign.tres                  # Campaign definition (converted from .fc2)
│   ├── progression.tres               # Campaign progression data
│   ├── pilot_data.tres                # Pilot progression data
│   ├── campaign_intro.tscn            # Campaign intro cutscene scene
│   ├── campaign_credits.tscn          # Campaign end credits scene
│   └── missions/                      # Mission scenes with integrated data
│       ├── m01_hermes/                # Mission 1 - all files together
│       │   ├── mission.tscn           # Main mission scene (converted from .fs2)
│       │   ├── mission_data.tres      # Mission configuration (converted from .fs2)
│       │   ├── briefing.txt           # Briefing text (converted from .txt)
│       │   ├── fiction.txt            # Fiction text (converted from .txt)
│       │   ├── objectives.tres        # Mission objectives (converted from .fs2)
│       │   ├── events.tres            # Mission events (converted from .fs2)
│       │   ├── messages.tres          # Mission messages (converted from .fs2)
│       │   ├── cutscenes/             # Mission-specific cutscenes
│       │   │   ├── intro.tscn         # Intro cutscene scene
│       │   │   └── outro.tscn         # Outro cutscene scene
│       │   └── assets/                # Mission-specific assets
│       │       ├── audio/             # Mission audio
│       │       │   ├── briefing.ogg   # Briefing voice audio
│       │       │   ├── music.ogg      # Mission background music
│       │       │   └── ambient.ogg    # Ambient mission sounds
│       │       └── visuals/           # Mission visuals
│       │           ├── cutscene_frames/ # Cutscene animation frames
│       │           └── briefing_background.png # Briefing background
│       ├── m02_hermes/                # Mission 2
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
│       └── templates/                 # Mission templates
├── brimstone/                         # Brimstone campaign
│   ├── campaign.tres
│   ├── progression.tres
│   ├── pilot_data.tres
│   └── missions/
│       ├── m01_brimstone/
│       │   ├── mission.tscn
│       │   ├── mission_data.tres
│       │   ├── briefing.txt
│       │   ├── fiction.txt
│       │   └── objectives.tres
│       └── templates/
├── training/                          # Training campaign
│   ├── campaign.tres
│   ├── tutorials.tres
│   └── missions/
│       ├── intro_training/
│       │   ├── mission.tscn
│       │   ├── mission_data.tres
│       │   ├── briefing.txt
│       │   └── objectives.tres
│       └── advanced_training/
│           ├── mission.tscn
│           ├── mission_data.tres
│           ├── briefing.txt
│           └── objectives.tres
└── multiplayer/                       # Multiplayer campaigns
    ├── coop.tres
    ├── teams.tres
    └── dogfight.tres
```

### Features Directory Structure
Mission-related UI components are organized within the `/features/ui/` directory, following the feature-based organization principle where each UI component is a self-contained entity with all its related assets.

```
features/
├── ui/                                # UI feature elements
│   ├── briefing/                      # Briefing interface
│   │   ├── briefing_screen.tscn       # Main briefing scene
│   │   ├── briefing_screen.gd         # Briefing controller script
│   │   └── assets/                    # Feature-specific assets
│   │       ├── backgrounds/           # Briefing backgrounds
│   │       ├── fonts/                 # Briefing fonts
│   │       └── sounds/                # Briefing interface sounds
│   ├── debriefing/                    # Debriefing interface
│   │   ├── debriefing_screen.tscn     # Main debriefing scene
│   │   ├── debriefing_screen.gd       # Debriefing controller script
│   │   └── assets/                    # Feature-specific assets
│   │       ├── backgrounds/           # Debriefing backgrounds
│   │       ├── fonts/                 # Debriefing fonts
│   │       └── sounds/                # Debriefing interface sounds
│   ├── tech_database/                 # Technical database (includes fiction viewer)
│   │   ├── tech_database.tscn         # Main tech database scene
│   │   ├── tech_database.gd           # Tech database controller script
│   │   └── assets/                    # Feature-specific assets
│   │       ├── backgrounds/           # Tech database backgrounds
│   │       ├── fonts/                 # Tech database fonts
│   │       └── sounds/                # Tech database interface sounds
│   └── _shared/                       # Shared UI assets
│       ├── fonts/                     # UI fonts
│       ├── icons/                     # UI icons
│       ├── themes/                    # UI themes
│       └── components/                # Reusable UI components
└── templates/                         # Feature templates
```

### Assets Directory Structure
Generic audio assets that are shared across multiple missions are organized in the global `/assets/` directory, following the "Global Litmus Test" principle.

```
assets/
├── audio/                             # Shared audio files
│   ├── sfx/                           # Generic sound effects
│   │   └── ui/                        # UI sound effects
│   │       ├── mission_start.ogg
│   │       ├── mission_complete.ogg
│   │       └── objective_complete.ogg
│   ├── music/                         # Background music tracks
│   │   ├── ambient_combat.ogg
│   │   ├── ambient_peaceful.ogg
│   │   └── mission_victory.ogg
│   └── voice/                         # Shared voice lines
│       ├── mission_briefing/
│       ├── mission_debriefing/
│       └── campaign_intro/
├── data/                              # Shared data resources
│   └── mission/                       # Mission data resources
│       ├── event_templates.tres       # Common event templates
│       ├── objective_templates.tres   # Common objective templates
│       └── message_templates.tres     # Common message templates
└── animations/                        # Shared animation files
    └── ui/                            # UI animations
        ├── mission_transition/
        ├── briefing_fade/
        └── debriefing_appear/
```

### Autoload Directory Structure
Mission management systems are implemented as autoload singletons, following the "Is this state or service truly global and required everywhere?" principle.

```
autoload/
├── mission_manager.gd                 # Mission orchestration and state management
├── event_bus.gd                       # Global event system for mission events
└── save_manager.gd                    # Save/load system for mission progression
```

### Scripts Directory Structure
Reusable mission system scripts are organized in the `/scripts/mission/` directory, following the separation of concerns principle.

```
scripts/
├── mission/                           # Mission system scripts
│   ├── mission_parser.gd              # FS2/FC2 file parser
│   ├── mission_manager.gd             # Mission orchestration logic
│   ├── event_system.gd                # Mission event handling
│   ├── objective_tracker.gd           # Objective tracking
│   ├── campaign_progression.gd        # Campaign progression logic
│   ├── briefing_system.gd             # Briefing presentation logic
│   └── debriefing_system.gd           # Debriefing evaluation logic
└── utilities/                         # Utility functions and helpers
    ├── resource_loader.gd             # Resource loading utilities
    └── text_formatter.gd              # Text formatting utilities
```

## Example Mapping
For Mission 1 (M01-BG-Hermes.fs2):
- M01-BG-Hermes.fs2 → /campaigns/hermes/missions/m01_hermes/mission.tscn (scene) and /campaigns/hermes/missions/m01_hermes/mission_data.tres (data resource)
- m1fiction.txt → /campaigns/hermes/missions/m01_hermes/fiction.txt
- codename_hermes.fc2 → /campaigns/hermes/campaign.tres
- hermes_intro.ogg → /campaigns/hermes/campaign_intro.tscn (with audio reference)
- hermes_credits.ogg → /campaigns/hermes/campaign_credits.tscn (with audio reference)
- Various briefing .ogg files → /campaigns/hermes/missions/m01_hermes/assets/audio/briefing.ogg
- Various .ani files → /campaigns/hermes/missions/m01_hermes/assets/visuals/cutscene_frames/

## Conversion Pipeline
1. **FS2/FC2 Parser**: Custom parser to extract mission and campaign definitions from .fs2/.fc2 files
2. **ANI Converter**: Convert .ani animation files to PNG sequences or video format
3. **TXT Formatter**: Convert .txt text files to BBCode formatted text resources
4. **Resource Generator**: Create Godot .tres files with converted mission and campaign data
5. **Scene Builder**: Generate Godot scenes (.tscn) for missions with integrated entity placements
6. **Event System**: Implement mission events using Godot's animation system and signals
7. **UI Integration**: Integrate mission data with briefing/debriefing UI components
8. **Validation**: Verify converted missions match original gameplay and narrative flow

## Relationship to Other Assets
Missions are closely related to:
- **Campaign System**: Organized in `/campaigns/` directory with mission sequencing and progression data
- **UI System**: Integrated with `/features/ui/briefing/` and `/features/ui/debriefing/` for mission presentation
- **Audio System**: Use shared mission sounds from `/assets/audio/` and mission-specific audio in `/campaigns/{campaign}/missions/{mission}/assets/audio/`
- **Text System**: Fiction viewer integrated with `/features/ui/tech_database/` for narrative presentation
- **Entity System**: Missions create and manage game entities from `/features/` directory
- **AI System**: Missions set AI directives and behaviors for entities
- **Save System**: Mission progression tracked in `/campaigns/{campaign}/pilot_data.tres`