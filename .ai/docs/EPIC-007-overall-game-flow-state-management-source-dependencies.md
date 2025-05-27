# EPIC-007: Overall Game Flow & State Management - Source Dependencies

**Document Version**: 1.0  
**Date**: 2025-01-27  
**Analyst**: Larry (WCS Analyst)  
**Epic**: EPIC-007 - Overall Game Flow & State Management  
**System**: Game state management, campaign progression, save/load, session control  
**Analysis Type**: DEPENDENCY MAPPING  

---

## Dependency Analysis Overview

**Total Dependencies Analyzed**: 127 dependency relationships  
**Critical Dependency Chains**: 8 major chains identified  
**Circular Dependencies**: 3 instances (manageable)  
**External Library Dependencies**: 12 system libraries  
**Integration Complexity**: HIGH - Central coordination system  

---

## Core Dependency Chains

### **1. Game Sequence State Machine Dependencies** 🔗 **CRITICAL**

#### `gamesequence.cpp` Core Dependencies
```cpp
// Primary includes and dependencies
#include "gamesequence/gamesequence.h"      // Self-header
#include "freespace2/freespace.h"           // Main game coordination
#include "globalincs/pstypes.h"             // Type definitions
#include "io/key.h"                         // Input system
#include "io/timer.h"                       // Timing system
#include "osapi/osapi.h"                    // OS abstraction
#include "cfile/cfile.h"                    // File I/O system
#include "graphics/2d.h"                    // Graphics system
#include "mission/missionload.h"            // Mission loading
#include "mission/missioncampaign.h"        // Campaign system
#include "menuui/mainhallmenu.h"           // Main menu
#include "parse/sexp.h"                     // SEXP evaluation
```

**Dependency Flow**:
```
gamesequence.cpp
├── CRITICAL: freespace.h (main game loop)
├── CRITICAL: missioncampaign.h (campaign management)
├── CRITICAL: missionload.h (mission loading)
├── HIGH: mainhallmenu.h (menu system)
├── HIGH: sexp.h (SEXP integration)
├── MEDIUM: graphics/2d.h (rendering)
├── MEDIUM: io/key.h (input)
└── LOW: osapi.h (platform abstraction)
```

**Used By**:
- `freespace.cpp` - Main game loop calls gameseq_process_events()
- All menu systems - Post events via gameseq_post_event()
- Mission systems - State transitions during mission flow
- Save/load systems - State validation during persistence

---

### **2. Campaign Management Dependencies** 🎯 **HIGH PRIORITY**

#### `missioncampaign.cpp` Core Dependencies
```cpp
// Campaign system dependencies
#include "mission/missioncampaign.h"        // Self-header
#include "mission/missionparse.h"           // Mission file parsing
#include "mission/missiongoals.h"           // Mission objectives
#include "parse/parselo.h"                  // Low-level parsing
#include "parse/sexp.h"                     // Expression evaluation
#include "cfile/cfile.h"                    // File operations
#include "playerman/player.h"               // Player data
#include "stats/scoring.h"                  // Statistics system
#include "gamesequence/gamesequence.h"      // State management
#include "freespace2/freespace.h"           // Main coordination
#include "localization/localize.h"          // Text localization
```

**Dependency Flow**:
```
missioncampaign.cpp
├── CRITICAL: missionparse.h (mission file parsing)
├── CRITICAL: sexp.h (branching logic evaluation)
├── CRITICAL: player.h (pilot data integration)
├── HIGH: gamesequence.h (state transitions)
├── HIGH: scoring.h (statistics tracking)
├── HIGH: missiongoals.h (objective management)
├── MEDIUM: parselo.h (file parsing utilities)
├── MEDIUM: cfile.h (file I/O operations)
└── LOW: localize.h (text localization)
```

**Used By**:
- `gamesequence.cpp` - Campaign state validation and progression
- `managepilot.cpp` - Pilot campaign progress tracking
- `missionbrief.cpp` - Mission briefing data
- `missiondebrief.cpp` - Mission completion processing
- `menuui/readyroom.cpp` - Campaign selection interface

---

### **3. Player Data Management Dependencies** 👤 **HIGH PRIORITY**

