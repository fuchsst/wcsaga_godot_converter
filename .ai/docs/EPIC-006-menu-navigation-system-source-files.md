# WCS System: Menu & Navigation System - Source Files List

## MenuUI Directory (Primary Menu Systems)

### Core Menu Files
- `source/code/menuui/mainhallmenu.cpp`: Main hall hub interface with animations, ambient sounds, and region detection
- `source/code/menuui/mainhallmenu.h`: Main hall interface declarations and constants
- `source/code/menuui/mainhalltemp.cpp`: Main hall template and configuration data parsing
- `source/code/menuui/mainhalltemp.h`: Main hall template structure definitions

### Pilot Management System  
- `source/code/menuui/barracks.cpp`: Pilot creation, selection, deletion, and statistics display (1,500+ lines)
- `source/code/menuui/barracks.h`: Barracks interface declarations

### Options and Configuration
- `source/code/menuui/optionsmenu.cpp`: Graphics, audio, control configuration interface (1,600+ lines)
- `source/code/menuui/optionsmenu.h`: Options menu structure definitions including slider components
- `source/code/menuui/optionsmenumulti.cpp`: Multiplayer-specific options and network configuration (2,000+ lines)
- `source/code/menuui/optionsmenumulti.h`: Multiplayer options interface declarations

### Player Information and Navigation
- `source/code/menuui/playermenu.cpp`: Player pilot selection and management interface (1,300+ lines)
- `source/code/menuui/playermenu.h`: Player menu interface declarations
- `source/code/menuui/readyroom.cpp`: Ready room interface for campaign and mission access (1,600+ lines)
- `source/code/menuui/readyroom.h`: Ready room interface declarations

### Secondary Menu Systems
- `source/code/menuui/techmenu.cpp`: Technical database browser for ships, weapons, and intelligence (1,300+ lines)
- `source/code/menuui/techmenu.h`: Tech menu interface declarations
- `source/code/menuui/trainingmenu.cpp`: Training mission selection and management
- `source/code/menuui/trainingmenu.h`: Training menu interface declarations
- `source/code/menuui/credits.cpp`: Credits display system with scrolling text and music
- `source/code/menuui/credits.h`: Credits interface declarations

### UI Framework Support
- `source/code/menuui/snazzyui.cpp`: Common UI animation and transition effects
- `source/code/menuui/snazzyui.h`: UI animation framework declarations
- `source/code/menuui/fishtank.cpp`: Animated background effects and particle systems
- `source/code/menuui/fishtank.h`: Fishtank animation declarations

## MissionUI Directory (Mission Flow Interface)

### Mission Briefing System
- `source/code/missionui/missionbrief.cpp`: Mission briefing presentation with animations and voice (1,600+ lines)
- `source/code/missionui/missionbrief.h`: Mission briefing interface declarations
- `source/code/missionui/missioncmdbrief.cpp`: Command briefing for special missions (600+ lines)
- `source/code/missionui/missioncmdbrief.h`: Command briefing interface declarations

### Mission Planning and Selection
- `source/code/missionui/missionshipchoice.cpp`: Ship selection interface with 3D preview (2,700+ lines)
- `source/code/missionui/missionshipchoice.h`: Ship selection interface declarations and hotspot definitions
- `source/code/missionui/missionweaponchoice.cpp`: Weapon loadout configuration interface (3,400+ lines)
- `source/code/missionui/missionweaponchoice.h`: Weapon selection interface declarations
- `source/code/missionui/missionloopbrief.cpp`: Campaign loop briefing system (230+ lines)
- `source/code/missionui/missionloopbrief.h`: Loop briefing interface declarations

### Mission Results and Debriefing
- `source/code/missionui/missiondebrief.cpp`: Post-mission debriefing and statistics (2,200+ lines)
- `source/code/missionui/missiondebrief.h`: Debriefing interface declarations
- `source/code/missionui/redalert.cpp`: Red alert mission transition interface (750+ lines)
- `source/code/missionui/redalert.h`: Red alert interface declarations

### Mission Flow Support
- `source/code/missionui/missionscreencommon.cpp`: Common mission screen functionality and navigation (1,300+ lines)
- `source/code/missionui/missionscreencommon.h`: Shared mission interface declarations and structures
- `source/code/missionui/missionpause.cpp`: In-mission pause menu system (240+ lines)
- `source/code/missionui/missionpause.h`: Mission pause interface declarations

### Communication and Interaction
- `source/code/missionui/chatbox.cpp`: Multiplayer chat interface for mission screens (1,000+ lines)
- `source/code/missionui/chatbox.h`: Chat interface declarations and data structures
- `source/code/missionui/fictionviewer.cpp`: Fiction/story viewer for campaign content (360+ lines)
- `source/code/missionui/fictionviewer.h`: Fiction viewer interface declarations

### Placeholder Systems (Minimal Implementation)
- `source/code/missionui/missionrecommend.cpp`: Mission recommendation system (minimal - 8 lines)
- `source/code/missionui/missionrecommend.h`: Mission recommendation declarations
- `source/code/missionui/missionstats.cpp`: Mission statistics system (minimal - 8 lines)
- `source/code/missionui/missionstats.h`: Mission statistics declarations

## Game Sequence System (Navigation Framework)

### Core Navigation Control
- `source/code/gamesequence/gamesequence.cpp`: Game state management and transition system (1,500+ lines)
- `source/code/gamesequence/gamesequence.h`: Game state definitions and event management framework

## Total File Count: 36 Files
- **MenuUI Files**: 24 files (12 .cpp + 12 .h)
- **MissionUI Files**: 26 files (13 .cpp + 13 .h) 
- **GameSequence Files**: 2 files (1 .cpp + 1 .h)
- **Total Lines of Code**: Approximately 25,000+ lines across all systems

## File Size Distribution
- **Large Implementation Files (1,000+ lines)**: 8 files
- **Medium Implementation Files (500-1,000 lines)**: 6 files  
- **Small Implementation Files (<500 lines)**: 10 files
- **Header Files**: 18 files (typically 50-200 lines each)