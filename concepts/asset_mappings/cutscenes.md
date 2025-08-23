# Explosions Asset Mapping

## Overview
This document maps the explosion definitions from weapon_expl.tbl and fireball.tbl to their corresponding visual and audio assets in the Wing Commander Saga Hermes campaign.

## Asset Types

### Explosion Definitions (.tbl)
Explosion definition tables define different types of explosive effects:
- weapon_expl.tbl - Weapon explosion effects
- fireball.tbl - Fireball and general explosion effects

Each explosion entry contains:
- Explosion name and description
- Visual effect references
- Audio effect references
- Physics parameters
- Damage characteristics
- Particle system properties
- Light emission properties
- Camera shake effects

Common explosion types:
- Small explosions (bullets, missiles)
- Medium explosions (fighters, small craft)
- Large explosions (capitals, stations)
- Shockwaves (area of effect waves)
- Debris clouds (fragmentation effects)
- Fireballs (burning effects)
- Electrical discharges (energy weapon impacts)
- Plasma bursts (high-energy explosions)
- Nuclear detonations (large-scale explosions)
- Antimatter reactions (exotic explosions)

### Visual Effects (.ani/.pcx)
Explosion visual assets:
- fireball_*.ani - Fireball animation sequences
- explosion_*.ani - Generic explosion animations
- debris_*.ani - Debris particle animations
- shockwave_*.ani - Shockwave effect animations
- smoke_*.ani - Smoke cloud animations
- flame_*.ani - Flame effect animations
- spark_*.ani - Spark particle animations
- glow_*.ani - Glow effect animations

Associated PCX textures:
- fireball_*.pcx - Fireball texture frames
- explosion_*.pcx - Explosion texture frames
- debris_*.pcx - Debris particle textures
- shockwave_*.pcx - Shockwave effect textures
- smoke_*.pcx - Smoke cloud textures
- flame_*.pcx - Flame effect textures
- spark_*.pcx - Spark particle textures
- glow_*.pcx - Glow effect textures

### Audio Effects (.wav/.ogg)
Explosion sound assets:
- expl_small_*.wav - Small explosion sounds
- expl_medium_*.wav - Medium explosion sounds
- expl_large_*.wav - Large explosion sounds
- shockwave_*.wav - Shockwave impact sounds
- debris_impact_*.wav - Debris impact sounds
- fire_*.wav - Burning fire sounds
- electrical_*.wav - Electrical discharge sounds
- plasma_*.wav - Plasma burst sounds
- nuclear_*.wav - Nuclear detonation sounds
- antimatter_*.wav - Antimatter reaction sounds

Audio effect properties:
- Volume levels for different distances
- Pitch variations for randomness
- Looping properties for sustained effects
- 3D positioning data
- Reverb and echo effects
- Layered sound combinations
- Fade in/out properties
- Doppler shift effects

### Particle Effects (.pcx/.png)
Explosion particle assets:
- particle_fire_*.pcx - Fire particle textures
- particle_smoke_*.pcx - Smoke particle textures
- particle_debris_*.pcx - Debris particle textures
- particle_spark_*.pcx - Spark particle textures
- particle_glow_*.pcx - Glow particle textures
- particle_flame_*.pcx - Flame particle textures
- particle_shockwave_*.pcx - Shockwave particle textures
- particle_electrical_*.pcx - Electrical discharge textures

Particle system properties:
- Emission rates and patterns
- Velocity and acceleration
- Lifetime and decay rates
- Size and scale variations
- Color and opacity changes
- Rotation and spin properties
- Gravity and physics effects
- Collision and bounce behaviors

