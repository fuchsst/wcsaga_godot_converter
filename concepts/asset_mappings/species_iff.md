# Species and IFF Asset Mapping

## Overview
This document maps the species and IFF definitions from Species_defs.tbl and iff_defs.tbl to their corresponding media assets in the Wing Commander Saga Hermes campaign, organized according to the Godot feature-based directory structure. The mapping follows the hybrid model where truly global data assets are organized in the `/assets/` directory, while species-specific and IFF-specific effects are co-located with their respective features.

## Species Asset Types

### Species Definitions (.tbl)
Species_defs.tbl defines different species with their properties:
- Terran - Human Confederation
- Kilrathi - Kilrathi Empire
- Pirate - Independent pirate factions
- Unknown - Unknown/neutral factions

Each species has specific properties:
- Thruster animation references
- Debris behavior characteristics
- Species-specific visual effects
- Default IFF affiliations
- FRED color definitions

### Species-Specific Assets

#### Terran Assets
- Thruster animations (.ani files) - thruster01.ani, thruster01a.ani, thruster02-01.ani, etc.
- Thruster glow effects (.dds files) - thrusterglow01.dds, thrusterglow01a.dds
- Shield hit animations (.ani files) - shieldhit01a.ani
- Debris textures (.dds files) - debris01a.dds
- Species-specific ship models and textures
- Engine sounds (.wav files)
- Voice acting for Terran characters
- Music themes for Terran missions

#### Kilrathi Assets
- Thruster animations (.ani files)
- Thruster glow effects (.dds files)
- Shield hit animations (.ani files)
- Debris textures (.dds files)
- Species-specific ship models and textures
- Engine sounds (.wav files)
- Voice acting for Kilrathi characters
- Music themes for Kilrathi missions

#### Pirate Assets
- Thruster animations (.ani files)
- Thruster glow effects (.dds files)
- Shield hit animations (.ani files)
- Debris textures (.dds files)
- Species-specific ship models and textures
- Engine sounds (.wav files)
- Voice acting for Pirate characters
- Music themes for Pirate missions

## IFF Asset Types

### IFF Definitions (.tbl)
iff_defs.tbl defines identification friend or foe relationships:
- Friendly factions (e.g., Terran Confederation)
- Hostile factions (e.g., Kilrathi Empire)
- Neutral factions (e.g., Pirates, Unknown)
- Traitor factions (special case)

Each IFF has properties:
- Color codes for radar/HUD display
- Relationship attack matrices
- Visibility flags
- Default ship flags
- Species affiliations

### IFF-Specific Assets

#### Radar Display Colors
- IFF color definitions for different factions
- Radar blip graphics for different IFF states
- Target box colors for different IFF states
- Warning colors for hostile contacts

#### HUD Display Elements
- IFF-specific targeting reticles
- IFF-specific weapon lock indicators
- IFF-specific threat warning displays
- IFF-specific communication indicators

#### Communication Assets
- IFF-specific voice acting
- IFF-specific radio chatter
- IFF-specific tactical calls
- IFF-specific identification protocols

## Format Conversion Process

### Legacy Formats to Godot Formats

**ANI Files (.ani)**
- Legacy animation format for effects like thrusters, shield hits, and debris
- Will be converted to sprite sheet animations or particle effects in Godot
- Animation frame sequences preserved during conversion
- Timing and looping properties maintained where appropriate

**DDS Files (.dds)**
- Legacy texture format for effects and UI elements
- Will be converted to WebP format for better compression and Godot compatibility
- Mipmaps and compression settings preserved during conversion
- Alpha channels maintained for transparency effects

**TBL Files (.tbl)**
- Legacy configuration format for species and IFF definitions
- Will be converted to Godot resource files (.tres) for data-driven design
- Property mappings preserved with appropriate Godot data types
- Relationship matrices maintained for gameplay logic

## Target Structure
Following the Godot project structure defined in directory_structure.md and the hybrid organizational model, species and IFF assets are organized as follows:

