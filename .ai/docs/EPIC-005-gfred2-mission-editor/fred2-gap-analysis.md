# FRED2 Mission Editor Gap Analysis

**Document Version**: 1.0  
**Date**: June 1, 2025  
**System**: FRED2 Mission Editor Gap Analysis  
**Scope**: Identify missing functionality, incomplete features, and architectural differences between our Godot GFRED2 implementation and the original WCS FRED2 C++ editor  

## Executive Summary

This analysis compares our current GFRED2 implementation in `/target/addons/gfred2/` against the original WCS FRED2 system in `/source/code/fred2/` to identify critical gaps in functionality that affect mission editing capability and user workflow.

**Key Findings:**
- 62 specialized dialog editors missing from our implementation
- Complex SEXP tree UI system partially implemented
- Mission file format I/O not yet implemented
- Advanced editing features like undo/redo system missing
- Campaign editor functionality completely absent
- Multi-object selection and operations limited

## 1. Missing Major Features

### 1.1 Specialized Dialog Editors (62 Missing)

**WCS FRED2 Has:** Complete dialog system with 62 specialized editors  
**Our GFRED2 Has:** 12 basic dialog implementations

**Critical Missing Dialogs:**
```
Core Editing:
- Wing Editor (wing_editor.cpp/h) - CRITICAL
- AI Goals Dialog (shipgoalsdlg.cpp/h) - CRITICAL  
- Initial Status Dialog (initialstatus.cpp/h) - CRITICAL
- Weapons Editor (weaponeditordlg.cpp/h) - CRITICAL
- Event Editor (eventeditor.cpp/h) - CRITICAL
- Background Editor (bgbitmapdlg.cpp/h) - HIGH
- Starfield Editor (starfieldeditor.cpp/h) - HIGH

Campaign System:
- Campaign Editor (campaigneditordlg.cpp/h) - CRITICAL
- Campaign Tree View (campaigntreeview.cpp/h) - CRITICAL
- Fiction Viewer (FictionViewerDlg.cpp/h) - MEDIUM

Advanced Features:
- Voice Acting Manager (voiceactingmanager.cpp/h) - MEDIUM
- Reinforcement Editor (reinforcementeditordlg.cpp/h) - MEDIUM
- Player Start Editor (playerstarteditor.cpp/h) - HIGH
- Custom Wing Names (customwingnames.cpp/h) - LOW
```

**Impact:** Users cannot perform essential mission editing tasks like wing management, AI goal configuration, and event scripting.

### 1.2 SEXP Tree System Gaps

**WCS FRED2 Has:** Complete SEXP tree implementation (sexp_tree.cpp/h - 2800+ lines)  
**Our GFRED2 Has:** Basic visual SEXP editor (visual_sexp_editor.gd - 300 lines)

**Missing SEXP Features:**
```
Core Tree Operations:
- Dynamic tree construction from SEXP data
- Drag-and-drop tree manipulation  
- Context-sensitive right-click menus
- Real-time syntax validation
- Auto-completion system
- Tree node type icons and visual feedback

Advanced SEXP Features:
- 300+ SEXP operators (get_listing_opf_* functions)
- Operator argument type checking
- Variable reference tracking
- Copy/paste/merge operations
- Find/replace in SEXP trees
- Collapse/expand tree branches
```

**Impact:** Mission scripters cannot create complex mission logic or validate SEXP expressions.

### 1.3 Mission File Format I/O

**WCS FRED2 Has:** Complete FS2 mission format I/O (missionsave.cpp/h)  
**Our GFRED2 Has:** Placeholder functions only

**Missing I/O Features:**
```
File Operations:
- FS2 mission file parsing (.fs2 format)
- Mission file generation and export
- Campaign file handling (.fc2 format)
- Backup system (9-level autosave)
- Import/export of specific mission components
- Version compatibility handling

Data Serialization:
- Object transformation data
- SEXP tree serialization
- Wing formation data
- Event timing and triggers
- Briefing and debriefing data
- Texture and model references
```

**Impact:** Cannot save/load missions or integrate with existing WCS campaign files.

## 2. UI Component Comparison

### 2.1 Architecture Differences

**WCS FRED2 Architecture:**
```
MFC Document/View Pattern:
- CFREDDoc (document management)
- CFREDView (viewport rendering)  
- CMainFrame (window management)
- Modal dialogs for all editors
- Centralized window state management
```

