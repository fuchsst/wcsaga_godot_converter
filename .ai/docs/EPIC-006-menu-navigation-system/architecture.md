# EPIC-006: Menu & Navigation System - Architecture

**Document Version**: 1.0  
**Date**: 2025-01-26  
**Architect**: Mo (Godot Architect)  
**Epic**: EPIC-006 - Menu & Navigation System  
**System**: Main menus, briefing screens, pilot management, navigation UI  
**Approval Status**: PENDING (SallySM)  

---

## Architecture Philosophy (Mo's Principles)

> **"Menus are the gateway to WCS - they must feel familiar yet leverage modern UI capabilities."**
> 
> This architecture creates a modern, responsive menu system using Godot's Control nodes while maintaining the authentic WCS interface feel through careful visual design and smooth transitions.

### Core Design Principles

1. **Scene-Based Navigation**: Each major menu is its own scene for clean separation
2. **Signal-Driven Flow**: Navigation uses signals for loose coupling
3. **Resource-Based Data**: Pilot data and settings use Godot Resources
4. **Responsive Design**: Adapts to different screen resolutions
5. **Accessibility First**: Clear typography, proper contrast, keyboard navigation
6. **Performance Optimized**: Fast transitions and minimal loading times

## System Architecture Overview

```
Menu & Navigation System
├── Core Navigation                    # Scene management and transitions
│   ├── MenuManager                   # Central navigation coordination
│   ├── SceneTransition              # Smooth scene transitions
│   ├── NavigationStack              # Menu history and back navigation
│   └── LoadingManager               # Loading screens and progress
├── Main Menu System                  # Primary game entry
│   ├── MainMenuScene                # Main hall and primary navigation
│   ├── MainHallBackground           # Animated background system
│   ├── CampaignSelection            # Campaign browser and selection
│   └── CreditsSystem                # Credits and information display
├── Pilot Management                  # Player profile system
│   ├── PilotCreation                # New pilot creation interface
│   ├── PilotSelection               # Pilot management and selection
│   ├── StatisticsDisplay            # Pilot stats and medal display
│   └── ProgressionTracker           # Campaign and skill progression
├── Mission Flow Interface            # Mission briefing/debriefing
│   ├── MissionBriefing              # Pre-mission briefing system
│   ├── ShipSelection                # Ship and loadout selection
│   ├── MissionDebrief               # Post-mission results
│   └── ObjectiveDisplay             # Mission objective tracking
├── Options & Configuration           # Settings management
│   ├── OptionsMain                  # Main options interface
│   ├── GraphicsOptions              # Graphics and performance settings
│   ├── AudioOptions                 # Audio configuration
│   ├── ControlsOptions              # Input and control mapping
│   └── GameplayOptions              # Gameplay preferences
└── Shared UI Components              # Reusable interface elements
    ├── MenuButton                   # Standardized menu button
    ├── DialogBox                    # Modal dialog system
    ├── LoadingScreen                # Loading screen management
    ├── TransitionEffects            # Screen transition effects
    └── SoundManager                 # Menu sound effects and music
```

## Key Component Interfaces

```gdscript
# Menu Manager - Central navigation coordination
class_name MenuManager
extends Node

# Scene navigation
func navigate_to_scene(scene_path: String, transition_type: TransitionType = TransitionType.FADE) -> void
func navigate_back() -> void
func get_current_scene() -> Node

# Menu state management
func push_menu_state(state: MenuState) -> void
func pop_menu_state() -> MenuState
func clear_menu_stack() -> void

# Pilot Management System
class_name PilotManager
extends RefCounted

# Pilot operations
func create_pilot(pilot_data: PilotProfile) -> bool
func load_pilot(pilot_name: String) -> PilotProfile
func save_pilot(pilot: PilotProfile) -> bool
func delete_pilot(pilot_name: String) -> bool
func get_pilot_list() -> Array[String]

# Statistics and progression
func update_pilot_stats(pilot: PilotProfile, mission_stats: MissionStats) -> void
func award_medal(pilot: PilotProfile, medal_type: MedalType) -> void
func update_campaign_progress(pilot: PilotProfile, mission_id: String) -> void

# Options Manager - Settings persistence
class_name OptionsManager
extends RefCounted

# Settings management
func load_settings() -> GameSettings
func save_settings(settings: GameSettings) -> void
func reset_to_defaults() -> void
func validate_settings(settings: GameSettings) -> ValidationResult

# Control mapping
func save_control_mapping(mapping: ControlMapping) -> void
func load_control_mapping() -> ControlMapping
func reset_controls_to_default() -> void
```

