# EPIC-005: GFRED2 Mission Editor - WCS Source Files

**Epic**: EPIC-005 - GFRED2 Mission Editor  
**Analyst**: Larry (WCS Analyst)  
**Analysis Date**: 2025-01-27  

## Core Application Framework Files

### Main Application Structure
- `source/code/fred2/fred.h`: Main application class definition, window management, UI types
- `source/code/fred2/fred.cpp`: Application initialization, message handling, main event loop
- `source/code/fred2/freddoc.h`: Document class for mission file management, undo system
- `source/code/fred2/freddoc.cpp`: Document implementation, file I/O coordination, backup system
- `source/code/fred2/fredview.h`: Main 3D viewport view class, camera controls, rendering options
- `source/code/fred2/fredview.cpp`: Viewport implementation, mouse/keyboard handling, display logic
- `source/code/fred2/mainfrm.h`: Main frame window, toolbar, menu management
- `source/code/fred2/mainfrm.cpp`: Frame window implementation, UI layout, window coordination

### Core Editor Infrastructure
- `source/code/fred2/editor.h`: Core editor definitions, shared constants
- `source/code/fred2/fredstubs.cpp`: Stub functions for game integration
- `source/code/fred2/fredrender.h`: Rendering system interface for 3D viewport
- `source/code/fred2/fredrender.cpp`: 3D rendering implementation, model display, visual effects
- `source/code/fred2/stdafx.h`: Standard includes and precompiled header definitions
- `source/code/fred2/stdafx.cpp`: Precompiled header implementation

## Object Management System Files

### Core Object Management
- `source/code/fred2/management.h`: Object management interface, selection system, creation/deletion
- `source/code/fred2/management.cpp`: Object management implementation, reference handling, validation

### Ship and Wing Management
- `source/code/fred2/ship_select.h`: Ship selection dialog and utilities
- `source/code/fred2/ship_select.cpp`: Ship browser, filtering, selection interface
- `source/code/fred2/wing.h`: Wing data structures and operations
- `source/code/fred2/wing.cpp`: Wing management implementation
- `source/code/fred2/wing_editor.h`: Wing editor dialog interface
- `source/code/fred2/wing_editor.cpp`: Wing formation editing, property management
- `source/code/fred2/createwingdlg.h`: Wing creation dialog interface
- `source/code/fred2/createwingdlg.cpp`: New wing creation wizard
- `source/code/fred2/customwingnames.h`: Custom wing naming system
- `source/code/fred2/customwingnames.cpp`: Wing name management and validation

### Waypoint and Navigation
- `source/code/fred2/waypointpathdlg.h`: Waypoint path editor dialog
- `source/code/fred2/waypointpathdlg.cpp`: Waypoint creation, path editing, navigation setup

## SEXP and Scripting System Files

### Visual SEXP Editor
- `source/code/fred2/sexp_tree.h`: SEXP tree control definition, node types, editing operations
- `source/code/fred2/sexp_tree.cpp`: SEXP tree implementation, visual editing, validation (8,000+ lines)

### Variable Management
- `source/code/fred2/addvariabledlg.h`: Add variable dialog interface
- `source/code/fred2/addvariabledlg.cpp`: Variable creation dialog implementation
- `source/code/fred2/modifyvariabledlg.h`: Modify variable dialog interface  
- `source/code/fred2/modifyvariabledlg.cpp`: Variable editing dialog implementation

### SEXP Operator Support
- `source/code/fred2/operatorargtypeselect.h`: Operator argument type selection dialog
- `source/code/fred2/operatorargtypeselect.cpp`: SEXP operator parameter configuration

## Ship and Object Editor Dialogs

### Main Ship Editor
- `source/code/fred2/shipeditordlg.h`: Primary ship editor dialog with comprehensive ship properties
- `source/code/fred2/shipeditordlg.cpp`: Ship editor implementation, property management (3,000+ lines)

