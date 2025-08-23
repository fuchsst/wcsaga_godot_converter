# Mission Module

## Purpose
The Mission Module handles all mission-related data, parsing, loading, and execution. It manages mission objectives, events, ships, wings, and the overall mission flow from briefing to debriefing.

## Components
- **Mission System** (`mission/`): Core mission functionality and management
- **Mission Parsing**: Reads .fs2 files and creates game entities
- **Parse Objects**: Intermediate representation of ships/wings before instantiation
- **Mission Events**: Scripted events and triggers based on conditions
- **Wing Management**: Grouped ships with coordinated behavior
- **Mission Goals**: Primary, secondary, and bonus objectives
- **Reinforcements**: Dynamic ship arrival system
- **Support Ships**: Repair/rearm functionality
- **Mission Flow**: State management from briefing to debriefing

## Dependencies
- **Core Entity Module**: Missions create and manage game objects
- **Ship Module**: Missions define ship properties and behaviors
- **Weapon Module**: Missions specify weapon loadouts
- **AI Module**: Missions set AI directives and goals
- **Game Sequence Module**: Missions integrate with game state management

## C++ Components
- `mission`: Structure containing overall mission properties
- `p_object`: Parse object representing ships/wings before creation
- `parse_main()`: Main mission parsing function
- `mission_parse_get_parse_object()`: Gets parse object by name/signature
- `parse_create_object()`: Creates game object from parse object
- `mission_parse_eval_stuff()`: Evaluates mission events and directives
- `get_mission_info()`: Gets basic mission information without loading

## Godot Equivalent Mapping

### Native GDScript Classes
```gdscript
# Mission class representing a single mission
class Mission:
    var name: String
    var description: String
    var author: String
    var version: float
    var gameType: int  # SINGLE, MULTI_COOP, MULTI_TEAMS, etc.
    var flags: int
    var missionScene: PackedScene
    var briefingText: String
    var debriefingText: String
    var objectives: Array[MissionObjective]
    var events: Array[MissionEvent]
    var wings: Array[Wing]
    var reinforcements: Array[Reinforcement]
    var supportShips: SupportShipInfo
    var skybox: String
    var ambientLight: Color
    var musicTrack: String
    
    func _init():
        objectives = []
        events = []
        wings = []
        reinforcements = []
        
    func start_mission():
        # Initialize mission state
        load_mission_scene()
        spawn_initial_entities()
        start_briefing_timer()
        
    func update_mission(delta):
        # Process mission events and objectives
        process_events(delta)
        check_objectives()
        update_wings(delta)
        update_reinforcements(delta)
        
    func load_mission_scene():
        # Load the mission environment scene
        var instance = missionScene.instantiate()
        get_tree().root.add_child(instance)
        
    func spawn_initial_entities():
        # Create initial ships and objects
        for wing in wings:
            wing.spawn_ships()
            
    func process_events(delta):
        # Evaluate mission events and triggers
        for event in events:
            if event.is_triggered():
                event.execute()
                
    func check_objectives():
        # Check if objectives are completed/failed
        for objective in objectives:
            objective.update_status()

# Mission objective representing mission goals
class MissionObjective:
    enum Type { DESTROY, PROTECT, ESCORT, SURVIVE, REACH, DISABLE }
    enum Status { INACTIVE, ACTIVE, COMPLETED, FAILED }
    
    var type: Type
    var status: Status
    var description: String
    var targetEntity: Node3D
    var requiredCount: int
    var currentCount: int
    var isPrimary: bool = true
    var bonusPoints: int = 0
    
    func update_status():
        match type:
            Type.DESTROY:
                if targetEntity == null or not is_instance_valid(targetEntity):
                    currentCount += 1
                    if currentCount >= requiredCount:
                        status = Status.COMPLETED
            Type.PROTECT:
                if targetEntity == null or not is_instance_valid(targetEntity):
                    status = Status.FAILED
            # ... other objective types
    
    func is_complete() -> bool:
        return status == Status.COMPLETED

# Mission event representing scripted triggers
class MissionEvent:
    var condition: Condition
    var actions: Array[Action]
    var isRepeatable: bool = false
    var hasExecuted: bool = false
    var delay: float = 0.0
    var delayTimer: float = 0.0
    
    func is_triggered() -> bool:
        if hasExecuted and not isRepeatable:
            return false
            
        if delayTimer > 0:
            delayTimer -= get_process_delta_time()
            return false
            
        return condition.evaluate()
        
    func execute():
        for action in actions:
            action.perform()
            
        if not isRepeatable:
            hasExecuted = true
        else:
            delayTimer = delay

# Wing representing grouped ships with coordinated behavior
class Wing:
    var name: String
    var ships: Array[ShipTemplate]
    var count: int
    var currentWave: int
    var totalWaves: int
    var formation: String
    var arrivalLocation: String
    var departureLocation: String
    var aiClass: String
    var spawnedShips: Array[Ship]
    
    func spawn_ships():
        # Create ships based on template
        for i in range(count):
            var ship = create_ship_from_template(ships[i % ships.size()])
            spawnedShips.append(ship)
            # Position in formation
            position_in_formation(ship, i)
            
    func create_ship_from_template(template: ShipTemplate) -> Ship:
        # Instantiate ship from template
        var shipScene = load(template.scenePath)
        var shipInstance = shipScene.instantiate() as Ship
        # Apply template properties
        shipInstance.shipClass = template.shipClass
        shipInstance.weaponLoadout = template.weaponLoadout
        return shipInstance
        
    func update_wing(delta):
        # Update wing behavior
        if should_spawn_next_wave():
            spawn_next_wave()

# Reinforcement representing dynamic ship arrivals
class Reinforcement:
    var wing: Wing
    var arrivalDelay: float
    var arrivalTimer: float
    var isAvailable: bool = true
    
    func update(delta):
        if not isAvailable:
            return
            
        arrivalTimer += delta
        if arrivalTimer >= arrivalDelay:
            spawn_reinforcement()
            
    func spawn_reinforcement():
        wing.spawn_ships()
        isAvailable = false

# Support ship information
class SupportShipInfo:
    var shipClass: ShipClass
    var maxHullRepair: float
    var maxSubsystemRepair: float
    var arrivalLocation: String
    var departureLocation: String
```