## Menu Flow Architecture

```gdscript
# Scene Transition System
class_name SceneTransitionManager
extends Node

enum TransitionType {
    INSTANT,
    FADE,
    SLIDE_LEFT,
    SLIDE_RIGHT,
    DISSOLVE
}

# Transition execution
func transition_to_scene(new_scene: PackedScene, transition: TransitionType) -> void:
    _start_transition_out(transition)
    await transition_out_complete
    _change_scene(new_scene)
    _start_transition_in(transition)
    await transition_in_complete

# Async loading for large scenes
func load_scene_async(scene_path: String) -> void:
    ResourceLoader.load_threaded_request(scene_path)
    _monitor_loading_progress(scene_path)

# Menu Navigation Stack
class_name NavigationStack
extends RefCounted

var _menu_stack: Array[MenuState] = []

func push_menu(menu_scene: String, data: Dictionary = {}) -> void:
    var state = MenuState.new()
    state.scene_path = menu_scene
    state.menu_data = data
    state.timestamp = Time.get_ticks_msec()
    _menu_stack.push_back(state)

func pop_menu() -> MenuState:
    if _menu_stack.size() > 1:  # Keep at least one menu
        return _menu_stack.pop_back()
    return null

func can_go_back() -> bool:
    return _menu_stack.size() > 1
```

## Data Architecture

```gdscript
# Pilot Profile Resource
class_name PilotProfile
extends Resource

@export var pilot_name: String
@export var callsign: String
@export var squadron: String
@export var pilot_image: String
@export var creation_date: String
@export var last_played: String

# Campaign progression
@export var current_campaign: String
@export var missions_completed: Array[String] = []
@export var campaign_variables: Dictionary = {}
@export var story_branch_choices: Dictionary = {}

# Statistics
@export var flight_time_hours: float = 0.0
@export var missions_flown: int = 0
@export var kills_total: int = 0
@export var friendly_kills: int = 0
@export var medals_earned: Array[String] = []

# Preferences
@export var control_scheme: String = "default"
@export var difficulty_level: int = 2
@export var hud_configuration: Dictionary = {}

# Validation
func is_valid() -> bool:
    return pilot_name.length() > 0 and callsign.length() > 0

# Game Settings Resource
class_name GameSettings
extends Resource

# Graphics settings
@export var resolution: Vector2i = Vector2i(1920, 1080)
@export var fullscreen_mode: int = 0  # 0=windowed, 1=fullscreen, 2=borderless
@export var vsync_enabled: bool = true
@export var quality_preset: int = 2  # 0=low, 1=medium, 2=high, 3=ultra

# Audio settings
@export var master_volume: float = 1.0
@export var music_volume: float = 0.8
@export var sfx_volume: float = 1.0
@export var voice_volume: float = 1.0

# Gameplay settings
@export var mouse_sensitivity: float = 1.0
@export var invert_mouse_y: bool = false
@export var auto_target_enabled: bool = true
@export var difficulty_level: int = 2
```

## UI Design Architecture

```gdscript
# Shared UI Theme System
class_name UIThemeManager
extends RefCounted

# Theme management
func load_wcs_theme() -> Theme:
    var theme = Theme.new()
    _setup_button_styles(theme)
    _setup_text_styles(theme)
    _setup_panel_styles(theme)
    return theme

func _setup_button_styles(theme: Theme) -> void:
    var button_style = StyleBoxFlat.new()
    button_style.bg_color = Color(0.2, 0.3, 0.4, 0.8)
    button_style.border_width_left = 2
    button_style.border_width_right = 2
    button_style.border_width_top = 2
    button_style.border_width_bottom = 2
    button_style.border_color = Color(0.6, 0.8, 1.0)
    button_style.corner_radius_top_left = 4
    button_style.corner_radius_top_right = 4
    button_style.corner_radius_bottom_left = 4
    button_style.corner_radius_bottom_right = 4
    
    theme.set_stylebox("normal", "Button", button_style)

# Responsive Layout System
class_name ResponsiveLayout
extends Control

# Layout adaptation
func _ready() -> void:
    get_viewport().size_changed.connect(_on_viewport_size_changed)
    _adapt_layout()

func _on_viewport_size_changed() -> void:
    _adapt_layout()

func _adapt_layout() -> void:
    var viewport_size = get_viewport().size
    if viewport_size.x < 1280:
        _apply_compact_layout()
    else:
        _apply_standard_layout()

# Animation System
class_name MenuAnimations
extends RefCounted

# Standard animations
func fade_in(control: Control, duration: float = 0.3) -> void:
    control.modulate.a = 0.0
    var tween = control.create_tween()
    tween.tween_property(control, "modulate:a", 1.0, duration)

func slide_in_from_left(control: Control, duration: float = 0.5) -> void:
    var start_pos = control.position
    control.position.x -= control.size.x
    var tween = control.create_tween()
    tween.tween_property(control, "position", start_pos, duration)
    tween.tween_callback(func(): control.position = start_pos)
```