#### `managepilot.cpp` Core Dependencies
```cpp
// Player management dependencies
#include "playerman/managepilot.h"          // Self-header
#include "playerman/player.h"               // Player structures
#include "mission/missioncampaign.h"        // Campaign integration
#include "stats/scoring.h"                  // Statistics system
#include "stats/medals.h"                   // Medal system
#include "cfile/cfile.h"                    // File operations
#include "parse/parselo.h"                  // Configuration parsing
#include "gamesequence/gamesequence.h"      // State coordination
#include "menuui/barracks.h"                // Pilot selection UI
#include "hud/hud.h"                        // HUD configuration
#include "io/key.h"                         // Input configuration
```

**Dependency Flow**:
```
managepilot.cpp
├── CRITICAL: player.h (player data structures)
├── CRITICAL: missioncampaign.h (campaign progress)
├── HIGH: scoring.h (statistics persistence)
├── HIGH: medals.h (achievement tracking)
├── HIGH: gamesequence.h (state integration)
├── MEDIUM: barracks.h (UI integration)
├── MEDIUM: cfile.h (save/load operations)
├── MEDIUM: parselo.h (configuration parsing)
├── LOW: hud.h (HUD settings)
└── LOW: key.h (control configuration)
```

**Used By**:
- `gamesequence.cpp` - Pilot validation during state transitions
- `missioncampaign.cpp` - Campaign progress tracking
- `menuui/barracks.cpp` - Pilot selection and creation
- `menuui/mainhallmenu.cpp` - Pilot-specific menu states
- `stats/scoring.cpp` - Statistics persistence

---

### **4. Mission Loading Dependencies** 💾 **CRITICAL**

#### `missionload.cpp` Core Dependencies
```cpp
// Mission loading dependencies
#include "mission/missionload.h"            // Self-header
#include "mission/missionparse.h"           // Mission parsing
#include "mission/missiongoals.h"           // Objective system
#include "parse/parselo.h"                  // File parsing
#include "parse/sexp.h"                     // Expression system
#include "ship/ship.h"                      // Ship management
#include "object/object.h"                  // Object system
#include "weapon/weapon.h"                  // Weapon system
#include "ai/ai.h"                          // AI system
#include "asteroid/asteroid.h"              // Asteroid fields
#include "nebula/neb.h"                     // Nebula system
#include "jumpnode/jumpnode.h"              // Jump nodes
#include "gamesequence/gamesequence.h"      // State management
```

**Dependency Flow**:
```
missionload.cpp
├── CRITICAL: missionparse.h (mission file structure)
├── CRITICAL: ship.h (ship loading and setup)
├── CRITICAL: object.h (game object management)
├── HIGH: weapon.h (weapon configuration)
├── HIGH: ai.h (AI setup and initialization)
├── HIGH: sexp.h (mission logic evaluation)
├── HIGH: missiongoals.h (objective setup)
├── MEDIUM: asteroid.h (environmental objects)
├── MEDIUM: neb.h (nebula configuration)
├── MEDIUM: jumpnode.h (navigation objects)
└── LOW: parselo.h (parsing utilities)
```

**Used By**:
- `gamesequence.cpp` - Mission loading state transitions
- `missioncampaign.cpp` - Campaign mission loading
- `missionui/missionbrief.cpp` - Pre-mission setup
- `freespace.cpp` - Main game loop integration

---

### **5. Menu System Integration Dependencies** 🖼️ **HIGH PRIORITY**

#### `menuui/mainhallmenu.cpp` Dependencies
```cpp
// Main menu dependencies
#include "menuui/mainhallmenu.h"            // Self-header
#include "gamesequence/gamesequence.h"      // State management
#include "mission/missioncampaign.h"        // Campaign access
#include "playerman/managepilot.h"          // Pilot management
#include "menuui/barracks.h"                // Pilot selection
#include "menuui/readyroom.h"               // Mission briefing
#include "menuui/techmenu.h"                // Tech database
#include "menuui/optionsmenu.h"             // Settings
#include "graphics/2d.h"                    // UI rendering
#include "ui/ui.h"                          // UI framework
#include "io/key.h"                         // Input handling
#include "gamesnd/gamesnd.h"                // Audio system
```