### Assets Directory Structure
Generic data assets that are shared across multiple features are organized in the global `/assets/` directory, following the "Global Litmus Test" principle: "If I delete three random features, is this asset still needed?"

```
assets/
├── data/                          # Shared data resources
│   ├── species/                   # Species data definitions
│   │   ├── terran_species.tres    # Terran species definition
│   │   ├── kilrathi_species.tres  # Kilrathi species definition
│   │   ├── pirate_species.tres    # Pirate species definition
│   │   └── unknown_species.tres   # Unknown species definition
│   └── iff/                       # IFF data definitions
│       ├── friendly_iff.tres      # Friendly IFF definition
│       ├── hostile_iff.tres       # Hostile IFF definition
│       ├── neutral_iff.tres       # Neutral IFF definition
│       └── traitor_iff.tres       # Traitor IFF definition
├── textures/                      # Shared texture files
│   ├── effects/                   # Particle textures used by multiple effects
│   │   ├── shield_hits/           # Shield hit effect textures
│   │   │   ├── shieldhit01a_0000.webp
│   │   │   ├── shieldhit01a_0001.webp
│   │   │   └── shieldhit01a_0002.webp
│   │   ├── debris/                # Debris effect textures
│   │   │   ├── debris01a.webp
│   │   │   ├── debris01c.webp
│   │   │   └── debris02.webp
│   │   └── thrusters/             # Thruster effect textures
│   │       ├── thrusterglow01.webp
│   │       ├── thrusterglow01a.webp
│   │       └── thrusterparticle.webp
│   └── ui/                        # Generic UI elements
│       ├── hud/                   # HUD display elements
│       │   ├── iff/               # IFF-specific HUD elements
│       │   │   ├── friendly/      # Friendly IFF elements
│       │   │   │   ├── target_box.webp
│       │   │   │   ├── lock_indicator.webp
│       │   │   │   └── threat_warning.webp
│       │   │   ├── hostile/       # Hostile IFF elements
│       │   │   │   ├── target_box.webp
│       │   │   │   ├── lock_indicator.webp
│       │   │   │   └── threat_warning.webp
│       │   │   ├── neutral/       # Neutral IFF elements
│       │   │   │   ├── target_box.webp
│       │   │   │   ├── lock_indicator.webp
│       │   │   │   └── threat_warning.webp
│       │   │   └── traitor/       # Traitor IFF elements
│       │   │       ├── target_box.webp
│       │   │       ├── lock_indicator.webp
│       │   │       └── threat_warning.webp
│       │   └── radar/             # Radar display elements
│       │       ├── iff_colors/    # IFF color definitions
│       │       │   ├── friendly.webp
│       │       │   ├── hostile.webp
│       │       │   ├── neutral.webp
│       │       │   └── traitor.webp
│       │       └── blips/         # Radar blip graphics
│       │           ├── friendly.webp
│       │           ├── hostile.webp
│       │           ├── neutral.webp
│       │           └── traitor.webp
│       └── fonts/                 # Font textures
├── audio/                         # Shared audio files
│   ├── voice/                     # Voice acting files
│   │   ├── terran/                # Terran voice acting
│   │   │   ├── pilots/            # Terran pilot voices
│   │   │   ├── command/           # Terran command voices
│   │   │   └── mission_control/   # Terran mission control voices
│   │   ├── kilrathi/              # Kilrathi voice acting
│   │   │   ├── pilots/            # Kilrathi pilot voices
│   │   │   ├── command/           # Kilrathi command voices
│   │   │   └── mission_control/   # Kilrathi mission control voices
│   │   └── pirate/                # Pirate voice acting
│   │       ├── pilots/            # Pirate pilot voices
│   │       ├── command/           # Pirate command voices
│   │       └── characters/        # Pirate character voices
│   ├── music/                     # Background music tracks
│   │   ├── terran/                # Terran music themes
│   │   │   ├── campaign/          # Terran campaign music
│   │   │   ├── combat/            # Terran combat music
│   │   │   └── ambient/           # Terran ambient music
│   │   ├── kilrathi/              # Kilrathi music themes
│   │   │   ├── campaign/          # Kilrathi campaign music
│   │   │   ├── combat/            # Kilrathi combat music
│   │   │   └── ambient/           # Kilrathi ambient music
│   │   └── pirate/                # Pirate music themes
│   │       ├── campaign/          # Pirate campaign music
│   │       ├── combat/            # Pirate combat music
│   │       └── ambient/           # Pirate ambient music
│   └── sfx/                       # Generic sound effects
└── animations/                    # Shared animation files
    ├── effects/                   # Generic effect animations
    │   ├── shield_hits/           # Shield hit animations
    │   │   └── shieldhit01a.webp  # Converted shield hit animation
    │   ├── debris/                # Debris animations
    │   │   ├── debris01.webp      # Converted debris animation
    │   │   └── debris02.webp      # Converted debris animation
    │   └── thrusters/             # Thruster animations
    │       ├── thruster01.webp    # Converted thruster animation
    │       └── thruster02.webp    # Converted thruster animation
    └── ui/                        # UI animations
```

