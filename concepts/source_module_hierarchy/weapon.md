# Weapon Module

## Purpose
The Weapon Module handles all projectile and beam-based weapons, including their properties, behavior, firing logic, and effects. It supports multiple weapon types with different characteristics and special behaviors, forming the core of combat gameplay.

## Components
- **Weapon System** (`weapon/`): Core weapon functionality and management
- **Weapon Classes** (`weapon_info`): Templates defining weapon properties
- **Weapon Types**: Lasers, missiles, beams, and countermeasures
- **Homing Systems**: Heat-seeking, aspect-lock, and javelin-style targeting
- **Special Effects**: Trails, particles, EMP, electronics effects
- **Damage Modeling**: Hull/shield damage with armor factors and multipliers
- **Ammunition Management**: Ammo tracking for ballistic weapons
- **Spawn Weapons**: Weapons that create other weapons on detonation
- **Beam Weapons**: Continuous energy weapons with special rendering
- **Countermeasures**: Chaff and other defensive systems

## Dependencies
- **Core Entity Module**: Weapons are specialized entities
- **Ship Module**: Weapons are fired by ships and affect ships
- **Model Module**: Weapon models and firing point positioning
- **Physics Module**: Weapon movement and trajectory
- **AI Module**: AI targeting and weapon selection
- **Particle Module**: Visual effects for weapons

## C++ Components
- `weapon_info`: Structure defining weapon class properties
- `weapon`: Structure representing individual weapon instances
- `weapon_create()`, `weapon_delete()`: Weapon lifecycle management
- `weapon_process_pre()`, `weapon_process_post()`: Frame update functions
- `weapon_hit()`: Weapon impact and damage application
- `weapon_fire_primary()`, `weapon_fire_secondary()`: Firing functions
- `beam_weapon_info`: Specialized data for beam weapons

## Godot Equivalent Mapping

### Native GDScript Classes
```gdscript
# Weapon class representing individual weapon instances
class Weapon extends Entity:
    var weaponClass: WeaponClass
    var owner: Ship
    var ammoCount: int
    var isFiring: bool = false
    var cooldownTimer: float = 0.0
    
    func _process(delta):
        if cooldownTimer > 0:
            cooldownTimer -= delta
            
    func fire(target: Node3D = null) -> bool:
        if can_fire():
            # Create projectile or beam effect
            create_projectile(target)
            ammoCount -= 1
            cooldownTimer = weaponClass.fireRate
            return true
        return false
        
    func can_fire() -> bool:
        return ammoCount > 0 and cooldownTimer <= 0 and isFiring_allowed()
        
    func create_projectile(target: Node3D):
        # Implementation depends on weapon type
        pass

# Weapon class template defining properties for weapon types
class WeaponClass extends Resource:
    var name: String
    var weaponType: String  # LASER, MISSILE, BEAM, etc.
    var damage: float
    var speed: float
    var fireRate: float  # Cooldown time between shots
    var ammoCapacity: int
    var modelPath: String
    var effects: Array[WeaponEffect]
    var homingType: String  # NONE, HEAT, ASPECT
    var specialProperties: Dictionary

# Projectile representing fired weapon projectiles
class Projectile extends Entity:
    var weaponClass: WeaponClass
    var target: Node3D
    var damage: float
    
    func _process(delta):
        move_towards_target(delta)
        check_collision()
        
    func move_towards_target(delta):
        # Movement logic based on weapon type and homing
        pass
        
    func check_collision():
        # Collision detection with other entities
        pass

# Beam weapon implementation
class BeamWeapon extends Weapon:
    var beamEffect: BeamEffect
    
    func fire(target: Node3D = null) -> bool:
        if can_fire():
            activate_beam(target)
            return true
        return false
        
    func activate_beam(target: Node3D):
        # Create beam visualization and apply damage over time
        pass
```

### TRES Resources
```ini
[gd_resource type="Resource" load_steps=3 format=2]

[ext_resource path="res://resources/weapon_effect.tres" type="Resource" id=1]

[resource]
resource_name = "Laser_Cannon"
name = "Mk.II Laser Cannon"
weapon_type = "LASER"
damage = 25.0
speed = 500.0
fire_rate = 0.2
ammo_capacity = -1  # Infinite ammo
model_path = "res://models/laser_cannon.tscn"
effects = [ExtResource(1)]
homing_type = "NONE"
special_properties = {"pierce_shields": true}
```

### TSCN Scenes
```ini
[gd_scene load_steps=4 format=2]

[ext_resource path="res://scripts/weapon.gd" type="Script" id=1]
[ext_resource path="res://resources/weapon_class.tres" type="Resource" id=2]
[ext_resource path="res://models/laser_cannon.tscn" type="PackedScene" id=3]

[node name="LaserCannon" type="Node3D"]
script = ExtResource(1)
weapon_class = ExtResource(2)

[node name="Model" type="Node3D" parent="."]
instance = ExtResource(3)

[node name="Muzzle" type="Node3D" parent="."]
position = Vector3(0, 0, 2)
```

### Implementation Notes
The Weapon Module in Godot leverages:
1. **Inheritance**: Weapons extend the base Entity class
2. **Resources**: Weapon classes as data-driven configurations
3. **Scene Composition**: Complex weapons with multiple components as scenes
4. **Component System**: Effects, homing behavior, and special properties as separate components
5. **Timers**: Built-in timer functionality for cooldown management
6. **PhysicsBody3D**: For collision detection with other entities

This replaces the C++ structure-based approach with Godot's node-based scene system while preserving the same gameplay functionality. Beam weapons are implemented as continuous effects rather than persistent entities.