# Species and IFF Asset Mapping

## Overview
This document maps the species and IFF definitions from Species_defs.tbl and iff_defs.tbl to their corresponding media assets in the Wing Commander Saga Hermes campaign.

## Species Asset Types

### Species Definitions (.tbl)
Species_defs.tbl and Species.tbl define different species with their properties:
- Terran - Human Confederation
- Kilrathi - Kilrathi Empire
- Pirate - Independent pirate factions
- Unknown - Unknown/neutral factions

Each species has specific properties:
- Thruster animation references
- Debris behavior characteristics
- Species-specific visual effects
- Hull and shield types
- Damage characteristics

### Species-Specific Assets

#### Terran Assets
- Ship models (.pof files)
- Ship textures (.pcx files)
- Engine sounds (.wav files)
- Thruster animations (.ani files)
- UI graphics for Terran faction
- Voice acting for Terran characters
- Music themes for Terran missions

#### Kilrathi Assets
- Ship models (.pof files)
- Ship textures (.pcx files)
- Engine sounds (.wav files)
- Thruster animations (.ani files)
- UI graphics for Kilrathi faction
- Voice acting for Kilrathi characters
- Music themes for Kilrathi missions

#### Pirate Assets
- Ship models (.pof files)
- Ship textures (.pcx files)
- Engine sounds (.wav files)
- Thruster animations (.ani files)
- UI graphics for Pirate faction
- Voice acting for Pirate characters
- Music themes for Pirate missions

## IFF Asset Types

### IFF Definitions (.tbl)
iff_defs.tbl defines identification friend or foe relationships:
- Friendly factions
- Hostile factions
- Neutral factions
- Unknown factions

Each IFF has properties:
- Color codes for radar/HUD display
- Relationship matrices
- Species affiliations
- Team assignments

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