## Performance Optimization

```gdscript
# Menu Preloading System
class_name MenuPreloader
extends Node

var _preloaded_scenes: Dictionary = {}
var _preloading_queue: Array[String] = []

# Preload common menus
func preload_common_menus() -> void:
    var common_menus = [
        "res://scenes/menus/main_menu.tscn",
        "res://scenes/menus/options_menu.tscn",
        "res://scenes/menus/pilot_selection.tscn"
    ]
    
    for menu_path in common_menus:
        _preload_scene_async(menu_path)

func _preload_scene_async(scene_path: String) -> void:
    if not _preloaded_scenes.has(scene_path):
        ResourceLoader.load_threaded_request(scene_path)
        _preloading_queue.append(scene_path)

func get_preloaded_scene(scene_path: String) -> PackedScene:
    return _preloaded_scenes.get(scene_path)

# Memory Management
func _process(_delta: float) -> void:
    _check_preloading_progress()
    _cleanup_unused_scenes()

func _cleanup_unused_scenes() -> void:
    # Remove preloaded scenes that haven't been used recently
    var current_time = Time.get_ticks_msec()
    for scene_path in _preloaded_scenes.keys():
        var last_used = _scene_last_used.get(scene_path, 0)
        if current_time - last_used > 300000:  # 5 minutes
            _preloaded_scenes.erase(scene_path)
```

## Integration Points

### Mission System Integration
```gdscript
# Mission briefing integration
func _on_mission_selected(mission_id: String) -> void:
    var mission_data = MissionManager.load_mission(mission_id)
    var briefing_scene = preload("res://scenes/menus/mission_briefing.tscn")
    var briefing = briefing_scene.instantiate()
    briefing.setup_mission_data(mission_data)
    MenuManager.navigate_to_scene_instance(briefing)

# Ship selection integration
func _on_ship_selection_confirmed(ship_class: String, loadout: WeaponLoadout) -> void:
    var pilot = PilotManager.get_current_pilot()
    pilot.selected_ship = ship_class
    pilot.weapon_loadout = loadout
    PilotManager.save_pilot(pilot)
    
    # Launch mission
    GameStateManager.start_mission(pilot.current_mission, pilot)
```

### Save System Integration
```gdscript
# Pilot data persistence
func save_pilot_progress(pilot: PilotProfile, mission_result: MissionResult) -> void:
    # Update pilot statistics
    pilot.missions_flown += 1
    pilot.flight_time_hours += mission_result.flight_time
    pilot.kills_total += mission_result.kills
    
    # Update campaign progress
    if mission_result.success:
        pilot.missions_completed.append(mission_result.mission_id)
        _update_campaign_variables(pilot, mission_result)
    
    # Save to disk
    var save_path = "user://pilots/" + pilot.pilot_name + ".tres"
    ResourceSaver.save(pilot, save_path)
```

---

**Critical Features:**
- **Intuitive Navigation**: Familiar WCS menu flow with modern responsiveness
- **Pilot Management**: Complete pilot creation, statistics, and progression
- **Fast Transitions**: Smooth scene changes under 2 seconds
- **Settings Persistence**: Robust configuration management across platforms

**Integration Points:**
- EPIC-007: Game Flow & State Management (scene transitions)
- EPIC-002: Asset Structures (pilot data, settings)
- EPIC-004: SEXP Expression System (mission briefing integration)
- EPIC-005: GFRED2 Mission Editor (mission selection)

**Next Steps:**
1. UI mockups and visual design specifications
2. Menu flow diagram and navigation mapping
3. Pilot data migration from existing WCS saves
4. Performance testing with different screen resolutions