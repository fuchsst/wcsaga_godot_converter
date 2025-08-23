# TBM Files Conversion Requirements

## Overview
TBM (Table Modular) files contain modular overrides and extensions to base TBL files in Wing Commander Saga. These files need to be parsed and integrated with their base table counterparts during the conversion process, following Godot's feature-based organization principles.

## File Types and Conversion Requirements

### Ship Definition Overrides
**Purpose**: Modifying or extending base ship properties
**Source Format**: TBM format with ship class sections
**Target Format**: Extensions to ShipClass resources
**Conversion Requirements**:
- Parse override properties for existing ship classes
- Merge with base ship definitions from TBL files
- Handle addition of new ship classes
- Maintain consistency with base table data
- Generate updated resource files with merged properties

### Weapon Definition Extensions
**Purpose**: Adding new weapons or modifying existing ones
**Source Format**: TBM format with weapon sections
**Target Format**: Extensions to WeaponClass resources
**Conversion Requirements**:
- Parse new weapon definitions
- Modify existing weapon properties
- Handle weapon balance adjustments
- Maintain compatibility with base weapon data
- Generate updated resource files with merged properties

### AI Profile Modifications
**Purpose**: Adjusting AI behaviors and difficulty settings
**Source Format**: TBM format with AI profile sections
**Target Format**: Extensions to AIProfile resources
**Conversion Requirements**:
- Parse modified AI behavior parameters
- Adjust tactical preferences and settings
- Handle difficulty scaling changes
- Maintain base AI profile compatibility
- Generate updated resource files with merged properties

### Species and IFF Extensions
**Purpose**: Adding new species or modifying faction relationships
**Source Format**: TBM format with species/IFF sections
**Target Format**: Extensions to Species/IFF resources
**Conversion Requirements**:
- Parse new species definitions
- Modify existing species properties
- Adjust IFF relationship matrices
- Handle cross-faction relationship changes
- Generate updated resource files with merged properties

## Conversion Process

### 1. Dependency Analysis Phase
- Identify base TBL file for each TBM
- Parse TBM file headers and structure
- Extract override and extension definitions
- Validate compatibility with base files
- Check for circular dependencies

### 2. Merge Processing Phase
- Load base table data from converted resources in `/data/` directories
- Parse TBM override sections
- Apply modifications to base properties
- Handle property additions and deletions
- Resolve conflicts between multiple TBM files

### 3. Validation Phase
- Validate merged data integrity
- Check for missing references or dependencies
- Verify property value ranges and constraints
- Ensure consistency with game balance
- Generate error reports for issues

### 4. Resource Update Phase
- Update existing Godot resources with merged data
- Create new resources for added definitions
- Maintain cross-references between resources using Godot's resource system
- Generate updated metadata and indices
- Validate resource compatibility

## Feature-Based Directory Structure
Following Godot's recommended directory structure:
```
/data/
├── ships/                 # Ship data resources
│   ├── terran/            # Terran ship data
│   │   ├── fighters/
│   │   │   ├── base.tres   # Base ship definitions
│   │   │   └── overrides/   # TBM override files
│   │   │       ├── expansion_pack.tbm
│   │   │       └── mod_override.tbm
│   │   ├── bombers/
│   │   │   ├── base.tres
│   │   │   └── overrides/
│   │   ├── capitals/
│   │   │   ├── base.tres
│   │   │   └── overrides/
│   │   └── support/
│   │       ├── base.tres
│   │       └── overrides/
│   ├── kilrathi/          # Kilrathi ship data
│   │   ├── fighters/
│   │   │   ├── base.tres
│   │   │   └── overrides/
│   │   ├── bombers/
│   │   │   ├── base.tres
│   │   │   └── overrides/
│   │   └── capitals/
│   │       ├── base.tres
│   │       └── overrides/
│   ├── pirate/            # Pirate ship data
│   │   ├── fighters/
│   │   │   ├── base.tres
│   │   │   └── overrides/
│   │   └── capitals/
│   │       ├── base.tres
│   │       └── overrides/
│   └── templates/         # Ship data templates
│       ├── base.tres
│       └── overrides/
├── weapons/               # Weapon data resources
│   ├── terran/            # Terran weapon data
│   │   ├── base.tres
│   │   └── overrides/
│   ├── kilrathi/          # Kilrathi weapon data
│   │   ├── base.tres
│   │   └── overrides/
│   ├── pirate/            # Pirate weapon data
│   │   ├── base.tres
│   │   └── overrides/
│   └── templates/         # Weapon data templates
│       ├── base.tres
│       └── overrides/
├── ai/                    # AI behavior data
│   ├── profiles/          # AI behavior profiles
│   │   ├── base.tres
│   │   └── overrides/
│   ├── behaviors/         # AI behavior trees
│   │   ├── base.tres
│   │   └── overrides/
│   ├── tactics/           # Combat tactics
│   │   ├── base.tres
│   │   └── overrides/
│   ├── formations/        # Formation flying patterns
│   │   ├── base.tres
│   │   └── overrides/
│   └── goals/             # AI goals
│       ├── base.tres
│       └── overrides/
├── species/               # Species data
│   ├── base.tres
│   └── overrides/
├── iff/                   # IFF relationship data
│   ├── base.tres
│   └── overrides/
├── armor/                 # Armor type data
│   ├── base.tres
│   └── overrides/
└── effects/               # Effect data resources
    ├── base.tres
    └── overrides/
```

## Entity Integration
TBM-modified data integrates with entity scenes in `/entities/` directories:
- Modified ship classes link to `/entities/fighters/{faction}/{ship_name}/` directories
- Updated weapon classes link to `/entities/weapons/{weapon_name}/` directories
- Changed AI profiles are referenced by ship entities
- Modified effect resources are used by visual effect entities

## System Integration
TBM data integrates with Godot systems in `/systems/` directories:
- `/systems/ai/` - AI behavior adjusted by modified profiles
- `/systems/weapon_control/` - Weapon behavior adjusted by modified properties
- `/systems/physics/` - Physics behavior adjusted by modified ship properties
- `/systems/mission_control/` - Mission behavior adjusted by modified data

## Closely Related Assets
- Base TBL files that are being extended or modified and converted to `/data/` directories
- Mission files that reference the modified table data from `/missions/` directories
- Ship and weapon models affected by property changes from `/entities/` directories
- AI behavior files that depend on modified profiles from `/systems/ai/` directories

## Entity Asset Organization
Each entity in `/entities/` references data resources from `/data/` directories:
- Ship entities reference modified ShipClass resources from `/data/ships/{faction}/{type}/`
- Weapon entities reference updated WeaponClass resources from `/data/weapons/{faction}/`
- Effect entities reference modified Effect resources from `/data/effects/`
- AI-controlled entities reference adjusted AIProfile resources from `/data/ai/profiles/`

## Common Shared Assets
- Standard override processing logic used across all table types in `/core/` directories
- Shared validation rules for data integrity in `/core/validation/`
- Common property inheritance patterns from `/data/templates/`
- Standard conflict resolution mechanisms in `/core/conflict_resolution/`
- Shared metadata for tracking modifications in `/core/metadata/`
- Universal data processing utilities from `/core/utils/`