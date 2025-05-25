# WCS FRED2 Mission Editor - Comprehensive System Analysis

## Executive Summary

FRED2 (FreeSpace Editor 2) is a sophisticated mission editor for the Wing Commander Saga engine, consisting of approximately 80+ C++ source files with complex MFC-based Windows UI and a partially-implemented cross-platform wxWidgets version. The system manages mission creation, editing, and validation through a rich set of interconnected subsystems handling everything from 3D object placement to complex event scripting.

**Key Finding**: FRED2 is a mission-critical development tool with high technical complexity that will require a complete architectural redesign for Godot implementation rather than direct porting.

## System Architecture Overview

### 1. Core Application Framework

**Primary Implementation**: `source/code/fred2/` (Windows MFC version)
**Cross-Platform Attempt**: `source/code/wxfred2/` (Incomplete wxWidgets version)

**Main Application Structure**:
- **CFREDApp** (`fred.cpp/h`): Main application class with Windows-specific initialization
- **CMainFrame** (`mainfrm.cpp/h`): Primary window frame with dockable toolbars
- **CFREDDoc** (`freddoc.cpp/h`): Document management for mission files
- **CFREDView** (`fredview.cpp/h`): 3D viewport with camera controls and object manipulation

### 2. Mission Data Management System

**Core Files**: `source/code/mission/missionparse.cpp/h`

**Mission File Format (.fs2)**:
```cpp
typedef struct mission {
    char name[NAME_LENGTH];
    char author[NAME_LENGTH];
    float version;
    char mission_desc[MISSION_DESC_LENGTH];
    int game_type;
    int flags;
    int num_players;
    uint num_respawns;
    support_ship_info support_ships;
    mission_cutscene cutscenes[...];
    // ... extensive additional fields
} mission;
```

**Parse Objects Structure**:
```cpp
typedef struct p_object {
    char name[NAME_LENGTH];
    vec3d pos;
    matrix orient;
    int ship_class;
    int team;
    int behavior;
    int ai_goals;
    int arrival_cue;    // SEXP node reference
    int departure_cue;  // SEXP node reference
    // ... 50+ additional fields for comprehensive ship configuration
} p_object;
```

### 3. SEXP (S-Expression) Scripting System

**Core Files**: `source/code/parse/sexp.cpp/h`, `source/code/fred2/sexp_tree.cpp/h`

**Architecture**:
- **Node-based tree structure** for complex conditional logic
- **1000+ built-in operators** across 10 major categories
- **Real-time validation** and type checking
- **Visual tree editor** with drag-and-drop support

**Categories Include**:
- Objective management (goals, events)
- AI behavior control
- Ship/wing status checking
- Mathematical operations
- Mission flow control
- Messaging and briefings
- Campaign progression

**Example SEXP Structure**:
```
(when
    (and
        (is-destroyed-delay "Ship1" 5)
        (< (distance "Player" "Waypoint1") 1000)
    )
    (send-message "Objective Complete" "Command" "High" 0)
    (end-mission-delay 10)
)
```

### 4. Object Management System

**Ship Editor**: `source/code/fred2/ShipEditorDlg.cpp/h`
- Complete ship configuration (class, team, AI, weapons)
- Arrival/departure conditions via SEXP trees
- Initial status and special properties
- Cargo and persona assignment

**Wing Formation Editor**: `source/code/fred2/wing_editor.cpp/h`
- Multi-ship group management
- Formation patterns and behavior
- Coordinated arrival/departure sequences

**Waypoint System**: `source/code/fred2/waypointpathdlg.cpp/h`
- 3D navigation path creation
- AI goal integration
- Mission flow waypoints

### 5. Event and Goal System

**Event Editor**: `source/code/fred2/eventeditor.cpp/h`
```cpp
class event_editor {
    event_sexp_tree m_event_tree;
    mission_event m_events[MAX_MISSION_EVENTS];
    // Real-time event validation and testing
};
```

**Mission Goals**: Integrated with SEXP system for:
- Primary/secondary objectives
- Bonus objectives  
- Failure conditions
- Dynamic goal modification

### 6. Briefing and Campaign Integration

**Briefing Editor**: `source/code/fred2/briefingeditordlg.cpp/h`
- Animated briefing sequences
- Icon placement and movement
- Voice acting integration
- Multi-stage briefing support

**Campaign Editor**: `source/code/fred2/campaigneditordlg.cpp/h`
- Mission branching logic
- Campaign-wide variable tracking
- Asset management across missions

### 7. Asset Integration System

**3D Model Rendering**: Integration with WCS rendering pipeline
- Real-time ship model display
- Subsystem visualization
- Texture replacement system

**Background Management**: `source/code/fred2/bgbitmapdlg.cpp/h`
- Starfield configuration
- Nebula effects
- Environment lighting

### 8. Validation and Quality Assurance

**Error Checking System**:
- Comprehensive mission validation
- SEXP logic verification
- Asset reference checking
- Performance optimization warnings

## Mission File Format Analysis

### File Structure (.fs2)
```
#Mission Info
$Version: 0.10
$Name: Mission Title
$Author: Creator Name
$Created: Date/Time
$Modified: Date/Time
...

#Objects
$Ships:
// Ship definitions with full configuration

$Wings:
// Wing formation definitions

#Plot Info
$Events:
// SEXP-based mission events

$Goals:
// Mission objectives

#Background
$Starfield:
// Environment configuration

#Briefing
// Briefing data and animations
```

### Key Data Structures

**Critical Dependencies**:
- **Object System**: 3D positioning, orientation, physics
- **AI System**: Behavior trees, goals, orders
- **Asset Manager**: Ship classes, weapons, textures
- **Campaign System**: Mission flow, variables, branching

