# WCS Data Migration Analysis Report
**Analysis Date**: 2025-01-25  
**Analyst**: Larry (WCS Analyst)  
**Project**: WCS-Godot Converter  

## Executive Summary

After conducting a deep archaeological dive into the WCS C++ codebase, I've uncovered a treasure trove of data formats that are absolutely *fascinating* from a reverse engineering perspective! The WCS data architecture shows sophisticated versioning systems, binary serialization patterns, and hierarchical data organization that we'll need to carefully migrate to Godot's modern resource system.

## 1. Save Game Data Formats (.PLR and .CSG Files)

### Player Files (.PLR)
- **Location**: `source/code/playerman/managepilot.cpp:46-76`
- **Current Version**: 242 (single player), 142 (multiplayer)
- **File Signature**: `0x46505346` ("FPSF" - FreeSpace Player File)
- **Binary Format**: Uses CFILE system with versioned serialization

**Key Data Structures**:
```cpp
typedef struct player {
    char callsign[CALLSIGN_LEN + 1];           // 32 char max
    char image_filename[MAX_FILENAME_LEN];     // pilot portrait
    char squad_filename[MAX_FILENAME_LEN];     // squadron logo
    char squad_name[NAME_LENGTH + 1];          // squadron name
    char current_campaign[MAX_FILENAME_LEN];   // active campaign
    campaign_info* campaigns;                  // multiple campaigns
    htarget_list keyed_targets[8];             // hotkey targets
    scoring_struct stats;                      // performance metrics
    // ... extensive pilot state data
} player;
```

**Critical Migration Notes**:
- Version compatibility system allows graceful upgrades
- Pilot portraits and squadron logos need asset path conversion  
- Campaign progress tracking requires state preservation
- Control configuration and HUD settings are embedded

### Campaign Save Files (.CSG)
- **Location**: `source/code/mission/missioncampaign.cpp:847-900`
- **Format**: Binary with mission state preservation
- **Contains**: Mission completion status, goals, variables, ship/weapon unlocks

**Data Flow**: Player → Campaign → Mission state chain must be preserved

## 2. Configuration and Settings Data

### Registry/Configuration System
- **Location**: `source/code/osapi/osregistry.cpp:27-100`
- **Windows**: Registry-based (`HKEY_CURRENT_USER\Software\Volition\WingCommanderSaga`)
- **Cross-platform**: INI file fallback system
- **Organization**: Company/App/Version hierarchy

**Key Configuration Categories**:
- **Graphics Settings**: Resolution, detail levels, effects
- **Audio Settings**: Music/SFX volumes, voice settings  
- **Control Configuration**: Keyboard/joystick bindings
- **Gameplay Options**: Difficulty, HUD configuration
- **Network Settings**: Multiplayer preferences

## 3. Mission and Campaign Data Structures

### Mission Files (.FS2)
- **Location**: `source/code/mission/missionparse.h:131-150`
- **Format**: Text-based with structured sections
- **Version**: 0.10f (Fred mission format)

**Mission Structure**:
```cpp
typedef struct mission {
    char name[NAME_LENGTH];                    // Mission title
    char author[NAME_LENGTH];                  // Creator
    char mission_desc[MISSION_DESC_LENGTH];    // Description
    int game_type;                            // Single/Multi/Coop/etc
    int flags;                                // Feature flags
    support_ship_info support_ships;          // Support ship config
    char loading_screen[2][MAX_FILENAME_LEN]; // Loading images
    char skybox_model[MAX_FILENAME_LEN];      // Background
    // ... extensive mission parameters
} mission;
```

### Campaign Files (.FSC)
- **Location**: `source/code/mission/missioncampaign.cpp:700-850`
- **Format**: Text-based with mission tree structure
- **Features**: Branching paths, prerequisites, variable tracking

## 4. Asset Data Formats

### 3D Models (.POF - Parallax Object Format)
- **Location**: `source/code/model/modelread.cpp:89-100`
- **Version Compatibility**: PM_COMPATIBLE_VERSION 1900, Major Version ≤ 30
- **Format**: Custom binary with BSP tree structure
- **Features**: LOD levels, subsystems, animations, collision data

**Critical Model Components**:
- **Subsystems**: Engines, turrets, sensors (12 types)
- **Animations**: Rotating parts, triggered movements
- **Collision**: BSP trees for precise hit detection
- **Materials**: Texture assignments, glow maps, damage states

