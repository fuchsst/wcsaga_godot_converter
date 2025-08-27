# TXT Files Conversion Requirements

## Overview
TXT files contain narrative fiction for missions and campaigns in Wing Commander Saga. These text files need to be converted to Godot's rich text format while preserving their formatting and presentation style, following Godot's feature-based organization principles and the hybrid model defined in our project structure.

Based on examination of the source assets, the TXT files found include:
- `d1fiction.txt` - Disc 1 fiction text (Prologue campaign)
- `d2fiction.txt` - Disc 2 fiction text (Prologue campaign)
- `d3fiction.txt` - Disc 3 fiction text (Prologue campaign)
- `d4fiction.txt` - Disc 4 fiction text (Prologue campaign)
- `d5fiction.txt` - Disc 5 fiction text (Prologue campaign)
- `m1fiction.txt` - Mission 1 fiction text (Hermes campaign)

These files contain custom formatting codes (e.g., $B for bold) and narrative content that needs to be converted to Godot's BBCode format for use with RichTextLabel components.

## File Types and Conversion Requirements

### Mission Fiction
**Purpose**: Story narrative and mission context
**Source Format**: Plain text with custom formatting codes
**Target Format**: Rich text resources with BBCode formatting
**Conversion Requirements**:
- Parse custom formatting codes (e.g., $B for bold)
- Convert to BBCode for Godot's RichTextLabel
- Maintain paragraph structure and line breaks
- Handle character names and dialogue formatting
- Preserve narrative pacing and presentation
- Map to appropriate campaign and mission directories

### Campaign Fiction
**Purpose**: Overarching campaign narrative and story context
**Source Format**: Plain text with chapter divisions and custom formatting
**Target Format**: Navigable text resources with BBCode formatting
**Conversion Requirements**:
- Parse chapter and section divisions
- Convert custom markup to BBCode formatting
- Maintain story progression and flow
- Handle character development notes
- Generate appropriate presentation structure

## Conversion Process

### 1. Format Analysis Phase
- Identify text file type and purpose (mission fiction, campaign fiction)
- Parse custom formatting codes and markup (e.g., $B for bold)
- Extract structural elements (chapters, sections, paragraphs)
- Identify character names and dialogue sections
- Check for cross-references and narrative connections

### 2. Content Conversion Phase
- Convert custom markup to BBCode (e.g., $B...$B → [b]...[/b])
- Preserve text content and narrative meaning
- Handle special characters and symbols
- Maintain paragraph and line structure
- Generate appropriate formatting hierarchy

### 3. Structuring Phase
- Create structured text resources in BBCode format
- Generate navigation and indexing data for longer texts
- Handle cross-references and narrative connections
- Create metadata for search and filtering
- Organize into appropriate campaign and mission directories

### 4. Integration Phase
- Integrate with Godot's RichTextLabel components
- Generate UI layouts for fiction presentation
- Handle scrolling and navigation controls
- Create search and filtering capabilities where appropriate
- Validate content presentation and readability

## Directory Structure Alignment
Following the Godot project structure defined in directory_structure.md and the hybrid organizational model:

### Campaigns Directory Structure
Fiction text files are co-located with mission scenes in campaign directories following the campaign-centric mission organization principle:

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
│       │   ├── briefing.txt         # Briefing text (converted from source)
│       │   ├── fiction.txt          # Fiction text (converted from m1fiction.txt)
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
│       └── m02_hermes/              # Mission 2
│           ├── mission.tscn
│           ├── mission_data.tres
│           ├── briefing.txt
│           ├── fiction.txt
│           ├── objectives.tres
│           ├── events.tres
│           ├── messages.tres
│           ├── cutscenes/
│           │   ├── intro.tscn
│           │   └── outro.tscn
│           └── assets/
│               ├── audio/
│               └── visuals/
├── prologue/                        # Prologue campaign (demo missions)
│   ├── campaign.tres                # Campaign definition
│   ├── progression.tres             # Campaign progression data
│   ├── pilot_data.tres              # Pilot progression data
│   └── missions/                    # Mission scenes with integrated data
│       ├── demo_01_prologue/        # Demo Mission 1
│       │   ├── mission.tscn         # Main mission scene
│       │   ├── mission_data.tres    # Mission configuration
│       │   ├── briefing.txt         # Briefing text
│       │   ├── fiction.txt          # Fiction text (converted from d1fiction.txt)
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
│       ├── demo_02_prologue/        # Demo Mission 2
│       │   ├── mission.tscn
│       │   ├── mission_data.tres
│       │   ├── briefing.txt
│       │   ├── fiction.txt          # Fiction text (converted from d2fiction.txt)
│       │   ├── objectives.tres
│       │   ├── events.tres
│       │   ├── messages.tres
│       │   ├── cutscenes/
│       │   │   ├── intro.tscn
│       │   │   └── outro.tscn
│       │   └── assets/
│       │       ├── audio/
│       │       └── visuals/
│       ├── demo_03_prologue/        # Demo Mission 3
│       │   ├── mission.tscn
│       │   ├── mission_data.tres
│       │   ├── briefing.txt
│       │   ├── fiction.txt          # Fiction text (converted from d3fiction.txt)
│       │   ├── objectives.tres
│       │   ├── events.tres
│       │   ├── messages.tres
│       │   ├── cutscenes/
│       │   │   ├── intro.tscn
│       │   │   └── outro.tscn
│       │   └── assets/
│       │       ├── audio/
│       │       └── visuals/
│       ├── demo_04_prologue/        # Demo Mission 4
│       │   ├── mission.tscn
│       │   ├── mission_data.tres
│       │   ├── briefing.txt
│       │   ├── fiction.txt          # Fiction text (converted from d4fiction.txt)
│       │   ├── objectives.tres
│       │   ├── events.tres
│       │   ├── messages.tres
│       │   ├── cutscenes/
│       │   │   ├── intro.tscn
│       │   │   └── outro.tscn
│       │   └── assets/
│       │       ├── audio/
│       │       └── visuals/
│       └── demo_05_prologue/        # Demo Mission 5
│           ├── mission.tscn
│           ├── mission_data.tres
│           ├── briefing.txt
│           ├── fiction.txt          # Fiction text (converted from d5fiction.txt)
│           ├── objectives.tres
│           ├── events.tres
│           ├── messages.tres
│           ├── cutscenes/
│           │   ├── intro.tscn
│           │   └── outro.tscn
│           └── assets/
│               ├── audio/
│               └── visuals/
```

### Features Directory Structure
UI components that display fiction content are organized within feature directories following the co-location principle:

```
features/
├── ui/                              # UI feature elements
│   ├── briefing/                    # Briefing interface
│   │   ├── briefing_screen.tscn     # Main briefing scene
│   │   ├── briefing_screen.gd       # Briefing controller script
│   │   ├── background.webp          # Background graphic
│   │   ├── text_display/            # Text display area
│   │   ├── mission_map/             # Mission map area
│   │   ├── animations/              # Briefing animations
│   │   └── sounds/                  # Briefing sounds
│   │       ├── voice_playback.ogg   # Voice playback sound
│   │       └── transition.ogg       # Screen transition sound
│   ├── debriefing/                  # Debriefing interface
│   │   ├── debriefing_screen.tscn   # Main debriefing scene
│   │   ├── debriefing_screen.gd     # Debriefing controller script
│   │   ├── background.webp          # Background graphic
│   │   ├── results_display/         # Results display area
│   │   ├── statistics/              # Statistics display
│   │   ├── animations/              # Debriefing animations
│   │   └── sounds/                  # Debriefing sounds
│   │       ├── voice_playback.ogg   # Voice playback sound
│   │       └── transition.ogg       # Screen transition sound
│   ├── tech_database/               # Technical database (includes fiction viewer)
│   │   ├── tech_database.tscn       # Main tech database scene
│   │   ├── tech_database.gd         # Tech database controller script
│   │   ├── backgrounds/             # Background graphics
│   │   ├── ship_entries/            # Ship entry graphics
│   │   ├── weapon_entries/          # Weapon entry graphics
│   │   ├── animations/              # Database animations
│   │   └── sounds/                  # Database sounds
│   │       ├── entry_select.ogg     # Entry selection sound
│   │       └── page_turn.ogg        # Page turn sound
│   └── _shared/                     # Shared UI assets
│       ├── fonts/                   # UI fonts
│       ├── icons/                   # UI icons
│       ├── themes/                  # UI themes
│       ├── cursors/                 # Cursor graphics
│       └── components/              # Reusable UI components
│           ├── buttons/             # Button components
│           ├── sliders/             # Slider components
│           ├── checkboxes/          # Checkbox components
│           ├── dropdowns/           # Dropdown components
│           ├── text_fields/         # Text field components
│           └── lists/               # List components
└── templates/                       # Feature templates
```

## Integration Points

### Data Converter Output Mapping
- Mission fiction files (d1fiction.txt, m1fiction.txt, etc.) → Converted to BBCode and co-located with mission scenes:
  - Prologue campaign fiction → `/campaigns/prologue/missions/{mission_id}_{mission_name}/fiction.txt`
  - Hermes campaign fiction → `/campaigns/hermes/missions/{mission_id}_{mission_name}/fiction.txt`
- Mission briefing text → `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/briefing.txt`
- Campaign data → `/campaigns/{campaign}/campaign.tres` with fiction progression references

### Resource References
- **Mission scenes** in `/campaigns/{campaign}/missions/` directly reference their co-located fiction text files
- **Briefing screens** in `/features/ui/briefing/` load and display mission-specific fiction content from campaign directories
- **Tech database** in `/features/ui/tech_database/` may reference narrative elements for context and lore
- **Fiction viewer** in `/features/ui/tech_database/` displays longer narrative content from campaign directories

## Relationship to Other Assets

### UI Integration
Text files integrate with UI components in `/features/ui/` directories following the feature-based organization:
- `/features/ui/briefing/` - Briefing screen fiction display for mission context
- `/features/ui/debriefing/` - Debriefing screen mission results and narrative follow-up
- `/features/ui/tech_database/` - Technical database with fiction viewer component for lore and backstory
- `/features/ui/main_menu/` - Main menu campaign selection with narrative context

### Mission Integration
Text files are co-located with mission scenes in `/campaigns/` directories following the campaign-centric organization:
- `/campaigns/prologue/missions/demo_01_prologue/fiction.txt` - Prologue demo mission 1 fiction
- `/campaigns/hermes/missions/m01_hermes/fiction.txt` - Hermes campaign mission 1 fiction
- `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/briefing.txt` - Mission briefing text
- `/campaigns/{campaign}/campaign.tres` - Campaign overview with references to fiction content progression

### System Integration
Text files integrate with Godot systems following the separation of concerns:
- `/autoload/audio_manager.gd` - Synchronized voice acting with fiction reading during briefings
- `/scripts/mission/briefing_system.gd` - Briefing presentation logic for fiction display
- `/scripts/mission/campaign_progression.gd` - Campaign progression with fiction unlocking and narrative flow
- `/features/ui/tech_database/tech_database.gd` - Tech database controller with fiction viewer integration
- `/scripts/utilities/text_formatter.gd` - BBCode conversion utilities for text formatting

### Closely Related Assets
Based on the asset mapping documentation and source file analysis:
- Mission files (.fs2) that reference specific fiction entries (Demo-01-BG-Hermes.fs2 references d1fiction.txt, M01-BG-Hermes.fs2 references m1fiction.txt)
- Briefing screens that display fiction content from `/features/ui/briefing/`
- Voice acting files that accompany fiction reading from `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/assets/audio/briefing.ogg`
- Campaign files (.fc2) that define campaign structure and fiction progression

### Entity Asset Organization
Following the co-location principle where all files related to a single feature are grouped together:
- Each mission in `/campaigns/{campaign}/missions/` contains its own fiction text files directly
- UI components in `/features/ui/` display fiction content with appropriate styling from `/features/ui/_shared/themes/`
- Audio assets in mission-specific directories synchronize with fiction reading

### Common Shared Assets
Following the "Global Litmus Test" principle for assets that belong in global directories:
- Standard formatting and styling for consistent presentation from `/features/ui/_shared/themes/`
- Common character names and terminology across all fiction texts
- Standard UI components for text display and navigation from `/features/ui/_shared/components/`
- Shared presentation templates for different text types from `/features/ui/templates/`
- Common BBCode conversion utilities in `/scripts/utilities/text_formatter.gd`

This structure follows the hybrid approach where narrative content is co-located with mission scenes in campaign directories following the campaign-centric principle as defined in the directory structure, while UI components that display fiction are organized within feature directories following the co-location principle. The structure maintains clear separation of concerns between different text types while ensuring easy access to all text resources needed for game features, and aligns with the actual fiction file references documented in the asset mappings.