**Our GFRED2 Architecture:**
```
Godot Scene-Based Pattern:
- Scene composition with dock system
- Control-based UI components
- Signal-based communication
- Modular dialog system
- Resource-based data management
```

**Gap Assessment:** Architecture is fundamentally different but functionally equivalent. No critical gaps here.

### 2.2 UI Control Types

**WCS FRED2 Controls:**
```
Specialized Controls:
- sexp_tree (custom tree control) - MISSING
- numeric_edit_control (validated input) - MISSING  
- CShipEditorDlg (complex multi-page dialog) - PARTIAL
- ship_goals_dlg (AI configuration) - MISSING
- management.cpp (object selection system) - PARTIAL
```

**Our GFRED2 Controls:**
```
Implemented Controls:
- Property inspector system - COMPLETE
- Base dialog framework - COMPLETE
- Object hierarchy view - COMPLETE
- 3D viewport integration - COMPLETE
- Dock management system - COMPLETE
```

**Impact:** Missing specialized controls prevent advanced editing operations.

## 3. Data Structure Gaps

### 3.1 Mission Data Representation

**WCS FRED2 Mission Structure:**
```cpp
// From missionparse.h
typedef struct mission {
    char name[NAME_LENGTH];
    char author[NAME_LENGTH]; 
    float version;
    char created[DATE_TIME_LENGTH];
    char modified[DATE_TIME_LENGTH];
    char notes[NOTES_LENGTH];
    char mission_desc[MISSION_DESC_LENGTH];
    int game_type;
    int flags;                        // 22+ mission flags
    int num_players;
    uint num_respawns;
    support_ship_info support_ships;
    char squad_filename[MAX_FILENAME_LEN];
    char squad_name[NAME_LENGTH];
    char loading_screen[GR_NUM_RESOLUTIONS][MAX_FILENAME_LEN];
    char skybox_model[MAX_FILENAME_LEN];
    // ... many more fields
};
```

**Our GFRED2 Mission Structure:**
```gdscript
# From mission_data.gd
class_name MissionData
@export var title := "Untitled"
@export var designer := "Unknown"  
@export var description := ""
@export var mission_type: MissionType
@export var all_teams_at_war := false
# ... simplified structure (~15 fields vs 50+ in WCS)
```

**Gaps Identified:**
```
Missing Fields:
- Mission version tracking
- Creation/modification timestamps  
- Designer notes vs mission description
- Complex support ship configuration
- Skybox and environment settings
- AI profile assignments
- Cutscene definitions
- Music assignments
- Nebula configuration
- Loading screen assignments
```

**Impact:** Cannot handle full WCS mission complexity or generate compatible mission files.

### 3.2 Object Management System

**WCS FRED2 Object System:**
```cpp
// From management.h
extern int cur_object_index;
extern int cur_ship;
extern int cur_wing;
extern int cur_wing_index;
extern int wing_objects[MAX_WINGS][MAX_SHIPS_PER_WING];
extern char Fred_alt_names[MAX_SHIPS][NAME_LENGTH+1];
extern char Fred_callsigns[MAX_SHIPS][NAME_LENGTH+1];
```

**Our GFRED2 Object System:**
```gdscript
# From mission_data.gd
var objects := {}  # Dictionary by ID
var root_objects := []  # Top-level objects
```

**Gap Assessment:** Our system is more modern (dictionary-based vs array-based) but lacks WCS-specific management features like alternate names and callsigns.

## 4. Integration Point Analysis

### 4.1 WCS Asset Core Integration

**Status:** IMPLEMENTED ✓  
**Assessment:** Our asset registry and preview systems properly integrate with WCS Asset Core addon.

### 4.2 SEXP System Integration

**Status:** PARTIAL ⚠️  
**Missing Components:**
- Complex SEXP operator validation
- Variable reference tracking across mission
- SEXP tree performance optimization
- Integration with ship/wing/waypoint systems

### 4.3 Viewport Integration

**Status:** IMPLEMENTED ✓  
**Assessment:** 3D viewport, camera controls, and object manipulation working correctly.

## 5. Performance Gaps

### 5.1 SEXP Tree Performance

**WCS FRED2:** Uses native C++ with optimized tree operations  
**Our GFRED2:** GDScript implementation may be slower for large SEXP trees  

**Potential Issues:**
- Large mission files with 1000+ SEXP nodes
- Real-time SEXP validation during editing
- Complex dependency graph updates

**Mitigation:** Consider C# implementation for performance-critical SEXP operations.

### 5.2 Object Selection Performance

