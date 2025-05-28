# EPIC-005: GFRED2 Mission Editor - WCS Source Dependencies

**Epic**: EPIC-005 - GFRED2 Mission Editor  
**Analyst**: Larry (WCS Analyst)  
**Analysis Date**: 2025-01-27  

This document maps the usage relationships between GFRED2 files, showing which files depend on core FRED2 components and which external WCS systems the editor relies upon.

## Core FRED2 Framework Dependencies

### File: `fred2/fred.h` included/used by:
- `fred2/fred.cpp` - Main application implementation
- `fred2/freddoc.cpp` - Document management system
- `fred2/fredview.cpp` - Main viewport view
- `fred2/mainfrm.cpp` - Main frame window
- `fred2/shipeditordlg.cpp` - Ship editor dialog
- `fred2/wing_editor.cpp` - Wing editor dialog
- `fred2/waypointpathdlg.cpp` - Waypoint editor
- `fred2/bgbitmapdlg.cpp` - Background bitmap dialog
- `fred2/briefingeditordlg.cpp` - Briefing editor
- All major dialog files require this for basic FRED2 types and globals

### File: `fred2/management.h` included/used by:
- `fred2/management.cpp` - Implementation file
- `fred2/ship_select.cpp` - Ship selection system
- `fred2/shipeditordlg.cpp` - Ship property editor (object management integration)
- `fred2/wing_editor.cpp` - Wing management (object creation/deletion)
- `fred2/eventeditor.cpp` - Event editor (object validation)
- `fred2/missiongoalsdlg.cpp` - Mission goals (object references)
- `fred2/fredview.cpp` - Main view (selection and manipulation)
- `fred2/waypointpathdlg.cpp` - Waypoint management
- `fred2/createwingdlg.cpp` - Wing creation dialog

### File: `fred2/sexp_tree.h` included/used by:
- `fred2/sexp_tree.cpp` - Implementation file
- `fred2/shipeditordlg.h` - Ship editor (AI goals, arrival/departure cues)
- `fred2/eventeditor.h` - Event editor (main SEXP integration)
- `fred2/missiongoalsdlg.cpp` - Mission goals (goal conditions)
- `fred2/briefingeditordlg.cpp` - Briefing editor (conditional text)
- `fred2/debriefingeditordlg.cpp` - Debriefing editor
- `fred2/campaigneditordlg.cpp` - Campaign editor (campaign progression)
- `fred2/reinforcementeditordlg.cpp` - Reinforcement editor (trigger conditions)

### File: `fred2/freddoc.h` included/used by:
- `fred2/freddoc.cpp` - Implementation file
- `fred2/fredview.h` - View requires document access
- `fred2/fred.cpp` - Main application document management
- `fred2/mainfrm.cpp` - Frame window document coordination
- `fred2/missionsave.cpp` - File I/O integration

### File: `fred2/fredview.h` included/used by:
- `fred2/fredview.cpp` - Implementation file
- `fred2/fred.cpp` - Main application view management
- `fred2/mainfrm.cpp` - Frame window view coordination
- `fred2/shipeditordlg.cpp` - Ship editor view integration
- `fred2/grid.cpp` - Grid system view integration

## Dialog System Dependencies

### File: `fred2/shipeditordlg.h` included/used by:
- `fred2/shipeditordlg.cpp` - Implementation file
- `fred2/fred.h` - Main application references ship editor
- `fred2/management.cpp` - Object management system integration
- `fred2/fredview.cpp` - View system integration

### File: `fred2/eventeditor.h` included/used by:
- `fred2/eventeditor.cpp` - Implementation file
- `fred2/fredview.cpp` - View system menu integration

### File: `fred2/wing_editor.h` included/used by:
- `fred2/wing_editor.cpp` - Implementation file
- `fred2/fred.h` - Main application wing editor access

## External WCS System Dependencies

### Mission System Dependencies
FRED2 heavily depends on core WCS mission parsing and management:

