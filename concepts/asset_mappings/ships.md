# Ships Asset Mapping

## Overview
This document maps the ship definitions from ships.tbl to their corresponding media assets in the Wing Commander Saga Hermes campaign.

## Asset Types

### 3D Models (.pof)
Ships.tbl references POF files that contain the 3D geometry for each ship class:
- tcf_arrow.pof - F-27B Arrow fighter
- tcf_ferret.pof - F-32B Ferret fighter
- tcf_hellcat_v.pof - F-63C Hellcat V fighter
- tcf_rapier.pof - F-44B Raptor fighter
- tcb_thunderbolt_vii.pof - F-72B Thunderbolt VII fighter
- tcs_behemoth.pof - TCS Behemoth capital ship
- tcs_prowler_d.pof - TCS Prowler-D capital ship
- tcs_venture.pof - TCS Venture capital ship
- kb_starbase.pof - Kilrathi starbase
- kim_paw.pof - Kilrathi Imperial-class PAKT
- And many others...

### Textures (.pcx)
Ship textures are typically stored in separate PCX files referenced by the POF models:
- Ship-specific diffuse textures (e.g., arrow.pcx for the Arrow fighter)
- Normal map textures (e.g., arrow_normals.pcx)
- Detail textures and other material maps

### Sounds (.wav)
Ships.tbl may reference engine and other sounds:
- Engine sounds for each ship class
- Weapon firing sounds specific to ship-mounted weapons
- Explosion sounds for ship destruction

## Target Structure
```
/data/ships/{faction}/{type}/{ship_name}.tres    # ShipClass resource
/entities/fighters/{faction}/{ship_name}/        # Entity directory
├── {ship_name}.tscn                             # Ship scene
├── {ship_name}.gd                               # Ship script
├── {ship_name}.tres                             # Ship instance data
├── {ship_name}.glb                              # Converted 3D model
├── {ship_name}_diffuse.webp                     # Diffuse texture
├── {ship_name}_normal.webp                      # Normal map
├── {ship_name}_engine.ogg                       # Engine sound
└── {ship_name}_muzzle.png                       # Muzzle flash effect
```

## Example Mapping
For F-27B Arrow fighter:
- ships.tbl entry → /data/ships/terran/fighters/arrow.tres
- tcf_arrow.pof → /entities/fighters/confed/arrow/arrow.glb
- arrow.pcx → /entities/fighters/confed/arrow/arrow_diffuse.webp
- arrow_normals.pcx → /entities/fighters/confed/arrow/arrow_normal.webp
- engine.wav → /entities/fighters/confed/arrow/arrow_engine.ogg