## Target Structure
```
/data/species/                       # Species data definitions
├── terran/                          # Terran species data
│   ├── species.tres                 # Species definition
│   ├── ships/                       # Terran ship associations
│   ├── weapons/                     # Terran weapon associations
│   ├── effects/                     # Terran effect associations
│   └── ui/                          # Terran UI associations
├── kilrathi/                        # Kilrathi species data
│   ├── species.tres                 # Species definition
│   ├── ships/                       # Kilrathi ship associations
│   ├── weapons/                     # Kilrathi weapon associations
│   ├── effects/                     # Kilrathi effect associations
│   └── ui/                          # Kilrathi UI associations
├── pirate/                          # Pirate species data
│   ├── species.tres                 # Species definition
│   ├── ships/                       # Pirate ship associations
│   ├── weapons/                     # Pirate weapon associations
│   ├── effects/                     # Pirate effect associations
│   └── ui/                          # Pirate UI associations
└── unknown/                         # Unknown species data
    ├── species.tres                 # Species definition
    ├── ships/                       # Unknown ship associations
    ├── weapons/                     # Unknown weapon associations
    ├── effects/                     # Unknown effect associations
    └── ui/                          # Unknown UI associations

/data/iff/                           # IFF data definitions
├── friendly/                        # Friendly IFF data
│   ├── iff.tres                     # IFF definition
│   ├── colors.tres                  # Color definitions
│   ├── relationships.tres           # Relationship definitions
│   └── ui/                          # UI associations
├── hostile/                         # Hostile IFF data
│   ├── iff.tres                     # IFF definition
│   ├── colors.tres                  # Color definitions
│   ├── relationships.tres           # Relationship definitions
│   └── ui/                          # UI associations
├── neutral/                         # Neutral IFF data
│   ├── iff.tres                     # IFF definition
│   ├── colors.tres                  # Color definitions
│   ├── relationships.tres           # Relationship definitions
│   └── ui/                          # UI associations
└── unknown/                         # Unknown IFF data
    ├── iff.tres                     # IFF definition
    ├── colors.tres                  # Color definitions
    ├── relationships.tres           # Relationship definitions
    └── ui/                          # UI associations

/textures/ui/hud/                    # HUD textures directory
├── iff/                             # IFF-specific HUD elements
│   ├── friendly/                    # Friendly IFF elements
│   │   ├── target_box.webp          # Target box for friendly
│   │   ├── lock_indicator.webp      # Lock indicator for friendly
│   │   └── threat_warning.webp      # Threat warning for friendly
│   ├── hostile/                     # Hostile IFF elements
│   │   ├── target_box.webp          # Target box for hostile
│   │   ├── lock_indicator.webp      # Lock indicator for hostile
│   │   └── threat_warning.webp      # Threat warning for hostile
│   ├── neutral/                     # Neutral IFF elements
│   │   ├── target_box.webp          # Target box for neutral
│   │   ├── lock_indicator.webp      # Lock indicator for neutral
│   │   └── threat_warning.webp      # Threat warning for neutral
│   └── unknown/                     # Unknown IFF elements
│       ├── target_box.webp          # Target box for unknown
│       ├── lock_indicator.webp      # Lock indicator for unknown
│       └── threat_warning.webp      # Threat warning for unknown
└── radar/                           # Radar display elements
    ├── iff_colors/                  # IFF color definitions
    │   ├── friendly.webp            # Friendly color
    │   ├── hostile.webp             # Hostile color
    │   ├── neutral.webp             # Neutral color
    │   └── unknown.webp             # Unknown color
    └── blips/                       # Radar blip graphics
        ├── friendly.webp            # Friendly blip
        ├── hostile.webp             # Hostile blip
        ├── neutral.webp             # Neutral blip
        └── unknown.webp             # Unknown blip

/audio/voice/                        # Voice acting directory
├── terran/                          # Terran voice acting
│   ├── pilots/                      # Terran pilot voices
│   ├── command/                     # Terran command voices
│   ├── mission_control/             # Terran mission control voices
│   └── characters/                  # Terran character voices
├── kilrathi/                        # Kilrathi voice acting
│   ├── pilots/                      # Kilrathi pilot voices
│   ├── command/                     # Kilrathi command voices
│   ├── mission_control/             # Kilrathi mission control voices
│   └── characters/                  # Kilrathi character voices
└── pirate/                          # Pirate voice acting
    ├── pilots/                      # Pirate pilot voices
    ├── command/                     # Pirate command voices
    └── characters/                  # Pirate character voices

/audio/music/                        # Music directory
├── terran/                          # Terran music themes
│   ├── campaign/                    # Terran campaign music
│   ├── combat/                      # Terran combat music
│   └── ambient/                     # Terran ambient music
├── kilrathi/                        # Kilrathi music themes
│   ├── campaign/                    # Kilrathi campaign music
│   ├── combat/                      # Kilrathi combat music
│   └── ambient/                     # Kilrathi ambient music
└── pirate/                          # Pirate music themes
    ├── campaign/                    # Pirate campaign music
    ├── combat/                      # Pirate combat music
    └── ambient/                     # Pirate ambient music

/animations/effects/species/         # Species-specific effects
├── terran/                          # Terran effects
│   ├── thrusters/                   # Terran thruster animations
│   ├── weapons/                     # Terran weapon effects
│   └── explosions/                  # Terran explosion effects
├── kilrathi/                        # Kilrathi effects
│   ├── thrusters/                   # Kilrathi thruster animations
│   ├── weapons/                     # Kilrathi weapon effects
│   └── explosions/                  # Kilrathi explosion effects
└── pirate/                          # Pirate effects
    ├── thrusters/                   # Pirate thruster animations
    ├── weapons/                     # Pirate weapon effects
    └── explosions/                  # Pirate explosion effects
```

## Example Mapping
For Terran species:
- Species_defs.tbl entry → /data/species/terran/species.tres
- terran_thruster.ani → /animations/effects/species/terran/thrusters/terran_thruster.png
- terran_engine.wav → /audio/sfx/environment/space/terran/terran_engine.ogg
- terran_ship.pof → /entities/fighters/terran/ship/ship.glb
- terran_ship.pcx → /textures/ships/terran/ship/ship_diffuse.webp

For Friendly IFF:
- iff_defs.tbl entry → /data/iff/friendly/iff.tres
- friendly_color definition → /textures/ui/hud/radar/iff_colors/friendly.webp
- friendly_target_box.pcx → /textures/ui/hud/iff/friendly/target_box.webp