### Features Directory Structure
Species-specific and IFF-specific effects that are closely tied to particular features are organized within their respective feature directories, following the co-location principle where all files related to a single feature are grouped together.

```
features/
├── fighters/                      # Fighter ship entities
│   ├── confed_rapier/             # F-44B Raptor fighter
│   │   ├── rapier.tscn            # Scene file
│   │   ├── rapier.gd              # Script file
│   │   ├── rapier.tres            # Ship data resource
│   │   ├── rapier.glb             # 3D model
│   │   ├── rapier.png             # Texture
│   │   └── assets/                # Feature-specific assets
│   │       ├── effects/           # Ship-specific effects
│   │       │   ├── thrusters/     # Thruster effects
│   │       │   │   ├── thruster01.webp
│   │       │   │   └── thrusterglow01.webp
│   │       │   └── shield_hits/   # Shield hit effects
│   │       │       └── shieldhit01a.webp
│   │       └── sounds/            # Ship-specific sounds
│   │           └── engine_loop.ogg # Engine sound
│   ├── kilrathi_dralthi/          # Dralthi fighter
│   │   ├── dralthi.tscn           # Scene file
│   │   ├── dralthi.gd             # Script file
│   │   ├── dralthi.tres           # Ship data resource
│   │   ├── dralthi.glb            # 3D model
│   │   ├── dralthi.png            # Texture
│   │   └── assets/                # Feature-specific assets
│   │       ├── effects/           # Ship-specific effects
│   │       │   ├── thrusters/     # Thruster effects
│   │       │   │   ├── thruster01.webp
│   │       │   │   └── thrusterglow01.webp
│   │       │   └── shield_hits/   # Shield hit effects
│   │       │       └── shieldhit01a.webp
│   │       └── sounds/            # Ship-specific sounds
│   │           └── engine_loop.ogg # Engine sound
│   └── _shared/                   # Shared fighter assets
│       ├── cockpits/              # Shared cockpit models
│       │   ├── standard_cockpit.glb
│       │   └── standard_cockpit_material.tres
│       └── effects/               # Shared fighter effects
│           ├── engine_trail.png
│           └── shield_effect.png
├── capital_ships/                 # Capital ship entities
│   ├── tcs_behemoth/              # TCS Behemoth capital ship
│   │   ├── behemoth.tscn          # Scene file
│   │   ├── behemoth.gd            # Script file
│   │   ├── behemoth.tres          # Ship data resource
│   │   ├── behemoth.glb           # 3D model
│   │   ├── behemoth.png           # Texture
│   │   └── assets/                # Feature-specific assets
│   │       ├── effects/           # Ship-specific effects
│   │       │   ├── thrusters/     # Thruster effects
│   │       │   │   ├── thruster_capital.webp
│   │       │   │   └── thrusterglow_capital.webp
│   │       │   └── shield_hits/   # Shield hit effects
│   │       │       └── shieldhit_capital.webp
│   │       └── sounds/            # Ship-specific sounds
│   │           └── engine_loop.ogg # Engine sound
│   └── _shared/                   # Shared capital ship assets
│       ├── bridge_models/         # Shared bridge components
│       └── turret_models/         # Shared turret models
├── effects/                       # Effect entities
│   ├── explosion/                 # Explosion effect
│   │   ├── explosion.tscn         # Scene file
│   │   ├── explosion.gd           # Script file
│   │   ├── explosion.tres         # Effect data resource
│   │   ├── explosion_fire.png     # Texture
│   │   └── assets/                # Feature-specific assets
│   │       └── sounds/            # Effect-specific sounds
│   │           └── explosion_sound.ogg # Explosion sound
│   ├── shield_hit/                # Shield hit effect
│   │   ├── shield_hit.tscn        # Scene file
│   │   ├── shield_hit.gd          # Script file
│   │   ├── shield_hit.tres        # Effect data resource
│   │   ├── shield_hit_frames/     # Animation frames directory
│   │   │   ├── frame_0000.webp    # Animation frame 0
│   │   │   ├── frame_0001.webp    # Animation frame 1
│   │   │   └── frame_0002.webp    # Animation frame 2
│   │   └── assets/                # Feature-specific assets
│   │       └── sounds/            # Effect-specific sounds
│   │           └── shield_hit_sound.ogg # Shield hit sound
│   └── thruster/                  # Thruster effect
│       ├── thruster.tscn          # Scene file
│       ├── thruster.gd            # Script file
│       ├── thruster.tres          # Effect data resource
│       ├── thruster_glow.png      # Glow texture
│       └── assets/                # Feature-specific assets
│           └── sounds/            # Effect-specific sounds
│               └── thruster_sound.ogg # Thruster sound
└── ui/                            # UI feature elements
    ├── hud/                       # Heads-up display
    │   ├── player_hud.tscn        # Scene file
    │   ├── player_hud.gd          # Script file
    │   ├── gauges/                # Gauge elements
    │   │   ├── speed/             # Speed gauge
    │   │   ├── shields/           # Shield gauge
    │   │   └── weapons/           # Weapon gauge
    │   ├── indicators/            # Indicator elements
    │   │   ├── targets/           # Target indicators
    │   │   │   └── iff/           # IFF-specific target indicators
    │   │   │       ├── friendly_target.webp
    │   │   │       ├── hostile_target.webp
    │   │   │       ├── neutral_target.webp
    │   │   │       └── traitor_target.webp
    │   │   ├── warnings/          # Warning indicators
    │   │   └── status/            # Status indicators
    │   └── assets/                # Feature-specific assets
    │       └── sounds/            # UI-specific sounds
    │           ├── warning.ogg    # Warning sound
    │           └── target_acquired.ogg # Target acquired sound
    └── _shared/                   # Shared UI assets
        ├── fonts/                 # UI fonts
        ├── icons/                 # UI icons
        ├── themes/                # UI themes
        └── components/            # Reusable UI components
```

