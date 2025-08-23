# Effects Asset Mapping

## Overview
This document maps the effect definitions from various TBL files to their corresponding media assets in the Wing Commander Saga Hermes campaign.

## Asset Types

### Fireball Effects (.ani/.pcx)
Fireball.tbl and related tables reference animated effects:
- fireball_*.ani - Explosion fireball animations
- debris_*.ani - Debris particle animations
- shockwave_*.ani - Shockwave effect animations
- explosion_*.ani - Generic explosion animations

Associated PCX textures:
- fireball_*.pcx - Fireball texture frames
- debris_*.pcx - Debris particle textures
- shockwave_*.pcx - Shockwave effect textures

### Weapon Effects (.ani/.pcx)
Weapon_expl.tbl references weapon impact effects:
- weapon_impact_*.ani - Weapon hit animations
- muzzle_flash_*.ani - Muzzle flash animations
- projectile_trail_*.ani - Projectile trail animations
- beam_effect_*.ani - Beam weapon animations

Associated PCX textures:
- weapon_impact_*.pcx - Weapon impact textures
- muzzle_flash_*.pcx - Muzzle flash textures
- projectile_trail_*.pcx - Projectile trail textures
- beam_effect_*.pcx - Beam weapon textures

### Particle Effects (.ani/.pcx)
Miscellaneous particle effects:
- engine_trail_*.ani - Engine exhaust trail animations
- thruster_*.ani - Thruster glow animations
- shield_hit_*.ani - Shield impact animations
- damage_smoke_*.ani - Hull damage smoke animations

Associated PCX textures:
- engine_trail_*.pcx - Engine trail textures
- thruster_*.pcx - Thruster glow textures
- shield_hit_*.pcx - Shield impact textures
- damage_smoke_*.pcx - Damage smoke textures

### Lighting Effects (.ani/.pcx)
Lightning.tbl and related effects:
- lightning_bolt_*.ani - Lightning bolt animations
- electrical_arc_*.ani - Electrical discharge animations
- energy_glow_*.ani - Energy weapon glow animations

Associated PCX textures:
- lightning_bolt_*.pcx - Lightning bolt textures
- electrical_arc_*.pcx - Electrical arc textures
- energy_glow_*.pcx - Energy glow textures

## Target Structure
```
/data/effects/                       # Effect data definitions
├── explosions/                      # Explosion effect definitions
├── weapons/                         # Weapon effect definitions
├── particles/                       # Particle effect definitions
├── lighting/                        # Lighting effect definitions
└── environment/                     # Environmental effect definitions

/animations/effects/                  # Effect animations directory
├── explosions/                      # Explosion animations
│   ├── fireballs/
│   ├── debris/
│   ├── shockwaves/
│   └── generic/
├── weapons/                         # Weapon animations
│   ├── impacts/
│   ├── muzzle_flashes/
│   ├── trails/
│   └── beams/
├── particles/                       # Particle animations
│   ├── engines/
│   ├── thrusters/
│   ├── shields/
│   └── damage/
├── lighting/                        # Lighting animations
│   ├── lightning/
│   ├── electrical/
│   └── energy/
└── environment/                     # Environmental animations
    ├── nebula/
    ├── stars/
    └── atmospheric/

/textures/effects/                   # Effect textures directory
├── explosions/                      # Explosion textures
│   ├── fireballs/
│   ├── debris/
│   ├── shockwaves/
│   └── generic/
├── weapons/                         # Weapon textures
│   ├── impacts/
│   ├── muzzle_flashes/
│   ├── trails/
│   └── beams/
├── particles/                       # Particle textures
│   ├── engines/
│   ├── thrusters/
│   ├── shields/
│   └── damage/
├── lighting/                        # Lighting textures
│   ├── lightning/
│   ├── electrical/
│   └── energy/
└── environment/                     # Environmental textures
    ├── nebula/
    ├── stars/
    └── atmospheric/
```

## Example Mapping
For fireball explosion effect:
- fireball.tbl entry → /data/effects/explosions/fireball.tres
- fireball_*.ani → /animations/effects/explosions/fireballs/fireball_*.png
- fireball_*.pcx → /textures/effects/explosions/fireballs/fireball_*.webp

For weapon muzzle flash:
- weapon_expl.tbl entry → /data/effects/weapons/muzzle_flash.tres
- muzzle_flash_*.ani → /animations/effects/weapons/muzzle_flashes/muzzle_flash_*.png
- muzzle_flash_*.pcx → /textures/effects/weapons/muzzle_flashes/muzzle_flash_*.webp