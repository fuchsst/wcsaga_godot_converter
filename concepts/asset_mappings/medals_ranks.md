# Medals and Ranks Asset Mapping

## Overview
This document maps the medal and rank definitions from medals.tbl and rank.tbl to their corresponding visual and textual assets in the Wing Commander Saga Hermes campaign, organized according to the Godot feature-based directory structure.

## Asset Types

### Medal Definitions (.tbl)
Medals.tbl defines military decorations and awards:
- Campaign medals
- Service medals
- Achievement medals
- Valor medals
- Special commendations

Each medal entry contains:
- Medal name
- Visual representation references (bitmap)
- Number of modifications/variations

Common medal types from the TBL file:
- Bronze Star - Basic service recognition
- Silver Star - Meritorious achievement
- Gold Star - Exceptional valor
- Starburst - Special commendation
- Flying Cross - Aerial achievement
- Distinguished Service Medal - Outstanding leadership
- Legion of Honor - Highest military honor
- Purple Heart - Wounded in action
- Air Medal - Combat flight excellence
- Navy Cross - Naval heroism
- Congressional Medal of Honor - Ultimate sacrifice/heroism
- Special commendations for specific actions

### Rank Definitions (.tbl)
Rank.tbl defines military rank structure:
- Enlisted ranks
- Commissioned officer ranks
- Flag officer ranks

Each rank entry contains:
- Rank title and abbreviation
- Rank insignia references (bitmap)
- Promotion requirements (points)
- Promotion voice references
- Promotion text

### Visual Assets (.dds/.pcx/.png)
Medal and rank visual representations:
- Medal icons and images
- Rank insignia graphics
- UI display elements for medals/ranks
- Debriefing screen representations

### Audio Assets (.wav)
Sound effects for ranks:
- Rank promotion announcement sounds
- Voice announcements for promotions

## Format Conversion Process

### Legacy Formats to Godot Formats

**DDS Files (.dds)**
- Legacy DirectDraw Surface texture format with compression
- Will be converted to WebP format for Godot compatibility
- Mipmaps and compression settings preserved where appropriate

**PCX Files (.pcx)**
- Legacy image format for older textures
- Will be converted to WebP format
- Used primarily for interface elements and some legacy textures

**WAV Files (.wav)**
- Legacy audio format for sound effects
- Will be converted to Ogg Vorbis format for Godot compatibility
- Audio quality and characteristics preserved

## Target Structure
Following the Godot project structure defined in directory_structure.md, medal and rank assets are organized as follows:

### Features Directory Structure
Medal and rank features are organized within the `/features/ui/` directory, following the feature-based organization principle where each UI component is a self-contained entity with all its related assets.

```
features/
├── ui/                             # UI feature elements
│   ├── medals_display/             # Medals display system
│   │   ├── medals_display.tscn     # Main medals display scene
│   │   ├── medals_display.gd       # Medals display controller script
│   │   ├── medals_data.tres        # Medals data resource (converted from medals.tbl)
│   │   └── assets/                 # Feature-specific assets
│   │       ├── icons/              # Medal icons (converted from DDS/PCX)
│   │       │   ├── bronze_star.webp
│   │       │   ├── silver_star.webp
│   │       │   ├── gold_star.webp
│   │       │   └── ...             # Additional medal icons
│   │       └── sounds/             # Medal-related sounds
│   │           └── achievement_unlock.ogg
│   ├── rank_display/               # Rank display system
│   │   ├── rank_display.tscn       # Main rank display scene
│   │   ├── rank_display.gd         # Rank display controller script
│   │   ├── rank_data.tres          # Rank data resource (converted from rank.tbl)
│   │   └── assets/                 # Feature-specific assets
│   │       ├── insignia/           # Rank insignia (converted from DDS/PCX)
│   │       │   ├── rank0.webp      # 2nd Lieutenant
│   │       │   ├── rank1.webp      # 1st Lieutenant
│   │       │   ├── rank2.webp      # Captain
│   │       │   └── ...             # Additional rank insignia
│   │       └── sounds/             # Rank-related sounds
│   │           └── promotion.ogg   # Promotion ceremony sound
│   └── _shared/                    # Shared UI assets
│       ├── fonts/                  # UI fonts
│       ├── icons/                  # Generic UI icons
│       ├── themes/                 # UI themes
│       └── components/             # Reusable UI components
└── templates/                      # Feature templates
```

### Assets Directory Structure
Generic UI assets that are shared across multiple UI components are organized in the global `/assets/` directory, following the "Global Litmus Test" principle.

```
assets/
├── audio/                          # Shared audio files
│   ├── sfx/                        # Generic sound effects
│   │   └── ui/                     # UI sound effects
│   │       ├── medal_earned.ogg
│   │       └── rank_promoted.ogg
│   └── music/                      # Background music tracks
├── textures/                       # Shared texture files
│   └── ui/                         # Generic UI elements
│       ├── medals/                 # Generic medal elements
│       └── ranks/                  # Generic rank elements
└── data/                           # Shared data resources
    └── ui/                         # UI data resources
        ├── medal_criteria.tres     # Medal award criteria data
        └── rank_requirements.tres # Rank promotion requirements
```

### Campaigns Directory Structure
Campaign-specific medal and rank progression data is organized in the `/campaigns/` directory.

```
campaigns/
├── hermes/                         # Hermes campaign
│   ├── pilot_data.tres             # Pilot progression data including medals/ranks
│   └── missions/                   # Mission scenes
│       ├── m01_hermes/             # Mission 1
│       │   └── pilot_progression.tres # Mission-specific pilot progression
│       └── ...                     # Additional missions
└── ...                             # Other campaigns
```

## Example Mapping
For Bronze Star Medal:
- medals.tbl entry → /features/ui/medals_display/medals_data.tres (BronzeStar definition)
- medal_bronze_star.dds → /features/ui/medals_display/assets/icons/bronze_star.webp
- Related debriefing assets (2_medal_bronze_stara.dds, etc.) → /features/ui/medals_display/assets/icons/bronze_star.webp

For 2nd Lieutenant Rank:
- rank.tbl entry → /features/ui/rank_display/rank_data.tres (2ndLieutenant definition)
- rank0.dds → /features/ui/rank_display/assets/insignia/rank0.webp
- bump.wav → /features/ui/rank_display/assets/sounds/promotion.ogg

## Conversion Pipeline
1. **TBL Parser**: Custom parser to extract medal and rank definitions from .tbl files
2. **DDS/PCX Converter**: Convert DDS and PCX textures to WebP format maintaining visual quality
3. **WAV Converter**: Convert WAV audio to Ogg Vorbis format
4. **Resource Generator**: Create Godot .tres files with converted medal and rank data
5. **Scene Builder**: Generate Godot scenes (.tscn) for medal/rank display UI components
6. **Validation**: Verify converted assets match original appearance and functionality

## Relationship to Other Assets
Medals and ranks are closely related to:
- **Campaign Progression**: Stored in `/campaigns/{campaign}/pilot_data.tres` for tracking earned medals and current rank
- **UI System**: Integrated into `/features/ui/debriefing/` for displaying earned medals after missions
- **Audio System**: Use shared UI sounds from `/assets/audio/sfx/ui/` for medal/rank notifications
- **Text System**: Promotion text and medal descriptions are integrated with briefing/debriefing systems