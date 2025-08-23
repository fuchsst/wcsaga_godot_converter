# Missions Asset Mapping

## Overview
This document maps the mission definitions from FS2 files to their corresponding media assets in the Wing Commander Saga Hermes campaign.

## Asset Types

### Mission Files (.fs2)
FS2 files contain complete mission definitions:
- M01-BG-Hermes.fs2 - Mission 1 file
- M02-BG-Hermes.fs2 - Mission 2 file
- M03-BG-Hermes.fs2 - Mission 3 file
- etc.

Each FS2 file contains:
- Mission briefing data
- Initial ship placements
- AI directives and events
- Scripting logic
- Objectives and goals
- Message sequences

### Briefing Text (.txt)
Mission-specific fiction and briefing text:
- m1fiction.txt - Mission 1 fiction text
- m2fiction.txt - Mission 2 fiction text
- m3fiction.txt - Mission 3 fiction text
- briefing_*.txt - Briefing screen text files

### Cutscenes (.ani/.ogg)
Mission-specific cutscene animations and audio:
- intro_*.ani - Intro cutscene animations
- outro_*.ani - Outro cutscene animations
- cutscene_*.ani - In-mission cutscenes
- briefing_*.ogg - Briefing voice audio
- cutscene_*.ogg - Cutscene voice audio
- outro_*.ogg - Outro voice audio

### Music Tracks (.ogg)
Mission-specific background music:
- ambient_*.ogg - Ambient mission music
- combat_*.ogg - Combat music tracks
- briefing_*.ogg - Briefing music
- victory_*.ogg - Victory music
- defeat_*.ogg - Defeat music

## Target Structure
```
/data/missions/hermes/               # Mission data definitions
├── m01_hermes/
│   ├── mission.tres                 # Mission definition
│   ├── objectives.tres              # Mission objectives
│   ├── events.tres                  # Mission events
│   └── messages.tres                # Mission messages
├── m02_hermes/
│   ├── mission.tres
│   ├── objectives.tres
│   ├── events.tres
│   └── messages.tres
└── ...                              # Additional missions

/missions/hermes/                    # Mission scenes directory
├── m01_hermes/
│   ├── mission.tscn                 # Mission scene
│   ├── briefing.txt                 # Briefing text (converted)
│   ├── fiction.txt                  # Fiction text (converted)
│   ├── intro_cutscene.tscn          # Intro cutscene
│   ├── outro_cutscene.tscn          # Outro cutscene
│   ├── briefing_audio.ogg           # Briefing voice audio
│   ├── intro_audio.ogg              # Intro cutscene audio
│   ├── outro_audio.ogg              # Outro cutscene audio
│   └── mission_music.ogg            # Mission background music
├── m02_hermes/
│   ├── mission.tscn
│   ├── briefing.txt
│   ├── fiction.txt
│   ├── intro_cutscene.tscn
│   ├── outro_cutscene.tscn
│   ├── briefing_audio.ogg
│   ├── intro_audio.ogg
│   ├── outro_audio.ogg
│   └── mission_music.ogg
└── ...                              # Additional missions

/text/fiction/hermes/                # Fiction text directory
├── m01_fiction.txt                  # Mission 1 fiction
├── m02_fiction.txt                  # Mission 2 fiction
├── m03_fiction.txt                  # Mission 3 fiction
└── ...                              # Additional mission fiction

/audio/voice/hermes/                 # Voice acting directory
├── missions/
│   ├── m01/
│   │   ├── briefing.ogg             # Briefing voice
│   │   ├── intro_cutscene.ogg       # Intro cutscene voice
│   │   ├── outro_cutscene.ogg       # Outro cutscene voice
│   │   └── inmission_*.ogg          # In-mission voice lines
│   ├── m02/
│   │   ├── briefing.ogg
│   │   ├── intro_cutscene.ogg
│   │   ├── outro_cutscene.ogg
│   │   └── inmission_*.ogg
│   └── ...                          # Additional missions
└── characters/                      # Character-specific voice lines
    ├── moran/
    ├── sandman/
    ├── honeybear/
    └── ...

/audio/music/hermes/                 # Mission music directory
├── m01/
│   ├── ambient.ogg                  # Ambient music
│   ├── combat.ogg                   # Combat music
│   ├── briefing.ogg                 # Briefing music
│   ├── victory.ogg                  # Victory music
│   └── defeat.ogg                   # Defeat music
├── m02/
│   ├── ambient.ogg
│   ├── combat.ogg
│   ├── briefing.ogg
│   ├── victory.ogg
│   └── defeat.ogg
└── ...                              # Additional missions

/animations/cutscenes/hermes/        # Cutscene animations directory
├── m01/
│   ├── intro_*.png                  # Intro cutscene frames
│   ├── outro_*.png                  # Outro cutscene frames
│   └── cutscene_*.png               # In-mission cutscene frames
├── m02/
│   ├── intro_*.png
│   ├── outro_*.png
│   └── cutscene_*.png
└── ...                              # Additional missions
```

## Example Mapping
For Mission 1:
- M01-BG-Hermes.fs2 → /missions/hermes/m01_hermes/mission.tscn
- m1fiction.txt → /text/fiction/hermes/m01_fiction.txt
- briefing_m01_*.ogg → /audio/voice/hermes/missions/m01/briefing.ogg
- ambient_mission_failed.ogg → /audio/music/hermes/m01/ambient.ogg
- intro_*.ani → /animations/cutscenes/hermes/m01/intro_*.png