### Ship Configuration Dialogs
- `source/code/fred2/shipclasseditordlg.h`: Ship class configuration dialog
- `source/code/fred2/shipclasseditordlg.cpp`: Ship class property editing
- `source/code/fred2/shipflagsdlg.h`: Ship behavior flags editor
- `source/code/fred2/shipflagsdlg.cpp`: Ship flags configuration interface
- `source/code/fred2/shipgoalsdlg.h`: Ship AI goals editor dialog
- `source/code/fred2/shipgoalsdlg.cpp`: AI goal assignment and configuration
- `source/code/fred2/shipspecialdamage.h`: Ship special damage configuration
- `source/code/fred2/shipspecialdamage.cpp`: Special damage system setup
- `source/code/fred2/shipspecialhitpoints.h`: Ship special hitpoints editor
- `source/code/fred2/shipspecialhitpoints.cpp`: Hitpoint distribution configuration
- `source/code/fred2/shiptexturesdlg.h`: Ship texture replacement dialog
- `source/code/fred2/shiptexturesdlg.cpp`: Texture customization interface

### Weapon and Loadout Editors
- `source/code/fred2/weaponeditordlg.h`: Weapon configuration dialog
- `source/code/fred2/weaponeditordlg.cpp`: Weapon loadout and property editing

### Alternative Ship Systems
- `source/code/fred2/AltShipClassDlg.h`: Alternative ship class dialog
- `source/code/fred2/AltShipClassDlg.cpp`: Alternative ship configuration system

## Mission Structure Editor Dialogs

### Event and Trigger Management
- `source/code/fred2/eventeditor.h`: Mission event editor dialog with SEXP integration
- `source/code/fred2/eventeditor.cpp`: Event creation, trigger management (2,500+ lines)

### Mission Goals and Objectives
- `source/code/fred2/missiongoalsdlg.h`: Mission goals editor dialog
- `source/code/fred2/missiongoalsdlg.cpp`: Objective definition and validation

### Message System
- `source/code/fred2/messageeditordlg.h`: In-game message editor dialog
- `source/code/fred2/messageeditordlg.cpp`: Message creation, persona assignment

### Briefing and Debriefing
- `source/code/fred2/briefingeditordlg.h`: Mission briefing editor dialog
- `source/code/fred2/briefingeditordlg.cpp`: Briefing creation with visual elements
- `source/code/fred2/debriefingeditordlg.h`: Mission debriefing editor dialog
- `source/code/fred2/debriefingeditordlg.cpp`: Debriefing message configuration
- `source/code/fred2/cmdbrief.h`: Command briefing editor interface
- `source/code/fred2/cmdbrief.cpp`: Command briefing creation and editing

### Player Configuration
- `source/code/fred2/playerstarteditor.h`: Player start position editor
- `source/code/fred2/playerstarteditor.cpp`: Player spawn configuration
- `source/code/fred2/initialships.h`: Initial ship loadout editor
- `source/code/fred2/initialships.cpp`: Player ship configuration
- `source/code/fred2/initialstatus.h`: Initial mission status editor
- `source/code/fred2/initialstatus.cpp`: Mission starting conditions

## Environment and Background Editors

### Background and Visual Setup
- `source/code/fred2/backgroundchooser.h`: Background image selection dialog
- `source/code/fred2/backgroundchooser.cpp`: Background configuration interface
- `source/code/fred2/bgbitmapdlg.h`: Background bitmap editor dialog
- `source/code/fred2/bgbitmapdlg.cpp`: Background image management
- `source/code/fred2/starfieldeditor.h`: Starfield configuration dialog
- `source/code/fred2/starfieldeditor.cpp`: Starfield and space environment setup

### Environmental Elements
- `source/code/fred2/asteroideditordlg.h`: Asteroid field editor dialog
- `source/code/fred2/asteroideditordlg.cpp`: Asteroid field configuration
- `source/code/fred2/reinforcementeditordlg.h`: Reinforcement waves editor
- `source/code/fred2/reinforcementeditordlg.cpp`: Reinforcement configuration and timing

