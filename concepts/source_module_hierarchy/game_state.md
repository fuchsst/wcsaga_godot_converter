# Game State Module

## Purpose
The Game State Module manages the overall game state and event flow, controlling transitions between different game modes such as menus, briefing, gameplay, and debriefing. It orchestrates the entire game flow from startup to shutdown.

## Components
- **Game Sequence System** (`gamesequence/`): State management and event processing
- **Game States**: Main menu, gameplay, briefing, debriefing, etc.
- **Game Events**: Triggers for state transitions
- **State Stack**: Push/pop mechanism for nested states
- **Event Queue**: Pending events awaiting processing
- **Main Game Loop** (`freespace2/`): Primary game execution cycle
- **Initialization**: System setup and resource loading
- **Shutdown**: Cleanup and resource deallocation

## Dependencies
- **All Major Game Systems**: States interact with their respective systems
- **UI Module**: State transitions often involve UI changes
- **Mission Module**: Mission loading and execution
- **Player Module**: Player state management

## C++ Components
- `gameseq_init()`: Initializes the game sequence system
- `gameseq_process_events()`: Processes pending events and updates state
- `gameseq_post_event()`: Posts an event for processing
- `gameseq_set_state()`: Changes the current game state
- `gameseq_get_state()`: Gets the current game state
- `game_enter_state()`: Called when entering a new state
- `game_leave_state()`: Called when leaving a state
- `game_do_state()`: Called each frame to process current state
- `game_init()`: Game initialization
- `game_main()`: Main game loop
- `game_shutdown()`: Game cleanup and shutdown

## Godot Equivalent Mapping

