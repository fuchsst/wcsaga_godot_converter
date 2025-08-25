# Physics Module (Godot Implementation)

## Purpose
The Physics Module handles movement, rotation, acceleration, and all physical behaviors of game objects in the Godot implementation. It implements space flight dynamics with customizable properties for different ship types, including Newtonian physics for space movement, while leveraging Godot's node-based architecture.

## Components
- **Physics Controller**: Main physics simulation and properties for entities
- **Physics Properties**: Data-driven configuration for different entity types
- **Movement Simulation**: Position and velocity integration using Newtonian physics
- **Rotation Simulation**: Angular velocity and orientation integration
- **Control Input Processing**: Translation from controls to physics forces
- **Thrust Management**: Forward, side, and vertical thrusters with afterburner
- **Damping Systems**: Velocity reduction over time for realistic space movement
- **Acceleration Models**: Time-based acceleration to maximum velocity
- **Impulse Handling**: Force application for collisions and weapons
- **Special Flight Modes**: Afterburner, gliding, and warping behaviors
- **Collision Response**: Physics reactions to collisions with other objects

## Dependencies
- **Core Entity Module** (/scripts/entities/): Physics properties are part of entity data
- **Math Module** (/scripts/utilities/): Vector and matrix mathematics for calculations (using Godot's built-in math)
- **Ship Module** (/features/fighters/): Ship-specific physics properties and behaviors

## Directory Structure Implementation
Following the feature-based organization principles, the Physics Module is organized as follows:

### Scripts Directory (/scripts/physics/)
The core physics logic is implemented as reusable scripts in `/scripts/physics/`:

- `/scripts/physics/physics_controller.gd` - Main physics controller class
- `/scripts/physics/physics_properties.gd` - Physics properties resource class
- `/scripts/physics/collision_handler.gd` - Collision response handling
- `/scripts/physics/space_environment.gd` - Global space effects controller
- `/scripts/physics/gravity_well.gd` - Gravity well area effect
- `/scripts/physics/nebula_field.gd` - Nebula field area effect
- `/scripts/physics/physics_manager.gd` - Global physics manager singleton
- `/scripts/physics/physics_debugger.gd` - Debug visualization tools

### Features Directory (/features/)
Physics-related visual effects and feature-specific implementations are organized in `/features/`:

- `/features/effects/thruster/` - Thruster visual effects
  - `thruster.tscn` - Thruster effect scene
  - `thruster.gd` - Thruster effect script
  - `thruster.tres` - Thruster effect properties
- `/features/environment/gravity_well/` - Gravity well environmental effect
  - `gravity_well.tscn` - Gravity well scene
  - `gravity_well.gd` - Gravity well script
  - `gravity_well.tres` - Gravity well properties
- `/features/environment/nebula/` - Nebula environmental effect
  - `nebula.tscn` - Nebula field scene
  - `nebula.gd` - Nebula field script
  - `nebula.tres` - Nebula field properties

### Autoload Directory (/autoload/)
Global physics systems are implemented as singletons in `/autoload/`:

- `/autoload/physics_manager.gd` - Global physics manager
- `/autoload/space_environment.gd` - Global space environment controller

### Assets Directory (/assets/)
Shared physics-related assets are organized in `/assets/`:

- `/assets/textures/effects/` - Particle textures for thruster effects
- `/assets/audio/sfx/` - Sound effects for thruster operations

## Godot Implementation Details

### Native GDScript Classes
```gdscript
# Physics controller that handles movement and forces for entities
# Location: /scripts/physics/physics_controller.gd
class PhysicsController extends Node:
    # Reference to the entity this controller manages
    var entity: Entity
    
    # Physics properties defining behavior
    var properties: PhysicsProperties
    
    # Current physical state
    var velocity: Vector3 = Vector3.ZERO
    var angular_velocity: Vector3 = Vector3.ZERO
    var acceleration: Vector3 = Vector3.ZERO
    var angular_acceleration: Vector3 = Vector3.ZERO
    
    # Control inputs
    var forward_thrust: float = 0.0
    var side_thrust: float = 0.0
    var vertical_thrust: float = 0.0
    var pitch_thrust: float = 0.0
    var yaw_thrust: float = 0.0
    var roll_thrust: float = 0.0
    
    # Special flight modes
    var is_afterburner_active: bool = false
    var is_gliding: bool = false
    var is_warping: bool = false
    
    # Physics state
    var mass: float = 1.0
    var moment_of_inertia: Vector3 = Vector3.ONE
    
    # Thrust effects
    var thruster_effects: Array[ThrusterEffect] = []
    
    func _init(owner_entity: Entity, physics_props: PhysicsProperties):
        entity = owner_entity
        properties = physics_props
        initialize_from_properties()
        
    func _ready():
        # Create thruster effects
        create_thruster_effects()
        
    func _process(delta):
        # Update physics simulation
        if entity.isActive and not is_warping:
            update_motion(delta)
            update_rotation(delta)
            update_thruster_effects(delta)
            
    func initialize_from_properties():
        # Initialize from physics properties
        mass = properties.mass
        moment_of_inertia = properties.momentOfInertia
        
        # Set initial velocities to zero
        velocity = Vector3.ZERO
        angular_velocity = Vector3.ZERO
        acceleration = Vector3.ZERO
        angular_acceleration = Vector3.ZERO
        
    func create_thruster_effects():
        # Create visual thruster effects based on properties
        for thruster_pos in properties.thrusterPositions:
            var thruster_effect = ThrusterEffect.new()
            thruster_effect.position = thruster_pos
            add_child(thruster_effect)
            thruster_effects.append(thruster_effect)
            
    func update_motion(delta):
        # Calculate linear acceleration based on thrust
        var forward = entity.global_transform.basis.z.normalized()
        var right = entity.global_transform.basis.x.normalized()
        var up = entity.global_transform.basis.y.normalized()
        
        # Apply thrust forces
        var thrust_vector = (forward * forward_thrust + 
                           right * side_thrust + 
                           up * vertical_thrust)
                           
        # Calculate acceleration (F = ma => a = F/m)
        acceleration = thrust_vector / mass
        
        # Apply acceleration to velocity
        velocity += acceleration * delta
        
        # Apply drag/damping
        var drag_force = velocity * properties.dragCoefficient
        var drag_acceleration = drag_force / mass
        velocity -= drag_acceleration * delta
        
        # Limit to maximum velocity
        var max_speed = get_current_max_speed()
        if velocity.length() > max_speed:
            velocity = velocity.normalized() * max_speed
            
        # Update position using velocity
        entity.global_position += velocity * delta
        
    func update_rotation(delta):
        # Calculate angular acceleration based on rotational thrust
        var torque = Vector3(pitch_thrust, yaw_thrust, roll_thrust)
        angular_acceleration = torque / moment_of_inertia
        
        # Apply angular acceleration to angular velocity
        angular_velocity += angular_acceleration * delta
        
        # Apply rotational damping
        var rotational_drag = angular_velocity * properties.rotationalDragCoefficient
        angular_velocity -= rotational_drag * delta
        
        # Limit to maximum rotational velocity
        var max_rotational_speed = properties.maxRotationalVelocity
        angular_velocity.x = clamp(angular_velocity.x, -max_rotational_speed.x, max_rotational_speed.x)
        angular_velocity.y = clamp(angular_velocity.y, -max_rotational_speed.y, max_rotational_speed.y)
        angular_velocity.z = clamp(angular_velocity.z, -max_rotational_speed.z, max_rotational_speed.z)
        
        # Update rotation using angular velocity
        entity.rotate(Vector3.RIGHT, angular_velocity.x * delta)
        entity.rotate(Vector3.UP, angular_velocity.y * delta)
        entity.rotate(Vector3.FORWARD, angular_velocity.z * delta)
        
    func update_thruster_effects(delta):
        # Update thruster visual effects based on current thrust
        for effect in thruster_effects:
            effect.set_thrust_level(get_combined_thrust_level())
            
    func get_combined_thrust_level() -> float:
        # Return combined thrust level for visual effects
        return abs(forward_thrust) + abs(side_thrust) + abs(vertical_thrust) + 
               abs(pitch_thrust) + abs(yaw_thrust) + abs(roll_thrust)
               
    func get_current_max_speed() -> float:
        # Return current maximum speed considering special modes
        var base_max = properties.maxVelocity.length()
        
        if is_afterburner_active and properties.hasAfterburner:
            return base_max * properties.afterburnerMultiplier
        elif is_gliding and properties.hasGliding:
            return base_max * properties.glidingMultiplier
            
        return base_max
        
    func apply_impulse(impulse: Vector3):
        # Apply instantaneous force (e.g., weapon impacts, explosions)
        velocity += impulse / mass
        
    func apply_torque(torque: Vector3):
        # Apply rotational force
        angular_velocity += torque / moment_of_inertia
        
    func apply_whack(force: Vector3, position: Vector3):
        # Apply force at a specific position (e.g., collision)
        # This creates both linear motion and rotation
        apply_impulse(force)
        
        # Calculate torque from force applied at offset position
        var offset = position - entity.global_position
        var torque = offset.cross(force)
        apply_torque(torque)
        
    func activate_afterburner(active: bool):
        # Activate/deactivate afterburner
        if properties.hasAfterburner:
            is_afterburner_active = active
            
    func activate_gliding(active: bool):
        # Activate/deactivate gliding
        if properties.hasGliding:
            is_gliding = active
            
    func initiate_warp(active: bool):
        # Initiate warp in/out sequence
        is_warping = active
        
    func set_control_input(forward: float, side: float, vertical: float,
                          pitch: float, yaw: float, roll: float):
        # Set control input values
        forward_thrust = clamp(forward, -1.0, 1.0)
        side_thrust = clamp(side, -1.0, 1.0)
        vertical_thrust = clamp(vertical, -1.0, 1.0)
        pitch_thrust = clamp(pitch, -1.0, 1.0)
        yaw_thrust = clamp(yaw, -1.0, 1.0)
        roll_thrust = clamp(roll, -1.0, 1.0)
        
    func get_velocity_magnitude() -> float:
        # Return current speed magnitude
        return velocity.length()
        
    func get_relative_velocity(other_entity: Entity) -> Vector3:
        # Return velocity relative to another entity
        if other_entity != null and other_entity.physicsController != null:
            return velocity - other_entity.physicsController.velocity
        return velocity

# Physics properties defining behavior for different entity types
# Location: /scripts/physics/physics_properties.gd
class PhysicsProperties extends Resource:
    # Basic physical properties
    @export var mass: float = 10.0  # Mass in arbitrary units
    @export var momentOfInertia: Vector3 = Vector3(1.0, 1.0, 1.0)  # Moment of inertia for rotation
    
    # Movement properties
    @export var maxVelocity: Vector3 = Vector3(300, 300, 300)  # Maximum velocity in each axis
    @export var maxRotationalVelocity: Vector3 = Vector3(2.0, 2.0, 2.0)  # Maximum rotational velocity
    @export var accelerationTime: float = 2.0  # Time to reach max velocity
    @export var decelerationTime: float = 3.0  # Time to stop from max velocity
    
    # Drag and damping
    @export var dragCoefficient: float = 0.01  # Linear drag coefficient
    @export var rotationalDragCoefficient: float = 0.05  # Rotational drag coefficient
    
    # Thrust properties
    @export var thrustPositions: Array[Vector3] = []  # Positions of thrusters
    @export var forwardAcceleration: float = 50.0  # Forward acceleration rate
    @export var lateralAcceleration: float = 30.0  # Side/vertical acceleration rate
    @export var rotationalAcceleration: float = 8.0  # Rotational acceleration rate
    
    # Special flight modes
    @export var hasAfterburner: bool = false
    @export var afterburnerMultiplier: float = 2.0
    @export var hasGliding: bool = false
    @export var glidingMultiplier: float = 1.5
    @export var hasWarp: bool = false
    
    # Collision properties
    @export var collisionResponseMultiplier: float = 1.0  # How much collisions affect this object
    
    func _init():
        resource_name = "PhysicsProperties"
        
    func get_forward_acceleration() -> float:
        # Calculate forward acceleration based on acceleration time
        return maxVelocity.x / accelerationTime
        
    func get_lateral_acceleration() -> float:
        # Calculate lateral acceleration based on acceleration time
        return maxVelocity.x / accelerationTime  # Assuming same as forward for now
        
    func get_rotational_acceleration() -> float:
        # Calculate rotational acceleration
        return rotationalAcceleration

# Thruster effect for visual feedback
# Location: /features/effects/thruster/thruster.gd
class ThrusterEffect extends Node3D:
    var particle_system: GPUParticles3D
    var light: OmniLight3D
    var thrust_level: float = 0.0
    
    func _ready():
        # Create particle system
        particle_system = GPUParticles3D.new()
        particle_system.emitting = false
        add_child(particle_system)
        
        # Create light
        light = OmniLight3D.new()
        light.light_energy = 0.0
        add_child(light)
        
    func set_thrust_level(level: float):
        # Set thrust level affecting particle emission and light
        thrust_level = clamp(level, 0.0, 1.0)
        
        particle_system.emitting = thrust_level > 0.1
        particle_system.amount_ratio = thrust_level
        
        # Animate light intensity
        light.light_energy = thrust_level * 5.0
        
    func set_color(color: Color):
        # Set thruster color
        if particle_system.process_material is StandardMaterial3D:
            particle_system.process_material.albedo_color = color
            
    func set_size(size: float):
        # Set thruster effect size
        particle_system.scale = Vector3(size, size, size)

# Collision handler for physics responses
# Location: /scripts/physics/collision_handler.gd
class CollisionHandler extends Node:
    var entity: Entity
    var physics_controller: PhysicsController
    
    func _ready():
        entity = get_parent()
        if entity is Entity:
            physics_controller = entity.physicsController
            
    func _on_body_entered(body):
        # Handle collision with another body
        if body != entity and body is Entity:
            handle_collision_with_entity(body)
            
    func handle_collision_with_entity(other_entity: Entity):
        # Calculate collision response
        if physics_controller != null and other_entity.physicsController != null:
            # Calculate collision force based on relative velocity and masses
            var relative_velocity = physics_controller.velocity - other_entity.physicsController.velocity
            var collision_force = relative_velocity * (physics_controller.mass + other_entity.physicsController.mass) * 0.1
            
            # Apply forces to both entities
            physics_controller.apply_whack(collision_force, entity.global_position)
            other_entity.physicsController.apply_whack(-collision_force, other_entity.global_position)
            
    func _on_area_entered(area):
        # Handle area-based effects (e.g., nebula, gravity wells)
        if area.name == "GravityWell":
            handle_gravity_well_effect(area)
        elif area.name == "Nebula":
            handle_nebula_effect(area)
            
    func handle_gravity_well_effect(gravity_well):
        # Apply gravitational pull toward gravity well
        if physics_controller != null:
            var direction = (gravity_well.global_position - entity.global_position).normalized()
            var distance = entity.global_position.distance_to(gravity_well.global_position)
            var gravity_force = direction * (10000.0 / (distance * distance))  # Inverse square law
            physics_controller.apply_impulse(gravity_force)
            
    func handle_nebula_effect(nebula):
        # Apply nebula effects (reduced visibility, increased drag)
        if physics_controller != null:
            # Increase drag in nebula
            physics_controller.properties.dragCoefficient *= 2.0

# Space environment controller for global physics effects
# Location: /autoload/space_environment.gd
class SpaceEnvironment extends Node:
    var gravity_wells: Array[GravityWell] = []
    var nebula_fields: Array[NebulaField] = []
    
    func _ready():
        # Find all gravity wells and nebula fields in the scene
        find_space_effects()
        
    func find_space_effects():
        # Search for space effect nodes in the scene
        for child in get_children():
            if child is GravityWell:
                gravity_wells.append(child)
            elif child is NebulaField:
                nebula_fields.append(child)
                
    func _process(delta):
        # Update space environment effects
        update_gravity_wells(delta)
        update_nebula_fields(delta)
        
    func update_gravity_wells(delta):
        # Update all gravity well effects
        for well in gravity_wells:
            well.update_effect(delta)
            
    func update_nebula_fields(delta):
        # Update all nebula field effects
        for nebula in nebula_fields:
            nebula.update_effect(delta)
            
    func get_gravity_influence(position: Vector3) -> Vector3:
        # Calculate combined gravitational influence at a position
        var total_gravity = Vector3.ZERO
        
        for well in gravity_wells:
            var direction = (well.global_position - position).normalized()
            var distance = position.distance_to(well.global_position)
            var gravity = direction * (well.strength / (distance * distance))
            total_gravity += gravity
            
        return total_gravity
        
    func get_nebula_density(position: Vector3) -> float:
        # Calculate nebula density at a position
        var max_density = 0.0
        
        for nebula in nebula_fields:
            var distance = position.distance_to(nebula.global_position)
            if distance < nebula.radius:
                var density = 1.0 - (distance / nebula.radius)
                max_density = max(max_density, density)
                
        return max_density

# Gravity well affecting physics in an area
# Location: /scripts/physics/gravity_well.gd
class GravityWell extends Area3D:
    @export var strength: float = 1000.0
    @export var radius: float = 1000.0
    
    func _ready():
        # Set up collision shape
        var collision_shape = CollisionShape3D.new()
        var sphere_shape = SphereShape3D.new()
        sphere_shape.radius = radius
        collision_shape.shape = sphere_shape
        add_child(collision_shape)
        
        # Set up monitoring
        monitoring = true
        monitorable = false
        
    func update_effect(delta):
        # Update gravity well effect (e.g., visual effects)
        pass
        
    func get_gravitational_force(position: Vector3) -> Vector3:
        # Calculate gravitational force at a position
        var direction = (global_position - position).normalized()
        var distance = position.distance_to(global_position)
        return direction * (strength / (distance * distance))

# Nebula field affecting physics and visibility
# Location: /scripts/physics/nebula_field.gd
class NebulaField extends Area3D:
    @export var density: float = 0.5
    @export var radius: float = 2000.0
    @export var effect_multiplier: float = 1.5
    
    func _ready():
        # Set up collision shape
        var collision_shape = CollisionShape3D.new()
        var sphere_shape = SphereShape3D.new()
        sphere_shape.radius = radius
        collision_shape.shape = sphere_shape
        add_child(collision_shape)
        
        # Set up monitoring
        monitoring = true
        monitorable = false
        
    func update_effect(delta):
        # Update nebula field effect (e.g., visual effects)
        pass
        
    func get_nebula_effect(position: Vector3) -> float:
        # Calculate nebula effect strength at a position
        var distance = position.distance_to(global_position)
        if distance < radius:
            return (1.0 - (distance / radius)) * density
        return 0.0

# Physics debugger for development and tuning
# Location: /scripts/physics/physics_debugger.gd
class PhysicsDebugger extends Node:
    var debug_labels: Dictionary = {}
    var target_entity: Entity = null
    
    func _ready():
        # Create debug UI if in debug mode
        if OS.has_feature("debug"):
            create_debug_ui()
            
    func create_debug_ui():
        # Create debug labels for physics information
        pass
        
    func _process(delta):
        # Update debug information
        if target_entity != null and OS.has_feature("debug"):
            update_debug_info(delta)
            
    func update_debug_info(delta):
        # Update physics debug information display
        if target_entity.physicsController != null:
            var physics = target_entity.physicsController
            
            # Update velocity display
            update_debug_label("velocity", "Velocity: %.2f" % physics.get_velocity_magnitude())
            
            # Update thrust display
            update_debug_label("thrust", "Thrust: F:%.2f S:%.2f V:%.2f" % 
                             [physics.forward_thrust, physics.side_thrust, physics.vertical_thrust])
                             
            # Update rotation display
            update_debug_label("rotation", "Rotation: P:%.2f Y:%.2f R:%.2f" % 
                             [physics.angular_velocity.x, physics.angular_velocity.y, physics.angular_velocity.z])
                             
            # Update special modes
            update_debug_label("modes", "Afterburner:%s Gliding:%s" % 
                              [str(physics.is_afterburner_active), str(physics.is_gliding)])
                              
    func update_debug_label(label_name: String, text: String):
        # Update or create debug label
        if not debug_labels.has(label_name):
            var label = Label.new()
            label.name = label_name
            label.text = text
            # Position label appropriately
            add_child(label)
            debug_labels[label_name] = label
        else:
            debug_labels[label_name].text = text
            
    func set_target_entity(entity: Entity):
        # Set entity to debug
        target_entity = entity

# Physics manager for global physics operations
# Location: /autoload/physics_manager.gd
class PhysicsManager extends Node:
    static var instance: PhysicsManager
    
    var space_environment: SpaceEnvironment
    var physics_debugger: PhysicsDebugger
    
    func _ready():
        # Initialize singleton
        instance = self
        
        # Find space environment
        space_environment = get_node_or_null("/root/SpaceEnvironment")
        if space_environment == null:
            # Create default space environment
            space_environment = SpaceEnvironment.new()
            space_environment.name = "SpaceEnvironment"
            get_tree().root.add_child(space_environment)
            
        # Create physics debugger in debug builds
        if OS.has_feature("debug"):
            physics_debugger = PhysicsDebugger.new()
            physics_debugger.name = "PhysicsDebugger"
            add_child(physics_debugger)
            
    func _process(delta):
        # Update global physics effects
        if space_environment != null:
            # Apply global effects like gravity wells
            apply_global_effects(delta)
            
    func apply_global_effects(delta):
        # Apply global physics effects to all entities
        # This would typically iterate through all physics-enabled entities
        pass
        
    func get_space_environment_influence(position: Vector3) -> PhysicsInfluence:
        # Get combined influence of space environment at a position
        var influence = PhysicsInfluence.new()
        
        if space_environment != null:
            influence.gravity = space_environment.get_gravity_influence(position)
            influence.nebula_density = space_environment.get_nebula_density(position)
            
        return influence
        
    static func get_instance() -> PhysicsManager:
        return instance

# Container for physics influences at a point in space
class PhysicsInfluence:
    var gravity: Vector3 = Vector3.ZERO
    var nebula_density: float = 0.0
    var electromagnetic_interference: float = 0.0
    
    func get_total_influence() -> Vector3:
        # Return combined influence vector
        return gravity  # Simplified for this example

# Extension to ship class for physics integration
# Location: /features/fighters/ship_physics_extension.gd
class ShipPhysicsExtension extends Node:
    var ship: Ship
    var physics_controller: PhysicsController
    
    func _ready():
        ship = get_parent()
        if ship != null:
            # Create physics controller for ship
            physics_controller = PhysicsController.new(ship, ship.shipClass.physicsProperties)
            add_child(physics_controller)
            
            # Link physics controller to ship
            ship.physicsController = physics_controller
            
    func _process(delta):
        # Update ship-specific physics
        if ship != null and physics_controller != null:
            # Apply ship-specific physics effects
            update_ship_physics(delta)
            
    func update_ship_physics(delta):
        # Update ship-specific physics effects like afterburner fuel consumption
        if physics_controller.is_afterburner_active:
            # Consume afterburner fuel
            if ship.afterburnerFuel > 0:
                ship.afterburnerFuel -= delta * 10  # Fuel consumption rate
            else:
                # Ran out of fuel, disable afterburner
                physics_controller.activate_afterburner(false)
                
        # Update engine sounds based on thrust
        update_engine_sounds()
        
    func update_engine_sounds():
        # Update engine sound effects based on current thrust
        var thrust_level = abs(physics_controller.forward_thrust) + 
                          abs(physics_controller.side_thrust) + 
                          abs(physics_controller.vertical_thrust)
                          
        # Adjust engine sound pitch/volume based on thrust
        # This would interface with the audio system
        
    func apply_damage_physics(damage_amount: float, damage_location: Vector3):
        # Apply physics effects from damage (e.g., system damage affecting physics)
        if ship.subsystems.has("ENGINE"):
            var engine = ship.subsystems["ENGINE"]
            if engine.health < 50:  # Engine damaged
                # Reduce thrust effectiveness
                physics_controller.properties.forwardAcceleration *= 0.5
                physics_controller.properties.lateralAcceleration *= 0.5
                
    func initiate_warp_sequence():
        # Initiate warp in/out sequence
        if physics_controller != null:
            physics_controller.initiate_warp(true)
            # This would trigger warp visual effects and eventually move the ship
            
    func complete_warp_sequence():
        # Complete warp sequence and re-enable normal physics
        if physics_controller != null:
            physics_controller.initiate_warp(false)
```

### TRES Resources
```ini
# Location: /features/fighters/confed_rapier/rapier_physics.tres
[gd_resource type="Resource" load_steps=2 format=2]

[resource]
resource_name = "Fighter_Physics_Properties"
mass = 10.0
moment_of_inertia = Vector3(1.0, 1.0, 1.0)
max_velocity = Vector3(300, 300, 300)
max_rotational_velocity = Vector3(2.0, 2.0, 2.0)
acceleration_time = 1.5
deceleration_time = 2.0
drag_coefficient = 0.01
rotational_drag_coefficient = 0.05
thrust_positions = [Vector3(0, 0, -5), Vector3(2, 0, -3), Vector3(-2, 0, -3)]
forward_acceleration = 200.0
lateral_acceleration = 150.0
rotational_acceleration = 8.0
has_afterburner = true
afterburner_multiplier = 2.0
has_gliding = true
gliding_multiplier = 1.5
has_warp = true
collision_response_multiplier = 1.0

# Location: /features/capital_ships/tcs_tigers_claw/tigers_claw_physics.tres
[gd_resource type="Resource" load_steps=2 format=2]

[resource]
resource_name = "Capital_Ship_Physics_Properties"
mass = 10000.0
moment_of_inertia = Vector3(1000.0, 1000.0, 1000.0)
max_velocity = Vector3(100, 100, 100)
max_rotational_velocity = Vector3(0.2, 0.2, 0.2)
acceleration_time = 30.0
deceleration_time = 45.0
drag_coefficient = 0.005
rotational_drag_coefficient = 0.01
thrust_positions = [Vector3(0, 0, -100), Vector3(50, 0, -50), Vector3(-50, 0, -50)]
forward_acceleration = 10.0
lateral_acceleration = 5.0
rotational_acceleration = 0.5
has_afterburner = false
afterburner_multiplier = 1.0
has_gliding = false
gliding_multiplier = 1.0
has_warp = true
collision_response_multiplier = 0.1
```

### TSCN Scenes
```ini
# Location: /features/fighters/confed_rapier/rapier.tscn
[gd_scene load_steps=4 format=2]

[ext_resource path="res://scripts/physics/physics_controller.gd" type="Script" id=1]
[ext_resource path="res://features/fighters/confed_rapier/rapier_physics.tres" type="Resource" id=2]
[ext_resource path="res://features/effects/thruster/thruster.tscn" type="PackedScene" id=3]

[node name="Fighter" type="Node3D"]

[node name="PhysicsController" type="Node" parent="."]
script = ExtResource(1)
properties = ExtResource(2)

[node name="Thruster1" type="Node3D" parent="."]
instance = ExtResource(3)
position = Vector3(0, 0, -5)

[node name="Thruster2" type="Node3D" parent="."]
instance = ExtResource(3)
position = Vector3(2, 0, -3)

[node name="Thruster3" type="Node3D" parent="."]
instance = ExtResource(3)
position = Vector3(-2, 0, -3)
```

### Implementation Notes
The Physics Module in Godot leverages:

1. **Newtonian Physics**: Implements realistic space movement with momentum and inertia
2. **Component Architecture**: Physics controllers as separate components attached to entities
3. **Resources**: Physics properties as data-driven configurations organized in feature directories
4. **Scene System**: Thruster effects as scene components in `/features/effects/`
5. **Area3D**: For spatial effects like gravity wells and nebula fields organized in `/features/environment/`
6. **Signals**: For physics event notifications
7. **Autoload**: PhysicsManager as a global singleton in `/autoload/`
8. **Custom Integration**: Rather than using Godot's built-in physics bodies, implements custom space physics

This replaces the C++ physics simulation with Godot's node-based approach while preserving the same space flight dynamics. The implementation uses a custom physics controller to handle space-specific behaviors like Newtonian movement, which differs from Godot's default physics that includes gravity.

The physics system is designed to be modular, allowing different entities to have different physics properties through the PhysicsProperties resource system. Special effects like afterburners and gliding are implemented as modifiers to the base physics properties.

Collision detection uses Godot's Area3D system for detecting overlaps, while actual collision response is handled through custom physics calculations that preserve momentum and apply realistic forces.

The system supports global environmental effects through the SpaceEnvironment node, which can apply gravity wells and nebula effects to all entities in the scene. This approach provides a flexible framework for implementing complex space physics while maintaining good performance through the use of Godot's optimized spatial partitioning systems.

Following the feature-based organization principles:
- Core physics logic resides in `/scripts/physics/` as reusable components
- Visual effects are implemented as features in `/features/effects/` and `/features/environment/`
- Global systems are implemented as singletons in `/autoload/`
- Feature-specific physics properties are co-located with their respective features in `/features/`
- Shared assets are organized in `/assets/`