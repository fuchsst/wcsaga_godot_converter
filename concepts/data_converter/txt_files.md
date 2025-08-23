# TXT Files Conversion Requirements

## Overview
TXT files contain narrative fiction, mission briefings, and technical database entries in Wing Commander Saga. These text files need to be converted to Godot's rich text format while preserving their formatting and presentation style, following Godot's feature-based organization principles.

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

### Technical Database Entries
**Purpose**: Ship and weapon specifications
**Source Format**: Plain text with structured data
**Target Format**: Structured text resources with formatting
**Conversion Requirements**:
- Parse technical specifications and properties
- Convert to structured data format
- Maintain consistent presentation style
- Handle cross-references to other entries
- Generate searchable metadata

### Credits and Documentation
**Purpose**: Game credits and technical documentation
**Source Format**: Plain text with simple formatting
**Target Format**: Scrollable text resources
**Conversion Requirements**:
- Preserve original text content and structure
- Convert to scrollable presentation format
- Handle long text sections efficiently
- Maintain consistent font and styling
- Generate appropriate layout properties

### Campaign Storyline
**Purpose**: Overarching campaign narrative
**Source Format**: Plain text with chapter divisions
**Target Format**: Navigable text resources with chapter structure
**Conversion Requirements**:
- Parse chapter and section divisions
- Convert to navigable text structure
- Maintain story progression and flow
- Handle character development notes
- Generate table of contents and navigation

## Conversion Process

### 1. Format Analysis Phase
- Identify text file type and purpose
- Parse custom formatting codes and markup
- Extract structural elements (chapters, sections)
- Identify character names and dialogue
- Check for cross-references and links

### 2. Content Conversion Phase
- Convert custom markup to BBCode
- Preserve text content and meaning
- Handle special characters and symbols
- Maintain paragraph and line structure
- Generate appropriate formatting hierarchy

### 3. Structuring Phase
- Create structured text resources
- Generate navigation and indexing data
- Handle cross-references and links
- Create metadata for search and filtering
- Organize into appropriate categories

### 4. Integration Phase
- Integrate with Godot's text display systems
- Generate UI layouts for presentation
- Handle scrolling and navigation controls
- Create search and filtering capabilities
- Validate content presentation and readability

## Feature-Based Directory Structure
Following Godot's recommended directory structure:
```
/text/
├── fiction/               # Narrative fiction
│   ├── hermes/            # Hermes campaign fiction
│   │   ├── m01_fiction.txt
│   │   ├── m02_fiction.txt
│   │   └── campaign_overview.txt
│   ├── brimstone/         # Brimstone campaign fiction
│   │   ├── m01_fiction.txt
│   │   ├── m02_fiction.txt
│   │   └── campaign_overview.txt
│   └── training/          # Training mission fiction
│       ├── intro_fiction.txt
│       └── advanced_fiction.txt
├── technical/             # Technical database entries
│   ├── ships/             # Ship specifications
│   │   ├── terran/
│   │   ├── kilrathi/
│   │   └── pirate/
│   ├── weapons/           # Weapon specifications
│   │   ├── terran/
│   │   ├── kilrathi/
│   │   └── pirate/
│   └── systems/           # System specifications
│       ├── engines/
│       ├── shields/
│       └── weapons/
├── credits/               # Game credits
│   ├── development.txt
│   ├── art.txt
│   ├── audio.txt
│   └── special_thanks.txt
└── documentation/         # Technical documentation
    ├── gameplay.txt
    ├── controls.txt
    └── faq.txt
```

## UI Integration
Text files integrate with UI components in `/ui/` directories:
- `/ui/briefing/` - Briefing screen fiction display
- `/ui/debriefing/` - Debriefing screen mission results
- `/ui/tech_database/` - Technical database entry display
- `/ui/credits/` - Credits screen scrolling text
- `/ui/documentation/` - Documentation viewer

## Mission Integration
Text files integrate with mission scenes in `/missions/` directories:
- `/missions/{campaign}/{mission}/fiction.txt` - Mission-specific fiction
- `/missions/{campaign}/{mission}/briefing.txt` - Mission briefing text
- `/missions/{campaign}/campaign.tres` - Campaign overview text

## System Integration
Text files integrate with Godot systems in `/systems/` directories:
- `/systems/mission_control/` - Mission briefing text
- `/systems/audio/` - Synchronized voice acting text
- `/systems/ui/` - UI text display components

## Closely Related Assets
- Mission files (.fs2) that reference specific fiction entries and are converted to `/missions/` directories
- Briefing screens that display fiction content from `/ui/briefing/`
- Tech database UI that presents technical entries from `/ui/tech_database/`
- Voice acting files that accompany fiction reading from `/audio/voice/`

## Entity Asset Organization
Each entity in `/entities/` may reference relevant text data:
- Ship entities reference technical specifications from `/text/technical/ships/`
- Weapon entities reference technical specifications from `/text/technical/weapons/`
- Effect entities may reference technical descriptions from `/text/technical/systems/`

## Common Shared Assets
- Standard formatting and styling for consistent presentation from `/ui/themes/`
- Common character names and terminology across all fiction texts
- Shared technical specifications and descriptions in `/text/technical/`
- Standard UI components for text display and navigation from `/ui/components/`
- Common presentation templates for different text types from `/ui/templates/`
- Shared glossary and terminology definitions for consistent references