### Scripts Directory Structure
Reusable species and IFF system scripts are organized in the `/scripts/` directory, following the separation of concerns principle.

```
scripts/
├── entities/                      # Base entity scripts
│   ├── species/                   # Species-related scripts
│   │   ├── species_manager.gd     # Species management system
│   │   ├── species_data.gd        # Species data structure
│   │   └── species_factory.gd     # Species creation factory
│   └── iff/                       # IFF-related scripts
│       ├── iff_manager.gd         # IFF management system
│       ├── iff_data.gd            # IFF data structure
│       └── iff_relationships.gd   # IFF relationship logic
├── ai/                            # AI behavior scripts
│   ├── species_behavior.gd        # Species-specific AI behaviors
│   └── iff_tactics.gd             # IFF-based tactical decisions
└── utilities/                     # Utility functions and helpers
    └── resource_loader.gd         # Resource loading utilities
```

### Autoload Directory Structure
Global species and IFF management systems are implemented as autoload singletons, following the "Is this state or service truly global and required everywhere?" principle.

```
autoload/
├── species_manager.gd             # Global species management system
└── iff_manager.gd                 # Global IFF management system
```

## Data Conversion Strategy

### Configuration Files (.tbl)
Convert to Godot resources (.tres) organized appropriately:
- Species definitions from Species_defs.tbl to SpeciesData resources in `/assets/data/species/`
- IFF definitions from iff_defs.tbl to IFFData resources in `/assets/data/iff/`
- Use Godot's resource system for data-driven design with centralized management
- Preserve relationship matrices and property mappings with appropriate Godot data types

