# Sounds Asset Mapping

## Overview
This document maps the sound definitions from sounds.tbl and music.tbl to their corresponding audio assets in the Wing Commander Saga Hermes campaign, organized according to the Godot feature-based directory structure. The mapping follows the hybrid model where truly global audio assets are organized in the `/assets/` directory, while feature-specific sounds are co-located with their respective features.

## Asset Types

### Sound Effects (.wav/.ogg)
Sounds.tbl references numerous WAV and OGG files for various game audio:
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

### Music Tracks (.ogg)
Music.tbl references OGG files for campaign music:
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

## Format Conversion Process

### Legacy Formats to Godot Formats

**WAV Files (.wav)**
- Legacy audio format for most sound effects
- Will be converted to Ogg Vorbis format for better compression and Godot compatibility
- Audio quality and characteristics preserved during conversion
- 3D positioning support maintained where appropriate

**OGG Files (.ogg)**
- Already in a Godot-compatible format
- Will be maintained as-is with metadata preservation
- Music tracks and some sound effects already in OGG format

## Target Structure
Following the Godot project structure defined in directory_structure.md and the hybrid organizational model, audio assets are organized as follows:

### Assets Directory Structure
Generic audio assets that are shared across multiple features are organized in the global `/assets/` directory, following the "Global Litmus Test" principle: "If I delete three random features, is this asset still needed?"

```
assets/
├── audio/                         # Shared audio files
│   ├── sfx/                       # Generic sound effects
│   │   ├── weapons/               # Weapon sound effects
│   │   │   ├── firing/            # Weapon firing sounds
│   │   │   │   ├── laser_fire.ogg
│   │   │   │   ├── missile_fire.ogg
│   │   │   │   └── turret_fire.ogg
│   │   │   ├── impacts/           # Weapon impact sounds
│   │   │   │   ├── laser_impact.ogg
│   │   │   │   ├── missile_impact.ogg
│   │   │   │   └── energy_impact.ogg
│   │   │   └── reloading/         # Weapon reload sounds
│   │   │       ├── missile_load.ogg
│   │   │       └── weapon_cycle.ogg
│   │   ├── explosions/            # Explosion sound effects
│   │   │   ├── ship_explosions/   # Ship explosion sounds
│   │   │   │   ├── small_ship_explode.ogg
│   │   │   │   ├── medium_ship_explode.ogg
│   │   │   │   └── large_ship_explode.ogg
│   │   │   ├── subsystem_explosions/ # Subsystem destruction
│   │   │   │   └── subsystem_destroyed.ogg
│   │   │   └── environmental_explosions/ # Environmental explosions
│   │   │       ├── asteroid_explode_large.ogg
│   │   │       └── asteroid_explode_small.ogg
│   │   ├── environment/           # Environmental sounds
│   │   │   ├── space/             # Space ambient sounds
│   │   │   │   ├── engine_loop_large.ogg
│   │   │   │   └── capital_warp_in.ogg
│   │   │   ├── cockpit/           # Cockpit sounds
│   │   │   │   ├── engine_cockpit.ogg
│   │   │   │   └── life_support_hum.ogg
│   │   │   └── ui/                # User interface sounds
│   │   │       ├── button_click.ogg
│   │   │       ├── menu_open.ogg
│   │   │       ├── menu_close.ogg
│   │   │       ├── target_acquire.ogg
│   │   │       └── warning_alert.ogg
│   │   ├── ships/                 # Generic ship sounds
│   │   │   ├── engines/           # Generic engine sounds
│   │   │   │   ├── fighter_engine_loop.ogg
│   │   │   │   └── capital_engine_loop.ogg
│   │   │   ├── movement/          # Ship movement sounds
│   │   │   │   ├── thruster_burst.ogg
│   │   │   │   └── maneuvering.ogg
│   │   │   └── destruction/       # Generic destruction sounds
│   │   │       ├── death_roll.ogg
│   │   │       └── hull_damage.ogg
│   │   └── ui/                    # UI sound effects
│   │       ├── buttons/           # Button interaction sounds
│   │       ├── menus/             # Menu navigation sounds
│   │       └── alerts/            # Alert and notification sounds
│   ├── music/                     # Background music tracks
│   │   ├── ambient/               # Ambient background music
│   │   │   ├── mission_ambient.ogg
│   │   │   └── space_ambient.ogg
│   │   ├── combat/                # Combat music tracks
│   │   │   ├── battle1.ogg
│   │   │   ├── battle2.ogg
│   │   │   └── battle3.ogg
│   │   ├── briefing/              # Mission briefing music
│   │   │   ├── briefing_theme.ogg
│   │   │   └── mission_briefing.ogg
│   │   ├── debriefing/            # Mission debriefing music
│   │   │   ├── debriefing_theme.ogg
│   │   │   └── mission_debriefing.ogg
│   │   ├── credits/               # Credits sequence music
│   │   │   └── credits_theme.ogg
│   │   └── cutscenes/             # Cutscene music
│   │       ├── intro_sequence.ogg
│   │       └── story_cutscene.ogg
│   └── voice/                     # Voice acting files
│       ├── mission_briefings/     # Mission briefing voice files
│       ├── character_dialogue/    # Character dialogue files
│       ├── system_announcements/  # System announcement voice files
│       └── mission_debriefings/   # Mission debriefing voice files
```