#### File: `mission/missionparse.h` included/used by:
- `fred2/fred.h` - Core mission data structures
- `fred2/freddoc.cpp` - Mission loading and validation
- `fred2/missionsave.cpp` - Mission file writing
- `fred2/management.cpp` - Object management integration
- `fred2/shipeditordlg.cpp` - Ship property access
- `fred2/eventeditor.cpp` - Event data structures
- `fred2/missiongoalsdlg.cpp` - Goal system integration
- `fred2/waypointpathdlg.cpp` - Waypoint data access
- `fred2/backgroundchooser.cpp` - Environment settings
- `fred2/asteroideditordlg.cpp` - Asteroid field configuration

#### File: `mission/missiongoals.h` included/used by:
- `fred2/eventeditor.h` - Event-goal integration
- `fred2/missiongoalsdlg.cpp` - Goal editing interface

#### File: `mission/missionmessage.h` included/used by:
- `fred2/eventeditor.h` - Message system integration
- `fred2/messageeditordlg.cpp` - Message editing interface

### SEXP System Dependencies
FRED2's SEXP editor requires extensive SEXP system integration:

#### File: `parse/sexp.h` included/used by:
- `fred2/sexp_tree.h` - SEXP tree editor core dependency
- `fred2/eventeditor.cpp` - Event SEXP validation
- `fred2/shipeditordlg.cpp` - Ship AI goal SEXP editing
- `fred2/missiongoalsdlg.cpp` - Goal condition SEXP editing
- `fred2/fredview.cpp` - SEXP validation integration

#### File: `parse/parselo.h` included/used by:
- `fred2/sexp_tree.h` - SEXP parsing utilities
- `fred2/missionsave.cpp` - Mission file parsing/writing
- `fred2/freddoc.cpp` - File parsing integration

### Ship and Object System Dependencies

#### File: `ship/ship.h` included/used by:
- `fred2/management.h` - Ship object management
- `fred2/shipeditordlg.cpp` - Ship property access and editing
- `fred2/ship_select.cpp` - Ship type selection
- `fred2/wing_editor.cpp` - Wing ship management
- `fred2/fredview.cpp` - Ship rendering and display

#### File: `object/object.h` included/used by:
- `fred2/management.cpp` - Core object management
- `fred2/fredview.cpp` - Object rendering and manipulation
- `fred2/waypointpathdlg.cpp` - Waypoint object integration

#### File: `object/waypoint.h` included/used by:
- `fred2/waypointpathdlg.cpp` - Waypoint editing interface
- `fred2/missionsave.cpp` - Waypoint data saving

### AI System Dependencies

#### File: `ai/aigoals.h` included/used by:
- `fred2/management.h` - AI goal list management
- `fred2/shipeditordlg.cpp` - Ship AI goal assignment
- `fred2/shipgoalsdlg.cpp` - Dedicated AI goal editing

#### File: `ai/ailocal.h` included/used by:
- `fred2/freddoc.h` - AI system integration
- `fred2/missionsave.h` - AI goal data saving

### Graphics and Rendering Dependencies

#### File: `graphics/2d.h` included/used by:
- `fred2/fredview.cpp` - 2D UI overlay rendering
- `fred2/fredrender.cpp` - 2D graphics integration

#### File: `render/3d.h` included/used by:
- `fred2/fredrender.cpp` - 3D model rendering
- `fred2/fredview.cpp` - 3D viewport integration

#### File: `model/model.h` included/used by:
- `fred2/fredrender.cpp` - Ship model rendering
- `fred2/shipeditordlg.cpp` - Model property access

### File System Dependencies

#### File: `cfile/cfile.h` included/used by:
- `fred2/missionsave.h` - Mission file I/O operations
- `fred2/freddoc.cpp` - File loading and saving

### Global System Dependencies

#### File: `globalincs/pstypes.h` included/used by:
- All FRED2 files - Basic type definitions
- Required for fundamental data types and constants

#### File: `globalincs/systemvars.h` included/used by:
- `fred2/fred.h` - System variable access
- `fred2/fredview.cpp` - Global state management

### Math and Utility Dependencies

#### File: `math/vecmat.h` included/used by:
- `fred2/management.cpp` - Vector and matrix operations for object positioning
- `fred2/fredview.cpp` - Camera and object transformation math
- `fred2/orienteditor.cpp` - Object orientation calculations

#### File: `io/timer.h` included/used by:
- `fred2/fredview.cpp` - Frame timing and animation
- `fred2/eventeditor.cpp` - Event timing calculations

