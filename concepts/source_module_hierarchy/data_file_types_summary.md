# Wing Commander Saga Data File Types Summary

## Overview
This document provides a comprehensive summary of all data file types used in the Wing Commander Saga Hermes campaign, organized by category and purpose.

## Table Files (.tbl)

### Core Configuration
- **ships.tbl** - Defines all spacecraft classes with complete properties
- **weapons.tbl** - Defines all weapon types and their characteristics
- **Species_defs.tbl** - Defines species properties and visual styles
- **iff_defs.tbl** - Defines faction relationships and identification
- **ai_profiles.tbl** - Defines AI behavior patterns and difficulty levels

### Visual/Audio Configuration
- **nebula.tbl** - Nebula properties and visual effects
- **fireball.tbl** - Explosion effects and properties
- **mflash.tbl** - Muzzle flash effects
- **weapon_expl.tbl** - Weapon explosion animations
- **pixels.tbl** - Pixel-based visual effects
- **lightning.tbl** - Lightning and electrical effects
- **stars.tbl** - Starfield background properties

### Interface/UX Configuration
- **hud_gauges.tbl** - HUD element definitions and properties
- **fonts.tbl** - Font definitions and character sets
- **icons.tbl** - Icon definitions for UI elements
- **mainhall.tbl** - Main hall interface configuration
- **menu.tbl** - Menu system definitions
- **help.tbl** - Help system content
- **launchhelp.tbl** - Launch help/tutorial content
- **tips.tbl** - In-game tips and hints

### Narrative/Localization
- **strings.tbl** - Game text strings and localization
- **tstrings.tbl** - Technical database strings
- **credits.tbl** - Credits and acknowledgements
- **rank.tbl** - Rank names and progression
- **medals.tbl** - Medal definitions and criteria
- **messages.tbl** - In-game message definitions
- **traitor.tbl** - Traitor detection messages
- **music.tbl** - Music track definitions
- **sounds.tbl** - Sound effect definitions
- **scripting.tbl** - Scripting function definitions

### Campaign/Progression
- **cutscenes.tbl** - Cutscene definitions and properties
- **ssm.tbl** - SSM (Space Switching Missile) definitions
- **autopilot.tbl** - Autopilot behavior definitions

## Mission Files (.fs2)

### Campaign Missions (M01-BG-Hermes.fs2 through M50-BG-Hermes.fs2)
- Define complete mission structure and gameplay
- Contain ship placements, AI directives, and events
- Include briefing/debriefing information
- Link to fiction viewer content
- Define mission objectives and success conditions

### Demo Missions (Demo-01-BG-Hermes.fs2 through Demo-05-BG-Hermes.fs2)
- Tutorial and demonstration missions
- Introduce players to game mechanics
- Provide controlled learning environments

## Fiction Files (.txt)

### Mission Fiction (d1fiction.txt through d5fiction.txt, m1fiction.txt through various)
- Narrative content setting up mission context
- Character development and story progression
- Background information on setting and situation
- Displayed in fiction viewer before missions

## Campaign Files (.fc2)

### Main Campaign
- **codename_hermes.fc2** - Main Hermes campaign definition
- **prologue.fc2** - Campaign prologue/introduction

## Other File Types

### Binary/Resource Files
- **.vf** - Font files (vector fonts)
- **.pcx** - Image files (Paletted Color eXchange)
- **.ogg** - Audio files (Ogg Vorbis format)
- **.pof** - 3D model files (Parallax Object File)
- **.eff** - Effect files (animation/effects)
- **.tbm** - Table modification files (extensions to .tbl)

### Configuration Files
- **.frc** - Friction configuration files

## File Relationships and Dependencies

### Hierarchical Structure
1. **Base Configuration** (ships.tbl, weapons.tbl, Species_defs.tbl)
   - Defines core game elements
   - Referenced by all mission files

2. **Mission Files** (.fs2)
   - Reference ship and weapon definitions
   - Include fiction file references
   - Link to audio/visual assets

3. **Fiction Files** (.txt)
   - Referenced by mission files
   - Provide narrative context

4. **Campaign Files** (.fc2)
   - Sequence mission files
   - Track player progression

### Cross-References
- Ships reference weapon capabilities
- Weapons reference ship vulnerabilities
- Missions reference ship classes and weapon types
- Fiction files connect to mission context
- Audio files linked through TBL definitions
- Visual effects linked through TBL definitions

## Data Flow in Game Execution

### Initialization Phase
1. Parse configuration TBL files
2. Load base ship/weapon definitions
3. Initialize species and IFF relationships
4. Set up AI behavior profiles

### Mission Loading Phase
1. Parse selected FS2 mission file
2. Instantiate ships from templates
3. Apply mission-specific modifications
4. Load referenced fiction content
5. Initialize mission objectives

### Runtime Phase
1. Execute mission events based on conditions
2. Update ship/weapon states
3. Process AI decisions
4. Handle player input
5. Manage narrative progression

## Conversion Mapping to Godot

### TBL Files → Godot Resources (.tres)
- Structured data converted to Resource classes
- Ship definitions → ShipClass resources
- Weapon definitions → WeaponClass resources
- Species definitions → Species resources
- IFF definitions → IFF resources

### FS2 Files → Godot Scenes (.tscn)
- Missions converted to scene compositions
- Ship placements → Scene node positions
- Events → Scripted timeline sequences
- Objectives → Mission goal nodes

### TXT Files → Godot Text Resources
- Fiction content → RichTextEffect resources
- Narrative formatting preserved
- Localization support maintained

### FC2 Files → Campaign Management System
- Mission sequencing → Level progression system
- Player state → Save game system
- Campaign variables → Global state management

## File Processing Requirements

### Text Processing
- Custom parser for TBL file format
- Multi-line text handling with $end_multi_text markers
- String localization with XSTR references
- Comment handling (lines starting with ;)

### Binary Processing
- POF model file parsing (3D geometry)
- Audio file loading (OGG format)
- Image file loading (PCX format)
- Font file processing (VF format)

### Validation Requirements
- Cross-reference checking between files
- Asset existence verification
- Data consistency validation
- Error reporting with line numbers

This comprehensive file structure enables the rich, data-driven gameplay experience that defines Wing Commander Saga, with each file type serving a specific purpose in the overall game architecture.