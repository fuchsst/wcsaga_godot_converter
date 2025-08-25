# Ship Module (Godot Implementation)

## Purpose
The Ship Module manages all aspects of spacecraft entities in the Godot implementation, including ship classes, subsystems, weapons, physics properties, and gameplay characteristics. This module handles ship creation, destruction, damage modeling, and all ship-specific behaviors while leveraging Godot's node-based architecture and following feature-based organization principles.

## Components
- **Ship Class**: Templates defining properties for different ship types
- **Ship Instance**: Individual ship entities with current state
- **Subsystem System**: Damageable components like engines, weapons, sensors
- **Weapon Management**: Primary/secondary weapon banks with ammo tracking
- **Damage Modeling**: Hull and shield damage with subsystem-specific effects
- **Physics Integration**: Mass, moment of inertia, and physics properties
- **Visual Effects**: Thrusters, afterburners, contrails, and special effects
- **Death Handling**: Multiple death stages with explosions and debris
- **Docking Support**: Ship docking and departure mechanics

## Dependencies
- **Core Entity Module** (/scripts/entities/): Ships are specialized entities
- **Physics Module** (/scripts/physics/): Ship movement and physics simulation
- **Weapon Module** (/features/weapons/): Ship weapons and firing logic
- **AI Module** (/scripts/ai/): Each ship has associated AI data
- **Model Module** (/features/fighters/): Ship models and subsystem positioning
- **Visual Effects Module** (/features/effects/): Particle effects and animations

## Directory Structure Implementation
Following the feature-based organization principles, the Ship Module is organized as follows:

### Features Directory (/features/)
Ship entities are implemented as self-contained features in `/features/fighters/`:

- `/features/fighters/confed_rapier/` - Raptor fighter
  - `rapier.tscn` - Main scene file
  - `rapier.gd` - Primary controller script
  - `rapier.tres` - Ship data resource
  - `rapier.glb` - 3D model
  - `rapier.png` - Texture
  - `rapier_engine.ogg` - Engine sound
- `/features/fighters/kilrathi_dralthi/` - Dralthi fighter
  - `dralthi.tscn` - Main scene file
  - `dralthi.gd` - Primary controller script
  - `dralthi.tres` - Ship data resource
  - `dralthi.glb` - 3D model
  - `dralthi.png` - Texture
  - `dralthi_engine.ogg` - Engine sound
- `/features/fighters/_shared/` - Shared fighter assets
  - `/cockpits/` - Shared cockpit models
    - `standard_cockpit.glb`
    - `standard_cockpit_material.tres`
  - `/effects/` - Shared fighter effects
    - `engine_trail.png`
    - `shield_effect.png`

### Scripts Directory (/scripts/)
Core ship logic is implemented as reusable scripts in `/scripts/entities/`:

- `/scripts/entities/base_fighter.gd` - Base fighter controller
- `/scripts/entities/ship_systems/weapon_system.gd` - Weapon system management
- `/scripts/entities/ship_systems/subsystem.gd` - Subsystem component
- `/scripts/entities/ship_systems/subsystem_template.gd` - Subsystem template resource

### Assets Directory (/assets/)
Shared ship-related assets are organized in `/assets/`:

- `/assets/textures/effects/` - Particle textures for ship effects
- `/assets/audio/sfx/` - Sound effects for ship operations

## Godot Implementation Details