### Campaign System Dependencies

#### File: `mission/missioncampaign.h` included/used by:
- `fred2/campaigneditordlg.cpp` - Campaign data structure access
- `fred2/campaigntreeview.cpp` - Campaign tree management

## Dialog Inter-Dependencies

### Ship Editor Dialog Dependencies
The ship editor has complex dependencies on multiple specialized dialogs:

#### Files that depend on `fred2/shipeditordlg.h`:
- `fred2/shipgoalsdlg.cpp` - AI goals sub-dialog
- `fred2/shipflagsdlg.cpp` - Ship flags configuration
- `fred2/shipspecialdamage.cpp` - Special damage configuration
- `fred2/shipspecialhitpoints.cpp` - Hitpoint distribution
- `fred2/shiptexturesdlg.cpp` - Texture replacement

### SEXP Editor Dependencies
Multiple dialogs integrate SEXP editing capabilities:

#### Files that depend on SEXP tree functionality:
- `fred2/eventeditor.cpp` - Main event SEXP editing
- `fred2/shipeditordlg.cpp` - Ship arrival/departure/goal SEXP editing
- `fred2/missiongoalsdlg.cpp` - Goal condition SEXP editing
- `fred2/campaigneditordlg.cpp` - Campaign progression SEXP editing
- `fred2/reinforcementeditordlg.cpp` - Reinforcement trigger SEXP editing

### Object Selection Dependencies
Many dialogs require object selection integration:

#### Files that depend on object selection system:
- `fred2/shipeditordlg.cpp` - Ship selection for editing
- `fred2/wing_editor.cpp` - Wing ship selection
- `fred2/eventeditor.cpp` - Object reference selection
- `fred2/missiongoalsdlg.cpp` - Target object selection
- `fred2/waypointpathdlg.cpp` - Waypoint selection

## Circular Dependencies and Resolution

### Identified Circular Dependencies

1. **View ↔ Document Dependency**:
   - `freddoc.h` needs `fredview.h` for view updates
   - `fredview.h` needs `freddoc.h` for document access
   - **Resolution**: Forward declarations and careful header organization

2. **Management ↔ Dialog Dependency**:
   - `management.cpp` needs dialog headers for update notifications
   - Dialog headers need `management.h` for object operations
   - **Resolution**: Interface abstraction and event-based communication

3. **SEXP Tree ↔ Mission Data Dependency**:
   - SEXP tree needs mission data for object validation
   - Mission data needs SEXP tree for expression storage
   - **Resolution**: Data accessor interfaces and validation callbacks

### Dependency Resolution Strategies for Godot

1. **Signal-Based Communication**: Replace circular dependencies with Godot signals
2. **Interface Abstraction**: Create abstract interfaces for complex dependencies
3. **Event Bus Pattern**: Central event coordination for dialog communication
4. **Resource References**: Use Godot's resource system for data dependencies

## Critical Integration Points for Godot Conversion

### Core Dependencies That Must Be Preserved
1. **Mission Data Access**: All dialogs need consistent mission data access
2. **Object Management**: Centralized object creation, selection, and modification
3. **SEXP Integration**: Visual SEXP editing throughout the editor
4. **Validation System**: Real-time validation across all editing operations
5. **Undo/Redo System**: Consistent undo/redo across all operations

### Dependencies That Can Be Simplified
1. **Windows MFC Dependencies**: Replace with Godot UI system
2. **File System Integration**: Use Godot's resource management
3. **Graphics System Integration**: Use Godot's rendering pipeline
4. **Direct WCS Integration**: Abstract through interface layer

### New Dependencies for Godot
1. **Godot Editor Plugin System**: Core plugin architecture
2. **Godot Resource System**: Mission data management
3. **Godot Scene System**: Object hierarchy management
4. **Godot Signal System**: Event communication
5. **Godot Inspector System**: Property editing framework

---

**Dependency Analysis Complete**: GFRED2 has extensive dependencies on virtually every WCS subsystem, requiring careful abstraction and interface design for Godot conversion. The core editing framework dependencies are manageable, but the deep integration with WCS game systems will require significant architectural adaptation.