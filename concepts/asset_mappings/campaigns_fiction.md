# Campaigns and Fiction Asset Mapping

## Overview
This document maps the campaign definitions and fiction text from various TBL and TXT files to their corresponding narrative assets in the Wing Commander Saga Hermes campaign.

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
- d1fiction.txt - Disc 1 fiction text
- d2fiction.txt - Disc 2 fiction text
- d3fiction.txt - Disc 3 fiction text
- d4fiction.txt - Disc 4 fiction text
- d5fiction.txt - Disc 5 fiction text
- m1fiction.txt - Mission 1 fiction text
- m2fiction.txt - Mission 2 fiction text
- And so on for each mission...

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
```
/data/campaigns/                     # Campaign data definitions
├── hermes/                          # Hermes campaign data
│   ├── campaign.tres                # Campaign definition
│   ├── missions/                    # Mission sequence
│   │   ├── m01.tres                 # Mission 1 definition
│   │   ├── m02.tres                 # Mission 2 definition
│   │   ├── m03.tres                 # Mission 3 definition
│   │   └── ...                      # Additional missions
│   ├── characters/                  # Character definitions
│   │   ├── moran.tres               # Captain Moran definition
│   │   ├── sandman.tres             # Sandman definition
│   │   ├── honeybear.tres           # Honeybear definition
│   │   └── ...                      # Additional characters
│   ├── factions/                    # Faction definitions
│   │   ├── terran.tres              # Terran Confederation
│   │   ├── kilrathi.tres            # Kilrathi Empire
│   │   └── pirate.tres              # Pirate factions
│   └── story/                       # Story progression data
│       ├── arcs.tres                # Story arc definitions
│       ├── chapters.tres            # Chapter definitions
│       └── plot_points.tres         # Key plot points

/campaigns/hermes/fiction/           # Campaign fiction directory
├── disc_01/                         # Disc 1 fiction
│   ├── d1fiction.txt                # Disc 1 fiction text
│   ├── characters/                  # Character introductions
│   ├── setting/                     # Setting descriptions
│   └── background/                  # Background information
├── disc_02/                         # Disc 2 fiction
│   ├── d2fiction.txt                # Disc 2 fiction text
│   ├── characters/                  # Character development
│   ├── conflicts/                   # Conflict escalation
│   └── revelations/                 # Plot reveals
├── disc_03/                         # Disc 3 fiction
│   ├── d3fiction.txt                # Disc 3 fiction text
│   ├── characters/                  # Character arcs
│   ├── politics/                    # Political intrigue
│   └── battles/                     # Battle descriptions
├── disc_04/                         # Disc 4 fiction
│   ├── d4fiction.txt                # Disc 4 fiction text
│   ├── characters/                  # Character climax
│   ├── turning_points/              # Story turning points
│   └── revelations/                 # Major reveals
├── disc_05/                         # Disc 5 fiction
│   ├── d5fiction.txt                # Disc 5 fiction text
│   ├── characters/                  # Character resolutions
│   ├── conclusion/                  # Story conclusion
│   └── aftermath/                   # Post-conflict aftermath
├── missions/                        # Mission-specific fiction
│   ├── m01/                         # Mission 1 fiction
│   │   ├── m1fiction.txt            # Mission 1 fiction text
│   │   ├── background.txt           # Mission background
│   │   ├── objectives.txt           # Mission objectives
│   │   └── outcome.txt              # Expected outcomes
│   ├── m02/                         # Mission 2 fiction
│   │   ├── m2fiction.txt            # Mission 2 fiction text
│   │   ├── background.txt           # Mission background
│   │   ├── objectives.txt           # Mission objectives
│   │   └── outcome.txt              # Expected outcomes
│   └── ...                          # Additional missions
└── characters/                      # Character-specific fiction
    ├── moran/                       # Captain Moran stories
    ├── sandman/                     # Sandman stories
    ├── honeybear/                   # Honeybear stories
    └── ...                          # Additional characters

/campaigns/hermes/briefing/          # Campaign briefing directory
├── missions/                        # Mission briefings
│   ├── m01/                         # Mission 1 briefing
│   │   ├── objectives.txt           # Mission objectives
│   │   ├── intel.txt                # Intelligence briefing
│   │   ├── tactics.txt              # Tactical advice
│   │   └── contingencies.txt        # Contingency plans
│   ├── m02/                         # Mission 2 briefing
│   │   ├── objectives.txt           # Mission objectives
│   │   ├── intel.txt                # Intelligence briefing
│   │   ├── tactics.txt              # Tactical advice
│   │   └── contingencies.txt        # Contingency plans
│   └── ...                          # Additional missions
└── campaigns/                       # Campaign briefings
    ├── disc_01/                     # Disc 1 briefing
    ├── disc_02/                     # Disc 2 briefing
    ├── disc_03/                     # Disc 3 briefing
    ├── disc_04/                     # Disc 4 briefing
    └── disc_05/                     # Disc 5 briefing

/audio/voice/fiction/                # Fiction voice acting directory
├── hermes/                          # Hermes campaign voices
│   ├── narrator/                    # Narrator voice
│   │   ├── disc_01/                 # Disc 1 narration
│   │   ├── disc_02/                 # Disc 2 narration
│   │   ├── disc_03/                 # Disc 3 narration
│   │   ├── disc_04/                 # Disc 4 narration
│   │   └── disc_05/                 # Disc 5 narration
│   ├── characters/                  # Character voices
│   │   ├── moran/                   # Captain Moran voice
│   │   │   ├── lines/
│   │   │   ├── emotional/
│   │   │   └── command/
│   │   ├── sandman/                 # Sandman voice
│   │   │   ├── lines/
│   │   │   ├── emotional/
│   │   │   └── tactical/
│   │   ├── honeybear/               # Honeybear voice
│   │   │   ├── lines/
│   │   │   ├── emotional/
│   │   │   └── technical/
│   │   └── ...                      # Additional characters
│   ├── missions/                    # Mission-specific voices
│   │   ├── m01/                     # Mission 1 voices
│   │   ├── m02/                     # Mission 2 voices
│   │   └── ...                      # Additional missions
│   └── cutscenes/                   # Cutscene voices
│       ├── intro/                   # Intro cutscene voices
│       ├── mission/                 # In-mission cutscene voices
│       └── outro/                   # Outro cutscene voices

/audio/music/fiction/                # Fiction music directory
├── hermes/                          # Hermes campaign music
│   ├── themes/                      # Character and faction themes
│   │   ├── moran_theme.ogg          # Captain Moran theme
│   │   ├── sandman_theme.ogg        # Sandman theme
│   │   ├── honeybear_theme.ogg      # Honeybear theme
│   │   ├── terran_theme.ogg         # Terran Confederation theme
│   │   ├── kilrathi_theme.ogg       # Kilrathi Empire theme
│   │   └── pirate_theme.ogg         # Pirate faction theme
│   ├── moods/                       # Mood-specific music
│   │   ├── dramatic.ogg             # Dramatic moments
│   │   ├── suspenseful.ogg          # Suspenseful moments
│   │   ├── triumphant.ogg           # Triumphant moments
│   │   ├── somber.ogg               # Somber moments
│   │   ├── mysterious.ogg           # Mysterious moments
│   │   ├── action.ogg               # Action sequences
│   │   └── romantic.ogg             # Romantic moments
│   ├── campaigns/                   # Campaign-specific music
│   │   ├── disc_01/                 # Disc 1 music
│   │   ├── disc_02/                 # Disc 2 music
│   │   ├── disc_03/                 # Disc 3 music
│   │   ├── disc_04/                 # Disc 4 music
│   │   └── disc_05/                 # Disc 5 music
│   └── missions/                    # Mission-specific music
│       ├── m01/                     # Mission 1 music
│       ├── m02/                     # Mission 2 music
│       └── ...                      # Additional missions

/animations/cutscenes/               # Cutscene animations directory
├── hermes/                          # Hermes campaign cutscenes
│   ├── intro/                       # Intro cutscenes
│   │   ├── campaign_intro/          # Campaign intro
│   │   └── disc_intros/             # Disc intro sequences
│   ├── missions/                    # Mission cutscenes
│   │   ├── m01/                     # Mission 1 cutscenes
│   │   │   ├── intro.ani            # Intro cutscene
│   │   │   ├── mid_mission.ani      # Mid-mission cutscene
│   │   │   └── outro.ani            # Outro cutscene
│   │   ├── m02/                     # Mission 2 cutscenes
│   │   │   ├── intro.ani            # Intro cutscene
│   │   │   ├── mid_mission.ani      # Mid-mission cutscene
│   │   │   └── outro.ani            # Outro cutscene
│   │   └── ...                      # Additional missions
│   └── outro/                       # Outro cutscenes
│       ├── campaign_outro/          # Campaign outro
│       └── disc_outros/             # Disc outro sequences

/ui/fiction_reader/                  # Fiction reader interface
├── hermes/                          # Hermes campaign reader
│   ├── backgrounds/                 # Reader backgrounds
│   ├── fonts/                       # Reader fonts
│   ├── themes/                      # Reader themes
│   ├── navigation/                  # Navigation controls
│   └── audio_controls/              # Audio playback controls
└── components/                      # Reusable reader components
    ├── text_display/                # Text display component
    ├── audio_player/                # Audio player component
    ├── navigation_panel/            # Navigation panel
    └── bookmark_system/             # Bookmark system

/scenes/fiction/                     # Fiction scenes directory
├── hermes/                          # Hermes campaign scenes
│   ├── reader/                      # Fiction reader scenes
│   │   ├── campaign_reader.tscn     # Campaign reader scene
│   │   ├── disc_reader.tscn         # Disc reader scene
│   │   └── mission_reader.tscn      # Mission reader scene
│   ├── cutscenes/                   # Cutscene scenes
│   │   ├── intro_cutscenes/         # Intro cutscene scenes
│   │   ├── mission_cutscenes/       # Mission cutscene scenes
│   │   └── outro_cutscenes/         # Outro cutscene scenes
│   └── briefing/                    # Briefing scenes
│       ├── campaign_briefing.tscn   # Campaign briefing scene
│       ├── mission_briefing.tscn    # Mission briefing scene
│       └── tactical_briefing.tscn   # Tactical briefing scene
```

## Example Mapping
For Disc 1 Fiction:
- d1fiction.txt → /campaigns/hermes/fiction/disc_01/d1fiction.txt
- fiction_narrator.wav → /audio/voice/fiction/hermes/narrator/disc_01/narration.ogg
- dramatic_underscore.ogg → /audio/music/fiction/hermes/moods/dramatic.ogg
- disc1_intro.ani → /animations/cutscenes/hermes/intro/disc_intros/disc1_intro.png
- fiction_reader_background.pcx → /ui/fiction_reader/hermes/backgrounds/disc1_background.webp

For Mission 1 Fiction:
- m1fiction.txt → /campaigns/hermes/fiction/missions/m01/m1fiction.txt
- m1_briefing.txt → /campaigns/hermes/briefing/missions/m01/objectives.txt
- mission1_briefing_voice.wav → /audio/voice/fiction/hermes/missions/m01/briefing.ogg
- m1_briefing_music.ogg → /audio/music/fiction/hermes/missions/m01/briefing.ogg
- m1_intro_cutscene.ani → /animations/cutscenes/hermes/missions/m01/intro.png