## Target Structure
```
/data/effects/explosions/            # Explosion effect data definitions
├── small/                          # Small explosion effects
│   ├── bullets/                    # Bullet impact explosions
│   │   ├── kinetic/                # Kinetic bullet impacts
│   │   │   ├── standard.tres        # Standard kinetic impact
│   │   │   ├── armor_piercing.tres  # Armor-piercing impact
│   │   │   └── explosive.tres       # Explosive bullet impact
│   │   ├── energy/                 # Energy bullet impacts
│   │   │   ├── laser.tres           # Laser impact
│   │   │   ├── plasma.tres          # Plasma impact
│   │   │   └── particle.tres        # Particle beam impact
│   │   └── electromagnetic/         # Electromagnetic impacts
│   │       ├── emp.tres             # EMP effect
│   │       ├── ion.tres             # Ion effect
│   │       └── disruptor.tres       # Disruptor effect
│   ├── missiles/                   # Missile explosions
│   │   ├── kinetic/                # Kinetic missile impacts
│   │   │   ├── standard.tres        # Standard kinetic impact
│   │   │   ├── armor_piercing.tres  # Armor-piercing impact
│   │   │   └── shaped_charge.tres   # Shaped charge impact
│   │   ├── energy/                 # Energy missile impacts
│   │   │   ├── laser.tres           # Laser impact
│   │   │   ├── plasma.tres          # Plasma impact
│   │   │   └── particle.tres        # Particle beam impact
│   │   └── electromagnetic/         # Electromagnetic impacts
│   │       ├── emp.tres             # EMP effect
│   │       ├── ion.tres             # Ion effect
│   │       └── disruptor.tres       # Disruptor effect
│   └── mines/                      # Mine explosions
│       ├── proximity/               # Proximity mine detonations
│       │   ├── standard.tres        # Standard proximity detonation
│       │   ├── delayed.tres         # Delayed detonation
│       │   └── contact.tres         # Contact detonation
│       ├── timed/                  # Timed mine detonations
│       │   ├── standard.tres        # Standard timed detonation
│       │   ├── delayed.tres         # Delayed detonation
│       │   └── remote.tres          # Remote detonation
│       └── triggered/               # Triggered mine detonations
│           ├── standard.tres        # Standard triggered detonation
│           ├── delayed.tres         # Delayed detonation
│           └── manual.tres          # Manual detonation
├── medium/                         # Medium explosion effects
│   ├── fighters/                   # Fighter craft explosions
│   │   ├── terran/                 # Terran fighter explosions
│   │   │   ├── arrow/              # Arrow fighter explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   ├── rapier/             # Raptor fighter explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   ├── hellcat/            # Hellcat fighter explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   └── thunderbolt/        # Thunderbolt fighter explosion
│   │   │       ├── primary.tres     # Primary explosion
│   │   │       ├── secondary.tres   # Secondary explosion
│   │   │       └── debris.tres      # Debris cloud
│   │   ├── kilrathi/               # Kilrathi fighter explosions
│   │   │   ├── dralthi/            # Dralthi fighter explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   ├── strakha/            # Strakha fighter explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   ├── vaktoth/            # Vaktoth fighter explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   └── var'kann/           # Var'kann fighter explosion
│   │   │       ├── primary.tres     # Primary explosion
│   │   │       ├── secondary.tres   # Secondary explosion
│   │   │       └── debris.tres      # Debris cloud
│   │   └── pirate/                 # Pirate fighter explosions
│   │       ├── corsair/            # Corsair fighter explosion
│   │       │   ├── primary.tres     # Primary explosion
│   │       │   ├── secondary.tres   # Secondary explosion
│   │       │   └── debris.tres      # Debris cloud
│   │       ├── bloodfang/          # Bloodfang fighter explosion
│   │       │   ├── primary.tres     # Primary explosion
│   │       │   ├── secondary.tres   # Secondary explosion
│   │       │   └── debris.tres      # Debris cloud
│   │       ├── darket/             # Darket fighter explosion
│   │       │   ├── primary.tres     # Primary explosion
│   │       │   ├── secondary.tres   # Secondary explosion
│   │       │   └── debris.tres      # Debris cloud
│   │       └── banshee/            # Banshee fighter explosion
│   │           ├── primary.tres     # Primary explosion
│   │           ├── secondary.tres   # Secondary explosion
│   │           └── debris.tres      # Debris cloud
│   ├── small_craft/                # Small craft explosions
│   │   ├── shuttles/               # Shuttle explosions
│   │   │   ├── transport/          # Transport shuttle explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   ├── cargo/              # Cargo shuttle explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   └── personnel/          # Personnel shuttle explosion
│   │   │       ├── primary.tres     # Primary explosion
│   │   │       ├── secondary.tres   # Secondary explosion
│   │   │       └── debris.tres      # Debris cloud
│   │   ├── fighters/               # Fighter explosions (already covered)
│   │   └── drones/                 # Drone explosions
│   │       ├── reconnaissance/     # Reconnaissance drone explosion
│   │       │   ├── primary.tres     # Primary explosion
│   │       │   ├── secondary.tres   # Secondary explosion
│   │       │   └── debris.tres      # Debris cloud
│   │       ├── combat/             # Combat drone explosion
│   │       │   ├── primary.tres     # Primary explosion
│   │       │   ├── secondary.tres   # Secondary explosion
│   │       │   └── debris.tres      # Debris cloud
│   │       └── support/            # Support drone explosion
│   │           ├── primary.tres     # Primary explosion
│   │           ├── secondary.tres   # Secondary explosion
│   │           └── debris.tres      # Debris cloud
│   └── weapons/                    # Weapon explosion effects
│       ├── missiles/               # Missile explosions
│       │   ├── dart/               # Dart missile explosion
│       │   │   ├── primary.tres     # Primary explosion
│       │   │   ├── secondary.tres   # Secondary explosion
│       │   │   └── debris.tres      # Debris cloud
│       │   ├── javelin/            # Javelin missile explosion
│       │   │   ├── primary.tres     # Primary explosion
│       │   │   ├── secondary.tres   # Secondary explosion
│       │   │   └── debris.tres      # Debris cloud
│       │   ├── spiculum/           # Spiculum missile explosion
│       │   │   ├── primary.tres     # Primary explosion
│       │   │   ├── secondary.tres   # Secondary explosion
│       │   │   └── debris.tres      # Debris cloud
│       │   └── lance/              # Lance missile explosion
│       │       ├── primary.tres     # Primary explosion
│       │       ├── secondary.tres   # Secondary explosion
│       │       └── debris.tres      # Debris cloud
│       ├── torpedoes/              # Torpedo explosions
│       │   ├── photon/             # Photon torpedo explosion
│       │   │   ├── primary.tres     # Primary explosion
│       │   │   ├── secondary.tres   # Secondary explosion
│       │   │   └── debris.tres      # Debris cloud
│       │   ├── meson/              # Meson torpedo explosion
│       │   │   ├── primary.tres     # Primary explosion
│       │   │   ├── secondary.tres   # Secondary explosion
│       │   │   └── debris.tres      # Debris cloud
│       │   └── quantum/            # Quantum torpedo explosion
│       │       ├── primary.tres     # Primary explosion
│       │       ├── secondary.tres   # Secondary explosion
│       │       └── debris.tres      # Debris cloud
│       └── mines/                  # Mine explosions
│           ├── proximity/          # Proximity mine explosion
│           │   ├── primary.tres     # Primary explosion
│           │   ├── secondary.tres   # Secondary explosion
│           │   └── debris.tres      # Debris cloud
│           ├── contact/            # Contact mine explosion
│           │   ├── primary.tres     # Primary explosion
│           │   ├── secondary.tres   # Secondary explosion
│           │   └── debris.tres      # Debris cloud
│           └── timed/              # Timed mine explosion
│               ├── primary.tres     # Primary explosion
│               ├── secondary.tres   # Secondary explosion
│               └── debris.tres      # Debris cloud
├── large/                          # Large explosion effects
│   ├── capitals/                   # Capital ship explosions
│   │   ├── terran/                 # Terran capital ship explosions
│   │   │   ├── tigers_claw/        # Tiger's Claw explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   ├── tertiary.tres    # Tertiary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   ├── prowler/            # Prowler explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   ├── tertiary.tres    # Tertiary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   ├── venture/            # Venture explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   ├── tertiary.tres    # Tertiary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   └── behemoth/           # Behemoth explosion
│   │   │       ├── primary.tres     # Primary explosion
│   │   │       ├── secondary.tres   # Secondary explosion
│   │   │       ├── tertiary.tres    # Tertiary explosion
│   │   │       └── debris.tres      # Debris cloud
│   │   ├── kilrathi/               # Kilrathi capital ship explosions
│   │   │   ├── sahkra/             # Sahkra explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   ├── tertiary.tres    # Tertiary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   ├── jakhar/             # Jakhar explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   ├── tertiary.tres    # Tertiary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   ├── raktha/             # Raktha explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   ├── tertiary.tres    # Tertiary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   └── khar/               # Khar explosion
│   │   │       ├── primary.tres     # Primary explosion
│   │   │       ├── secondary.tres   # Secondary explosion
│   │   │       ├── tertiary.tres    # Tertiary explosion
│   │   │       └── debris.tres      # Debris cloud
│   │   └── pirate/                 # Pirate capital ship explosions
│   │       ├── corsair/            # Corsair capital explosion
│   │       │   ├── primary.tres     # Primary explosion
│   │       │   ├── secondary.tres   # Secondary explosion
│   │       │   ├── tertiary.tres    # Tertiary explosion
│   │       │   └── debris.tres      # Debris cloud
│   │       ├── dreadnought/        # Dreadnought explosion
│   │       │   ├── primary.tres     # Primary explosion
│   │       │   ├── secondary.tres   # Secondary explosion
│   │       │   ├── tertiary.tres    # Tertiary explosion
│   │       │   └── debris.tres      # Debris cloud
│   │       ├── frigate/            # Frigate explosion
│   │       │   ├── primary.tres     # Primary explosion
│   │       │   ├── secondary.tres   # Secondary explosion
│   │       │   ├── tertiary.tres    # Tertiary explosion
│   │       │   └── debris.tres      # Debris cloud
│   │       └── destroyer/          # Destroyer explosion
│   │           ├── primary.tres     # Primary explosion
│   │           ├── secondary.tres   # Secondary explosion
│   │           ├── tertiary.tres    # Tertiary explosion
│   │           └── debris.tres      # Debris cloud
│   ├── stations/                   # Station explosions
│   │   ├── supply_bases/           # Supply base explosions
│   │   │   ├── standard/           # Standard supply base explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   ├── tertiary.tres    # Tertiary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   ├── reinforced/         # Reinforced supply base explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   ├── tertiary.tres    # Tertiary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   └── fortified/          # Fortified supply base explosion
│   │   │       ├── primary.tres     # Primary explosion
│   │   │       ├── secondary.tres   # Secondary explosion
│   │   │       ├── tertiary.tres    # Tertiary explosion
│   │   │       └── debris.tres      # Debris cloud
│   │   ├── orbital_stations/       # Orbital station explosions
│   │   │   ├── standard/           # Standard orbital station explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   ├── tertiary.tres    # Tertiary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   ├── reinforced/         # Reinforced orbital station explosion
│   │   │   │   ├── primary.tres     # Primary explosion
│   │   │   │   ├── secondary.tres   # Secondary explosion
│   │   │   │   ├── tertiary.tres    # Tertiary explosion
│   │   │   │   └── debris.tres      # Debris cloud
│   │   │   └── fortified/          # Fortified orbital station explosion
│   │   │       ├── primary.tres     # Primary explosion
│   │   │       ├── secondary.tres   # Secondary explosion
│   │   │       ├── tertiary.tres    # Tertiary explosion
│   │   │       └── debris.tres      # Debris cloud
│   │   └── drydocks/               # Drydock explosions
│   │       ├── standard/           # Standard drydock explosion
│   │       │   ├── primary.tres     # Primary explosion
│   │       │   ├── secondary.tres   # Secondary explosion
│   │       │   ├── tertiary.tres    # Tertiary explosion
│   │       │   └── debris.tres      # Debris cloud
│   │       ├── reinforced/         # Reinforced drydock explosion
│   │       │   ├── primary.tres     # Primary explosion
│   │       │   ├── secondary.tres   # Secondary explosion
│   │       │   ├── tertiary.tres    # Tertiary explosion
│   │       │   └── debris.tres      # Debris cloud
│   │       └── fortified/          # Fortified drydock explosion
│   │           ├── primary.tres     # Primary explosion
│   │           ├── secondary.tres   # Secondary explosion
│   │           ├── tertiary.tres    # Tertiary explosion
│   │           └── debris.tres      # Debris cloud
│   └── installations/              # Installation explosions
│       ├── mining_facilities/      # Mining facility explosions
│       │   ├── standard/           # Standard mining facility explosion
│       │   │   ├── primary.tres     # Primary explosion
│       │   │   ├── secondary.tres   # Secondary explosion
│       │   │   ├── tertiary.tres    # Tertiary explosion
│       │   │   └── debris.tres      # Debris cloud
│       │   ├── reinforced/         # Reinforced mining facility explosion
│       │   │   ├── primary.tres     # Primary explosion
│       │   │   ├── secondary.tres   # Secondary explosion
│       │   │   ├── tertiary.tres    # Tertiary explosion
│       │   │   └── debris.tres      # Debris cloud
│       │   └── fortified/          # Fortified mining facility explosion
│       │       ├── primary.tres     # Primary explosion
│       │       ├── secondary.tres   # Secondary explosion
│       │       ├── tertiary.tres    # Tertiary explosion
│       │       └── debris.tres      # Debris cloud
│       ├── research_stations/      # Research station explosions
│       │   ├── standard/           # Standard research station explosion
│       │   │   ├── primary.tres     # Primary explosion
│       │   │   ├── secondary.tres   # Secondary explosion
│       │   │   ├── tertiary.tres    # Tertiary explosion
│       │   │   └── debris.tres      # Debris cloud
│       │   ├── reinforced/         # Reinforced research station explosion
│       │   │   ├── primary.tres     # Primary explosion
│       │   │   ├── secondary.tres   # Secondary explosion
│       │   │   ├── tertiary.tres    # Tertiary explosion
│       │   │   └── debris.tres      # Debris cloud
│       │   └── fortified/          # Fortified research station explosion
│       │       ├── primary.tres     # Primary explosion
│       │       ├── secondary.tres   # Secondary explosion
│       │       ├── tertiary.tres    # Tertiary explosion
│       │       └── debris.tres      # Debris cloud
│       └── manufacturing_plants/   # Manufacturing plant explosions
│           ├── standard/           # Standard manufacturing plant explosion
│           │   ├── primary.tres     # Primary explosion
│           │   ├── secondary.tres   # Secondary explosion
│           │   ├── tertiary.tres    # Tertiary explosion
│           │   └── debris.tres      # Debris cloud
│           ├── reinforced/         # Reinforced manufacturing plant explosion
│           │   ├── primary.tres     # Primary explosion
│           │   ├── secondary.tres   # Secondary explosion
│           │   ├── tertiary.tres    # Tertiary explosion
│           │   └── debris.tres      # Debris cloud
│           └── fortified/          # Fortified manufacturing plant explosion
│               ├── primary.tres     # Primary explosion
│               ├── secondary.tres   # Secondary explosion
│               ├── tertiary.tres    # Tertiary explosion
│               └── debris.tres      # Debris cloud
└── special/                        # Special explosion effects
    ├── shockwaves/                 # Shockwave effects
    │   ├── kinetic/                # Kinetic shockwaves
    │   │   ├── standard.tres        # Standard kinetic shockwave
    │   │   ├── enhanced.tres        # Enhanced kinetic shockwave
    │   │   └── massive.tres         # Massive kinetic shockwave
    │   ├── energy/                 # Energy shockwaves
    │   │   ├── standard.tres        # Standard energy shockwave
    │   │   ├── enhanced.tres        # Enhanced energy shockwave
    │   │   └── massive.tres         # Massive energy shockwave
    │   └── electromagnetic/         # Electromagnetic shockwaves
    │       ├── standard.tres        # Standard electromagnetic shockwave
    │       ├── enhanced.tres        # Enhanced electromagnetic shockwave
    │       └── massive.tres         # Massive electromagnetic shockwave
    ├── fireballs/                  # Fireball effects
    │   ├── small/                  # Small fireballs
    │   │   ├── standard.tres        # Standard small fireball
    │   │   ├── intense.tres         # Intense small fireball
    │   │   └── weak.tres            # Weak small fireball
    │   ├── medium/                 # Medium fireballs
    │   │   ├── standard.tres        # Standard medium fireball
    │   │   ├── intense.tres         # Intense medium fireball
    │   │   └── weak.tres            # Weak medium fireball
    │   └── large/                  # Large fireballs
    │       ├── standard.tres        # Standard large fireball
    │       ├── intense.tres         # Intense large fireball
    │       └── weak.tres            # Weak large fireball
    ├── debris_clouds/              # Debris cloud effects
    │   ├── metal/                  # Metal debris clouds
    │   │   ├── standard.tres        # Standard metal debris cloud
    │   │   ├── dense.tres           # Dense metal debris cloud
    │   │   └── sparse.tres          # Sparse metal debris cloud
    │   ├── organic/                # Organic debris clouds
    │   │   ├── standard.tres        # Standard organic debris cloud
    │   │   ├── dense.tres           # Dense organic debris cloud
    │   │   └── sparse.tres          # Sparse organic debris cloud
    │   └── mixed/                  # Mixed debris clouds
    │       ├── standard.tres        # Standard mixed debris cloud
    │       ├── dense.tres           # Dense mixed debris cloud
    │       └── sparse.tres          # Sparse mixed debris cloud
    ├── electrical/                 # Electrical effects
    │   ├── lightning/              # Lightning effects
    │   │   ├── standard.tres        # Standard lightning effect
    │   │   ├── intense.tres         # Intense lightning effect
    │   │   └── weak.tres            # Weak lightning effect
    │   ├── arcs/                   # Electrical arc effects
    │   │   ├── standard.tres        # Standard electrical arc
    │   │   ├── intense.tres         # Intense electrical arc
    │   │   └── weak.tres            # Weak electrical arc
    │   └── discharges/             # Electrical discharge effects
    │       ├── standard.tres        # Standard electrical discharge
    │       ├── intense.tres         # Intense electrical discharge
    │       └── weak.tres            # Weak electrical discharge
    ├── plasma/                     # Plasma effects
    │   ├── bursts/                 # Plasma burst effects
    │   │   ├── standard.tres        # Standard plasma burst
    │   │   ├── intense.tres         # Intense plasma burst
    │   │   └── weak.tres            # Weak plasma burst
    │   ├── streams/                # Plasma stream effects
    │   │   ├── standard.tres        # Standard plasma stream
    │   │   ├── intense.tres         # Intense plasma stream
    │   │   └── weak.tres            # Weak plasma stream
    │   └── clouds/                 # Plasma cloud effects
    │       ├── standard.tres        # Standard plasma cloud
    │       ├── intense.tres         # Intense plasma cloud
    │       └── weak.tres            # Weak plasma cloud
    ├── nuclear/                    # Nuclear effects
    │   ├── detonations/            # Nuclear detonation effects
    │   │   ├── standard.tres        # Standard nuclear detonation
    │   │   ├── enhanced.tres        # Enhanced nuclear detonation
    │   │   └── massive.tres         # Massive nuclear detonation
    │   ├── radiation/              # Radiation effects
    │   │   ├── standard.tres        # Standard radiation effect
    │   │   ├── enhanced.tres        # Enhanced radiation effect
    │   │   └── massive.tres         # Massive radiation effect
    │   └── fallout/                # Fallout effects
    │       ├── standard.tres        # Standard fallout effect
    │       ├── enhanced.tres        # Enhanced fallout effect
    │       └── massive.tres         # Massive fallout effect
    └── antimatter/                 # Antimatter effects
        ├── reactions/              # Antimatter reaction effects
        │   ├── standard.tres        # Standard antimatter reaction
        │   ├── enhanced.tres        # Enhanced antimatter reaction
        │   └── massive.tres         # Massive antimatter reaction
        ├── annihilation/           # Annihilation effects
        │   ├── standard.tres        # Standard annihilation effect
        │   ├── enhanced.tres        # Enhanced annihilation effect
        │   └── massive.tres         # Massive annihilation effect
        └── containment_failures/   # Containment failure effects
            ├── standard.tres        # Standard containment failure
            ├── enhanced.tres        # Enhanced containment failure
            └── massive.tres         # Massive containment failure

/animations/effects/explosions/      # Explosion animation directory
├── small/                          # Small explosion animations
│   ├── bullets/                    # Bullet impact animations
│   │   ├── kinetic/                # Kinetic bullet impacts
│   │   │   ├── standard/           # Standard kinetic impacts
│   │   │   │   ├── impact.png       # Impact frame sequence
│   │   │   │   ├── flash.png        # Flash frame sequence
│   │   │   │   └── sparks.png       # Spark frame sequence
│   │   │   ├── armor_piercing/     # Armor-piercing impacts
│   │   │   │   ├── impact.png       # Impact frame sequence
│   │   │   │   ├── flash.png        # Flash frame sequence
│   │   │   │   └── sparks.png       # Spark frame sequence
│   │   │   └── explosive/          # Explosive bullet impacts
│   │   │       ├── impact.png       # Impact frame sequence
│   │   │       ├── flash.png        # Flash frame sequence
│   │   │       └── sparks.png       # Spark frame sequence
│   │   ├── energy/                 # Energy bullet impacts
│   │   │   ├── laser/              # Laser impacts
│   │   │   │   ├── impact.png       # Impact frame sequence
│   │   │   │   ├── flash.png        # Flash frame sequence
│   │   │   │   └── sparks.png       # Spark frame sequence
│   │   │   ├── plasma/             # Plasma impacts
│   │   │   │   ├── impact.png       # Impact frame sequence
│   │   │   │   ├── flash.png        # Flash frame sequence
│   │   │   │   └── sparks.png       # Spark frame sequence
│   │   │   └── particle/           # Particle beam impacts
│   │   │       ├── impact.png       # Impact frame sequence
│   │   │       ├── flash.png        # Flash frame sequence
│   │   │       └── sparks.png       # Spark frame sequence
│   │   └── electromagnetic/         # Electromagnetic impacts
│   │       ├── emp/                # EMP effects
│   │       │   ├── impact.png       # Impact frame sequence
│   │       │   ├── flash.png        # Flash frame sequence
│   │       │   └── sparks.png       # Spark frame sequence
│   │       ├── ion/                # Ion effects
│   │       │   ├── impact.png       # Impact frame sequence
│   │       │   ├── flash.png        # Flash frame sequence
│   │       │   └── sparks.png       # Spark frame sequence
│   │       └── disruptor/          # Disruptor effects
│   │           ├── impact.png       # Impact frame sequence
│   │           ├── flash.png        # Flash frame sequence
│   │           └── sparks.png       # Spark frame sequence
│   ├── missiles/                   # Missile explosion animations
│   │   ├── kinetic/                # Kinetic missile explosions
│   │   │   ├── standard/           # Standard kinetic explosions
│   │   │   │   ├── explosion.png    # Explosion frame sequence
│   │   │   │   ├── debris.png       # Debris frame sequence
│   │   │   │   └── smoke.png        # Smoke frame sequence
│   │   │   ├── armor_piercing/     # Armor-piercing explosions
│   │   │   │   ├── explosion.png    # Explosion frame sequence
│   │   │   │   ├── debris.png       # Debris frame sequence
│   │   │   │   └── smoke.png        # Smoke frame sequence
│   │   │   └── shaped_charge/      # Shaped charge explosions
│   │   │       ├── explosion.png    # Explosion frame sequence
│   │   │       ├── debris.png       # Debris frame sequence
│   │   │       └── smoke.png        # Smoke frame sequence
│   │   ├── energy/                 # Energy missile explosions
│   │   │   ├── laser/              # Laser explosions
│   │   │   │   ├── explosion.png    # Explosion frame sequence
│   │   │   │   ├── debris.png       # Debris frame sequence
│   │   │   │   └── smoke.png        # Smoke frame sequence
│   │   │   ├── plasma/             # Plasma explosions
│   │   │   │   ├── explosion.png    # Explosion frame sequence
│   │   │   │   ├── debris.png       # Debris frame sequence
│   │   │   │   └── smoke.png        # Smoke frame sequence
│   │   │   └── particle/           # Particle beam explosions
│   │   │       ├── explosion.png    # Explosion frame sequence
│   │   │       ├── debris.png       # Debris frame sequence
│   │   │       └── smoke.png        # Smoke frame sequence
│   │   └── electromagnetic/         # Electromagnetic explosions
│   │       ├── emp/                # EMP explosions
│   │       │   ├── explosion.png    # Explosion frame sequence
│   │       │   ├── debris.png       # Debris frame sequence
│   │       │   └── smoke.png        # Smoke frame sequence
│   │       ├── ion/                # Ion explosions
│   │       │   ├── explosion.png    # Explosion frame sequence
│   │       │   ├── debris.png       # Debris frame sequence
│   │       │   └── smoke.png        # Smoke frame sequence
│   │       └── disruptor/          # Disruptor explosions
│   │           ├── explosion.png    # Explosion frame sequence
│   │           ├── debris.png       # Debris frame sequence
│   │           └── smoke.png        # Smoke frame sequence
│   └── mines/                      # Mine explosion animations
│       ├── proximity/               # Proximity mine detonations
│       │   ├── standard/           # Standard proximity detonations
│       │   │   ├── explosion.png    # Explosion frame sequence
│       │   │   ├── debris.png       # Debris frame sequence
│       │   │   └── smoke.png        # Smoke frame sequence
│       │   ├── delayed/            # Delayed detonations
│       │   │   ├── explosion.png    # Explosion frame sequence
│       │   │   ├── debris.png       # Debris frame sequence
│       │   │   └── smoke.png        # Smoke frame sequence
│       │   └── contact/            # Contact detonations
│       │       ├── explosion.png    # Explosion frame sequence
│       │       ├── debris.png       # Debris frame sequence
│       │       └── smoke.png        # Smoke frame sequence
│       ├── timed/                  # Timed mine detonations
│       │   ├── standard/           # Standard timed detonations
│       │   │   ├── explosion.png    # Explosion frame sequence
│       │   │   ├── debris.png       # Debris frame sequence
│       │   │   └── smoke.png        # Smoke frame sequence
│       │   ├── delayed/            # Delayed detonations
│       │   │   ├── explosion.png    # Explosion frame sequence
│       │   │   ├── debris.png       # Debris frame sequence
│       │   │   └── smoke.png        # Smoke frame sequence
│       │   └── remote/             # Remote detonations
│       │       ├── explosion.png    # Explosion frame sequence
│       │       ├── debris.png       # Debris frame sequence
│       │       └── smoke.png        # Smoke frame sequence
│       └── triggered/               # Triggered mine detonations
│           ├── standard/           # Standard triggered detonations
│           │   ├── explosion.png    # Explosion frame sequence
│           │   ├── debris.png       # Debris frame sequence
│           │   └── smoke.png        # Smoke frame sequence
│           ├── delayed/            # Delayed detonations
│           │   ├── explosion.png    # Explosion frame sequence
│           │   ├── debris.png       # Debris frame sequence
│           │   └── smoke.png        # Smoke frame sequence
│           └── manual/             # Manual detonations
│               ├── explosion.png    # Explosion frame sequence
│               ├── debris.png       # Debris frame sequence
│               └── smoke.png        # Smoke frame sequence
├── medium/                         # Medium explosion animations
│   ├── fighters/                   # Fighter craft explosions
│   │   ├── terran/                 # Terran fighter explosions
│   │   │   ├── arrow/              # Arrow fighter explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── wreckage/       # Wreckage explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   ├── rapier/             # Raptor fighter explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── wreckage/       # Wreckage explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   ├── hellcat/            # Hellcat fighter explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── wreckage/       # Wreckage explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   └── thunderbolt/        # Thunderbolt fighter explosion
│   │   │       ├── primary/        # Primary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       ├── secondary/      # Secondary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       └── wreckage/       # Wreckage explosion sequence
│   │   │           ├── explosion.png # Explosion frame sequence
│   │   │           ├── debris.png    # Debris frame sequence
│   │   │           └── smoke.png     # Smoke frame sequence
│   │   ├── kilrathi/               # Kilrathi fighter explosions
│   │   │   ├── dralthi/            # Dralthi fighter explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── wreckage/       # Wreckage explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   ├── strakha/            # Strakha fighter explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── wreckage/       # Wreckage explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   ├── vaktoth/            # Vaktoth fighter explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── wreckage/       # Wreckage explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   └── var'kann/           # Var'kann fighter explosion
│   │   │       ├── primary/        # Primary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       ├── secondary/      # Secondary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       └── wreckage/       # Wreckage explosion sequence
│   │   │           ├── explosion.png # Explosion frame sequence
│   │   │           ├── debris.png    # Debris frame sequence
│   │   │           └── smoke.png     # Smoke frame sequence
│   │   └── pirate/                 # Pirate fighter explosions
│   │       ├── corsair/            # Corsair fighter explosion
│   │       │   ├── primary/        # Primary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   ├── secondary/      # Secondary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   └── wreckage/       # Wreckage explosion sequence
│   │       │       ├── explosion.png # Explosion frame sequence
│   │       │       ├── debris.png    # Debris frame sequence
│   │       │       └── smoke.png     # Smoke frame sequence
│   │       ├── bloodfang/          # Bloodfang fighter explosion
│   │       │   ├── primary/        # Primary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   ├── secondary/      # Secondary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   └── wreckage/       # Wreckage explosion sequence
│   │       │       ├── explosion.png # Explosion frame sequence
│   │       │       ├── debris.png    # Debris frame sequence
│   │       │       └── smoke.png     # Smoke frame sequence
│   │       ├── darket/             # Darket fighter explosion
│   │       │   ├── primary/        # Primary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   ├── secondary/      # Secondary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   └── wreckage/       # Wreckage explosion sequence
│   │       │       ├── explosion.png # Explosion frame sequence
│   │       │       ├── debris.png    # Debris frame sequence
│   │       │       └── smoke.png     # Smoke frame sequence
│   │       └── banshee/            # Banshee fighter explosion
│   │           ├── primary/        # Primary explosion sequence
│   │           │   ├── explosion.png # Explosion frame sequence
│   │           │   ├── debris.png    # Debris frame sequence
│   │           │   └── smoke.png     # Smoke frame sequence
│   │           ├── secondary/      # Secondary explosion sequence
│   │           │   ├── explosion.png # Explosion frame sequence
│   │           │   ├── debris.png    # Debris frame sequence
│   │           │   └── smoke.png     # Smoke frame sequence
│   │           └── wreckage/       # Wreckage explosion sequence
│   │               ├── explosion.png # Explosion frame sequence
│   │               ├── debris.png    # Debris frame sequence
│   │               └── smoke.png     # Smoke frame sequence
│   ├── small_craft/                # Small craft explosions
│   │   ├── shuttles/               # Shuttle explosions
│   │   │   ├── transport/          # Transport shuttle explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── wreckage/       # Wreckage explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   ├── cargo/              # Cargo shuttle explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── wreckage/       # Wreckage explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   └── personnel/          # Personnel shuttle explosion
│   │   │       ├── primary/        # Primary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       ├── secondary/      # Secondary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       └── wreckage/       # Wreckage explosion sequence
│   │   │           ├── explosion.png # Explosion frame sequence
│   │   │           ├── debris.png    # Debris frame sequence
│   │   │           └── smoke.png     # Smoke frame sequence
│   │   └── drones/                 # Drone explosions
│   │       ├── reconnaissance/     # Reconnaissance drone explosion
│   │       │   ├── primary/        # Primary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   ├── secondary/      # Secondary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   └── wreckage/       # Wreckage explosion sequence
│   │       │       ├── explosion.png # Explosion frame sequence
│   │       │       ├── debris.png    # Debris frame sequence
│   │       │       └── smoke.png     # Smoke frame sequence
│   │       ├── combat/             # Combat drone explosion
│   │       │   ├── primary/        # Primary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   ├── secondary/      # Secondary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   └── wreckage/       # Wreckage explosion sequence
│   │       │       ├── explosion.png # Explosion frame sequence
│   │       │       ├── debris.png    # Debris frame sequence
│   │       │       └── smoke.png     # Smoke frame sequence
│   │       └── support/            # Support drone explosion
│   │           ├── primary/        # Primary explosion sequence
│   │           │   ├── explosion.png # Explosion frame sequence
│   │           │   ├── debris.png    # Debris frame sequence
│   │           │   └── smoke.png     # Smoke frame sequence
│   │           ├── secondary/      # Secondary explosion sequence
│   │           │   ├── explosion.png # Explosion frame sequence
│   │           │   ├── debris.png    # Debris frame sequence
│   │           │   └── smoke.png     # Smoke frame sequence
│   │           └── wreckage/       # Wreckage explosion sequence
│   │               ├── explosion.png # Explosion frame sequence
│   │               ├── debris.png    # Debris frame sequence
│   │               └── smoke.png     # Smoke frame sequence
│   └── weapons/                    # Weapon explosion animations
│       ├── missiles/               # Missile explosions
│       │   ├── dart/               # Dart missile explosion
│       │   │   ├── primary/        # Primary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   ├── secondary/      # Secondary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   └── fragmentation/  # Fragmentation sequence
│       │   │       ├── explosion.png # Explosion frame sequence
│       │   │       ├── debris.png    # Debris frame sequence
│       │   │       └── smoke.png     # Smoke frame sequence
│       │   ├── javelin/            # Javelin missile explosion
│       │   │   ├── primary/        # Primary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   ├── secondary/      # Secondary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   └── fragmentation/  # Fragmentation sequence
│       │   │       ├── explosion.png # Explosion frame sequence
│       │   │       ├── debris.png    # Debris frame sequence
│       │   │       └── smoke.png     # Smoke frame sequence
│       │   ├── spiculum/           # Spiculum missile explosion
│       │   │   ├── primary/        # Primary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   ├── secondary/      # Secondary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   └── fragmentation/  # Fragmentation sequence
│       │   │       ├── explosion.png # Explosion frame sequence
│       │   │       ├── debris.png    # Debris frame sequence
│       │   │       └── smoke.png     # Smoke frame sequence
│       │   └── lance/              # Lance missile explosion
│       │       ├── primary/        # Primary explosion sequence
│       │       │   ├── explosion.png # Explosion frame sequence
│       │       │   ├── debris.png    # Debris frame sequence
│       │       │   └── smoke.png     # Smoke frame sequence
│       │       ├── secondary/      # Secondary explosion sequence
│       │       │   ├── explosion.png # Explosion frame sequence
│       │       │   ├── debris.png    # Debris frame sequence
│       │       │   └── smoke.png     # Smoke frame sequence
│       │       └── fragmentation/  # Fragmentation sequence
│       │           ├── explosion.png # Explosion frame sequence
│       │           ├── debris.png    # Debris frame sequence
│       │           └── smoke.png     # Smoke frame sequence
│       ├── torpedoes/              # Torpedo explosions
│       │   ├── photon/             # Photon torpedo explosion
│       │   │   ├── primary/        # Primary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   ├── secondary/      # Secondary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   └── shockwave/      # Shockwave sequence
│       │   │       ├── explosion.png # Explosion frame sequence
│       │   │       ├── debris.png    # Debris frame sequence
│       │   │       └── smoke.png     # Smoke frame sequence
│       │   ├── meson/              # Meson torpedo explosion
│       │   │   ├── primary/        # Primary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   ├── secondary/      # Secondary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   └── shockwave/      # Shockwave sequence
│       │   │       ├── explosion.png # Explosion frame sequence
│       │   │       ├── debris.png    # Debris frame sequence
│       │   │       └── smoke.png     # Smoke frame sequence
│       │   └── quantum/            # Quantum torpedo explosion
│       │       ├── primary/        # Primary explosion sequence
│       │       │   ├── explosion.png # Explosion frame sequence
│       │       │   ├── debris.png    # Debris frame sequence
│       │       │   └── smoke.png     # Smoke frame sequence
│       │       ├── secondary/      # Secondary explosion sequence
│       │       │   ├── explosion.png # Explosion frame sequence
│       │       │   ├── debris.png    # Debris frame sequence
│       │       │   └── smoke.png     # Smoke frame sequence
│       │       └── shockwave/      # Shockwave sequence
│       │           ├── explosion.png # Explosion frame sequence
│       │           ├── debris.png    # Debris frame sequence
│       │           └── smoke.png     # Smoke frame sequence
│       └── mines/                  # Mine explosions
│           ├── proximity/          # Proximity mine explosion
│           │   ├── primary/        # Primary explosion sequence
│           │   │   ├── explosion.png # Explosion frame sequence
│           │   │   ├── debris.png    # Debris frame sequence
│           │   │   └── smoke.png     # Smoke frame sequence
│           │   ├── secondary/      # Secondary explosion sequence
│           │   │   ├── explosion.png # Explosion frame sequence
│           │   │   ├── debris.png    # Debris frame sequence
│           │   │   └── smoke.png     # Smoke frame sequence
│           │   └── fragmentation/  # Fragmentation sequence
│           │       ├── explosion.png # Explosion frame sequence
│           │       ├── debris.png    # Debris frame sequence
│           │       └── smoke.png     # Smoke frame sequence
│           ├── contact/            # Contact mine explosion
│           │   ├── primary/        # Primary explosion sequence
│           │   │   ├── explosion.png # Explosion frame sequence
│           │   │   ├── debris.png    # Debris frame sequence
│           │   │   └── smoke.png     # Smoke frame sequence
│           │   ├── secondary/      # Secondary explosion sequence
│           │   │   ├── explosion.png # Explosion frame sequence
│           │   │   ├── debris.png    # Debris frame sequence
│           │   │   └── smoke.png     # Smoke frame sequence
│           │   └── fragmentation/  # Fragmentation sequence
│           │       ├── explosion.png # Explosion frame sequence
│           │       ├── debris.png    # Debris frame sequence
│           │       └── smoke.png     # Smoke frame sequence
│           └── timed/              # Timed mine explosion
│               ├── primary/        # Primary explosion sequence
│               │   ├── explosion.png # Explosion frame sequence
│               │   ├── debris.png    # Debris frame sequence
│               │   └── smoke.png     # Smoke frame sequence
│               ├── secondary/      # Secondary explosion sequence
│               │   ├── explosion.png # Explosion frame sequence
│               │   ├── debris.png    # Debris frame sequence
│               │   └── smoke.png     # Smoke frame sequence
│               └── fragmentation/  # Fragmentation sequence
│                   ├── explosion.png # Explosion frame sequence
│                   ├── debris.png    # Debris frame sequence
│                   └── smoke.png     # Smoke frame sequence
├── large/                          # Large explosion animations
│   ├── capitals/                   # Capital ship explosions
│   │   ├── terran/                 # Terran capital ship explosions
│   │   │   ├── tigers_claw/        # Tiger's Claw explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── tertiary/       # Tertiary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── final/          # Final explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   ├── prowler/            # Prowler explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── tertiary/       # Tertiary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── final/          # Final explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   ├── venture/            # Venture explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── tertiary/       # Tertiary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── final/          # Final explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   └── behemoth/           # Behemoth explosion
│   │   │       ├── primary/        # Primary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       ├── secondary/      # Secondary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       ├── tertiary/       # Tertiary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       └── final/          # Final explosion sequence
│   │   │           ├── explosion.png # Explosion frame sequence
│   │   │           ├── debris.png    # Debris frame sequence
│   │   │           └── smoke.png     # Smoke frame sequence
│   │   ├── kilrathi/               # Kilrathi capital ship explosions
│   │   │   ├── sahkra/             # Sahkra explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── tertiary/       # Tertiary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── final/          # Final explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   ├── jakhar/             # Jakhar explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── tertiary/       # Tertiary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── final/          # Final explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   ├── raktha/             # Raktha explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── tertiary/       # Tertiary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── final/          # Final explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   └── khar/               # Khar explosion
│   │   │       ├── primary/        # Primary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       ├── secondary/      # Secondary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       ├── tertiary/       # Tertiary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       └── final/          # Final explosion sequence
│   │   │           ├── explosion.png # Explosion frame sequence
│   │   │           ├── debris.png    # Debris frame sequence
│   │   │           └── smoke.png     # Smoke frame sequence
│   │   └── pirate/                 # Pirate capital ship explosions
│   │       ├── corsair/            # Corsair capital explosion
│   │       │   ├── primary/        # Primary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   ├── secondary/      # Secondary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   ├── tertiary/       # Tertiary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   └── final/          # Final explosion sequence
│   │       │       ├── explosion.png # Explosion frame sequence
│   │       │       ├── debris.png    # Debris frame sequence
│   │       │       └── smoke.png     # Smoke frame sequence
│   │       ├── dreadnought/        # Dreadnought explosion
│   │       │   ├── primary/        # Primary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   ├── secondary/      # Secondary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   ├── tertiary/       # Tertiary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   └── final/          # Final explosion sequence
│   │       │       ├── explosion.png # Explosion frame sequence
│   │       │       ├── debris.png    # Debris frame sequence
│   │       │       └── smoke.png     # Smoke frame sequence
│   │       ├── frigate/            # Frigate explosion
│   │       │   ├── primary/        # Primary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   ├── secondary/      # Secondary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   ├── tertiary/       # Tertiary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   └── final/          # Final explosion sequence
│   │       │       ├── explosion.png # Explosion frame sequence
│   │       │       ├── debris.png    # Debris frame sequence
│   │       │       └── smoke.png     # Smoke frame sequence
│   │       └── destroyer/          # Destroyer explosion
│   │           ├── primary/        # Primary explosion sequence
│   │           │   ├── explosion.png # Explosion frame sequence
│   │           │   ├── debris.png    # Debris frame sequence
│   │           │   └── smoke.png     # Smoke frame sequence
│   │           ├── secondary/      # Secondary explosion sequence
│   │           │   ├── explosion.png # Explosion frame sequence
│   │           │   ├── debris.png    # Debris frame sequence
│   │           │   └── smoke.png     # Smoke frame sequence
│   │           ├── tertiary/       # Tertiary explosion sequence
│   │           │   ├── explosion.png # Explosion frame sequence
│   │           │   ├── debris.png    # Debris frame sequence
│   │           │   └── smoke.png     # Smoke frame sequence
│   │           └── final/          # Final explosion sequence
│   │               ├── explosion.png # Explosion frame sequence
│   │               ├── debris.png    # Debris frame sequence
│   │               └── smoke.png     # Smoke frame sequence
│   ├── stations/                   # Station explosions
│   │   ├── supply_bases/           # Supply base explosions
│   │   │   ├── standard/           # Standard supply base explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── tertiary/       # Tertiary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── final/          # Final explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   ├── reinforced/         # Reinforced supply base explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── tertiary/       # Tertiary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── final/          # Final explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   └── fortified/          # Fortified supply base explosion
│   │   │       ├── primary/        # Primary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       ├── secondary/      # Secondary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       ├── tertiary/       # Tertiary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       └── final/          # Final explosion sequence
│   │   │           ├── explosion.png # Explosion frame sequence
│   │   │           ├── debris.png    # Debris frame sequence
│   │   │           └── smoke.png     # Smoke frame sequence
│   │   ├── orbital_stations/       # Orbital station explosions
│   │   │   ├── standard/           # Standard orbital station explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── tertiary/       # Tertiary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── final/          # Final explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   ├── reinforced/         # Reinforced orbital station explosion
│   │   │   │   ├── primary/        # Primary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── secondary/      # Secondary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   ├── tertiary/       # Tertiary explosion sequence
│   │   │   │   │   ├── explosion.png # Explosion frame sequence
│   │   │   │   │   ├── debris.png    # Debris frame sequence
│   │   │   │   │   └── smoke.png     # Smoke frame sequence
│   │   │   │   └── final/          # Final explosion sequence
│   │   │   │       ├── explosion.png # Explosion frame sequence
│   │   │   │       ├── debris.png    # Debris frame sequence
│   │   │   │       └── smoke.png     # Smoke frame sequence
│   │   │   └── fortified/          # Fortified orbital station explosion
│   │   │       ├── primary/        # Primary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       ├── secondary/      # Secondary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       ├── tertiary/       # Tertiary explosion sequence
│   │   │       │   ├── explosion.png # Explosion frame sequence
│   │   │       │   ├── debris.png    # Debris frame sequence
│   │   │       │   └── smoke.png     # Smoke frame sequence
│   │   │       └── final/          # Final explosion sequence
│   │   │           ├── explosion.png # Explosion frame sequence
│   │   │           ├── debris.png    # Debris frame sequence
│   │   │           └── smoke.png     # Smoke frame sequence
│   │   └── drydocks/               # Drydock explosions
│   │       ├── standard/           # Standard drydock explosion
│   │       │   ├── primary/        # Primary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   ├── secondary/      # Secondary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   ├── tertiary/       # Tertiary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   └── final/          # Final explosion sequence
│   │       │       ├── explosion.png # Explosion frame sequence
│   │       │       ├── debris.png    # Debris frame sequence
│   │       │       └── smoke.png     # Smoke frame sequence
│   │       ├── reinforced/         # Reinforced drydock explosion
│   │       │   ├── primary/        # Primary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   ├── secondary/      # Secondary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   ├── tertiary/       # Tertiary explosion sequence
│   │       │   │   ├── explosion.png # Explosion frame sequence
│   │       │   │   ├── debris.png    # Debris frame sequence
│   │       │   │   └── smoke.png     # Smoke frame sequence
│   │       │   └── final/          # Final explosion sequence
│   │       │       ├── explosion.png # Explosion frame sequence
│   │       │       ├── debris.png    # Debris frame sequence
│   │       │       └── smoke.png     # Smoke frame sequence
│   │       └── fortified/          # Fortified drydock explosion
│   │           ├── primary/        # Primary explosion sequence
│   │           │   ├── explosion.png # Explosion frame sequence
│   │           │   ├── debris.png    # Debris frame sequence
│   │           │   └── smoke.png     # Smoke frame sequence
│   │           ├── secondary/      # Secondary explosion sequence
│   │           │   ├── explosion.png # Explosion frame sequence
│   │           │   ├── debris.png    # Debris frame sequence
│   │           │   └── smoke.png     # Smoke frame sequence
│   │           ├── tertiary/       # Tertiary explosion sequence
│   │           │   ├── explosion.png # Explosion frame sequence
│   │           │   ├── debris.png    # Debris frame sequence
│   │           │   └── smoke.png     # Smoke frame sequence
│   │           └── final/          # Final explosion sequence
│   │               ├── explosion.png # Explosion frame sequence
│   │               ├── debris.png    # Debris frame sequence
│   │               └── smoke.png     # Smoke frame sequence
│   └── installations/              # Installation explosions
│       ├── mining_facilities/      # Mining facility explosions
│       │   ├── standard/           # Standard mining facility explosion
│       │   │   ├── primary/        # Primary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   ├── secondary/      # Secondary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   ├── tertiary/       # Tertiary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   └── final/          # Final explosion sequence
│       │   │       ├── explosion.png # Explosion frame sequence
│       │   │       ├── debris.png    # Debris frame sequence
│       │   │       └── smoke.png     # Smoke frame sequence
│       │   ├── reinforced/         # Reinforced mining facility explosion
│       │   │   ├── primary/        # Primary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   ├── secondary/      # Secondary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   ├── tertiary/       # Tertiary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   └── final/          # Final explosion sequence
│       │   │       ├── explosion.png # Explosion frame sequence
│       │   │       ├── debris.png    # Debris frame sequence
│       │   │       └── smoke.png     # Smoke frame sequence
│       │   └── fortified/          # Fortified mining facility explosion
│       │       ├── primary/        # Primary explosion sequence
│       │       │   ├── explosion.png # Explosion frame sequence
│       │       │   ├── debris.png    # Debris frame sequence
│       │       │   └── smoke.png     # Smoke frame sequence
│       │       ├── secondary/      # Secondary explosion sequence
│       │       │   ├── explosion.png # Explosion frame sequence
│       │       │   ├── debris.png    # Debris frame sequence
│       │       │   └── smoke.png     # Smoke frame sequence
│       │       ├── tertiary/       # Tertiary explosion sequence
│       │       │   ├── explosion.png # Explosion frame sequence
│       │       │   ├── debris.png    # Debris frame sequence
│       │       │   └── smoke.png     # Smoke frame sequence
│       │       └── final/          # Final explosion sequence
│       │           ├── explosion.png # Explosion frame sequence
│       │           ├── debris.png    # Debris frame sequence
│       │           └── smoke.png     # Smoke frame sequence
│       ├── research_stations/      # Research station explosions
│       │   ├── standard/           # Standard research station explosion
│       │   │   ├── primary/        # Primary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   ├── secondary/      # Secondary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   ├── tertiary/       # Tertiary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   └── final/          # Final explosion sequence
│       │   │       ├── explosion.png # Explosion frame sequence
│       │   │       ├── debris.png    # Debris frame sequence
│       │   │       └── smoke.png     # Smoke frame sequence
│       │   ├── reinforced/         # Reinforced research station explosion
│       │   │   ├── primary/        # Primary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   ├── secondary/      # Secondary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   ├── tertiary/       # Tertiary explosion sequence
│       │   │   │   ├── explosion.png # Explosion frame sequence
│       │   │   │   ├── debris.png    # Debris frame sequence
│       │   │   │   └── smoke.png     # Smoke frame sequence
│       │   │   └── final/          # Final explosion sequence
│       │   │       ├── explosion.png # Explosion frame sequence
│       │   │       ├── debris.png    # Debris frame sequence
│       │   │       └── smoke.png     # Smoke frame sequence
│       │   └── fortified/          # Fortified research station explosion
│       │       ├── primary/        # Primary explosion sequence
│       │       │   ├── explosion.png # Explosion frame sequence
│       │       │   ├── debris.png    # Debris frame sequence
│       │       │   └── smoke.png     # Smoke frame sequence
│       │       ├── secondary/      # Secondary explosion sequence
│       │       │   ├── explosion.png # Explosion frame sequence
│       │       │   ├── debris.png    # Debris frame sequence
│       │       │   └── smoke.png     # Smoke frame sequence
│       │       ├── tertiary/       # Tertiary explosion sequence
│       │       │   ├── explosion.png # Explosion frame sequence
│       │       │   ├── debris.png    # Debris frame sequence
│       │       │   └── smoke.png     # Smoke frame sequence
│       │       └── final/          # Final explosion sequence
│       │           ├── explosion.png # Explosion frame sequence
│       │           ├── debris.png    # Debris frame sequence
│       │           └── smoke.png     # Smoke frame sequence
│       └── manufacturing_plants/   # Manufacturing plant explosions
│           ├── standard/           # Standard manufacturing plant explosion
│           │   ├── primary/        # Primary explosion sequence
│           │   │   ├── explosion.png # Explosion frame sequence
│           │   │   ├── debris.png    # Debris frame sequence
│           │   │   └── smoke.png     # Smoke frame sequence
│           │   ├── secondary/      # Secondary explosion sequence
│           │   │   ├── explosion.png # Explosion frame sequence
│           │   │   ├── debris.png    # Debris frame sequence
│           │   │   └── smoke.png     # Smoke frame sequence
│           │   ├── tertiary/       # Tertiary explosion sequence
│           │   │   ├── explosion.png # Explosion frame sequence
│           │   │   ├── debris.png    # Debris frame sequence
│           │   │   └── smoke.png     # Smoke frame sequence
│           │   └── final/          # Final explosion sequence
│           │       ├── explosion.png # Explosion frame sequence
│           │       ├── debris.png    # Debris frame sequence
│           │       └── smoke.png     # Smoke frame sequence
│           ├── reinforced/         # Reinforced manufacturing plant explosion
│           │   ├── primary/        # Primary explosion sequence
│           │   │   ├── explosion.png # Explosion frame sequence
│           │   │   ├── debris.png    # Debris frame sequence
│           │   │   └── smoke.png     # Smoke frame sequence
│           │   ├── secondary/      # Secondary explosion sequence
│           │   │   ├── explosion.png # Explosion frame sequence
│           │   │   ├── debris.png    # Debris frame sequence
│           │   │   └── smoke.png     # Smoke frame sequence
│           │   ├── tertiary/       # Tertiary explosion sequence
│           │   │   ├── explosion.png # Explosion frame sequence
│           │   │   ├── debris.png    # Debris frame sequence
│           │   │   └── smoke.png     # Smoke frame sequence
│           │   └── final/          # Final explosion sequence
│           │       ├── explosion.png # Explosion frame sequence
│           │       ├── debris.png    # Debris frame sequence
│           │       └── smoke.png     # Smoke frame sequence
│           └── fortified/          # Fortified manufacturing plant explosion
│               ├── primary/        # Primary explosion sequence
│               │   ├── explosion.png # Explosion frame sequence
│               │   ├── debris.png    # Debris frame sequence
│               │   └── smoke.png     # Smoke frame sequence
│               ├── secondary/      # Secondary explosion sequence
│               │   ├── explosion.png # Explosion frame sequence
│               │   ├── debris.png    # Debris frame sequence
│               │   └── smoke.png     # Smoke frame sequence
│               ├── tertiary/       # Tertiary explosion sequence
│               │   ├── explosion.png # Explosion frame sequence
│               │   ├── debris.png    # Debris frame sequence
│               │   └── smoke.png     # Smoke frame sequence
│               └── final/          # Final explosion sequence
│                   ├── explosion.png # Explosion frame sequence
│                   ├── debris.png    # Debris frame sequence
│                   └── smoke.png     # Smoke frame sequence
└── special/                        # Special explosion animations
    ├── shockwaves/                 # Shockwave animations
    │   ├── kinetic/                # Kinetic shockwaves
    │   │   ├── standard/           # Standard kinetic shockwave
    │   │   │   ├── wave_front.png    # Wave front animation
    │   │   │   ├── pressure_ring.png # Pressure ring animation
    │   │   │   └── energy_burst.png  # Energy burst animation
    │   │   ├── enhanced/           # Enhanced kinetic shockwave
    │   │   │   ├── wave_front.png    # Wave front animation
    │   │   │   ├── pressure_ring.png # Pressure ring animation
    │   │   │   └── energy_burst.png  # Energy burst animation
    │   │   └── massive/            # Massive kinetic shockwave
    │   │       ├── wave_front.png    # Wave front animation
    │   │       ├── pressure_ring.png # Pressure ring animation
    │   │       └── energy_burst.png  # Energy burst animation
    │   ├── energy/                 # Energy shockwaves
    │   │   ├── standard/           # Standard energy shockwave
    │   │   │   ├── wave_front.png    # Wave front animation
    │   │   │   ├── pressure_ring.png # Pressure ring animation
    │   │   │   └── energy_burst.png  # Energy burst animation
    │   │   ├── enhanced/           # Enhanced energy shockwave
    │   │   │   ├── wave_front.png    # Wave front animation
    │   │   │   ├── pressure_ring.png # Pressure ring animation
    │   │   │   └── energy_burst.png  # Energy burst animation
    │   │   └── massive/            # Massive energy shockwave
    │   │       ├── wave_front.png    # Wave front animation
    │   │       ├── pressure_ring.png # Pressure ring animation
    │   │       └── energy_burst.png  # Energy burst animation
    │   └── electromagnetic/         # Electromagnetic shockwaves
    │       ├── standard/           # Standard electromagnetic shockwave
    │       │   ├── wave_front.png    # Wave front animation
    │       │   ├── pressure_ring.png # Pressure ring animation
    │       │   └── energy_burst.png  # Energy burst animation
    │       ├── enhanced/           # Enhanced electromagnetic shockwave
    │       │   ├── wave_front.png    # Wave front animation
    │       │   ├── pressure_ring.png # Pressure ring animation
    │       │   └── energy_burst.png  # Energy burst animation
    │       └── massive/            # Massive electromagnetic shockwave
    │           ├── wave_front.png    # Wave front animation
    │           ├── pressure_ring.png # Pressure ring animation
    │           └── energy_burst.png  # Energy burst animation
    ├── fireballs/                  # Fireball animations
    │   ├── small/                  # Small fireballs
    │   │   ├── standard/           # Standard small fireball
    │   │   │   ├── core.png         # Core animation
    │   │   │   ├── outer_flame.png  # Outer flame animation
    │   │   │   └── smoke_trail.png  # Smoke trail animation
    │   │   ├── intense/            # Intense small fireball
    │   │   │   ├── core.png         # Core animation
    │   │   │   ├── outer_flame.png  # Outer flame animation
    │   │   │   └── smoke_trail.png  # Smoke trail animation
    │   │   └── weak/               # Weak small fireball
    │   │       ├── core.png         # Core animation
    │   │       ├── outer_flame.png  # Outer flame animation
    │   │       └── smoke_trail.png  # Smoke trail animation
    │   ├── medium/                 # Medium fireballs
    │   │   ├── standard/           # Standard medium fireball
    │   │   │   ├── core.png         # Core animation
    │   │   │   ├── outer_flame.png  # Outer flame animation
    │   │   │   └── smoke_trail.png  # Smoke trail animation
    │   │   ├── intense/            # Intense medium fireball
    │   │   │   ├── core.png         # Core animation
    │   │   │   ├── outer_flame.png  # Outer flame animation
    │   │   │   └── smoke_trail.png  # Smoke trail animation
    │   │   └── weak/               # Weak medium fireball
    │   │       ├── core.png         # Core animation
    │   │       ├── outer_flame.png  # Outer flame animation
    │   │       └── smoke_trail.png  # Smoke trail animation
    │   └── large/                  # Large fireballs
    │       ├── standard/           # Standard large fireball
    │       │   ├── core.png         # Core animation
    │       │   ├── outer_flame.png  # Outer flame animation
    │       │   └── smoke_trail.png  # Smoke trail animation
    │       ├── intense/            # Intense large fireball
    │       │   ├── core.png         # Core animation
    │       │   ├── outer_flame.png  # Outer flame animation
    │       │   └── smoke_trail.png  # Smoke trail animation
    │       └── weak/               # Weak large fireball
    │           ├── core.png         # Core animation
    │           ├── outer_flame.png  # Outer flame animation
    │           └── smoke_trail.png  # Smoke trail animation
    ├── debris_clouds/              # Debris cloud animations
    │   ├── metal/                  # Metal debris clouds
    │   │   ├── standard/           # Standard metal debris cloud
    │   │   │   ├── fragment_spray.png # Fragment spray animation
    │   │   │   ├── dust_cloud.png    # Dust cloud animation
    │   │   │   └── particle_swarm.png # Particle swarm animation
    │   │   ├── dense/              # Dense metal debris cloud
    │   │   │   ├── fragment_spray.png # Fragment spray animation
    │   │   │   ├── dust_cloud.png    # Dust cloud animation
    │   │   │   └── particle_swarm.png # Particle swarm animation
    │   │   └── sparse/             # Sparse metal debris cloud
    │   │       ├── fragment_spray.png # Fragment spray animation
    │   │       ├── dust_cloud.png    # Dust cloud animation
    │   │       └── particle_swarm.png # Particle swarm animation
    │   ├── organic/                # Organic debris clouds
    │   │   ├── standard/           # Standard organic debris cloud
    │   │   │   ├── fragment_spray.png # Fragment spray animation
    │   │   │   ├── dust_cloud.png    # Dust cloud animation
    │   │   │   └── particle_swarm.png # Particle swarm animation
    │   │   ├── dense/              # Dense organic debris cloud
    │   │   │   ├── fragment_spray.png # Fragment spray animation
    │   │   │   ├── dust_cloud.png    # Dust cloud animation
    │   │   │   └── particle_swarm.png # Particle swarm animation
    │   │   └── sparse/             # Sparse organic debris cloud
    │   │       ├── fragment_spray.png # Fragment spray animation
    │   │       ├── dust_cloud.png    # Dust cloud animation
    │   │       └── particle_swarm.png # Particle swarm animation
    │   └── mixed/                  # Mixed debris clouds
    │       ├── standard/           # Standard mixed debris cloud
    │       │   ├── fragment_spray.png # Fragment spray animation
    │       │   ├── dust_cloud.png    # Dust cloud animation
    │       │   └── particle_swarm.png # Particle swarm animation
    │       ├── dense/              # Dense mixed debris cloud
    │       │   ├── fragment_spray.png # Fragment spray animation
    │       │   ├── dust_cloud.png    # Dust cloud animation
    │       │   └── particle_swarm.png # Particle swarm animation
    │       └── sparse/             # Sparse mixed debris cloud
    │           ├── fragment_spray.png # Fragment spray animation
    │           ├── dust_cloud.png    # Dust cloud animation
    │           └── particle_swarm.png # Particle swarm animation
    ├── electrical/                 # Electrical animations
    │   ├── lightning/              # Lightning animations
    │   │   ├── standard/           # Standard lightning effect
    │   │   │   ├── bolt_strike.png   # Bolt strike animation
    │   │   │   ├── energy_arcs.png   # Energy arcs animation
    │   │   │   └── electric_flash.png # Electric flash animation
    │   │   ├── intense/            # Intense lightning effect
    │   │   │   ├── bolt_strike.png   # Bolt strike animation
    │   │   │   ├── energy_arcs.png   # Energy arcs animation
    │   │   │   └── electric_flash.png # Electric flash animation
    │   │   └── weak/               # Weak lightning effect
    │   │       ├── bolt_strike.png   # Bolt strike animation
    │   │       ├── energy_arcs.png   # Energy arcs animation
    │   │       └── electric_flash.png # Electric flash animation
    │   ├── arcs/                   # Electrical arc animations
    │   │   ├── standard/           # Standard electrical arc
    │   │   │   ├── arc_strike.png    # Arc strike animation
    │   │   │   ├── energy_flow.png   # Energy flow animation
    │   │   │   └── electric_spark.png # Electric spark animation
    │   │   ├── intense/            # Intense electrical arc
    │   │   │   ├── arc_strike.png    # Arc strike animation
    │   │   │   ├── energy_flow.png   # Energy flow animation
    │   │   │   └── electric_spark.png # Electric spark animation
    │   │   └── weak/               # Weak electrical arc
    │   │       ├── arc_strike.png    # Arc strike animation
    │   │       ├── energy_flow.png   # Energy flow animation
    │   │       └── electric_spark.png # Electric spark animation
    │   └── discharges/             # Electrical discharge animations
    │       ├── standard/           # Standard electrical discharge
    │       │   ├── discharge_burst.png # Discharge burst animation
    │       │   ├── energy_pulse.png    # Energy pulse animation
    │       │   └── electric_flash.png  # Electric flash animation
    │       ├── intense/            # Intense electrical discharge
    │       │   ├── discharge_burst.png # Discharge burst animation
    │       │   ├── energy_pulse.png    # Energy pulse animation
    │       │   └── electric_flash.png  # Electric flash animation
    │       └── weak/               # Weak electrical discharge
    │           ├── discharge_burst.png # Discharge burst animation
    │           ├── energy_pulse.png    # Energy pulse animation
    │           └── electric_flash.png  # Electric flash animation
    ├── plasma/                     # Plasma animations
    │   ├── bursts/                 # Plasma burst animations
    │   │   ├── standard/           # Standard plasma burst
    │   │   │   ├── energy_burst.png  # Energy burst animation
    │   │   │   ├── plasma_sphere.png # Plasma sphere animation
    │   │   │   └── energy_flash.png  # Energy flash animation
    │   │   ├── intense/            # Intense plasma burst
    │   │   │   ├── energy_burst.png  # Energy burst animation
    │   │   │   ├── plasma_sphere.png # Plasma sphere animation
    │   │   │   └── energy_flash.png  # Energy flash animation
    │   │   └── weak/               # Weak plasma burst
    │   │       ├── energy_burst.png  # Energy burst animation
    │   │       ├── plasma_sphere.png # Plasma sphere animation
    │   │       └── energy_flash.png  # Energy flash animation
    │   ├── streams/                # Plasma stream animations
    │   │   ├── standard/           # Standard plasma stream
    │   │   │   ├── energy_stream.png # Energy stream animation
    │   │   │   ├── plasma_flow.png   # Plasma flow animation
    │   │   │   └── energy_trail.png  # Energy trail animation
    │   │   ├── intense/            # Intense plasma stream
    │   │   │   ├── energy_stream.png # Energy stream animation
    │   │   │   ├── plasma_flow.png   # Plasma flow animation
    │   │   │   └── energy_trail.png  # Energy trail animation
    │   │   └── weak/               # Weak plasma stream
    │   │       ├── energy_stream.png # Energy stream animation
    │   │       ├── plasma_flow.png   # Plasma flow animation
    │   │       └── energy_trail.png  # Energy trail animation
    │   └── clouds/                 # Plasma cloud animations
    │       ├── standard/           # Standard plasma cloud
    │       │   ├── energy_cloud.png  # Energy cloud animation
    │       │   ├── plasma_swirl.png  # Plasma swirl animation
    │       │   └── energy_glow.png   # Energy glow animation
    │       ├── intense/            # Intense plasma cloud
    │       │   ├── energy_cloud.png  # Energy cloud animation
    │       │   ├── plasma_swirl.png  # Plasma swirl animation
    │       │   └── energy_glow.png   # Energy glow animation
    │       └── weak/               # Weak plasma cloud
    │           ├── energy_cloud.png  # Energy cloud animation
    │           ├── plasma_swirl.png  # Plasma swirl animation
    │           └── energy_glow.png   # Energy glow animation
    ├── nuclear/                    # Nuclear animations
    │   ├── detonations/            # Nuclear detonation animations
    │   │   ├── standard/           # Standard nuclear detonation
    │   │   │   ├── mushroom_cloud.png # Mushroom cloud animation
    │   │   │   ├── radiation_burst.png # Radiation burst animation
    │   │   │   └── thermal_flash.png  # Thermal flash animation
    │   │   ├── enhanced/           # Enhanced nuclear detonation
    │   │   │   ├── mushroom_cloud.png # Mushroom cloud animation
    │   │   │   ├── radiation_burst.png # Radiation burst animation
    │   │   │   └── thermal_flash.png  # Thermal flash animation
    │   │   └── massive/            # Massive nuclear detonation
    │   │       ├── mushroom_cloud.png # Mushroom cloud animation
    │   │       ├── radiation_burst.png # Radiation burst animation
    │   │       └── thermal_flash.png  # Thermal flash animation
    │   ├── radiation/              # Radiation animations
    │   │   ├── standard/           # Standard radiation effect
    │   │   │   ├── radiation_wave.png # Radiation wave animation
    │   │   │   ├── energy_pulse.png   # Energy pulse animation
    │   │   │   └── toxic_cloud.png    # Toxic cloud animation
    │   │   ├── enhanced/           # Enhanced radiation effect
    │   │   │   ├── radiation_wave.png # Radiation wave animation
    │   │   │   ├── energy_pulse.png   # Energy pulse animation
    │   │   │   └── toxic_cloud.png    # Toxic cloud animation
    │   │   └── massive/            # Massive radiation effect
    │   │       ├── radiation_wave.png # Radiation wave animation
    │   │       ├── energy_pulse.png   # Energy pulse animation
    │   │       └── toxic_cloud.png    # Toxic cloud animation
    │   └── fallout/                # Fallout animations
    │       ├── standard/           # Standard fallout effect
    │       │   ├── radioactive_dust.png # Radioactive dust animation
    │       │   ├── contamination_cloud.png # Contamination cloud animation
    │       │   └── toxic_precipitation.png # Toxic precipitation animation
    │       ├── enhanced/           # Enhanced fallout effect
    │       │   ├── radioactive_dust.png # Radioactive dust animation
    │       │   ├── contamination_cloud.png # Contamination cloud animation
    │       │   └── toxic_precipitation.png # Toxic precipitation animation
    │       └── massive/            # Massive fallout effect
    │           ├── radioactive_dust.png # Radioactive dust animation
    │           ├── contamination_cloud.png # Contamination cloud animation
    │           └── toxic_precipitation.png # Toxic precipitation animation
    └── antimatter/                 # Antimatter animations
        ├── reactions/              # Antimatter reaction animations
        │   ├── standard/           # Standard antimatter reaction
        │   │   ├── matter_annihilation.png # Matter annihilation animation
        │   │   ├── energy_release.png      # Energy release animation
        │   │   └── spacetime_distortion.png # Spacetime distortion animation
        │   ├── enhanced/           # Enhanced antimatter reaction
        │   │   ├── matter_annihilation.png # Matter annihilation animation
        │   │   ├── energy_release.png      # Energy release animation
        │   │   └── spacetime_distortion.png # Spacetime distortion animation
        │   └── massive/            # Massive antimatter reaction
        │       ├── matter_annihilation.png # Matter annihilation animation
        │       ├── energy_release.png      # Energy release animation
        │       └── spacetime_distortion.png # Spacetime distortion animation
        ├── annihilation/           # Annihilation animations
        │   ├── standard/           # Standard annihilation effect
        │   │   ├── particle_collision.png  # Particle collision animation
        │   │   ├── energy_explosion.png    # Energy explosion animation
        │   │   └── void_creation.png       # Void creation animation
        │   ├── enhanced/           # Enhanced annihilation effect
        │   │   ├── particle_collision.png  # Particle collision animation
        │   │   ├── energy_explosion.png    # Energy explosion animation
        │   │   └── void_creation.png       # Void creation animation
        │   └── massive/            # Massive annihilation effect
        │       ├── particle_collision.png  # Particle collision animation
        │       ├── energy_explosion.png    # Energy explosion animation
        │       └── void_creation.png       # Void creation animation
        └── containment_failures/   # Containment failure animations
            ├── standard/           # Standard containment failure
            │   ├── barrier_breach.png   # Barrier breach animation
            │   ├── energy_leak.png      # Energy leak animation
            │   └── system_malfunction.png # System malfunction animation
            ├── enhanced/           # Enhanced containment failure
            │   ├── barrier_breach.png   # Barrier breach animation
            │   ├── energy_leak.png      # Energy leak animation
            │   └── system_malfunction.png # System malfunction animation
            └── massive/            # Massive containment failure
                ├── barrier_breach.png   # Barrier breach animation
                ├── energy_leak.png      # Energy leak animation
                └── system_malfunction.png # System malfunction animation

/textures/effects/explosions/      # Explosion texture directory
├── small/                          # Small explosion textures
│   ├── bullets/                    # Bullet impact textures
│   │   ├── kinetic/                # Kinetic bullet impact textures
│   │   │   ├── standard/           # Standard kinetic impact textures
│   │   │   │   ├── impact.webp      # Impact texture
│   │   │   │   ├── flash.webp       # Flash texture
│   │   │   │   └── sparks.webp      # Spark texture
│   │   │   ├── armor_piercing/     # Armor-piercing impact textures
│   │   │   │   ├── impact.webp      # Impact texture
│   │   │   │   ├── flash.webp       # Flash texture
│   │   │   │   └── sparks.webp      # Spark texture
│   │   │   └── explosive/          # Explosive bullet impact textures
│   │   │       ├── impact.webp      # Impact texture
│   │   │       ├── flash.webp       # Flash texture
│   │   │       └── sparks.webp      # Spark texture
│   │   ├── energy/                 # Energy bullet impact textures
│   │   │   ├── laser/              # Laser impact textures
│   │   │   │   ├── impact.webp      # Impact texture
│   │   │   │   ├── flash.webp       # Flash texture
│   │   │   │   └── sparks.webp      # Spark texture
│   │   │   ├── plasma/             # Plasma impact textures
│   │   │   │   ├── impact.webp      # Impact texture
│   │   │   │   ├── flash.webp       # Flash texture
│   │   │   │   └── sparks.webp      # Spark texture
│   │   │   └── particle/           # Particle beam impact textures
│   │   │       ├── impact.webp      # Impact texture
│   │   │       ├── flash.webp       # Flash texture
│   │   │       └── sparks.webp      # Spark texture
│   │   └── electromagnetic/         # Electromagnetic impact textures
│   │       ├── emp/                # EMP effect textures
│   │       │   ├── impact.webp      # Impact texture
│   │       │   ├── flash.webp       # Flash texture
│   │       │   └── sparks.webp      # Spark texture
│   │       ├── ion/                # Ion effect textures
│   │       │   ├── impact.webp      # Impact texture
│   │       │   ├── flash.webp       # Flash texture
│   │       │   └── sparks.webp      # Spark texture
│   │       └── disruptor/          # Disruptor effect textures
│   │           ├── impact.webp      # Impact texture
│   │           ├── flash.webp       # Flash texture
│   │           └── sparks.webp      # Spark texture
│   ├── missiles/                   # Missile explosion textures
│   │   ├── kinetic/                # Kinetic missile explosion textures
│   │   │   ├── standard/           # Standard kinetic explosion textures
│   │   │   │   ├── explosion.webp   # Explosion texture
│   │   │   │   ├── debris.webp      # Debris texture
│   │   │   │   └── smoke.webp       # Smoke texture
│   │   │   ├── armor_piercing/     # Armor-piercing explosion textures
│   │   │   │   ├── explosion.webp   # Explosion texture
│   │   │   │   ├── debris.webp      # Debris texture
│   │   │   │   └── smoke.webp       # Smoke texture
│   │   │   └── shaped_charge/      # Shaped charge explosion textures
│   │   │       ├── explosion.webp   # Explosion texture
│   │   │       ├── debris.webp      # Debris texture
│   │   │       └── smoke.webp       # Smoke texture
│   │   ├── energy/                 # Energy missile explosion textures
│   │   │   ├── laser/              # Laser explosion textures
│   │   │   │   ├── explosion.webp   # Explosion texture
│   │   │   │   ├── debris.webp      # Debris texture
│   │   │   │   └── smoke.webp       # Smoke texture
│   │   │   ├── plasma/             # Plasma explosion textures
│   │   │   │   ├── explosion.webp   # Explosion texture
│   │   │   │   ├── debris.webp      # Debris texture
│   │   │   │   └── smoke.webp       # Smoke texture
│   │   │   └── particle/           # Particle beam explosion textures
│   │   │       ├── explosion.webp   # Explosion texture
│   │   │       ├── debris.webp      # Debris texture
│   │   │       └── smoke.webp       # Smoke texture
│   │   └── electromagnetic/         # Electromagnetic explosion textures
│   │       ├── emp/                # EMP explosion textures
│   │       │   ├── explosion.webp   # Explosion texture
│   │       │   ├── debris.webp      # Debris texture
│   │       │   └── smoke.webp       # Smoke texture
│   │       ├── ion/                # Ion explosion textures
│   │       │   ├── explosion.webp   # Explosion texture
│   │       │   ├── debris.webp      # Debris texture
│   │       │   └── smoke.webp       # Smoke texture
│   │       └── disruptor/          # Disruptor explosion textures
│   │           ├── explosion.webp   # Explosion texture
│   │           ├── debris.webp      # Debris texture
│   │           └── smoke.webp       # Smoke texture
│   └── mines/                      # Mine explosion textures
│       ├── proximity/               # Proximity mine explosion textures
│       │   ├── standard/           # Standard proximity explosion textures
│       │   │   ├── explosion.webp   # Explosion texture
│       │   │   ├── debris.webp      # Debris texture
│       │   │   └── smoke.webp       # Smoke texture
│       │   ├── delayed/            # Delayed explosion textures
│       │   │   ├── explosion.webp   # Explosion texture
│       │   │   ├── debris.webp      # Debris texture
│       │   │   └── smoke.webp       # Smoke texture
│       │   └── contact/            # Contact explosion textures
│       │       ├── explosion.webp   # Explosion texture
│       │       ├── debris.webp      # Debris texture
│       │       └── smoke.webp       # Smoke texture
│       ├── timed/                  # Timed mine explosion textures
│       │   ├── standard/           # Standard timed explosion textures
│       │   │   ├── explosion.webp   # Explosion texture
│       │   │   ├── debris.webp      # Debris texture
│       │   │   └── smoke.webp       # Smoke texture
│       │   ├── delayed/            # Delayed explosion textures
│       │   │   ├── explosion.webp   # Explosion texture
│       │   │   ├── debris.webp      # Debris texture
│       │   │   └── smoke.webp       # Smoke texture
│       │   └── remote/             # Remote explosion textures
│       │       ├── explosion.webp   # Explosion texture
│       │       ├── debris.webp      # Debris texture
│       │       └── smoke.webp       # Smoke texture
│       └── triggered/               # Triggered mine explosion textures
│           ├── standard/           # Standard triggered explosion textures
│           │   ├── explosion.webp   # Explosion texture
│           │   ├── debris.webp      # Debris texture
│           │   └── smoke.webp       # Smoke texture
│           ├── delayed/            # Delayed explosion textures
│           │   ├── explosion.webp   # Explosion texture
│           │   ├── debris.webp      # Debris texture
│           │   └── smoke.webp       # Smoke texture
│           └── manual/             # Manual explosion textures
│               ├── explosion.webp   # Explosion texture
│               ├── debris.webp      # Debris texture
│               └── smoke.webp       # Smoke texture
├── medium/                         # Medium explosion textures
│   ├── fighters/                   # Fighter craft explosion textures
│   │   ├── terran/                 # Terran fighter explosion textures
│   │   │   ├── arrow/              # Arrow fighter explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── wreckage/       # Wreckage explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   ├── rapier/             # Raptor fighter explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── wreckage/       # Wreckage explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   ├── hellcat/            # Hellcat fighter explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── wreckage/       # Wreckage explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   └── thunderbolt/        # Thunderbolt fighter explosion textures
│   │   │       ├── primary/        # Primary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       ├── secondary/      # Secondary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       └── wreckage/       # Wreckage explosion textures
│   │   │           ├── explosion.webp # Explosion texture
│   │   │           ├── debris.webp    # Debris texture
│   │   │           └── smoke.webp     # Smoke texture
│   │   ├── kilrathi/               # Kilrathi fighter explosion textures
│   │   │   ├── dralthi/            # Dralthi fighter explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── wreckage/       # Wreckage explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   ├── strakha/            # Strakha fighter explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── wreckage/       # Wreckage explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   ├── vaktoth/            # Vaktoth fighter explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── wreckage/       # Wreckage explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   └── var'kann/           # Var'kann fighter explosion textures
│   │   │       ├── primary/        # Primary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       ├── secondary/      # Secondary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       └── wreckage/       # Wreckage explosion textures
│   │   │           ├── explosion.webp # Explosion texture
│   │   │           ├── debris.webp    # Debris texture
│   │   │           └── smoke.webp     # Smoke texture
│   │   └── pirate/                 # Pirate fighter explosion textures
│   │       ├── corsair/            # Corsair fighter explosion textures
│   │       │   ├── primary/        # Primary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   ├── secondary/      # Secondary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   └── wreckage/       # Wreckage explosion textures
│   │       │       ├── explosion.webp # Explosion texture
│   │       │       ├── debris.webp    # Debris texture
│   │       │       └── smoke.webp     # Smoke texture
│   │       ├── bloodfang/          # Bloodfang fighter explosion textures
│   │       │   ├── primary/        # Primary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   ├── secondary/      # Secondary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   └── wreckage/       # Wreckage explosion textures
│   │       │       ├── explosion.webp # Explosion texture
│   │       │       ├── debris.webp    # Debris texture
│   │       │       └── smoke.webp     # Smoke texture
│   │       ├── darket/             # Darket fighter explosion textures
│   │       │   ├── primary/        # Primary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   ├── secondary/      # Secondary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   └── wreckage/       # Wreckage explosion textures
│   │       │       ├── explosion.webp # Explosion texture
│   │       │       ├── debris.webp    # Debris texture
│   │       │       └── smoke.webp     # Smoke texture
│   │       └── banshee/            # Banshee fighter explosion textures
│   │           ├── primary/        # Primary explosion textures
│   │           │   ├── explosion.webp # Explosion texture
│   │           │   ├── debris.webp    # Debris texture
│   │           │   └── smoke.webp     # Smoke texture
│   │           ├── secondary/      # Secondary explosion textures
│   │           │   ├── explosion.webp # Explosion texture
│   │           │   ├── debris.webp    # Debris texture
│   │           │   └── smoke.webp     # Smoke texture
│   │           └── wreckage/       # Wreckage explosion textures
│   │               ├── explosion.webp # Explosion texture
│   │               ├── debris.webp    # Debris texture
│   │               └── smoke.webp     # Smoke texture
│   ├── small_craft/                # Small craft explosion textures
│   │   ├── shuttles/               # Shuttle explosion textures
│   │   │   ├── transport/          # Transport shuttle explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── wreckage/       # Wreckage explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   ├── cargo/              # Cargo shuttle explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── wreckage/       # Wreckage explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   └── personnel/          # Personnel shuttle explosion textures
│   │   │       ├── primary/        # Primary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       ├── secondary/      # Secondary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       └── wreckage/       # Wreckage explosion textures
│   │   │           ├── explosion.webp # Explosion texture
│   │   │           ├── debris.webp    # Debris texture
│   │   │           └── smoke.webp     # Smoke texture
│   │   └── drones/                 # Drone explosion textures
│   │       ├── reconnaissance/     # Reconnaissance drone explosion textures
│   │       │   ├── primary/        # Primary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   ├── secondary/      # Secondary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   └── wreckage/       # Wreckage explosion textures
│   │       │       ├── explosion.webp # Explosion texture
│   │       │       ├── debris.webp    # Debris texture
│   │       │       └── smoke.webp     # Smoke texture
│   │       ├── combat/             # Combat drone explosion textures
│   │       │   ├── primary/        # Primary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   ├── secondary/      # Secondary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   └── wreckage/       # Wreckage explosion textures
│   │       │       ├── explosion.webp # Explosion texture
│   │       │       ├── debris.webp    # Debris texture
│   │       │       └── smoke.webp     # Smoke texture
│   │       └── support/            # Support drone explosion textures
│   │           ├── primary/        # Primary explosion textures
│   │           │   ├── explosion.webp # Explosion texture
│   │           │   ├── debris.webp    # Debris texture
│   │           │   └── smoke.webp     # Smoke texture
│   │           ├── secondary/      # Secondary explosion textures
│   │           │   ├── explosion.webp # Explosion texture
│   │           │   ├── debris.webp    # Debris texture
│   │           │   └── smoke.webp     # Smoke texture
│   │           └── wreckage/       # Wreckage explosion textures
│   │               ├── explosion.webp # Explosion texture
│   │               ├── debris.webp    # Debris texture
│   │               └── smoke.webp     # Smoke texture
│   └── weapons/                    # Weapon explosion textures
│       ├── missiles/               # Missile explosion textures
│       │   ├── dart/               # Dart missile explosion textures
│       │   │   ├── primary/        # Primary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   ├── secondary/      # Secondary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   └── fragmentation/  # Fragmentation textures
│       │   │       ├── explosion.webp # Explosion texture
│       │   │       ├── debris.webp    # Debris texture
│       │   │       └── smoke.webp     # Smoke texture
│       │   ├── javelin/            # Javelin missile explosion textures
│       │   │   ├── primary/        # Primary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   ├── secondary/      # Secondary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   └── fragmentation/  # Fragmentation textures
│       │   │       ├── explosion.webp # Explosion texture
│       │   │       ├── debris.webp    # Debris texture
│       │   │       └── smoke.webp     # Smoke texture
│       │   ├── spiculum/           # Spiculum missile explosion textures
│       │   │   ├── primary/        # Primary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   ├── secondary/      # Secondary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   └── fragmentation/  # Fragmentation textures
│       │   │       ├── explosion.webp # Explosion texture
│       │   │       ├── debris.webp    # Debris texture
│       │   │       └── smoke.webp     # Smoke texture
│       │   └── lance/              # Lance missile explosion textures
│       │       ├── primary/        # Primary explosion textures
│       │       │   ├── explosion.webp # Explosion texture
│       │       │   ├── debris.webp    # Debris texture
│       │       │   └── smoke.webp     # Smoke texture
│       │       ├── secondary/      # Secondary explosion textures
│       │       │   ├── explosion.webp # Explosion texture
│       │       │   ├── debris.webp    # Debris texture
│       │       │   └── smoke.webp     # Smoke texture
│       │       └── fragmentation/  # Fragmentation textures
│       │           ├── explosion.webp # Explosion texture
│       │           ├── debris.webp    # Debris texture
│       │           └── smoke.webp     # Smoke texture
│       ├── torpedoes/              # Torpedo explosion textures
│       │   ├── photon/             # Photon torpedo explosion textures
│       │   │   ├── primary/        # Primary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   ├── secondary/      # Secondary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   └── shockwave/      # Shockwave textures
│       │   │       ├── explosion.webp # Explosion texture
│       │   │       ├── debris.webp    # Debris texture
│       │   │       └── smoke.webp     # Smoke texture
│       │   ├── meson/              # Meson torpedo explosion textures
│       │   │   ├── primary/        # Primary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   ├── secondary/      # Secondary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   └── shockwave/      # Shockwave textures
│       │   │       ├── explosion.webp # Explosion texture
│       │   │       ├── debris.webp    # Debris texture
│       │   │       └── smoke.webp     # Smoke texture
│       │   └── quantum/            # Quantum torpedo explosion textures
│       │       ├── primary/        # Primary explosion textures
│       │       │   ├── explosion.webp # Explosion texture
│       │       │   ├── debris.webp    # Debris texture
│       │       │   └── smoke.webp     # Smoke texture
│       │       ├── secondary/      # Secondary explosion textures
│       │       │   ├── explosion.webp # Explosion texture
│       │       │   ├── debris.webp    # Debris texture
│       │       │   └── smoke.webp     # Smoke texture
│       │       └── shockwave/      # Shockwave textures
│       │           ├── explosion.webp # Explosion texture
│       │           ├── debris.webp    # Debris texture
│       │           └── smoke.webp     # Smoke texture
│       └── mines/                  # Mine explosion textures
│           ├── proximity/          # Proximity mine explosion textures
│           │   ├── primary/        # Primary explosion textures
│           │   │   ├── explosion.webp # Explosion texture
│           │   │   ├── debris.webp    # Debris texture
│           │   │   └── smoke.webp     # Smoke texture
│           │   ├── secondary/      # Secondary explosion textures
│           │   │   ├── explosion.webp # Explosion texture
│           │   │   ├── debris.webp    # Debris texture
│           │   │   └── smoke.webp     # Smoke texture
│           │   └── fragmentation/  # Fragmentation textures
│           │       ├── explosion.webp # Explosion texture
│           │       ├── debris.webp    # Debris texture
│           │       └── smoke.webp     # Smoke texture
│           ├── contact/            # Contact mine explosion textures
│           │   ├── primary/        # Primary explosion textures
│           │   │   ├── explosion.webp # Explosion texture
│           │   │   ├── debris.webp    # Debris texture
│           │   │   └── smoke.webp     # Smoke texture
│           │   ├── secondary/      # Secondary explosion textures
│           │   │   ├── explosion.webp # Explosion texture
│           │   │   ├── debris.webp    # Debris texture
│           │   │   └── smoke.webp     # Smoke texture
│           │   └── fragmentation/  # Fragmentation textures
│           │       ├── explosion.webp # Explosion texture
│           │       ├── debris.webp    # Debris texture
│           │       └── smoke.webp     # Smoke texture
│           └── timed/              # Timed mine explosion textures
│               ├── primary/        # Primary explosion textures
│               │   ├── explosion.webp # Explosion texture
│               │   ├── debris.webp    # Debris texture
│               │   └── smoke.webp     # Smoke texture
│               ├── secondary/      # Secondary explosion textures
│               │   ├── explosion.webp # Explosion texture
│               │   ├── debris.webp    # Debris texture
│               │   └── smoke.webp     # Smoke texture
│               └── fragmentation/  # Fragmentation textures
│                   ├── explosion.webp # Explosion texture
│                   ├── debris.webp    # Debris texture
│                   └── smoke.webp     # Smoke texture
├── large/                          # Large explosion textures
│   ├── capitals/                   # Capital ship explosion textures
│   │   ├── terran/                 # Terran capital ship explosion textures
│   │   │   ├── tigers_claw/        # Tiger's Claw explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── tertiary/       # Tertiary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── final/          # Final explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   ├── prowler/            # Prowler explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── tertiary/       # Tertiary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── final/          # Final explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   ├── venture/            # Venture explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── tertiary/       # Tertiary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── final/          # Final explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   └── behemoth/           # Behemoth explosion textures
│   │   │       ├── primary/        # Primary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       ├── secondary/      # Secondary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       ├── tertiary/       # Tertiary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       └── final/          # Final explosion textures
│   │   │           ├── explosion.webp # Explosion texture
│   │   │           ├── debris.webp    # Debris texture
│   │   │           └── smoke.webp     # Smoke texture
│   │   ├── kilrathi/               # Kilrathi capital ship explosion textures
│   │   │   ├── sahkra/             # Sahkra explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── tertiary/       # Tertiary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── final/          # Final explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   ├── jakhar/             # Jakhar explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── tertiary/       # Tertiary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── final/          # Final explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   ├── raktha/             # Raktha explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── tertiary/       # Tertiary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── final/          # Final explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   └── khar/               # Khar explosion textures
│   │   │       ├── primary/        # Primary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       ├── secondary/      # Secondary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       ├── tertiary/       # Tertiary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       └── final/          # Final explosion textures
│   │   │           ├── explosion.webp # Explosion texture
│   │   │           ├── debris.webp    # Debris texture
│   │   │           └── smoke.webp     # Smoke texture
│   │   └── pirate/                 # Pirate capital ship explosion textures
│   │       ├── corsair/            # Corsair capital explosion textures
│   │       │   ├── primary/        # Primary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   ├── secondary/      # Secondary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   ├── tertiary/       # Tertiary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   └── final/          # Final explosion textures
│   │       │       ├── explosion.webp # Explosion texture
│   │       │       ├── debris.webp    # Debris texture
│   │       │       └── smoke.webp     # Smoke texture
│   │       ├── dreadnought/        # Dreadnought explosion textures
│   │       │   ├── primary/        # Primary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   ├── secondary/      # Secondary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   ├── tertiary/       # Tertiary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   └── final/          # Final explosion textures
│   │       │       ├── explosion.webp # Explosion texture
│   │       │       ├── debris.webp    # Debris texture
│   │       │       └── smoke.webp     # Smoke texture
│   │       ├── frigate/            # Frigate explosion textures
│   │       │   ├── primary/        # Primary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   ├── secondary/      # Secondary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   ├── tertiary/       # Tertiary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   └── final/          # Final explosion textures
│   │       │       ├── explosion.webp # Explosion texture
│   │       │       ├── debris.webp    # Debris texture
│   │       │       └── smoke.webp     # Smoke texture
│   │       └── destroyer/          # Destroyer explosion textures
│   │           ├── primary/        # Primary explosion textures
│   │           │   ├── explosion.webp # Explosion texture
│   │           │   ├── debris.webp    # Debris texture
│   │           │   └── smoke.webp     # Smoke texture
│   │           ├── secondary/      # Secondary explosion textures
│   │           │   ├── explosion.webp # Explosion texture
│   │           │   ├── debris.webp    # Debris texture
│   │           │   └── smoke.webp     # Smoke texture
│   │           ├── tertiary/       # Tertiary explosion textures
│   │           │   ├── explosion.webp # Explosion texture
│   │           │   ├── debris.webp    # Debris texture
│   │           │   └── smoke.webp     # Smoke texture
│   │           └── final/          # Final explosion textures
│   │               ├── explosion.webp # Explosion texture
│   │               ├── debris.webp    # Debris texture
│   │               └── smoke.webp     # Smoke texture
│   ├── stations/                   # Station explosion textures
│   │   ├── supply_bases/           # Supply base explosion textures
│   │   │   ├── standard/           # Standard supply base explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── tertiary/       # Tertiary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── final/          # Final explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   ├── reinforced/         # Reinforced supply base explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── tertiary/       # Tertiary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── final/          # Final explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   └── fortified/          # Fortified supply base explosion textures
│   │   │       ├── primary/        # Primary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       ├── secondary/      # Secondary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       ├── tertiary/       # Tertiary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       └── final/          # Final explosion textures
│   │   │           ├── explosion.webp # Explosion texture
│   │   │           ├── debris.webp    # Debris texture
│   │   │           └── smoke.webp     # Smoke texture
│   │   ├── orbital_stations/       # Orbital station explosion textures
│   │   │   ├── standard/           # Standard orbital station explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── tertiary/       # Tertiary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── final/          # Final explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   ├── reinforced/         # Reinforced orbital station explosion textures
│   │   │   │   ├── primary/        # Primary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── secondary/      # Secondary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   ├── tertiary/       # Tertiary explosion textures
│   │   │   │   │   ├── explosion.webp # Explosion texture
│   │   │   │   │   ├── debris.webp    # Debris texture
│   │   │   │   │   └── smoke.webp     # Smoke texture
│   │   │   │   └── final/          # Final explosion textures
│   │   │   │       ├── explosion.webp # Explosion texture
│   │   │   │       ├── debris.webp    # Debris texture
│   │   │   │       └── smoke.webp     # Smoke texture
│   │   │   └── fortified/          # Fortified orbital station explosion textures
│   │   │       ├── primary/        # Primary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       ├── secondary/      # Secondary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       ├── tertiary/       # Tertiary explosion textures
│   │   │       │   ├── explosion.webp # Explosion texture
│   │   │       │   ├── debris.webp    # Debris texture
│   │   │       │   └── smoke.webp     # Smoke texture
│   │   │       └── final/          # Final explosion textures
│   │   │           ├── explosion.webp # Explosion texture
│   │   │           ├── debris.webp    # Debris texture
│   │   │           └── smoke.webp     # Smoke texture
│   │   └── drydocks/               # Drydock explosion textures
│   │       ├── standard/           # Standard drydock explosion textures
│   │       │   ├── primary/        # Primary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   ├── secondary/      # Secondary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   ├── tertiary/       # Tertiary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   └── final/          # Final explosion textures
│   │       │       ├── explosion.webp # Explosion texture
│   │       │       ├── debris.webp    # Debris texture
│   │       │       └── smoke.webp     # Smoke texture
│   │       ├── reinforced/         # Reinforced drydock explosion textures
│   │       │   ├── primary/        # Primary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   ├── secondary/      # Secondary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   ├── tertiary/       # Tertiary explosion textures
│   │       │   │   ├── explosion.webp # Explosion texture
│   │       │   │   ├── debris.webp    # Debris texture
│   │       │   │   └── smoke.webp     # Smoke texture
│   │       │   └── final/          # Final explosion textures
│   │       │       ├── explosion.webp # Explosion texture
│   │       │       ├── debris.webp    # Debris texture
│   │       │       └── smoke.webp     # Smoke texture
│   │       └── fortified/          # Fortified drydock explosion textures
│   │           ├── primary/        # Primary explosion textures
│   │           │   ├── explosion.webp # Explosion texture
│   │           │   ├── debris.webp    # Debris texture
│   │           │   └── smoke.webp     # Smoke texture
│   │           ├── secondary/      # Secondary explosion textures
│   │           │   ├── explosion.webp # Explosion texture
│   │           │   ├── debris.webp    # Debris texture
│   │           │   └── smoke.webp     # Smoke texture
│   │           ├── tertiary/       # Tertiary explosion textures
│   │           │   ├── explosion.webp # Explosion texture
│   │           │   ├── debris.webp    # Debris texture
│   │           │   └── smoke.webp     # Smoke texture
│   │           └── final/          # Final explosion textures
│   │               ├── explosion.webp # Explosion texture
│   │               ├── debris.webp    # Debris texture
│   │               └── smoke.webp     # Smoke texture
│   └── installations/              # Installation explosion textures
│       ├── mining_facilities/      # Mining facility explosion textures
│       │   ├── standard/           # Standard mining facility explosion textures
│       │   │   ├── primary/        # Primary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   ├── secondary/      # Secondary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   ├── tertiary/       # Tertiary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   └── final/          # Final explosion textures
│       │   │       ├── explosion.webp # Explosion texture
│       │   │       ├── debris.webp    # Debris texture
│       │   │       └── smoke.webp     # Smoke texture
│       │   ├── reinforced/         # Reinforced mining facility explosion textures
│       │   │   ├── primary/        # Primary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   ├── secondary/      # Secondary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   ├── tertiary/       # Tertiary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   └── final/          # Final explosion textures
│       │   │       ├── explosion.webp # Explosion texture
│       │   │       ├── debris.webp    # Debris texture
│       │   │       └── smoke.webp     # Smoke texture
│       │   └── fortified/          # Fortified mining facility explosion textures
│       │       ├── primary/        # Primary explosion textures
│       │       │   ├── explosion.webp # Explosion texture
│       │       │   ├── debris.webp    # Debris texture
│       │       │   └── smoke.webp     # Smoke texture
│       │       ├── secondary/      # Secondary explosion textures
│       │       │   ├── explosion.webp # Explosion texture
│       │       │   ├── debris.webp    # Debris texture
│       │       │   └── smoke.webp     # Smoke texture
│       │       ├── tertiary/       # Tertiary explosion textures
│       │       │   ├── explosion.webp # Explosion texture
│       │       │   ├── debris.webp    # Debris texture
│       │       │   └── smoke.webp     # Smoke texture
│       │       └── final/          # Final explosion textures
│       │           ├── explosion.webp # Explosion texture
│       │           ├── debris.webp    # Debris texture
│       │           └── smoke.webp     # Smoke texture
│       ├── research_stations/      # Research station explosion textures
│       │   ├── standard/           # Standard research station explosion textures
│       │   │   ├── primary/        # Primary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   ├── secondary/      # Secondary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   ├── tertiary/       # Tertiary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   └── final/          # Final explosion textures
│       │   │       ├── explosion.webp # Explosion texture
│       │   │       ├── debris.webp    # Debris texture
│       │   │       └── smoke.webp     # Smoke texture
│       │   ├── reinforced/         # Reinforced research station explosion textures
│       │   │   ├── primary/        # Primary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   ├── secondary/      # Secondary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   ├── tertiary/       # Tertiary explosion textures
│       │   │   │   ├── explosion.webp # Explosion texture
│       │   │   │   ├── debris.webp    # Debris texture
│       │   │   │   └── smoke.webp     # Smoke texture
│       │   │   └── final/          # Final explosion textures
│       │   │       ├── explosion.webp # Explosion texture
│       │   │       ├── debris.webp    # Debris texture
│       │   │       └── smoke.webp     # Smoke texture
│       │   └── fortified/          # Fortified research station explosion textures
│       │       ├── primary/        # Primary explosion textures
│       │       │   ├── explosion.webp # Explosion texture
│       │       │   ├── debris.webp    # Debris texture
│       │       │   └── smoke.webp     # Smoke texture
│       │       ├── secondary/      # Secondary explosion textures
│       │       │   ├── explosion.webp # Explosion texture
│       │       │   ├── debris.webp    # Debris texture
│       │       │   └── smoke.webp     # Smoke texture
│       │       ├── tertiary/       # Tertiary explosion textures
│       │       │   ├── explosion.webp # Explosion texture
│       │       │   ├── debris.webp    # Debris texture
│       │       │   └── smoke.webp     # Smoke texture
│       │       └── final/          # Final explosion textures
│       │           ├── explosion.webp # Explosion texture
│       │           ├── debris.webp    # Debris texture
│       │           └── smoke.webp     # Smoke texture
│       └── manufacturing_plants/   # Manufacturing plant explosion textures
│           ├── standard/           # Standard manufacturing plant explosion textures
│           │   ├── primary/        # Primary explosion textures
│           │   │   ├── explosion.webp # Explosion texture
│           │   │   ├── debris.webp    # Debris texture
│           │   │   └── smoke.webp     # Smoke texture
│           │   ├── secondary/      # Secondary explosion textures
│           │   │   ├── explosion.webp # Explosion texture
│           │   │   ├── debris.webp    # Debris texture
│           │   │   └── smoke.webp     # Smoke texture
│           │   ├── tertiary/       # Tertiary explosion textures
│           │   │   ├── explosion.webp # Explosion texture
│           │   │   ├── debris.webp    # Debris texture
│           │   │   └── smoke.webp     # Smoke texture
│           │   └── final/          # Final explosion textures
│           │       ├── explosion.webp # Explosion texture
│           │       ├── debris.webp    # Debris texture
│           │       └── smoke.webp     # Smoke texture
│           ├── reinforced/         # Reinforced manufacturing plant explosion textures
│           │   ├── primary/        # Primary explosion textures
│           │   │   ├── explosion.webp # Explosion texture
│           │   │   ├── debris.webp    # Debris texture
│           │   │   └── smoke.webp     # Smoke texture
│           │   ├── secondary/      # Secondary explosion textures
│           │   │   ├── explosion.webp # Explosion texture
│           │   │   ├── debris.webp    # Debris texture
│           │   │   └── smoke.webp     # Smoke texture
│           │   ├── tertiary/       # Tertiary explosion textures
│           │   │   ├── explosion.webp # Explosion texture
│           │   │   ├── debris.webp    # Debris texture
│           │   │   └── smoke.webp     # Smoke texture
│           │   └── final/          # Final explosion textures
│           │       ├── explosion.webp # Explosion texture
│           │       ├── debris.webp    # Debris texture
│           │       └── smoke.webp     # Smoke texture
│           └── fortified/          # Fortified manufacturing plant explosion textures
│               ├── primary/        # Primary explosion textures
│               │   ├── explosion.webp # Explosion texture
│               │   ├── debris.webp    # Debris texture
│               │   └── smoke.webp     # Smoke texture
│               ├── secondary/      # Secondary explosion textures
│               │   ├── explosion.webp # Explosion texture
│               │   ├── debris.webp    # Debris texture
│               │   └── smoke.webp     # Smoke texture
│               ├── tertiary/       # Tertiary explosion textures
│               │   ├── explosion.webp # Explosion texture
│               │   ├── debris.webp    # Debris texture
│               │   └── smoke.webp     # Smoke texture
│               └── final/          # Final explosion textures
│                   ├── explosion.webp # Explosion texture
│                   ├── debris.webp    # Debris texture
│                   └── smoke.webp     # Smoke texture
└── special/                        # Special explosion textures
    ├── shockwaves/                 # Shockwave textures
    │   ├── kinetic/                # Kinetic shockwave textures
    │   │   ├── standard/           # Standard kinetic shockwave textures
    │   │   │   ├── wave_front.webp  # Wave front texture
    │   │   │   ├── pressure_ring.webp # Pressure ring texture
    │   │   │   └── energy_burst.webp # Energy burst texture
    │   │   ├── enhanced/           # Enhanced kinetic shockwave textures
    │   │   │   ├── wave_front.webp  # Wave front texture
    │   │   │   ├── pressure_ring.webp # Pressure ring texture
    │   │   │   └── energy_burst.webp # Energy burst texture
    │   │   └── massive/            # Massive kinetic shockwave textures
    │   │       ├── wave_front.webp  # Wave front texture
    │   │       ├── pressure_ring.webp # Pressure ring texture
    │   │       └── energy_burst.webp # Energy burst texture
    │   ├── energy/                 # Energy shockwave textures
    │   │   ├── standard/           # Standard energy shockwave textures
    │   │   │   ├── wave_front.webp  # Wave front texture
    │   │   │   ├── pressure_ring.webp # Pressure ring texture
    │   │   │   └── energy_burst.webp # Energy burst texture
    │   │   ├── enhanced/           # Enhanced energy shockwave textures
    │   │   │   ├── wave_front.webp  # Wave front texture
    │   │   │   ├── pressure_ring.webp # Pressure ring texture
    │   │   │   └── energy_burst.webp # Energy burst texture
    │   │   └── massive/            # Massive energy shockwave textures
    │   │       ├── wave_front.webp  # Wave front texture
    │   │       ├── pressure_ring.webp # Pressure ring texture
    │   │       └── energy_burst.webp # Energy burst texture
    │   └── electromagnetic/         # Electromagnetic shockwave textures
    │       ├── standard/           # Standard electromagnetic shockwave textures
    │       │   ├── wave_front.webp  # Wave front texture
    │       │   ├── pressure_ring.webp # Pressure ring texture
    │       │   └── energy_burst.webp # Energy burst texture
    │       ├── enhanced/           # Enhanced electromagnetic shockwave textures
    │       │   ├── wave_front.webp  # Wave front texture
    │       │   ├── pressure_ring.webp # Pressure ring texture
    │       │   └── energy_burst.webp # Energy burst texture
    │       └── massive/            # Massive electromagnetic shockwave textures
    │           ├── wave_front.webp  # Wave front texture
    │           ├── pressure_ring.webp # Pressure ring texture
    │           └── energy_burst.webp # Energy burst texture
    ├── fireballs/                  # Fireball textures
    │   ├── small/                  # Small fireball textures
    │   │   ├── standard/           # Standard small fireball textures
    │   │   │   ├── core.webp        # Core texture
    │   │   │   ├── outer_flame.webp # Outer flame texture
    │   │   │   └── smoke_trail.webp # Smoke trail texture
    │   │   ├── intense/            # Intense small fireball textures
    │   │   │   ├── core.webp        # Core texture
    │   │   │   ├── outer_flame.webp # Outer flame texture
    │   │   │   └── smoke_trail.webp # Smoke trail texture
    │   │   └── weak/               # Weak small fireball textures
    │   │       ├── core.webp        # Core texture
    │   │       ├── outer_flame.webp # Outer flame texture
    │   │       └── smoke_trail.webp # Smoke trail texture
    │   ├── medium/                 # Medium fireball textures
    │   │   ├── standard/           # Standard medium fireball textures
    │   │   │   ├── core.webp        # Core texture
    │   │   │   ├── outer_flame.webp # Outer flame texture
    │   │   │   └── smoke_trail.webp # Smoke trail texture
    │   │   ├── intense/            # Intense medium fireball textures
    │   │   │   ├── core.webp        # Core texture
    │   │   │   ├── outer_flame.webp # Outer flame texture
    │   │   │   └── smoke_trail.webp # Smoke trail texture
    │   │   └── weak/               # Weak medium fireball textures
    │   │       ├── core.webp        # Core texture
    │   │       ├── outer_flame.webp # Outer flame texture
    │   │       └── smoke_trail.webp # Smoke trail texture
    │   └── large/                  # Large fireball textures
    │       ├── standard/           # Standard large fireball textures
    │       │   ├── core.webp        # Core texture
    │       │   ├── outer_flame.webp # Outer flame texture
    │       │   └── smoke_trail.webp # Smoke trail texture
    │       ├── intense/            # Intense large fireball textures
    │       │   ├── core.webp        # Core texture
    │       │   ├── outer_flame.webp # Outer flame texture
    │       │   └── smoke_trail.webp # Smoke trail texture
    │       └── weak/               # Weak large fireball textures
    │           ├── core.webp        # Core texture
    │           ├── outer_flame.webp # Outer flame texture
    │           └── smoke_trail.webp # Smoke trail texture
    ├── debris_clouds/              # Debris cloud textures
    │   ├── metal/                  # Metal debris cloud textures
    │   │   ├── standard/           # Standard metal debris cloud textures
    │   │   │   ├── fragment_spray.webp # Fragment spray texture
    │   │   │   ├── dust_cloud.webp    # Dust cloud texture
    │   │   │   └── particle_swarm.webp # Particle swarm texture
    │   │   ├── dense/              # Dense metal debris cloud textures
    │   │   │   ├── fragment_spray.webp # Fragment spray texture
    │   │   │   ├── dust_cloud.webp    # Dust cloud texture
    │   │   │   └── particle_swarm.webp # Particle swarm texture
    │   │   └── sparse/             # Sparse metal debris cloud textures
    │   │       ├── fragment_spray.webp # Fragment spray texture
    │   │       ├── dust_cloud.webp    # Dust cloud texture
    │   │       └── particle_swarm.webp # Particle swarm texture
    │   ├── organic/                # Organic debris cloud textures
    │   │   ├── standard/           # Standard organic debris cloud textures
    │   │   │   ├── fragment_spray.webp # Fragment spray texture
    │   │   │   ├── dust_cloud.webp    # Dust cloud texture
    │   │   │   └── particle_swarm.webp # Particle swarm texture
    │   │   ├── dense/              # Dense organic debris cloud textures
    │   │   │   ├── fragment_spray.webp # Fragment spray texture
    │   │   │   ├── dust_cloud.webp    # Dust cloud texture
    │   │   │   └── particle_swarm.webp # Particle swarm texture
    │   │   └── sparse/             # Sparse organic debris cloud textures
    │   │       ├── fragment_spray.webp # Fragment spray texture
    │   │       ├── dust_cloud.webp    # Dust cloud texture
    │   │       └── particle_swarm.webp # Particle swarm texture
    │   └── mixed/                  # Mixed debris cloud textures
    │       ├── standard/           # Standard mixed debris cloud textures
    │       │   ├── fragment_spray.webp # Fragment spray texture
    │       │   ├── dust_cloud.webp    # Dust cloud texture
    │       │   └── particle_swarm.webp # Particle swarm texture
    │       ├── dense/              # Dense mixed debris cloud textures
    │       │   ├── fragment_spray.webp # Fragment spray texture
    │       │   ├── dust_cloud.webp    # Dust cloud texture
    │       │   └── particle_swarm.webp # Particle swarm texture
    │       └── sparse/             # Sparse mixed debris cloud textures
    │           ├── fragment_spray.webp # Fragment spray texture
    │           ├── dust_cloud.webp    # Dust cloud texture
    │           └── particle_swarm.webp # Particle swarm texture
    ├── electrical/                 # Electrical textures
    │   ├── lightning/              # Lightning textures
    │   │   ├── standard/           # Standard lightning effect textures
    │   │   │   ├── bolt_strike.webp # Bolt strike texture
    │   │   │   ├── energy_arcs.webp # Energy arcs texture
    │   │   │   └── electric_flash.webp # Electric flash texture
    │   │   ├── intense/            # Intense lightning effect textures
    │   │   │   ├── bolt_strike.webp # Bolt strike texture
    │   │   │   ├── energy_arcs.webp # Energy arcs texture
    │   │   │   └── electric_flash.webp # Electric flash texture
    │   │   └── weak/               # Weak lightning effect textures
    │   │       ├── bolt_strike.webp # Bolt strike texture
    │   │       ├── energy_arcs.webp # Energy arcs texture
    │   │       └── electric_flash.webp # Electric flash texture
    │   ├── arcs/                   # Electrical arc textures
    │   │   ├── standard/           # Standard electrical arc textures
    │   │   │   ├── arc_strike.webp  # Arc strike texture
    │   │   │   ├── energy_flow.webp # Energy flow texture
    │   │   │   └── electric_spark.webp # Electric spark texture
    │   │   ├── intense/            # Intense electrical arc textures
    │   │   │   ├── arc_strike.webp  # Arc strike texture
    │   │   │   ├── energy_flow.webp # Energy flow texture
    │   │   │   └── electric_spark.webp # Electric spark texture
    │   │   └── weak/               # Weak electrical arc textures
    │   │       ├── arc_strike.webp  # Arc strike texture
    │   │       ├── energy_flow.webp # Energy flow texture
    │   │       └── electric_spark.webp # Electric spark texture
    │   └── discharges/             # Electrical discharge textures
    │       ├── standard/           # Standard electrical discharge textures
    │       │   ├── discharge_burst.webp # Discharge burst texture
    │       │   ├── energy_pulse.webp    # Energy pulse texture
    │       │   └── electric_flash.webp  # Electric flash texture
    │       ├── intense/            # Intense electrical discharge textures
    │       │   ├── discharge_burst.webp # Discharge burst texture
    │       │   ├── energy_pulse.webp    # Energy pulse texture
    │       │   └── electric_flash.webp  # Electric flash texture
    │       └── weak/               # Weak electrical discharge textures
    │           ├── discharge_burst.webp # Discharge burst texture
    │           ├── energy_pulse.webp    # Energy pulse texture
    │           └── electric_flash.webp  # Electric flash texture
    ├── plasma/                     # Plasma textures
    │   ├── bursts/                 # Plasma burst textures
    │   │   ├── standard/           # Standard plasma burst textures
    │   │   │   ├── energy_burst.webp # Energy burst texture
    │   │   │   ├── plasma_sphere.webp # Plasma sphere texture
    │   │   │   └── energy_flash.webp # Energy flash texture
    │   │   ├── intense/            # Intense plasma burst textures
    │   │   │   ├── energy_burst.webp # Energy burst texture
    │   │   │   ├── plasma_sphere.webp # Plasma sphere texture
    │   │   │   └── energy_flash.webp # Energy flash texture
    │   │   └── weak/               # Weak plasma burst textures
    │   │       ├── energy_burst.webp # Energy burst texture
    │   │       ├── plasma_sphere.webp # Plasma sphere texture
    │   │       └── energy_flash.webp # Energy flash texture
    │   ├── streams/                # Plasma stream textures
    │   │   ├── standard/           # Standard plasma stream textures
    │   │   │   ├── energy_stream.webp # Energy stream texture
    │   │   │   ├── plasma_flow.webp   # Plasma flow texture
    │   │   │   └── energy_trail.webp  # Energy trail texture
    │   │   ├── intense/            # Intense plasma stream textures
    │   │   │   ├── energy_stream.webp # Energy stream texture
    │   │   │   ├── plasma_flow.webp   # Plasma flow texture
    │   │   │   └── energy_trail.webp  # Energy trail texture
    │   │   └── weak/               # Weak plasma stream textures
    │   │       ├── energy_stream.webp # Energy stream texture
    │   │       ├── plasma_flow.webp   # Plasma flow texture
    │   │       └── energy_trail.webp  # Energy trail texture
    │   └── clouds/                 # Plasma cloud textures
    │       ├── standard/           # Standard plasma cloud textures
    │       │   ├── energy_cloud.webp # Energy cloud texture
    │       │   ├── plasma_swirl.webp # Plasma swirl texture
    │       │   └── energy_glow.webp  # Energy glow texture
    │       ├── intense/            # Intense plasma cloud textures
    │       │   ├── energy_cloud.webp # Energy cloud texture
    │       │   ├── plasma_swirl.webp # Plasma swirl texture
    │       │   └── energy_glow.webp  # Energy glow texture
    │       └── weak/               # Weak plasma cloud textures
    │           ├── energy_cloud.webp # Energy cloud texture
    │           ├── plasma_swirl.webp # Plasma swirl texture
    │           └── energy_glow.webp  # Energy glow texture
    ├── nuclear/                    # Nuclear textures
    │   ├── detonations/            # Nuclear detonation textures
    │   │   ├── standard/           # Standard nuclear detonation textures
    │   │   │   ├── mushroom_cloud.webp # Mushroom cloud texture
    │   │   │   ├── radiation_burst.webp # Radiation burst texture
    │   │   │   └── thermal_flash.webp  # Thermal flash texture
    │   │   ├── enhanced/           # Enhanced nuclear detonation textures
    │   │   │   ├── mushroom_cloud.webp # Mushroom cloud texture
    │   │   │   ├── radiation_burst.webp # Radiation burst texture
    │   │   │   └── thermal_flash.webp  # Thermal flash texture
    │   │   └── massive/            # Massive nuclear detonation textures
    │   │       ├── mushroom_cloud.webp # Mushroom cloud texture
    │   │       ├── radiation_burst.webp # Radiation burst texture
    │   │       └── thermal_flash.webp  # Thermal flash texture
    │   ├── radiation/              # Radiation textures
    │   │   ├── standard/           # Standard radiation effect textures
    │   │   │   ├── radiation_wave.webp # Radiation wave texture
    │   │   │   ├── energy_pulse.webp   # Energy pulse texture
    │   │   │   └── toxic_cloud.webp    # Toxic cloud texture
    │   │   ├── enhanced/           # Enhanced radiation effect textures
    │   │   │   ├── radiation_wave.webp # Radiation wave texture
    │   │   │   ├── energy_pulse.webp   # Energy pulse texture
    │   │   │   └── toxic_cloud.webp    # Toxic cloud texture
    │   │   └── massive/            # Massive radiation effect textures
    │   │       ├── radiation_wave.webp # Radiation wave texture
    │   │       ├── energy_pulse.webp   # Energy pulse texture
    │   │       └── toxic_cloud.webp    # Toxic cloud texture
    │   └── fallout/                # Fallout textures
    │       ├── standard/           # Standard fallout effect textures
    │       │   ├── radioactive_dust.webp # Radioactive dust texture
    │       │   ├── contamination_cloud.webp # Contamination cloud texture
    │       │   └── toxic_precipitation.webp # Toxic precipitation texture
    │       ├── enhanced/           # Enhanced fallout effect textures
    │       │   ├── radioactive_dust.webp # Radioactive dust texture
    │       │   ├── contamination_cloud.webp # Contamination cloud texture
    │       │   └── toxic_precipitation.webp # Toxic precipitation texture
    │       └── massive/            # Massive fallout effect textures
    │           ├── radioactive_dust.webp # Radioactive dust texture
    │           ├── contamination_cloud.webp # Contamination cloud texture
    │           └── toxic_precipitation.webp # Toxic precipitation texture
    └── antimatter/                 # Antimatter textures
        ├── reactions/              # Antimatter reaction textures
        │   ├── standard/           # Standard antimatter reaction textures
        │   │   ├── matter_annihilation.webp # Matter annihilation texture
        │   │   ├── energy_release.webp      # Energy release texture
        │   │   └── spacetime_distortion.webp # Spacetime distortion texture
        │   ├── enhanced/           # Enhanced antimatter reaction textures
        │   │   ├── matter_annihilation.webp # Matter annihilation texture
        │   │   ├── energy_release.webp      # Energy release texture
        │   │   └── spacetime_distortion.webp # Spacetime distortion texture
        │   └── massive/            # Massive antimatter reaction textures
        │       ├── matter_annihilation.webp # Matter annihilation texture
        │       ├── energy_release.webp      # Energy release texture
        │       └── spacetime_distortion.webp # Spacetime distortion texture
        ├── annihilation/           # Annihilation textures
        │   ├── standard/           # Standard annihilation effect textures
        │   │   ├── particle_collision.webp  # Particle collision texture
        │   │   ├── energy_explosion.webp    # Energy explosion texture
        │   │   └── void_creation.webp       # Void creation texture
        │   ├── enhanced/           # Enhanced annihilation effect textures
        │   │   ├── particle_collision.webp  # Particle collision texture
        │   │   ├── energy_explosion.webp    # Energy explosion texture
        │   │   └── void_creation.webp       # Void creation texture
        │   └── massive/            # Massive annihilation effect textures
        │       ├── particle_collision.webp  # Particle collision texture
        │       ├── energy_explosion.webp    # Energy explosion texture
        │       └── void_creation.webp       # Void creation texture
        └── containment_failures/   # Containment failure textures
            ├── standard/           # Standard containment failure textures
            │   ├── barrier_breach.webp   # Barrier breach texture
            │   ├── energy_leak.webp      # Energy leak texture
            │   └── system_malfunction.webp # System malfunction texture
            ├── enhanced/           # Enhanced containment failure textures
            │   ├── barrier_breach.webp   # Barrier breach texture
            │   ├── energy_leak.webp      # Energy leak texture
            │   └── system_malfunction.webp # System malfunction texture
            └── massive/            # Massive containment failure textures
                ├── barrier_breach.webp   # Barrier breach texture
                ├── energy_leak.webp      # Energy leak texture
                └── system_malfunction.webp # System malfunction texture

/ui/cutscenes/                      # Cutscene UI directory
├── hermes/                         # Hermes campaign UI
│   ├── player/                     # Player cutscene UI
│   │   ├── interface/              # Interface elements
│   │   │   ├── subtitles/          # Subtitle display
│   │   │   │   ├── text_box.tscn    # Text box scene
│   │   │   │   ├── speaker_label.tscn # Speaker label scene
│   │   │   │   └── progress_indicator.tscn # Progress indicator scene
│   │   │   ├── controls/           # Control elements
│   │   │   │   ├── skip_button.tscn # Skip button scene
│   │   │   │   ├── pause_button.tscn # Pause button scene
│   │   │   │   └── volume_slider.tscn # Volume slider scene
│   │   │   ├── overlays/           # Overlay elements
│   │   │   │   ├── fade_in.tscn     # Fade in overlay
│   │   │   │   ├── fade_out.tscn    # Fade out overlay
│   │   │   │   └── transition.tscn  # Transition overlay
│   │   │   └── backgrounds/        # Background elements
│   │   │       ├── cinematic_border.tscn # Cinematic border scene
│   │   │       ├── letterbox_mask.tscn # Letterbox mask scene
│   │   │       └── vignette_effect.tscn # Vignette effect scene
│   │   ├── subtitles/              # Subtitle elements
│   │   │   ├── display/            # Subtitle display
│   │   │   │   ├── text_display.tscn # Text display scene
│   │   │   │   ├── character_name.tscn # Character name scene
│   │   │   │   └── dialogue_marker.tscn # Dialogue marker scene
│   │   │   ├── formatting/         # Subtitle formatting
│   │   │   │   ├── emphasis.tscn    # Emphasis formatting
│   │   │   │   ├── italics.tscn     # Italics formatting
│   │   │   │   └── highlighting.tscn # Highlighting formatting
│   │   │   └── timing/             # Subtitle timing
│   │   │       ├── sync.tscn        # Synchronization controls
│   │   │       ├── delay.tscn       # Delay controls
│   │   │       └── advance.tscn     # Advance controls
│   │   ├── controls/               # Control elements
│   │   │   ├── playback/           # Playback controls
│   │   │   │   ├── play.tscn        # Play button
│   │   │   │   ├── pause.tscn       # Pause button
│   │   │   │   ├── stop.tscn        # Stop button
│   │   │   │   ├── skip.tscn        # Skip button
│   │   │   │   └── rewind.tscn      # Rewind button
│   │   │   ├── navigation/         # Navigation controls
│   │   │   │   ├── next.tscn        # Next button
│   │   │   │   ├── previous.tscn    # Previous button
│   │   │   │   └── menu.tscn        # Menu button
│   │   │   └── settings/           # Settings controls
│   │   │       ├── volume.tscn      # Volume control
│   │   │       ├── subtitles.tscn   # Subtitle control
│   │   │       └── quality.tscn     # Quality control
│   │   └── overlays/               # Overlay elements
│   │       ├── transitions/        # Transition overlays
│   │       │   ├── fade.tscn        # Fade transition
│   │       │   ├── wipe.tscn        # Wipe transition
│   │       │   └── dissolve.tscn    # Dissolve transition
│   │       ├── effects/            # Special effect overlays
│   │       │   ├── blur.tscn        # Blur effect
│   │       │   ├── distortion.tscn  # Distortion effect
│   │       │   └── chromatic_aberration.tscn # Chromatic aberration effect
│   │       └── ui_elements/        # UI element overlays
│   │           ├── button_prompts.tscn # Button prompts
│   │           ├── loading_indicators.tscn # Loading indicators
│   │           └── status_displays.tscn # Status displays
│   ├── mission/                    # Mission cutscene UI
│   │   ├── interface/              # Interface elements
│   │   ├── subtitles/              # Subtitle elements
│   │   ├── controls/               # Control elements
│   │   └── overlays/               # Overlay elements
│   ├── character/                  # Character cutscene UI
│   │   ├── interface/              # Interface elements
│   │   ├── subtitles/              # Subtitle elements
│   │   ├── controls/               # Control elements
│   │   └── overlays/               # Overlay elements
│   ├── plot/                       # Plot cutscene UI
│   │   ├── interface/              # Interface elements
│   │   ├── subtitles/              # Subtitle elements
│   │   ├── controls/               # Control elements
│   │   └── overlays/               # Overlay elements
│   └── outro/                      # Outro cutscene UI
│       ├── interface/              # Interface elements
│       ├── subtitles/              # Subtitle elements
│       ├── controls/               # Control elements
│       └── overlays/               # Overlay elements
├── brimstone/                      # Brimstone campaign UI
│   ├── player/
│   ├── mission/
│   ├── character/
│   ├── plot/
│   └── outro/
└── training/                       # Training mission UI
    ├── player/
    ├── mission/
    ├── character/
    ├── plot/
    └── outro/

/scenes/cutscenes/                  # Cutscene scene directory
├── hermes/                         # Hermes campaign scenes
│   ├── intro/                      # Campaign intro scenes
│   │   ├── campaign_intro.tscn     # Campaign intro scene
│   │   ├── disc_intros/            # Disc intro scenes
│   │   │   ├── disc_01.tscn        # Disc 1 intro scene
│   │   │   ├── disc_02.tscn        # Disc 2 intro scene
│   │   │   ├── disc_03.tscn        # Disc 3 intro scene
│   │   │   ├── disc_04.tscn        # Disc 4 intro scene
│   │   │   └── disc_05.tscn        # Disc 5 intro scene
│   │   └── mission_intros/         # Mission intro scenes
│   │       ├── m01_intro.tscn      # Mission 1 intro scene
│   │       ├── m02_intro.tscn      # Mission 2 intro scene
│   │       ├── m03_intro.tscn      # Mission 3 intro scene
│   │       └── ...                 # Additional mission intros
│   ├── missions/                   # Mission scenes
│   │   ├── m01/                    # Mission 1 scenes
│   │   │   ├── briefing.tscn       # Mission 1 briefing scene
│   │   │   ├── mid_mission.tscn    # Mission 1 mid-mission cutscene
│   │   │   ├── debriefing.tscn     # Mission 1 debriefing scene
│   │   │   ├── victory.tscn        # Mission 1 victory sequence
│   │   │   └── defeat.tscn         # Mission 1 defeat sequence
│   │   ├── m02/                    # Mission 2 scenes
│   │   │   ├── briefing.tscn       # Mission 2 briefing scene
│   │   │   ├── mid_mission.tscn    # Mission 2 mid-mission cutscene
│   │   │   ├── debriefing.tscn     # Mission 2 debriefing scene
│   │   │   ├── victory.tscn        # Mission 2 victory sequence
│   │   │   └── defeat.tscn         # Mission 2 defeat sequence
│   │   └── ...                     # Additional missions
│   ├── character/                  # Character scenes
│   │   ├── introduction/           # Character introduction scenes
│   │   │   ├── moran.tscn          # Moran introduction
│   │   │   ├── sandman.tscn        # Sandman introduction
│   │   │   ├── honeybear.tscn      # Honeybear introduction
│   │   │   └── ...                 # Additional characters
│   │   ├── development/            # Character development scenes
│   │   │   ├── moran.tscn          # Moran development
│   │   │   ├── sandman.tscn        # Sandman development
│   │   │   ├── honeybear.tscn      # Honeybear development
│   │   │   └── ...                 # Additional characters
│   │   └── revelation/             # Character revelation scenes
│   │       ├── moran.tscn          # Moran revelation
│   │       ├── sandman.tscn        # Sandman revelation
│   │       ├── honeybear.tscn      # Honeybear revelation
│   │       └── ...                 # Additional characters
│   ├── plot/                       # Plot-related scenes
│   │   ├── revelation/             # Plot revelation scenes
│   │   │   ├── secret_disclosed.tscn # Secret disclosed scene
│   │   │   ├── betrayal_revealed.tscn # Betrayal revealed scene
│   │   │   ├── truth_uncovered.tscn # Truth uncovered scene
│   │   │   └── conspiracy_exposed.tscn # Conspiracy exposed scene
│   │   ├── twist/                  # Plot twist scenes
│   │   │   ├── unexpected_alliance.tscn # Unexpected alliance scene
│   │   │   ├── hidden_agenda.tscn   # Hidden agenda scene
│   │   │   ├── double_cross.tscn    # Double cross scene
│   │   │   └── surprise_attack.tscn # Surprise attack scene
│   │   └── climax/                 # Climactic scenes
│   │       ├── confrontation.tscn   # Confrontation scene
│   │       ├── showdown.tscn        # Showdown scene
│   │       ├── final_battle.tscn    # Final battle scene
│   │       └── resolution.tscn      # Resolution scene
│   ├── outro/                      # Campaign outro scenes
│   │   ├── campaign_outro.tscn      # Campaign outro scene
│   │   ├── disc_outros/            # Disc outro scenes
│   │   │   ├── disc_01.tscn        # Disc 1 outro scene
│   │   │   ├── disc_02.tscn        # Disc 2 outro scene
│   │   │   ├── disc_03.tscn        # Disc 3 outro scene
│   │   │   ├── disc_04.tscn        # Disc 4 outro scene
│   │   │   └── disc_05.tscn        # Disc 5 outro scene
│   │   └── mission_outros/         # Mission outro scenes
│   │       ├── m01_outro.tscn      # Mission 1 outro scene
│   │       ├── m02_outro.tscn      # Mission 2 outro scene
│   │       ├── m03_outro.tscn      # Mission 3 outro scene
│   │       └── ...                 # Additional mission outros
│   └── credits/                    # Credit sequence scenes
│       ├── opening_credits.tscn     # Opening credits scene
│       ├── closing_credits.tscn     # Closing credits scene
│       ├── cast_roll.tscn          # Cast roll scene
│       ├── crew_roll.tscn          # Crew roll scene
│       └── special_thanks.tscn      # Special thanks scene
├── brimstone/                      # Brimstone campaign scenes
│   ├── intro/
│   ├── missions/
│   ├── character/
│   ├── plot/
│   ├── outro/
│   └── credits/
└── training/                       # Training mission scenes
    ├── intro/
    ├── lessons/
    ├── character/
    ├── outro/
    └── credits/
```