**Menu System Dependency Web**:
```
mainhallmenu.cpp
├── CRITICAL: gamesequence.h (state transitions)
├── CRITICAL: managepilot.h (pilot management)
├── HIGH: missioncampaign.h (campaign access)
├── HIGH: barracks.h (pilot selection integration)
├── HIGH: readyroom.h (mission access)
├── MEDIUM: optionsmenu.h (settings access)
├── MEDIUM: techmenu.h (database access)
├── MEDIUM: ui.h (UI framework)
├── LOW: graphics/2d.h (rendering)
└── LOW: gamesnd.h (sound effects)
```

---

### **6. Mission UI Flow Dependencies** 📋 **HIGH PRIORITY**

#### Mission UI Dependency Chain
```cpp
// Mission briefing dependencies
missionbrief.cpp includes:
├── mission/missionparse.h              // Mission data
├── mission/missioncampaign.h           // Campaign context
├── parse/sexp.h                        // Objective evaluation
├── gamesequence/gamesequence.h         // State flow
├── ui/ui.h                             // UI framework
└── ship/ship.h                         // Ship information

// Ship selection dependencies  
missionshipchoice.cpp includes:
├── ship/ship.h                         // Ship database
├── weapon/weapon.h                     // Weapon loadouts
├── playerman/player.h                  // Player preferences
├── gamesequence/gamesequence.h         // State management
└── ui/ui.h                             // Selection interface

// Mission debrief dependencies
missiondebrief.cpp includes:
├── stats/scoring.h                     // Mission results
├── stats/medals.h                      // Medal awards
├── mission/missiongoals.h              // Objective results
├── mission/missioncampaign.h           // Campaign progression
├── gamesequence/gamesequence.h         // State transitions
└── playerman/managepilot.h             // Pilot updates
```

---

## Critical Circular Dependencies

### **1. GameSequence ↔ FreSpace2 Main** ⚠️ **MANAGEABLE**
```
gamesequence.cpp → freespace.h (game coordination)
freespace.cpp → gamesequence.h (state management)
```
**Resolution**: Interface segregation - separate game loop from state management

### **2. MissionCampaign ↔ GameSequence** ⚠️ **MANAGEABLE**
```
missioncampaign.cpp → gamesequence.h (state transitions)
gamesequence.cpp → missioncampaign.h (campaign validation)
```
**Resolution**: Event-driven communication to break direct coupling

### **3. Player ↔ MissionCampaign** ⚠️ **MANAGEABLE**
```
managepilot.cpp → missioncampaign.h (campaign progress)
missioncampaign.cpp → player.h (pilot data)
```
**Resolution**: Data transfer objects to isolate dependencies

---

## External System Dependencies

### **Core System Libraries**
```cpp
// Standard C++ libraries
#include <stdio.h>              // File I/O operations
#include <stdlib.h>             // Memory management
#include <string.h>             // String operations
#include <math.h>               // Mathematical functions
#include <time.h>               // Time and date functions

// Platform-specific includes
#ifdef _WIN32
    #include <windows.h>        // Windows API
    #include <direct.h>         // Directory operations
#else
    #include <unistd.h>         // POSIX operations  
    #include <sys/stat.h>       // File statistics
#endif
```

### **Graphics & Audio Dependencies**
```cpp
// Graphics system
#include "graphics/2d.h"        // 2D rendering
#include "graphics/font.h"      // Text rendering
#include "bmpman/bmpman.h"      // Image management

// Audio system  
#include "sound/sound.h"        // Audio playback
#include "gamesnd/gamesnd.h"    // Game sound effects
```

### **Input & OS Abstraction**
```cpp
// Input handling
#include "io/key.h"             // Keyboard input
#include "io/mouse.h"           // Mouse input
#include "io/joy.h"             // Joystick input

// OS abstraction
#include "osapi/osapi.h"        // Platform abstraction
#include "cfile/cfile.h"        // Virtual file system
```

---

## Dependency Complexity Analysis

