# Game State Module (Godot Implementation)

## Purpose
The Game State Module manages the overall game state and event flow in the Godot implementation, controlling transitions between different game modes such as menus, briefing, gameplay, and debriefing. It orchestrates the entire game flow from startup to shutdown while leveraging Godot's node-based architecture and scene system, following the feature-based organization principles with the hybrid model approach.

## Components
- **Game State Manager**: Central state management and event processing
- **Game States**: Main menu, gameplay, briefing, debriefing, etc.
- **Game Events**: Triggers for state transitions
- **State Stack**: Push/pop mechanism for nested states
- **Event Queue**: Pending events awaiting processing
- **Main Game Loop**: Primary game execution cycle
- **Initialization**: System setup and resource loading
- **Shutdown**: Cleanup and resource deallocation
- **Configuration Management**: Game settings and preferences
- **Save System**: Player progress and campaign state

## Dependencies
- **All Major Game Systems**: States interact with their respective systems
- **UI Module**: State transitions often involve UI changes
- **Mission Module**: Mission loading and execution
- **Player Module**: Player state management
- **Audio Module**: Music and sound state management
- **Graphics Module**: Rendering state and quality settings

## Implementation Notes
The Game State Module in Godot leverages several key features following feature-based organization with the hybrid model approach:

1. **Singleton Pattern**: GameStateManager as global singleton using Godot's autoload system, located in `/autoload/game_state.gd`, following the "Is this state or service truly global and required everywhere?" principle
2. **State Machine**: Robust state management with enter/leave state callbacks
3. **Event System**: Queue-based event processing with delayed state changes, utilizing the global event bus in `/autoload/event_bus.gd`
4. **Resource System**: Configuration and difficulty profiles as data-driven resources
5. **Scene System**: State transitions using scene switching between UI features in `/features/ui/`, with each UI state organized as a self-contained feature following the co-location principle
6. **Input System**: Integrated input handling with remappable controls
7. **Save System**: Persistent save game management with metadata, utilizing `/autoload/save_manager.gd`
8. **Configuration Management**: Flexible settings system with file persistence

This replaces the C++ game sequence system with Godot's node-based approach while preserving the same state management functionality. The implementation uses Godot's scene tree for state transitions and the resource system for configuration management.

The event system provides decoupled communication between systems through the global event bus, and the input manager handles cross-state input mapping. The save system provides persistent player progress, and the difficulty system scales gameplay appropriately.

The campaign manager handles mission sequencing and progression, while the difficulty manager adjusts gameplay balance. The configuration manager provides a centralized settings system that persists between sessions.

The implementation uses Godot's built-in systems for most functionality, reducing the need for custom implementations while maintaining the same overall architecture and gameplay flow.

Game state data resources are organized in `/features/templates/` for generic templates, following the template structure defined in directory_structure.md. Specific UI scenes for each state (main menu, briefing, debriefing, etc.) are organized in their respective self-contained directories under `/features/ui/`:

- Main menu scenes in `/features/ui/main_menu/`
- HUD scenes in `/features/ui/hud/`
- Briefing scenes in `/features/ui/briefing/`
- Debriefing scenes in `/features/ui/debriefing/`
- Options scenes in `/features/ui/options/`
- Tech database scenes in `/features/ui/tech_database/`

Shared UI components that might be used across multiple states are located in `/features/ui/_shared/`, following the "Managing Dependencies and Shared Feature-Assets" pattern from the Godot_Project_Structure_Refinement.md document. Truly global UI assets like generic sound effects, fonts, and UI themes are organized in `/assets/audio/ui/`, `/assets/textures/ui/`, and `/assets/textures/fonts/` respectively, following the "Global Litmus Test": "If I delete three random features, is this asset still needed?"

This approach treats each UI feature as a self-contained module, aligning perfectly with Godot's design philosophy of creating self-contained scenes that encapsulate their own logic and resources. Each UI feature directory contains all files related to that specific UI element, eliminating the inefficient and error-prone process of "folder hopping" that plagues type-organized projects.