### TRES Resources
```ini
[gd_resource type="Resource" load_steps=4 format=2]

[ext_resource path="res://resources/mission_objective.tres" type="Resource" id=1]
[ext_resource path="res://resources/mission_event.tres" type="Resource" id=2]
[ext_resource path="res://resources/wing.tres" type="Resource" id=3]

[resource]
resource_name = "Mission_Kilrah_Attack"
name = "Attack on Kilrah"
description = "Lead the assault on the Kilrathi homeworld"
author = "Blair"
version = 1.0
game_type = 0  # SINGLE
flags = 0
mission_scene = "res://missions/kilrah_attack.tscn"
briefing_text = "Today we strike at the heart of the Kilrathi Empire..."
debriefing_text = "Mission successful! The Kilrathi capital is in ruins."
objectives = [ExtResource(1)]
events = [ExtResource(2)]
wings = [ExtResource(3)]
skybox = "res://textures/space_nebula.dds"
ambient_light = Color(0.1, 0.1, 0.2)
music_track = "res://music/combat_theme.ogg"
```

### TSCN Scenes
```ini
[gd_scene load_steps=4 format=2]

[ext_resource path="res://scripts/mission.gd" type="Script" id=1]
[ext_resource path="res://resources/kilrah_attack_mission.tres" type="Resource" id=2]
[ext_resource path="res://missions/kilrah_environment.tscn" type="PackedScene" id=3]

[node name="MissionManager" type="Node"]
script = ExtResource(1)
current_mission = ExtResource(2)

[node name="Environment" type="Node3D" parent="."]
instance = ExtResource(3)

[node name="PlayerStart" type="Node3D" parent="."]
position = Vector3(0, 0, 0)
```

### Implementation Notes
The Mission Module in Godot leverages:
1. **Scene System**: Missions as complete scenes with all entities
2. **Resources**: Mission data as data-driven configurations
3. **Signals**: Event system using Godot's signal mechanism
4. **Node Management**: Dynamic spawning and management of entities
5. **Autoload**: Mission manager as a global singleton
6. **State Management**: Integration with Godot's scene tree for state changes

This replaces the C++ file parsing system with Godot's resource system while preserving the same mission structure and gameplay functionality. The event system is implemented using Godot's built-in signal system for better integration with the engine.