### Features Directory Structure
Feature-specific audio assets are organized within their respective feature directories, following the co-location principle where all files related to a single feature are grouped together.

```
features/
├── fighters/                      # Fighter ship entities
│   ├── confed_arrow/              # F-27B Arrow fighter
│   │   ├── arrow.tscn             # Scene file
│   │   ├── arrow.gd               # Script file
│   │   ├── arrow.tres             # Ship data resource
│   │   ├── arrow.glb              # 3D model
│   │   ├── arrow.png              # Texture
│   │   ├── assets/                # Feature-specific assets
│   │   │   └── sounds/            # Ship-specific sounds
│   │   │       ├── engine_loop.ogg # Engine loop sound
│   │   │       ├── maneuver.ogg    # Maneuvering thrusters
│   │   │       └── afterburner.ogg # Afterburner sound
│   │   └── arrow_engine.ogg       # Engine sound (legacy placement)
│   ├── confed_rapier/             # F-44B Raptor fighter
│   │   ├── rapier.tscn            # Scene file
│   │   ├── rapier.gd              # Script file
│   │   ├── rapier.tres            # Ship data resource
│   │   ├── rapier.glb             # 3D model
│   │   ├── rapier.png             # Texture
│   │   └── assets/                # Feature-specific assets
│   │       └── sounds/            # Ship-specific sounds
│   │           └── engine_loop.ogg # Engine loop sound
│   └── templates/                 # Fighter templates
├── capital_ships/                 # Capital ship entities
│   ├── tcs_behemoth/              # TCS Behemoth capital ship
│   │   ├── behemoth.tscn          # Scene file
│   │   ├── behemoth.gd            # Script file
│   │   ├── behemoth.tres          # Ship data resource
│   │   ├── behemoth.glb           # 3D model
│   │   ├── behemoth.png           # Texture
│   │   └── assets/                # Feature-specific assets
│   │       └── sounds/            # Ship-specific sounds
│   │           └── engine_loop.ogg # Engine loop sound
│   └── templates/                 # Capital ship templates
├── weapons/                       # Weapon entities
│   ├── laser_cannon/              # Laser cannon
│   │   ├── laser_cannon.tscn      # Scene
│   │   ├── laser_cannon.gd        # Script
│   │   ├── laser_cannon.tres      # Weapon data
│   │   ├── laser_cannon.glb       # Model
│   │   ├── laser_cannon.png       # Texture
│   │   └── assets/                # Feature-specific assets
│   │       └── sounds/            # Weapon-specific sounds
│   │           ├── fire_sound.ogg # Firing sound
│   │           └── impact_sound.ogg # Impact sound
│   └── templates/                 # Weapon templates
├── effects/                       # Effect entities
│   ├── explosion/                 # Explosion effect
│   │   ├── explosion.tscn         # Scene file
│   │   ├── explosion.gd           # Script file
│   │   ├── explosion.tres         # Effect data resource
│   │   ├── explosion_fire.png     # Texture
│   │   └── assets/                # Feature-specific assets
│   │       └── sounds/            # Effect-specific sounds
│   │           └── explosion_sound.ogg # Explosion sound
│   └── templates/                 # Effect templates
└── ui/                            # UI feature elements
    ├── main_menu/                 # Main menu interface
    │   ├── main_menu.tscn         # Scene file
    │   ├── main_menu.gd           # Script file
    │   ├── background.png         # Background texture
    │   └── assets/                # Feature-specific assets
    │       └── sounds/            # UI-specific sounds
    │           ├── click.ogg      # Button click sound
    │           ├── hover.ogg      # Button hover sound
    │           └── transition.ogg # Menu transition sound
    └── templates/                 # UI templates
```

