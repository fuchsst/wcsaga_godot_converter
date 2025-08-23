# UI Module

## Purpose
The UI Module provides all user interface functionality, including menus, HUD elements, briefing screens, debriefing displays, and in-game information panels. It handles both the foundational UI framework and specific game UI screens.

## Components
- **UI System** (`ui/`): Foundational user interface framework
- **Menu UI** (`menuui/`): Main menu and options interface elements
- **Mission UI** (`missionui/`): Mission-specific interface elements
- **HUD System** (`hud/`): In-game information display
- **Radar System** (`radar/`): Tactical object tracking display
- **Control Configuration** (`controlconfig/`): Input mapping and settings

## Dependencies
- **Core Entity Module**: UI displays information about game objects
- **Ship Module**: Ship status and weapon information
- **Weapon Module**: Weapon status display
- **Mission Module**: Mission data and objectives
- **Player Module**: Player-specific information
- **Graphics Module**: Rendering functions

## C++ Components
- Window management and rendering
- Control creation and interaction
- Input handling for mouse and keyboard
- UI event processing system
- Widget and component framework
- Main menu rendering and navigation
- Options and configuration screens
- Briefing screen rendering and interaction
- Debriefing screen with mission results
- HUD rendering functions
- Radar display functions
- Control binding management

## Godot Equivalent Mapping

### Native GDScript Classes
```gdscript
# Base UI screen class
class UIScreen extends Control:
    var screenName: String
    var isActive: bool = false
    
    func show():
        visible = true
        isActive = true
        on_show()
        
    func hide():
        visible = false
        isActive = false
        on_hide()
        
    func on_show():
        # Override in subclasses
        pass
        
    func on_hide():
        # Override in subclasses
        pass
        
    func _input(event):
        # Handle input when screen is active
        if isActive:
            handle_input(event)
            
    func handle_input(event):
        # Override in subclasses
        pass

# Main menu screen
class MainMenuScreen extends UIScreen:
    @onready var newGameButton = $Buttons/NewGame
    @onready var loadGameButton = $Buttons/LoadGame
    @onready var optionsButton = $Buttons/Options
    @onready var quitButton = $Buttons/Quit
    
    func _ready():
        screenName = "MainMenu"
        newGameButton.connect("pressed", Callable(self, "_on_new_game_pressed"))
        loadGameButton.connect("pressed", Callable(self, "_on_load_game_pressed"))
        optionsButton.connect("pressed", Callable(self, "_on_options_pressed"))
        quitButton.connect("pressed", Callable(self, "_on_quit_pressed"))
        
    func _on_new_game_pressed():
        # Start new campaign
        GameManager.start_new_campaign()
        
    func _on_load_game_pressed():
        # Show load game screen
        UIManager.show_screen("LoadGame")
        
    func _on_options_pressed():
        # Show options screen
        UIManager.show_screen("Options")
        
    func _on_quit_pressed():
        # Quit game
        get_tree().quit()

# Options screen
class OptionsScreen extends UIScreen:
    @onready var graphicsSettings = $Settings/Graphics
    @onready var audioSettings = $Settings/Audio
    @onready var controlSettings = $Settings/Controls
    
    func _ready():
        screenName = "Options"
        # Initialize settings from config
        load_settings()
        
    func load_settings():
        # Load current settings from config file
        graphicsSettings.set_values(Config.graphics_settings)
        audioSettings.set_values(Config.audio_settings)
        controlSettings.set_values(Config.control_settings)
        
    func save_settings():
        # Save settings to config file
        Config.graphics_settings = graphicsSettings.get_values()
        Config.audio_settings = audioSettings.get_values()
        Config.control_settings = controlSettings.get_values()
        Config.save()

# HUD system for in-game display
class HUD extends CanvasLayer:
    @onready var hullBar = $HullBar
    @onready var shieldBar = $ShieldBar
    @onready var weaponDisplay = $WeaponDisplay
    @onready var targetDisplay = $TargetDisplay
    @onready var radar = $Radar
    @onready var messageLog = $MessageLog
    
    var playerShip: Ship
    
    func _ready():
        # Connect to game events
        GameManager.connect("ship_selected", Callable(self, "_on_ship_selected"))
        GameManager.connect("target_changed", Callable(self, "_on_target_changed"))
        
    func _process(delta):
        if playerShip != null:
            update_ship_status()
            
    func _on_ship_selected(ship: Ship):
        playerShip = ship
        update_ship_status()
        
    func update_ship_status():
        hullBar.value = playerShip.hullStrength / playerShip.shipClass.maxHullStrength
        shieldBar.value = playerShip.shieldStrength / playerShip.shipClass.maxShieldStrength
        weaponDisplay.update_weapons(playerShip.weapon_system)
        
    func _on_target_changed(target: Entity):
        targetDisplay.show_target(target)
        
    func add_message(message: String, color: Color = Color.WHITE):
        messageLog.add_message(message, color)

# Radar display
class RadarDisplay extends Control:
    var radarRange: float = 10000.0
    var contacts: Array[RadarContact]
    
    func _draw():
        # Draw radar background
        draw_circle(Vector2(size.x/2, size.y/2), min(size.x, size.y)/2, Color(0, 0, 1, 0.3))
        
        # Draw contacts
        for contact in contacts:
            var screenPos = world_to_radar(contact.position)
            var color = get_contact_color(contact)
            draw_circle(screenPos, 3, color)
            
    func world_to_radar(worldPos: Vector3) -> Vector2:
        # Convert 3D world position to 2D radar position
        var relativePos = worldPos - GameManager.player_ship.global_position
        var distance = relativePos.length()
        if distance > radarRange:
            # Position on edge of radar
            relativePos = relativePos.normalized() * radarRange
            
        # Project to 2D radar display
        var normalizedPos = relativePos / radarRange
        return Vector2(
            size.x/2 + normalizedPos.x * size.x/2,
            size.y/2 + normalizedPos.z * size.y/2
        )
        
    func get_contact_color(contact: RadarContact) -> Color:
        match contact.type:
            RadarContact.Type.FRIEND: return Color.GREEN
            RadarContact.Type.ENEMY: return Color.RED
            RadarContact.Type.NEUTRAL: return Color.YELLOW
            _: return Color.WHITE

# Radar contact data
class RadarContact:
    enum Type { FRIEND, ENEMY, NEUTRAL, ASTEROID }
    var position: Vector3
    var type: Type
    var is_selected: bool = false

# Weapon display panel
class WeaponDisplay extends HBoxContainer:
    @onready var primaryDisplay = $PrimaryWeapon
    @onready var secondaryDisplay = $SecondaryWeapon
    
    func update_weapons(weaponSystem: WeaponSystem):
        # Update primary weapon display
        if weaponSystem.primary_weapons.size() > 0:
            var weapon = weaponSystem.primary_weapons[0]
            primaryDisplay.text = "%s: %d" % [weapon.weaponClass.name, weapon.ammoCount]
            
        # Update secondary weapon display
        if weaponSystem.secondary_weapons.size() > 0:
            var weapon = weaponSystem.secondary_weapons[0]
            secondaryDisplay.text = "%s: %d" % [weapon.weaponClass.name, weapon.ammoCount]

# Target display panel
class TargetDisplay extends VBoxContainer:
    @onready var targetName = $TargetInfo/Name
    @onready var targetType = $TargetInfo/Type
    @onready var targetHealth = $TargetInfo/Health
    
    func show_target(target: Entity):
        if target is Ship:
            targetName.text = target.shipClass.name
            targetType.text = "Ship"
            targetHealth.value = target.hullStrength / target.shipClass.maxHullStrength
        elif target is Asteroid:
            targetName.text = "Asteroid"
            targetType.text = "Asteroid"
            targetHealth.value = 1.0  # Asteroids don't have health in this example
        else:
            targetName.text = "Unknown"
            targetType.text = "Unknown"
            targetHealth.value = 0.0

# UI manager for screen switching
class UIManager:
    var currentScreen: UIScreen
    var screens: Dictionary = {}
    
    func _ready():
        # Initialize all screens
        initialize_screens()
        
    func initialize_screens():
        # Load and register all UI screens
        screens["MainMenu"] = preload("res://ui/screens/main_menu.tscn").instantiate()
        screens["Options"] = preload("res://ui/screens/options.tscn").instantiate()
        screens["Briefing"] = preload("res://ui/screens/briefing.tscn").instantiate()
        screens["Debriefing"] = preload("res://ui/screens/debriefing.tscn").instantiate()
        
        # Add screens to scene tree
        for screen in screens.values():
            get_tree().root.add_child(screen)
            screen.hide()
            
    func show_screen(screenName: String):
        # Hide current screen
        if currentScreen != null:
            currentScreen.hide()
            
        # Show new screen
        if screens.has(screenName):
            currentScreen = screens[screenName]
            currentScreen.show()
            
    func hide_current_screen():
        if currentScreen != null:
            currentScreen.hide()
            currentScreen = null
```

