# WAV Files Conversion Requirements

## Overview
WAV files contain sound effects, music, and voice acting used throughout Wing Commander Saga. These audio files need to be converted to Ogg Vorbis format for better compression and compatibility with Godot's audio system, following Godot's feature-based organization principles and the hybrid model defined in our project structure.

## File Types and Conversion Requirements

### Sound Effects
**Purpose**: Weapon sounds, explosion effects, and UI feedback
**Source Format**: WAV format (various bit depths and sample rates)
**Target Format**: Ogg Vorbis with appropriate quality settings
**Conversion Requirements**:
- Convert to standardized sample rate (44.1kHz or 48kHz)
- Apply appropriate bit rate for quality/size balance
- Maintain mono/stereo channel configuration
- Preserve dynamic range and sound characteristics
- Handle looping properties for continuous effects

### Music Tracks
**Purpose**: Background music for menus, missions, and cutscenes
**Source Format**: WAV format (typically higher quality)
**Target Format**: Ogg Vorbis with high quality settings
**Conversion Requirements**:
- Convert to standardized sample rate (44.1kHz)
- Use higher bit rates for music quality
- Maintain stereo channel configuration
- Preserve full frequency range and dynamics
- Handle seamless looping for ambient tracks

### Voice Acting
**Purpose**: Pilot communication, mission briefings, and character dialogue
**Source Format**: WAV format with voice-optimized encoding
**Target Format**: Ogg Vorbis with speech-optimized settings
**Conversion Requirements**:
- Convert to standardized sample rate (22.05kHz or 44.1kHz)
- Use appropriate bit rates for speech clarity
- Apply noise reduction if needed
- Maintain consistent volume levels
- Handle dialogue timing and synchronization

### Ambient Sounds
**Purpose**: Environmental audio for space, nebulae, and planetary surfaces
**Source Format**: WAV format with spatial characteristics
**Target Format**: Ogg Vorbis with 3D audio properties
**Conversion Requirements**:
- Convert to appropriate sample rate for environmental audio
- Maintain spatial properties for 3D positioning
- Apply reverb and environmental effects
- Handle long looped samples efficiently
- Preserve atmospheric qualities

## Conversion Process

### 1. Format Analysis Phase
- Validate WAV file headers and structure
- Extract audio properties (sample rate, bit depth, channels)
- Identify intended use (SFX, music, voice, ambient)
- Check for special properties or metadata
- Assess audio quality and characteristics

### 2. Quality Optimization Phase
- Apply appropriate sample rate conversion
- Optimize bit depth and format for target use
- Apply noise reduction and audio cleanup
- Normalize volume levels where appropriate
- Preserve important audio characteristics

### 3. Format Conversion Phase
- Convert to Ogg Vorbis with appropriate settings
- Apply different quality levels based on audio type
- Handle stereo/mono conversion if needed
- Maintain loop points and special markers
- Generate multiple quality variants for different platforms

### 4. Metadata Integration Phase
- Embed descriptive metadata in audio files
- Maintain cross-references to game events
- Handle 3D positioning properties
- Preserve timing and synchronization data
- Generate resource definitions for Godot integration

## Directory Structure Alignment
Following the Godot project structure defined in directory_structure.md and the hybrid organizational model:

### Assets Directory Structure (Global Assets)
Global audio assets that follow the "Global Litmus Test" principle: "If I delete three random features, is this asset still needed?"

```
assets/
├── audio/                         # Shared audio files
│   ├── sfx/                       # Generic sound effects
│   │   ├── weapons/               # Weapon sound effects
│   │   │   ├── firing/            # Weapon firing sounds
│   │   │   ├── impacts/           # Weapon impact sounds
│   │   │   ├── explosions/        # Explosion sounds
│   │   │   └── flyby/             # Projectile flyby sounds
│   │   ├── environment/           # Environmental sounds
│   │   │   ├── space/             # Space ambient sounds
│   │   │   ├── cockpit/           # Cockpit sounds
│   │   │   └── ui/                # User interface sounds
│   │   ├── ships/                 # Generic ship sounds
│   │   │   ├── engines/           # Generic engine sounds
│   │   │   ├── movement/          # Ship movement sounds
│   │   │   └── destruction/       # Generic destruction sounds
│   │   └── effects/               # Generic effect sounds
│   ├── music/                     # Background music tracks
│   │   ├── ambient/               # Ambient background music
│   │   ├── combat/                # Combat music tracks
│   │   ├── briefing/              # Mission briefing music
│   │   ├── debriefing/            # Mission debriefing music
│   │   ├── credits/               # Credits sequence music
│   │   └── cutscenes/             # Cutscene music
│   └── voice/                     # Voice acting files
│       ├── mission_briefings/     # Mission briefing voice files
│       ├── character_dialogue/    # Character dialogue files
│       ├── system_announcements/  # System announcement voice files
│       └── mission_debriefings/   # Mission debriefing voice files
├── data/                          # Shared data resources
│   ├── ai/                        # AI data resources
│   │   └── profiles/              # AI profile definitions
│   └── mission/                   # Mission data resources
├── textures/                      # Shared texture files
│   ├── ui/                        # Generic UI elements
│   ├── effects/                   # Particle textures used by multiple effects
│   └── fonts/                     # Font textures
└── animations/                    # Shared animation files
    ├── ui/                        # UI animations
    └── effects/                   # Generic effect animations
```

