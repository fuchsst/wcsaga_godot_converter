# Campaigns and Fiction Asset Mapping

## Overview
This document maps the campaign definitions and fiction text from various TBL and TXT files to their corresponding narrative assets in the Wing Commander Saga Hermes campaign, organized according to the Godot feature-based directory structure as defined in directory_structure.md and Godot_Project_Structure_Refinement.md.

## Asset Types

### Campaign Definitions (.tbl)
Campaign definition files reference mission sequences and overarching story elements:
- Campaign structure and mission ordering
- Campaign-specific briefing/fiction text
- Campaign-specific UI elements
- Campaign-specific music tracks
- Campaign-specific voice acting
- Campaign-specific cutscenes

### Fiction Text (.txt)
Narrative text files contain the story elements:
- d1fiction.txt - Disc 1 fiction text (Prologue campaign)
- d2fiction.txt - Disc 2 fiction text (Prologue campaign)
- d3fiction.txt - Disc 3 fiction text (Prologue campaign)
- d4fiction.txt - Disc 4 fiction text (Prologue campaign)
- d5fiction.txt - Disc 5 fiction text (Prologue campaign)
- m1fiction.txt - Mission 1 fiction text (Hermes campaign)

Fiction text content includes:
- Mission background and context
- Character development and relationships
- Political and military situation
- Historical references and lore
- Technical exposition
- Emotional and dramatic elements
- Plot advancement and revelations

### Briefing Text (.txt)
Mission briefing files contain tactical information:
- Mission objectives and goals
- Enemy force composition
- Strategic importance of mission
- Intelligence updates
- Equipment and loadout information
- Tactical recommendations
- Potential complications
- Contingency plans

### Cutscene Scripts (.txt/.tbl)
Cutscene definition files contain:
- Dialogue scripts for characters
- Scene direction and staging
- Camera movement instructions
- Timing and synchronization data
- Special effects triggers
- Audio cue points
- Character entrance/exit timing
- Emotion and performance notes

### Voice Acting (.wav/.ogg)
Narrative voice files:
- Character dialogue recordings
- Narrator storytelling
- Mission briefing voice
- Cutscene dialogue
- Radio communication
- Command announcements
- Pilot chatter
- News broadcasts

### Music Tracks (.ogg)
Narrative music files:
- Dramatic underscore for fiction scenes
- Atmospheric ambient music
- Emotional character themes
- Epic action music
- Somber reflective pieces
- Tense suspense tracks
- Triumphant victory themes
- Tragic loss compositions

## Target Structure
Following the Godot project structure defined in directory_structure.md, campaign fiction assets are organized as follows:

### Campaigns Directory Structure
Campaign-related narrative content is organized within the `/campaigns/` directory, which separates reusable game mechanics (in `/features/`) from specific content that uses those mechanics.

```
campaigns/
├── hermes/                          # Hermes campaign (main campaign)
│   ├── campaign.tres                # Campaign definition
│   ├── fiction/                     # Campaign fiction directory
│   │   └── missions/                # Mission-specific fiction
│   │       └── m01/                 # Mission 1 fiction
│   │           └── m1fiction.txt    # Mission 1 fiction text
│   └── missions/                    # Mission scenes
│       └── m01_hermes/              # Mission 1
│           ├── fiction.txt          # Fiction text (reference to m1fiction.txt)
│           └── mission.tscn         # Main mission scene
├── prologue/                        # Prologue campaign (demo missions)
│   ├── campaign.tres                # Campaign definition
│   ├── fiction/                     # Campaign fiction directory
│   │   ├── disc_01/                 # Disc 1 fiction
│   │   │   └── d1fiction.txt        # Disc 1 fiction text
│   │   ├── disc_02/                 # Disc 2 fiction
│   │   │   └── d2fiction.txt        # Disc 2 fiction text
│   │   ├── disc_03/                 # Disc 3 fiction
│   │   │   └── d3fiction.txt        # Disc 3 fiction text
│   │   ├── disc_04/                 # Disc 4 fiction
│   │   │   └── d4fiction.txt        # Disc 4 fiction text
│   │   └── disc_05/                 # Disc 5 fiction
│   │       └── d5fiction.txt        # Disc 5 fiction text
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

## Actual File References
Based on scanning all FS2 and TBL files in the source assets, these are the ONLY confirmed references to fiction text files:

### Prologue Campaign (Demo Missions)
- Demo-01-BG-Hermes.fs2 references: d1fiction.txt
- Demo-02-BG-Hermes.fs2 references: d2fiction.txt
- Demo-03-BG-Hermes.fs2 references: d3fiction.txt
- Demo-04-BG-Hermes.fs2 references: d4fiction.txt
- Demo-05-BG-Hermes.fs2 references: d5fiction.txt

### Hermes Campaign
- M01-BG-Hermes.fs2 references: m1fiction.txt

No other fiction text file references were found in any TBL or FS2 files.