**WCS FRED2:** Direct memory access to object arrays  
**Our GFRED2:** Dictionary-based lookups with signals

**Assessment:** Unlikely to be a bottleneck for typical mission sizes.

## 6. User Workflow Gaps

### 6.1 Mission Creation Workflow

**WCS FRED2 Workflow:**
```
1. File → New Mission
2. Mission Specs Dialog (automatic)
3. Grid setup and camera positioning
4. Object placement via Create menu
5. Property editing via specialized dialogs
6. Event/Goal setup via Event Editor
7. SEXP tree construction
8. Save as .fs2 file
```

**Our GFRED2 Workflow:**
```
1. Editor launch (plugin)
2. New mission creation - MISSING
3. Object placement via 3D viewport
4. Property editing via inspector
5. Limited dialog editing
6. No SEXP tree construction
7. No file I/O
```

**Critical Workflow Gaps:**
- No mission creation wizard
- No structured object creation workflow  
- No event/goal creation workflow
- No mission testing/validation

### 6.2 Advanced Editing Features

**Missing from Our Implementation:**
```
Selection and Manipulation:
- Multi-object selection operations
- Object grouping and ungrouping
- Copy/paste operations across missions
- Find/replace for object properties
- Bulk property editing

Validation and Testing:
- Real-time mission validation
- SEXP syntax checking
- Reference integrity checking
- Mission playability testing
- Performance warnings

Workflow Enhancements:
- Undo/redo system (CRITICAL)
- Autosave functionality
- Session state persistence
- Customizable toolbars/shortcuts
- Context-sensitive help system
```

## 7. Priority Recommendations

### 7.1 Critical Priority (Blocks Basic Functionality)

1. **Mission File I/O System**
   - Implement FS2 mission file parser
   - Add mission export functionality
   - File format version handling

2. **Core Dialog Editors**
   - Wing Editor implementation
   - Event Editor with SEXP integration
   - Ship Goals/AI configuration dialog

3. **SEXP Tree UI System**
   - Complete tree control implementation
   - Operator palette and validation
   - Drag-and-drop functionality

4. **Undo/Redo System**
   - Command pattern implementation
   - Integrated with all editing operations

### 7.2 High Priority (Major User Experience Issues)

1. **Mission Creation Workflow**
   - New mission wizard
   - Mission specs dialog
   - Template system

2. **Object Management Enhancements**
   - Multi-selection operations
   - Copy/paste functionality
   - Bulk property editing

3. **Additional Dialog Editors**
   - Weapons configuration
   - Background/starfield editor
   - Initial status dialog

### 7.3 Medium Priority (Feature Completeness)

1. **Campaign Editor System**
   - Campaign file handling
   - Campaign tree visualization
   - Fiction viewer integration

2. **Advanced Validation**
   - Real-time error checking
   - Reference integrity validation
   - Performance analysis

3. **Workflow Enhancements**
   - Autosave system
   - Session persistence
   - Customizable interface

## 8. Implementation Strategy

### 8.1 Phase 1: Core Functionality (4-6 weeks)
- Mission file I/O implementation
- Basic SEXP tree system
- Wing editor dialog
- Undo/redo framework

### 8.2 Phase 2: Essential Dialogs (3-4 weeks)
- Event editor with SEXP integration
- Ship goals/AI configuration
- Mission specs editor enhancement
- Object selection improvements

### 8.3 Phase 3: Advanced Features (4-5 weeks)
- Campaign editor system
- Advanced validation framework
- Performance optimization
- Workflow enhancements

## 9. Technical Notes

### 9.1 File Format Compatibility
- Must maintain 100% compatibility with WCS .fs2 mission format
- Version handling for different FRED2 versions
- Backup compatibility with legacy missions

### 9.2 Integration Requirements
- Seamless integration with existing WCS Asset Core
- SEXP addon compatibility
- Performance profiling integration

### 9.3 User Experience Considerations
- Familiar workflow for existing FRED2 users
- Modern UI patterns where appropriate
- Contextual help and validation feedback

## Conclusion

The current GFRED2 implementation provides a solid foundation with modern architecture and good integration with Godot systems. However, significant gaps exist in core mission editing functionality, particularly:

1. **Mission file I/O** - Complete absence blocks any real usage
2. **SEXP tree system** - Critical for mission scripting
3. **Specialized dialogs** - Essential for advanced editing
4. **Workflow features** - Needed for productive editing

Addressing the Critical and High priority gaps would bring GFRED2 to basic parity with the original FRED2, enabling real mission creation and editing workflows.