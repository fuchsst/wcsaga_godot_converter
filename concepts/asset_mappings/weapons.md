# Weapons Asset Mapping

## Overview
This document maps the weapon definitions from weapons.tbl to their corresponding media assets in the Wing Commander Saga Hermes campaign.

## Asset Types

### 3D Models (.pof)
Weapons.tbl references POF files for projectile models:
- tcm_dart.pof - Dart projectile model
- tcm_javelin.pof - Javelin projectile model
- tcm_spiculum.pof - Spiculum projectile model
- tcm_lance.pof - Lance projectile model
- tcm_warhammer.pof - Warhammer projectile model
- misc_ghostmissile.pof - Ghost missile model

### Textures (.pcx)
Weapon textures referenced by POF models:
- Projectile-specific textures for visual appearance
- Glow and effect textures for weapon trails
- Muzzle flash effects

### Sounds (.wav)
Weapons.tbl references various audio files:
- Firing sounds for each weapon type
- Impact sounds for weapon hits
- Explosion sounds for warheads
- Reload/charging sounds
- Special effect sounds (e.g., EMP discharge)

### Animations (.ani)
Animated effects for weapons:
- Muzzle flash animations
- Projectile trail effects
- Impact explosion animations
- Charging/arming sequences

## Target Structure
```
/data/weapons/{faction}/{weapon_type}/{weapon_name}.tres    # WeaponClass resource
/entities/weapons/{weapon_name}/                           # Weapon entity directory
├── {weapon_name}.tscn                                    # Weapon scene
├── {weapon_name}.gd                                      # Weapon script
├── {weapon_name}.tres                                    # Weapon instance data
├── {weapon_name}.glb                                     # Weapon 3D model
├── {weapon_name}_texture.webp                           # Weapon texture
├── {weapon_name}_fire.ogg                               # Firing sound
├── {weapon_name}_impact.ogg                             # Impact sound
├── {weapon_name}_muzzle.png                             # Muzzle flash
└── {weapon_name}_trail.webp                             # Projectile trail
```

## Example Mapping
For Dart missile:
- weapons.tbl entry → /data/weapons/terran/missiles/dart.tres
- tcm_dart.pof → /entities/weapons/dart/dart.glb
- dart_texture.pcx → /entities/weapons/dart/dart_texture.webp
- dart_fire.wav → /entities/weapons/dart/dart_fire.ogg
- dart_impact.wav → /entities/weapons/dart/dart_impact.ogg
- muzzle_flash.ani → /entities/weapons/dart/dart_muzzle.png