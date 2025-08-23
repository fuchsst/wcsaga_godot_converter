# TBL Files Conversion Requirements

## Overview
TBL (Table) files contain structured data definitions for various game elements in Wing Commander Saga. These files need to be converted to Godot's resource format (.tres) to maintain the data-driven design approach, following Godot's feature-based organization principles.

## File Types and Conversion Requirements

### Ship Definitions (ships.tbl)
**Purpose**: Defines all playable and AI ship classes with their properties
**Source Format**: Custom TBL format with sections for each ship class
**Target Format**: ShipClass resources (.tres)
**Conversion Requirements**:
- Parse ship names, descriptions, and classifications
- Extract physics properties (mass, max velocity, acceleration)
- Convert weapon hardpoints and subsystem locations
- Map damage characteristics and armor values
- Preserve IFF (Identification Friend or Foe) settings
- Maintain 3D model references for later POF conversion
- Handle modular TBM overrides

### Weapon Definitions (weapons.tbl)
**Purpose**: Defines all weapon types with their characteristics
**Source Format**: Custom TBL format with weapon sections
**Target Format**: WeaponClass resources (.tres)
**Conversion Requirements**:
- Parse weapon names, descriptions, and types (laser, missile, etc.)
- Extract damage values, fire rates, and ranges
- Convert homing characteristics for missiles
- Map special effects (EMP, electronics, spawn weapons)
- Preserve 3D model references for later POF conversion
- Handle beam weapon properties (duration, width)
- Maintain audio references for firing/impact sounds

### AI Profiles (ai_profiles.tbl)
**Purpose**: Defines AI behavior characteristics and difficulty settings
**Source Format**: Custom TBL format with AI profile sections
**Target Format**: AIProfile resources (.tres)
**Conversion Requirements**:
- Parse profile names and descriptions
- Extract behavior parameters (aggression, courage, accuracy)
- Convert tactical preferences (strafing, evasion patterns)
- Map weapon selection preferences
- Maintain difficulty scaling factors

### Species Definitions (species_defs.tbl)
**Purpose**: Defines alien species properties and characteristics
**Source Format**: Custom TBL format with species sections
**Target Format**: Species resources (.tres)
**Conversion Requirements**:
- Parse species names and descriptions
- Extract thruster animation references
- Convert debris behavior properties
- Map species-specific visual effects
- Maintain IFF relationship mappings

### IFF Definitions (iff_defs.tbl)
**Purpose**: Defines faction relationships and identification properties
**Source Format**: Custom TBL format with IFF sections
**Target Format**: IFF resources (.tres)
**Conversion Requirements**:
- Parse faction names and descriptions
- Extract color codes for radar/HUD display
- Convert relationship matrices (friendly, hostile, neutral)
- Map species affiliations
- Maintain team assignments

### Armor Types (armor.tbl)
**Purpose**: Defines damage resistance properties for different armor types
**Source Format**: Custom TBL format with armor type sections
**Target Format**: ArmorType resources (.tres)
**Conversion Requirements**:
- Parse armor type names and descriptions
- Extract damage factor multipliers for different weapon types
- Convert shield penetration properties
- Map armor to specific subsystems or ships

### Particle Effects (particles.tbl)
**Purpose**: Defines particle effect properties and behaviors
**Source Format**: Custom TBL format with particle effect sections
**Target Format**: ParticleEffect resources (.tres)
**Conversion Requirements**:
- Parse effect names and descriptions
- Extract particle properties (size, lifetime, velocity)
- Convert visual properties (color, texture references)
- Map emission patterns and behaviors
- Maintain special effect flags

### Animation Definitions (anim.tbl)
**Purpose**: Defines animation sequences and properties
**Source Format**: Custom TBL format with animation sections
**Target Format**: Animation resources (.tres)
**Conversion Requirements**:
- Parse animation names and descriptions
- Extract frame sequences and timing
- Convert animation type properties
- Map animations to specific game events
- Maintain animation groupings

## Conversion Process

### 1. Parsing Phase
- Read TBL file line by line
- Identify section headers and data blocks
- Parse key-value pairs within sections
- Handle comments and special directives
- Validate data integrity

### 2. Data Transformation Phase
- Map WCS data structures to Godot resource properties
- Convert units and coordinate systems where necessary
- Apply default values for missing data
- Resolve cross-references between table entries
- Handle modular TBM file overrides

### 3. Resource Generation Phase
- Create Godot Resource objects for each table entry
- Serialize resources to .tres files
- Organize resources in feature-based directory structure following Godot conventions
- Generate metadata for relationship mapping
- Validate generated resources

## Feature-Based Directory Structure
Following Godot's recommended directory structure:
```
/data/
├── ships/                 # Ship data resources
│   ├── terran/            # Terran ship data
│   │   ├── fighters/
│   │   ├── bombers/
│   │   ├── capitals/
│   │   └── support/
│   ├── kilrathi/          # Kilrathi ship data
│   │   ├── fighters/
│   │   ├── bombers/
│   │   └── capitals/
│   ├── pirate/            # Pirate ship data
│   │   ├── fighters/
│   │   └── capitals/
│   └── templates/         # Ship data templates
├── weapons/               # Weapon data resources
│   ├── terran/            # Terran weapon data
│   ├── kilrathi/          # Kilrathi weapon data
│   ├── pirate/            # Pirate weapon data
│   └── templates/         # Weapon data templates
├── ai/                    # AI behavior data
│   ├── profiles/          # AI behavior profiles
│   ├── behaviors/         # AI behavior trees
│   ├── tactics/           # Combat tactics
│   ├── formations/        # Formation flying patterns
│   └── goals/             # AI goals
├── species/               # Species data
├── iff/                   # IFF relationship data
├── armor/                 # Armor type data
└── effects/               # Effect data resources
```

## Entity Integration
Converted TBL data integrates with entity scenes in the `/entities/` directory:
- ShipClass resources link to `/entities/fighters/{faction}/{ship_name}/` directories
- WeaponClass resources link to `/entities/weapons/{weapon_name}/` directories
- AIProfile resources are referenced by ship entities
- Effect resources are used by visual effect entities

## Common Shared Assets
- Cross-faction weapon definitions (shared between Terran and Kilrathi)
- Standard particle effects used across multiple systems
- Common animation sequences for UI elements
- Shared IFF color definitions for radar display
- Universal AI behavior templates