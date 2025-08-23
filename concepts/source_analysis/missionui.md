# Mission UI System Analysis

## Purpose
The mission UI system handles all user interface elements specific to missions, including briefing, debriefing, ship selection, and weapon loadout screens.

## Main Public Interfaces
- Briefing screen rendering and interaction
- Debriefing screen with mission results
- Ship selection interface
- Weapon loadout configuration
- Mission objectives display

## Key Components
- **Briefing System**: Mission introduction and intelligence
- **Debriefing System**: Mission results and statistics
- **Ship Selection**: Player ship choice interface
- **Weapon Loadout**: Equipment configuration
- **Objectives Display**: Current mission goals
- **Campaign Progress**: Story progression information

## Dependencies
- `ui.h` - General UI framework
- `mission.h` - Mission data and objectives
- `ship.h` - Ship information and properties
- `weapon.h` - Weapon information and properties
- `graphics.h` - Rendering functions

## Game Logic Integration
The mission UI system manages mission flow:
- Provides essential pre-mission information
- Handles post-mission evaluation and statistics
- Enables player customization of ship and weapons
- Integrates with campaign system for story progression
- Supports mission objectives and goal tracking