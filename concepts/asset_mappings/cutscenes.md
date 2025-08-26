# Cutscenes Asset Mapping

## Overview
This document maps the cutscene definitions from cutscenes.tbl and their references in campaign (.fc2) and mission (.fs2) files to their corresponding audio assets in the Wing Commander Saga Hermes campaign, organized according to the Godot feature-based directory structure.

## Asset Types

### Cutscene Definitions (.tbl)
Cutscene definition table (cutscenes.tbl) defines different cutscenes:
- Cutscene name and description
- Audio file reference (.ogg)
- CD location reference
- Narrative context and purpose

Common cutscene types:
- Campaign Intro Cutscenes (campaign introduction sequences)
- Campaign End Cutscenes (campaign conclusion sequences)
- Campaign Credits Cutscenes (campaign credits sequences)
- Mission Briefing Cutscenes (pre-mission narrative sequences)
- Mission Debriefing Cutscenes (post-mission narrative sequences)
- Episode Outro Cutscenes (episode conclusion sequences)

### Audio Assets (.ogg)
Cutscene audio assets are organized in two separate directories:
- hermes_movies/ - Contains main campaign cutscene audio files
- hermes_movies_prologue/ - Contains prologue campaign cutscene audio files

Confirmed audio files include:
Campaign Introduction:
- intro.ogg - Main game introduction
- prologue_intro.ogg - Prologue campaign introduction
- hermes_intro.ogg - Hermes campaign introduction

Campaign Conclusion/Credits:
- prologue_outro.ogg - Prologue campaign conclusion
- episode_XX_outro.ogg - Episode conclusion sequences (one per episode)
- hermes_outro.ogg - Hermes campaign conclusion
- hermes_credits.ogg - Hermes campaign credits sequence

Mission Briefing Sequences:
- episode_01_briefing_XX.ogg - Episode 1 briefing sequences
- episode_02_briefing_XX.ogg - Episode 2 briefing sequences
- episode_03_briefing_XX.ogg - Episode 3 briefing sequences
- episode_04_briefing_XX.ogg - Episode 4 briefing sequences
- episode_05_briefing_XX.ogg - Episode 5 briefing sequences
- episode_06_briefing_XX.ogg - Episode 6 briefing sequences
- episode_07_briefing_XX.ogg - Episode 7 briefing sequences
- prologue_briefing_XX.ogg - Prologue briefing sequences

Audio effect properties:
- Volume levels for narrative clarity
- Music and dialogue mixing
- Looping properties for sustained sequences
- Fade in/out properties for smooth transitions

## Target Structure
Following the Godot project structure defined in directory_structure.md, cutscene assets are organized as follows:

### Campaigns Directory Structure
Campaign-related cutscene content is organized within the `/campaigns/` directory, following the feature-based organization principle where all files related to a single campaign are grouped together.

```
campaigns/
├── hermes/                          # Hermes campaign (main campaign)
│   ├── campaign.tres                # Campaign definition
│   ├── cutscenes/                   # Campaign cutscene definitions
│   │   ├── intro.tres               # Campaign intro cutscene definition
│   │   ├── outro.tres               # Campaign outro cutscene definition
│   │   └── credits.tres             # Campaign credits cutscene definition
│   └── missions/                    # Mission scenes
│       ├── m01_hermes/              # Mission 1
│       │   ├── briefing_cutscene.tres  # Briefing cutscene definition
│       │   └── mission.tscn         # Main mission scene
│       └── ...                      # Additional missions
├── prologue/                        # Prologue campaign
│   ├── campaign.tres                # Campaign definition
│   ├── cutscenes/                   # Campaign cutscene definitions
│   │   ├── intro.tres               # Campaign intro cutscene definition
│   │   └── outro.tres               # Campaign outro cutscene definition
│   └── missions/                    # Mission scenes
│       ├── demo_01_prologue/        # Demo Mission 1
│       │   ├── briefing_cutscene.tres  # Briefing cutscene definition
│       │   └── mission.tscn         # Main mission scene
│       └── ...                      # Additional missions
```

### Assets Directory Structure
Audio assets for cutscenes are stored in the global `/assets/` directory, following the "Global Litmus Test" principle since these are context-agnostic audio files that would still be needed even if specific missions were removed.

```
assets/
├── audio/                           # Shared audio files
│   └── cutscenes/                   # Cutscene audio
│       ├── hermes/                  # Main Hermes campaign audio
│       │   ├── intro.ogg            # Main campaign intro
│       │   ├── outro.ogg            # Main campaign outro
│       │   ├── credits.ogg          # Main campaign credits
│       │   └── episodes/            # Episode-specific audio
│       │       ├── episode_01/      # Episode 1 audio
│       │       │   ├── briefing_01.ogg  # Mission briefing segment
│       │       │   ├── briefing_02.ogg  # Mission briefing segment
│       │       │   └── outro.ogg    # Episode outro
│       │       └── ...              # Additional episodes
│       └── prologue/                # Prologue campaign audio
│           ├── intro.ogg            # Prologue intro
│           ├── outro.ogg            # Prologue outro
│           └── briefing_01.ogg      # Prologue briefing segment
```

## Actual File References
Based on scanning all FC2, FS2, and TBL files in the source assets and examining the actual movie directories, these are the confirmed cutscene references:

### Cutscenes.tbl Definitions
- intro.ogg - Introduction
- prologue_intro.ogg - Reporting Aboard
- prologue_outro.ogg - The Beginning in the End
- hermes_intro.ogg - Hit the Ground Running
- episode_01_outro.ogg - The Bombardment of Vega Prime
- episode_02_outro.ogg - Kinney Memorial Service
- episode_03_outro.ogg - Hiding a Behemoth
- episode_04_outro.ogg - The Behemoth Disaster
- episode_05_outro.ogg - Force Multiplier
- episode_06_outro.ogg - The Fleet
- hermes_outro.ogg - The Treaty of Torgo
- hermes_credits.ogg - Credits

### Campaign File References
- codename_hermes.fc2 references:
  - hermes_intro.ogg (Campaign Intro Cutscene)
  - hermes_credits.ogg (Campaign End Cutscene)
- prologue.fc2 references:
  - prologue_intro.ogg (Campaign Intro Cutscene)
  - prologue_outro.ogg (Campaign End Cutscene)

### Mission File References (Sample)
- M01-BG-Hermes.fs2 references:
  - episode_01_briefing_01.ogg (Briefing Cutscene)
- M50-BG-Hermes.fs2 references:
  - episode_07_briefing_08.ogg (Briefing Cutscene)
  - hermes_outro.ogg (Debriefing Cutscene)

The actual audio files are stored in:
- /home/fuchsst/projects/personal/wcsaga_godot_converter/source_assets/wcs_hermes_campaign/hermes_movies/
- /home/fuchsst/projects/personal/wcsaga_godot_converter/source_assets/wcs_hermes_campaign/hermes_movies_prologue/

No other cutscene file references were found in any TBL or FS2 files beyond those listed above.