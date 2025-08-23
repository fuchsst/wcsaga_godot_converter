# Sounds Asset Mapping

## Overview
This document maps the sound definitions from sounds.tbl to their corresponding audio assets in the Wing Commander Saga Hermes campaign.

## Asset Types

### Sound Effects (.wav)
Sounds.tbl references numerous WAV files for various game audio:
- snd_missile_tracking.wav - Missile tracking/acquiring lock (looped)
- snd_missile_lock.wav - Missile lock acquired (non-looping)
- snd_primary_cycle.wav - Cycle primary weapon
- snd_secondary_cycle.wav - Cycle secondary weapon
- snd_engine.wav - Engine sound (as heard in cockpit)
- snd_cargo_reveal.wav - Cargo revealed notification
- snd_death_roll.wav - Ship death roll (3D sound)
- snd_ship_explode_1.wav - Ship explosion (3D sound)
- snd_target_acquire.wav - Target acquired
- snd_weapon_fire_*.wav - Weapon firing sounds
- snd_engine_*.wav - Engine sounds for different ship classes
- snd_explosion_*.wav - Explosion sounds for various effects
- snd_ui_*.wav - User interface feedback sounds

### Music Tracks (.wav/.ogg)
Music.tbl references WAV files for campaign music:
- ambient_mission_failed.ogg - Ambient music for failed missions
- player_dead_b_01.ogg - Music when player dies
- ambient_a_01.ogg - General ambient music
- aarrival_normal_b_01.ogg - Allied arrival during normal situations
- earrival_normal_b_01.ogg - Enemy arrival during normal situations
- battle1_b_01.ogg - Battle music track 1
- battle2_b_01.ogg - Battle music track 2
- battle3_b_01.ogg - Battle music track 3
- victory_b_01.ogg - Victory music
- goal_achieved_b_01.ogg - Goal completed music
- goal_failed_b_01.ogg - Goal failed music
- briefing music tracks
- debriefing music tracks
- credits music tracks

## Target Structure
```
/audio/sfx/                          # Sound effects directory
├── weapons/                         # Weapon sound effects
│   ├── firing/
│   ├── impacts/
│   └── reloading/
├── explosions/                      # Explosion sound effects
├── environment/                     # Environmental sounds
│   ├── space/
│   ├── cockpit/
│   └── ui/
├── ui/                              # User interface sounds
│   ├── buttons/
│   ├── menus/
│   └── alerts/
└── ships/                           # Ship-specific sounds
    ├── engines/
    ├── weapons/
    └── destruction/

/audio/music/                        # Music tracks directory
├── ambient/                         # Ambient background music
├── combat/                          # Combat music tracks
├── briefing/                        # Mission briefing music
├── debriefing/                      # Mission debriefing music
├── credits/                         # Credits sequence music
└── cutscenes/                       # Cutscene music
```

## Example Mapping
For missile tracking sound:
- sounds.tbl entry → Missile tracking sound definition
- snd_missile_tracking.wav → /audio/sfx/weapons/tracking/snd_missile_tracking.ogg

For battle music:
- music.tbl entry → Battle music track definition
- battle1_b_01.ogg → /audio/music/combat/battle1_b_01.ogg