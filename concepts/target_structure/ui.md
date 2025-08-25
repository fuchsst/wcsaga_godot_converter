# UI Module (Godot Implementation)

## Purpose
The UI Module provides all user interface functionality in the Godot implementation, including menus, HUD elements, briefing screens, debriefing displays, and in-game information panels. It handles both the foundational UI framework and specific game UI screens while leveraging Godot's powerful UI system, organized in a feature-based structure.

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
- **Core Entity Module** (/scripts/entities/): UI displays information about game objects
- **Ship Module** (/features/fighters/): Ship status and weapon information
- **Weapon Module** (/features/weapons/): Weapon status display
- **Mission Module** (/campaigns/): Mission data and objectives
- **Player Module** (/scripts/entities/): Player-specific information
- **Game State Module** (/autoload/): UI state management and screen transitions
- **Audio Module** (/autoload/): Interface sound effects and feedback
- **Graphics Module** (/scripts/graphics/): Rendering functions and visual effects

## Directory Structure Implementation
Following the feature-based organization principles, the UI Module is organized as follows:

### Features Directory (/features/ui/)
UI elements are implemented as self-contained features in `/features/ui/`:

- `/features/ui/main_menu/` - Main menu interface
  - `main_menu.tscn` - Main scene file
  - `main_menu.gd` - Primary controller script
  - `background.png` - Background texture
  - `/buttons/` - Button assets
    - `/normal/` - Normal button states
    - `/hover/` - Hover button states
    - `/pressed/` - Pressed button states
  - `/animations/` - Menu animations
    - `/transitions/` - Screen transitions
    - `/background/` - Background animations
  - `/sounds/` - Menu sounds
    - `click.ogg` - Button click sound
    - `hover.ogg` - Button hover sound
    - `transition.ogg` - Transition sound

- `/features/ui/hud/` - Heads-up display
  - `player_hud.tscn` - Main HUD scene
  - `player_hud.gd` - HUD controller script
  - `/gauges/` - Gauge components
    - `/speed/` - Speed indicator
    - `/shields/` - Shield status
    - `/weapons/` - Weapon status
    - `/fuel/` - Fuel level
  - `/indicators/` - HUD indicators
    - `/targets/` - Targeting indicators
    - `/warnings/` - Warning indicators
    - `/status/` - System status
  - `/animations/` - HUD animations
    - `/warnings/` - Warning animations
    - `/status/` - Status animations
  - `/sounds/` - HUD sounds
    - `warning.ogg` - Warning sound
    - `target_acquired.ogg` - Target acquisition sound
    - `system_status.ogg` - System status sound

- `/features/ui/briefing/` - Briefing interface
  - `briefing_screen.tscn` - Main briefing scene
  - `briefing_screen.gd` - Briefing controller script
  - `background.png` - Background texture
  - `/text_display/` - Text display components
  - `/mission_map/` - Mission map display
  - `/animations/` - Briefing animations
  - `/sounds/` - Briefing sounds
    - `voice_playback.ogg` - Voice playback
    - `transition.ogg` - Transition sound

- `/features/ui/debriefing/` - Debriefing interface
  - `debriefing_screen.tscn` - Main debriefing scene
  - `debriefing_screen.gd` - Debriefing controller script
  - `background.png` - Background texture
  - `/results_display/` - Results display components
  - `/statistics/` - Statistics display
  - `/animations/` - Debriefing animations
  - `/sounds/` - Debriefing sounds
    - `voice_playback.ogg` - Voice playback
    - `transition.ogg` - Transition sound

- `/features/ui/options/` - Options menu
  - `options_menu.tscn` - Main options scene
  - `options_menu.gd` - Options controller script
  - `/backgrounds/` - Background textures
  - `/sliders/` - Slider components
  - `/checkboxes/` - Checkbox components
  - `/animations/` - Options animations
  - `/sounds/` - Options sounds
    - `change_setting.ogg` - Setting change sound
    - `reset_defaults.ogg` - Reset defaults sound

- `/features/ui/tech_database/` - Technical database
  - `tech_database.tscn` - Main database scene
  - `tech_database.gd` - Database controller script
  - `/backgrounds/` - Background textures
  - `/ship_entries/` - Ship entry components
  - `/weapon_entries/` - Weapon entry components
  - `/animations/` - Database animations
  - `/sounds/` - Database sounds
    - `entry_select.ogg` - Entry selection sound
    - `page_turn.ogg` - Page turn sound

- `/features/ui/_shared/` - Shared UI assets
  - `/fonts/` - UI fonts
  - `/icons/` - UI icons
  - `/themes/` - UI themes
  - `/cursors/` - Cursor graphics
  - `/components/` - Reusable UI components
    - `/buttons/` - Button components
    - `/sliders/` - Slider components
    - `/checkboxes/` - Checkbox components
    - `/dropdowns/` - Dropdown components
    - `/text_fields/` - Text field components
    - `/lists/` - List components

- `/features/ui/templates/` - UI templates
  - Template scenes for creating new UI elements

### Autoload Directory (/autoload/)
Global UI-related singletons:

- `/autoload/ui_manager.gd` - Central UI system management
- `/autoload/game_state.gd` - Game state management affecting UI
- `/autoload/audio_manager.gd` - Audio management for UI sounds

### Scripts Directory (/scripts/)
Reusable UI logic and components:

- `/scripts/ui/base_ui_element.gd` - Base UI element class
- `/scripts/ui/ui_manager.gd` - UI management logic
- `/scripts/ui/hud_components/` - HUD component classes
- `/scripts/ui/menu_systems/` - Menu system classes

### Assets Directory (/assets/)
Shared UI assets used across multiple features:

- `/assets/textures/ui/` - Generic UI elements
- `/assets/audio/sfx/ui/` - UI sound effects
- `/assets/animations/ui/` - Generic UI animations

## Implementation Notes
The UI Module in Godot leverages feature-based organization principles:

1. **Self-Contained Features**: Each UI screen or component is a self-contained directory with all related assets
2. **Shared Assets**: Common UI assets are organized in `/features/ui/_shared/` for semi-global access
3. **Templates**: UI templates are available in `/features/ui/templates/` for consistent creation of new elements
4. **Global Systems**: Core UI management is handled by autoload scripts in `/autoload/`
5. **Reusable Components**: Abstract UI logic is organized in `/scripts/ui/` for extension by features
6. **Global Assets**: Truly generic UI assets are placed in `/assets/textures/ui/` and `/assets/audio/sfx/ui/`

This replaces the C++ structure-based approach with Godot's node-based scene system while preserving the same gameplay functionality. The implementation uses Godot's Control nodes for UI elements and the resource system for UI configurations, organized according to Godot's feature-based best practices where each UI element has its own self-contained directory with all related assets.

Following the feature-based organization principles:
- UI elements are implemented as self-contained features in `/features/ui/`
- Core UI logic is implemented as reusable scripts in `/scripts/ui/`
- Shared UI assets are organized in `/features/ui/_shared/`
- Global UI systems are implemented as autoloads in `/autoload/`
- Truly generic UI assets are placed in `/assets/`