# Visual Effects Module

## Purpose
The Visual Effects Module handles all special visual effects in the game, including particles, explosions, animations, lighting, and other graphical enhancements that enhance the visual quality and provide feedback for gameplay events.

## Components
- **Particle System** (`particle/`): Special effects through particle rendering
- **Fireball System** (`fireball/`): Explosion effects and area damage visualization
- **Animation System** (`anim/`): Sprite-based animations and texture animations
- **Lighting System** (`lighting/`): Dynamic and static lighting calculations
- **Debris System** (`debris/`): Destruction effects and debris physics
- **Model System** (`model/`): 3D models with special effects capabilities
- **Bitmap Manager** (`bmpman/`): Texture loading and management

## Dependencies
- **Core Entity Module**: Effects are often entity-based
- **Graphics Module**: Rendering functions and pipeline
- **Model Module**: 3D models for effects
- **Physics Module**: Physics for particle and debris movement
- **Weapon Module**: Weapon effect particles
- **Ship Module**: Engine trail particles

## C++ Components
- `particle_create()`, `particle_process()`: Particle effects management
- `fireball_create()`, `fireball_process()`: Explosion effects
- `anim_load()`, `anim_render()`: Animation system
- `light_add()`, `light_apply()`: Lighting system
- `debris_create()`, `debris_process()`: Debris system
- `model_render()`: 3D model rendering with effects
- `bm_load()`, `bm_create()`: Bitmap/texture management

## Godot Equivalent Mapping

### Native GDScript Classes
```gdscript
# Particle system controller for special effects
class ParticleSystem:
    var entity: Entity
    var particles: Array[Particle]
    var emitter: ParticleEmitter
    var material: ParticleMaterial
    var lifetime: float = 5.0
    var isEmitting: bool = false
    
    func _init(owner_entity: Entity):
        entity = owner_entity
        particles = []
        
    func _process(delta):
        update_particles(delta)
        if isEmitting:
            emit_particles(delta)
            
    func update_particles(delta):
        # Update existing particles
        for i in range(particles.size() - 1, -1, -1):
            var particle = particles[i]
            particle.lifetime -= delta
            if particle.lifetime <= 0:
                particles.remove_at(i)
            else:
                particle.position += particle.velocity * delta
                particle.update_visual(delta)
                
    func emit_particles(delta):
        # Create new particles based on emitter properties
        var particles_to_create = emitter.particles_per_second * delta
        for i in range(ceil(particles_to_create)):
            var particle = create_particle()
            particles.append(particle)
            
    func create_particle() -> Particle:
        var particle = Particle.new()
        particle.position = entity.global_position
        particle.velocity = emitter.get_random_velocity()
        particle.lifetime = emitter.particle_lifetime
        particle.start_color = emitter.start_color
        particle.end_color = emitter.end_color
        particle.start_size = emitter.start_size
        particle.end_size = emitter.end_size
        return particle

# Individual particle for effects
class Particle:
    var position: Vector3
    var velocity: Vector3
    var lifetime: float
    var start_color: Color
    var end_color: Color
    var start_size: float
    var end_size: float
    var mesh_instance: MeshInstance3D
    
    func update_visual(delta):
        # Update visual representation
        var life_ratio = 1.0 - (lifetime / get_initial_lifetime())
        var current_color = start_color.lerp(end_color, life_ratio)
        var current_size = lerp(start_size, end_size, life_ratio)
        
        if mesh_instance != null:
            mesh_instance.material_override.albedo_color = current_color
            mesh_instance.scale = Vector3(current_size, current_size, current_size)

# Particle emitter configuration
class ParticleEmitter:
    var particles_per_second: float = 100
    var particle_lifetime: float = 2.0
    var start_color: Color = Color(1, 1, 0, 1)  # Yellow
    var end_color: Color = Color(1, 0, 0, 0)    # Red to transparent
    var start_size: float = 0.5
    var end_size: float = 0.1
    var velocity_min: Vector3 = Vector3(-10, -10, -10)
    var velocity_max: Vector3 = Vector3(10, 10, 10)
    
    func get_random_velocity() -> Vector3:
        return Vector3(
            randf_range(velocity_min.x, velocity_max.x),
            randf_range(velocity_min.y, velocity_max.y),
            randf_range(velocity_min.z, velocity_max.z)
        )

# Explosion effect combining multiple systems
class ExplosionEffect:
    var position: Vector3
    var radius: float
    var intensity: float
    var particle_system: GPUParticles3D
    var light: OmniLight3D
    var lifetime: float = 3.0
    var current_lifetime: float = 0.0
    
    func _init(explosion_position: Vector3, explosion_radius: float, explosion_intensity: float):
        position = explosion_position
        radius = explosion_radius
        intensity = explosion_intensity
        
        # Create particle system
        particle_system = GPUParticles3D.new()
        particle_system.position = position
        particle_system.emitting = true
        particle_system.lifetime = 2.0
        particle_system.one_shot = true
        
        # Create light
        light = OmniLight3D.new()
        light.position = position
        light.light_energy = intensity
        light.light_color = Color(1, 0.5, 0)  # Orange
        light.omni_range = radius * 2
        
        # Add to scene
        var root = get_tree().root
        root.add_child(particle_system)
        root.add_child(light)
        
    func _process(delta):
        current_lifetime += delta
        if current_lifetime >= lifetime:
            # Fade out light
            light.light_energy = lerp(light.light_energy, 0.0, delta * 2)
            if light.light_energy < 0.01:
                queue_free()
                
    func queue_free():
        if particle_system != null:
            particle_system.queue_free()
        if light != null:
            light.queue_free()

# Animated texture system
class AnimatedTexture:
    var frames: Array[Texture2D]
    var current_frame: int = 0
    var frame_time: float = 0.1
    var current_time: float = 0.0
    var is_looping: bool = true
    var material: StandardMaterial3D
    
    func _init(texture_frames: Array[Texture2D], frame_duration: float):
        frames = texture_frames
        frame_time = frame_duration
        if frames.size() > 0:
            update_material_texture()
            
    func _process(delta):
        current_time += delta
        if current_time >= frame_time:
            current_time = 0
            current_frame = (current_frame + 1) % frames.size()
            update_material_texture()
            
    func update_material_texture():
        if material != null and frames.size() > 0:
            material.albedo_texture = frames[current_frame]
```