### Native GDScript Classes
```gdscript
# Ship class representing individual spacecraft instances
# Location: /features/fighters/confed_rapier/rapier.gd
class Ship extends Entity:
    # Reference to the ship class template
    var shipClass: ShipClass
    
    # Current state values
    var hullStrength: float
    var shieldStrength: float
    var subsystems: Array[Subsystem]
    
    # Weapon systems
    var weaponSystem: WeaponSystem
    
    # Physics controller
    var physicsController: PhysicsController
    
    # AI controller
    var aiController: AIController
    
    # Visual effects components
    var engineEffects: Array[EngineEffect]
    var afterburnerEffects: Array[AfterburnerEffect]
    
    # Player control flags
    var isPlayerControlled: bool = false
    var isSelected: bool = false
    
    # Docking state
    var isDocked: bool = false
    var dockedTo: Ship = null
    
    # Events
    signal ship_damaged(amount, location, damage_type)
    signal ship_destroyed(killer)
    signal subsystem_damaged(subsystem, amount)
    signal subsystem_destroyed(subsystem)
    
    func _ready():
        # Initialize ship from class template
        initialize_from_class()
        super._ready()
        
    func _process(delta):
        if isActive:
            # Update systems
            update_physics(delta)
            update_weapons(delta)
            update_subsystems(delta)
            update_visual_effects(delta)
            
        super._process(delta)
        
    func initialize_from_class():
        # Copy properties from ship class
        hullStrength = shipClass.maxHullStrength
        shieldStrength = shipClass.maxShieldStrength
        
        # Initialize subsystems
        initialize_subsystems()
        
        # Initialize weapon system
        weaponSystem = WeaponSystem.new(self)
        
        # Initialize physics controller
        physicsController = PhysicsController.new(self, shipClass.physicsProperties)
        
        # Initialize AI controller if not player-controlled
        if not isPlayerControlled:
            aiController = AIController.new(self)
            
        # Initialize visual effects
        initialize_visual_effects()
        
    func initialize_subsystems():
        # Create subsystem instances based on ship class
        for subsystem_template in shipClass.subsystemTemplates:
            var subsystem = Subsystem.new(subsystem_template)
            subsystems.append(subsystem)
            
    func initialize_visual_effects():
        # Create engine and afterburner effects
        for thruster_pos in shipClass.thrusterPositions:
            var engine_effect = EngineEffect.new()
            engine_effect.position = thruster_pos
            add_child(engine_effect)
            engineEffects.append(engine_effect)
            
    func update_physics(delta):
        # Update physics if controller exists
        if physicsController != null:
            physicsController.update(delta)
            
    func update_weapons(delta):
        # Update weapon system
        if weaponSystem != null:
            weaponSystem.update(delta)
            
    func update_subsystems(delta):
        # Update all subsystems
        for subsystem in subsystems:
            subsystem.update(delta)
            
    func update_visual_effects(delta):
        # Update engine effects based on thrust
        for effect in engineEffects:
            effect.set_thrust_level(physicsController.forward_thrust)
            
        # Update afterburner effects
        for effect in afterburnerEffects:
            effect.set_active(physicsController.is_afterburner_active)
            
    func take_damage(amount: float, location: Vector3, damage_type: String = "NORMAL"):
        # Apply damage to shields first, then hull
        var damage_remaining = amount
        
        # Shield damage
        if shieldStrength > 0:
            var shield_damage = min(shieldStrength, damage_remaining)
            shieldStrength -= shield_damage
            damage_remaining -= shield_damage
            
        # Hull damage
        if damage_remaining > 0:
            hullStrength -= damage_remaining
            
            # Apply subsystem damage
            apply_subsystem_damage(damage_remaining, location)
            
        # Emit damage signal
        emit_signal("ship_damaged", amount, location, damage_type)
        
        # Check for destruction
        if hullStrength <= 0:
            destroy_ship()
            
    func apply_subsystem_damage(amount: float, location: Vector3):
        # Find closest subsystem to damage location
        var closest_subsystem = null
        var closest_distance = INF
        
        for subsystem in subsystems:
            if not subsystem.isDestroyed:
                var distance = location.distance_to(subsystem.position)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_subsystem = subsystem
                    
        # Apply damage to closest subsystem
        if closest_subsystem != null:
            closest_subsystem.take_damage(amount * 0.5)  # 50% to subsystem
            
    func destroy_ship(killer = null):
        # Handle ship destruction
        emit_signal("ship_destroyed", killer)
        
        # Create explosion effect
        var explosion = ExplosionEffect.new(global_position, 100.0, 1.0)
        
        # Deactivate ship
        deactivate()
        
        # Handle destruction based on ship class
        if shipClass.destructionType == "EXPLODE":
            # Normal explosion
            pass
        elif shipClass.destructionType == "BREAK_APART":
            # Create debris pieces
            create_debris()
            
        # Clean up
        queue_free()
        
    func create_debris():
        # Create debris pieces from ship model
        pass
        
    func dock_with(ship: Ship):
        # Handle docking procedure
        isDocked = true
        dockedTo = ship
        
    func undock():
        # Handle undocking procedure
        isDocked = false
        dockedTo = null

# Ship class template defining properties for ship types
# Location: /scripts/entities/ship_systems/ship_class.gd
class ShipClass extends Resource:
    # Basic identification
    @export var name: String
    @export var description: String
    @export var manufacturer: String
    @export var shipType: String  # FIGHTER, BOMBER, CAPITAL, etc.
    
    # Visual properties
    @export var modelPath: String
    @export var iconPath: String
    @export var thrusterPositions: Array[Vector3]
    
    # Combat properties
    @export var maxHullStrength: float
    @export var maxShieldStrength: float
    @export var shieldRechargeRate: float
    
    # Physics properties
    @export var physicsProperties: PhysicsProperties
    
    # Subsystem definitions
    @export var subsystemTemplates: Array[SubsystemTemplate]
    
    # Weapon hardpoints
    @export var weaponHardpoints: Array[WeaponHardpoint]
    
    # Death handling
    @export var destructionType: String = "EXPLODE"  # EXPLODE, BREAK_APART
    
    # AI properties
    @export var defaultAIProfile: String = "DEFAULT"
    
    func _init():
        resource_name = name

# Subsystem representing damageable ship components
# Location: /scripts/entities/ship_systems/subsystem.gd
class Subsystem:
    # Template this subsystem is based on
    var template: SubsystemTemplate
    
    # Current state
    var health: float
    var isDestroyed: bool = false
    
    # Position in ship space
    var position: Vector3
    
    func _init(subsystem_template: SubsystemTemplate):
        template = subsystem_template
        health = template.maxHealth
        position = template.position
        
    func take_damage(amount: float):
        if not isDestroyed:
            health -= amount
            if health <= 0:
                health = 0
                isDestroyed = true
                on_destroyed()
                
    func on_destroyed():
        # Handle subsystem destruction effects
        match template.functionType:
            "ENGINE":
                # Reduce ship mobility
                pass
            "WEAPON":
                # Disable associated weapons
                pass
            "SENSOR":
                # Reduce detection range
                pass
                
    func update(delta):
        # Update subsystem behavior
        if not isDestroyed:
            # Regenerate health if applicable
            if template.canRegenerate and health < template.maxHealth:
                health = min(health + template.regenRate * delta, template.maxHealth)

# Template for subsystem properties
# Location: /scripts/entities/ship_systems/subsystem_template.gd
class SubsystemTemplate extends Resource:
    @export var name: String
    @export var functionType: String  # ENGINE, WEAPON, SENSOR, etc.
    @export var maxHealth: float
    @export var position: Vector3
    @export var canRegenerate: bool = false
    @export var regenRate: float = 0.0
    @export var armorFactor: float = 1.0

# Weapon system managing ship's weapons
# Location: /scripts/entities/ship_systems/weapon_system.gd
class WeaponSystem:
    var ship: Ship
    var primaryWeapons: Array[Weapon]
    var secondaryWeapons: Array[Weapon]
    
    func _init(owner_ship: Ship):
        ship = owner_ship
        # Initialize weapons from ship class
        initialize_weapons()
        
    func initialize_weapons():
        # Create weapon instances based on ship class hardpoints
        pass
        
    func update(delta):
        # Update all weapons
        for weapon in primaryWeapons:
            weapon.update(delta)
        for weapon in secondaryWeapons:
            weapon.update(delta)
            
    func fire_primary(target = null):
        # Fire all primary weapons
        for weapon in primaryWeapons:
            if weapon.can_fire():
                weapon.fire(target)
                
    func fire_secondary(target = null):
        # Fire all secondary weapons
        for weapon in secondaryWeapons:
            if weapon.can_fire():
                weapon.fire(target)
                
    func get_max_range() -> float:
        # Return maximum weapon range
        var max_range = 0.0
        for weapon in primaryWeapons:
            max_range = max(max_range, weapon.weaponClass.maxRange)
        for weapon in secondaryWeapons:
            max_range = max(max_range, weapon.weaponClass.maxRange)
        return max_range

# Visual effect for ship engines
# Location: /features/effects/thruster/thruster.gd
class EngineEffect extends Node3D:
    var thrust_level: float = 0.0
    var particle_system: GPUParticles3D
    
    func _ready():
        # Initialize particle system
        particle_system = GPUParticles3D.new()
        add_child(particle_system)
        
    func set_thrust_level(level: float):
        thrust_level = clamp(level, 0.0, 1.0)
        # Adjust particle emission rate based on thrust
        particle_system.amount_ratio = thrust_level
        
    func set_active(is_active: bool):
        particle_system.emitting = is_active

# Afterburner effect
# Location: /features/effects/afterburner/afterburner.gd
class AfterburnerEffect extends Node3D:
    var particle_system: GPUParticles3D
    
    func set_active(is_active: bool):
        if particle_system != null:
            particle_system.emitting = is_active
```

