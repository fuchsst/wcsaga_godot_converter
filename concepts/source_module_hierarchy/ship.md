# Ship Module

## Purpose
The Ship Module manages all aspects of spacecraft entities, including their classes, subsystems, weapons, physics properties, and gameplay characteristics. This is one of the most complex modules in the system, handling ship creation, destruction, damage modeling, and all ship-specific behaviors.

## Components
- **Ship System** (`ship/`): Core ship functionality and management
- **Ship Classes** (`ship_info`): Templates defining ship properties
- **Subsystems** (`ship_subsys`): Damageable components like engines, weapons, sensors
- **Weapon Management**: Primary/secondary weapon banks with ammo tracking
- **Damage Modeling**: Hull and shield damage with subsystem-specific effects
- **Visual Effects**: Thrusters, afterburners, contrails, and special effects
- **Death Handling**: Multiple death stages with explosions and debris
- **Docking Support**: Ship docking and departure mechanics

## Dependencies
- **Core Entity Module**: Ships are specialized entities
- **Physics Module**: Ship movement and physics simulation
- **Model Module**: Ship models and subsystem positioning
- **AI Module**: Each ship has associated AI data
- **Weapon Module**: Ship weapons and firing logic
- **Mission Module**: Mission-specific ship properties and behaviors

## C++ Components
- `ship_info`: Structure defining ship class properties
- `ship`: Structure representing individual ship instances
- `ship_subsys`: Structure for ship subsystems
- `ship_create()`, `ship_delete()`: Ship lifecycle management
- `ship_process_pre()`, `ship_process_post()`: Frame update functions
- `ship_recalc_subsys_strength()`: Subsystem integrity calculations
- `ship_do_rearm_frame()`: Rearm/reload logic

## Godot Equivalent Mapping

### Native GDScript Classes
```gdscript
# Ship class representing individual spacecraft instances
class Ship extends Entity:
    var shipClass: ShipClass
    var subsystems: Array[Subsystem]
    var weapons: WeaponSystem
    var hullStrength: float
    var shieldStrength: float
    var isPlayerControlled: bool = false
    
    func _ready():
        initialize_subsystems()
        
    func _process(delta):
        update_physics(delta)
        update_weapons(delta)
        update_subsystems(delta)
        
    func take_damage(amount: float, location: Vector3, damage_type: String):
        # Handle damage to hull/shields/subsystems
        pass
        
    func initialize_subsystems():
        # Create subsystem instances based on ship class
        pass

# Ship class template defining properties for ship types
class ShipClass extends Resource:
    var name: String
    var modelPath: String
    var maxHullStrength: float
    var maxShieldStrength: float
    var maxVelocity: Vector3
    var subsystemTemplates: Array[SubsystemTemplate]
    var weaponHardpoints: Array[WeaponHardpoint]
    var thrusterPositions: Array[Vector3]

# Subsystem representing damageable ship components
class Subsystem:
    var template: SubsystemTemplate
    var health: float
    var isDestroyed: bool = false
    
    func take_damage(amount: float):
        health -= amount
        if health <= 0:
            isDestroyed = true
            on_destroyed()

# Template for subsystem properties
class SubsystemTemplate extends Resource:
    var name: String
    var maxHealth: float
    var functionType: String  # ENGINE, WEAPON, SENSOR, etc.
```

### TRES Resources
```ini
[gd_resource type="Resource" load_steps=4 format=2]

[ext_resource path="res://resources/subsystem_template.tres" type="Resource" id=1]
[ext_resource path="res://resources/weapon_hardpoint.tres" type="Resource" id=2]

[resource]
resource_name = "Terran_Fighter"
name = "F-22A Raptor"
model_path = "res://models/fighter.tscn"
max_hull_strength = 100.0
max_shield_strength = 50.0
max_velocity = Vector3(200, 200, 200)
subsystem_templates = [ExtResource(1)]
weapon_hardpoints = [ExtResource(2)]
thruster_positions = [Vector3(0, 0, -5), Vector3(0, 0, 5)]
```

### TSCN Scenes
```ini
[gd_scene load_steps=4 format=2]

[ext_resource path="res://scripts/ship.gd" type="Script" id=1]
[ext_resource path="res://resources/ship_class.tres" type="Resource" id=2]
[ext_resource path="res://models/fighter.tscn" type="PackedScene" id=3]

[node name="Fighter" type="Node3D"]
script = ExtResource(1)
ship_class = ExtResource(2)

[node name="Model" type="Node3D" parent="."]
instance = ExtResource(3)

[node name="Thruster1" type="Node3D" parent="."]
position = Vector3(0, 0, -5)

[node name="Thruster2" type="Node3D" parent="."]
position = Vector3(0, 0, 5)
```

### Implementation Notes
The Ship Module in Godot leverages:
1. **Inheritance**: Ships extend the base Entity class
2. **Resources**: Ship classes and subsystem templates as data-driven configurations
3. **Scene Composition**: Complex ships with multiple components as scenes
4. **Component System**: Subsystems, weapons, and effects as separate components
5. **Signals**: Damage and destruction events using Godot's signal system

This replaces the C++ structure-based approach with Godot's node-based scene system while preserving the same gameplay functionality.