### Native GDScript Classes
```gdscript
# Game state manager handling state transitions and events
class GameStateManager:
    enum State {
        NONE,
        MAIN_MENU,
        OPTIONS_MENU,
        CAMPAIGN_MENU,
        BRIEFING,
        GAMEPLAY,
        DEBRIEFING,
        PAUSE_MENU,
        LOADING,
        CREDITS,
        QUIT
    }
    
    enum Event {
        NONE,
        START_GAME,
        END_GAME,
        PAUSE_GAME,
        RESUME_GAME,
        SHOW_OPTIONS,
        SHOW_MAIN_MENU,
        SHOW_CREDITS,
        QUIT_GAME,
        MISSION_COMPLETED,
        PLAYER_DIED,
        LOAD_MISSION
    }
    
    var current_state: State = State.NONE
    var previous_state: State = State.NONE
    var state_stack: Array[State] = []
    var event_queue: Array[Event] = []
    var pending_state_change: State = State.NONE
    var state_change_timer: float = 0.0
    var state_change_delay: float = 0.1  # Small delay to prevent rapid state changes
    
    func _ready():
        # Initialize the game state system
        initialize()
        
    func _process(delta):
        # Process state changes with delay protection
        if state_change_timer > 0:
            state_change_timer -= delta
        elif pending_state_change != State.NONE:
            change_state_immediately(pending_state_change)
            pending_state_change = State.NONE
            
        # Process the current state
        process_current_state(delta)
        
        # Process pending events
        process_events()
        
    func initialize():
        # Initialize game systems
        initialize_subsystems()
        # Start with main menu
        change_state(State.MAIN_MENU)
        
    func initialize_subsystems():
        # Initialize all required subsystems
        Config.load()
        SoundDatabase.load_sound_definitions()
        # ... other initialization
        
    func change_state(new_state: State):
        # Schedule state change with delay protection
        if state_change_timer <= 0:
            change_state_immediately(new_state)
        else:
            pending_state_change = new_state
            
    func change_state_immediately(new_state: State):
        # Handle state transition immediately
        if new_state == current_state:
            return
            
        # Leave current state
        leave_state(current_state)
        
        # Save previous state and update current
        previous_state = current_state
        current_state = new_state
        
        # Enter new state
        enter_state(new_state)
        
        # Reset state change timer
        state_change_timer = state_change_delay
        
    func enter_state(state: State):
        # Handle entering a new state
        match state:
            State.MAIN_MENU:
                UIManager.show_screen("MainMenu")
                AudioManager.play_music("main_theme")
                
            State.OPTIONS_MENU:
                UIManager.show_screen("Options")
                
            State.BRIEFING:
                UIManager.show_screen("Briefing")
                AudioManager.play_music("briefing_theme")
                
            State.GAMEPLAY:
                # Hide UI screens and start gameplay
                UIManager.hide_current_screen()
                MissionManager.start_current_mission()
                AudioManager.play_music("combat_theme")
                
            State.DEBRIEFING:
                UIManager.show_screen("Debriefing")
                MissionManager.end_current_mission()
                AudioManager.play_music("debriefing_theme")
                
            State.PAUSE_MENU:
                UIManager.show_screen("PauseMenu")
                # Pause game systems
                get_tree().paused = true
                
            State.LOADING:
                UIManager.show_screen("Loading")
                
            State.CREDITS:
                UIManager.show_screen("Credits")
                AudioManager.play_music("credits_theme")
                
            State.QUIT:
                get_tree().quit()
                
    func leave_state(state: State):
        # Handle leaving a state
        match state:
            State.MAIN_MENU:
                UIManager.hide_current_screen()
                
            State.GAMEPLAY:
                # Clean up gameplay state
                MissionManager.cleanup_current_mission()
                
            State.PAUSE_MENU:
                UIManager.hide_current_screen()
                # Resume game systems
                get_tree().paused = false
                
            State.LOADING:
                UIManager.hide_current_screen()
                
    func process_current_state(delta):
        # Handle per-frame processing for current state
        match current_state:
            State.GAMEPLAY:
                # Update gameplay systems
                MissionManager.update_current_mission(delta)
                EntityManager.update_entities(delta)
                
            State.LOADING:
                # Update loading progress
                update_loading_progress(delta)
                
    func post_event(event: Event):
        # Add event to queue for processing
        event_queue.append(event)
        
    func process_events():
        # Process all pending events
        while event_queue.size() > 0:
            var event = event_queue.pop_front()
            handle_event(event)
            
    func handle_event(event: Event):
        # Handle specific events
        match event:
            Event.START_GAME:
                change_state(State.LOADING)
                # Load mission in background
                MissionManager.load_mission_async()
                # When loading complete, transition to briefing
                call_deferred("change_state", State.BRIEFING)
                
            Event.END_GAME:
                change_state(State.DEBRIEFING)
                
            Event.PAUSE_GAME:
                # Push current state to stack and enter pause
                state_stack.push_back(current_state)
                change_state(State.PAUSE_MENU)
                
            Event.RESUME_GAME:
                # Pop state from stack and return
                if state_stack.size() > 0:
                    var previous = state_stack.pop_back()
                    change_state(previous)
                else:
                    change_state(State.GAMEPLAY)
                    
            Event.SHOW_OPTIONS:
                # Push current state and show options
                state_stack.push_back(current_state)
                change_state(State.OPTIONS_MENU)
                
            Event.SHOW_MAIN_MENU:
                change_state(State.MAIN_MENU)
                
            Event.MISSION_COMPLETED:
                change_state(State.DEBRIEFING)
                
            Event.PLAYER_DIED:
                # Handle player death
                if MissionManager.current_mission.allows_respawn():
                    MissionManager.respawn_player()
                else:
                    change_state(State.DEBRIEFING)
                    
            Event.LOAD_MISSION:
                change_state(State.LOADING)
                
    func push_state(new_state: State):
        # Push current state and enter new one
        state_stack.push_back(current_state)
        change_state(new_state)
        
    func pop_state():
        # Return to previous state in stack
        if state_stack.size() > 0:
            var previous = state_stack.pop_back()
            change_state(previous)
            
    func get_state() -> State:
        return current_state
        
    func get_previous_state() -> State:
        return previous_state

# Mission manager handling mission loading and execution
class MissionManager:
    var current_mission: Mission
    var is_mission_active: bool = false
    var mission_progress: float = 0.0
    
    func load_mission_async():
        # Asynchronously load mission data
        # This would typically run in a thread or use await
        pass
        
    func start_current_mission():
        if current_mission != null:
            current_mission.start_mission()
            is_mission_active = true
            
    func update_current_mission(delta):
        if is_mission_active and current_mission != null:
            current_mission.update_mission(delta)
            check_mission_end_conditions()
            
    func end_current_mission():
        if current_mission != null:
            current_mission.end_mission()
            is_mission_active = false
            
    func cleanup_current_mission():
        # Clean up mission resources
        if current_mission != null:
            current_mission.cleanup()
            current_mission = null
            
    func check_mission_end_conditions():
        # Check if mission is completed or failed
        if current_mission != null:
            if current_mission.is_completed():
                GameStateManager.post_event(GameStateManager.Event.MISSION_COMPLETED)
            elif current_mission.is_failed():
                GameStateManager.post_event(GameStateManager.Event.PLAYER_DIED)

# Game configuration manager
class Config:
    var graphics_settings: Dictionary = {}
    var audio_settings: Dictionary = {}
    var control_settings: Dictionary = {}
    var player_settings: Dictionary = {}
    
    func load():
        # Load configuration from file
        var file = FileAccess.open("user://config.cfg", FileAccess.READ)
        if file != null:
            var data = file.get_as_text()
            var json = JSON.new()
            var parse_result = json.parse(data)
            if parse_result == OK:
                var config_data = json.get_data()
                graphics_settings = config_data.get("graphics", {})
                audio_settings = config_data.get("audio", {})
                control_settings = config_data.get("controls", {})
                player_settings = config_data.get("player", {})
                
    func save():
        # Save configuration to file
        var config_data = {
            "graphics": graphics_settings,
            "audio": audio_settings,
            "controls": control_settings,
            "player": player_settings
        }
        
        var json = JSON.new()
        var data = json.stringify(config_data)
        
        var file = FileAccess.open("user://config.cfg", FileAccess.WRITE)
        if file != null:
            file.store_string(data)
            file.close()
            
    func get_graphics_setting(key: String, default_value):
        return graphics_settings.get(key, default_value)
        
    func set_graphics_setting(key: String, value):
        graphics_settings[key] = value
        
    func get_audio_setting(key: String, default_value):
        return audio_settings.get(key, default_value)
        
    func set_audio_setting(key: String, value):
        audio_settings[key] = value

# Game manager as main game controller
class GameManager:
    var player_ship: Ship
    var player_profile: PlayerProfile
    var is_game_running: bool = false
    
    func _ready():
        # Initialize game systems
        GameStateManager.initialize()
        
    func start_new_campaign():
        # Create new player profile and start campaign
        player_profile = PlayerProfile.new()
        player_profile.create_new_pilot("Blair")
        # Load first mission
        MissionManager.current_mission = MissionDatabase.get_mission("first_mission")
        GameStateManager.post_event(GameStateManager.Event.START_GAME)
        
    func load_campaign(save_file: String):
        # Load existing campaign
        player_profile = PlayerProfile.load_from_file(save_file)
        # Load current mission
        MissionManager.current_mission = MissionDatabase.get_mission(
            player_profile.current_mission)
        GameStateManager.post_event(GameStateManager.Event.START_GAME)
        
    func save_campaign():
        # Save current campaign state
        if player_profile != null:
            player_profile.save_to_file()
```