## Example Mapping
For a typical mission briefing cutscene:
- cutscenes.tbl entry → /data/cutscenes/hermes/missions/m01/briefing.tres
- briefing.ani → /animations/cutscenes/hermes/missions/m01/briefing/briefing.png
- briefing_video.webm → /videos/cutscenes/hermes/missions/m01/briefing/briefing_video.webm
- briefing_music.ogg → /audio/music/cutscenes/hermes/missions/m01/briefing/briefing_theme.ogg
- briefing_voice.wav → /audio/voice/cutscenes/hermes/missions/m01/briefing/moran/briefing_dialogue.ogg
- briefing_subtitles.txt → /text/subtitles/cutscenes/hermes/missions/m01/briefing/moran.txt
- briefing_ui.tscn → /ui/cutscenes/hermes/mission/interface/subtitles/text_box.tscn
- briefing_scene.tscn → /scenes/cutscenes/hermes/missions/m01/briefing.tscn

For a capital ship explosion effect:
- weapon_expl.tbl entry → /data/effects/explosions/large/capitals/terran/tigers_claw/primary.tres
- explosion.ani → /animations/effects/explosions/large/capitals/terran/tigers_claw/primary/explosion.png
- explosion.pcx → /textures/effects/explosions/large/capitals/terran/tigers_claw/primary/explosion.webp
- debris.ani → /animations/effects/explosions/large/capitals/terran/tigers_claw/primary/debris.png
- debris.pcx → /textures/effects/explosions/large/capitals/terran/tigers_claw/primary/debris.webp
- smoke.ani → /animations/effects/explosions/large/capitals/terran/tigers_claw/primary/smoke.png
- smoke.pcx → /textures/effects/explosions/large/capitals/terran/tigers_claw/primary/smoke.webp
- explosion_sound.wav → /audio/sfx/effects/explosions/large/capitals/terran/tigers_claw/primary/explosion.ogg