### Autoload Directory Structure
Audio management systems are implemented as autoload singletons, following the "Is this state or service truly global and required everywhere?" principle.

```
autoload/
├── audio_manager.gd               # Audio management system
├── music_player.gd                # Music playback system
└── voice_system.gd                # Voice acting system
```

### Scripts Directory Structure
Reusable audio system scripts are organized in the `/scripts/audio/` directory, following the separation of concerns principle.

```
scripts/
├── audio/                         # Audio system scripts
│   ├── sound_manager.gd           # Sound effect management
│   ├── music_player.gd            # Music playback system
│   └── voice_system.gd            # Voice acting system
└── utilities/                     # Utility functions and helpers
    └── resource_loader.gd         # Resource loading utilities
```

## Data Conversion Strategy

### Configuration Files (.tbl)
Convert to Godot resources (.tres) organized appropriately:
- Sound definitions from sounds.tbl to SoundData resources in `/assets/data/audio/`
- Music definitions from music.tbl to MusicData resources in `/assets/data/audio/`
- Use Godot's resource system for data-driven design with centralized management

### Audio Conversion Process
1. **WAV to OGG Converter**: Convert .wav files to Ogg Vorbis format with quality preservation
2. **Metadata Preservation**: Maintain audio characteristics like 3D positioning, volume, and looping properties
3. **Resource Generation**: Create Godot .tres files with converted audio data
4. **Directory Organization**: Place converted audio files in appropriate directories following the structure above
5. **Validation**: Verify converted audio maintains original characteristics and quality

## Example Mapping

### For missile tracking sound:
- sounds.tbl entry → Missile tracking sound definition with 3D properties
- snd_missile_tracking.wav → /assets/audio/sfx/weapons/firing/missile_tracking.ogg

### For battle music:
- music.tbl entry → Battle music track definition with timing information
- battle1_b_01.ogg → /assets/audio/music/combat/battle1.ogg

### For F-27B Arrow fighter engine sound:
- sounds.tbl entry → Engine sound definition
- Feature-specific engine sound → /features/fighters/confed_arrow/assets/sounds/engine_loop.ogg

### For laser cannon firing sound:
- sounds.tbl entry → Weapon firing sound definition
- Feature-specific firing sound → /features/weapons/laser_cannon/assets/sounds/fire_sound.ogg

### For explosion effect sound:
- sounds.tbl entry → Explosion sound definition
- Feature-specific explosion sound → /features/effects/explosion/assets/sounds/explosion_sound.ogg

## Relationship to Other Assets
Audio assets are closely related to:
- **Ship System**: Ships use engine sounds from `/assets/audio/sfx/ships/engines/` and feature-specific sounds from their directories
- **Weapon System**: Weapons use firing and impact sounds from `/assets/audio/sfx/weapons/` and feature-specific sounds
- **Effect System**: Effects use sound files from `/assets/audio/sfx/` and feature-specific sounds
- **UI System**: UI elements use sounds from `/assets/audio/sfx/ui/` and feature-specific sounds
- **Audio Manager**: Global audio system in `/autoload/audio_manager.gd` controls all audio playback
- **Mission System**: Missions trigger specific music tracks from `/assets/audio/music/`
- **Voice System**: Voice acting files organized in `/assets/audio/voice/` for dialogue and announcements

This organization follows the hybrid approach where truly global audio assets are organized in the `/assets/audio/` directory following the "Global Litmus Test" principle, while feature-specific sounds are co-located with their respective features in the `/features/` directory. The structure maintains clear separation of concerns between different audio types while ensuring easy access to all audio assets needed for game features.