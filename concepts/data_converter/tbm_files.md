# TBM Files Conversion Requirements

## Overview
TBM (Table Modular) files contain modular overrides and extensions to base TBL files in Wing Commander Saga. These files need to be parsed and integrated with their base table counterparts during the conversion process, following Godot's feature-based organization principles and the hybrid model defined in our project structure.

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
- Load base table data from converted resources in `/assets/data/` directories
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

## Directory Structure Alignment
Following the Godot project structure defined in directory_structure.md and the hybrid organizational model:

### Assets Directory Structure (Global Data)
Global data resources that follow the "Global Litmus Test" principle: "If I delete three random features, is this asset still needed?"

```
assets/
├── audio/                         # Shared audio files
│   ├── sfx/                       # Generic sound effects
│   ├── music/                     # Background music tracks
│   └── ui/                        # UI sound effects
├── behavior_trees/                # Shared LimboAI behavior trees
│   ├── ai/                        # AI behavior trees
│   │   ├── combat/                # Combat-related behavior trees
│   │   ├── navigation/            # Navigation behavior trees
│   │   └── tactical/              # Tactical behavior trees
│   └── mission/                   # Mission-specific behavior trees
├── data/                          # Shared data resources
│   ├── ai/                        # AI data resources
│   │   └── profiles/              # AI profile definitions
│   │       ├── base.tres          # Base AI profiles
│   │       └── overrides/         # TBM override files
│   ├── ships/                     # Ship data resources
│   │   ├── base.tres              # Base ship definitions
│   │   └── overrides/             # TBM override files
│   ├── weapons/                   # Weapon data resources
│   │   ├── base.tres              # Base weapon definitions
│   │   └── overrides/             # TBM override files
│   ├── species/                   # Species data resources
│   │   ├── base.tres              # Base species definitions
│   │   └── overrides/             # TBM override files
│   ├── iff/                       # IFF relationship data
│   │   ├── base.tres              # Base IFF definitions
│   │   └── overrides/             # TBM override files
│   ├── armor/                     # Armor type data
│   │   ├── base.tres              # Base armor definitions
│   │   └── overrides/             # TBM override files
│   └── effects/                   # Effect data resources
│       ├── base.tres              # Base effect definitions
│       └── overrides/             # TBM override files
├── textures/                      # Shared texture files
│   ├── ui/                        # Generic UI elements
│   ├── effects/                   # Particle textures used by multiple effects
│   └── fonts/                     # Font textures
└── animations/                    # Shared animation files
    ├── ui/                        # UI animations
    └── effects/                   # Generic effect animations
```

## Integration Points

### Data Converter Output Mapping
- ShipClass overrides → Merged with base resources in `/assets/data/ships/`
- WeaponClass overrides → Merged with base resources in `/assets/data/weapons/`
- AIProfile overrides → Merged with base resources in `/assets/data/ai/profiles/`
- Species overrides → Merged with base resources in `/assets/data/species/`
- IFF overrides → Merged with base resources in `/assets/data/iff/`
- ArmorType overrides → Merged with base resources in `/assets/data/armor/`
- Effect overrides → Merged with base resources in `/assets/data/effects/`

### Resource References
- **Entity scenes** in `/features/` reference updated data resources from `/assets/data/`
- **Mission scenes** in `/campaigns/{campaign}/missions/` reference updated data resources
- **AI systems** in `/scripts/ai/` reference updated AIProfile resources
- **Weapon systems** in `/scripts/weapons/` reference updated WeaponClass resources

## Relationship to Other Assets

### Entity Integration
TBM-modified data integrates with entity scenes following the feature-based organization:
- Modified ship classes are referenced by ship entity scenes in `/features/fighters/{faction}_{ship_name}/{ship_name}.tres`
- Updated weapon classes are referenced by weapon entity scenes in `/features/weapons/{weapon_name}/{weapon_name}.tres`
- Changed AI profiles are referenced by AI behavior scripts in `/scripts/ai/`
- Modified effect resources are used by visual effect entities in `/features/effects/{effect_name}/{effect_name}.tres`

### System Integration
TBM data integrates with Godot systems in `/scripts/` directories following the separation of concerns:
- `/scripts/ai/ai_behavior.gd` - AI behavior adjusted by modified profiles
- `/scripts/weapons/weapon_system.gd` - Weapon behavior adjusted by modified properties
- `/scripts/physics/flight_model.gd` - Physics behavior adjusted by modified ship properties
- `/scripts/mission/mission_manager.gd` - Mission behavior adjusted by modified data

### Closely Related Assets
- Base TBL files that are being extended or modified and converted to `/assets/data/` directories
- Mission files that reference the modified table data from `/campaigns/` directories
- Ship and weapon models affected by property changes from `/features/` directories
- AI behavior files that depend on modified profiles from `/scripts/ai/` directories

### Entity Asset Organization
Each entity in `/features/` references data resources from `/assets/data/` directories:
- Ship entities reference modified ShipClass resources from `/assets/data/ships/{ship_class}.tres`
- Weapon entities reference updated WeaponClass resources from `/assets/data/weapons/{weapon_class}.tres`
- Effect entities reference modified Effect resources from `/assets/data/effects/{effect_name}.tres`
- AI-controlled entities reference adjusted AIProfile resources from `/assets/data/ai/profiles/{profile_name}.tres`

### Common Shared Assets
Following the "Global Litmus Test" principle for assets that belong in `/assets/data/`:
- Standard override processing logic used across all table types
- Shared validation rules for data integrity
- Common property inheritance patterns from base resources
- Standard conflict resolution mechanisms for TBM merging
- Shared metadata for tracking modifications
- Universal data processing utilities

This structure follows the hybrid approach where truly global, context-agnostic data assets are organized in `/assets/` following the "Global Litmus Test" principle: "If I delete three random features, is this asset still needed?". The structure maintains clear separation of concerns between different data types while ensuring easy access to all data resources needed for game features, with TBM overrides properly integrated into the base data resources. The organization aligns with the target directory structure defined in `directory_structure.md` and follows the integration plan outlined in `integration_plan.md`.