### Texture Formats
**Supported Extensions** (from `source/code/cfile/cfile.cpp:48-87`):
- **Legacy**: .PCX (primary), .ANI (animations)
- **Modern**: .TGA, .JPG, .PNG, .DDS  
- **Organization**: Hierarchical directory structure

### Audio Formats
- **Music**: .OGG, .WAV
- **SFX**: .WAV, .OGG  
- **Voice**: Organized by type (briefing, personas, special)

### Table Files (.TBL/.TBM)
- **Format**: Text-based data definitions
- **Purpose**: Ship stats, weapon properties, game balance
- **Modding**: .TBM files override .TBL defaults

## 5. File System Architecture (CFILE)

The CFILE system (`source/code/cfile/cfile.cpp`) is brilliantly designed! It provides:

### Virtual File System
- **37 Path Types**: From CF_TYPE_ROOT to CF_TYPE_FICTION
- **Archive Support**: .VP files (volume packs)
- **Priority System**: Mod files override base game files
- **Cross-platform**: Unified path handling

### Key Directories:
```
data/
├── maps/          # Textures and animations
├── models/        # 3D models (.POF)
├── tables/        # Game data (.TBL/.TBM)
├── sounds/        # Audio files
├── missions/      # Mission files (.FS2)
├── players/       # Save games
│   ├── single/    # Single player (.PLR, .CSG)
│   └── multi/     # Multiplayer (.PLR)
└── config/        # Configuration files
```

## 6. Migration Script Requirements

### Priority 1: Core Data Migration
1. **Player Profile Converter**
   - Convert .PLR binary to Godot Resource format
   - Preserve pilot stats, campaign progress, settings
   - Handle version compatibility gracefully

2. **Campaign State Converter** 
   - Convert .CSG binary to Godot save format
   - Maintain mission completion tree
   - Preserve goal/variable states

3. **Configuration Migrator**
   - Extract registry/INI settings
   - Convert to Godot project settings format
   - Maintain control bindings compatibility

### Priority 2: Asset Pipeline Migration
4. **POF Model Converter**
   - Convert binary POF to Godot .scene format
   - Preserve subsystem hierarchy
   - Convert animations to Godot AnimationPlayer

5. **Texture Asset Converter**
   - Batch convert PCX/TGA to modern formats
   - Maintain directory structure in Godot
   - Generate proper .import files

6. **Mission File Parser**
   - Convert .FS2 text format to Godot scene
   - Translate ship/object positions
   - Convert SEXP logic to GDScript

### Priority 3: Advanced Features
7. **Table File Processor**
   - Convert .TBL/.TBM to Godot Resources
   - Generate typed Resource classes for data
   - Maintain modding capabilities

8. **Audio Asset Migrator**
   - Convert/copy audio files to Godot structure
   - Generate proper AudioStream resources
   - Preserve directional audio metadata

## 7. Technical Recommendations

### Data Architecture Strategy
- **Use Godot Resources**: Replace binary formats with .tres/.res files
- **Maintain Compatibility**: Support incremental migration
- **Version Control**: Implement format versioning like WCS
- **Modding Support**: Preserve override system capabilities

### Migration Script Architecture
```gdscript
class_name WCSDataMigrator
extends RefCounted

# Core migration pipeline
func migrate_player_data(plr_path: String) -> PlayerProfile
func migrate_campaign_data(csg_path: String) -> CampaignState  
func migrate_configuration(config_source: String) -> void
func migrate_assets(wcs_data_path: String) -> void
```

### Error Handling & Validation
- **Format Validation**: Verify file signatures before processing
- **Graceful Degradation**: Handle missing/corrupted data
- **Progress Reporting**: Provide detailed migration feedback
- **Rollback Capability**: Allow migration reversal if needed

## 8. Godot Integration Points

### Resource System Mapping
- **WCS .PLR** → `PlayerProfile extends Resource`
- **WCS .CSG** → `CampaignState extends Resource`  
- **WCS .POF** → `PackedScene with MeshInstance3D`
- **WCS .TBL** → `GameData extends Resource`

### Save System Integration  
- Leverage Godot's FileAccess for cross-platform compatibility
- Use ResourceSaver/ResourceLoader for type safety
- Implement auto-save using Godot's built-in systems

This analysis reveals that WCS has a remarkably sophisticated data architecture that we can faithfully recreate in Godot while gaining modern benefits like type safety, cross-platform compatibility, and integrated modding support!

---
**Next Steps**: Hand off to Mo (Godot Architect) for design of equivalent Godot systems, then to Dev for implementation of migration scripts.