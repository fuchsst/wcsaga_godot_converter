# Physics Module

## Purpose
The Physics Module handles movement, rotation, acceleration, and all physical behaviors of game objects. It implements space flight dynamics with customizable properties for different ship types, including Newtonian physics for space movement.

## Components
- **Physics System** (`physics/`): Core physics simulation and properties
- **Movement Simulation**: Position and velocity integration
- **Rotation Simulation**: Angular velocity and orientation integration
- **Control Input Processing**: Translation from controls to physics forces
- **Thrust Management**: Forward, side, and vertical thrusters
- **Damping Systems**: Velocity reduction over time
- **Acceleration Models**: Time-based acceleration to maximum velocity
- **Impulse Handling**: Force application for collisions and weapons
- **Special Flight Modes**: Afterburner, gliding, and warping

## Dependencies
- **Core Entity Module**: Physics properties are part of object data
- **Math Module**: Vector and matrix mathematics for calculations
- **Ship Module**: Ship-specific physics properties

## C++ Components
- `physics_info`: Structure containing physics properties for objects
- `physics_sim()`: Main physics simulation function
- `physics_read_flying_controls()`: Processes control input
- `physics_init()`: Initializes physics properties
- `physics_apply_whack()`: Applies impulse forces
- `physics_collide_whack()`: Applies collision forces

## Godot Equivalent Mapping

### Native GDScript Classes
```gdscript
# Physics properties component for entities
class PhysicsProperties:
    var mass: float = 1.0
    var drag_coefficient: float = 0.01
    var max_velocity: Vector3 = Vector3(100, 100, 100)
    var max_rotational_velocity: Vector3 = Vector3(1, 1, 1)
    var acceleration_time: float = 2.0  # Time to reach max velocity
    var deceleration_time: float = 3.0  # Time to stop from max velocity
    var rotational_acceleration: float = 5.0
    
    # Special flight modes
    var has_afterburner: bool = false
    var afterburner_multiplier: float = 2.0
    var has_gliding: bool = false

# Physics controller that handles movement and forces
class PhysicsController:
    var entity: Entity
    var properties: PhysicsProperties
    var velocity: Vector3 = Vector3.ZERO
    var angular_velocity: Vector3 = Vector3.ZERO
    var acceleration: Vector3 = Vector3.ZERO
    var is_afterburner_active: bool = false
    var is_gliding: bool = false
    
    func _init(owner_entity: Entity, physics_props: PhysicsProperties):
        entity = owner_entity
        properties = physics_props
        
    func _process(delta):
        # Apply forces and update position
        update_motion(delta)
        update_rotation(delta)
        
    func update_motion(delta):
        # Apply acceleration to velocity
        velocity += acceleration * delta
        
        # Apply drag/damping
        var drag = velocity * properties.drag_coefficient
        velocity -= drag * delta
        
        # Limit to maximum velocity
        var max_speed = get_current_max_speed()
        if velocity.length() > max_speed:
            velocity = velocity.normalized() * max_speed
            
        # Update position
        entity.global_position += velocity * delta
        
    func update_rotation(delta):
        # Apply rotational acceleration
        # Update rotation based on angular velocity
        entity.rotate(Vector3.RIGHT, angular_velocity.x * delta)
        entity.rotate(Vector3.UP, angular_velocity.y * delta)
        entity.rotate(Vector3.FORWARD, angular_velocity.z * delta)
        
    func get_current_max_speed() -> float:
        var base_max = properties.max_velocity.length()
        if is_afterburner_active and properties.has_afterburner:
            return base_max * properties.afterburner_multiplier
        return base_max
        
    func apply_thrust(direction: Vector3, thrust_amount: float):
        # Apply forward thrust in the specified direction
        var thrust_force = direction * thrust_amount
        acceleration = thrust_force / properties.mass
        
    func apply_impulse(impulse: Vector3):
        # Apply instantaneous force (e.g., weapon impacts)
        velocity += impulse / properties.mass
        
    func apply_torque(torque: Vector3):
        # Apply rotational force
        angular_velocity += torque * delta
        
    func activate_afterburner(active: bool):
        if properties.has_afterburner:
            is_afterburner_active = active
            
    func activate_gliding(active: bool):
        if properties.has_gliding:
            is_gliding = active

# Specialized physics for space ships
class ShipPhysicsController extends PhysicsController:
    var ship: Ship
    var forward_thrust: float = 0.0
    var side_thrust: float = 0.0
    var vertical_thrust: float = 0.0
    var pitch_thrust: float = 0.0
    var yaw_thrust: float = 0.0
    var roll_thrust: float = 0.0
    
    func _init(owner_ship: Ship, physics_props: PhysicsProperties):
        super._init(owner_ship, physics_props)
        ship = owner_ship
        
    func update_motion(delta):
        # Apply ship-specific thrust
        var forward = ship.global_transform.basis.z.normalized()
        var right = ship.global_transform.basis.x.normalized()
        var up = ship.global_transform.basis.y.normalized()
        
        # Apply linear thrust
        var thrust_vector = (forward * forward_thrust + 
                           right * side_thrust + 
                           up * vertical_thrust)
        apply_thrust(thrust_vector, 1.0)
        
        super.update_motion(delta)
        
    func update_rotation(delta):
        # Apply rotational thrust
        angular_velocity.x += pitch_thrust * properties.rotational_acceleration * delta
        angular_velocity.y += yaw_thrust * properties.rotational_acceleration * delta
        angular_velocity.z += roll_thrust * properties.rotational_acceleration * delta
        
        # Apply rotational damping
        angular_velocity *= (1.0 - properties.drag_coefficient * delta)
        
        super.update_rotation(delta)
```