### Features Directory Structure (Feature-Specific Assets)
Feature-specific audio assets that are closely tied to particular features and follow the co-location principle:

```
features/
├── fighters/                      # Fighter ship entities
│   ├── confed_arrow/              # F-27B Arrow fighter
│   │   ├── arrow.tscn             # Scene file
│   │   ├── arrow.gd               # Script file
│   │   ├── arrow.tres             # Ship data resource
│   │   ├── arrow.glb              # 3D model
│   │   ├── arrow_diffuse.webp     # Texture
│   │   ├── arrow_normal.webp      # Normal map
│   │   └── assets/                # Feature-specific assets
│   │       └── sounds/            # Ship-specific sounds
│   │           ├── engine_loop.ogg # Engine loop sound
│   │           ├── maneuver.ogg    # Maneuvering thrusters
│   │           └── afterburner.ogg # Afterburner sound
│   ├── confed_rapier/             # F-44B Raptor fighter
│   │   ├── rapier.tscn            # Scene file
│   │   ├── rapier.gd              # Script file
│   │   ├── rapier.tres            # Ship data resource
│   │   ├── rapier.glb             # 3D model
│   │   ├── rapier.png             # Texture
│   │   └── assets/                # Feature-specific assets
│   │       └── sounds/            # Ship-specific sounds
│   │           └── engine_loop.ogg # Engine loop sound
│   └── _shared/                   # Shared fighter assets
├── capital_ships/                 # Capital ship entities
│   ├── tcs_behemoth/              # TCS Behemoth capital ship
│   │   ├── behemoth.tscn          # Scene file
│   │   ├── behemoth.gd            # Script file
│   │   ├── behemoth.tres          # Ship data resource
│   │   ├── behemoth.glb           # 3D model
│   │   ├── behemoth_diffuse.webp  # Texture
│   │   ├── behemoth_normal.webp   # Normal map
│   │   └── assets/                # Feature-specific assets
│   │       └── sounds/            # Ship-specific sounds
│   │           └── engine_loop.ogg # Engine loop sound
│   └── _shared/                   # Shared capital ship assets
├── weapons/                       # Weapon entities
│   ├── ion_cannon/                # Ion cannon weapon
│   │   ├── ion_cannon.tscn        # Scene
│   │   ├── ion_cannon.gd          # Script
│   │   ├── ion_cannon.tres        # Weapon data
│   │   ├── ion_cannon.glb         # Model
│   │   ├── ion_cannon.webp        # Texture
│   │   └── assets/                # Feature-specific assets
│   │       └── sounds/            # Weapon-specific sounds
│   │           ├── fire_sound.ogg # Firing sound
│   │           └── impact_sound.ogg # Impact sound
│   ├── javelin_missile/           # Javelin missile weapon
│   │   ├── javelin_missile.tscn   # Scene
│   │   ├── javelin_missile.gd     # Script
│   │   ├── javelin_missile.tres   # Weapon data
│   │   ├── javelin_missile.glb    # Model
│   │   ├── javelin_missile.webp   # Texture
│   │   └── assets/                # Feature-specific assets
│   │       └── sounds/            # Weapon-specific sounds
│   │           ├── fire_sound.ogg # Firing sound
│   │           └── impact_sound.ogg # Impact sound
│   └── _shared/                   # Shared weapon assets
├── effects/                       # Effect entities
│   ├── explosion/                 # Explosion effect
│   │   ├── explosion.tscn         # Scene file
│   │   ├── explosion.gd           # Script file
│   │   ├── explosion.tres         # Effect data resource
│   │   ├── explosion_fire.webp    # Texture
│   │   └── assets/                # Feature-specific assets
│   │       └── sounds/            # Effect-specific sounds
│   │           └── explosion_sound.ogg # Explosion sound
│   ├── fireball/                  # Fireball effect
│   │   ├── fireball.tscn          # Scene file
│   │   ├── fireball.gd            # Script file
│   │   ├── fireball.tres          # Effect data resource
│   │   ├── fireball_texture.webp  # Texture
│   │   └── assets/                # Feature-specific assets
│   │       └── sounds/            # Effect-specific sounds
│   │           └── fireball_sound.ogg # Fireball sound
│   └── _shared/                   # Shared effect assets
├── environment/                   # Environmental objects and props
│   ├── asteroid/                  # Asteroid object
│   │   ├── asteroid.tscn          # Scene file
│   │   ├── asteroid.gd            # Script file
│   │   ├── asteroid.tres          # Data resource
│   │   ├── asteroid.glb           # 3D model
│   │   ├── asteroid.webp          # Texture
│   │   └── assets/                # Feature-specific assets
│   │       └── sounds/            # Environment-specific sounds
│   │           └── collision_sound.ogg # Collision sound
│   └── _shared/                   # Shared environment assets
└── ui/                            # UI feature elements
    ├── main_menu/                 # Main menu interface
    │   ├── main_menu.tscn         # Scene file
    │   ├── main_menu.gd           # Script file
    │   ├── background.webp        # Background texture
    │   └── assets/                # Feature-specific assets
    │       └── sounds/            # UI-specific sounds
    │           ├── click.ogg      # Button click sound
    │           ├── hover.ogg      # Button hover sound
    │           └── transition.ogg # Menu transition sound
    ├── hud/                       # Heads-up display
    │   ├── player_hud.tscn        # Scene file
    │   ├── player_hud.gd          # Script file
    │   └── assets/                # Feature-specific assets
    │       └── sounds/            # UI-specific sounds
    │           ├── warning.ogg        # Warning sound
    │           ├── target_acquired.ogg # Target acquired sound
    │           └── system_status.ogg  # System status sound
    └── _shared/                   # Shared UI assets
```