### TRES Resources
```ini
[gd_resource type="Resource" load_steps=2 format=2]

[resource]
resource_name = "Default_Game_Config"
graphics_settings = {
    "resolution": Vector2(1920, 1080),
    "fullscreen": true,
    "vsync": true,
    "quality": "high"
}
audio_settings = {
    "master_volume": 1.0,
    "music_volume": 0.8,
    "sfx_volume": 1.0,
    "voice_volume": 1.0
}
control_settings = {
    "mouse_sensitivity": 1.0,
    "invert_y": false,
    "key_bindings": {
        "throttle_up": "Key.W",
        "throttle_down": "Key.S",
        "turn_left": "Key.A",
        "turn_right": "Key.D"
    }
}
player_settings = {
    "pilot_name": "Blair",
    "difficulty": "normal"
}
```

### TSCN Scenes
```ini
[gd_scene load_steps=3 format=2]

[ext_resource path="res://scripts/game_manager.gd" type="Script" id=1]
[ext_resource path="res://scripts/game_state_manager.gd" type="Script" id=2]

[node name="Game" type="Node"]
script = ExtResource(1)

[node name="GameStateManager" type="Node" parent="."]
script = ExtResource(2)

[node name="AudioManager" type="Node" parent="."]
script = "res://scripts/audio_manager.gd"
```

### Implementation Notes
The Game State Module in Godot leverages:
1. **State Machine Pattern**: For managing game states and transitions
2. **Event Queue**: For processing game events in order
3. **Autoload**: GameStateManager as a global singleton
4. **Scene System**: State transitions involving UI screen changes
5. **Signals**: For communication between systems
6. **Resource System**: Configuration as data-driven assets
7. **Node Tree**: Game systems as nodes in the scene tree

This replaces the C++ game sequence system with Godot's node-based approach while preserving the same state management functionality. The implementation uses Godot's scene tree for state transitions and the resource system for configuration management.