### TRES Resources
```ini
[gd_resource type="Resource" load_steps=2 format=2]

[resource]
resource_name = "Fighter_Physics"
mass = 10.0
drag_coefficient = 0.05
max_velocity = Vector3(300, 300, 300)
max_rotational_velocity = Vector3(2, 2, 2)
acceleration_time = 1.5
deceleration_time = 2.0
rotational_acceleration = 8.0
has_afterburner = true
afterburner_multiplier = 2.0
has_gliding = true

[gd_resource type="Resource" load_steps=2 format=2]

[resource]
resource_name = "Capital_Ship_Physics"
mass = 10000.0
drag_coefficient = 0.02
max_velocity = Vector3(100, 100, 100)
max_rotational_velocity = Vector3(0.2, 0.2, 0.2)
acceleration_time = 15.0
deceleration_time = 20.0
rotational_acceleration = 1.0
has_afterburner = false
has_gliding = false
```

### TSCN Scenes
```ini
[gd_scene load_steps=4 format=2]

[ext_resource path="res://scripts/ship.gd" type="Script" id=1]
[ext_resource path="res://scripts/physics_controller.gd" type="Script" id=2]
[ext_resource path="res://resources/fighter_physics.tres" type="Resource" id=3]

[node name="Fighter" type="Node3D"]
script = ExtResource(1)

[node name="PhysicsController" type="Node" parent="."]
script = ExtResource(2)
properties = ExtResource(3)
```

### Implementation Notes
The Physics Module in Godot leverages:
1. **Built-in Physics Engine**: Godot's physics engine for collision detection
2. **RigidBody3D**: For entities that need realistic physics simulation
3. **Custom Motion**: For space-specific movement that doesn't rely on gravity
4. **Resources**: Physics properties as data-driven configurations
5. **Component System**: Physics controllers as separate components attached to entities

This replaces the C++ physics simulation with Godot's node-based approach while preserving the same space flight dynamics. The implementation uses a custom physics controller to handle space-specific behaviors like Newtonian movement, which differs from Godot's default physics that includes gravity.