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
Fiction text files are organized within campaign directories following the campaign-centric mission organization principle:

```
campaigns/
├── hermes/                          # Hermes campaign (main campaign)
│   ├── campaign.tres                # Campaign definition
│   ├── fiction/                     # Campaign fiction directory
│   │   └── missions/                # Mission-specific fiction
│   │       └── m01/                 # Mission 1 fiction
│   │           └── m1fiction.txt    # Mission 1 fiction text (converted from source)
│   └── missions/                    # Mission scenes
│       └── m01_hermes/              # Mission 1
│           ├── fiction.txt          # Fiction text (reference to m1fiction.txt)
│           └── mission.tscn         # Main mission scene
├── prologue/                        # Prologue campaign (demo missions)
│   ├── campaign.tres                # Campaign definition
│   ├── fiction/                     # Campaign fiction directory
│   │   ├── disc_01/                 # Disc 1 fiction
│   │   │   └── d1fiction.txt        # Disc 1 fiction text (converted from source)
│   │   ├── disc_02/                 # Disc 2 fiction
│   │   │   └── d2fiction.txt        # Disc 2 fiction text (converted from source)
│   │   ├── disc_03/                 # Disc 3 fiction
│   │   │   └── d3fiction.txt        # Disc 3 fiction text (converted from source)
│   │   ├── disc_04/                 # Disc 4 fiction
│   │   │   └── d4fiction.txt        # Disc 4 fiction text (converted from source)
│   │   └── disc_05/                 # Disc 5 fiction
│   │       └── d5fiction.txt        # Disc 5 fiction text (converted from source)
│   └── missions/                    # Mission scenes
│       ├── demo_01_prologue/        # Demo Mission 1
│       │   ├── fiction.txt          # Fiction text (reference to d1fiction.txt)
│       │   └── mission.tscn         # Main mission scene
│       ├── demo_02_prologue/        # Demo Mission 2
│       │   ├── fiction.txt          # Fiction text (reference to d2fiction.txt)
│       │   └── mission.tscn         # Main mission scene
│       ├── demo_03_prologue/        # Demo Mission 3
│       │   ├── fiction.txt          # Fiction text (reference to d3fiction.txt)
│       │   └── mission.tscn         # Main mission scene
│       ├── demo_04_prologue/        # Demo Mission 4
│       │   ├── fiction.txt          # Fiction text (reference to d4fiction.txt)
│       │   └── mission.tscn         # Main mission scene
│       └── demo_05_prologue/        # Demo Mission 5
│           ├── fiction.txt          # Fiction text (reference to d5fiction.txt)
│           └── mission.tscn         # Main mission scene
```

### Features Directory Structure
UI components that display fiction content are organized within feature directories following the co-location principle:

```
features/
├── ui/                              # UI feature elements
│   ├── briefing/                    # Briefing interface
│   │   ├── briefing_screen.tscn     # Main briefing scene
│   │   ├── briefing_screen.gd       # Briefing controller script
│   │   └── assets/                  # Feature-specific assets
│   │       └── text/                # Briefing text resources
│   ├── debriefing/                  # Debriefing interface
│   │   ├── debriefing_screen.tscn   # Main debriefing scene
│   │   ├── debriefing_screen.gd     # Debriefing controller script
│   │   └── assets/                  # Feature-specific assets
│   │       └── text/                # Debriefing text resources
│   ├── tech_database/               # Technical database (includes fiction viewer)
│   │   ├── tech_database.tscn       # Main tech database scene
│   │   ├── tech_database.gd         # Tech database controller script
│   │   └── assets/                  # Feature-specific assets
│   │       └── text/                # Tech database text resources
│   └── _shared/                     # Shared UI assets
│       └── text/                    # Shared text resources and formatting templates
└── templates/                       # Feature templates
```

## Integration Points

### Data Converter Output Mapping
- Mission fiction files (d1fiction.txt, m1fiction.txt, etc.) → Converted to BBCode and placed in appropriate campaign fiction directories:
  - Prologue campaign fiction → `/campaigns/prologue/fiction/disc_{number}/{filename}.txt`
  - Hermes campaign fiction → `/campaigns/hermes/fiction/missions/{mission_id}/{filename}.txt`
- Mission scenes reference fiction → Mission-specific fiction references in `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/fiction.txt`

### Resource References
- **Mission scenes** in `/campaigns/{campaign}/missions/` reference fiction text from their campaign directories
- **Briefing screens** in `/features/ui/briefing/` display mission-specific fiction content
- **Tech database** in `/features/ui/tech_database/` may reference narrative elements for context
- **Fiction viewer** in `/features/ui/tech_database/` displays longer narrative content

## Relationship to Other Assets

### UI Integration
Text files integrate with UI components in `/features/ui/` directories following the feature-based organization:
- `/features/ui/briefing/` - Briefing screen fiction display for mission context
- `/features/ui/debriefing/` - Debriefing screen mission results and follow-up
- `/features/ui/tech_database/` - Technical database with fiction viewer component
- `/features/ui/main_menu/` - Main menu campaign selection with narrative context

### Mission Integration
Text files integrate with mission scenes in `/campaigns/` directories following the campaign-centric organization:
- `/campaigns/prologue/fiction/disc_{number}/d{number}fiction.txt` - Prologue campaign fiction
- `/campaigns/hermes/fiction/missions/m01/m1fiction.txt` - Hermes campaign mission fiction
- `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/fiction.txt` - Symbolic links or references to campaign fiction
- `/campaigns/{campaign}/campaign.tres` - Campaign overview with references to fiction content

### System Integration
Text files integrate with Godot systems following the separation of concerns:
- `/autoload/audio_manager.gd` - Synchronized voice acting with fiction reading
- `/scripts/ui/briefing_system.gd` - Briefing presentation logic for fiction display
- `/scripts/mission/campaign_progression.gd` - Campaign progression with fiction unlocking
- `/features/ui/tech_database/tech_database.gd` - Tech database controller with fiction viewer

### Closely Related Assets
Based on the asset mapping documentation and source file analysis:
- Mission files (.fs2) that reference specific fiction entries (Demo-01-BG-Hermes.fs2 references d1fiction.txt, M01-BG-Hermes.fs2 references m1fiction.txt)
- Briefing screens that display fiction content from `/features/ui/briefing/`
- Voice acting files that accompany fiction reading from `/assets/audio/voice/mission_briefings/`
- Campaign files (.fc2) that define campaign structure and fiction progression

### Entity Asset Organization
Following the co-location principle where all files related to a single feature are grouped together:
- Each mission in `/campaigns/{campaign}/missions/` references its fiction from the campaign fiction directory
- UI components in `/features/ui/` display fiction content with appropriate styling from `/features/ui/_shared/themes/`
- Audio assets in `/assets/audio/voice/mission_briefings/` synchronize with fiction reading

### Common Shared Assets
Following the "Global Litmus Test" principle for assets that belong in global directories:
- Standard formatting and styling for consistent presentation from `/features/ui/_shared/themes/`
- Common character names and terminology across all fiction texts
- Standard UI components for text display and navigation from `/features/ui/_shared/components/`
- Shared presentation templates for different text types from `/features/ui/templates/`
- Common BBCode conversion utilities in `/scripts/utilities/text_formatter.gd`

This structure follows the hybrid approach where narrative content is organized in campaign directories following the campaign-centric principle as defined in the directory structure, while UI components that display fiction are organized within feature directories following the co-location principle. The structure maintains clear separation of concerns between different text types while ensuring easy access to all text resources needed for game features, and aligns with the actual fiction file references documented in the asset mappings.