### TSCN Scenes
```ini
[gd_scene load_steps=5 format=2]

[ext_resource path="res://ui/screens/main_menu.gd" type="Script" id=1]
[ext_resource path="res://ui/themes/main_menu_theme.tres" type="Theme" id=2]
[ext_resource path="res://ui/screens/main_menu_background.tscn" type="PackedScene" id=3]

[node name="MainMenu" type="Control"]
script = ExtResource(1)
theme = ExtResource(2)

[node name="Background" type="Node3D" parent="."]
instance = ExtResource(3)

[node name="Buttons" type="VBoxContainer" parent="."]
anchor_right = 1.0
anchor_bottom = 1.0
offset_left = 400.0
offset_top = 200.0
offset_right = -400.0
offset_bottom = -200.0

[node name="NewGame" type="Button" parent="Buttons"]
text = "New Campaign"

[node name="LoadGame" type="Button" parent="Buttons"]
text = "Load Game"

[node name="Options" type="Button" parent="Buttons"]
text = "Options"

[node name="Quit" type="Button" parent="Buttons"]
text = "Quit"
```

### TRES Resources
```ini
[gd_resource type="Theme" load_steps=3 format=2]

[ext_resource path="res://ui/fonts/title_font.tres" type="Font" id=1]
[ext_resource path="res://ui/fonts/body_font.tres" type="Font" id=2]

[resource]
button_styles/normal = SubResource(1)
button_styles/hover = SubResource(2)
button_styles/pressed = SubResource(3)
font = ExtResource(2)
font_color = Color(1, 1, 1, 1)
font_color_hover = Color(1, 1, 0, 1)
font_color_pressed = Color(0.8, 0.8, 0.8, 1)
```

### Implementation Notes
The UI Module in Godot leverages:
1. **Control Nodes**: Godot's UI system with CanvasLayer and Control nodes
2. **Scene System**: UI screens as separate scenes for modularity
3. **Signals**: Event-driven UI updates and interactions
4. **Themes**: Consistent styling across UI elements
5. **Autoload**: UIManager as a global singleton for screen management
6. **Containers**: VBoxContainer, HBoxContainer for automatic layout
7. **Custom Drawing**: Control._draw() for custom UI elements like radar

This replaces the C++ custom UI framework with Godot's built-in UI system while preserving the same functionality. The UI is data-driven through scenes and resources, making it easier to modify and extend.