## Campaign Management Files

### Campaign Structure
- `source/code/fred2/campaigneditordlg.h`: Campaign editor main dialog
- `source/code/fred2/campaigneditordlg.cpp`: Campaign structure management
- `source/code/fred2/campaigntreeview.h`: Campaign tree view control
- `source/code/fred2/campaigntreeview.cpp`: Campaign tree visualization
- `source/code/fred2/campaigntreewnd.h`: Campaign tree window management
- `source/code/fred2/campaigntreewnd.cpp`: Campaign tree UI coordination

### Campaign Support
- `source/code/fred2/campaignfilelistbox.h`: Campaign file list control
- `source/code/fred2/campaignfilelistbox.cpp`: Campaign file management interface

## Utility and Support Dialogs

### Grid and Alignment
- `source/code/fred2/grid.h`: 3D grid system interface
- `source/code/fred2/grid.cpp`: Grid display, snapping, measurement tools
- `source/code/fred2/adjustgriddlg.h`: Grid adjustment dialog
- `source/code/fred2/adjustgriddlg.cpp`: Grid configuration interface

### Object Orientation and Positioning
- `source/code/fred2/orienteditor.h`: Object orientation editor dialog
- `source/code/fred2/orienteditor.cpp`: Object rotation and alignment tools

### Special System Editors
- `source/code/fred2/shieldsysdlg.h`: Shield system editor dialog
- `source/code/fred2/shieldsysdlg.cpp`: Shield configuration interface
- `source/code/fred2/restrictpaths.h`: Restricted navigation paths editor
- `source/code/fred2/restrictpaths.cpp`: Navigation restriction configuration
- `source/code/fred2/ignoreordersdlg.h`: Ignore orders configuration dialog
- `source/code/fred2/ignoreordersdlg.cpp`: Ship order ignoring setup

### Global Configuration
- `source/code/fred2/setglobalshipflags.h`: Global ship flags editor
- `source/code/fred2/setglobalshipflags.cpp`: Mission-wide ship flag configuration

## File I/O and Data Management

### Mission Save/Load System
- `source/code/fred2/missionsave.h`: Mission file save system interface
- `source/code/fred2/missionsave.cpp`: Mission file writing, format management

## Voice Acting and Media Support

### Voice Acting Management
- `source/code/fred2/voiceactingmanager.h`: Voice acting management dialog
- `source/code/fred2/voiceactingmanager.cpp`: Voice file organization and scripting

### Fiction and Story Elements
- `source/code/fred2/FictionViewerDlg.h`: Fiction viewer dialog for story content
- `source/code/fred2/FictionViewerDlg.cpp`: Fiction display and editing interface

## User Interface Support Files

### List and Selection Controls
- `source/code/fred2/shipchecklistbox.h`: Ship checkbox list control
- `source/code/fred2/shipchecklistbox.cpp`: Multi-selection ship interface

### Dialog Support
- `source/code/fred2/textviewdlg.h`: Text viewing dialog for help and info
- `source/code/fred2/textviewdlg.cpp`: Text display interface
- `source/code/fred2/prefsdlg.h`: Editor preferences dialog
- `source/code/fred2/prefsdlg.cpp`: User preference configuration
- `source/code/fred2/folderdlg.h`: Folder selection dialog
- `source/code/fred2/folderdlg.cpp`: Directory browsing interface

### Miscellaneous Dialogs
- `source/code/fred2/dialog1.h`: Generic dialog interface
- `source/code/fred2/dialog1.cpp`: Multi-purpose dialog implementation
- `source/code/fred2/missionnotesdlg.h`: Mission notes editor dialog
- `source/code/fred2/missionnotesdlg.cpp`: Mission documentation interface

## Development and Debug Support

### Statistics and Analysis
- `source/code/fred2/dumpstats.h`: Mission statistics dumping interface
- `source/code/fred2/dumpstats.cpp`: Mission analysis and statistics generation