### TRES Resources
```ini
# Location: /features/fighters/confed_rapier/rapier.tres
[gd_resource type="Resource" load_steps=4 format=2]

[ext_resource path="res://scripts/physics/fighter_physics.tres" type="Resource" id=1]
[ext_resource path="res://scripts/entities/ship_systems/templates/subsystem_template.tres" type="Resource" id=2]
[ext_resource path="res://features/weapons/templates/weapon_hardpoint.tres" type="Resource" id=3]

[resource]
resource_name = "F-27B_Arrow"
name = "F-27B Arrow"
description = "Light Fighter"
manufacturer = "Douglas Aerospace"
ship_type = "FIGHTER"
model_path = "res://features/fighters/confed_rapier/rapier.glb"
icon_path = "res://features/fighters/confed_rapier/rapier_icon.png"
thruster_positions = [Vector3(0, 0, -10), Vector3(2, 0, -5), Vector3(-2, 0, -5)]
max_hull_strength = 280.0
max_shield_strength = 800.0
shield_recharge_rate = 0.04
physics_properties = ExtResource(1)
subsystem_templates = [ExtResource(2)]
weapon_hardpoints = [ExtResource(3)]
destruction_type = "EXPLODE"
default_ai_profile = "CAPTAIN"
```

### TSCN Scenes
```ini
# Location: /features/fighters/confed_rapier/rapier.tscn
[gd_scene load_steps=4 format=2]

[ext_resource path="res://features/fighters/confed_rapier/rapier.gd" type="Script" id=1]
[ext_resource path="res://features/fighters/confed_rapier/rapier.tres" type="Resource" id=2]
[ext_resource path="res://features/fighters/confed_rapier/rapier.glb" type="PackedScene" id=3]

[node name="Arrow" type="Node3D"]
script = ExtResource(1)
ship_class = ExtResource(2)

[node name="Model" type="Node3D" parent="."]
instance = ExtResource(3)

[node name="Thruster1" type="Node3D" parent="."]
position = Vector3(0, 0, -10)

[node name="Thruster2" type="Node3D" parent="."]
position = Vector3(2, 0, -5)

[node name="Thruster3" type="Node3D" parent="."]
position = Vector3(-2, 0, -5)
```

