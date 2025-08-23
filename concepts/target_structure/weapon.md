# Weapon Module (Godot Implementation)

## Purpose
The Weapon Module handles all projectile and beam-based weapons in the Godot implementation, including their properties, behavior, firing logic, and effects. It supports multiple weapon types with different characteristics and special behaviors, forming the core of combat gameplay while leveraging Godot's node-based architecture and following feature-based organization principles.

## Components
- **Weapon Class**: Templates defining weapon properties and behavior
- **Weapon Instance**: Individual weapon entities with current state
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
- **Visual Effects Module**: Particle effects and animations
- **Audio Module**: Weapon firing sounds and effects

## Godot Implementation Details

### Native GDScript Classes
```gdscript
# Weapon class representing individual weapon instances
class Weapon extends Entity:
    # Reference to the weapon class template
    var weaponClass: WeaponClass
    
    # Owner ship that fired this weapon
    var owner: Ship
    
    # Current ammunition count
    var ammoCount: int
    
    # Firing state
    var isFiring: bool = false
    var cooldownTimer: float = 0.0
    
    # Target tracking for homing weapons
    var target: Node3D = null
    var lockTime: float = 0.0
    
    # Visual effects
    var muzzleFlash: MuzzleFlashEffect
    var trailEffect: TrailEffect
    
    # Events
    signal weapon_fired(weapon, target)
    signal weapon_cooldown(weapon)
    signal weapon_out_of_ammo(weapon)
    
    func _ready():
        # Initialize from weapon class
        initialize_from_class()
        super._ready()
        
    func _process(delta):
        # Update cooldown timer
        if cooldownTimer > 0:
            cooldownTimer -= delta
            if cooldownTimer <= 0:
                emit_signal("weapon_cooldown", self)
                
        # Update homing lock for guided weapons
        if target != null and weaponClass.homingType != "NONE":
            update_homing_lock(delta)
            
        super._process(delta)
        
    func initialize_from_class():
        # Set initial ammo count
        ammoCount = weaponClass.ammoCapacity
        
        # Create visual effects
        initialize_visual_effects()
        
    func initialize_visual_effects():
        # Create muzzle flash effect
        muzzleFlash = MuzzleFlashEffect.new()
        add_child(muzzleFlash)
        
        # Create trail effect for projectiles
        if weaponClass.weaponType == "MISSILE" or weaponClass.weaponType == "PROJECTILE":
            trailEffect = TrailEffect.new()
            add_child(trailEffect)
            
    func fire(target_entity: Node3D = null) -> bool:
        # Check if weapon can fire
        if not can_fire():
            return false
            
        # Consume ammo if applicable
        if weaponClass.ammoCapacity > 0:
            ammoCount -= 1
            
        # Set cooldown
        cooldownTimer = weaponClass.fireRate
        
        # Create projectile or beam effect
        if weaponClass.weaponType == "BEAM":
            create_beam_effect(target_entity)
        else:
            create_projectile(target_entity)
            
        # Trigger muzzle flash
        if muzzleFlash != null:
            muzzleFlash.trigger()
            
        # Emit fired signal
        emit_signal("weapon_fired", self, target_entity)
        
        # Check for out of ammo
        if ammoCount <= 0:
            emit_signal("weapon_out_of_ammo", self)
            
        return true
        
    func can_fire() -> bool:
        # Check if weapon is ready to fire
        return isActive and cooldownTimer <= 0 and ammoCount != 0 and isFiring_allowed()
        
    func isFiring_allowed() -> bool:
        # Check if firing is allowed (e.g., not in safe zones, etc.)
        return true  # Override in subclasses for specific rules
        
    func create_projectile(target_entity: Node3D):
        # Create projectile instance based on weapon class
        var projectile = Projectile.new()
        projectile.weaponClass = weaponClass
        projectile.owner = owner
        projectile.target = target_entity
        projectile.damage = weaponClass.damage
        projectile.speed = weaponClass.speed
        projectile.homingType = weaponClass.homingType
        
        # Set initial position to weapon's global position
        projectile.global_position = global_position
        
        # Set initial velocity in forward direction
        var forward = global_transform.basis.z.normalized()
        projectile.velocity = forward * weaponClass.speed
        
        # Add to scene
        get_tree().root.add_child(projectile)
        
        # Apply parent velocity for relative movement
        if owner != null and owner.physicsController != null:
            projectile.velocity += owner.physicsController.velocity
            
    func create_beam_effect(target_entity: Node3D):
        # Create beam visualization and apply damage over time
        var beam = BeamEffect.new()
        beam.start_position = global_position
        beam.end_position = target_entity.global_position if target_entity != null else global_position + global_transform.basis.z * 1000
        beam.duration = weaponClass.beamDuration
        beam.damage_per_second = weaponClass.damage
        add_child(beam)
        
    func update_homing_lock(delta):
        # Update homing lock progress
        if weaponClass.homingType == "LOCK":
            lockTime += delta
            # Check if lock is achieved
            if lockTime >= weaponClass.lockTime:
                # Lock achieved, weapon can now be fired
                pass
                
    func get_max_range() -> float:
        # Return weapon's maximum effective range
        return weaponClass.maxRange

# Weapon class template defining properties for weapon types
class WeaponClass extends Resource:
    # Basic identification
    @export var name: String
    @export var description: String
    @export var weaponType: String  # LASER, MISSILE, BEAM, PROJECTILE, COUNTERMEASURE
    
    # Visual properties
    @export var modelPath: String
    @export var iconPath: String
    @export var muzzleFlashEffect: MuzzleFlashEffect
    @export var trailEffect: TrailEffect
    
    # Combat properties
    @export var damage: float
    @export var speed: float
    @export var fireRate: float  # Time between shots in seconds
    @export var ammoCapacity: int = -1  # -1 for infinite ammo
    @export var maxRange: float = 1000.0
    
    # Homing properties
    @export var homingType: String = "NONE"  # NONE, HEAT, ASPECT, LOCK
    @export var lockTime: float = 0.0  # Time to achieve lock
    @export var turnRate: float = 0.0  # For guided weapons
    
    # Beam weapon properties
    @export var beamDuration: float = 1.0
    @export var beamWidth: float = 1.0
    
    # Special effects
    @export var empEffect: bool = false
    @export var electronicsEffect: bool = false
    @export var spawnWeapons: Array[SpawnWeaponInfo]
    
    # Physics properties
    @export var mass: float = 1.0
    @export var dragCoefficient: float = 0.01
    
    # Audio properties
    @export var fireSound: String = ""
    @export var impactSound: String = ""
    
    func _init():
        resource_name = name

# Projectile representing fired weapon projectiles
class Projectile extends Entity:
    # Weapon class that created this projectile
    var weaponClass: WeaponClass
    
    # Owner and target references
    var owner: Ship
    var target: Node3D
    
    # Physical properties
    var velocity: Vector3 = Vector3.ZERO
    var damage: float
    
    # Homing properties
    var homingType: String = "NONE"
    var lockProgress: float = 0.0
    
    # Lifetime management
    var lifetime: float = 10.0
    var currentLifetime: float = 0.0
    
    func _process(delta):
        # Update lifetime
        currentLifetime += delta
        if currentLifetime >= lifetime:
            expire()
            return
            
        # Update movement
        update_movement(delta)
        
        # Update homing if applicable
        if target != null and homingType != "NONE":
            update_homing(delta)
            
        # Update trail effect
        if trailEffect != null:
            trailEffect.update_position(global_position)
            
        super._process(delta)
        
    func update_movement(delta):
        # Simple linear movement
        global_position += velocity * delta
        
    func update_homing(delta):
        # Heat-seeking homing
        if homingType == "HEAT":
            if target != null:
                # Calculate direction to target
                var direction_to_target = (target.global_position - global_position).normalized()
                var current_direction = velocity.normalized()
                
                # Calculate turn toward target
                var turn_speed = weaponClass.turnRate * delta
                var new_direction = current_direction.slerp(direction_to_target, turn_speed)
                
                # Apply new velocity
                velocity = new_direction * weaponClass.speed
                
        # Aspect-lock homing
        elif homingType == "ASPECT":
            # More sophisticated homing that predicts target position
            pass
            
    func check_collision():
        # Check for collision with other entities
        # This would typically use physics queries or area monitoring
        pass
        
    func on_impact(hit_entity: Node3D = null):
        # Handle weapon impact
        if hit_entity != null:
            # Apply damage
            if hit_entity is Ship:
                hit_entity.take_damage(damage, global_position, "WEAPON")
                
        # Create impact effects
        create_impact_effects()
        
        # Handle spawn weapons
        for spawn_info in weaponClass.spawnWeapons:
            spawn_spawn_weapon(spawn_info)
            
        # Destroy projectile
        destroy()
        
    func create_impact_effects():
        # Create explosion or impact effects
        var explosion = ExplosionEffect.new(global_position, 50.0, 0.5)
        
    func spawn_spawn_weapon(spawn_info: SpawnWeaponInfo):
        # Create spawned weapon at impact location
        var spawn_weapon = Weapon.new()
        spawn_weapon.weaponClass = spawn_info.weaponClass
        spawn_weapon.global_position = global_position
        spawn_weapon.fire()
        
    func expire():
        # Handle projectile expiration (timeout)
        destroy()
        
    func destroy():
        # Clean up effects and destroy
        if trailEffect != null:
            trailEffect.queue_free()
        super.destroy()

# Beam weapon implementation
class BeamEffect extends Node3D:
    # Beam properties
    var start_position: Vector3
    var end_position: Vector3
    var duration: float
    var current_duration: float = 0.0
    var damage_per_second: float
    
    # Visual representation
    var beam_mesh: MeshInstance3D
    var beam_material: ShaderMaterial
    
    func _ready():
        # Create beam visualization
        create_beam_visualization()
        
    func _process(delta):
        # Update duration
        current_duration += delta
        if current_duration >= duration:
            queue_free()
            return
            
        # Update beam visualization
        update_beam_visualization()
        
    func create_beam_visualization():
        # Create mesh for beam visualization
        beam_mesh = MeshInstance3D.new()
        
        # Create cylinder mesh for beam
        var cylinder_mesh = CylinderMesh.new()
        cylinder_mesh.top_radius = 0.5
        cylinder_mesh.bottom_radius = 0.5
        cylinder_mesh.height = 1.0
        beam_mesh.mesh = cylinder_mesh
        
        # Create material
        beam_material = ShaderMaterial.new()
        beam_material.shader = preload("res://shaders/beam_shader.gdshader")
        beam_mesh.material_override = beam_material
        
        add_child(beam_mesh)
        
    func update_beam_visualization():
        # Update beam position and orientation
        var direction = end_position - start_position
        var length = direction.length()
        var center = (start_position + end_position) / 2.0
        
        # Position beam
        global_position = center
        
        # Scale beam to length
        beam_mesh.scale = Vector3(1.0, length, 1.0)
        
        # Rotate beam to face direction
        var basis = Basis()
        basis = basis.looking_at(direction.normalized())
        global_transform.basis = basis
        
    func set_damage_target(target: Node3D, delta):
        # Apply damage to target over time
        if target != null and target is Ship:
            target.take_damage(damage_per_second * delta, global_position, "BEAM")

# Muzzle flash effect
class MuzzleFlashEffect extends Node3D:
    var particles: GPUParticles3D
    var light: OmniLight3D
    
    func _ready():
        # Create particle system
        particles = GPUParticles3D.new()
        particles.emitting = false
        particles.one_shot = true
        add_child(particles)
        
        # Create light
        light = OmniLight3D.new()
        light.light_energy = 0.0
        add_child(light)
        
    func trigger():
        # Trigger muzzle flash effect
        particles.restart()
        particles.emitting = true
        
        # Flash light
        light.light_energy = 10.0
        var tween = create_tween()
        tween.tween_property(light, "light_energy", 0.0, 0.1)
        
    func set_color(color: Color):
        # Set flash color
        if particles.process_material is StandardMaterial3D:
            particles.process_material.albedo_color = color

# Trail effect for projectiles
class TrailEffect extends Node3D:
    var trail_points: Array[Vector3] = []
    var max_points: int = 20
    var trail_mesh: ImmediateMesh
    var trail_instance: MeshInstance3D
    
    func _ready():
        # Create trail mesh
        trail_mesh = ImmediateMesh.new()
        trail_instance = MeshInstance3D.new()
        trail_instance.mesh = trail_mesh
        add_child(trail_instance)
        
    func update_position(position: Vector3):
        # Add new trail point
        trail_points.append(position)
        
        # Remove oldest point if exceeding max
        if trail_points.size() > max_points:
            trail_points.pop_front()
            
        # Update trail visualization
        update_trail_visualization()
        
    func update_trail_visualization():
        # Clear mesh
        trail_mesh.clear_surfaces()
        
        # Create trail geometry
        if trail_points.size() >= 2:
            var surface = SurfaceTool.new()
            surface.begin(Mesh.PRIMITIVE_LINE_STRIP)
            
            for i in range(trail_points.size()):
                var point = trail_points[i]
                var width = lerp(0.1, 1.0, float(i) / float(trail_points.size()))
                surface.set_color(Color(1.0, 1.0, 1.0, width))
                surface.add_vertex(point)
                
            surface.commit(trail_mesh)

# Information for spawn weapons
class SpawnWeaponInfo extends Resource:
    @export var weaponClass: WeaponClass
    @export var count: int = 1
    @export var spreadAngle: float = 30.0

# Weapon system managing multiple weapons on a ship
class WeaponSystem:
    var ship: Ship
    var primary_weapons: Array[Weapon]
    var secondary_weapons: Array[Weapon]
    var selected_primary: int = 0
    var selected_secondary: int = 0
    
    func _init(owner_ship: Ship):
        ship = owner_ship
        initialize_weapons()
        
    func initialize_weapons():
        # Create weapon instances based on ship class hardpoints
        # This would typically be populated from the ship class definition
        pass
        
    func update(delta):
        # Update all weapons
        for weapon in primary_weapons:
            weapon.update(delta)
        for weapon in secondary_weapons:
            weapon.update(delta)
            
    func fire_primary(target = null) -> bool:
        # Fire selected primary weapon
        if selected_primary < primary_weapons.size():
            var weapon = primary_weapons[selected_primary]
            return weapon.fire(target)
        return false
        
    func fire_secondary(target = null) -> bool:
        # Fire selected secondary weapon
        if selected_secondary < secondary_weapons.size():
            var weapon = secondary_weapons[selected_secondary]
            return weapon.fire(target)
        return false
        
    func cycle_primary():
        # Cycle to next primary weapon
        if primary_weapons.size() > 0:
            selected_primary = (selected_primary + 1) % primary_weapons.size()
            
    func cycle_secondary():
        # Cycle to next secondary weapon
        if secondary_weapons.size() > 0:
            selected_secondary = (selected_secondary + 1) % secondary_weapons.size()
            
    func get_max_range() -> float:
        # Return maximum range of any equipped weapon
        var max_range = 0.0
        for weapon in primary_weapons:
            max_range = max(max_range, weapon.get_max_range())
        for weapon in secondary_weapons:
            max_range = max(max_range, weapon.get_max_range())
        return max_range
```

