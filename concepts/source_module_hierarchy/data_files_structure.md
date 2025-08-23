# Wing Commander Saga Data Files Structure

## Overview
The Wing Commander Saga data files contain all the configuration, assets, and mission information needed to run the game. These files are organized into several categories that define everything from ship characteristics to mission flow and narrative content. Understanding these files is crucial for converting the game to a modern engine like Godot.

## File Types and Their Roles

### 1. TBL Files (Table Files)
TBL files are the primary configuration files that define game data in a structured format. They contain definitions for ships, weapons, species, and other game elements.

#### Key TBL Files:
- **ships.tbl**: Defines all ship classes with their properties, weapons, physics, and visual characteristics
- **weapons.tbl**: Defines all weapon types with damage, velocity, and effects
- **Species_defs.tbl**: Defines different species (Terran, Kilrathi, Pirate) with visual styles and properties
- **iff_defs.tbl**: Defines faction relationships and colors
- **ai_profiles.tbl**: Defines AI behavior profiles
- **nebula.tbl**: Defines nebula properties and effects

#### Structure of TBL Files:
TBL files use a key-value structure with sections defined by `$` prefixes:

```
$Section Name: Value
    +SubProperty: Value
    +Description:
        Multi-line text description
        $end_multi_text
```

Example from ships.tbl:
```tbl
$Name: F-27B Arrow
$Species: Terran
$POF file: tcf_arrow.pof
$Max Velocity: 0.0, 0.0, 82.1
$Shields: 800
```

### 2. FS2 Files (Mission Files)
FS2 files define individual missions with all their objects, events, and scripting. These are the core gameplay files that determine mission flow.

#### Structure of FS2 Files:
FS2 files contain multiple sections that define different aspects of a mission:

- **#Mission Info**: Basic mission metadata
- **#Objects**: All ships, weapons, and other entities in the mission
- **#Wings**: Grouped ships with coordinated behavior
- **#Events**: Scripted events and triggers
- **#Goals**: Mission objectives
- **#Cutscenes**: Video cutscenes to play

Example structure:
```fs2
#Mission Info
$Name: XSTR("Brimstone 1", -1)
$Author: Romanyuk, Schmitt

#Objects
$Name: Alpha 1
+Class: F-86C Hellcat V
+IFF: Friendly

#Events
+Name: Initial Spawn
+Formula: ( true )
```

### 3. TXT Files (Text/Narrative Files)
TXT files contain narrative content including mission fiction, briefing text, and story elements.

#### Types of TXT Files:
- **Fiction files** (m1fiction.txt, etc.): Narrative fiction that sets up the mission context
- **Briefing text**: In-mission briefing content
- **Debriefing text**: Post-mission evaluation text

Example from m1fiction.txt:
```
$BIntroduction

$BShuttle $B326

$BOn $BApproach $Bto $BTCS $BHermes$B, $BBrimstone $BSystem

"This is your Captain Crazy Jane speaking," the shuttle pilot said...
```

### 4. FC2 Files (Campaign Files)
FC2 files define campaign structure and progression, linking missions together and managing player progression.

#### Structure of FC2 Files:
- Campaign metadata (name, description, author)
- Mission sequence and dependencies
- Campaign-specific variables and flags
- Ending conditions

## Detailed File Analysis

### Ships.tbl Structure
The ships.tbl file defines all spacecraft in the game with comprehensive properties:

1. **Basic Identification**:
   - Name, alternative names, and short names
   - Species affiliation
   - Classification (fighter, bomber, capital ship)

2. **Physical Properties**:
   - Model file (POF file reference)
   - Dimensions and mass
   - Density and damping values

3. **Performance Characteristics**:
   - Maximum velocity in all axes
   - Acceleration and deceleration rates
   - Rotation times
   - Glide capabilities

4. **Combat Properties**:
   - Shield strength and color
   - Hull hitpoints
   - Armor factors
   - Weapon energy and regeneration

5. **Weapons**:
   - Primary and secondary weapon banks
   - Allowed weapon types per bank
   - Default weapon loadouts
   - Ammunition capacity