### Implementation Notes
The Ship Module in Godot leverages feature-based organization principles:

1. **Inheritance**: Ships extend the base Entity class located in `/scripts/entities/`
2. **Composition**: Complex systems (weapons, physics, AI) as separate components organized in `/scripts/entities/ship_systems/`
3. **Resources**: Ship classes and subsystem templates as data-driven configurations organized in feature directories
4. **Scene System**: Ships as self-contained scenes organized by feature in `/features/fighters/{name}/`
5. **Signals**: Event-driven communication between systems
6. **Node Hierarchy**: Visual effects as child nodes for proper positioning
7. **Pooling**: Efficient ship creation/destruction through EntityManager

This replaces the C++ structure-based approach with Godot's node-based scene system while preserving the same gameplay functionality. The implementation uses Godot's built-in particle systems for engine effects and the resource system for ship class definitions, organized according to Godot's feature-based best practices where each ship type has its own self-contained directory with all related assets.

Following the feature-based organization principles:
- Ship entities are implemented as self-contained features in `/features/fighters/`
- Core ship logic is implemented as reusable scripts in `/scripts/entities/`
- Shared assets are organized in `/assets/`
- Visual effects are implemented as features in `/features/effects/`
- Ship systems are organized in `/scripts/entities/ship_systems/`