### TRES Resources
```ini
[gd_resource type="Resource" load_steps=3 format=2]

[ext_resource path="res://data/effects/muzzle_flash_effect.tres" type="Resource" id=1]
[ext_resource path="res://data/effects/trail_effect.tres" type="Resource" id=2]

[resource]
resource_name = "MkII_Laser_Cannon"
name = "Mk.II Laser Cannon"
description = "Standard laser cannon"
weapon_type = "LASER"
model_path = "res://entities/weapons/laser_cannon/laser_cannon.glb"
icon_path = "res://entities/weapons/laser_cannon/laser_cannon_icon.png"
damage = 25.0
speed = 500.0
fire_rate = 0.25  # Four shots per second
ammo_capacity = -1  # Infinite ammo
max_range = 1000.0
homing_type = "NONE"
muzzle_flash_effect = ExtResource(1)
trail_effect = ExtResource(2)
fire_sound = "laser_fire_01"
impact_sound = "laser_impact_01"
```

### TSCN Scenes
```ini
[gd_scene load_steps=4 format=2]

[ext_resource path="res://entities/weapons/laser_cannon/laser_cannon.gd" type="Script" id=1]
[ext_resource path="res://data/weapons/terran/lasers/laser_cannon.tres" type="Resource" id=2]
[ext_resource path="res://entities/weapons/laser_cannon/laser_cannon.glb" type="PackedScene" id=3]

[node name="LaserCannon" type="Node3D"]
script = ExtResource(1)
weapon_class = ExtResource(2)

[node name="Model" type="Node3D" parent="."]
instance = ExtResource(3)

[node name="MuzzlePoint" type="Node3D" parent="."]
position = Vector3(0, 0, 2)
```

