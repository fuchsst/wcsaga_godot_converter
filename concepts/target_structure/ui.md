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

## Godot Implementation Details

### Native GDScript Classes
```gdscript
# UI manager for handling all UI screens and systems
class UIManager extends Node:
    # UI system components
    var hud_system: HUDSystem = null
    var radar_system: RadarSystem = null
    var message_system: MessageSystem = null
    var tech_database: TechDatabase = null
    var fiction_viewer: FictionViewer = null
    var cutscene_player: CutscenePlayer = null
    var loading_screen: LoadingScreen = null
    
    # Screen management
    var current_screen: Control = null
    var screen_stack: Array[Control] = []
    var screens: Dictionary = {}
    
    # UI state
    var is_ui_visible: bool = true
    var ui_scale: float = 1.0
    var ui_theme: Theme = null
    
    # Signals
    signal screen_changed(old_screen, new_screen)
    signal ui_visibility_changed(visible)
    signal hud_element_added(element)
    signal hud_element_removed(element)
    
    func _ready():
        # Initialize UI manager
        initialize()
        
    func _process(delta):
        # Update UI systems
        update_ui_systems(delta)
        
    func initialize():
        # Initialize UI systems
        initialize_ui_systems()
        
        # Load UI theme
        load_ui_theme()
        
        # Create base UI screens
        create_base_screens()
        
    func initialize_ui_systems():
        # Initialize HUD system
        hud_system = HUDSystem.new()
        add_child(hud_system)
        
        # Initialize radar system
        radar_system = RadarSystem.new()
        add_child(radar_system)
        
        # Initialize message system
        message_system = MessageSystem.new()
        add_child(message_system)
        
        # Initialize tech database
        tech_database = TechDatabase.new()
        add_child(tech_database)
        
        # Initialize fiction viewer
        fiction_viewer = FictionViewer.new()
        add_child(fiction_viewer)
        
        # Initialize cutscene player
        cutscene_player = CutscenePlayer.new()
        add_child(cutscene_player)
        
        # Initialize loading screen
        loading_screen = LoadingScreen.new()
        add_child(loading_screen)
        
    func load_ui_theme():
        # Load UI theme from resources
        ui_theme = preload("res://ui/themes/default_theme.tres")
        
    func create_base_screens():
        # Create and register base UI screens
        screens["MainMenu"] = preload("res://ui/screens/main_menu.tscn").instantiate()
        screens["OptionsMenu"] = preload("res://ui/screens/options_menu.tscn").instantiate()
        screens["CampaignMenu"] = preload("res://ui/screens/campaign_menu.tscn").instantiate()
        screens["TrainingMenu"] = preload("res://ui/screens/training_menu.tscn").instantiate()
        screens["TechMenu"] = preload("res://ui/screens/tech_menu.tscn").instantiate()
        screens["Briefing"] = preload("res://ui/screens/briefing_screen.tscn").instantiate()
        screens["Debriefing"] = preload("res://ui/screens/debriefing_screen.tscn").instantiate()
        screens["PauseMenu"] = preload("res://ui/screens/pause_menu.tscn").instantiate()
        screens["Loading"] = loading_screen
        screens["FictionViewer"] = fiction_viewer
        screens["CutscenePlayer"] = cutscene_player
        screens["TechDatabase"] = tech_database
        
        # Add screens to scene tree
        for screen_name in screens.keys():
            var screen = screens[screen_name]
            if screen != null:
                add_child(screen)
                screen.hide()
                
    func show_screen(screen_name: String):
        # Show specified UI screen
        if screens.has(screen_name):
            var new_screen = screens[screen_name]
            if new_screen != current_screen:
                # Hide current screen
                if current_screen != null:
                    hide_current_screen()
                    
                # Show new screen
                current_screen = new_screen
                current_screen.show()
                
                # Emit screen changed signal
                emit_signal("screen_changed", null, current_screen)
                
    func hide_current_screen():
        # Hide current UI screen
        if current_screen != null:
            current_screen.hide()
            current_screen = null
            
    func push_screen(screen_name: String):
        # Push current screen to stack and show new one
        if current_screen != null:
            screen_stack.push_back(current_screen)
            
        show_screen(screen_name)
        
    func pop_screen():
        # Return to previous screen in stack
        if not screen_stack.is_empty():
            var previous_screen = screen_stack.pop_back()
            if previous_screen != null:
                # Hide current screen
                if current_screen != null:
                    current_screen.hide()
                    
                # Show previous screen
                current_screen = previous_screen
                current_screen.show()
                
                # Emit screen changed signal
                emit_signal("screen_changed", null, current_screen)
                
    func hide_screen(screen_name: String):
        # Hide specified UI screen
        if screens.has(screen_name):
            var screen = screens[screen_name]
            if screen != null and screen.visible:
                screen.hide()
                if current_screen == screen:
                    current_screen = null
                    
    func is_screen_active(screen_name: String) -> bool:
        # Check if specified screen is currently active
        if screens.has(screen_name):
            var screen = screens[screen_name]
            return screen != null and screen.visible
        return false
        
    func get_current_screen() -> Control:
        # Get currently active screen
        return current_screen
        
    func get_screen(screen_name: String) -> Control:
        # Get specified screen
        return screens.get(screen_name, null)
        
    func show_hud():
        # Show HUD system
        if hud_system != null:
            hud_system.show_hud()
            
    func hide_hud():
        # Hide HUD system
        if hud_system != null:
            hud_system.hide_hud()
            
    func toggle_hud():
        # Toggle HUD visibility
        if hud_system != null:
            hud_system.toggle_hud()
            
    func is_hud_visible() -> bool:
        # Check if HUD is currently visible
        if hud_system != null:
            return hud_system.is_visible()
        return false
        
    func update_ui_systems(delta):
        # Update all active UI systems
        if hud_system != null:
            hud_system.update_hud(delta)
            
        if radar_system != null:
            radar_system.update_radar(delta)
            
        if message_system != null:
            message_system.update_messages(delta)
            
    func set_player_ship(player_ship: Ship):
        # Set player ship for UI systems
        if hud_system != null:
            hud_system.set_player_ship(player_ship)
            
        if radar_system != null:
            radar_system.set_player_ship(player_ship)
            
        if message_system != null:
            message_system.set_player_ship(player_ship)
            
    func add_message(message: String, message_type: MessageType = MessageType.INFO, 
                     duration: float = 3.0, color: Color = Color.WHITE):
        # Add message to message system
        if message_system != null:
            message_system.add_message(message, message_type, duration, color)
            
    func show_loading_screen(loading_text: String = "Loading..."):
        # Show loading screen with text
        if loading_screen != null:
            loading_screen.set_loading_text(loading_text)
            show_screen("Loading")
            
    func update_loading_progress(progress: float, status_text: String = ""):
        # Update loading progress
        if loading_screen != null:
            loading_screen.update_progress(progress, status_text)
            
    func hide_loading_screen():
        # Hide loading screen
        hide_screen("Loading")
        
    func show_briefing(mission: Mission):
        # Show mission briefing
        if screens.has("Briefing"):
            var briefing_screen = screens["Briefing"] as BriefingScreen
            if briefing_screen != null:
                briefing_screen.set_mission(mission)
                show_screen("Briefing")
                
    func show_debriefing(mission: Mission, success: bool, statistics: Dictionary):
        # Show mission debriefing
        if screens.has("Debriefing"):
            var debriefing_screen = screens["Debriefing"] as DebriefingScreen
            if debriefing_screen != null:
                debriefing_screen.set_mission_result(mission, success, statistics)
                show_screen("Debriefing")
                
    func show_fiction(fiction_file: String):
        # Show fiction viewer with specified file
        if fiction_viewer != null:
            fiction_viewer.load_fiction_file(fiction_file)
            show_screen("FictionViewer")
            
    func show_cutscene(cutscene_file: String):
        # Show cutscene player with specified file
        if cutscene_player != null:
            cutscene_player.load_cutscene(cutscene_file)
            show_screen("CutscenePlayer")
            
    func show_tech_entry(entry_type: String, entry_name: String):
        # Show tech database entry
        if tech_database != null:
            tech_database.show_entry(entry_type, entry_name)
            show_screen("TechDatabase")
            
    func set_ui_scale(scale: float):
        # Set UI scale factor
        ui_scale = clamp(scale, 0.5, 2.0)
        
        # Apply scale to all UI elements
        for screen in screens.values():
            if screen != null:
                screen.scale = Vector2(ui_scale, ui_scale)
                
    func get_ui_scale() -> float:
        # Get current UI scale
        return ui_scale
        
    func set_ui_theme(theme: Theme):
        # Set UI theme
        ui_theme = theme
        
        # Apply theme to all screens
        for screen in screens.values():
            if screen != null:
                screen.theme = theme
                
    func get_ui_theme() -> Theme:
        # Get current UI theme
        return ui_theme
        
    func set_ui_visibility(visible: bool):
        # Set overall UI visibility
        is_ui_visible = visible
        
        # Update HUD visibility
        if hud_system != null:
            if visible:
                hud_system.show_hud()
            else:
                hud_system.hide_hud()
                
        # Update screen visibility
        if current_screen != null:
            current_screen.visible = visible
            
        # Emit visibility changed signal
        emit_signal("ui_visibility_changed", visible)
        
    func is_ui_visible() -> bool:
        # Check if UI is currently visible
        return is_ui_visible
        
    func cleanup():
        # Clean up UI systems
        if hud_system != null:
            hud_system.cleanup()
            
        if radar_system != null:
            radar_system.cleanup()
            
        if message_system != null:
            message_system.cleanup()
            
        if tech_database != null:
            tech_database.cleanup()
            
        if fiction_viewer != null:
            fiction_viewer.cleanup()
            
        if cutscene_player != null:
            cutscene_player.cleanup()

# HUD system for in-game information display
class HUDSystem extends CanvasLayer:
    # HUD elements
    var hull_bar: ProgressBar = null
    var shield_bar: ProgressBar = null
    var weapon_display: WeaponDisplay = null
    var target_display: TargetDisplay = null
    var comm_display: CommunicationDisplay = null
    var objective_display: ObjectiveDisplay = null
    var energy_display: EnergyDisplay = null
    var subsystem_display: SubsystemDisplay = null
    var countermeasure_display: CountermeasureDisplay = null
    var wingman_display: WingmanDisplay = null
    var afterburner_display: AfterburnerDisplay = null
    var glide_display: GlideDisplay = null
    var auto_pilot_display: AutoPilotDisplay = null
    var missile_lock_display: MissileLockDisplay = null
    var damage_indicator: DamageIndicator = null
    var reticle: Reticle = null
    var speed_indicator: SpeedIndicator = null
    var altitude_indicator: AltitudeIndicator = null
    
    # Player reference
    var player_ship: Ship = null
    
    # HUD state
    var is_hud_active: bool = true
    var show_full_hud: bool = true
    var hud_elements: Array[Control] = []
    
    # HUD settings
    var hud_color: Color = Color.WHITE
    var hud_alpha: float = 1.0
    var hud_scale: float = 1.0
    var show_damage_flash: bool = true
    var show_targeting: bool = true
    var show_wingmen: bool = true
    var show_communications: bool = true
    
    func _ready():
        # Initialize HUD system
        initialize_hud()
        
    func _process(delta):
        # Update HUD elements
        if is_hud_active and player_ship != null:
            update_hud_elements(delta)
            
    func initialize_hud():
        # Create HUD elements
        create_hud_elements()
        
        # Set initial visibility
        set_hud_visibility(true)
        
    func create_hud_elements():
        # Create and initialize HUD elements
        hull_bar = preload("res://ui/hud/elements/hull_bar.tscn").instantiate()
        add_child(hull_bar)
        hud_elements.append(hull_bar)
        
        shield_bar = preload("res://ui/hud/elements/shield_bar.tscn").instantiate()
        add_child(shield_bar)
        hud_elements.append(shield_bar)
        
        weapon_display = preload("res://ui/hud/elements/weapon_display.tscn").instantiate()
        add_child(weapon_display)
        hud_elements.append(weapon_display)
        
        target_display = preload("res://ui/hud/elements/target_display.tscn").instantiate()
        add_child(target_display)
        hud_elements.append(target_display)
        
        comm_display = preload("res://ui/hud/elements/communication_display.tscn").instantiate()
        add_child(comm_display)
        hud_elements.append(comm_display)
        
        objective_display = preload("res://ui/hud/elements/objective_display.tscn").instantiate()
        add_child(objective_display)
        hud_elements.append(objective_display)
        
        energy_display = preload("res://ui/hud/elements/energy_display.tscn").instantiate()
        add_child(energy_display)
        hud_elements.append(energy_display)
        
        subsystem_display = preload("res://ui/hud/elements/subsystem_display.tscn").instantiate()
        add_child(subsystem_display)
        hud_elements.append(subsystem_display)
        
        countermeasure_display = preload("res://ui/hud/elements/countermeasure_display.tscn").instantiate()
        add_child(countermeasure_display)
        hud_elements.append(countermeasure_display)
        
        wingman_display = preload("res://ui/hud/elements/wingman_display.tscn").instantiate()
        add_child(wingman_display)
        hud_elements.append(wingman_display)
        
        afterburner_display = preload("res://ui/hud/elements/afterburner_display.tscn").instantiate()
        add_child(afterburner_display)
        hud_elements.append(afterburner_display)
        
        glide_display = preload("res://ui/hud/elements/glide_display.tscn").instantiate()
        add_child(glide_display)
        hud_elements.append(glide_display)
        
        auto_pilot_display = preload("res://ui/hud/elements/auto_pilot_display.tscn").instantiate()
        add_child(auto_pilot_display)
        hud_elements.append(auto_pilot_display)
        
        missile_lock_display = preload("res://ui/hud/elements/missile_lock_display.tscn").instantiate()
        add_child(missile_lock_display)
        hud_elements.append(missile_lock_display)
        
        damage_indicator = preload("res://ui/hud/elements/damage_indicator.tscn").instantiate()
        add_child(damage_indicator)
        hud_elements.append(damage_indicator)
        
        reticle = preload("res://ui/hud/elements/reticle.tscn").instantiate()
        add_child(reticle)
        hud_elements.append(reticle)
        
        speed_indicator = preload("res://ui/hud/elements/speed_indicator.tscn").instantiate()
        add_child(speed_indicator)
        hud_elements.append(speed_indicator)
        
        altitude_indicator = preload("res://ui/hud/elements/altitude_indicator.tscn").instantiate()
        add_child(altitude_indicator)
        hud_elements.append(altitude_indicator)
        
    func update_hud_elements(delta):
        # Update all HUD elements with current player data
        if player_ship != null:
            # Update hull and shield bars
            var hull_percent = player_ship.hullStrength / player_ship.shipClass.maxHullStrength
            var shield_percent = player_ship.shieldStrength / player_ship.shipClass.maxShieldStrength
            
            hull_bar.value = hull_percent * 100
            shield_bar.value = shield_percent * 100
            
            # Update weapon display
            if weapon_display != null and player_ship.weaponSystem != null:
                weapon_display.update_weapons(player_ship.weaponSystem)
                
            # Update energy display
            if energy_display != null:
                energy_display.update_energy(player_ship.energyLevels)
                
            # Update subsystem display
            if subsystem_display != null:
                subsystem_display.update_subsystems(player_ship.subsystems)
                
            # Update speed indicator
            if speed_indicator != null and player_ship.physicsController != null:
                speed_indicator.set_speed(player_ship.physicsController.get_velocity_magnitude())
                
            # Update afterburner/glide displays
            if afterburner_display != null and player_ship.physicsController != null:
                afterburner_display.set_active(player_ship.physicsController.is_afterburner_active)
                
            if glide_display != null and player_ship.physicsController != null:
                glide_display.set_active(player_ship.physicsController.is_gliding)
                
            # Update auto-pilot display
            if auto_pilot_display != null:
                auto_pilot_display.set_active(player_ship.is_auto_pilot_active)
                
            # Update missile lock display
            if missile_lock_display != null:
                missile_lock_display.update_locks(player_ship.get_missile_locks())
                
        # Update target display with current target
        if target_display != null:
            target_display.update_target(get_current_target())
            
        # Update wingman display
        if wingman_display != null:
            wingman_display.update_wingmen(get_wingmen())
            
        # Update communications
        if comm_display != null:
            comm_display.update_communications(get_recent_communications())
            
        # Update objectives
        if objective_display != null:
            objective_display.update_objectives(get_current_objectives())
            
        # Update countermeasures
        if countermeasure_display != null and player_ship != null:
            countermeasure_display.update_countermeasures(player_ship.countermeasures)
            
    func get_current_target() -> Node3D:
        # Get current player target (would interface with targeting system)
        if player_ship != null:
            return player_ship.currentTarget
        return null
        
    func get_wingmen() -> Array[Ship]:
        # Get player's wingmen
        if player_ship != null and player_ship.wing != null:
            return player_ship.wing.spawnedShips
        return []
        
    func get_recent_communications() -> Array[CommunicationMessage]:
        # Get recent communications (would interface with comm system)
        return []
        
    func get_current_objectives() -> Array[MissionObjective]:
        # Get current mission objectives (would interface with mission system)
        return []
        
    func set_player_ship(ship: Ship):
        # Set player ship reference
        player_ship = ship
        
        # Update HUD elements with player ship
        for element in hud_elements:
            if element.has_method("set_player_ship"):
                element.set_player_ship(ship)
                
    func show_hud():
        # Show HUD elements
        is_hud_active = true
        set_hud_visibility(true)
        
    func hide_hud():
        # Hide HUD elements
        is_hud_active = false
        set_hud_visibility(false)
        
    func toggle_hud():
        # Toggle HUD visibility
        if is_hud_active:
            hide_hud()
        else:
            show_hud()
            
    func set_hud_visibility(visible: bool):
        # Set visibility of all HUD elements
        for element in hud_elements:
            element.visible = visible and is_hud_active
            
    func is_visible() -> bool:
        # Check if HUD is visible
        return is_hud_active and visible
        
    func set_hud_color(color: Color):
        # Set HUD color
        hud_color = color
        
        # Apply to all elements
        for element in hud_elements:
            if element is ColorRect or element is Label:
                element.modulate = color
                
    func set_hud_alpha(alpha: float):
        # Set HUD alpha/transparency
        hud_alpha = clamp(alpha, 0.0, 1.0)
        
        # Apply to all elements
        for element in hud_elements:
            var current_modulate = element.modulate
            element.modulate = Color(current_modulate.r, current_modulate.g, current_modulate.b, alpha)
            
    func set_hud_scale(scale: float):
        # Set HUD scale
        hud_scale = clamp(scale, 0.5, 2.0)
        
        # Apply to all elements
        for element in hud_elements:
            element.scale = Vector2(scale, scale)
            
    func set_hud_setting(setting: String, value):
        # Set HUD setting
        match setting:
            "show_damage_flash":
                show_damage_flash = value
                if damage_indicator != null:
                    damage_indicator.visible = value
                    
            "show_targeting":
                show_targeting = value
                if target_display != null:
                    target_display.visible = value
                    
            "show_wingmen":
                show_wingmen = value
                if wingman_display != null:
                    wingman_display.visible = value
                    
            "show_communications":
                show_communications = value
                if comm_display != null:
                    comm_display.visible = value
                    
            "full_hud":
                show_full_hud = value
                # Show/hide optional elements
                set_optional_elements_visibility(value)
                
    func set_optional_elements_visibility(visible: bool):
        # Set visibility of optional HUD elements
        if target_display != null:
            target_display.visible = visible and show_targeting
            
        if comm_display != null:
            comm_display.visible = visible and show_communications
            
        if wingman_display != null:
            wingman_display.visible = visible and show_wingmen
            
        if objective_display != null:
            objective_display.visible = visible
            
        if energy_display != null:
            energy_display.visible = visible
            
        if subsystem_display != null:
            subsystem_display.visible = visible
            
        if countermeasure_display != null:
            countermeasure_display.visible = visible
            
        if afterburner_display != null:
            afterburner_display.visible = visible
            
        if glide_display != null:
            glide_display.visible = visible
            
        if auto_pilot_display != null:
            auto_pilot_display.visible = visible
            
        if missile_lock_display != null:
            missile_lock_display.visible = visible
            
    func show_damage_flash(damage_type: String, damage_amount: float):
        # Show damage flash effect
        if show_damage_flash and damage_indicator != null:
            damage_indicator.show_damage_flash(damage_type, damage_amount)
            
    func show_target_lock(target: Node3D):
        # Show target lock indicator
        if show_targeting and target_display != null:
            target_display.show_target_lock(target)
            
    func show_missile_lock(lock_level: int):
        # Show missile lock indicator
        if missile_lock_display != null:
            missile_lock_display.show_lock(lock_level)
            
    func update_hud(delta):
        # Update HUD systems
        if is_hud_active:
            # Update damage indicator
            if damage_indicator != null:
                damage_indicator.update(delta)
                
            # Update weapon display cooldowns
            if weapon_display != null:
                weapon_display.update_cooldowns(delta)
                
            # Update targeting display
            if target_display != null:
                target_display.update_targeting(delta)
                
    func add_hud_element(element: Control):
        # Add custom HUD element
        if element != null:
            add_child(element)
            hud_elements.append(element)
            emit_signal("hud_element_added", element)
            
    func remove_hud_element(element: Control):
        # Remove custom HUD element
        if element != null and hud_elements.has(element):
            hud_elements.erase(element)
            element.queue_free()
            emit_signal("hud_element_removed", element)
            
    func cleanup():
        # Clean up HUD system
        for element in hud_elements:
            if element != null:
                element.queue_free()
                
        hud_elements.clear()
        player_ship = null

# Radar system for tactical object tracking
class RadarSystem extends Control:
    # Radar properties
    var radar_range: float = 10000.0
    var radar_scale: float = 1.0
    var radar_contacts: Array[RadarContact] = []
    var player_ship: Ship = null
    var show_friendly: bool = true
    var show_hostile: bool = true
    var show_neutral: bool = true
    var show_asteroids: bool = true
    var show_waypoints: bool = true
    var show_targets_only: bool = false
    var radar_mode: RadarMode = RadarMode.TACTICAL
    
    # Radar display
    var radar_background: TextureRect = null
    var contact_container: Node2D = null
    var selected_contact_indicator: TextureRect = null
    var range_indicator: Label = null
    
    # Radar settings
    var show_contact_names: bool = false
    var show_contact_distances: bool = true
    var show_contact_velocities: bool = false
    var contact_size: float = 4.0
    var contact_alpha: float = 0.8
    var show_grid: bool = true
    var grid_color: Color = Color(0, 0.5, 1, 0.3)
    
    enum RadarMode { TACTICAL, LONG_RANGE, NEBULA }
    enum ContactType { FRIENDLY, HOSTILE, NEUTRAL, ASTEROID, WAYPOINT, UNKNOWN }
    
    func _ready():
        # Initialize radar system
        initialize_radar()
        
    func _draw():
        # Draw radar background and grid
        draw_radar_background()
        if show_grid:
            draw_radar_grid()
            
    func initialize_radar():
        # Create radar display elements
        create_radar_display()
        
        # Set initial range indicator
        update_range_indicator()
        
    func create_radar_display():
        # Create radar background
        radar_background = TextureRect.new()
        radar_background.texture = preload("res://ui/radar/background.png")
        radar_background.anchor_right = 1.0
        radar_background.anchor_bottom = 1.0
        add_child(radar_background)
        
        # Create contact container
        contact_container = Node2D.new()
        add_child(contact_container)
        
        # Create selected contact indicator
        selected_contact_indicator = TextureRect.new()
        selected_contact_indicator.texture = preload("res://ui/radar/selected_contact.png")
        selected_contact_indicator.visible = false
        add_child(selected_contact_indicator)
        
        # Create range indicator
        range_indicator = Label.new()
        range_indicator.align = HORIZONTAL_ALIGNMENT_RIGHT
        range_indicator.vertical_alignment = VERTICAL_ALIGNMENT_BOTTOM
        range_indicator.anchor_right = 1.0
        range_indicator.anchor_bottom = 1.0
        range_indicator.offset_left = -100
        range_indicator.offset_top = -30
        range_indicator.offset_right = -10
        range_indicator.offset_bottom = -10
        add_child(range_indicator)
        
    func update_radar(delta):
        # Update radar contacts and display
        update_contacts()
        update_contact_display()
        update_selected_contact_indicator()
        update_range_indicator()
        
    func update_contacts():
        # Update radar contacts list
        radar_contacts.clear()
        
        if player_ship == null:
            return
            
        # Get nearby entities (would interface with entity system)
        var nearby_entities = get_nearby_entities(player_ship.global_position, radar_range)
        
        for entity in nearby_entities:
            # Filter entities based on radar mode and settings
            if should_show_entity(entity):
                var contact = create_radar_contact(entity)
                if contact != null:
                    radar_contacts.append(contact)
                    
    func should_show_entity(entity: Node3D) -> bool:
        # Determine if entity should be shown on radar
        if entity == player_ship:
            return false  # Don't show player ship
            
        # Filter based on settings
        if entity is Ship:
            var ship = entity as Ship
            if ship.isFriendlyTo(player_ship):
                return show_friendly
            elif ship.isHostileTo(player_ship):
                return show_hostile
            else:
                return show_neutral
                
        elif entity is Asteroid:
            return show_asteroids
            
        elif entity is Waypoint:
            return show_waypoints
            
        return false
        
    func create_radar_contact(entity: Node3D) -> RadarContact:
        # Create radar contact for entity
        var contact = RadarContact.new()
        contact.entity = entity
        contact.position = entity.global_position
        contact.type = get_entity_contact_type(entity)
        contact.name = get_entity_name(entity)
        contact.distance = player_ship.global_position.distance_to(entity.global_position)
        contact.velocity = get_entity_velocity(entity)
        contact.is_selected = (entity == player_ship.currentTarget)
        return contact
        
    func get_entity_contact_type(entity: Node3D) -> ContactType:
        # Determine contact type for entity
        if entity is Ship:
            var ship = entity as Ship
            if ship.isFriendlyTo(player_ship):
                return ContactType.FRIENDLY
            elif ship.isHostileTo(player_ship):
                return ContactType.HOSTILE
            else:
                return ContactType.NEUTRAL
                
        elif entity is Asteroid:
            return ContactType.ASTEROID
            
        elif entity is Waypoint:
            return ContactType.WAYPOINT
            
        return ContactType.UNKNOWN
        
    func get_entity_name(entity: Node3D) -> String:
        # Get name for entity
        if entity is Ship:
            return (entity as Ship).shipClass.name
        elif entity is Asteroid:
            return "Asteroid"
        elif entity is Waypoint:
            return (entity as Waypoint).name
        return "Unknown"
        
    func get_entity_velocity(entity: Node3D) -> Vector3:
        # Get velocity for entity (would interface with physics)
        if entity is Ship and (entity as Ship).physicsController != null:
            return (entity as Ship).physicsController.velocity
        return Vector3.ZERO
        
    func update_contact_display():
        # Update visual display of contacts
        # Clear existing contact visuals
        for child in contact_container.get_children():
            child.queue_free()
            
        # Create new contact visuals
        for contact in radar_contacts:
            if show_contact_on_radar(contact):
                var contact_sprite = create_contact_sprite(contact)
                if contact_sprite != null:
                    contact_container.add_child(contact_sprite)
                    
    func show_contact_on_radar(contact: RadarContact) -> bool:
        # Determine if contact should be displayed based on filters
        if show_targets_only and not contact.is_selected:
            return false
            
        match contact.type:
            ContactType.FRIENDLY:
                return show_friendly
            ContactType.HOSTILE:
                return show_hostile
            ContactType.NEUTRAL:
                return show_neutral
            ContactType.ASTEROID:
                return show_asteroids
            ContactType.WAYPOINT:
                return show_waypoints
            _:
                return true
                
    func create_contact_sprite(contact: RadarContact) -> Sprite2D:
        # Create visual sprite for radar contact
        var sprite = Sprite2D.new()
        sprite.texture = get_contact_texture(contact.type)
        sprite.centered = true
        sprite.modulate = get_contact_color(contact.type, contact.is_selected)
        sprite.scale = Vector2(contact_size / 16.0, contact_size / 16.0)
        sprite.position = world_to_radar(contact.position)
        return sprite
        
    func get_contact_texture(contact_type: ContactType) -> Texture2D:
        # Get texture for contact type
        match contact_type:
            ContactType.FRIENDLY:
                return preload("res://ui/radar/contact_friendly.png")
            ContactType.HOSTILE:
                return preload("res://ui/radar/contact_hostile.png")
            ContactType.NEUTRAL:
                return preload("res://ui/radar/contact_neutral.png")
            ContactType.ASTEROID:
                return preload("res://ui/radar/contact_asteroid.png")
            ContactType.WAYPOINT:
                return preload("res://ui/radar/contact_waypoint.png")
            _:
                return preload("res://ui/radar/contact_unknown.png")
                
    func get_contact_color(contact_type: ContactType, is_selected: bool) -> Color:
        # Get color for contact type
        var base_color = Color.WHITE
        match contact_type:
            ContactType.FRIENDLY:
                base_color = Color.GREEN
            ContactType.HOSTILE:
                base_color = Color.RED
            ContactType.NEUTRAL:
                base_color = Color.YELLOW
            ContactType.ASTEROID:
                base_color = Color.GRAY
            ContactType.WAYPOINT:
                base_color = Color.BLUE
            _:
                base_color = Color.WHITE
                
        # Modify color for selected contacts
        if is_selected:
            base_color = base_color.lightened(0.5)
            
        # Apply alpha
        base_color.a = contact_alpha
        return base_color
        
    func world_to_radar(world_position: Vector3) -> Vector2:
        # Convert 3D world position to 2D radar position
        var relative_pos = world_position - player_ship.global_position
        var distance = relative_pos.length()
        
        # Clamp to radar range
        if distance > radar_range:
            relative_pos = relative_pos.normalized() * radar_range
            
        # Project to 2D radar display (X-Z plane)
        var normalized_pos = relative_pos / radar_range
        return Vector2(
            (size.x / 2) + (normalized_pos.x * (size.x / 2)),
            (size.y / 2) + (normalized_pos.z * (size.y / 2))
        )
        
    func update_selected_contact_indicator():
        # Update visual indicator for selected contact
        if player_ship != null and player_ship.currentTarget != null:
            var contact_pos = world_to_radar(player_ship.currentTarget.global_position)
            selected_contact_indicator.position = contact_pos
            selected_contact_indicator.visible = true
        else:
            selected_contact_indicator.visible = false
            
    func update_range_indicator():
        # Update radar range indicator
        if range_indicator != null:
            range_indicator.text = "%.0f km" % (radar_range / 1000.0)
            
    func draw_radar_background():
        # Draw radar background circle
        draw_circle(Vector2(size.x / 2, size.y / 2), min(size.x, size.y) / 2, Color(0, 0.5, 1, 0.1))
        
    func draw_radar_grid():
        # Draw radar grid lines
        var center = Vector2(size.x / 2, size.y / 2)
        var radius = min(size.x, size.y) / 2
        
        # Draw concentric circles
        for i in range(1, 5):
            var circle_radius = radius * (float(i) / 4.0)
            draw_arc(center, circle_radius, 0, TAU, 32, grid_color, 1.0)
            
        # Draw crosshairs
        draw_line(Vector2(center.x - radius, center.y), Vector2(center.x + radius, center.y), grid_color, 1.0)
        draw_line(Vector2(center.x, center.y - radius), Vector2(center.x, center.y + radius), grid_color, 1.0)
        
    func set_player_ship(ship: Ship):
        # Set player ship reference
        player_ship = ship
        
    func set_radar_range(range: float):
        # Set radar range
        radar_range = max(range, 1000.0)  # Minimum 1km range
        update()
        
    func get_radar_range() -> float:
        # Get current radar range
        return radar_range
        
    func set_radar_mode(mode: RadarMode):
        # Set radar mode
        radar_mode = mode
        match mode:
            RadarMode.TACTICAL:
                radar_range = 10000.0  # 10km
            RadarMode.LONG_RANGE:
                radar_range = 50000.0  # 50km
            RadarMode.NEBULA:
                radar_range = 5000.0  # 5km (reduced in nebula)
        update()
        
    func get_radar_mode() -> RadarMode:
        # Get current radar mode
        return radar_mode
        
    func toggle_contact_type(contact_type: ContactType):
        # Toggle visibility of contact type
        match contact_type:
            ContactType.FRIENDLY:
                show_friendly = not show_friendly
            ContactType.HOSTILE:
                show_hostile = not show_hostile
            ContactType.NEUTRAL:
                show_neutral = not show_neutral
            ContactType.ASTEROID:
                show_asteroids = not show_asteroids
            ContactType.WAYPOINT:
                show_waypoints = not show_waypoints
                
    func set_show_targets_only(show: bool):
        # Set targets only mode
        show_targets_only = show
        update()
        
    func is_showing_targets_only() -> bool:
        # Check if showing targets only
        return show_targets_only
        
    func get_contact_count() -> int:
        # Get number of contacts on radar
        return radar_contacts.size()
        
    func get_contact_by_position(screen_pos: Vector2, tolerance: float = 10.0) -> Node3D:
        # Get entity at screen position (for clicking contacts)
        for contact in radar_contacts:
            var contact_pos = world_to_radar(contact.position)
            if contact_pos.distance_to(screen_pos) <= tolerance:
                return contact.entity
        return null
        
    func _gui_input(event):
        # Handle GUI input (clicking on contacts)
        if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
            var clicked_contact = get_contact_by_position(event.position)
            if clicked_contact != null:
                # Select clicked contact (would interface with targeting system)
                if player_ship != null:
                    player_ship.set_target(clicked_contact)
                    
    func cleanup():
        # Clean up radar system
        radar_contacts.clear()
        player_ship = null

# Radar contact data structure
class RadarContact:
    var entity: Node3D = null
    var position: Vector3 = Vector3.ZERO
    var type: RadarSystem.ContactType = RadarSystem.ContactType.UNKNOWN
    var name: String = "Unknown"
    var distance: float = 0.0
    var velocity: Vector3 = Vector3.ZERO
    var is_selected: bool = false
    var threat_level: int = 0  # 0-10 threat level
    var is_damaged: bool = false
    
    func _init():
        pass

# Message system for combat messages and communications
class MessageSystem extends Control:
    # Message queue
    var message_queue: Array[Message] = []
    var active_messages: Array[Message] -> Array[Message] = []
    var message_history: Array[Message] = []
    var max_history: int = 100
    
    # Message display
    var message_container: VBoxContainer = null
    var history_container: VBoxContainer = null
    var scroll_container: ScrollContainer = null
    
    # Player reference
    var player_ship: Ship = null
    
    # Message settings
    var max_messages_on_screen: int = 5
    var message_duration: float = 5.0
    var message_fade_duration: float = 1.0
    var show_timestamps: bool = false
    var group_similar: bool = true
    
    # Message types
    enum MessageType {
        INFO,       # General information
        WARNING,    # Warning messages
        ERROR,      # Error messages
        COMBAT,     # Combat messages (kills, damage)
        COMM,       # Communications from other ships
        OBJECTIVE,  # Mission objectives
        SYSTEM,     # System status messages
        DEBUG       # Debug messages (only in debug builds)
    }
    
    # Message structure
    class Message:
        var text: String = ""
        var type: MessageType = MessageType.INFO
        var timestamp: float = 0.0
        var duration: float = 5.0
        var color: Color = Color.WHITE
        var is_fading: bool = false
        var fade_start_time: float = 0.0
        var sender: String = ""
        var priority: int = 0  # Higher priority messages shown first
        
        func _init(msg_text: String, msg_type: MessageType, msg_duration: float, msg_color: Color, msg_sender: String = ""):
            text = msg_text
            type = msg_type
            duration = msg_duration
            color = msg_color
            sender = msg_sender
            timestamp = Time.get_ticks_msec() / 1000.0
            priority = get_type_priority(msg_type)
            
        func get_type_priority(msg_type: MessageType) -> int:
            # Return priority for message type (higher = more important)
            match msg_type:
                MessageType.ERROR:
                    return 100
                MessageType.COMBAT:
                    return 80
                MessageType.COMM:
                    return 70
                MessageType.WARNING:
                    return 60
                MessageType.OBJECTIVE:
                    return 50
                MessageType.SYSTEM:
                    return 40
                MessageType.INFO:
                    return 30
                MessageType.DEBUG:
                    return 10
                _:
                    return 0
                    
        func is_expired(current_time: float) -> bool:
            # Check if message has expired
            return (current_time - timestamp) >= duration
            
        func should_fade(current_time: float, fade_duration: float) -> bool:
            # Check if message should start fading
            var age = current_time - timestamp
            return age >= (duration - fade_duration)
            
        func get_fade_alpha(current_time: float, fade_start: float, fade_duration: float) -> float:
            # Get alpha value for fade effect
            var fade_elapsed = current_time - fade_start
            if fade_elapsed <= 0:
                return 1.0
            return 1.0 - (fade_elapsed / fade_duration)
            
    func _ready():
        # Initialize message system
        initialize_message_system()
        
    func _process(delta):
        # Update message system
        update_messages(delta)
        
    func initialize_message_system():
        # Create message display containers
        create_message_containers()
        
    func create_message_containers():
        # Create message display containers
        scroll_container = ScrollContainer.new()
        scroll_container.anchor_right = 1.0
        scroll_container.anchor_bottom = 1.0
        add_child(scroll_container)
        
        message_container = VBoxContainer.new()
        message_container.anchor_right = 1.0
        message_container.anchor_bottom = 1.0
        scroll_container.add_child(message_container)
        
        # Create history container (hidden by default)
        history_container = VBoxContainer.new()
        history_container.anchor_right = 1.0
        history_container.anchor_bottom = 1.0
        history_container.visible = false
        scroll_container.add_child(history_container)
        
    func add_message(text: String, message_type: MessageType = MessageType.INFO, 
                    duration: float = 5.0, color: Color = Color.WHITE, sender: String = ""):
        # Add message to queue
        var message = Message.new(text, message_type, duration, color, sender)
        message_queue.append(message)
        
        # Add to history
        message_history.append(message)
        if message_history.size() > max_history:
            message_history.pop_front()
            
    func add_combat_message(text: String, priority: int = 0):
        # Add combat message
        var color = Color.RED
        if priority > 50:
            color = Color.ORANGE
        add_message(text, MessageType.COMBAT, message_duration, color)
        
    func add_comm_message(text: String, sender: String = ""):
        # Add communication message
        add_message(text, MessageType.COMM, message_duration * 1.5, Color.CYAN, sender)
        
    func add_objective_message(text: String):
        # Add objective message
        add_message(text, MessageType.OBJECTIVE, message_duration * 2.0, Color.GREEN)
        
    func add_system_message(text: String):
        # Add system message
        add_message(text, MessageType.SYSTEM, message_duration, Color.YELLOW)
        
    func add_debug_message(text: String):
        # Add debug message (only in debug builds)
        if OS.has_feature("debug"):
            add_message(text, MessageType.DEBUG, message_duration, Color.GRAY)
            
    func update_messages(delta: float):
        # Process message queue
        process_message_queue()
        
        # Update active messages
        update_active_messages()
        
        # Clean up expired messages
        cleanup_expired_messages()
        
    func process_message_queue():
        # Process messages in queue
        while not message_queue.is_empty():
            var message = message_queue.pop_front()
            add_message_to_display(message)
            
    func add_message_to_display(message: Message):
        # Add message to active display
        if active_messages.size() >= max_messages_on_screen:
            # Remove oldest low-priority message if needed
            remove_lowest_priority_message()
            
        active_messages.append(message)
        create_message_display(message)
        
    func create_message_display(message: Message):
        # Create visual display for message
        var message_label = Label.new()
        message_label.text = format_message_text(message)
        message_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        message_label.custom_minimum_size = Vector2(300, 0)
        
        # Set font and color based on message type
        set_message_appearance(message_label, message)
        
        # Add to message container
        message_container.add_child(message_label)
        
    func format_message_text(message: Message) -> String:
        # Format message text with timestamp if enabled
        var formatted_text = message.text
        if show_timestamps:
            var timestamp = Time.get_time_string_from_system()
            formatted_text = "[%s] %s" % [timestamp, formatted_text]
            
        # Add sender if present
        if message.sender != "" and message.type == MessageType.COMM:
            formatted_text = "%s: %s" % [message.sender, formatted_text]
            
        return formatted_text
        
    func set_message_appearance(label: Label, message: Message):
        # Set visual appearance based on message type
        var font_size = 14
        var font_color = message.color
        
        # Adjust appearance based on message type
        match message.type:
            MessageType.ERROR:
                font_size = 16
                font_color = Color.RED
            MessageType.WARNING:
                font_color = Color.ORANGE
            MessageType.COMBAT:
                font_size = 15
                font_color = Color.RED
            MessageType.COMM:
                font_color = Color.CYAN
            MessageType.OBJECTIVE:
                font_size = 16
                font_color = Color.GREEN
            MessageType.SYSTEM:
                font_color = Color.YELLOW
            MessageType.DEBUG:
                font_color = Color.GRAY
                font_size = 12
            _:
                font_color = Color.WHITE
                
        # Apply appearance
        label.add_theme_font_size_override("font_size", font_size)
        label.add_theme_color_override("font_color", font_color)
        
    func remove_lowest_priority_message():
        # Remove lowest priority message to make room
        if active_messages.is_empty():
            return
            
        var lowest_priority_index = 0
        var lowest_priority = active_messages[0].priority
        
        for i in range(1, active_messages.size()):
            if active_messages[i].priority < lowest_priority:
                lowest_priority = active_messages[i].priority
                lowest_priority_index = i
                
        # Remove message display
        if lowest_priority_index < message_container.get_child_count():
            var message_display = message_container.get_child(lowest_priority_index)
            message_display.queue_free()
            
        # Remove from active messages
        active_messages.remove_at(lowest_priority_index)
        
    func update_active_messages():
        # Update active messages (fade effects, etc.)
        var current_time = Time.get_ticks_msec() / 1000.0
        
        # Update message displays
        for i in range(active_messages.size()):
            var message = active_messages[i]
            var display_index = message_container.get_child_count() - active_messages.size() + i
            
            if display_index >= 0 and display_index < message_container.get_child_count():
                var message_display = message_container.get_child(display_index) as Label
                
                # Check if message should start fading
                if message.should_fade(current_time, message_fade_duration):
                    if not message.is_fading:
                        message.is_fading = true
                        message.fade_start_time = current_time
                        
                # Apply fade effect
                if message.is_fading:
                    var alpha = message.get_fade_alpha(current_time, message.fade_start_time, message_fade_duration)
                    var current_color = message_display.get_theme_color("font_color")
                    message_display.add_theme_color_override("font_color", Color(current_color.r, current_color.g, current_color.b, alpha))
                    
    func cleanup_expired_messages():
        # Remove expired messages from display
        var current_time = Time.get_ticks_msec() / 1000.0
        
        for i in range(active_messages.size() - 1, -1, -1):
            var message = active_messages[i]
            if message.is_expired(current_time):
                # Remove message display
                var display_index = message_container.get_child_count() - active_messages.size() + i
                if display_index >= 0 and display_index < message_container.get_child_count():
                    var message_display = message_container.get_child(display_index)
                    message_display.queue_free()
                    
                # Remove from active messages
                active_messages.remove_at(i)
                
    func clear_messages():
        # Clear all active messages
        for i in range(message_container.get_child_count() - 1, -1, -1):
            var child = message_container.get_child(i)
            child.queue_free()
            
        active_messages.clear()
        
    func clear_message_history():
        # Clear message history
        message_history.clear()
        
    func get_message_history() -> Array[Message]:
        # Get message history
        return message_history.duplicate()
        
    func show_message_history():
        # Show message history in scrollable container
        # Hide current messages and show history
        message_container.visible = false
        history_container.visible = true
        scroll_container.scroll_vertical = scroll_container.get_v_scroll_bar().max_value
        
        # Populate history container
        for message in message_history:
            var message_label = Label.new()
            message_label.text = format_message_text(message)
            set_message_appearance(message_label, message)
            history_container.add_child(message_label)
            
    func hide_message_history():
        # Hide message history and show current messages
        history_container.visible = false
        message_container.visible = true
        
        # Clear history container
        for child in history_container.get_children():
            child.queue_free()
            
    func set_player_ship(ship: Ship):
        # Set player ship reference
        player_ship = ship
        
    func set_max_messages(count: int):
        # Set maximum messages on screen
        max_messages_on_screen = max(count, 1)
        
    func get_max_messages() -> int:
        # Get maximum messages on screen
        return max_messages_on_screen
        
    func set_message_duration(duration: float):
        # Set default message duration
        message_duration = max(duration, 1.0)
        
    func get_message_duration() -> float:
        # Get default message duration
        return message_duration
        
    func set_show_timestamps(show: bool):
        # Set timestamp visibility
        show_timestamps = show
        
    func get_show_timestamps() -> bool:
        # Get timestamp visibility
        return show_timestamps
        
    func set_group_similar(group: bool):
        # Set similar message grouping
        group_similar = group
        
    func get_group_similar() -> bool:
        # Get similar message grouping
        return group_similar
        
    func set_max_history(count: int):
        # Set maximum history size
        max_history = max(count, 10)
        
    func get_max_history() -> int:
        # Get maximum history size
        return max_history
        
    func cleanup():
        # Clean up message system
        clear_messages()
        clear_message_history()
        player_ship = null

# Tech database for ship and weapon information
class TechDatabase extends Control:
    # Database entries
    var ship_entries: Dictionary = {}
    var weapon_entries: Dictionary = {}
    var equipment_entries: Dictionary = {}
    var mission_entries: Dictionary = {}
    
    # UI elements
    var category_tabs: TabContainer = null
    var entry_list: ItemList = null
    var entry_details: RichTextLabel = null
    var search_box: LineEdit = null
    var filter_dropdown: OptionButton = null
    
    # Current state
    var current_category: String = "SHIPS"
    var current_entry: String = ""
    var search_filter: String = ""
    var filter_option: int = 0
    
    # Filtering options
    enum FilterOption { ALL, PLAYABLE, ENEMY, OBSOLETE }
    
    func _ready():
        # Initialize tech database
        initialize_database()
        
    func initialize_database():
        # Create UI elements
        create_ui_elements()
        
        # Load database entries
        load_database_entries()
        
        # Populate initial display
        populate_category_list()
        populate_entry_list()
        
    func create_ui_elements():
        # Create tech database UI elements
        # This would use Godot's container system to layout the interface
        # For brevity, we'll assume the UI is created in the scene file
        
        # Get references to UI elements
        category_tabs = $CategoryTabs
        entry_list = $EntryList
        entry_details = $EntryDetails
        search_box = $SearchBox
        filter_dropdown = $FilterDropdown
        
        # Connect signals
        if entry_list != null:
            entry_list.connect("item_selected", Callable(self, "_on_entry_selected"))
            
        if search_box != null:
            search_box.connect("text_changed", Callable(self, "_on_search_changed"))
            
        if filter_dropdown != null:
            filter_dropdown.connect("item_selected", Callable(self, "_on_filter_changed"))
            
    func load_database_entries():
        # Load tech database entries from resources
        load_ship_entries()
        load_weapon_entries()
        load_equipment_entries()
        load_mission_entries()
        
    func load_ship_entries():
        # Load ship entries from ship class database
        var ship_classes = ShipClassDatabase.get_all_classes()
        for ship_class in ship_classes:
            var entry = create_ship_entry(ship_class)
            ship_entries[ship_class.name] = entry
            
    func create_ship_entry(ship_class: ShipClass) -> Dictionary:
        # Create ship entry from ship class
        return {
            "name": ship_class.name,
            "description": ship_class.description,
            "manufacturer": ship_class.manufacturer,
            "type": ship_class.shipType,
            "species": ship_class.species,
            "playable": ship_class.flags & ShipClass.FLAG_PLAYER_SHIP,
            "max_velocity": ship_class.maxVelocity,
            "hull_strength": ship_class.maxHullStrength,
            "shield_strength": ship_class.maxShieldStrength,
            "weapon_hardpoints": ship_class.weaponHardpoints.size(),
            "is_obsolete": ship_class.flags & ShipClass.FLAG_OBSOLETE,
            "tech_level": ship_class.techLevel,
            "image": ship_class.imagePath,
            "3d_model": ship_class.modelPath
        }
        
    func load_weapon_entries():
        # Load weapon entries from weapon class database
        var weapon_classes = WeaponClassDatabase.get_all_classes()
        for weapon_class in weapon_classes:
            var entry = create_weapon_entry(weapon_class)
            weapon_entries[weapon_class.name] = entry
            
    func create_weapon_entry(weapon_class: WeaponClass) -> Dictionary:
        # Create weapon entry from weapon class
        return {
            "name": weapon_class.name,
            "description": weapon_class.description,
            "type": weapon_class.weaponType,
            "damage": weapon_class.damage,
            "speed": weapon_class.speed,
            "range": weapon_class.maxRange,
            "fire_rate": 1.0 / weapon_class.fireRate if weapon_class.fireRate > 0 else 0,
            "ammo_capacity": weapon_class.ammoCapacity,
            "playable": weapon_class.flags & WeaponClass.FLAG_PLAYER_ALLOWED,
            "is_obsolete": weapon_class.flags & WeaponClass.FLAG_OBSOLETE,
            "tech_level": weapon_class.techLevel,
            "image": weapon_class.imagePath,
            "3d_model": weapon_class.modelPath
        }
        
    func load_equipment_entries():
        # Load equipment entries (subsystems, countermeasures, etc.)
        # This would load from equipment definition files
        pass
        
    func load_mission_entries():
        # Load mission entries from campaign data
        # This would load from campaign/mission files
        pass
        
    func populate_category_list():
        # Populate category tabs
        if category_tabs != null:
            # Clear existing tabs
            while category_tabs.get_tab_count() > 0:
                category_tabs.remove_tab(0)
                
            # Add category tabs
            category_tabs.add_child(preload("res://ui/tech_database/ship_category.tscn").instantiate())
            category_tabs.set_tab_title(category_tabs.get_tab_count() - 1, "Ships")
            
            category_tabs.add_child(preload("res://ui/tech_database/weapon_category.tscn").instantiate())
            category_tabs.set_tab_title(category_tabs.get_tab_count() - 1, "Weapons")
            
            category_tabs.add_child(preload("res://ui/tech_database/equipment_category.tscn").instantiate())
            category_tabs.set_tab_title(category_tabs.get_tab_count() - 1, "Equipment")
            
            category_tabs.add_child(preload("res://ui/tech_database/mission_category.tscn").instantiate())
            category_tabs.set_tab_title(category_tabs.get_tab_count() - 1, "Missions")
            
    func populate_entry_list():
        # Populate entry list with filtered entries
        if entry_list != null:
            entry_list.clear()
            
            var entries = get_filtered_entries()
            for entry_name in entries:
                entry_list.add_item(entry_name)
                
    func get_filtered_entries() -> Dictionary:
        # Get entries filtered by current settings
        var filtered = {}
        
        match current_category:
            "SHIPS":
                filtered = filter_entries(ship_entries)
            "WEAPONS":
                filtered = filter_entries(weapon_entries)
            "EQUIPMENT":
                filtered = filter_entries(equipment_entries)
            "MISSIONS":
                filtered = filter_entries(mission_entries)
                
        return filtered
        
    func filter_entries(entries: Dictionary) -> Dictionary:
        # Filter entries based on current filter settings
        var filtered = {}
        
        for entry_name in entries.keys():
            var entry = entries[entry_name]
            
            # Apply search filter
            if search_filter != "" and not entry_name.containsn(search_filter):
                continue
                
            # Apply type filter
            if not should_show_entry(entry):
                continue
                
            filtered[entry_name] = entry
            
        return filtered
        
    func should_show_entry(entry: Dictionary) -> bool:
        # Check if entry should be shown based on filter option
        match filter_option:
            FilterOption.ALL:
                return true
            FilterOption.PLAYABLE:
                return entry.get("playable", false)
            FilterOption.ENEMY:
                return not entry.get("playable", true)
            FilterOption.OBSOLETE:
                return entry.get("is_obsolete", false)
            _:
                return true
                
    func show_entry(entry_type: String, entry_name: String):
        # Show specific entry in database
        current_category = entry_type.to_upper()
        current_entry = entry_name
        populate_entry_list()
        select_entry(entry_name)
        
    func select_entry(entry_name: String):
        # Select entry in list and show details
        if entry_list != null:
            for i in range(entry_list.get_item_count()):
                if entry_list.get_item_text(i) == entry_name:
                    entry_list.select(i)
                    _on_entry_selected(i)
                    break
                    
    func _on_entry_selected(index: int):
        # Handle entry selection
        if entry_list != null and index < entry_list.get_item_count():
            var entry_name = entry_list.get_item_text(index)
            show_entry_details(entry_name)
            
    func show_entry_details(entry_name: String):
        # Show details for selected entry
        if entry_details != null:
            var entry = get_entry_details(entry_name)
            if entry != null:
                entry_details.text = format_entry_details(entry)
            else:
                entry_details.text = "Entry not found: %s" % entry_name
                
    func get_entry_details(entry_name: String) -> Dictionary:
        # Get details for entry
        if ship_entries.has(entry_name):
            return ship_entries[entry_name]
        elif weapon_entries.has(entry_name):
            return weapon_entries[entry_name]
        elif equipment_entries.has(entry_name):
            return equipment_entries[entry_name]
        elif mission_entries.has(entry_name):
            return mission_entries[entry_name]
        return {}
        
    func format_entry_details(entry: Dictionary) -> String:
        # Format entry details for display
        var details = "[font_size=18][b]%s[/b][/font_size]\n\n" % entry.get("name", "Unknown")
        
        # Add description
        details += "[i]%s[/i]\n\n" % entry.get("description", "No description available.")
        
        # Add technical specifications
        var specs = get_technical_specifications(entry)
        if not specs.is_empty():
            details += "[b]Technical Specifications:[/b]\n"
            details += specs + "\n\n"
            
        # Add additional information
        var additional = get_additional_information(entry)
        if not additional.is_empty():
            details += "[b]Additional Information:[/b]\n"
            details += additional + "\n\n"
            
        return details
        
    func get_technical_specifications(entry: Dictionary) -> String:
        # Get technical specifications for entry
        var specs = ""
        
        # Add common specs
        if entry.has("type"):
            specs += "Type: %s\n" % entry["type"]
            
        if entry.has("manufacturer"):
            specs += "Manufacturer: %s\n" % entry["manufacturer"]
            
        if entry.has("damage"):
            specs += "Damage: %.0f\n" % entry["damage"]
            
        if entry.has("speed"):
            specs += "Speed: %.0f\n" % entry["speed"]
            
        if entry.has("range"):
            specs += "Range: %.0f\n" % entry["range"]
            
        if entry.has("fire_rate"):
            specs += "Fire Rate: %.2f/sec\n" % entry["fire_rate"]
            
        if entry.has("max_velocity"):
            var velocity = entry["max_velocity"] as Vector3
            specs += "Max Velocity: (%.0f, %.0f, %.0f)\n" % [velocity.x, velocity.y, velocity.z]
            
        if entry.has("hull_strength"):
            specs += "Hull Strength: %.0f\n" % entry["hull_strength"]
            
        if entry.has("shield_strength"):
            specs += "Shield Strength: %.0f\n" % entry["shield_strength"]
            
        if entry.has("weapon_hardpoints"):
            specs += "Weapon Hardpoints: %d\n" % entry["weapon_hardpoints"]
            
        if entry.has("ammo_capacity"):
            specs += "Ammo Capacity: %d\n" % entry["ammo_capacity"]
            
        return specs
        
    func get_additional_information(entry: Dictionary) -> String:
        # Get additional information for entry
        var info = ""
        
        if entry.has("tech_level"):
            info += "Tech Level: %d\n" % entry["tech_level"]
            
        if entry.has("playable"):
            info += "Playable: %s\n" % ("Yes" if entry["playable"] else "No")
            
        if entry.has("is_obsolete"):
            info += "Obsolete: %s\n" % ("Yes" if entry["is_obsolete"] else "No")
            
        return info
        
    func _on_search_changed(text: String):
        # Handle search text change
        search_filter = text
        populate_entry_list()
        
    func _on_filter_changed(index: int):
        # Handle filter option change
        filter_option = index
        populate_entry_list()
        
    func get_categories() -> Array:
        # Get available categories
        return ["SHIPS", "WEAPONS", "EQUIPMENT", "MISSIONS"]
        
    func get_category_entries(category: String) -> Array:
        # Get entries for category
        match category:
            "SHIPS":
                return ship_entries.keys()
            "WEAPONS":
                return weapon_entries.keys()
            "EQUIPMENT":
                return equipment_entries.keys()
            "MISSIONS":
                return mission_entries.keys()
            _:
                return []
                
    func search_entries(query: String) -> Array:
        # Search all entries for query
        var results = []
        
        # Search ships
        for ship_name in ship_entries.keys():
            if ship_name.containsn(query):
                results.append({"category": "SHIPS", "name": ship_name})
                
        # Search weapons
        for weapon_name in weapon_entries.keys():
            if weapon_name.containsn(query):
                results.append({"category": "WEAPONS", "name": weapon_name})
                
        # Search equipment
        for equipment_name in equipment_entries.keys():
            if equipment_name.containsn(query):
                results.append({"category": "EQUIPMENT", "name": equipment_name})
                
        # Search missions
        for mission_name in mission_entries.keys():
            if mission_name.containsn(query):
                results.append({"category": "MISSIONS", "name": mission_name})
                
        return results
        
    func get_entry_image(entry_name: String) -> Texture2D:
        # Get image for entry
        var entry = get_entry_details(entry_name)
        if entry.has("image") and entry["image"] != "":
            return load(entry["image"]) as Texture2D
        return null
        
    func get_entry_model(entry_name: String) -> PackedScene:
        # Get 3D model for entry
        var entry = get_entry_details(entry_name)
        if entry.has("3d_model") and entry["3d_model"] != "":
            return load(entry["3d_model"]) as PackedScene
        return null
        
    func show_entry_model(entry_name: String):
        # Show 3D model view for entry
        var model = get_entry_model(entry_name)
        if model != null:
            # This would show the model in a 3D view
            pass
            
    func compare_entries(entry1: String, entry2: String) -> Dictionary:
        # Compare two entries
        var details1 = get_entry_details(entry1)
        var details2 = get_entry_details(entry2)
        
        return {
            "entry1": details1,
            "entry2": details2,
            "comparison": generate_comparison(details1, details2)
        }
        
    func generate_comparison(entry1: Dictionary, entry2: Dictionary) -> String:
        # Generate comparison text
        var comparison = ""
        
        # Compare common attributes
        if entry1.has("type") and entry2.has("type"):
            comparison += "Type: %s vs %s\n" % [entry1["type"], entry2["type"]]
            
        if entry1.has("damage") and entry2.has("damage"):
            comparison += "Damage: %.0f vs %.0f\n" % [entry1["damage"], entry2["damage"]]
            
        if entry1.has("speed") and entry2.has("speed"):
            comparison += "Speed: %.0f vs %.0f\n" % [entry1["speed"], entry2["speed"]]
            
        if entry1.has("hull_strength") and entry2.has("hull_strength"):
            comparison += "Hull: %.0f vs %.0f\n" % [entry1["hull_strength"], entry2["hull_strength"]]
            
        return comparison
        
    func export_entry(entry_name: String, format: String = "json") -> String:
        # Export entry data
        var entry = get_entry_details(entry_name)
        if entry.is_empty():
            return ""
            
        match format:
            "json":
                var json = JSON.new()
                return json.stringify(entry, "  ")
            "xml":
                return generate_xml(entry)
            "csv":
                return generate_csv(entry)
            _:
                return ""
                
    func generate_xml(entry: Dictionary) -> String:
        # Generate XML representation
        var xml = "<entry>\n"
        for key in entry.keys():
            xml += "  <%s>%s</%s>\n" % [key, str(entry[key]), key]
        xml += "</entry>"
        return xml
        
    func generate_csv(entry: Dictionary) -> String:
        # Generate CSV representation
        var csv = ""
        for key in entry.keys():
            csv += "%s,%s\n" % [key, str(entry[key])]
        return csv
        
    func cleanup():
        # Clean up tech database
        ship_entries.clear()
        weapon_entries.clear()
        equipment_entries.clear()
        mission_entries.clear()
        current_category = ""
        current_entry = ""

# Fiction viewer for narrative content
class FictionViewer extends Control:
    # Fiction content
    var fiction_content: String = ""
    var current_section: int = 0
    var sections: Array[String] = []
    var section_headers: Array[String] = []
    
    # UI elements
    var title_label: Label = null
    var content_label: RichTextLabel = null
    var next_button: Button = null
    var prev_button: Button = null
    var section_list: ItemList = null
    var scroll_container: ScrollContainer = null
    
    # Formatting
    var bold_marker: String = "$B"
    var title_marker: String = "$Title"
    var paragraph_break: String = "\n\n"
    
    # Navigation
    var show_section_list: bool = false
    
    func _ready():
        # Initialize fiction viewer
        initialize_fiction_viewer()
        
    func initialize_fiction_viewer():
        # Get references to UI elements
        title_label = $TitleLabel
        content_label = $ScrollContainer/ContentLabel
        next_button = $Navigation/NextButton
        prev_button = $Navigation/PrevButton
        section_list = $SectionList
        scroll_container = $ScrollContainer
        
        # Connect signals
        if next_button != null:
            next_button.connect("pressed", Callable(self, "_on_next_pressed"))
            
        if prev_button != null:
            prev_button.connect("pressed", Callable(self, "_on_prev_pressed"))
            
        if section_list != null:
            section_list.connect("item_selected", Callable(self, "_on_section_selected"))
            
    func load_fiction_file(file_path: String):
        # Load fiction content from file
        var file = FileAccess.open(file_path, FileAccess.READ)
        if file != null:
            fiction_content = file.get_as_text()
            file.close()
            parse_fiction_content()
            show_section(0)
            
    func parse_fiction_content():
        # Parse fiction content into sections
        sections = []
        section_headers = []
        
        # Split content by double line breaks (paragraph breaks)
        var paragraphs = fiction_content.split(paragraph_break)
        
        # Parse sections and extract headers
        var current_section = ""
        for paragraph in paragraphs:
            if paragraph.begins_with(title_marker):
                # New section with title
                if current_section != "":
                    sections.append(current_section)
                    current_section = ""
                    
                # Extract header (remove $Title marker)
                var header = paragraph.substr(title_marker.length()).strip_edges()
                section_headers.append(header)
            else:
                # Add paragraph to current section
                if current_section != "":
                    current_section += paragraph_break
                current_section += paragraph.strip_edges()
                
        # Add final section
        if current_section != "":
            sections.append(current_section)
            
        # Create section list
        populate_section_list()
        
    func populate_section_list():
        # Populate section list with headers
        if section_list != null:
            section_list.clear()
            for i in range(section_headers.size()):
                var header = section_headers[i] if i < section_headers.size() else "Section %d" % (i + 1)
                section_list.add_item(header)
                
    func show_section(section_index: int):
        # Show specified section
        if section_index >= 0 and section_index < sections.size():
            current_section = section_index
            
            # Update title
            if title_label != null:
                var title = section_headers[section_index] if section_index < section_headers.size() else "Section %d" % (section_index + 1)
                title_label.text = title
                
            # Update content
            if content_label != null:
                var content = sections[section_index]
                content_label.text = format_fiction_text(content)
                
            # Update navigation buttons
            update_navigation_buttons()
            
            # Scroll to top
            if scroll_container != null:
                scroll_container.scroll_vertical = 0
                
    func format_fiction_text(text: String) -> String:
        # Format fiction text with markup
        var formatted = text
        
        # Replace bold markers with BBCode
        formatted = formatted.replace(bold_marker, "[b]")
        formatted = formatted.replace("[/$B]", "[/b]")  # Handle closing tags
        formatted = formatted.replace("/$B", "[/b]")   # Handle malformed closing tags
        
        # Handle title markers
        formatted = formatted.replace(title_marker, "[font_size=18][b]")
        formatted = formatted.replace("[/$Title]", "[/b][/font_size]")
        formatted = formatted.replace("/$Title", "[/b][/font_size]")
        
        return formatted
        
    func update_navigation_buttons():
        # Update navigation button states
        if next_button != null:
            next_button.disabled = current_section >= sections.size() - 1
            
        if prev_button != null:
            prev_button.disabled = current_section <= 0
            
        # Update section list selection
        if section_list != null:
            section_list.select(current_section)
            
    func _on_next_pressed():
        # Handle next section button
        if current_section < sections.size() - 1:
            show_section(current_section + 1)
            
    func _on_prev_pressed():
        # Handle previous section button
        if current_section > 0:
            show_section(current_section - 1)
            
    func _on_section_selected(index: int):
        # Handle section selection from list
        show_section(index)
        
    func next_section():
        # Go to next section
        _on_next_pressed()
        
    func previous_section():
        # Go to previous section
        _on_prev_pressed()
        
    func get_current_section() -> int:
        # Get current section index
        return current_section
        
    func get_section_count() -> int:
        # Get total number of sections
        return sections.size()
        
    func get_section_title(section_index: int) -> String:
        # Get title for section
        if section_index >= 0 and section_index < section_headers.size():
            return section_headers[section_index]
        return "Section %d" % (section_index + 1)
        
    func get_current_section_title() -> String:
        # Get title for current section
        return get_section_title(current_section)
        
    func get_section_content(section_index: int) -> String:
        # Get content for section
        if section_index >= 0 and section_index < sections.size():
            return sections[section_index]
        return ""
        
    func get_current_section_content() -> String:
        # Get content for current section
        return get_section_content(current_section)
        
    func search_sections(query: String) -> Array[int]:
        # Search sections for query
        var results = []
        for i in range(sections.size()):
            var content = sections[i]
            if content.containsn(query):
                results.append(i)
        return results
        
    func set_font(font_name: String, font_size: int):
        # Set font for fiction display
        if content_label != null:
            content_label.add_theme_font_override("normal_font", load("res://fonts/%s.tres" % font_name))
            content_label.add_theme_font_size_override("normal_font_size", font_size)
            
    func set_color_scheme(background: Color, text: Color):
        # Set color scheme for fiction viewer
        if content_label != null:
            content_label.add_theme_color_override("font_color", text)
            # Would also set background color for container
            
    func toggle_section_list():
        # Toggle section list visibility
        if section_list != null:
            show_section_list = not show_section_list
            section_list.visible = show_section_list
            
    func is_section_list_visible() -> bool:
        # Check if section list is visible
        return show_section_list
        
    func scroll_to_top():
        # Scroll to top of current section
        if scroll_container != null:
            scroll_container.scroll_vertical = 0
            
    func scroll_to_bottom():
        # Scroll to bottom of current section
        if scroll_container != null:
            scroll_container.scroll_vertical = scroll_container.get_v_scroll_bar().max_value
            
    func scroll_page_up():
        # Scroll one page up
        if scroll_container != null:
            scroll_container.scroll_vertical = max(0, scroll_container.scroll_vertical - scroll_container.size.y)
            
    func scroll_page_down():
        # Scroll one page down
        if scroll_container != null:
            var max_scroll = scroll_container.get_v_scroll_bar().max_value
            scroll_container.scroll_vertical = min(max_scroll, scroll_container.scroll_vertical + scroll_container.size.y)
            
    func cleanup():
        # Clean up fiction viewer
        fiction_content = ""
        sections.clear()
        section_headers.clear()
        current_section = 0

# Cutscene player for video and real-time cutscenes
class CutscenePlayer extends Control:
    # Cutscene state
    var current_cutscene: String = ""
    var is_playing: bool = false
    var is_paused: bool = false
    var current_time: float = 0.0
    var total_duration: float = 0.0
    
    # Playback components
    var video_player: VideoPlayer = null
    var subtitle_display: Label = null
    var skip_button: Button = null
    var progress_bar: ProgressBar = null
    
    # Subtitle system
    var subtitles: Dictionary = {}
    var current_subtitle: String = ""
    var subtitle_start_time: float = 0.0
    var subtitle_duration: float = 0.0
    
    # Audio
    var cutscene_audio: AudioStreamPlayer = null
    var voice_audio: AudioStreamPlayer = null
    
    # Events
    var cutscene_events: Array[CutsceneEvent] = []
    var pending_events: Array[CutsceneEvent] = []
    
    func _ready():
        # Initialize cutscene player
        initialize_cutscene_player()
        
    func initialize_cutscene_player():
        # Get references to UI elements
        video_player = $VideoPlayer
        subtitle_display = $SubtitleDisplay
        skip_button = $SkipButton
        progress_bar = $ProgressBar
        cutscene_audio = $CutsceneAudio
        voice_audio = $VoiceAudio
        
        # Connect signals
        if skip_button != null:
            skip_button.connect("pressed", Callable(self, "_on_skip_pressed"))
            
        if video_player != null:
            video_player.connect("finished", Callable(self, "_on_cutscene_finished"))
            
    func load_cutscene(cutscene_file: String):
        # Load cutscene from file
        current_cutscene = cutscene_file
        
        # Load video file
        if video_player != null:
            var video_path = "res://cutscenes/%s.webm" % cutscene_file
            video_player.stream = load(video_path) as VideoStream
            
        # Load subtitles
        load_subtitles(cutscene_file)
        
        # Load audio
        load_audio(cutscene_file)
        
        # Load events
        load_cutscene_events(cutscene_file)
        
    func load_subtitles(cutscene_file: String):
        # Load subtitles for cutscene
        var subtitle_file = "res://cutscenes/%s.srt" % cutscene_file
        var file = FileAccess.open(subtitle_file, FileAccess.READ)
        if file != null:
            parse_subtitle_file(file)
            file.close()
            
    func parse_subtitle_file(file: FileAccess):
        # Parse subtitle file (SRT format)
        subtitles.clear()
        var line = file.get_line()
        while not file.eof_reached():
            if line.is_valid_int():
                # Subtitle index
                var index = line.to_int()
                var time_line = file.get_line()
                var content = ""
                
                # Read subtitle content
                line = file.get_line()
                while line != "" and not file.eof_reached():
                    if content != "":
                        content += "\n"
                    content += line
                    line = file.get_line()
                    
                # Parse time codes
                var times = parse_time_codes(time_line)
                if times.size() == 2:
                    subtitles[times[0]] = {
                        "start": times[0],
                        "end": times[1],
                        "content": content
                    }
                    
            line = file.get_line()
            
    func parse_time_codes(time_line: String) -> Array[float]:
        # Parse SRT time codes
        var times = []
        # Format: "HH:MM:SS,mmm --> HH:MM:SS,mmm"
        var parts = time_line.split(" --> ")
        if parts.size() == 2:
            times.append(parse_time_code(parts[0]))
            times.append(parse_time_code(parts[1]))
        return times
        
    func parse_time_code(code: String) -> float:
        # Parse time code to seconds
        # Format: "HH:MM:SS,mmm" or "HH:MM:SS.mmm"
        var clean_code = code.replace(",", ".")
        var parts = clean_code.split(":")
        if parts.size() == 3:
            var hours = parts[0].to_float()
            var minutes = parts[1].to_float()
            var seconds = parts[2].to_float()
            return hours * 3600 + minutes * 60 + seconds
        return 0.0
        
    func load_audio(cutscene_file: String):
        # Load audio for cutscene
        var audio_file = "res://cutscenes/%s.ogg" % cutscene_file
        if cutscene_audio != null:
            cutscene_audio.stream = load(audio_file) as AudioStream
            
        var voice_file = "res://cutscenes/%s_voice.ogg" % cutscene_file
        if voice_audio != null:
            voice_audio.stream = load(voice_file) as AudioStream
            
    func load_cutscene_events(cutscene_file: String):
        # Load events for cutscene
        cutscene_events.clear()
        pending_events.clear()
        
        var events_file = "res://cutscenes/%s.tscn" % cutscene_file
        var events_scene = load(events_file) as PackedScene
        if events_scene != null:
            var events_root = events_scene.instantiate()
            if events_root != null:
                # Extract events from scene
                extract_events_from_scene(events_root)
                events_root.queue_free()
                
    func extract_events_from_scene(scene_root: Node):
        # Extract events from scene tree
        for child in scene_root.get_children():
            if child is CutsceneEvent:
                cutscene_events.append(child)
                
    func play():
        # Start playing cutscene
        if video_player != null:
            video_player.play()
            is_playing = true
            is_paused = false
            
        if cutscene_audio != null:
            cutscene_audio.play()
            
        # Start event processing
        start_event_processing()
        
    func pause():
        # Pause cutscene
        if video_player != null:
            video_player.paused = true
            is_paused = true
            
        if cutscene_audio != null:
            cutscene_audio.stream_paused = true
            
    func resume():
        # Resume cutscene
        if video_player != null:
            video_player.paused = false
            is_playing = true
            is_paused = false
            
        if cutscene_audio != null:
            cutscene_audio.stream_paused = false
            
    func stop():
        # Stop cutscene
        if video_player != null:
            video_player.stop()
            is_playing = false
            is_paused = false
            
        if cutscene_audio != null:
            cutscene_audio.stop()
            
        # Clear subtitle
        if subtitle_display != null:
            subtitle_display.text = ""
            
        # Clear events
        cutscene_events.clear()
        pending_events.clear()
        
    func _process(delta):
        # Update cutscene playback
        if is_playing and not is_paused:
            update_playback(delta)
            update_subtitles()
            update_events()
            update_progress()
            
    func update_playback(delta: float):
        # Update playback time
        if video_player != null:
            current_time = video_player.stream_position
            if video_player.stream != null:
                total_duration = video_player.stream.get_length()
                
    func update_subtitles():
        # Update subtitle display
        var current_subtitle = get_current_subtitle(current_time)
        if subtitle_display != null and current_subtitle != self.current_subtitle:
            self.current_subtitle = current_subtitle
            subtitle_display.text = current_subtitle
            
    func get_current_subtitle(time: float) -> String:
        # Get subtitle for current time
        for subtitle_time in subtitles.keys():
            var subtitle = subtitles[subtitle_time]
            if time >= subtitle["start"] and time <= subtitle["end"]:
                return subtitle["content"]
        return ""
        
    func update_events():
        # Process cutscene events
        for i in range(pending_events.size() - 1, -1, -1):
            var event = pending_events[i]
            if event.time <= current_time:
                execute_event(event)
                pending_events.remove_at(i)
                
    func start_event_processing():
        # Start processing cutscene events
        pending_events = cutscene_events.duplicate()
        # Sort by time
        pending_events.sort_custom(Callable(self, "sort_events_by_time"))
        
    func sort_events_by_time(a: CutsceneEvent, b: CutsceneEvent) -> bool:
        # Sort events by time
        return a.time < b.time
        
    func execute_event(event: CutsceneEvent):
        # Execute cutscene event
        if event.event_type == "SUBTITLE":
            # Show subtitle event
            if subtitle_display != null:
                subtitle_display.text = event.parameters.get("text", "")
                
        elif event.event_type == "SOUND":
            # Play sound event
            if voice_audio != null:
                var sound_file = event.parameters.get("sound", "")
                if sound_file != "":
                    voice_audio.stream = load(sound_file) as AudioStream
                    voice_audio.play()
                    
        elif event.event_type == "CAMERA":
            # Camera event (would control camera system)
            pass
            
        elif event.event_type == "EFFECT":
            # Visual effect event
            pass
            
    func update_progress():
        # Update progress bar
        if progress_bar != null and total_duration > 0:
            progress_bar.value = (current_time / total_duration) * 100
            
    func _on_skip_pressed():
        # Handle skip button
        finish_cutscene()
        
    func _on_cutscene_finished():
        # Handle cutscene completion
        finish_cutscene()
        
    func finish_cutscene():
        # Finish cutscene and notify completion
        stop()
        # Would emit signal or call completion callback
        
    func set_volume(volume: float):
        # Set cutscene volume
        if cutscene_audio != null:
            cutscene_audio.volume_db = linear_to_db(volume)
            
        if voice_audio != null:
            voice_audio.volume_db = linear_to_db(volume)
            
    func get_volume() -> float:
        # Get cutscene volume
        if cutscene_audio != null:
            return db_to_linear(cutscene_audio.volume_db)
        return 1.0
        
    func is_cutscene_active() -> bool:
        # Check if cutscene is currently active
        return is_playing or is_paused
        
    func get_current_time() -> float:
        # Get current playback time
        return current_time
        
    func get_total_duration() -> float:
        # Get total cutscene duration
        return total_duration
        
    func get_progress_percentage() -> float:
        # Get playback progress as percentage
        if total_duration > 0:
            return current_time / total_duration
        return 0.0
        
    func seek(time: float):
        # Seek to specific time in cutscene
        if video_player != null:
            video_player.stream_position = time
            current_time = time
            
        if cutscene_audio != null:
            cutscene_audio.seek(time)
            
    func set_subtitle_visibility(visible: bool):
        # Set subtitle display visibility
        if subtitle_display != null:
            subtitle_display.visible = visible
            
    func is_subtitle_visible() -> bool:
        # Check if subtitles are visible
        if subtitle_display != null:
            return subtitle_display.visible
        return true
        
    func cleanup():
        # Clean up cutscene player
        stop()
        current_cutscene = ""
        subtitles.clear()

# Base class for cutscene events
class CutsceneEvent extends Resource:
    @export var time: float = 0.0
    @export var event_type: String = "UNKNOWN"
    @export var parameters: Dictionary = {}
    
    func _init():
        pass

# Loading screen for resource loading
class LoadingScreen extends Control:
    # Loading state
    var is_loading: bool = false
    var progress: float = 0.0
    var status_text: String = "Loading..."
    
    # UI elements
    var progress_bar: ProgressBar = null
    var status_label: Label = null
    var loading_text: Label = null
    var background: TextureRect = null
    
    # Loading phases
    var phases: Array[LoadingPhase] = []
    var current_phase: int = 0
    
    # Timing
    var start_time: float = 0.0
    var estimated_time: float = 0.0
    var last_update: float = 0.0
    
    class LoadingPhase:
        var name: String
        var weight: float
        var progress: float
        
        func _init(phase_name: String, phase_weight: float):
            name = phase_name
            weight = phase_weight
            progress = 0.0
            
    func _ready():
        # Initialize loading screen
        initialize_loading_screen()
        
    func initialize_loading_screen():
        # Get references to UI elements
        progress_bar = $ProgressBar
        status_label = $StatusLabel
        loading_text = $LoadingText
        background = $Background
        
        # Set initial state
        set_progress(0.0)
        set_status_text("Initializing...")
        
    func set_loading_text(text: String):
        # Set loading text
        if loading_text != null:
            loading_text.text = text
            
    func set_status_text(text: String):
        # Set status text
        status_text = text
        if status_label != null:
            status_label.text = text
            
    func update_progress(progress_value: float, status: String = ""):
        # Update loading progress
        progress = clamp(progress_value, 0.0, 1.0)
        if status != "":
            set_status_text(status)
            
        # Update UI elements
        if progress_bar != null:
            progress_bar.value = progress * 100
            
        if status_label != null:
            if status != "":
                status_label.text = status
            elif estimated_time > 0:
                var elapsed = Time.get_ticks_msec() / 1000.0 - start_time
                var remaining = estimated_time - elapsed
                if remaining > 0:
                    status_label.text = "Estimated time remaining: %d seconds" % remaining
                    
    func set_progress(progress_value: float):
        # Set progress value (0.0 to 1.0)
        progress = clamp(progress_value, 0.0, 1.0)
        if progress_bar != null:
            progress_bar.value = progress * 100
            
    func get_progress() -> float:
        # Get current progress
        return progress
        
    func show_loading_screen():
        # Show loading screen
        is_loading = true
        start_time = Time.get_ticks_msec() / 1000.0
        if visible:
            show()
            
    func hide_loading_screen():
        # Hide loading screen
        is_loading = false
        if visible:
            hide()
            
    func is_loading_active() -> bool:
        # Check if loading is active
        return is_loading
        
    func start_loading_phase(phase_name: String, weight: float = 1.0):
        # Start a loading phase
        var phase = LoadingPhase.new(phase_name, weight)
        phases.append(phase)
        current_phase = phases.size() - 1
        set_status_text(phase_name)
        
    func update_loading_phase(progress_value: float):
        # Update current loading phase
        if current_phase < phases.size():
            var phase = phases[current_phase]
            phase.progress = clamp(progress_value, 0.0, 1.0)
            update_overall_progress()
            
    func complete_loading_phase():
        # Complete current loading phase
        if current_phase < phases.size():
            var phase = phases[current_phase]
            phase.progress = 1.0
            update_overall_progress()
            
    func update_overall_progress():
        # Update overall loading progress based on phases
        var total_weight = 0.0
        var weighted_progress = 0.0
        
        for phase in phases:
            total_weight += phase.weight
            weighted_progress += phase.progress * phase.weight
            
        if total_weight > 0:
            var overall_progress = weighted_progress / total_weight
            set_progress(overall_progress)
            
    func reset_loading():
        # Reset loading state
        progress = 0.0
        status_text = "Loading..."
        phases.clear()
        current_phase = 0
        start_time = 0.0
        estimated_time = 0.0
        last_update = 0.0
        
        # Update UI
        set_progress(0.0)
        set_status_text("Loading...")
        
    func set_estimated_time(seconds: float):
        # Set estimated loading time
        estimated_time = seconds
        
    func get_estimated_time() -> float:
        # Get estimated loading time
        return estimated_time
        
    func set_background(image_path: String):
        # Set loading screen background
        if background != null:
            background.texture = load(image_path) as Texture2D
            
    func set_background_color(color: Color):
        # Set loading screen background color
        if background != null:
            background.modulate = color
            
    func set_text_color(color: Color):
        # Set loading text color
        if loading_text != null:
            loading_text.add_theme_color_override("font_color", color)
        if status_label != null:
            status_label.add_theme_color_override("font_color", color)
        if progress_bar != null:
            progress_bar.add_theme_color_override("font_color", color)
            
    func set_bar_color(color: Color):
        # Set progress bar color
        if progress_bar != null:
            progress_bar.add_theme_color_override("tint_under", color)
            progress_bar.add_theme_color_override("tint_over", color.lightened(0.3))
            
    func add_loading_tip(tip: String):
        # Add loading tip (would show randomly)
        pass
        
    func show_random_tip():
        # Show random loading tip
        pass
        
    func cleanup():
        # Clean up loading screen
        reset_loading()
        phases.clear()
        current_phase = 0

# Briefing screen for mission introduction
class BriefingScreen extends Control:
    # Mission data
    var current_mission: Mission = null
    
    # UI elements
    var mission_title: Label = null
    var mission_description: RichTextLabel = null
    var objective_list: ItemList = null
    var ship_selection: VBoxContainer = null
    var weapon_selection: VBoxContainer = null
    var start_mission_button: Button = null
    var back_button: Button = null
    var fiction_button: Button = null
    
    # Player configuration
    var player_ship_class: ShipClass = null
    var player_weapons: Array[WeaponClass] = []
    
    func _ready():
        # Initialize briefing screen
        initialize_briefing_screen()
        
    func initialize_briefing_screen():
        # Get references to UI elements
        mission_title = $MissionTitle
        mission_description = $MissionDescription
        objective_list = $ObjectiveList
        ship_selection = $ShipSelection
        weapon_selection = $WeaponSelection
        start_mission_button = $StartMissionButton
        back_button = $BackButton
        fiction_button = $FictionButton
        
        # Connect signals
        if start_mission_button != null:
            start_mission_button.connect("pressed", Callable(self, "_on_start_mission_pressed"))
            
        if back_button != null:
            back_button.connect("pressed", Callable(self, "_on_back_pressed"))
            
        if fiction_button != null:
            fiction_button.connect("pressed", Callable(self, "_on_fiction_pressed"))
            
    func set_mission(mission: Mission):
        # Set mission for briefing
        current_mission = mission
        update_briefing_display()
        
    func update_briefing_display():
        # Update briefing display with mission information
        if current_mission == null:
            return
            
        # Update mission title
        if mission_title != null:
            mission_title.text = current_mission.name
            
        # Update mission description
        if mission_description != null:
            mission_description.text = current_mission.description
            
        # Update objectives list
        update_objectives_list()
        
        # Update ship and weapon selection
        update_ship_selection()
        update_weapon_selection()
        
        # Update button states
        update_button_states()
        
    func update_objectives_list():
        # Update mission objectives display
        if objective_list != null:
            objective_list.clear()
            
            for objective in current_mission.objectives:
                var text = "[ ] "
                if objective.isPrimary:
                    text += "[Primary] "
                else:
                    text += "[Secondary] "
                text += objective.description
                objective_list.add_item(text)
                
    func update_ship_selection():
        # Update ship selection interface
        # This would populate ship selection based on mission and player unlocks
        pass
        
    func update_weapon_selection():
        # Update weapon selection interface
        # This would populate weapon selection based on ship and player unlocks
        pass
        
    func update_button_states():
        # Update button enabled/disabled states
        if start_mission_button != null:
            start_mission_button.disabled = (player_ship_class == null)
            
        if fiction_button != null:
            fiction_button.disabled = (current_mission == null or current_mission.fictionFile == "")
            
    func select_ship(ship_class_name: String):
        # Select player ship for mission
        player_ship_class = ShipClassDatabase.get_class(ship_class_name)
        update_button_states()
        
    func select_weapon(weapon_slot: int, weapon_class_name: String):
        # Select weapon for mission
        if weapon_slot >= 0 and weapon_slot < player_weapons.size():
            player_weapons[weapon_slot] = WeaponClassDatabase.get_class(weapon_class_name)
            
    func _on_start_mission_pressed():
        # Handle start mission button
        # Would start mission with selected ship/weapons
        pass
        
    func _on_back_pressed():
        # Handle back button
        # Would return to previous screen
        pass
        
    func _on_fiction_pressed():
        # Handle fiction button
        # Would show mission fiction
        if current_mission != null and current_mission.fictionFile != "":
            # Would open fiction viewer with mission fiction
            pass
            
    func get_selected_ship_class() -> ShipClass:
        # Get selected ship class
        return player_ship_class
        
    func get_selected_weapons() -> Array[WeaponClass]:
        # Get selected weapons
        return player_weapons
        
    func set_ship_loadout(ship_class: ShipClass, weapons: Array[WeaponClass]):
        # Set player ship and weapon loadout
        player_ship_class = ship_class
        player_weapons = weapons
        update_briefing_display()
        
    func get_mission() -> Mission:
        # Get current mission
        return current_mission
        
    func cleanup():
        # Clean up briefing screen
        current_mission = null
        player_ship_class = null
        player_weapons.clear()

# Debriefing screen for mission evaluation
class DebriefingScreen extends Control:
    # Mission result data
    var mission_result: Mission = null
    var mission_success: bool = false
    var mission_statistics: Dictionary = {}
    
    # UI elements
    var mission_outcome: Label = null
    var mission_stats: VBoxContainer = null
    var objective_results: VBoxContainer = null
    func _ready():
        # Initialize debriefing screen
        initialize_debriefing_screen()
        
    func initialize_debriefing_screen():
        # Get references to UI elements
        mission_outcome = $MissionOutcome
        mission_stats = $MissionStats
        objective_results = $ObjectiveResults
        # Add other UI element references
        
        # Connect signals
        # Connect button signals
        
    func set_mission_result(mission: Mission, success: bool, statistics: Dictionary):
        # Set mission result for debriefing
        mission_result = mission
        mission_success = success
        mission_statistics = statistics
        update_debriefing_display()
        
    func update_debriefing_display():
        # Update debriefing display with mission results
        if mission_result == null:
            return
            
        # Update mission outcome
        update_mission_outcome()
        
        # Update statistics display
        update_statistics_display()
        
        # Update objective results
        update_objective_results()
        
        # Update medal awards
        update_medal_awards()
        
        # Update campaign progression
        update_campaign_progression()
        
    func update_mission_outcome():
        # Update mission outcome display
        if mission_outcome != null:
            var outcome_text = "MISSION "
            outcome_text += "SUCCESS" if mission_success else "FAILED"
            outcome_text += "\n\n"
            
            if mission_statistics.has("score"):
                outcome_text += "Score: %d" % mission_statistics["score"]
                
            if mission_statistics.has("time"):
                outcome_text += "\nTime: %.1f seconds" % mission_statistics["time"]
                
            mission_outcome.text = outcome_text
            
    func update_statistics_display():
        # Update mission statistics display
        # This would populate the statistics section with mission data
        pass
        
    func update_objective_results():
        # Update objective results display
        # This would show which objectives were completed/failed
        pass
        
    func update_medal_awards():
        # Update medal awards display
        # This would show earned medals and awards
        pass
        
    func update_campaign_progression():
        # Update campaign progression
        # This would update campaign state and unlock new content
        pass
        
    func get_mission_result() -> Mission:
        # Get mission result
        return mission_result
        
    func get_mission_success() -> bool:
        # Get mission success status
        return mission_success
        
    func get_mission_statistics() -> Dictionary:
        # Get mission statistics
        return mission_statistics
        
    func cleanup():
        # Clean up debriefing screen
        mission_result = null
        mission_success = false
        mission_statistics.clear()

# Base class for HUD elements
class HUDElement extends Control:
    # Element properties
    var element_name: String = "HUDElement"
    var is_active: bool = true
    var position_offset: Vector2 = Vector2.ZERO
    var element_scale: float = 1.0
    var element_alpha: float = 1.0
    var is_visible: bool = true
    
    # Player reference
    var player_ship: Ship = null
    
    # Update frequency
    var update_frequency: float = 0.1  # Update every 100ms
    var last_update: float = 0.0
    
    func _ready():
        # Initialize HUD element
        initialize_hud_element()
        
    func initialize_hud_element():
        # Common initialization for HUD elements
        pass
        
    func _process(delta):
        # Update HUD element
        if is_active and is_visible:
            var current_time = Time.get_ticks_msec() / 1000.0
            if current_time - last_update >= update_frequency:
                update_element(delta)
                last_update = current_time
                
    func update_element(delta: float):
        # Update element display
        # Override in subclasses
        pass
        
    func set_player_ship(ship: Ship):
        # Set player ship reference
        player_ship = ship
        
    func activate():
        # Activate HUD element
        is_active = true
        visible = true
        
    func deactivate():
        # Deactivate HUD element
        is_active = false
        visible = false
        
    func toggle():
        # Toggle HUD element state
        if is_active:
            deactivate()
        else:
            activate()
            
    func set_position_offset(offset: Vector2):
        # Set position offset for element
        position_offset = offset
        position = position_offset
        
    func set_scale(scale: float):
        # Set element scale
        element_scale = clamp(scale, 0.5, 2.0)
        scale = Vector2(element_scale, element_scale)
        
    func set_alpha(alpha: float):
        # Set element alpha/transparency
        element_alpha = clamp(alpha, 0.0, 1.0)
        modulate = Color(modulate.r, modulate.g, modulate.b, element_alpha)
        
    func set_visibility(visible: bool):
        # Set element visibility
        is_visible = visible
        self.visible = visible and is_active
        
    func is_element_active() -> bool:
        # Check if element is active
        return is_active
        
    func is_element_visible() -> bool:
        # Check if element is visible
        return is_visible and visible
        
    func get_element_name() -> String:
        # Get element name
        return element_name
        
    func cleanup():
        # Clean up HUD element
        player_ship = null

# Weapon display HUD element
class WeaponDisplay extends HUDElement:
    # Weapon display components
    var primary_display: VBoxContainer = null
    var secondary_display: VBoxContainer = null
    var primary_ammo_labels: Array[Label] = []
    var secondary_ammo_labels: Array[Label] = []
    var primary_name_labels: Array[Label] = []
    var secondary_name_labels: Array[Label] = []
    var primary_cooldown_bars: Array[ProgressBar] = []
    var secondary_cooldown_bars: Array[ProgressBar] = []
    
    # Display settings
    var show_ammo: bool = true
    var show_cooldown: bool = true
    var show_weapon_names: bool = true
    var compact_mode: bool = false
    
    func _ready():
        # Initialize weapon display
        element_name = "WeaponDisplay"
        initialize_weapon_display()
        
    func initialize_weapon_display():
        # Initialize weapon display components
        primary_display = $PrimaryDisplay
        secondary_display = $SecondaryDisplay
        # Initialize arrays for ammo labels, name labels, cooldown bars
        
    func update_element(delta: float):
        # Update weapon display
        if player_ship == null or player_ship.weaponSystem == null:
            return
            
        update_primary_weapons()
        update_secondary_weapons()
        update_weapon_cooldowns(delta)
        
    func update_primary_weapons():
        # Update primary weapon display
        var primary_weapons = player_ship.weaponSystem.primaryWeapons
        for i in range(primary_weapons.size()):
            if i < primary_ammo_labels.size():
                var weapon = primary_weapons[i]
                var label = primary_ammo_labels[i]
                
                # Update ammo display
                if show_ammo:
                    label.text = "%s: %d" % [weapon.weaponClass.name, weapon.ammoCount]
                else:
                    label.text = weapon.weaponClass.name
                    
                # Update name display
                if show_weapon_names and i < primary_name_labels.size():
                    primary_name_labels[i].text = weapon.weaponClass.name
                    
    func update_secondary_weapons():
        # Update secondary weapon display
        var secondary_weapons = player_ship.weaponSystem.secondaryWeapons
        for i in range(secondary_weapons.size()):
            if i < secondary_ammo_labels.size():
                var weapon = secondary_weapons[i]
                var label = secondary_ammo_labels[i]
                
                # Update ammo display
                if show_ammo:
                    label.text = "%s: %d" % [weapon.weaponClass.name, weapon.ammoCount]
                else:
                    label.text = weapon.weaponClass.name
                    
                # Update name display
                if show_weapon_names and i < secondary_name_labels.size():
                    secondary_name_labels[i].text = weapon.weaponClass.name
                    
    func update_weapon_cooldowns(delta: float):
        # Update weapon cooldown displays
        update_primary_cooldowns(delta)
        update_secondary_cooldowns(delta)
        
    func update_primary_cooldowns(delta: float):
        # Update primary weapon cooldowns
        var primary_weapons = player_ship.weaponSystem.primaryWeapons
        for i in range(min(primary_weapons.size(), primary_cooldown_bars.size())):
            var weapon = primary_weapons[i]
            var bar = primary_cooldown_bars[i]
            
            if show_cooldown:
                if weapon.cooldownTimer > 0:
                    var cooldown_progress = 1.0 - (weapon.cooldownTimer / weapon.weaponClass.fireRate)
                    bar.value = cooldown_progress * 100
                    bar.visible = true
                else:
                    bar.value = 100
                    bar.visible = false
                    
    func update_secondary_cooldowns(delta: float):
        # Update secondary weapon cooldowns
        var secondary_weapons = player_ship.weaponSystem.secondaryWeapons
        for i in range(min(secondary_weapons.size(), secondary_cooldown_bars.size())):
            var weapon = secondary_weapons[i]
            var bar = secondary_cooldown_bars[i]
            
            if show_cooldown:
                if weapon.cooldownTimer > 0:
                    var cooldown_progress = 1.0 - (weapon.cooldownTimer / weapon.weaponClass.fireRate)
                    bar.value = cooldown_progress * 100
                    bar.visible = true
                else:
                    bar.value = 100
                    bar.visible = false
                    
    func set_show_ammo(show: bool):
        # Set ammo display visibility
        show_ammo = show
        # Update display
        
    func set_show_cooldown(show: bool):
        # Set cooldown display visibility
        show_cooldown = show
        # Update display
        
    func set_show_weapon_names(show: bool):
        # Set weapon name display visibility
        show_weapon_names = show
        # Update display
        
    func set_compact_mode(compact: bool):
        # Set compact display mode
        compact_mode = compact
        # Update display layout
        
    func get_ammo_count(weapon_index: int, is_primary: bool) -> int:
        # Get ammo count for weapon
        if player_ship == null or player_ship.weaponSystem == null:
            return 0
            
        var weapons = player_ship.weaponSystem.primaryWeapons if is_primary else player_ship.weaponSystem.secondaryWeapons
        if weapon_index >= 0 and weapon_index < weapons.size():
            return weapons[weapon_index].ammoCount
        return 0
        
    func get_weapon_name(weapon_index: int, is_primary: bool) -> String:
        # Get name of weapon
        if player_ship == null or player_ship.weaponSystem == null:
            return "Unknown"
            
        var weapons = player_ship.weaponSystem.primaryWeapons if is_primary else player_ship.weaponSystem.secondaryWeapons
        if weapon_index >= 0 and weapon_index < weapons.size():
            return weapons[weapon_index].weaponClass.name
        return "Unknown"
        
    func is_weapon_ready(weapon_index: int, is_primary: bool) -> bool:
        # Check if weapon is ready to fire
        if player_ship == null or player_ship.weaponSystem == null:
            return false
            
        var weapons = player_ship.weaponSystem.primaryWeapons if is_primary else player_ship.weaponSystem.secondaryWeapons
        if weapon_index >= 0 and weapon_index < weapons.size():
            return weapons[weapon_index].cooldownTimer <= 0
        return false

# Target display HUD element
class TargetDisplay extends HUDElement:
    # Target display components
    var target_name: Label = null
    var target_type: Label = null
    var target_health_bar: ProgressBar = null
    var target_subsystem_list: VBoxContainer = null
    var target_distance: Label = null
    var target_speed: Label = null
    var target_escort_list: VBoxContainer = null
    
    # Target information
    var current_target: Node3D = null
    var target_subsystems: Array[Subsystem] = []
    var target_escorts: Array[Ship] = []
    
    # Display settings
    var show_subsystems: bool = true
    var show_escorts: bool = true
    var show_target_distance: bool = true
    var show_target_speed: bool = true
    var target_update_frequency: float = 0.5  # Update every 500ms
    
    func _ready():
        # Initialize target display
        element_name = "TargetDisplay"
        initialize_target_display()
        
    func initialize_target_display():
        # Initialize target display components
        target_name = $TargetInfo/TargetName
        target_type = $TargetInfo/TargetType
        target_health_bar = $TargetInfo/TargetHealth
        target_subsystem_list = $TargetSubsystems
        target_distance = $TargetDistance
        target_speed = $TargetSpeed
        target_escort_list = $TargetEscorts
        
    func update_element(delta: float):
        # Update target display
        if player_ship == null:
            return
            
        // Update target information
        update_target_info(delta)
        
        // Update subsystem information
        update_subsystem_info()
        
        // Update escort information
        update_escort_info()
        
        // Update target metrics
        update_target_metrics()
        
    func update_target_info(delta: float):
        // Update current target display
        var target = player_ship.currentTarget
        if target != current_target:
            current_target = target
            update_target_identity()
            
        if current_target != null:
            update_target_health()
            
    func update_target_identity():
        // Update target identity display
        if current_target == null:
            if target_name != null:
                target_name.text = "No Target"
            if target_type != null:
                target_type.text = ""
            if target_health_bar != null:
                target_health_bar.value = 0
            return
            
        // Determine target type
        var target_class = "Unknown"
        var target_name_text = "Unknown"
        
        if current_target is Ship:
            var ship = current_target as Ship
            target_class = "Ship"
            target_name_text = ship.shipClass.name
            
        elif current_target is Asteroid:
            target_class = "Asteroid"
            target_name_text = "Asteroid"
            
        else:
            target_class = "Object"
            target_name_text = current_target.name
            
        // Update display
        if target_name != null:
            target_name.text = target_name_text
        if target_type != null:
            target_type.text = target_class
            
    func update_target_health():
        // Update target health display
        if current_target == null or target_health_bar == null:
            return
            
        var health_percent = 100.0
        if current_target is Ship:
            var ship = current_target as Ship
            health_percent = (ship.hullStrength / ship.shipClass.maxHullStrength) * 100
            
        target_health_bar.value = health_percent
        
    func update_subsystem_info():
        // Update subsystem information display
        if not show_subsystems or current_target == null or not (current_target is Ship):
            return
            
        var ship = current_target as Ship
        target_subsystems = ship.subsystems
        
        // Update subsystem list display
        if target_subsystem_list != null:
            for child in target_subsystem_list.get_children():
                child.queue_free()
                
            for subsystem in target_subsystems:
                var subsystem_label = Label.new()
                var subsystem_text = subsystem.template.name
                if not subsystem.isDestroyed:
                    subsystem_text += " (%.0f%%)" % ((subsystem.health / subsystem.template.maxHealth) * 100)
                else:
                    subsystem_text += " [DESTROYED]"
                subsystem_label.text = subsystem_text
                target_subsystem_list.add_child(subsystem_label)
                
    func update_escort_info():
        // Update escort information display
        if not show_escorts or player_ship == null:
            return
            
        // Get player's escorts (would interface with wing system)
        target_escorts = get_player_escorts()
        
        // Update escort list display
        if target_escort_list != null:
            for child in target_escort_list.get_children():
                child.queue_free()
                
            for escort in target_escorts:
                var escort_label = Label.new()
                escort_label.text = escort.shipClass.name
                target_escort_list.add_child(escort_label)
                
    func get_player_escorts() -> Array[Ship]:
        // Get player's escort ships
        var escorts = []
        if player_ship != null and player_ship.wing != null:
            for wingman in player_ship.wing.spawnedShips:
                if wingman != player_ship:  // Exclude player
                    escorts.append(wingman)
        return escorts
        
    func update_target_metrics():
        // Update target metrics display
        if current_target == null or player_ship == null:
            return
            
        // Calculate distance
        var distance = player_ship.global_position.distance_to(current_target.global_position)
        if target_distance != null and show_target_distance:
            target_distance.text = "Distance: %.0fm" % distance
            
        // Calculate speed
        var relative_speed = 0.0
        if current_target is Ship and (current_target as Ship).physicsController != null:
            var escort_ship = current_target as Ship
            var player_speed = player_ship.physicsController.get_velocity_magnitude()
            var escort_speed = escort_ship.physicsController.get_velocity_magnitude()
            relative_speed = abs(player_speed - escort_speed)
            
        if target_speed != null and show_target_speed:
            target_speed.text = "Speed: %.0fm/s" % relative_speed
            
    func set_show_subsystems(show: bool):
        // Set subsystem display visibility
        show_subsystems = show
        if target_subsystem_list != null:
            target_subsystem_list.visible = show
            
    func set_show_escorts(show: bool):
        // Set escort display visibility
        show_escorts = show
        if target_escort_list != null:
            target_escort_list.visible = show
            
    func set_show_target_distance(show: bool):
        // Set target distance display visibility
        show_target_distance = show
        if target_distance != null:
            target_distance.visible = show
            
    func set_show_target_speed(show: bool):
        // Set target speed display visibility
        show_target_speed = show
        if target_speed != null:
            target_speed.visible = show
            
    func set_target_update_frequency(frequency: float):
        // Set target update frequency
        target_update_frequency = max(frequency, 0.1)  // Minimum 100ms
        
    func get_target_update_frequency() -> float:
        // Get target update frequency
        return target_update_frequency
        
    func get_current_target() -> Node3D:
        // Get current target
        return current_target
        
    func get_target_subsystems() -> Array[Subsystem]:
        // Get target subsystems
        return target_subsystems
        
    func get_target_escorts() -> Array[Ship]:
        // Get target escorts
        return target_escorts
        
    func set_target(target: Node3D):
        // Set target display
        current_target = target
        update_target_identity()
        update_target_health()
        
    func refresh_display():
        // Refresh target display
        update_target_info(0.0)
        update_subsystem_info()
        update_escort_info()
        update_target_metrics()

# Message display HUD element
class MessageDisplay extends HUDElement:
    // Message queue
    var message_queue: Array[HUDMessage] = []
    var active_messages: Array[HUDMessage] = []
    var max_messages: int = 5
    
    // UI elements
    var message_container: VBoxContainer = null
    var message_labels: Array[Label] = []
    
    // Message types
    enum MessageType { INFO, WARNING, ERROR, COMBAT, COMM, OBJECTIVE }
    
    // Message structure
    class HUDMessage:
        var text: String = ""
        var type: MessageType = MessageType.INFO
        var timestamp: float = 0.0
        var duration: float = 5.0
        var color: Color = Color.WHITE
        var is_fading: bool = false
        var fade_start_time: float = 0.0
        
        func _init(msg_text: String, msg_type: MessageType, msg_duration: float, msg_color: Color):
            text = msg_text
            type = msg_type
            duration = msg_duration
            color = msg_color
            timestamp = Time.get_ticks_msec() / 1000.0
            
    func _ready():
        // Initialize message display
        element_name = "MessageDisplay"
        initialize_message_display()
        
    func initialize_message_display():
        // Initialize message display components
        message_container = $MessageContainer
        // Initialize message labels
        
    func _process(delta):
        // Update message display
        update_messages(delta)
        
    func update_messages(delta: float):
        // Update message displays
        if player_ship == null:
            return
            
        // Process message queue
        process_message_queue()
        
        // Update active messages
        update_active_messages()
        
        // Clean up expired messages
        cleanup_expired_messages()
        
    func process_message_queue():
        // Process messages in queue
        while not message_queue.is_empty():
            var message = message_queue.pop_front()
            add_message_to_display(message)
            
    func add_message_to_display(message: HUDMessage):
        // Add message to active display
        if active_messages.size() >= max_messages:
            // Remove oldest message
            var oldest = active_messages.pop_front()
            remove_message_display(oldest)
            
        active_messages.append(message)
        create_message_display(message)
        
    func create_message_display(message: HUDMessage):
        // Create visual display for message
        var message_label = Label.new()
        message_label.text = message.text
        message_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        message_label.custom_minimum_size = Vector2(300, 0)
        message_label.modulate = message.color
        
        // Add to message container
        if message_container != null:
            message_container.add_child(message_label)
            message_labels.append(message_label)
            
    func remove_message_display(message: HUDMessage):
        // Remove message display
        for i in range(message_labels.size()):
            if i < message_labels.size():
                var label = message_labels[i]
                label.queue_free()
                message_labels.remove_at(i)
                break
                
    func update_active_messages():
        // Update active message displays (fading, etc.)
        var current_time = Time.get_ticks_msec() / 1000.0
        
        for i in range(active_messages.size()):
            var message = active_messages[i]
            if i < message_labels.size():
                var label = message_labels[i]
                
                // Check if message should start fading
                var message_age = current_time - message.timestamp
                if message_age >= (message.duration - 1.0):  // Start fading 1 second before expiry
                    if not message.is_fading:
                        message.is_fading = true
                        message.fade_start_time = current_time
                        
                // Apply fade effect
                if message.is_fading:
                    var fade_elapsed = current_time - message.fade_start_time
                    var fade_alpha = 1.0 - fade_elapsed
                    label.modulate = Color(message.color.r, message.color.g, message.color.b, fade_alpha)
                    
    func cleanup_expired_messages():
        // Remove expired messages
        var current_time = Time.get_ticks_misc() / 1000.0
        
        for i in range(active_messages.size() - 1, -1, -1):
            var message = active_messages[i]
            var message_age = current_time - message.timestamp
            
            if message_age >= message.duration:
                remove_message_display(message)
                active_messages.remove_at(i)
                
    func add_message(text: String, message_type: MessageType = MessageType.INFO, duration: float = 5.0, color: Color = Color.WHITE):
        // Add message to queue
        var message = HUDMessage.new(text, message_type, duration, color)
        message_queue.append(message)
        
        // Apply type-specific settings
        match message_type:
            MessageType.WARNING:
                message.color = Color.ORANGE
                message.duration = duration * 1.5
            MessageType.ERROR:
                message.color = Color.RED
                message.duration = duration * 2.0
            MessageType.COMBAT:
                message.color = Color.RED
                message.duration = duration * 1.2
            MessageType.COMM:
                message.color = Color.CYAN
            MessageType.OBJECTIVE:
                message.color = Color.GREEN
                message.duration = duration * 2.0
                
    func add_combat_message(text: String):
        // Add combat message
        add_message(text, MessageType.COMBAT, 4.0, Color.RED)
        
    func add_comm_message(text: String, sender: String = ""):
        // Add communication message
        var full_text = text
        if sender != "":
            full_text = "%s: %s" % [sender, text]
        add_message(full_text, MessageType.COMM, 6.0, Color.CYAN)
        
    func add_objective_message(text: String):
        // Add objective message
        add_message(text, MessageType.OBJECTIVE, 8.0, Color.GREEN)
        
    func add_system_message(text: String):
        // Add system message
        add_message(text, MessageType.INFO, 3.0, Color.YELLOW)
        
    func clear_messages():
        // Clear all messages
        for message in active_messages:
            remove_message_display(message)
        active_messages.clear()
        message_queue.clear()
        
    func set_max_messages(max_count: int):
        // Set maximum messages to display
        max_messages = max(max_count, 1)
        
    func get_max_messages() -> int:
        // Get maximum messages
        return max_messages
        
    func get_message_count() -> int:
        // Get active message count
        return active_messages.size()
        
    func get_queued_message_count() -> int:
        // Get queued message count
        return message_queue.size()
        
    func set_message_visibility(visible: bool):
        // Set message display visibility
        if message_container != null:
            message_container.visible = visible
            
    func is_message_visible() -> bool:
        // Check if message display is visible
        if message_container != null:
            return message_container.visible
        return true
        
    func cleanup():
        // Clean up message display
        clear_messages()
        message_labels.clear()

# Radar contact representation
class RadarContact:
    // Contact properties
    var position: Vector3 = Vector3.ZERO
    var type: String = "UNKNOWN"  // FRIENDLY, HOSTILE, NEUTRAL, ASTEROID, WEAPON
    var is_selected: bool = false
    var threat_level: int = 0  // 0-10 threat level
    var is_damaged: bool = false
    var is_destroyed: bool = false
    
    // Display properties
    var display_position: Vector2 = Vector2.ZERO
    var display_size: float = 4.0
    var display_color: Color = Color.WHITE
    var is_flashing: bool = false
    var flash_timer: float = 0.0
    
    func _init(contact_position: Vector3, contact_type: String):
        position = contact_position
        type = contact_type
        
    func update_display(radar_system: RadarSystem):
        // Update display properties based on contact properties
        display_position = radar_system.world_to_radar(position)
        display_color = get_contact_color()
        display_size = get_contact_size()
        
    func get_contact_color() -> Color:
        // Get contact color based on type
        match type:
            "FRIENDLY":
                return Color.GREEN
            "HOSTILE":
                return Color.RED
            "NEUTRAL":
                return Color.YELLOW
            "ASTEROID":
                return Color.GRAY
            "WEAPON":
                return Color.CYAN
            _:
                return Color.WHITE
                
    func get_contact_size() -> float:
        // Get contact size based on type and properties
        var size = 4.0
        match type:
            "HOSTILE":
                // Increase size for high threat levels
                size += threat_level * 0.5
            "WEAPON":
                // Smaller size for weapons
                size = 2.0
                
        // Increase size for selected contacts
        if is_selected:
            size *= 1.5
            
        return size
        
    func update_flash(delta: float):
        // Update flash animation
        if is_flashing:
            flash_timer += delta
            if flash_timer >= 0.5:  // Flash duration
                is_flashing = false
                flash_timer = 0.0
                
    func start_flash():
        // Start flash animation
        is_flashing = true
        flash_timer = 0.0
        
    func is_flashing_now() -> bool:
        // Check if contact is currently flashing
        return is_flashing
        
    func get_flash_alpha() -> float:
        // Get flash alpha for animation
        if is_flashing:
            // Create pulsing effect
            return 0.5 + 0.5 * sin(flash_timer * PI * 4)  // 2 flashes per second
        return 1.0
        
    func set_threat_level(level: int):
        // Set threat level for contact
        threat_level = clamp(level, 0, 10)
        
    func get_threat_level() -> int:
        // Get threat level
        return threat_level
        
    func set_selected(selected: bool):
        // Set selected state
        is_selected = selected
        
    func is_selected_contact() -> bool:
        // Check if contact is selected
        return is_selected
        
    func set_destroyed(destroyed: bool):
        // Set destroyed state
        is_destroyed = destroyed
        if destroyed:
            is_flashing = true
            flash_timer = 0.0
            
    func is_contact_destroyed() -> bool:
        // Check if contact is destroyed
        return is_destroyed
        
    func get_contact_type() -> String:
        // Get contact type
        return type
        
    func get_contact_position() -> Vector3:
        // Get contact position
        return position

# HUD element manager
class HUDElementManager extends Node:
    // Managed HUD elements
    var hud_elements: Dictionary = {}
    var active_elements: Array[String] = []
    
    // Element configuration
    var element_positions: Dictionary = {}
    var element_scales: Dictionary = {}
    var element_visibilities: Dictionary = {}
    
    // Player reference
    var player_ship: Ship = null
    
    func _ready():
        // Initialize HUD element manager
        initialize_manager()
        
    func initialize_manager():
        // Initialize HUD element manager
        load_element_configuration()
        
    func load_element_configuration():
        // Load element configuration from resources
        var config = preload("res://ui/hud/element_config.tres")
        if config != null:
            element_positions = config.positions
            element_scales = config.scales
            element_visibilities = config.visibilities
            
    func register_element(element_name: String, element: HUDElement):
        // Register HUD element
        hud_elements[element_name] = element
        active_elements.append(element_name)
        
        // Apply configuration
        if element_positions.has(element_name):
            element.set_position_offset(element_positions[element_name])
            
        if element_scales.has(element_name):
            element.set_scale(element_scales[element_name])
            
        if element_visibilities.has(element_name):
            element.set_visibility(element_visibilities[element_name])
            
        // Set player reference
        element.set_player_ship(player_ship)
        
    func unregister_element(element_name: String):
        // Unregister HUD element
        if hud_elements.has(element_name):
            hud_elements.erase(element_name)
            
        if active_elements.has(element_name):
            active_elements.erase(element_name)
            
    func show_element(element_name: String):
        // Show HUD element
        if hud_elements.has(element_name):
            var element = hud_elements[element_name] as HUDElement
            element.activate()
            element.set_visibility(true)
            
    func hide_element(element_name: String):
        // Hide HUD element
        if hud_elements.has(element_name):
            var element = hud_elements[element_name] as HUDElement
            element.deactivate()
            element.set_visibility(false)
            
    func toggle_element(element_name: String):
        // Toggle HUD element visibility
        if hud_elements.has(element_name):
            var element = hud_elements[element_name] as HUDElement
            element.toggle()
            
    func show_all_elements():
        // Show all registered elements
        for element_name in active_elements:
            show_element(element_name)
            
    func hide_all_elements():
        // Hide all registered elements
        for element_name in active_elements:
            hide_element(element_name)
            
    func set_element_visibility(element_name: String, visible: bool):
        // Set element visibility
        if visible:
            show_element(element_name)
        else:
            hide_element(element_name)
            
    func is_element_visible(element_name: String) -> bool:
        // Check if element is visible
        if hud_elements.has(element_name):
            var element = hud_elements[element_name] as HUDElement
            return element.is_element_visible()
        return false
        
    func set_element_position(element_name: String, position: Vector2):
        // Set element position
        if hud_elements.has(element_name):
            var element = hud_elements[element_name] as HUDElement
            element.set_position_offset(position)
            
        // Save position for configuration
        element_positions[element_name] = position
        
    func get_element_position(element_name: String) -> Vector2:
        // Get element position
        if element_positions.has(element_name):
            return element_positions[element_name]
        return Vector2.ZERO
        
    func set_element_scale(element_name: String, scale: float):
        // Set element scale
        if hud_elements.has(element_name):
            var element = hud_elements[element_name] as HUDElement
            element.set_scale(scale)
            
        // Save scale for configuration
        element_scales[element_name] = scale
        
    func get_element_scale(element_name: String) -> float:
        // Get element scale
        if element_scales.has(element_name):
            return element_scales[element_name]
        return 1.0
        
    func get_element(element_name: String) -> HUDElement:
        // Get HUD element
        return hud_elements.get(element_name, null)
        
    func get_elements() -> Array[String]:
        // Get all registered elements
        return active_elements.duplicate()
        
    func set_player_ship(ship: Ship):
        // Set player ship reference
        player_ship = ship
        
        // Update all elements with player ship
        for element_name in active_elements:
            if hud_elements.has(element_name):
                var element = hud_elements[element_name] as HUDElement
                element.set_player_ship(ship)
                
    func get_player_ship() -> Ship:
        // Get player ship reference
        return player_ship
        
    func save_configuration():
        // Save HUD element configuration
        var config = preload("res://ui/hud/element_config.tres").duplicate()
        config.positions = element_positions
        config.scales = element_scales
        config.visibilities = element_visibilities
        
        // Save to file
        ResourceSaver.save(config, "user://hud_config.tres")
        
    func load_configuration():
        // Load HUD element configuration
        var config = load("user://hud_config.tres")
        if config != null:
            element_positions = config.positions
            element_scales = config.scales
            element_visibilities = config.visibilities
            
    func reset_configuration():
        // Reset HUD element configuration
        element_positions.clear()
        element_scales.clear()
        element_visibilities.clear()
        load_element_configuration()
        
    func cleanup():
        // Clean up HUD element manager
        for element in hud_elements.values():
            if element is HUDElement:
                element.cleanup()
                
        hud_elements.clear()
        active_elements.clear()
        player_ship = null

# Enumeration of UI element types
enum UIElementType {
    BUTTON,
    LABEL,
    PROGRESS_BAR,
    SLIDER,
    CHECKBOX,
    RADIO_BUTTON,
    TEXT_FIELD,
    TEXT_AREA,
    LIST,
    DROPDOWN,
    PANEL,
    WINDOW,
    CUSTOM
}

# Base class for custom UI elements
class CustomUIElement extends Control:
    // Element properties
    var element_type: UIElementType = UIElementType.CUSTOM
    var element_name: String = "CustomElement"
    var element_tooltip: String = ""
    var element_enabled: bool = true
    
    // Theme properties
    var element_theme: Theme = null
    var element_style: String = "default"
    
    // Event handling
    var click_handlers: Array[Callable] = []
    var hover_handlers: Array[Callable] = []
    var focus_handlers: Array[Callable] = []
    
    // Animation
    var animations: Dictionary = {}
    var current_animation: String = ""
    
    func _ready():
        // Initialize custom UI element
        initialize_element()
        
    func initialize_element():
        // Common initialization for custom UI elements
        mouse_filter = Control.MOUSE_FILTER_STOP
        
    func _gui_input(event):
        // Handle GUI input events
        handle_gui_input(event)
        
    func handle_gui_input(event):
        // Handle GUI input events
        if event is InputEventMouseButton and event.pressed:
            if event.button_index == MOUSE_BUTTON_LEFT:
                on_clicked(event.position)
        elif event is InputEventMouseMotion:
            on_hovered(event.position)
            
    func on_clicked(position: Vector2):
        // Handle click event
        for handler in click_handlers:
            if handler.is_valid():
                handler.call(position)
                
    func on_hovered(position: Vector2):
        // Handle hover event
        for handler in hover_handlers:
            if handler.is_valid():
                handler.call(position)
                
    func on_focused():
        // Handle focus event
        for handler in focus_handlers:
            if handler.is_valid():
                handler.call()
                
    func add_click_handler(handler: Callable):
        // Add click event handler
        click_handlers.append(handler)
        
    func remove_click_handler(handler: Callable):
        // Remove click event handler
        if click_handlers.has(handler):
            click_handlers.erase(handler)
            
    func add_hover_handler(handler: Callable):
        // Add hover event handler
        hover_handlers.append(handler)
        
    func remove_hover_handler(handler: Callable):
        // Remove hover event handler
        if hover_handlers.has(handler):
            hover_handlers.erase(handler)
            
    func add_focus_handler(handler: Callable):
        // Add focus event handler
        focus_handlers.append(handler)
        
    func remove_focus_handler(handler: Callable):
        // Remove focus event handler
        if focus_handlers.has(handler):
            focus_handlers.erase(handler)
            
    func set_tooltip(tooltip: String):
        // Set element tooltip
        element_tooltip = tooltip
        hint_tooltip = tooltip
        
    func get_tooltip() -> String:
        // Get element tooltip
        return element_tooltip
        
    func set_enabled(enabled: bool):
        // Set element enabled state
        element_enabled = enabled
        mouse_filter = Control.MOUSE_FILTER_STOP if enabled else Control.MOUSE_FILTER_IGNORE
        
    func is_enabled() -> bool:
        // Check if element is enabled
        return element_enabled
        
    func set_theme(theme: Theme):
        // Set element theme
        element_theme = theme
        self.theme = theme
        
    func get_theme() -> Theme:
        // Get element theme
        return element_theme
        
    func set_style(style: String):
        // Set element style
        element_style = style
        // Apply style to element
        
    func get_style() -> String:
        // Get element style
        return element_style
        
    func add_animation(animation_name: String, animation: Animation):
        // Add animation to element
        animations[animation_name] = animation
        
    func play_animation(animation_name: String):
        // Play animation on element
        if animations.has(animation_name):
            current_animation = animation_name
            // Play animation
            
    func stop_animation():
        // Stop current animation
        current_animation = ""
        // Stop animation playback
        
    func is_animation_playing() -> bool:
        // Check if animation is currently playing
        return current_animation != ""
        
    func get_current_animation() -> String:
        // Get name of current animation
        return current_animation
        
    func get_animations() -> Array[String]:
        // Get all available animations
        return animations.keys()
        
    func set_element_name(name: String):
        // Set element name
        element_name = name
        
    func get_element_name() -> String:
        // Get element name
        return element_name
        
    func get_element_type() -> UIElementType:
        // Get element type
        return element_type
        
    func cleanup():
        // Clean up element
        click_handlers.clear()
        hover_handlers.clear()
        focus_handlers.clear()
        animations.clear()
        element_theme = null
        
    func _on_theme_changed():
        // Handle theme change
        update_theme()
        
    func update_theme():
        // Update element appearance based on theme
        if element_theme != null:
            // Apply theme properties to element
            pass
            
    func _on_size_flags_changed():
        // Handle size flag changes
        update_layout()
        
    func update_layout():
        // Update element layout
        // Override in subclasses
        
    func _on_minimum_size_changed():
        // Handle minimum size changes
        update_size()
        
    func update_size():
        // Update element size
        // Override in subclasses

// Custom button element
class CustomButton extends CustomUIElement:
    // Button properties
    var button_text: String = "Button"
    var button_icon: Texture2D = null
    var button_style_normal: StyleBox = null
    var button_style_hover: StyleBox = null
    var button_style_pressed: StyleBox = null
    var button_style_disabled: StyleBox = null
    
    // Button states
    var is_pressed: bool = false
    var is_hovered: bool = false
    var is_disabled: bool = false
    
    // Button events
    signal button_pressed()
    signal button_released()
    signal button_hovered()
    signal button_unhovered()
    
    func _ready():
        // Initialize button
        element_type = UIElementType.BUTTON
        element_name = "CustomButton"
        initialize_button()
        
    func initialize_button():
        // Initialize button properties
        mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
        
    func _draw():
        // Draw button
        draw_button_background()
        draw_button_contents()
        
    func draw_button_background():
        // Draw button background based on state
        var style = get_current_style()
        if style != null:
            draw_style_box(style, Rect2(Vector2.ZERO, size))
            
    func draw_button_contents():
        // Draw button contents (text, icon, etc.)
        if button_icon != null:
            // Draw icon
            draw_texture(button_icon, Vector2(5, (size.y - button_icon.get_height()) / 2))
            
        if button_text != "":
            // Draw text
            var text_position = Vector2(5, 0)
            if button_icon != null:
                text_position.x = button_icon.get_width() + 10
                
            draw_string(get_theme_font("font"), text_position, button_text, HORIZONTAL_ALIGNMENT_LEFT, 
                       size.x - text_position.x, get_theme_font_size("font_size"), get_theme_color("font_color"))
                       
    func get_current_style() -> StyleBox:
        // Get current button style based on state
        if is_disabled:
            return button_style_disabled
        elif is_pressed:
            return button_style_pressed
        elif is_hovered:
            return button_style_hover
        else:
            return button_style_normal
            
    func set_text(text: String):
        // Set button text
        button_text = text
        update_minimum_size()
        queue_redraw()
        
    func get_text() -> String:
        // Get button text
        return button_text
        
    func set_icon(icon: Texture2D):
        // Set button icon
        button_icon = icon
        update_minimum_size()
        queue_redraw()
        
    func get_icon() -> Texture2D:
        // Get button icon
        return button_icon
        
    func set_disabled(disabled: bool):
        // Set button disabled state
        is_disabled = disabled
        set_enabled(not disabled)
        queue_redraw()
        
    func is_button_disabled() -> bool:
        // Check if button is disabled
        return is_disabled
        
    func set_pressed(pressed: bool):
        // Set button pressed state
        is_pressed = pressed
        queue_redraw()
        
    func is_button_pressed() -> bool:
        // Check if button is pressed
        return is_pressed
        
    func update_minimum_size():
        // Update minimum size based on contents
        var min_width = 20  // Minimum button width
        var min_height = 20  // Minimum button height
        
        // Add space for text
        if button_text != "":
            min_width += get_theme_font("font").get_string_size(button_text, HORIZONTAL_ALIGNMENT_LEFT, 
                                                               -1, get_theme_font_size("font_size")).x
                                                               
        // Add space for icon
        if button_icon != null:
            min_width += button_icon.get_width() + 10
            min_height = max(min_height, button_icon.get_height() + 10)
            
        custom_minimum_size = Vector2(min_width, min_height)
        
    func _on_mouse_entered():
        // Handle mouse enter
        is_hovered = true
        emit_signal("button_hovered")
        queue_redraw()
        
    func _on_mouse_exited():
        // Handle mouse exit
        is_hovered = false
        emit_signal("button_unhovered")
        queue_redraw()
        
    func _on_gui_input(event):
        // Handle GUI input
        if event is InputEventMouseButton:
            if event.button_index == MOUSE_BUTTON_LEFT:
                if event.pressed:
                    is_pressed = true
                    emit_signal("button_pressed")
                else:
                    is_pressed = false
                    emit_signal("button_released")
                queue_redraw()
                
    func _notification(what):
        // Handle notifications
        match what:
            NOTIFICATION_THEME_CHANGED:
                update_theme()
            NOTIFICATION_RESIZED:
                queue_redraw()
                
    func update_theme():
        // Update button theme
        super.update_theme()
        
        // Get theme styles
        button_style_normal = get_theme_stylebox("normal", "Button")
        button_style_hover = get_theme_stylebox("hover", "Button")
        button_style_pressed = get_theme_stylebox("pressed", "Button")
        button_style_disabled = get_theme_stylebox("disabled", "Button")
        
        // Update appearance
        queue_redraw()

// Custom slider element
class CustomSlider extends CustomUIElement:
    // Slider properties
    var min_value: float = 0.0
    var max_value: float = 100.0
    var current_value: float = 50.0
    var step: float = 1.0
    var orientation: int = HORIZONTAL
    
    // Slider appearance
    var slider_style: StyleBox = null
    var grabber_style: StyleBox = null
    var tick_count: int = 0
    var ticks_on_borders: bool = false
    
    // Slider events
    signal value_changed(value: float)
    signal drag_started(value: float)
    event drag_ended(value: float)
    
    func _ready():
        // Initialize slider
        element_type = UIElementType.SLIDER
        element_name = "CustomSlider"
        initialize_slider()
        
    func initialize_slider():
        // Initialize slider properties
        mouse_filter = Control.MOUSE_FILTER_STOP
        
    func _draw():
        // Draw slider
        draw_slider_background()
        draw_slider_grabber()
        draw_slider_ticks()
        
    func draw_slider_background():
        // Draw slider background
        if slider_style != null:
            draw_style_box(slider_style, Rect2(Vector2.ZERO, size))
            
    func draw_slider_grabber():
        // Draw slider grabber
        if grabber_style != null:
            var grabber_rect = get_grabber_rect()
            draw_style_box(grabber_style, grabber_rect)
            
    func draw_slider_ticks():
        // Draw slider ticks
        if tick_count > 0:
            var tick_step = size.x / tick_count
            for i in range(tick_count + 1):
                var tick_position = i * tick_step
                draw_line(Vector2(tick_position, 0), Vector2(tick_position, size.y), Color.WHITE, 1.0)
                
    func get_grabber_rect() -> Rect2:
        // Get rectangle for grabber
        var grabber_size = Vector2(10, size.y)  // Default grabber size
        if orientation == VERTICAL:
            grabber_size = Vector2(size.x, 10)
            
        var grabber_position = Vector2.ZERO
        var value_ratio = (current_value - min_value) / (max_value - min_value)
        
        if orientation == HORIZONTAL:
            grabber_position.x = value_ratio * (size.x - grabber_size.x)
        else:
            grabber_position.y = value_ratio * (size.y - grabber_size.y)
            
        return Rect2(grabber_position, grabber_size)
        
    func set_min_value(value: float):
        // Set minimum value
        min_value = value
        if current_value < min_value:
            current_value = min_value
            emit_signal("value_changed", current_value)
        queue_redraw()
        
    func get_min_value() -> float:
        // Get minimum value
        return min_value
        
    func set_max_value(value: float):
        // Set maximum value
        max_value = value
        if current_value > max_value:
            current_value = max_value
            emit_signal("value_changed", current_value)
        queue_redraw()
        
    func get_max_value() -> float:
        // Get maximum value
        return max_value
        
    func set_value(value: float):
        // Set current value
        var old_value = current_value
        current_value = clamp(value, min_value, max_value)
        if current_value != old_value:
            emit_signal("value_changed", current_value)
        queue_redraw()
        
    func get_value() -> float:
        // Get current value
        return current_value
        
    func set_step(step_value: float):
        // Set step value
        step = step_value
        
    func get_step() -> float:
        // Get step value
        return step
        
    func set_orientation(orientation_value: int):
        // Set slider orientation
        orientation = orientation_value
        queue_redraw()
        
    func get_orientation() -> int:
        // Get slider orientation
        return orientation
        
    func set_tick_count(count: int):
        // Set tick count
        tick_count = max(count, 0)
        queue_redraw()
        
    func get_tick_count() -> int:
        // Get tick count
        return tick_count
        
    func _gui_input(event):
        // Handle GUI input
        if event is InputEventMouseButton:
            if event.button_index == MOUSE_BUTTON_LEFT:
                if event.pressed:
                    emit_signal("drag_started", current_value)
                    handle_mouse_press(event.position)
                else:
                    emit_signal("drag_ended", current_value)
        elif event is InputEventMouseMotion:
            if Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
                handle_mouse_drag(event.position)
                
    func handle_mouse_press(position: Vector2):
        // Handle mouse press
        var value_ratio = 0.0
        if orientation == HORIZONTAL:
            value_ratio = position.x / size.x
        else:
            value_ratio = position.y / size.y
            
        var new_value = min_value + value_ratio * (max_value - min_value)
        new_value = stepify(new_value, step)
        set_value(new_value)
        
    func handle_mouse_drag(position: Vector2):
        // Handle mouse drag
        handle_mouse_press(position)
        
    func _notification(what):
        // Handle notifications
        match what:
            NOTIFICATION_THEME_CHANGED:
                update_theme()
            NOTIFICATION_RESIZED:
                queue_redraw()
                
    func update_theme():
        // Update slider theme
        super.update_theme()
        
        // Get theme styles
        slider_style = get_theme_stylebox("slider", "Slider")
        grabber_style = get_theme_stylebox("grabber", "Slider")
        
        // Update appearance
        queue_redraw()

// HUD element factory for creating HUD elements
class HUDElementFactory extends Node:
    // Available element types
    var element_types: Dictionary = {
        "weapon_display": WeaponDisplay,
        "target_display": TargetDisplay,
        "message_display": MessageDisplay,
        "radar_display": RadarSystem,
        "energy_display": EnergyDisplay,
        "subsystem_display": SubsystemDisplay,
        "objective_display": ObjectiveDisplay,
        "countermeasure_display": CountermeasureDisplay,
        "wingman_display": WingmanDisplay,
        "afterburner_display": AfterburnerDisplay,
        "glide_display": GlideDisplay,
        "auto_pilot_display": AutoPilotDisplay,
        "missile_lock_display": MissileLockDisplay,
        "damage_indicator": DamageIndicator,
        "reticle": Reticle,
        "speed_indicator": SpeedIndicator,
        "altitude_indicator": AltitudeIndicator,
        "comm_display": CommunicationDisplay
    }
    
    func _ready():
        // Initialize factory
        initialize_factory()
        
    func initialize_factory():
        // Initialize element factory
        pass
        
    func create_element(element_type: String, player_ship: Ship = null) -> HUDElement:
        // Create HUD element of specified type
        if element_types.has(element_type):
            var element_class = element_types[element_type]
            var element = element_class.new()
            element.element_name = element_type
            
            // Set player reference if provided
            if player_ship != null:
                element.set_player_ship(player_ship)
                
            return element
            
        return null
        
    func get_available_element_types() -> Array[String]:
        // Get available element types
        return element_types.keys()
        
    func register_element_type(type_name: String, type_class: GDScript):
        // Register new element type
        element_types[type_name] = type_class
        
    func unregister_element_type(type_name: String):
        // Unregister element type
        if element_types.has(type_name):
            element_types.erase(type_name)
            
    func create_default_hud(player_ship: Ship) -> Array[HUDElement]:
        // Create default HUD with standard elements
        var hud_elements = []
        
        // Create standard HUD elements
        var elements_to_create = [
            "weapon_display",
            "target_display", 
            "message_display",
            "radar_display",
            "energy_display",
            "subsystem_display",
            "objective_display",
            "countermeasure_display",
            "wingman_display",
            "damage_indicator",
            "reticle",
            "speed_indicator",
            "altitude_indicator",
            "comm_display"
        ]
        
        for element_type in elements_to_create:
            var element = create_element(element_type, player_ship)
            if element != null:
                hud_elements.append(element)
                
        return hud_elements
        
    func create_minimal_hud(player_ship: Ship) -> Array[HUDElement]:
        // Create minimal HUD with essential elements
        var hud_elements = []
        
        // Create minimal HUD elements
        var elements_to_create = [
            "reticle",
            "message_display",
            "damage_indicator"
        ]
        
        for element_type in elements_to_create:
            var element = create_element(element_type, player_ship)
            if element != null:
                hud_elements.append(element)
                
        return hud_elements
        
    func create_full_hud(player_ship: Ship) -> Array[HUDElement]:
        // Create full HUD with all elements
        var hud_elements = []
        
        // Create all available HUD elements
        for element_type in element_types.keys():
            var element = create_element(element_type, player_ship)
            if element != null:
                hud_elements.append(element)
                
        return hud_elements
        
    func get_element_description(element_type: String) -> String:
        // Get description for element type
        match element_type:
            "weapon_display":
                return "Displays weapon status and ammunition"
            "target_display":
                return "Shows target information and health"
            "message_display":
                return "Displays combat messages and alerts"
            "radar_display":
                return "Shows nearby contacts and threats"
            "energy_display":
                return "Displays energy distribution"
            "subsystem_display":
                return "Shows subsystem status"
            "objective_display":
                return "Displays mission objectives"
            "countermeasure_display":
                return "Shows countermeasure status"
            "wingman_display":
                return "Displays wingman status"
            "damage_indicator":
                return "Shows damage effects and warnings"
            "reticle":
                return "Aiming reticle and targeting"
            "speed_indicator":
                return "Displays current speed"
            "altitude_indicator":
                return "Displays altitude information"
            "comm_display":
                return "Displays communications"
            _:
                return "Custom HUD element"
                
    func get_element_default_position(element_type: String) -> Vector2:
        // Get default position for element type
        match element_type:
            "weapon_display":
                return Vector2(10, 10)
            "target_display":
                return Vector2(10, 200)
            "message_display":
                return Vector2(10, 400)
            "radar_display":
                return Vector2(600, 10)
            "energy_display":
                return Vector2(10, 300)
            "subsystem_display":
                return Vector2(10, 250)
            "objective_display":
                return Vector2(10, 450)
            "countermeasure_display":
                return Vector2(10, 500)
            "wingman_display":
                return Vector2(10, 550)
            "damage_indicator":
                return Vector2(400, 300)
            "reticle":
                return Vector2(384, 288)  // Center of 768x576 screen
            "speed_indicator":
                return Vector2(10, 100)
            "altitude_indicator":
                return Vector2(10, 150)
            "comm_display":
                return Vector2(10, 600)
            _:
                return Vector2.ZERO
                
    func get_element_default_scale(element_type: String) -> float:
        // Get default scale for element type
        return 1.0

// Communication message structure
class CommunicationMessage extends Resource:
    // Message properties
    @export var sender: String = ""
    @export var message: String = ""
    @export var timestamp: float = 0.0
    @export var priority: int = 0  // Higher priority messages shown first
    @export var message_type: String = "COMM"  // COMM, ALERT, OBJECTIVE
    @export var is_read: bool = false
    @export var is_important: bool = false
    
    func _init():
        timestamp = Time.get_ticks_msec() / 1000.0
        
    func mark_as_read():
        // Mark message as read
        is_read = true
        
    func is_message_read() -> bool:
        // Check if message has been read
        return is_read
        
    func set_important(important: bool):
        // Set message importance
        is_important = important
        
    func is_message_important() -> bool:
        // Check if message is important
        return is_important or priority > 50
        
    func get_display_time() -> String:
        // Get formatted display time
        var datetime = Time.get_datetime_dict_from_system()
        return "%02d:%02d" % [datetime.hour, datetime.minute]
        
    func get_formatted_message() -> String:
        // Get formatted message text
        var formatted = ""
        if sender != "":
            formatted = "%s: " % sender
        formatted += message
        return formatted
        
    func get_message_color() -> Color:
        // Get color based on message type
        match message_type:
            "ALERT":
                return Color.RED
            "OBJECTIVE":
                return Color.GREEN
            "WARNING":
                return Color.ORANGE
            _:
                return Color.WHITE
                
    func get_message_icon() -> Texture2D:
        // Get icon based on message type
        match message_type:
            "ALERT":
                return preload("res://ui/icons/alert.png")
            "OBJECTIVE":
                return preload("res://ui/icons/objective.png")
            "WARNING":
                return preload("res://ui/icons/warning.png")
            _:
                return preload("res://ui/icons/comm.png")
                
    func is_message_expired() -> bool:
        // Check if message has expired
        var current_time = Time.get_ticks_msec() / 1000.0
        return (current_time - timestamp) > 300  // Expire after 5 minutes
        
    func get_message_priority() -> int:
        // Get message priority
        return priority
        
    func set_message_priority(priority_value: int):
        // Set message priority
        priority = priority_value