# EPIC-004: SEXP Expression System - WCS Source Files

**Epic**: EPIC-004 - SEXP Expression System  
**Analyst**: Larry (WCS Analyst)  
**Analysis Date**: 2025-01-27  

## Core SEXP Engine Files

### Primary SEXP Implementation
- `source/code/parse/sexp.h`: Main SEXP header with 444 operator definitions, type system, node structures
- `source/code/parse/sexp.cpp`: Core SEXP evaluation engine, operator implementations, expression parsing

### Variable System
- `source/code/variables/variables.h`: Variable system interface, expression evaluator, mathematical operations
- `source/code/variables/variables.cpp`: Variable implementation, game state access, expression parsing

### Mission Integration
- `source/code/mission/missionparse.h`: Mission file structures with SEXP integration (arrival_cue, departure_cue, ai_goals)
- `source/code/mission/missionparse.cpp`: Mission loading with SEXP expression parsing
- `source/code/mission/missiongoals.h`: Mission objective system with SEXP-driven goals
- `source/code/mission/missiongoals.cpp`: Goal evaluation and tracking using SEXP expressions
- `source/code/mission/missionmessage.h`: Message system with SEXP-triggered communications
- `source/code/mission/missionmessage.cpp`: Message display and SEXP integration
- `source/code/mission/missiontraining.h`: Training mission support with SEXP-driven tutorials
- `source/code/mission/missiontraining.cpp`: Training system implementation

### Campaign Integration
- `source/code/mission/missioncampaign.h`: Campaign progression with SEXP-driven branching
- `source/code/mission/missioncampaign.cpp`: Campaign state management and SEXP evaluation

## FRED2 Editor Integration

### Visual SEXP Editor
- `source/code/fred2/sexp_tree.h`: Visual SEXP tree editor interface, drag-drop functionality
- `source/code/fred2/sexp_tree.cpp`: Tree view implementation, visual expression building

### Variable Management Dialogs
- `source/code/fred2/addvariabledlg.h`: Dialog for adding new SEXP variables
- `source/code/fred2/addvariabledlg.cpp`: Variable creation interface
- `source/code/fred2/modifyvariabledlg.h`: Dialog for editing existing variables
- `source/code/fred2/modifyvariabledlg.cpp`: Variable modification interface

### Mission Editor Integration
- `source/code/fred2/briefingeditordlg.h`: Briefing editor with SEXP integration
- `source/code/fred2/debriefingeditordlg.h`: Debriefing editor with SEXP integration
- `source/code/fred2/eventeditor.h`: Event editor using SEXP expressions
- `source/code/fred2/missiongoalsdlg.h`: Mission goals dialog with SEXP editing
- `source/code/fred2/shipeditordlg.h`: Ship editor with SEXP-based AI goals
- `source/code/fred2/wing_editor.h`: Wing editor with SEXP arrival/departure cues

### Campaign Editor
- `source/code/fred2/campaigntreewnd.cpp`: Campaign tree with SEXP-driven branching logic

## Multiplayer Support

### Network Synchronization
- `source/code/network/multi_sexp.h`: Multiplayer SEXP synchronization interface
- `source/code/network/multi_sexp.cpp`: Network-synchronized SEXP evaluation

## AI Integration

### AI Goals and Behavior
- `source/code/ai/aigoals.h`: AI goal system with SEXP-driven behaviors
- `source/code/ai/aigoals.cpp`: AI goal implementation and SEXP integration

## Additional Integration Points

### HUD Integration
- `source/code/hud/hudsquadmsg.cpp`: Squadron message system with SEXP triggers

### Game State Integration
- `source/code/freespace2/freespace.cpp`: Main game loop with SEXP evaluation

### Object System Integration
- `source/code/object/objcollide.cpp`: Collision system with SEXP event triggers
- `source/code/object/waypoint.h`: Waypoint system for SEXP spatial queries
- `source/code/object/objectsnd.cpp`: Object sound system with SEXP triggers

### Parsing Support
- `source/code/parse/parselo.h`: General parsing utilities used by SEXP system
- `source/code/parse/parselo.cpp`: Parsing implementation for SEXP text processing

### Lua Scripting Integration
- `source/code/parse/lua.h`: Lua scripting system interface
- `source/code/parse/lua.cpp`: Lua integration (some SEXP functions call Lua)
- `source/code/parse/scripting.h`: General scripting system interface
- `source/code/parse/scripting.cpp`: Scripting coordination between SEXP and Lua

## File Count and Scope

**Total Files Analyzed**: 37
- **Core SEXP Engine**: 4 files
- **Mission Integration**: 8 files  
- **FRED2 Editor Support**: 12 files
- **Network/Multiplayer**: 2 files
- **AI Integration**: 2 files
- **Additional Integration**: 9 files

**Lines of Code (Estimated)**:
- `sexp.cpp`: ~25,000 lines (massive implementation file)
- `sexp.h`: ~2,000 lines (444 operator definitions)
- `variables.cpp`: ~3,000 lines (expression evaluator)
- `sexp_tree.cpp`: ~8,000 lines (visual editor)
- **Total**: ~40,000+ lines of SEXP-related code

## Critical Dependencies

### Required Header Files
All SEXP files require these fundamental headers:
- `globalincs/pstypes.h`: Basic type definitions
- `parse/parselo.h`: Text parsing utilities
- `mission/missionparse.h`: Mission data structures

### System Integration Headers
SEXP system includes virtually every WCS subsystem:
- Ship system (`ship/ship.h`)
- Weapon system (`weapon/weapon.h`) 
- AI system (`ai/aigoals.h`)
- Graphics system (`graphics/2d.h`)
- Sound system (`gamesnd/gamesnd.h`)
- Network system (`network/multi.h`)
- HUD system (`hud/hud.h`)

## Conversion Priority

### Phase 1: Core Files (Critical)
1. `parse/sexp.h` - Operator definitions and type system
2. `parse/sexp.cpp` - Core evaluation engine
3. `variables/variables.*` - Variable system and expression evaluator
4. `mission/missionparse.*` - Mission integration

### Phase 2: Mission Integration (High)
5. `mission/missiongoals.*` - Objective system
6. `mission/missionmessage.*` - Message system
7. `mission/missioncampaign.*` - Campaign progression

### Phase 3: Editor Support (Medium)
8. `fred2/sexp_tree.*` - Visual SEXP editor
9. `fred2/*variabledlg.*` - Variable management dialogs

### Phase 4: Advanced Features (Low)
10. `network/multi_sexp.*` - Multiplayer synchronization
11. `parse/lua.*` - Lua scripting integration

---

**Analysis Result**: EPIC-004 touches 37 source files across virtually every WCS subsystem, confirming the critical importance and complexity of the SEXP expression system. The core engine files must be implemented first, followed by mission integration, then editor support.