### Implementation Notes
The Weapon Module in Godot leverages feature-based organization principles:

1. **Inheritance**: Weapons extend the base Entity class
2. **Resources**: Weapon classes as data-driven configurations organized in `/data/weapons/{faction}/{type}/`
3. **Scene Composition**: Complex weapons with multiple components as self-contained scenes organized by feature in `/entities/weapons/{name}/`
4. **Component System**: Effects, homing behavior, and special properties as separate components
5. **Timers**: Built-in timer functionality for cooldown management
6. **PhysicsBody3D**: For collision detection with other entities
7. **Particles**: GPUParticles3D for visual effects like muzzle flashes and trails
8. **Tweening**: For smooth light and effect animations
9. **ImmediateMesh**: For dynamic trail effects
10. **Signals**: For event-driven weapon behavior

This replaces the C++ structure-based approach with Godot's node-based scene system while preserving the same gameplay functionality. Beam weapons are implemented as continuous effects rather than persistent entities, and the particle system uses Godot's optimized GPU-based particles rather than CPU-based particle management.

The implementation uses Godot's resource system for weapon definitions, making it easy to balance and modify weapons without changing code. Visual effects are implemented using Godot's built-in particle systems and shaders for high performance. All assets are organized according to Godot's feature-based best practices where each weapon type has its own self-contained directory with all related assets.