# Game State Module (Godot Implementation)

## Purpose
The Game State Module manages the overall game state and event flow in the Godot implementation, controlling transitions between different game modes such as menus, briefing, gameplay, and debriefing. It orchestrates the entire game flow from startup to shutdown while leveraging Godot's node-based architecture and scene system.

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

## Godot Implementation Details

### Native GDScript Classes
```gdscript
# Game state manager handling state transitions and events
class GameStateManager extends Node:
    # Game state enumeration
    enum State {
        NONE,
        SPLASH_SCREEN,
        MAIN_MENU,
        OPTIONS_MENU,
        CAMPAIGN_MENU,
        TRAINING_MENU,
        TECH_MENU,
        BRIEFING,
        GAMEPLAY,
        DEBRIEFING,
        PAUSE_MENU,
        LOADING,
        CREDITS,
        CUTSCENE,
        FICTION_VIEWER,
        QUIT
    }
    
    # Game event enumeration
    enum Event {
        NONE,
        START_GAME,
        END_GAME,
        PAUSE_GAME,
        RESUME_GAME,
        SHOW_OPTIONS,
        SHOW_MAIN_MENU,
        SHOW_CAMPAIGN,
        SHOW_CREDITS,
        QUIT_GAME,
        MISSION_COMPLETED,
        PLAYER_DIED,
        LOAD_MISSION,
        SHOW_BRIEFING,
        SHOW_DEBRIEFING,
        SHOW_CUTSCENE,
        SHOW_FICTION,
        SAVE_GAME,
        LOAD_GAME
    }
    
    # Current state management
    var currentState: State = State.NONE
    var previousState: State = State.NONE
    var stateStack: Array[State] = []
    var pendingStateChange: State = State.NONE
    var stateChangeTimer: float = 0.0
    var stateChangeDelay: float = 0.1  # Small delay to prevent rapid state changes
    
    # Event queue
    var eventQueue: Array[Event] = []
    var pendingEvents: Array[Dictionary] = []  # Events with parameters
    
    # Game systems
    var missionManager: MissionManager = null
    var playerManager: PlayerManager = null
    var audioManager: AudioManager = null
    var uiManager: UIManager = null
    var configManager: ConfigManager = null
    
    # Game flow control
    var isGameRunning: bool = false
    var isPaused: bool = false
    var gameTimeScale: float = 1.0
    
    # Signals
    signal state_changed(old_state, new_state)
    signal event_processed(event)
    signal game_initialized()
    signal game_shutdown()
    
    func _ready():
        # Initialize the game state system
        initialize()
        
    func _process(delta):
        # Process state changes with delay protection
        if stateChangeTimer > 0:
            stateChangeTimer -= delta
        elif pendingStateChange != State.NONE:
            change_state_immediately(pendingStateChange)
            pendingStateChange = State.NONE
            
        # Process the current state
        process_current_state(delta)
        
        # Process pending events
        process_events()
        
    func initialize():
        # Initialize game systems
        initialize_subsystems()
        
        # Start with splash screen or main menu
        change_state(State.SPLASH_SCREEN)
        
        # Emit initialization signal
        emit_signal("game_initialized")
        
    func initialize_subsystems():
        # Initialize all required subsystems
        configManager = ConfigManager.new()
        configManager.load_config()
        
        # Initialize managers
        missionManager = MissionManager.new()
        playerManager = PlayerManager.new()
        audioManager = AudioManager.new()
        uiManager = UIManager.new()
        
        # Add managers as children for proper node lifecycle
        add_child(missionManager)
        add_child(playerManager)
        add_child(audioManager)
        add_child(uiManager)
        
        # Connect signals
        connect_managers_signals()
        
    func connect_managers_signals():
        # Connect manager signals
        if missionManager != null:
            missionManager.connect("mission_loaded", Callable(self, "_on_mission_loaded"))
            missionManager.connect("mission_started", Callable(self, "_on_mission_started"))
            missionManager.connect("mission_completed", Callable(self, "_on_mission_completed"))
            
        if playerManager != null:
            playerManager.connect("player_ship_changed", Callable(self, "_on_player_ship_changed"))
            
    func change_state(new_state: State):
        # Schedule state change with delay protection
        if stateChangeTimer <= 0:
            change_state_immediately(new_state)
        else:
            pendingStateChange = new_state
            
    func change_state_immediately(new_state: State):
        # Handle state transition immediately
        if new_state == currentState:
            return
            
        # Leave current state
        leave_state(currentState)
        
        # Save previous state and update current
        previousState = currentState
        currentState = new_state
        
        # Enter new state
        enter_state(new_state)
        
        # Reset state change timer
        stateChangeTimer = stateChange_delay
        
        # Emit state change signal
        emit_signal("state_changed", previousState, currentState)
        
    func enter_state(state: State):
        # Handle entering a new state
        match state:
            State.SPLASH_SCREEN:
                uiManager.show_screen("SplashScreen")
                audioManager.play_music("intro_theme")
                
            State.MAIN_MENU:
                uiManager.show_screen("MainMenu")
                audioManager.play_music("main_theme")
                
            State.OPTIONS_MENU:
                uiManager.show_screen("OptionsMenu")
                
            State.CAMPAIGN_MENU:
                uiManager.show_screen("CampaignMenu")
                
            State.TRAINING_MENU:
                uiManager.show_screen("TrainingMenu")
                
            State.TECH_MENU:
                uiManager.show_screen("TechMenu")
                
            State.BRIEFING:
                uiManager.show_screen("Briefing")
                audioManager.play_music("briefing_theme")
                
            State.GAMEPLAY:
                # Hide UI screens and start gameplay
                uiManager.hide_current_screen()
                start_gameplay()
                audioManager.play_music("combat_theme")
                
            State.DEBRIEFING:
                uiManager.show_screen("Debriefing")
                end_current_mission()
                audioManager.play_music("debriefing_theme")
                
            State.PAUSE_MENU:
                # Push current state to stack and enter pause
                stateStack.push_back(currentState)
                uiManager.show_screen("PauseMenu")
                # Pause game systems
                isPaused = true
                get_tree().paused = true
                
            State.LOADING:
                uiManager.show_screen("Loading")
                
            State.CREDITS:
                uiManager.show_screen("Credits")
                audioManager.play_music("credits_theme")
                
            State.CUTSCENE:
                uiManager.show_screen("CutscenePlayer")
                
            State.FICTION_VIEWER:
                uiManager.show_screen("FictionViewer")
                
            State.QUIT:
                shutdown_game()
                
    func leave_state(state: State):
        # Handle leaving a state
        match state:
            State.MAIN_MENU:
                uiManager.hide_current_screen()
                
            State.GAMEPLAY:
                # Clean up gameplay state
                cleanup_gameplay()
                
            State.PAUSE_MENU:
                uiManager.hide_current_screen()
                # Resume game systems
                isPaused = false
                get_tree().paused = false
                
            State.LOADING:
                uiManager.hide_current_screen()
                
            State.BRIEFING:
                uiManager.hide_current_screen()
                
            State.DEBRIEFING:
                uiManager.hide_current_screen()
                
    func process_current_state(delta):
        # Handle per-frame processing for current state
        if isPaused:
            return
            
        match currentState:
            State.GAMEPLAY:
                # Update gameplay systems
                update_gameplay(delta)
                
            State.LOADING:
                # Update loading progress
                update_loading_progress(delta)
                
            State.CUTSCENE:
                # Update cutscene playback
                update_cutscene(delta)
                
    func start_gameplay():
        # Start gameplay systems
        isGameRunning = true
        
        # Start current mission
        if missionManager != null:
            missionManager.start_current_mission()
            
    func update_gameplay(delta):
        # Update gameplay systems with time scaling
        var scaled_delta = delta * gameTimeScale
        
        # Update mission
        if missionManager != null:
            missionManager.update_current_mission(scaled_delta)
            
        # Update player
        if playerManager != null:
            playerManager.update_player(scaled_delta)
            
        # Check mission end conditions
        check_mission_end_conditions()
        
    func cleanup_gameplay():
        # Clean up gameplay state
        isGameRunning = false
        
        # Clean up mission
        if missionManager != null:
            missionManager.cleanup_current_mission()
            
    func check_mission_end_conditions():
        # Check if mission is completed or failed
        if missionManager != null:
            if missionManager.is_mission_completed():
                post_event(Event.MISSION_COMPLETED)
            elif missionManager.is_mission_failed():
                post_event(Event.PLAYER_DIED)
                
    func update_loading_progress(delta):
        # Update loading progress
        if missionManager != null:
            var progress = missionManager.get_loading_progress()
            # Update loading screen UI with progress
            uiManager.update_loading_progress(progress)
            
            # Check if loading is complete
            if missionManager.is_loading_complete():
                # Transition to briefing or gameplay
                if missionManager.should_show_briefing():
                    change_state(State.BRIEFING)
                else:
                    change_state(State.GAMEPLAY)
                    
    func update_cutscene(delta):
        # Update cutscene playback
        # This would interface with the cutscene system
        pass
        
    func post_event(event: Event, parameters: Dictionary = {}):
        # Add event to queue for processing
        pendingEvents.append({
            "event": event,
            "parameters": parameters,
            "timestamp": Time.get_ticks_msec()
        })
        
    func process_events():
        # Process all pending events
        while not pendingEvents.is_empty():
            var event_data = pendingEvents.pop_front()
            var event = event_data["event"]
            var parameters = event_data["parameters"]
            handle_event(event, parameters)
            emit_signal("event_processed", event)
            
    func handle_event(event: Event, parameters: Dictionary = {}):
        # Handle specific events
        match event:
            Event.START_GAME:
                change_state(State.LOADING)
                # Load mission in background
                if missionManager != null:
                    missionManager.load_mission_async()
                    
            Event.END_GAME:
                change_state(State.DEBRIEFING)
                
            Event.PAUSE_GAME:
                # Push current state to stack and enter pause
                stateStack.push_back(currentState)
                change_state(State.PAUSE_MENU)
                
            Event.RESUME_GAME:
                # Pop state from stack and return
                if not stateStack.is_empty():
                    var previous = stateStack.pop_back()
                    change_state(previous)
                else:
                    change_state(State.GAMEPLAY)
                    
            Event.SHOW_OPTIONS:
                # Push current state and show options
                stateStack.push_back(currentState)
                change_state(State.OPTIONS_MENU)
                
            Event.SHOW_MAIN_MENU:
                change_state(State.MAIN_MENU)
                
            Event.MISSION_COMPLETED:
                change_state(State.DEBRIEFING)
                
            Event.PLAYER_DIED:
                # Handle player death
                if missionManager != null and missionManager.current_mission.allows_respawn():
                    if missionManager.respawn_player():
                        # Player respawned, continue gameplay
                        pass
                    else:
                        # Respawn failed, end mission
                        change_state(State.DEBRIEFING)
                else:
                    change_state(State.DEBRIEFING)
                    
            Event.LOAD_MISSION:
                change_state(State.LOADING)
                
            Event.SHOW_BRIEFING:
                change_state(State.BRIEFING)
                
            Event.SHOW_DEBRIEFING:
                change_state(State.DEBRIEFING)
                
            Event.SHOW_CUTSCENE:
                change_state(State.CUTSCENE)
                
            Event.SHOW_FICTION:
                change_state(State.FICTION_VIEWER)
                
            Event.SAVE_GAME:
                if playerManager != null:
                    playerManager.save_game()
                    
            Event.LOAD_GAME:
                if playerManager != null:
                    var save_file = parameters.get("save_file", "")
                    if playerManager.load_game(save_file):
                        change_state(State.GAMEPLAY)
                        
    func push_state(new_state: State):
        # Push current state and enter new one
        stateStack.push_back(currentState)
        change_state(new_state)
        
    func pop_state():
        # Return to previous state in stack
        if not stateStack.is_empty():
            var previous = stateStack.pop_back()
            change_state(previous)
            
    func get_state() -> State:
        return currentState
        
    func get_previous_state() -> State:
        return previousState
        
    func is_in_gameplay() -> bool:
        return currentState == State.GAMEPLAY
        
    func is_in_menu() -> bool:
        return currentState in [State.MAIN_MENU, State.OPTIONS_MENU, State.CAMPAIGN_MENU, 
                                State.TRAINING_MENU, State.TECH_MENU]
                                
    func is_game_paused() -> bool:
        return isPaused
        
    func set_game_paused(paused: bool):
        isPaused = paused
        get_tree().paused = paused
        
    func set_time_scale(scale: float):
        gameTimeScale = clamp(scale, 0.1, 10.0)
        
    func get_time_scale() -> float:
        return gameTimeScale
        
    func save_config():
        # Save game configuration
        if configManager != null:
            configManager.save_config()
            
    func load_config():
        # Load game configuration
        if configManager != null:
            configManager.load_config()
            
    func shutdown_game():
        # Shutdown game systems
        emit_signal("game_shutdown")
        
        # Save configuration
        save_config()
        
        # Cleanup resources
        cleanup_resources()
        
        # Quit application
        get_tree().quit()
        
    func cleanup_resources():
        # Cleanup game resources
        if missionManager != null:
            missionManager.cleanup()
            
        if audioManager != null:
            audioManager.cleanup()
            
    func get_mission_manager() -> MissionManager:
        return missionManager
        
    func get_player_manager() -> PlayerManager:
        return playerManager
        
    func get_audio_manager() -> AudioManager:
        return audioManager
        
    func get_ui_manager() -> UIManager:
        return uiManager
        
    func get_config_manager() -> ConfigManager:
        return configManager
        
    # Signal handlers
    func _on_mission_loaded(mission):
        # Handle mission loaded event
        pass
        
    func _on_mission_started():
        # Handle mission started event
        pass
        
    func _on_mission_completed(success: bool):
        # Handle mission completed event
        post_event(Event.MISSION_COMPLETED)
        
    func _on_player_ship_changed(new_ship: Ship):
        # Handle player ship changed event
        pass

# Configuration manager for game settings
class ConfigManager extends Node:
    # Graphics settings
    var graphics_resolution: Vector2 = Vector2(1920, 1080)
    var graphics_fullscreen: bool = true
    var graphics_vsync: bool = true
    var graphics_quality: String = "high"
    var graphics_brightness: float = 1.0
    var graphics_contrast: float = 1.0
    
    # Audio settings
    var audio_master_volume: float = 1.0
    var audio_music_volume: float = 0.8
    var audio_sfx_volume: float = 1.0
    var audio_voice_volume: float = 1.0
    var audio_enable_3d: bool = true
    
    # Control settings
    var control_mouse_sensitivity: float = 1.0
    var control_invert_y: bool = false
    var control_keyboard_bindings: Dictionary = {}
    var control_joystick_bindings: Dictionary = {}
    var control_use_joystick: bool = false
    
    # Gameplay settings
    var gameplay_difficulty: String = "normal"
    var gameplay_auto_pilot: bool = false
    var gameplay_show_hud: bool = true
    var gameplay_show_radar: bool = true
    
    # Multiplayer settings
    var multiplayer_name: String = "Pilot"
    var multiplayer_port: int = 7808
    var multiplayer_server: String = "localhost"
    
    func _ready():
        # Load default configuration
        load_defaults()
        
    func load_defaults():
        # Set default configuration values
        graphics_resolution = Vector2(1920, 1080)
        graphics_fullscreen = true
        graphics_vsync = true
        graphics_quality = "high"
        graphics_brightness = 1.0
        graphics_contrast = 1.0
        
        audio_master_volume = 1.0
        audio_music_volume = 0.8
        audio_sfx_volume = 1.0
        audio_voice_volume = 1.0
        audio_enable_3d = true
        
        control_mouse_sensitivity = 1.0
        control_invert_y = false
        control_use_joystick = false
        
        gameplay_difficulty = "normal"
        gameplay_auto_pilot = false
        gameplay_show_hud = true
        gameplay_show_radar = true
        
        multiplayer_name = "Blair"
        multiplayer_port = 7808
        multiplayer_server = "localhost"
        
    func load_config():
        # Load configuration from file
        var config_file = "user://config.cfg"
        var file = FileAccess.open(config_file, FileAccess.READ)
        
        if file != null:
            var data = file.get_as_text()
            var json = JSON.new()
            var parse_result = json.parse(data)
            
            if parse_result == OK:
                var config_data = json.data
                
                # Load graphics settings
                if config_data.has("graphics"):
                    var graphics = config_data["graphics"]
                    graphics_resolution = Vector2(graphics.get("resolution_x", 1920), 
                                                 graphics.get("resolution_y", 1080))
                    graphics_fullscreen = graphics.get("fullscreen", true)
                    graphics_vsync = graphics.get("vsync", true)
                    graphics_quality = graphics.get("quality", "high")
                    graphics_brightness = graphics.get("brightness", 1.0)
                    graphics_contrast = graphics.get("contrast", 1.0)
                    
                # Load audio settings
                if config_data.has("audio"):
                    var audio = config_data["audio"]
                    audio_master_volume = audio.get("master_volume", 1.0)
                    audio_music_volume = audio.get("music_volume", 0.8)
                    audio_sfx_volume = audio.get("sfx_volume", 1.0)
                    audio_voice_volume = audio.get("voice_volume", 1.0)
                    audio_enable_3d = audio.get("enable_3d", true)
                    
                # Load control settings
                if config_data.has("controls"):
                    var controls = config_data["controls"]
                    control_mouse_sensitivity = controls.get("mouse_sensitivity", 1.0)
                    control_invert_y = controls.get("invert_y", false)
                    control_keyboard_bindings = controls.get("keyboard_bindings", {})
                    control_joystick_bindings = controls.get("joystick_bindings", {})
                    control_use_joystick = controls.get("use_joystick", false)
                    
                # Load gameplay settings
                if config_data.has("gameplay"):
                    var gameplay = config_data["gameplay"]
                    gameplay_difficulty = gameplay.get("difficulty", "normal")
                    gameplay_auto_pilot = gameplay.get("auto_pilot", false)
                    gameplay_show_hud = gameplay.get("show_hud", true)
                    gameplay_show_radar = gameplay.get("show_radar", true)
                    
                # Load multiplayer settings
                if config_data.has("multiplayer"):
                    var multiplayer = config_data["multiplayer"]
                    multiplayer_name = multiplayer.get("name", "Blair")
                    multiplayer_port = multiplayer.get("port", 7808)
                    multiplayer_server = multiplayer.get("server", "localhost")
                    
            file.close()
            
    func save_config():
        # Save configuration to file
        var config_data = {
            "graphics": {
                "resolution_x": graphics_resolution.x,
                "resolution_y": graphics_resolution.y,
                "fullscreen": graphics_fullscreen,
                "vsync": graphics_vsync,
                "quality": graphics_quality,
                "brightness": graphics_brightness,
                "contrast": graphics_contrast
            },
            "audio": {
                "master_volume": audio_master_volume,
                "music_volume": audio_music_volume,
                "sfx_volume": audio_sfx_volume,
                "voice_volume": audio_voice_volume,
                "enable_3d": audio_enable_3d
            },
            "controls": {
                "mouse_sensitivity": control_mouse_sensitivity,
                "invert_y": control_invert_y,
                "keyboard_bindings": control_keyboard_bindings,
                "joystick_bindings": control_joystick_bindings,
                "use_joystick": control_use_joystick
            },
            "gameplay": {
                "difficulty": gameplay_difficulty,
                "auto_pilot": gameplay_auto_pilot,
                "show_hud": gameplay_show_hud,
                "show_radar": gameplay_show_radar
            },
            "multiplayer": {
                "name": multiplayer_name,
                "port": multiplayer_port,
                "server": multiplayer_server
            }
        }
        
        var json = JSON.new()
        var data = json.stringify(config_data, "  ")
        
        var config_file = "user://config.cfg"
        var file = FileAccess.open(config_file, FileAccess.WRITE)
        if file != null:
            file.store_string(data)
            file.close()
            
    func apply_graphics_settings():
        # Apply graphics settings to rendering system
        if DisplayServer.has_feature("window_management"):
            # Set resolution
            DisplayServer.window_set_size(Vector2i(graphics_resolution))
            
            # Set fullscreen
            if graphics_fullscreen:
                DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_FULLSCREEN)
            else:
                DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
                
            # Set VSync
            # This would depend on the rendering backend
            
        # Apply brightness/contrast adjustments
        # This would interface with post-processing effects
        
    func apply_audio_settings():
        # Apply audio settings to audio system
        if GameStateManager.get_instance().audioManager != null:
            var audio = GameStateManager.get_instance().audioManager
            audio.set_master_volume(audio_master_volume)
            audio.set_music_volume(audio_music_volume)
            audio.set_sfx_volume(audio_sfx_volume)
            audio.set_voice_volume(audio_voice_volume)
            
    func get_graphics_setting(key: String, default_value):
        # Get graphics setting with default fallback
        match key:
            "resolution_x": return graphics_resolution.x
            "resolution_y": return graphics_resolution.y
            "fullscreen": return graphics_fullscreen
            "vsync": return graphics_vsync
            "quality": return graphics_quality
            "brightness": return graphics_brightness
            "contrast": return graphics_contrast
            _:
                return default_value
                
    func set_graphics_setting(key: String, value):
        # Set graphics setting
        match key:
            "resolution_x": graphics_resolution.x = value
            "resolution_y": graphics_resolution.y = value
            "fullscreen": graphics_fullscreen = value
            "vsync": graphics_vsync = value
            "quality": graphics_quality = value
            "brightness": graphics_brightness = value
            "contrast": graphics_contrast = value
            
    func get_audio_setting(key: String, default_value):
        # Get audio setting with default fallback
        match key:
            "master_volume": return audio_master_volume
            "music_volume": return audio_music_volume
            "sfx_volume": return audio_sfx_volume
            "voice_volume": return audio_voice_volume
            "enable_3d": return audio_enable_3d
            _:
                return default_value
                
    func set_audio_setting(key: String, value):
        # Set audio setting
        match key:
            "master_volume": audio_master_volume = value
            "music_volume": audio_music_volume = value
            "sfx_volume": audio_sfx_volume = value
            "voice_volume": audio_voice_volume = value
            "enable_3d": audio_enable_3d = value
            
    func get_control_setting(key: String, default_value):
        # Get control setting with default fallback
        match key:
            "mouse_sensitivity": return control_mouse_sensitivity
            "invert_y": return control_invert_y
            "use_joystick": return control_use_joystick
            _:
                return default_value
                
    func set_control_setting(key: String, value):
        # Set control setting
        match key:
            "mouse_sensitivity": control_mouse_sensitivity = value
            "invert_y": control_invert_y = value
            "use_joystick": control_use_joystick = value
            
    func get_gameplay_setting(key: String, default_value):
        # Get gameplay setting with default fallback
        match key:
            "difficulty": return gameplay_difficulty
            "auto_pilot": return gameplay_auto_pilot
            "show_hud": return gameplay_show_hud
            "show_radar": return gameplay_show_radar
            _:
                return default_value
                
    func set_gameplay_setting(key: String, value):
        # Set gameplay setting
        match key:
            "difficulty": gameplay_difficulty = value
            "auto_pilot": gameplay_auto_pilot = value
            "show_hud": gameplay_show_hud = value
            "show_radar": gameplay_show_radar = value
            
    func get_multiplayer_setting(key: String, default_value):
        # Get multiplayer setting with default fallback
        match key:
            "name": return multiplayer_name
            "port": return multiplayer_port
            "server": return multiplayer_server
            _:
                return default_value
                
    func set_multiplayer_setting(key: String, value):
        # Set multiplayer setting
        match key:
            "name": multiplayer_name = value
            "port": multiplayer_port = value
            "server": multiplayer_server = value

# Save game system for player progress
class SaveGameManager extends Node:
    var save_slots: Array[SaveSlot] = []
    var max_save_slots: int = 10
    
    func _ready():
        # Initialize save system
        initialize_save_system()
        
    func initialize_save_system():
        # Create save directory if it doesn't exist
        var save_dir = "user://saves/"
        if not DirAccess.dir_exists_absolute(save_dir):
            DirAccess.make_dir_absolute(save_dir)
            
        # Load existing save slots
        load_save_slots()
        
    func load_save_slots():
        # Load save slot information
        save_slots.clear()
        
        var save_dir = "user://saves/"
        var dir = DirAccess.open(save_dir)
        if dir != null:
            dir.list_dir_begin()
            var file_name = dir.get_next()
            while file_name != "":
                if file_name.ends_with(".save"):
                    var slot = SaveSlot.new()
                    slot.file_name = file_name
                    slot.slot_number = int(file_name.substr(0, file_name.find(".")))
                    slot.load_metadata()
                    save_slots.append(slot)
                file_name = dir.get_next()
            dir.list_dir_end()
            
    func create_new_save_slot(pilot_name: String) -> int:
        # Create a new save slot
        var slot_number = get_next_available_slot()
        if slot_number >= 0:
            var slot = SaveSlot.new()
            slot.slot_number = slot_number
            slot.pilot_name = pilot_name
            slot.created_date = Time.get_date_string_from_system()
            slot.last_played = Time.get_datetime_string_from_system()
            save_slots.append(slot)
            return slot_number
        return -1
        
    func get_next_available_slot() -> int:
        # Find next available save slot number
        for i in range(max_save_slots):
            var slot_used = false
            for slot in save_slots:
                if slot.slot_number == i:
                    slot_used = true
                    break
            if not slot_used:
                return i
        return -1
        
    func save_game(slot_number: int, player_data: PlayerData) -> bool:
        # Save game to specified slot
        for slot in save_slots:
            if slot.slot_number == slot_number:
                return slot.save_game(player_data)
        return false
        
    func load_game(slot_number: int) -> PlayerData:
        # Load game from specified slot
        for slot in save_slots:
            if slot.slot_number == slot_number:
                return slot.load_game()
        return null
        
    func delete_save_slot(slot_number: int) -> bool:
        # Delete save slot
        for i in range(save_slots.size()):
            var slot = save_slots[i]
            if slot.slot_number == slot_number:
                if slot.delete_save_file():
                    save_slots.remove_at(i)
                    return true
        return false
        
    func get_save_slot(slot_number: int) -> SaveSlot:
        # Get save slot information
        for slot in save_slots:
            if slot.slot_number == slot_number:
                return slot
        return null
        
    func get_all_save_slots() -> Array[SaveSlot]:
        # Get all save slots
        return save_slots.duplicate()

# Save slot representing a save game
class SaveSlot extends Resource:
    @export var slot_number: int = -1
    @export var pilot_name: String = ""
    @export var campaign_name: String = ""
    @export var mission_name: String = ""
    @export var created_date: String = ""
    @export var last_played: String = ""
    @export var play_time: float = 0.0
    @export var difficulty: String = ""
    @export var rank: String = ""
    @export var score: int = 0
    
    var file_name: String = ""
    
    func _init():
        if slot_number >= 0:
            file_name = str(slot_number) + ".save"
        else:
            file_name = "autosave.save"
            
    func save_game(player_data: PlayerData) -> bool:
        # Save player data to save file
        var save_data = {
            "pilot_name": pilot_name,
            "campaign_name": campaign_name,
            "mission_name": mission_name,
            "created_date": created_date,
            "last_played": Time.get_datetime_string_from_system(),
            "play_time": play_time,
            "difficulty": difficulty,
            "rank": rank,
            "score": score,
            "player_data": player_data.serialize() if player_data != null else {}
        }
        
        var json = JSON.new()
        var data = json.stringify(save_data, "  ")
        
        var save_file = "user://saves/" + file_name
        var file = FileAccess.open(save_file, FileAccess.WRITE)
        if file != null:
            file.store_string(data)
            file.close()
            return true
        return false
        
    func load_game() -> PlayerData:
        # Load player data from save file
        var save_file = "user://saves/" + file_name
        var file = FileAccess.open(save_file, FileAccess.READ)
        if file != null:
            var data = file.get_as_text()
            file.close()
            
            var json = JSON.new()
            var parse_result = json.parse(data)
            if parse_result == OK:
                var save_data = json.data
                
                # Update metadata
                pilot_name = save_data.get("pilot_name", pilot_name)
                campaign_name = save_data.get("campaign_name", campaign_name)
                mission_name = save_data.get("mission_name", mission_name)
                last_played = save_data.get("last_played", last_played)
                play_time = save_data.get("play_time", play_time)
                difficulty = save_data.get("difficulty", difficulty)
                rank = save_data.get("rank", rank)
                score = save_data.get("score", score)
                
                # Load player data
                var player_data_dict = save_data.get("player_data", {})
                if not player_data_dict.is_empty():
                    var player_data = PlayerData.new()
                    player_data.deserialize(player_data_dict)
                    return player_data
                    
        return null
        
    func load_metadata():
        # Load only metadata from save file (for save slot display)
        var save_file = "user://saves/" + file_name
        var file = FileAccess.open(save_file, FileAccess.READ)
        if file != null:
            var data = file.get_as_text()
            file.close()
            
            var json = JSON.new()
            var parse_result = json.parse(data)
            if parse_result == OK:
                var save_data = json.data
                
                pilot_name = save_data.get("pilot_name", "Untitled")
                campaign_name = save_data.get("campaign_name", "No Campaign")
                mission_name = save_data.get("mission_name", "No Mission")
                created_date = save_data.get("created_date", "")
                last_played = save_data.get("last_played", "")
                play_time = save_data.get("play_time", 0.0)
                difficulty = save_data.get("difficulty", "normal")
                rank = save_data.get("rank", "Ensign")
                score = save_data.get("score", 0)
                
    func delete_save_file() -> bool:
        # Delete save file
        var save_file = "user://saves/" + file_name
        return DirAccess.remove_absolute(save_file) == OK
        
    func get_formatted_play_time() -> String:
        # Return formatted play time string
        var hours = int(play_time / 3600)
        var minutes = int((play_time % 3600) / 60)
        return "%02d:%02d" % [hours, minutes]
        
    func get_formatted_last_played() -> String:
        # Return formatted last played string
        return last_played

# Player data for saving/loading
class PlayerData extends Resource:
    @export var pilot_name: String = ""
    @export var campaign_progress: Dictionary = {}
    @export var ship_classes_unlocked: Array[String] = []
    @export var weapons_unlocked: Array[String] = []
    @export var medals_earned: Array[String] = []
    @export var total_score: int = 0
    @export var total_play_time: float = 0.0
    @export var current_campaign: String = ""
    @export var current_mission: String = ""
    @export var player_ship_setup: PlayerShipSetup = null
    @export var statistics: PlayerStatistics = null
    
    func serialize() -> Dictionary:
        # Serialize player data to dictionary
        return {
            "pilot_name": pilot_name,
            "campaign_progress": campaign_progress,
            "ship_classes_unlocked": ship_classes_unlocked,
            "weapons_unlocked": weapons_unlocked,
            "medals_earned": medals_earned,
            "total_score": total_score,
            "total_play_time": total_play_time,
            "current_campaign": current_campaign,
            "current_mission": current_mission,
            "player_ship_setup": player_ship_setup.serialize() if player_ship_setup != null else {},
            "statistics": statistics.serialize() if statistics != null else {}
        }
        
    func deserialize(data: Dictionary):
        # Deserialize player data from dictionary
        pilot_name = data.get("pilot_name", pilot_name)
        campaign_progress = data.get("campaign_progress", campaign_progress)
        ship_classes_unlocked = data.get("ship_classes_unlocked", ship_classes_unlocked)
        weapons_unlocked = data.get("weapons_unlocked", weapons_unlocked)
        medals_earned = data.get("medals_earned", medals_earned)
        total_score = data.get("total_score", total_score)
        total_play_time = data.get("total_play_time", total_play_time)
        current_campaign = data.get("current_campaign", current_campaign)
        current_mission = data.get("current_mission", current_mission)
        
        # Deserialize nested objects
        var ship_setup_data = data.get("player_ship_setup", {})
        if not ship_setup_data.is_empty():
            player_ship_setup = PlayerShipSetup.new()
            player_ship_setup.deserialize(ship_setup_data)
            
        var stats_data = data.get("statistics", {})
        if not stats_data.is_empty():
            statistics = PlayerStatistics.new()
            statistics.deserialize(stats_data)

# Player statistics tracking
class PlayerStatistics extends Resource:
    @export var missions_completed: int = 0
    @export var missions_failed: int = 0
    @export var enemies_destroyed: int = 0
    @export var friendly_fire_incidents: int = 0
    @export var total_play_time: float = 0.0
    @export var highest_score: int = 0
    @export var longest_mission_time: float = 0.0
    @export var fastest_mission_completion: float = 0.0
    @export var total_ships_flyable_time: float = 0.0
    
    func serialize() -> Dictionary:
        # Serialize statistics to dictionary
        return {
            "missions_completed": missions_completed,
            "missions_failed": missions_failed,
            "enemies_destroyed": enemies_destroyed,
            "friendly_fire_incidents": friendly_fire_incidents,
            "total_play_time": total_play_time,
            "highest_score": highest_score,
            "longest_mission_time": longest_mission_time,
            "fastest_mission_completion": fastest_mission_completion,
            "total_ships_flyable_time": total_ships_flyable_time
        }
        
    func deserialize(data: Dictionary):
        # Deserialize statistics from dictionary
        missions_completed = data.get("missions_completed", missions_completed)
        missions_failed = data.get("missions_failed", missions_failed)
        enemies_destroyed = data.get("enemies_destroyed", enemies_destroyed)
        friendly_fire_incidents = data.get("friendly_fire_incidents", friendly_fire_incidents)
        total_play_time = data.get("total_play_time", total_play_time)
        highest_score = data.get("highest_score", highest_score)
        longest_mission_time = data.get("longest_mission_time", longest_mission_time)
        fastest_mission_completion = data.get("fastest_mission_completion", fastest_mission_completion)
        total_ships_flyable_time = data.get("total_ships_flyable_time", total_ships_flyable_time)
        
    func record_mission_completion(success: bool, mission_time: float, score: int):
        # Record mission completion statistics
        if success:
            missions_completed += 1
        else:
            missions_failed += 1
            
        total_play_time += mission_time
        
        if success:
            # Update completion time records
            if fastest_mission_completion == 0.0 or mission_time < fastest_mission_completion:
                fastest_mission_completion = mission_time
                
            if mission_time > longest_mission_time:
                longest_mission_time = mission_time
                
        # Update score records
        if score > highest_score:
            highest_score = score
            
    func record_ship_destruction(is_enemy: bool, is_friendly: bool):
        # Record ship destruction statistics
        if is_enemy:
            enemies_destroyed += 1
        elif is_friendly:
            friendly_fire_incidents += 1
            
    func record_flight_time(time: float):
        # Record flight time statistics
        total_ships_flyable_time += time
        
    func get_completion_rate() -> float:
        # Return mission completion rate (0.0 to 1.0)
        var total_missions = missions_completed + missions_failed
        if total_missions > 0:
            return float(missions_completed) / float(total_missions)
        return 0.0
        
    func get_kdr() -> float:
        # Return kill/death ratio
        if missions_failed > 0:
            return float(enemies_destroyed) / float(missions_failed)
        elif enemies_destroyed > 0:
            return float(enemies_destroyed)  # Perfect KDR
        return 0.0

# Game input manager for handling input across states
class GameInputManager extends Node:
    # Input actions
    var input_actions: Dictionary = {
        "throttle_up": "ui_up",
        "throttle_down": "ui_down",
        "turn_left": "ui_left",
        "turn_right": "ui_right",
        "pitch_up": "ui_page_up",
        "pitch_down": "ui_page_down",
        "roll_left": "q",
        "roll_right": "e",
        "fire_primary": "mouse_button_1",
        "fire_secondary": "mouse_button_2",
        "cycle_primary": "tab",
        "cycle_secondary": "shift+tab",
        "target_next": "t",
        "target_prev": "shift+t",
        "target_closest": "r",
        "target_reticle": "shift+r",
        "match_target_speed": "m",
        "toggle_auto_pilot": "a",
        "toggle_hud": "ctrl+d",
        "toggle_radar": "ctrl+r",
        "pause_game": "escape",
        "show_objectives": "j",
        "afterburner": "shift",
        "glide": "alt",
        "shield_equalize": "s",
        "shield_transfer": "shift+s",
        "energy_equalize": "e",
        "energy_transfer": "shift+e",
        "increase_shield": "1",
        "increase_weapon": "2",
        "increase_engine": "3",
        "decrease_shield": "ctrl+1",
        "decrease_weapon": "ctrl+2",
        "decrease_engine": "ctrl+3"
    }
    
    # Input states
    var throttle: float = 0.0
    var turn: float = 0.0
    var pitch: float = 0.0
    var roll: float = 0.0
    var fire_primary: bool = false
    var fire_secondary: bool = false
    var afterburner: bool = false
    var glide: bool = false
    var shield_increase: bool = false
    var weapon_increase: bool = false
    var engine_increase: bool = false
    var shield_decrease: bool = false
    var weapon_decrease: bool = false
    var engine_decrease: bool = false
    
    func _ready():
        # Initialize input manager
        initialize_input()
        
    func initialize_input():
        # Set up input map
        setup_input_actions()
        
    func setup_input_actions():
        # Register input actions with Godot's input system
        for action_name in input_actions.keys():
            var input_event = input_actions[action_name]
            # In practice, this would use InputMap to add actions
            # For simplicity, we're using Godot's built-in actions
            
    func _input(event):
        # Handle input events
        handle_input_event(event)
        
    func handle_input_event(event):
        # Handle specific input events
        if event is InputEventKey:
            handle_key_event(event)
        elif event is InputEventMouseButton:
            handle_mouse_button_event(event)
        elif event is InputEventJoypadButton:
            handle_joystick_button_event(event)
        elif event is InputEventJoypadMotion:
            handle_joystick_motion_event(event)
            
    func handle_key_event(key_event: InputEventKey):
        # Handle keyboard input
        if key_event.pressed:
            # Handle key press
            pass
        else:
            # Handle key release
            pass
            
    func handle_mouse_button_event(mouse_event: InputEventMouseButton):
        # Handle mouse button input
        pass
        
    func handle_joystick_button_event(joy_event: InputEventJoypadButton):
        # Handle joystick button input
        pass
        
    func handle_joystick_motion_event(joy_event: InputEventJoypadMotion):
        # Handle joystick axis input
        pass
        
    func update_input_state():
        # Update input state based on current input
        throttle = Input.get_action_strength("throttle_up") - Input.get_action_strength("throttle_down")
        turn = Input.get_action_strength("turn_right") - Input.get_action_strength("turn_left")
        pitch = Input.get_action_strength("pitch_down") - Input.get_action_strength("pitch_up")
        roll = Input.get_action_strength("roll_right") - Input.get_action_strength("roll_left")
        
        fire_primary = Input.is_action_pressed("fire_primary")
        fire_secondary = Input.is_action_pressed("fire_secondary")
        afterburner = Input.is_action_pressed("afterburner")
        glide = Input.is_action_pressed("glide")
        
        shield_increase = Input.is_action_just_pressed("increase_shield")
        weapon_increase = Input.is_action_just_pressed("increase_weapon")
        engine_increase = Input.is_action_just_pressed("increase_engine")
        shield_decrease = Input.is_action_just_pressed("decrease_shield")
        weapon_decrease = Input.is_action_just_pressed("decrease_weapon")
        engine_decrease = Input.is_action_just_pressed("decrease_engine")
        
    func get_throttle() -> float:
        return throttle
        
    func get_turn() -> float:
        return turn
        
    func get_pitch() -> float:
        return pitch
        
    func get_roll() -> float:
        return roll
        
    func is_firing_primary() -> bool:
        return fire_primary
        
    func is_firing_secondary() -> bool:
        return fire_secondary
        
    func is_afterburner_active() -> bool:
        return afterburner
        
    func is_gliding_active() -> bool:
        return glide
        
    func should_increase_shield() -> bool:
        return shield_increase
        
    func should_increase_weapon() -> bool:
        return weapon_increase
        
    func should_increase_engine() -> bool:
        return engine_increase
        
    func should_decrease_shield() -> bool:
        return shield_decrease
        
    func should_decrease_weapon() -> bool:
        return weapon_decrease
        
    func should_decrease_engine() -> bool:
        return engine_decrease
        
    func remap_action(action_name: String, new_input: String):
        # Remap input action
        if input_actions.has(action_name):
            input_actions[action_name] = new_input
            # Update InputMap
            # This would require actual InputMap manipulation
            
    func save_input_config():
        # Save input configuration
        # This would save the current input mapping

# Difficulty profiles for gameplay scaling
class DifficultyProfile extends Resource:
    @export var name: String = "Normal"
    @export var description: String = "Standard difficulty level"
    @export var ai_accuracy: float = 1.0  # 0.0 to 2.0
    @export var ai_evasion: float = 1.0  # 0.0 to 2.0
    @export var ai_courage: float = 1.0  # 0.0 to 2.0
    @export var player_shield_regen: float = 1.0  # Shield regeneration multiplier
    @export var player_weapon_regen: float = 1.0  # Weapon energy regeneration
    @export var player_damage_taken: float = 1.0  # Damage multiplier for player
    @export var enemy_damage_given: float = 1.0  # Damage multiplier for enemies
    @export var spawn_rate_multiplier: float = 1.0  # Enemy spawn rate
    @export var reinforcement_delay: float = 1.0  # Reinforcement arrival delay multiplier
    @export var hint_frequency: float = 1.0  # Frequency of tutorial hints
    
    func _init():
        resource_name = name
        
    func apply_to_ai(ai_controller: AIController):
        # Apply difficulty modifiers to AI controller
        if ai_controller.aiProfile != null:
            ai_controller.aiProfile.accuracy *= ai_accuracy
            ai_controller.aiProfile.evasion *= ai_evasion
            ai_controller.aiProfile.courage *= ai_courage
            
    func apply_to_player(player_ship: Ship):
        # Apply difficulty modifiers to player ship
        # This would modify player ship properties
        pass
        
    func get_modified_damage(damage: float, is_player: bool) -> float:
        # Get damage modified by difficulty settings
        if is_player:
            return damage * player_damage_taken
        else:
            return damage * enemy_damage_given
            
    func get_modified_shield_regen(regen: float) -> float:
        # Get shield regeneration modified by difficulty
        return regen * player_shield_regen
        
    func get_modified_weapon_regen(regen: float) -> float:
        # Get weapon energy regeneration modified by difficulty
        return regen * player_weapon_regen

# Difficulty manager for handling game difficulty
class DifficultyManager extends Node:
    var current_difficulty: DifficultyProfile = null
    var difficulty_profiles: Dictionary = {}
    
    func _ready():
        # Initialize difficulty profiles
        initialize_difficulty_profiles()
        set_difficulty("Normal")
        
    func initialize_difficulty_profiles():
        # Create default difficulty profiles
        var easy = DifficultyProfile.new()
        easy.name = "Easy"
        easy.description = "Reduced enemy difficulty, enhanced player survivability"
        easy.ai_accuracy = 0.7
        easy.ai_evasion = 0.7
        easy.ai_courage = 0.7
        easy.player_shield_regen = 1.5
        easy.player_weapon_regen = 1.5
        easy.player_damage_taken = 0.7
        easy.enemy_damage_given = 0.7
        difficulty_profiles["Easy"] = easy
        
        var normal = DifficultyProfile.new()
        normal.name = "Normal"
        normal.description = "Standard difficulty level"
        normal.ai_accuracy = 1.0
        normal.ai_evasion = 1.0
        normal.ai_courage = 1.0
        normal.player_shield_regen = 1.0
        normal.player_weapon_regen = 1.0
        normal.player_damage_taken = 1.0
        normal.enemy_damage_given = 1.0
        difficulty_profiles["Normal"] = normal
        
        var hard = DifficultyProfile.new()
        hard.name = "Hard"
        hard.description = "Increased enemy difficulty, reduced player advantages"
        hard.ai_accuracy = 1.3
        hard.ai_evasion = 1.3
        hard.ai_courage = 1.3
        hard.player_shield_regen = 0.7
        hard.player_weapon_regen = 0.7
        hard.player_damage_taken = 1.3
        hard.enemy_damage_given = 1.3
        difficulty_profiles["Hard"] = hard
        
        var insane = DifficultyProfile.new()
        insane.name = "Insane"
        insane.description = "Maximum challenge, minimal player advantages"
        insane.ai_accuracy = 1.5
        insane.ai_evasion = 1.5
        insane.ai_courage = 1.5
        insane.player_shield_regen = 0.5
        insane.player_weapon_regen = 0.5
        insane.player_damage_taken = 1.5
        insane.enemy_damage_given = 1.5
        difficulty_profiles["Insane"] = insane
        
    func set_difficulty(difficulty_name: String):
        # Set current difficulty profile
        if difficulty_profiles.has(difficulty_name):
            current_difficulty = difficulty_profiles[difficulty_name]
        else:
            current_difficulty = difficulty_profiles["Normal"]
            
    func get_difficulty() -> DifficultyProfile:
        # Get current difficulty profile
        return current_difficulty
        
    func get_difficulty_names() -> Array:
        # Get list of available difficulty names
        return difficulty_profiles.keys()
        
    func get_difficulty_description(difficulty_name: String) -> String:
        # Get description for difficulty
        if difficulty_profiles.has(difficulty_name):
            return difficulty_profiles[difficulty_name].description
        return ""

# Campaign manager for handling campaign progression
class CampaignManager extends Node:
    var current_campaign: Campaign = null
    var campaigns: Dictionary = {}
    var is_campaign_active: bool = false
    
    func _ready():
        # Initialize campaign manager
        initialize_campaigns()
        
    func initialize_campaigns():
        # Load available campaigns
        load_campaigns()
        
    func load_campaigns():
        # Load campaign resources
        var campaign_files = get_campaign_files()
        for file_path in campaign_files:
            var campaign = load(file_path)
            if campaign is Campaign:
                campaigns[campaign.name] = campaign
                
    func get_campaign_files() -> Array:
        # Return list of campaign file paths
        return [
            "res://campaigns/hermes_campaign.tres",
            "res://campaigns/demo_campaign.tres"
        ]
        
    func start_campaign(campaign_name: String, pilot_name: String) -> bool:
        # Start a new campaign
        if campaigns.has(campaign_name):
            current_campaign = campaigns[campaign_name]
            is_campaign_active = true
            
            # Initialize campaign state
            if current_campaign.playerProgress == null:
                current_campaign.playerProgress = PlayerProgress.new()
                
            # Set pilot name
            current_campaign.playerProgress.pilot_name = pilot_name
            
            return true
        return false
        
    func load_campaign(save_slot: int) -> bool:
        # Load campaign from save slot
        # This would interface with the save system
        return false
        
    func get_current_campaign() -> Campaign:
        # Get current campaign
        return current_campaign
        
    func get_campaign_names() -> Array:
        # Get list of available campaign names
        return campaigns.keys()
        
    func get_campaign_description(campaign_name: String) -> String:
        # Get campaign description
        if campaigns.has(campaign_name):
            return campaigns[campaign_name].description
        return ""
        
    func advance_to_next_mission() -> String:
        # Advance campaign to next mission
        if current_campaign != null:
            return current_campaign.get_next_mission()
        return ""
        
    func is_mission_available(mission_name: String) -> bool:
        # Check if mission is available in current campaign
        if current_campaign != null:
            return current_campaign.is_mission_available(mission_name)
        return false
        
    func complete_mission(mission_name: String, success: bool):
        # Record mission completion in campaign
        if current_campaign != null:
            current_campaign.complete_mission(mission_name, success)
            
    func is_campaign_complete() -> bool:
        # Check if current campaign is complete
        if current_campaign != null:
            # Check if all required missions are complete
            return false  # Simplified for example
        return false
        
    func get_available_missions() -> Array:
        # Get list of currently available missions
        if current_campaign != null:
            var available = []
            for mission in current_campaign.missions:
                if current_campaign.is_mission_available(mission.missionName):
                    available.append(mission.missionName)
            return available
        return []
        
    func unlock_ship_class(ship_class_name: String):
        # Unlock ship class for player
        if current_campaign != null and current_campaign.playerProgress != null:
            if not current_campaign.playerProgress.shipsUnlocked.has(ship_class_name):
                current_campaign.playerProgress.shipsUnlocked.append(ship_class_name)
                
    func unlock_weapon(weapon_name: String):
        # Unlock weapon for player
        if current_campaign != null and current_campaign.playerProgress != null:
            if not current_campaign.playerProgress.weaponsUnlocked.has(weapon_name):
                current_campaign.playerProgress.weaponsUnlocked.append(weapon_name)
                
    func earn_medal(medal_name: String):
        # Earn medal for player
        if current_campaign != null and current_campaign.playerProgress != null:
            if not current_campaign.playerProgress.medalsEarned.has(medal_name):
                current_campaign.playerProgress.medalsEarned.append(medal_name)
                
    func get_player_progress() -> PlayerProgress:
        # Get current player progress
        if current_campaign != null:
            return current_campaign.playerProgress
        return null
```