## Technical Complexity Assessment

### High Complexity Components
1. **SEXP System**: 1000+ operators, complex validation, visual editing
2. **3D Viewport**: Real-time rendering, object manipulation, camera controls
3. **Event System**: Real-time validation, complex dependency tracking
4. **Asset Integration**: Deep coupling with game engine systems

### Medium Complexity Components
1. **Mission File I/O**: Well-defined format, extensive parsing
2. **Dialog Management**: Standard property pages and editors
3. **Object Configuration**: Form-based editing with validation

### Low Complexity Components
1. **Briefing Editor**: Mostly data entry with simple animation
2. **Campaign Editor**: File management and linking system

## Integration Requirements with WCS Systems

### Direct Dependencies
- **Ship/Weapon Classes**: `source/code/ship/`, `source/code/weapon/`
- **AI System**: `source/code/ai/`
- **Physics**: `source/code/physics/`
- **Asset Loading**: `source/code/model/`, `source/code/bmpman/`
- **Math Library**: `source/code/math/`

### Indirect Dependencies
- **Mission Runtime**: For validation and testing
- **Campaign System**: For mission integration
- **Audio System**: For briefing voice-overs
- **Rendering**: For 3D preview capabilities

## Cross-Platform Implementation Analysis

### wxfred2 Status
The `source/code/wxfred2/` directory contains a **minimal, incomplete** cross-platform implementation:
- **Basic framework only** (application shell, menu structure)
- **No core editing functionality** implemented
- **Proof-of-concept level** - not production ready
- **Missing**: 3D viewport, SEXP editor, object manipulation, file I/O

### Implementation Challenges
1. **Platform-specific 3D rendering** (Direct3D → OpenGL transition needed)
2. **Complex UI components** (tree controls, property sheets, custom widgets)
3. **File system integration** (Windows-specific paths and registry usage)
4. **Memory management** (MFC patterns vs. modern C++ practices)

## Recommended Conversion Approach for Godot

### Phase 1: Core Data Model (High Priority)
1. **Mission Data Structure**: Convert C++ structs to GDScript classes
2. **SEXP System**: Node-based system using Godot's built-in tree structures
3. **File I/O**: Custom parser for .fs2 format with robust error handling
4. **Object Management**: Godot scene-based object representation

### Phase 2: Essential Editing Tools (High Priority)
1. **3D Viewport**: Godot's built-in 3D editor integration
2. **Object Placement**: Gizmo-based manipulation tools
3. **Property Editors**: Godot UI-based configuration panels
4. **Basic SEXP Editor**: Tree-based visual scripting interface

### Phase 3: Advanced Features (Medium Priority)
1. **Advanced SEXP Operations**: Full operator set implementation
2. **Briefing System**: Animation timeline editor
3. **Event Validation**: Real-time logic checking
4. **Asset Preview**: Integration with Godot's asset pipeline

### Phase 4: Professional Features (Lower Priority)
1. **Campaign Integration**: Multi-mission management
2. **Error Checking**: Comprehensive validation system
3. **Export Tools**: Direct integration with WCS-Godot runtime
4. **Collaboration Tools**: Version control and sharing features

## Architecture Recommendations for Godot Implementation

### Core Design Principles
1. **Scene-based Architecture**: Each mission as a Godot scene
2. **Node-centric Design**: Objects as specialized nodes with custom components
3. **Signal-driven Communication**: Replace direct coupling with signal/slot patterns
4. **Resource-based Assets**: Leverage Godot's resource system for ship classes, weapons
5. **Tool Script Integration**: Built-in editor extensions for custom functionality

### Proposed Godot Structure
```
MissionEditor/
├── core/
│   ├── MissionData.gd          # Core mission data structure
│   ├── ParseObject.gd          # Individual object representation
│   ├── SexpSystem.gd           # S-expression evaluation engine
│   └── FileIO.gd               # Mission file parser/writer
├── ui/
│   ├── MainEditor.tscn/gd      # Primary editor interface
│   ├── ObjectInspector.gd      # Property editing panels
│   ├── SexpEditor.gd           # Visual scripting interface
│   └── Viewport3D.gd           # 3D manipulation viewport
├── tools/
│   ├── Validators.gd           # Mission validation tools
│   ├── AssetManager.gd         # Asset integration system
│   └── ExportTools.gd          # Export to runtime format
└── data/
    ├── ship_classes.tres       # Ship class definitions
    ├── weapon_types.tres       # Weapon configurations
    └── sexp_operators.tres     # SEXP operator definitions
```

### Key Conversion Challenges

1. **SEXP System Complexity**: 1000+ operators with complex interdependencies
2. **3D Manipulation**: Camera controls, object selection, gizmo interactions
3. **Real-time Validation**: Performance considerations for large missions
4. **Asset Integration**: Seamless workflow with Godot's asset pipeline
5. **File Format Compatibility**: Maintaining .fs2 file format compatibility

## Conclusion

FRED2 represents a mature, feature-rich mission editor with deep integration into the WCS engine. The conversion to Godot will require:

- **Complete architectural redesign** leveraging Godot's strengths
- **Significant development effort** (~6-12 months for core functionality)
- **Careful preservation** of existing mission file compatibility
- **Gradual migration strategy** with incremental feature implementation

The analysis reveals that while complex, the conversion is highly feasible and will result in a more maintainable, cross-platform solution that leverages Godot's modern editor architecture and built-in 3D capabilities.

**Next Steps**: Proceed with PRD creation for a Godot-native mission editor that preserves FRED2's essential capabilities while modernizing the user experience and technical foundation.