6. **Visual Effects**:
   - Thruster animations and glows
   - Explosion properties
   - Shockwave effects

7. **Audio**:
   - Engine sound references
   - Weapon firing sounds

### Weapons.tbl Structure
The weapons.tbl file defines all weapons with their characteristics:

1. **Basic Properties**:
   - Name and description
   - Technical database information
   - Model file reference

2. **Visual Effects**:
   - Laser bitmap and glow
   - Color properties
   - Length and radius

3. **Ballistics**:
   - Velocity and mass
   - Fire rate (fire wait)
   - Lifetime

4. **Damage**:
   - Base damage
   - Armor, shield, and subsystem factors
   - Special effects (homing, EMP, etc.)

5. **Resource Usage**:
   - Energy consumption
   - Cargo space requirements

6. **Audio/Visual**:
   - Launch and impact sounds
   - Impact explosion effects

### Mission Files (FS2) Structure
Mission files are the most complex data files, containing complete mission definitions:

1. **Mission Info Section**:
   - Version information
   - Mission name and author
   - Creation/modification dates
   - Mission description
   - Game type flags

2. **Object Definitions**:
   - Ships with class, position, and orientation
   - Initial velocity and AI class
   - Weapon loadouts
   - IFF assignments

3. **Wing Definitions**:
   - Grouped ships with formation flying
   - Arrival and departure cues
   - Wave management

4. **Events Section**:
   - Scripted events with conditions
   - Actions to perform when triggered
   - Message displays and cutscenes

5. **Goals Section**:
   - Primary, secondary, and bonus objectives
   - Success/failure conditions

6. **Cutscenes**:
   - Video cutscene references
   - Trigger conditions

### Fiction Files (TXT) Structure
Fiction files provide narrative context and are displayed in the fiction viewer:

1. **Formatting Codes**:
   - `$B` for bold text
   - `$Title` for section headers
   - Line breaks and spacing

2. **Content Structure**:
   - Mission setting and context
   - Character introductions
   - Story progression elements

## Data Relationships

### Ship-Weapon Relationships
- Ships define which weapons they can carry
- Weapons define their effects on different ship types
- Species definitions affect weapon availability

### Mission-Ship Relationships
- Missions place specific ship instances
- Ship classes define the properties of mission ships
- AI profiles determine ship behavior in missions

### Campaign-Mission Relationships
- Campaign files sequence missions
- Missions reference campaign variables
- Player progression tracked across missions

## Conversion Considerations for Godot

### TBL Files to Godot Resources
- Convert to `.tres` resource files
- Use Godot's resource system for data-driven design
- Create specific resource types for ships, weapons, etc.

### FS2 Files to Godot Scenes
- Convert to `.tscn` scene files
- Use Godot's node system for object placement
- Implement events using Godot's scripting system

### TXT Files to Godot Text Resources
- Convert to formatted text resources
- Use Godot's rich text capabilities
- Implement fiction viewer as UI scene

### FC2 Files to Campaign Management
- Convert to campaign progression system
- Use Godot's save system for player state
- Implement mission sequencing logic

## File Processing Pipeline

1. **Parsing Phase**:
   - Read TBL files to build game data
   - Parse FS2 files for mission structure
   - Load TXT files for narrative content

2. **Validation Phase**:
   - Check for missing references
   - Validate data consistency
   - Ensure all required assets exist

3. **Runtime Phase**:
   - Load mission data on demand
   - Instantiate objects from templates
   - Execute mission events and scripting

## Integration with Game Systems

### Asset Management
- POF model files referenced in TBL files
- Texture and animation files linked to objects
- Sound files referenced by name/ID

### Game Logic
- AI behavior defined in TBL files
- Mission objectives defined in FS2 files
- Event scripting using conditional logic

### User Interface
- Text content from TXT files
- Technical database from TBL descriptions
- Mission briefings from FS2 files

This data file structure provides a comprehensive, data-driven approach to game design that can be effectively converted to Godot's resource and scene systems while preserving the original gameplay experience.