### Animation Conversion Process
1. **ANI to Sprite Sheet Converter**: Convert .ani animation files to sprite sheet animations with WebP format
2. **Frame Sequence Preservation**: Maintain animation frame sequences and timing properties
3. **Looping Properties**: Preserve looping and playback characteristics
4. **Resource Generation**: Create Godot .tres files with converted animation data
5. **Directory Organization**: Place converted animation files in appropriate directories following the structure above
6. **Validation**: Verify converted animations maintain original visual characteristics and timing

### Texture Conversion Process
1. **DDS to WebP Converter**: Convert .dds texture files to WebP format with quality preservation
2. **Mipmap Preservation**: Maintain mipmap levels and compression settings
3. **Alpha Channel Handling**: Preserve alpha channels for transparency effects
4. **Resource Generation**: Create Godot .tres files with converted texture data
5. **Directory Organization**: Place converted texture files in appropriate directories following the structure above
6. **Validation**: Verify converted textures maintain original visual quality and properties

## Example Mapping

### For Terran species:
- Species_defs.tbl entry → /assets/data/species/terran_species.tres
- thruster01.ani → /assets/animations/effects/thrusters/thruster01.webp
- shieldhit01a.ani → /assets/animations/effects/shield_hits/shieldhit01a.webp
- debris01a.dds → /assets/textures/effects/debris/debris01a.webp
- thrusterglow01.dds → /assets/textures/effects/thrusters/thrusterglow01.webp

### For Friendly IFF:
- iff_defs.tbl entry → /assets/data/iff/friendly_iff.tres
- Friendly color definition (24, 72, 232) → /assets/textures/ui/hud/radar/iff_colors/friendly.webp
- Friendly target box → /assets/textures/ui/hud/iff/friendly/target_box.webp
- Friendly radar blip → /assets/textures/ui/hud/radar/blips/friendly.webp

### For Shield Hit Effect (species-specific):
- Effect definition → /features/effects/shield_hit/shield_hit.tres
- Animation frames from shieldhit01a.ani → /features/effects/shield_hit/shield_hit_frames/
- Sound effect → /features/effects/shield_hit/assets/sounds/shield_hit_sound.ogg

## Relationship to Other Assets
Species and IFF assets are closely related to:
- **Ship System**: Ships inherit species properties for thruster animations, debris behavior, and visual effects
- **AI System**: AI behavior is influenced by species characteristics and IFF relationships
- **Weapon System**: Weapon targeting is affected by IFF relationships
- **Effect System**: Visual effects use species-specific animations and textures
- **UI System**: HUD and radar displays use IFF color codes and blip graphics
- **Audio System**: Voice acting and music are organized by species/IFF
- **Mission System**: Mission objectives and events are influenced by species and IFF relationships
- **Species Manager**: Global species management system in `/autoload/species_manager.gd`
- **IFF Manager**: Global IFF management system in `/autoload/iff_manager.gd`

This organization follows the hybrid approach where truly global data assets are organized in the `/assets/data/` directory following the "Global Litmus Test" principle, while species-specific and IFF-specific effects are co-located with their respective features in the `/features/` directory. The structure maintains clear separation of concerns between different asset types while ensuring easy access to all species and IFF assets needed for game features.