### TRES Resources
```ini
[gd_resource type="Resource" load_steps=2 format=2]

[resource]
resource_name = "Normal_Difficulty_Profile"
name = "Normal"
description = "Standard difficulty level"
ai_accuracy = 1.0
ai_evasion = 1.0
ai_courage = 1.0
player_shield_regen = 1.0
player_weapon_regen = 1.0
player_damage_taken = 1.0
enemy_damage_given = 1.0
spawn_rate_multiplier = 1.0
reinforcement_delay = 1.0
hint_frequency = 1.0

[gd_resource type="Resource" load_steps=2 format=2]

[resource]
resource_name = "Default_Game_Configuration"
graphics_resolution = Vector2(1920, 1080)
graphics_fullscreen = true
graphics_vsync = true
graphics_quality = "high"
graphics_brightness = 1.0
graphics_contrast = 1.0
audio_master_volume = 1.0
audio_music_volume = 0.8
audio_sfx_volume = 1.0
audio_voice_volume = 1.0
audio_enable_3d = true
control_mouse_sensitivity = 1.0
control_invert_y = false
control_use_joystick = false
gameplay_difficulty = "normal"
gameplay_auto_pilot = false
gameplay_show_hud = true
gameplay_show_radar = true
multiplayer_name = "Blair"
multiplayer_port = 7808
multiplayer_server = "localhost"
```