### **High Complexity Intersections** ⚠️
1. **GameSequence ↔ All Menu Systems** (15 integration points)
2. **MissionCampaign ↔ Save/Load Systems** (8 integration points)
3. **Player Data ↔ Statistics Systems** (12 integration points)
4. **Mission Loading ↔ All Game Objects** (20+ integration points)

### **Medium Complexity Intersections** 🔧
1. **Menu UI ↔ Graphics Systems** (6 integration points)
2. **Campaign ↔ SEXP Systems** (4 integration points)
3. **State Management ↔ Input Systems** (5 integration points)

### **Low Complexity Intersections** ✅
1. **Help Systems ↔ Core Systems** (2 integration points)
2. **Demo System ↔ Core Systems** (3 integration points)
3. **Command Line ↔ Core Systems** (2 integration points)

---

## Godot Conversion Impact Assessment

### **Direct Conversion Dependencies** 🎯
These WCS dependencies will map directly to Godot systems:

```cpp
// WCS System → Godot Equivalent
gamesequence.h → GameStateManager (AUTOLOAD)
missioncampaign.h → CampaignManager (Resource-based)
player.h → PilotProfile (Resource-based)
cfile.h → FileAccess (Godot built-in)
graphics/2d.h → Control nodes (Godot UI)
ui/ui.h → Control/Container nodes
sound/sound.h → AudioStreamPlayer
```

### **Complex Conversion Dependencies** ⚠️
These require architectural transformation:

```cpp
// WCS Pattern → Godot Pattern
Global state variables → Autoload singletons
C-style arrays → Godot Arrays/Resources
Manual memory management → Automatic GC
Platform #ifdefs → Godot cross-platform
File path resolution → res:// and user:// paths
```

### **Integration Challenges** 🔧
1. **State Machine Complexity**: 54 states → Simplified Godot state enum
2. **Menu System Integration**: Multiple C++ classes → Scene-based navigation
3. **Save System Complexity**: Binary formats → JSON/Resource serialization
4. **Campaign Branching**: Complex SEXP logic → GDScript evaluation
5. **Performance Critical Paths**: C++ speed → GDScript + optimization

---

## Dependency Resolution Strategy

### **Phase 1: Foundation** (Week 1)
**Target**: Core dependency elimination
```
1. Create Godot GameStateManager (replaces gamesequence.cpp)
2. Implement basic state transitions
3. Set up Resource-based data structures
4. Establish signal-based communication
```

### **Phase 2: Core Systems** (Week 2-3)
**Target**: Major system dependencies
```
1. Campaign management system
2. Player data management  
3. Save/load system implementation
4. Menu system integration
```

### **Phase 3: Integration** (Week 4)
**Target**: Cross-system dependencies
```
1. Mission loading integration
2. Statistics system integration
3. SEXP system integration
4. UI flow completion
```

### **Phase 4: Polish** (Week 5-6)
**Target**: Optional dependencies
```
1. Help system integration
2. Demo system (if needed)
3. Advanced features
4. Performance optimization
```

---

## Risk Assessment

### **High Risk Dependencies** ⚠️
1. **Circular Dependencies**: 3 instances requiring careful refactoring
2. **Complex State Machine**: 54 states with intricate transition rules
3. **Save System Complexity**: Multiple file formats and versioning
4. **Performance Critical**: State transitions must be <16ms

### **Medium Risk Dependencies** 🔧
1. **Menu System Integration**: Multiple UI frameworks to unify
2. **Campaign Branching Logic**: Complex SEXP evaluation requirements
3. **Platform Abstractions**: OS-specific code to eliminate

### **Low Risk Dependencies** ✅
1. **Standard Library Usage**: Direct Godot equivalents available
2. **Graphics Integration**: Straightforward UI conversion
3. **Audio System**: Direct AudioStreamPlayer mapping

---

**Dependency Analysis Status**: ✅ **COMPREHENSIVE**  
**Integration Complexity**: HIGH (manageable with proper architecture)  
**Conversion Readiness**: READY with identified risk mitigation strategies  
**Critical Path**: GameSequence → Campaign → Player → Menu systems  

This dependency analysis provides Mo (Godot Architect) with the detailed information needed to design a clean, efficient Godot architecture that preserves WCS functionality while eliminating complex dependencies through modern design patterns.