## Integration Points

### Data Converter Output Mapping
- Sound effects → Converted to Ogg Vorbis and placed in `/assets/audio/sfx/` or `/features/{category}/{entity}/assets/sounds/`
- Music tracks → Converted to Ogg Vorbis and placed in `/assets/audio/music/`
- Voice acting → Converted to Ogg Vorbis and placed in `/assets/audio/voice/`
- Ambient sounds → Converted to Ogg Vorbis and placed in `/assets/audio/sfx/environment/`

### Resource References
- **Global audio assets** in `/assets/audio/` are referenced by multiple features and systems
- **Feature-specific audio** in `/features/{category}/{entity}/assets/sounds/` are referenced directly by their entity scenes
- **Audio managers** in `/autoload/audio_manager.gd` handle playback of both global and feature-specific audio
- **Game events** trigger specific audio files through signal connections

## Relationship to Other Assets

### Entity Integration
Audio files integrate with entity scenes following the feature-based organization and hybrid model:
- Ship entities reference engine sounds from `/features/fighters/{faction}_{ship_name}/assets/sounds/` or use shared sounds from `/assets/audio/sfx/ships/engines/`
- Weapon entities reference firing sounds from `/features/weapons/{weapon_name}/assets/sounds/` or use shared sounds from `/assets/audio/sfx/weapons/firing/`
- Explosion entities reference impact sounds from `/features/effects/{effect_name}/assets/sounds/` or use shared sounds from `/assets/audio/sfx/explosions/`
- UI components reference interface sounds from `/features/ui/{component_name}/assets/sounds/` or use shared sounds from `/assets/audio/sfx/ui/`

### System Integration
Audio files integrate with Godot systems in `/scripts/` directories following the separation of concerns:
- `/scripts/audio/sound_manager.gd` - Sound effect management
- `/scripts/audio/music_player.gd` - Music playback system
- `/scripts/audio/voice_system.gd` - Voice acting system
- `/scripts/weapons/weapon_system.gd` - Weapon firing sounds
- `/scripts/mission/mission_manager.gd` - Mission-specific audio triggers

### Campaign Integration
Audio files integrate with campaign content in `/campaigns/` directories following the campaign-centric organization:
- Mission-specific voice acting organized by campaign and mission in `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/assets/audio/`
- Campaign-specific music tracks for intro/outro sequences referenced in `/campaigns/{campaign}/campaign.tres`
- Briefing and debriefing audio files stored with mission data in `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/assets/audio/`

### Closely Related Assets
- Mission files (.fs2) that reference specific audio events and are converted to `/campaigns/{campaign}/missions/{mission_id}_{mission_name}/`
- Table files (.tbl) that define sound effect mappings in `/assets/data/`
- Animation files (.ani) that synchronize with audio and are converted to sprite sheets in `/assets/animations/` or feature directories
- Particle effect definitions that trigger associated sounds from `/assets/data/effects/`

### Common Shared Assets
Following the "Global Litmus Test" principle for assets that belong in `/assets/`:
- Standard UI sound effects used across different interfaces from `/assets/audio/sfx/ui/`
- Common weapon and explosion sound effects from `/assets/audio/sfx/weapons/` and `/assets/audio/sfx/explosions/`
- Shared ambient background tracks for similar environments from `/assets/audio/sfx/environment/`
- Standard voice prompts and system messages from `/assets/audio/voice/system_announcements/`
- Common transition and menu navigation sounds from `/assets/audio/sfx/ui/`

This structure follows the hybrid approach where truly global, context-agnostic audio assets are organized in `/assets/audio/`, while feature-specific audio assets are co-located with their respective features in `/features/{category}/{entity}/assets/sounds/`. The guiding principle is: "If I delete three random features, is this asset still needed?" If yes, it belongs in `/assets/audio/`; if only needed by specific features, it belongs in those feature directories. The organization aligns with the target directory structure defined in `directory_structure.md` and follows the integration plan outlined in `integration_plan.md`.