### TSCN Scenes
```ini
[gd_scene load_steps=4 format=2]

[ext_resource path="res://scripts/game_state_manager.gd" type="Script" id=1]
[ext_resource path="res://resources/default_config.tres" type="Resource" id=2]
[ext_resource path="res://scenes/main_menu.tscn" type="PackedScene" id=3]

[node name="GameStateManager" type="Node"]
script = ExtResource(1)
config_manager = ExtResource(2)

[node name="MainMenu" type="Node" parent="."]
instance = ExtResource(3)

[node name="AudioManager" type="Node" parent="."]
script = "res://scripts/audio_manager.gd"

[node name="UIManager" type="Node" parent="."]
script = "res://scripts/ui_manager.gd"
```

### Implementation Notes
The Game State Module in Godot leverages:

1. **Singleton Pattern**: GameStateManager as global singleton using Godot's autoload system
2. **State Machine**: Robust state management with enter/leave state callbacks
3. **Event System**: Queue-based event processing with delayed state changes
4. **Resource System**: Configuration and difficulty profiles as data-driven resources
5. **Scene System**: State transitions using scene switching
6. **Input System**: Integrated input handling with remappable controls
7. **Save System**: Persistent save game management with metadata
8. **Configuration Management**: Flexible settings system with file persistence

This replaces the C++ game sequence system with Godot's node-based approach while preserving the same state management functionality. The implementation uses Godot's scene tree for state transitions and the resource system for configuration management.

The event system provides decoupled communication between systems, and the input manager handles cross-state input mapping. The save system provides persistent player progress, and the difficulty system scales gameplay appropriately.

The campaign manager handles mission sequencing and progression, while the difficulty manager adjusts gameplay balance. The configuration manager provides a centralized settings system that persists between sessions.

The implementation uses Godot's built-in systems for most functionality, reducing the need for custom implementations while maintaining the same overall architecture and gameplay flow.