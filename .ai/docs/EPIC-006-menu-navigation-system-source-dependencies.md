# WCS System: Menu & Navigation System - Source Dependencies (Used By)

## Core Game Integration

### File: `source/code/gamesequence/gamesequence.h` included/used by:
- `source/code/freespace2/freespace.cpp` - Main game entry point and state management
- `source/code/menuui/mainhallmenu.cpp` - Main hall navigation integration
- `source/code/menuui/barracks.cpp` - Pilot menu state transitions
- `source/code/menuui/optionsmenu.cpp` - Options menu navigation
- `source/code/menuui/readyroom.cpp` - Ready room navigation
- `source/code/menuui/techmenu.cpp` - Tech database navigation
- `source/code/menuui/trainingmenu.cpp` - Training menu navigation
- `source/code/missionui/missionbrief.cpp` - Mission briefing flow control
- `source/code/missionui/missionshipchoice.cpp` - Ship selection flow control
- `source/code/missionui/missionweaponchoice.cpp` - Weapon selection flow control
- `source/code/missionui/missiondebrief.cpp` - Debriefing flow control
- `source/code/missionui/missionscreencommon.cpp` - Common mission navigation

### File: `source/code/gamesequence/gamesequence.cpp` included/used by:
- `source/code/freespace2/freespace.cpp` - Game state processing and main loop

## MenuUI System Dependencies

### File: `source/code/menuui/mainhallmenu.h` included/used by:
- `source/code/freespace2/freespace.cpp` - Main game integration for hall interface
- `source/code/cutscene/cutscenes.cpp` - Cutscene to main hall transitions
- `source/code/menuui/mainhallmenu.cpp` - Self-inclusion for implementation

### File: `source/code/menuui/barracks.h` included/used by:
- `source/code/freespace2/freespace.cpp` - Main game integration for pilot management
- `source/code/menuui/barracks.cpp` - Self-inclusion for implementation

### File: `source/code/menuui/optionsmenu.h` included/used by:
- `source/code/freespace2/freespace.cpp` - Main game integration for options
- `source/code/menuui/optionsmenu.cpp` - Self-inclusion for implementation

### File: `source/code/menuui/playermenu.h` included/used by:
- `source/code/freespace2/freespace.cpp` - Main game integration for player selection
- `source/code/menuui/playermenu.cpp` - Self-inclusion for implementation
- `source/code/menuui/barracks.cpp` - Player management integration

### File: `source/code/menuui/readyroom.h` included/used by:
- `source/code/freespace2/freespace.cpp` - Main game integration for ready room
- `source/code/menuui/readyroom.cpp` - Self-inclusion for implementation

### File: `source/code/menuui/techmenu.h` included/used by:
- `source/code/freespace2/freespace.cpp` - Main game integration for tech database
- `source/code/menuui/techmenu.cpp` - Self-inclusion for implementation
- `source/code/fred2/management.cpp` - Mission editor tech data integration
- `source/code/fred2/sexp_tree.cpp` - SEXP editor intel integration

### File: `source/code/menuui/snazzyui.h` included/used by:
- `source/code/freespace2/freespace.cpp` - Main game UI animation integration
- `source/code/menuui/snazzyui.cpp` - Self-inclusion for implementation
- `source/code/menuui/mainhallmenu.cpp` - Main hall UI animations
- `source/code/missionui/missionbrief.cpp` - Mission briefing animations

### File: `source/code/menuui/credits.h` included/used by:
- `source/code/freespace2/freespace.cpp` - Main game integration for credits
- `source/code/menuui/credits.cpp` - Self-inclusion for implementation

## MissionUI System Dependencies

### File: `source/code/missionui/missionscreencommon.h` included/used by:
- `source/code/missionui/missionbrief.cpp` - Mission briefing common functionality
- `source/code/missionui/missionshipchoice.cpp` - Ship selection common functionality
- `source/code/missionui/missionweaponchoice.cpp` - Weapon selection common functionality
- `source/code/missionui/missiondebrief.cpp` - Debriefing common functionality
- `source/code/missionui/missionscreencommon.cpp` - Self-inclusion for implementation

### File: `source/code/missionui/missionbrief.h` included/used by:
- `source/code/missionui/missionbrief.cpp` - Self-inclusion for implementation
- `source/code/missionui/missionscreencommon.cpp` - Mission flow integration

### File: `source/code/missionui/missionshipchoice.h` included/used by:
- `source/code/missionui/missionshipchoice.cpp` - Self-inclusion for implementation
- `source/code/missionui/missionscreencommon.cpp` - Mission flow integration
- `source/code/missionui/missionweaponchoice.cpp` - Ship/weapon selection coordination

### File: `source/code/missionui/missionweaponchoice.h` included/used by:
- `source/code/missionui/missionweaponchoice.cpp` - Self-inclusion for implementation
- `source/code/missionui/missionscreencommon.cpp` - Mission flow integration

### File: `source/code/missionui/missiondebrief.h` included/used by:
- `source/code/missionui/missiondebrief.cpp` - Self-inclusion for implementation

### File: `source/code/missionui/chatbox.h` included/used by:
- `source/code/missionui/chatbox.cpp` - Self-inclusion for implementation
- `source/code/missionui/missionbrief.cpp` - Multiplayer chat integration
- `source/code/missionui/missionscreencommon.cpp` - Common chat functionality

### File: `source/code/missionui/redalert.h` included/used by:
- `source/code/missionui/redalert.cpp` - Self-inclusion for implementation

## External System Dependencies

### Core Game System Integration:
- **UI Framework**: All menu systems depend on `ui/ui.h` for button, slider, and window management
- **Graphics System**: All systems depend on `graphics/` modules for rendering and bitmap management
- **Sound System**: All systems depend on `gamesnd/` modules for audio feedback and music
- **Input System**: All systems depend on `io/` modules for keyboard and mouse input
- **Game State**: All systems depend on `gamesequence/` for navigation and state transitions

### Asset Management Dependencies:
- **Animation System**: `anim/` modules for background animations and transitions
- **Model System**: `model/` modules for 3D ship previews in selection screens
- **Palette Management**: `palman/` modules for interface color management
- **Bitmap Management**: `bmpman/` modules for loading interface graphics

### Data System Dependencies:
- **Player Management**: `playerman/` modules for pilot data and statistics
- **Mission System**: `mission/` modules for mission data and campaign integration
- **Parse System**: `parse/` modules for configuration file parsing
- **Network System**: `network/` modules for multiplayer interface support

## Integration Complexity Analysis

### High Integration Points (>10 dependencies):
1. **gamesequence.h** - Core navigation framework used by all UI systems
2. **missionscreencommon.h** - Shared mission interface functionality
3. **UI framework headers** - Foundation for all interface systems

### Medium Integration Points (5-10 dependencies):
1. **mainhallmenu.h** - Main hub interface with moderate integration
2. **snazzyui.h** - UI animation system used across multiple screens

### Low Integration Points (<5 dependencies):
1. **Specialized menu headers** - Individual menu system interfaces
2. **Mission-specific headers** - Focused mission flow interfaces

This dependency structure reveals a well-organized hierarchical system where game sequence management provides the foundation, common UI frameworks provide shared functionality, and individual menu systems implement specific interfaces while maintaining clean separation of concerns.