## Resource Files

### Visual Resources
- `source/code/fred2/res/`: Directory containing bitmaps, icons, cursors for UI elements
  - `wcsaga_fred.ico`: Main FRED2 application icon
  - `toolbar.bmp`, `toolbar1.bmp`: Toolbar button images
  - `data*.bmp`: Progress/percentage indicator bitmaps (20 files)
  - `variable.bmp`, `root.bmp`, `chained.bmp`: SEXP tree node icons
  - Various cursor files for different editing modes

### Build and Configuration
- `source/code/fred2/fred.rc`: Windows resource file defining dialogs, menus, strings
- `source/code/fred2/resource.h`: Resource ID definitions
- `source/code/fred2/resource.hm`: Help mapping for context-sensitive help
- `source/code/fred2/fred.aps`: Visual Studio resource file
- `source/code/fred2/makehelp.bat`: Help file generation script

### Help System
- `source/code/fred2/hlp/`: Help file directory with documentation resources

## File Count and Scope Summary

**Total Files Analyzed**: 125
- **Core Application**: 8 files (main app, document, view, frame)
- **Object Management**: 12 files (ships, wings, waypoints, selection)
- **SEXP System**: 6 files (tree editor, variables, operators)
- **Ship Editors**: 16 files (main editor plus specialized dialogs)
- **Mission Structure**: 12 files (events, goals, messages, briefings)
- **Environment**: 6 files (backgrounds, starfield, asteroids)
- **Campaign**: 6 files (campaign editor, tree management)
- **Utilities**: 15 files (grid, alignment, configuration)
- **I/O System**: 2 files (mission save/load)
- **Media Support**: 4 files (voice acting, fiction viewer)
- **UI Support**: 10 files (lists, dialogs, preferences)
- **Resources**: 28 files (bitmaps, dialogs, help files)

**Lines of Code (Estimated)**:
- `sexp_tree.cpp`: ~8,000 lines (visual SEXP editor)
- `shipeditordlg.cpp`: ~3,000 lines (ship property editor)
- `eventeditor.cpp`: ~2,500 lines (mission event editor)
- `management.cpp`: ~2,000 lines (object management)
- `fredview.cpp`: ~2,000 lines (3D viewport)
- **Total**: ~40,000+ lines of FRED2-specific code

## Conversion Priority Classification

### Phase 1: Core Infrastructure (Critical)
1. **Core Application Framework**: `fred.*`, `freddoc.*`, `fredview.*`, `mainfrm.*`
2. **Object Management**: `management.*`, `ship_select.*`
3. **Basic SEXP Integration**: `sexp_tree.*` (simplified)
4. **Mission I/O**: `missionsave.*`

### Phase 2: Essential Editing (High Priority)
5. **Ship Editor**: `shipeditordlg.*`, `wing_editor.*`
6. **Event Editor**: `eventeditor.*`, `missiongoalsdlg.*`
7. **Environment Setup**: `backgroundchooser.*`, `starfieldeditor.*`
8. **Grid and Viewport**: `grid.*`, `fredrender.*`

### Phase 3: Advanced Features (Medium Priority)
9. **Full SEXP Editor**: Complete `sexp_tree.*` functionality
10. **Campaign System**: `campaigneditordlg.*`, `campaigntreeview.*`
11. **Specialized Editors**: Weapon, texture, special damage dialogs
12. **Validation System**: Error checking and mission validation

### Phase 4: Polish and Enhancement (Low Priority)
13. **Voice Acting**: `voiceactingmanager.*`
14. **Advanced Configuration**: Various specialized dialogs
15. **Statistics and Analysis**: `dumpstats.*`
16. **Help Integration**: Help system and context-sensitive assistance

---

**Analysis Result**: EPIC-005 encompasses 125 source files implementing a comprehensive 3D mission editor with sophisticated object management, visual scripting, and extensive property editing capabilities. The core application framework and object management systems represent the critical path for Godot conversion.