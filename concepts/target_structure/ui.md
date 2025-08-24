# UI Module (Godot Implementation)

## Purpose
The UI Module provides all user interface functionality in the Godot implementation, including menus, HUD elements, briefing screens, debriefing displays, and in-game information panels. It handles both the foundational UI framework and specific game UI screens while leveraging Godot's powerful UI system.

## Components
- **UI Manager**: Central UI system management and screen switching
- **UI Screens**: Main menu, options, campaign, and gameplay screens
- **HUD System**: In-game information display with gauges and indicators
- **Radar System**: Tactical object tracking display with IFF coloring
- **Briefing System**: Mission introduction and intelligence presentation
- **Debriefing System**: Mission results and statistics evaluation
- **Fiction Viewer**: Narrative text presentation with formatting support
- **Cutscene Player**: Video and real-time cutscene presentation
- **Control Configuration**: Input mapping and settings interface
- **Tech Database**: Ship and weapon information displays
- **Options System**: Graphics, audio, and gameplay settings
- **Loading Screen**: Progress indication during resource loading
- **Message System**: Combat messages and communication display
- **Statistics Display**: Player performance and achievement tracking

## Dependencies
- **Core Entity Module**: UI displays information about game objects
- **Ship Module**: Ship status and weapon information
- **Weapon Module**: Weapon status display
- **Mission Module**: Mission data and objectives
- **Player Module**: Player-specific information
- **Game State Module**: UI state management and screen transitions
- **Audio Module**: Interface sound effects and feedback
- **Graphics Module**: Rendering functions and visual effects