### TRES Resources
```ini
[gd_resource type="Resource" load_steps=3 format=2]

[ext_resource path="res://textures/explosion_01.png" type="Texture2D" id=1]
[ext_resource path="res://textures/explosion_02.png" type="Texture2D" id=2]

[resource]
resource_name = "Explosion_Particle_Material"
particles_per_second = 200
particle_lifetime = 1.5
start_color = Color(1, 1, 0, 1)
end_color = Color(1, 0, 0, 0)
start_size = 1.0
end_size = 0.1
velocity_min = Vector3(-50, -50, -50)
velocity_max = Vector3(50, 50, 50)

[gd_resource type="Resource" load_steps=3 format=2]

[resource]
resource_name = "Engine_Trail_Animation"
frames = [ExtResource(1), ExtResource(2)]
frame_time = 0.05
is_looping = true
```

### TSCN Scenes
```ini
[gd_scene load_steps=4 format=2]

[ext_resource path="res://scripts/particle_system.gd" type="Script" id=1]
[ext_resource path="res://resources/explosion_material.tres" type="Resource" id=2]
[ext_resource path="res://models/explosion_effect.tscn" type="PackedScene" id=3]

[node name="ExplosionEffect" type="Node3D"]

[node name="ParticleSystem" type="Node" parent="."]

[node name="ExplosionModel" type="Node3D" parent="."]
instance = ExtResource(3)
```

### Implementation Notes
The Visual Effects Module in Godot leverages:
1. **GPUParticles3D**: For high-performance particle effects
2. **AnimatedTexture**: For sprite-based animations
3. **Light3D**: For dynamic lighting effects
4. **ShaderMaterials**: For custom visual effects
5. **Resources**: Effect configurations as data-driven assets
6. **Scene System**: Complex effects as scene compositions

This replaces the C++ custom rendering systems with Godot's built-in visual effects systems while preserving the same visual quality and gameplay feedback. The particle system uses Godot's optimized GPU-based particles rather than CPU-based particle management.