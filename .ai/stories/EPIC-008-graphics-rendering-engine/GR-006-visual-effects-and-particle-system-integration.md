# STORY GR-006: Visual Effects and Particle System Integration

## Story Overview
**Story ID**: GR-006  
**Epic**: EPIC-008 Graphics & Rendering Engine  
**Priority**: Critical  
**Status**: Ready for Development  
**Estimated Effort**: 5 days  
**Assignee**: Dev (GDScript Developer)

## User Story
**As a** game developer  
**I want** a comprehensive visual effects system that creates authentic WCS explosions, weapon effects, and environmental particles  
**So that** space combat feels visually engaging and authentic to the original WCS experience

## Background
This story implements the visual effects management system that coordinates all particle-based effects including explosions, weapon impacts, engine trails, and environmental effects. The system must integrate with the shader system and provide efficient effect lifecycle management.

## Acceptance Criteria

### Visual Effects Management
- [ ] **Effects Manager**: Central coordination of all visual effects
  - Manages effect creation, animation, and destruction lifecycle
  - Provides effect templates for common scenarios (weapons, explosions, engines)
  - Implements effect pooling for performance optimization
  - Coordinates with lighting and shader systems

- [ ] **Effect Categories**: Comprehensive effect type support
  - Weapon effects (muzzle flashes, beam impacts, projectile trails)
  - Explosion effects (ship destructions, missile impacts, multi-stage explosions)
  - Engine effects (thruster trails, afterburner glow, jump drive effects)
  - Environmental effects (space dust, nebula particles, atmospheric effects)
  - Shield effects (energy barriers, impact ripples, overload sequences)

- [ ] **Effect Templates**: Reusable effect configurations
  - Pre-configured effect definitions for different weapon types
  - Explosion templates for various ship classes and damage levels
  - Engine effect templates for different propulsion systems
  - Environmental effect presets for different space regions

### Particle System Integration
- [ ] **GPU Particle Integration**: Efficient Godot particle utilization
  - GPUParticles3D integration for high-performance effects
  - Custom ParticleProcessMaterial configurations for WCS-style effects
  - Particle system pooling and reuse for memory efficiency
  - Quality-based particle count adjustment

- [ ] **Particle Effect Types**: Specialized particle systems
  - Explosion particles with debris, fire, and smoke phases
  - Weapon impact sparks and energy discharge particles
  - Engine exhaust with heat distortion and particle trails
  - Space debris and environmental dust particles
  - Shield energy particles and electromagnetic effects

- [ ] **Effect Animation**: Time-based effect progression
  - Multi-stage effect sequences with timing control
  - Particle property animation (color, size, velocity, transparency)
  - Effect fade-in and fade-out transitions
  - Synchronized audio-visual effect coordination

### Weapon Effects System
- [ ] **Weapon Visual Effects**: Complete weapon effect library
  - Laser beam effects with energy fluctuation
  - Plasma bolt effects with particle trails
  - Missile exhaust trails and impact explosions
  - Mass driver projectile effects and kinetic impacts
  - Energy weapon charging and discharge effects

- [ ] **Impact Effects**: Weapon hit visualization
  - Surface-specific impact effects (hull, shield, asteroid)
  - Damage visualization with sparks, debris, and energy discharge
  - Penetration effects for different weapon types
  - Critical hit effects with enhanced visual feedback

### Explosion Effects System
- [ ] **Multi-Stage Explosions**: Authentic WCS explosion sequences
  - Initial flash with bright core and energy expansion
  - Secondary fire and plasma effects with debris
  - Tertiary smoke and dissipation effects
  - Shockwave effects for large explosions

- [ ] **Ship Destruction Effects**: Class-specific destruction sequences
  - Fighter destruction with single-stage explosion
  - Capital ship destruction with multiple explosion points
  - Subsystem destruction with localized effects
  - Debris field generation with physics-based movement

### Signal Architecture
- [ ] **Effects System Signals**: Event-driven effect coordination
  ```gdscript
  # Effect lifecycle signals
  signal effect_created(effect_id: String, effect_type: String, position: Vector3)
  signal effect_animation_started(effect_id: String, animation_name: String)
  signal effect_animation_completed(effect_id: String, animation_name: String)
  signal effect_destroyed(effect_id: String)
  
  # Performance management signals
  signal effects_performance_updated(active_effects: int, particle_count: int)
  signal effect_pool_resized(pool_name: String, pool_size: int)
  signal effect_quality_adjusted(quality_level: int)
  
  # Integration signals
  signal effect_lighting_requested(effect_id: String, lighting_config: Dictionary)
  signal effect_audio_triggered(effect_id: String, audio_config: Dictionary)
  ```

### Testing Requirements
- [ ] **Unit Tests**: Comprehensive effects system testing
  - Test effect creation and lifecycle management
  - Test particle system integration and pooling
  - Test effect template loading and application
  - Test performance optimization and quality scaling

- [ ] **Visual Tests**: Effect appearance and animation validation
  - Compare explosion effects with WCS reference sequences
  - Test weapon effect visual accuracy and timing
  - Validate particle system behavior and performance
  - Test effect synchronization with audio and lighting

- [ ] **Performance Tests**: Effects system optimization
  - Test performance with multiple simultaneous effects
  - Test memory usage with effect pooling
  - Test quality scaling responsiveness
  - Test effect cleanup and garbage collection

## Technical Specifications

### Effects Manager Architecture
```gdscript
class_name WCSEffectsManager
extends Node

## Central management for all visual effects and particle systems

signal effect_created(effect_id: String, effect_type: String, position: Vector3)
signal effect_animation_started(effect_id: String, animation_name: String)
signal effect_animation_completed(effect_id: String, animation_name: String)
signal effect_destroyed(effect_id: String)
signal effects_performance_updated(active_effects: int, particle_count: int)
signal effect_pool_resized(pool_name: String, pool_size: int)
signal effect_quality_adjusted(quality_level: int)
signal effect_lighting_requested(effect_id: String, lighting_config: Dictionary)
signal effect_audio_triggered(effect_id: String, audio_config: Dictionary)

var active_effects: Dictionary = {}
var effect_pools: Dictionary = {}
var effect_templates: Dictionary = {}
var lighting_controller: WCSLightingController
var shader_manager: WCSShaderManager

# Performance settings
var max_active_effects: int = 50
var max_particles_per_effect: int = 1000
var current_quality_level: int = 2
var effect_culling_distance: float = 2000.0

class VisualEffect:
    var effect_id: String
    var effect_type: String
    var effect_node: Node3D
    var particle_systems: Array[GPUParticles3D]
    var animation_player: AnimationPlayer
    var creation_time: float
    var duration: float
    var priority: int
    var is_looping: bool
    
    func _init(id: String, type: String, node: Node3D, prio: int = 5) -> void:
        effect_id = id
        effect_type = type
        effect_node = node
        priority = prio
        creation_time = Time.get_ticks_msec()
        duration = -1.0  # Infinite by default
        is_looping = false
        particle_systems = []

class EffectTemplate extends Resource:
    @export var template_name: String
    @export var effect_type: String
    @export var duration: float = 2.0
    @export var particle_configs: Array[ParticleConfig] = []
    @export var lighting_config: Dictionary = {}
    @export var audio_config: Dictionary = {}
    @export var shader_effects: Array[String] = []
    
    func is_valid() -> bool:
        return not template_name.is_empty() and duration > 0.0

class ParticleConfig extends Resource:
    @export var system_name: String
    @export var emission_count: int = 100
    @export var lifetime: float = 2.0
    @export var start_color: Color = Color.WHITE
    @export var end_color: Color = Color.TRANSPARENT
    @export var start_scale: float = 1.0
    @export var end_scale: float = 0.1
    @export var velocity_min: Vector3 = Vector3.ZERO
    @export var velocity_max: Vector3 = Vector3(10, 10, 10)
    @export var material_path: String

func _ready() -> void:
    load_effect_templates()
    setup_effect_pools()
    setup_performance_monitoring()

func load_effect_templates() -> void:
    var template_paths: Array[String] = WCSAssetRegistry.discover_assets_by_type("EffectTemplate")
    
    for template_path in template_paths:
        var template: EffectTemplate = WCSAssetLoader.load_asset(template_path)
        if template and template.is_valid():
            effect_templates[template.template_name] = template
        else:
            push_error("Failed to load effect template: " + template_path)

func create_weapon_effect(weapon_type: String, start_pos: Vector3, end_pos: Vector3, 
                         intensity: float = 1.0) -> String:
    var effect_id: String = _generate_effect_id()
    var effect_template: EffectTemplate = effect_templates.get(weapon_type + "_effect")
    
    if not effect_template:
        push_warning("No template found for weapon type: " + weapon_type)
        effect_template = effect_templates.get("default_weapon_effect")
    
    var effect_node: Node3D = _create_effect_from_template(effect_template, start_pos)
    
    # Configure weapon-specific properties
    _configure_weapon_effect(effect_node, weapon_type, start_pos, end_pos, intensity)
    
    # Register effect
    var visual_effect: VisualEffect = VisualEffect.new(effect_id, "weapon", effect_node, 7)
    active_effects[effect_id] = visual_effect
    
    effect_created.emit(effect_id, "weapon", start_pos)
    
    # Request lighting integration
    if effect_template.lighting_config:
        effect_lighting_requested.emit(effect_id, effect_template.lighting_config)
    
    return effect_id

func create_explosion_effect(position: Vector3, explosion_type: String, 
                           scale_factor: float = 1.0) -> String:
    var effect_id: String = _generate_effect_id()
    var template_name: String = explosion_type + "_explosion"
    var effect_template: EffectTemplate = effect_templates.get(template_name)
    
    if not effect_template:
        effect_template = effect_templates.get("default_explosion")
    
    var effect_node: Node3D = _create_effect_from_template(effect_template, position)
    effect_node.scale = Vector3.ONE * scale_factor
    
    # Create multi-stage explosion sequence
    _create_explosion_sequence(effect_node, explosion_type, scale_factor)
    
    # Register effect
    var visual_effect: VisualEffect = VisualEffect.new(effect_id, "explosion", effect_node, 9)
    visual_effect.duration = effect_template.duration * scale_factor
    active_effects[effect_id] = visual_effect
    
    effect_created.emit(effect_id, "explosion", position)
    
    return effect_id

func create_engine_trail_effect(ship_node: Node3D, engine_positions: Array[Vector3], 
                               throttle_level: float = 1.0) -> Array[String]:
    var effect_ids: Array[String] = []
    
    for engine_pos in engine_positions:
        var effect_id: String = _generate_effect_id()
        var effect_template: EffectTemplate = effect_templates.get("engine_trail")
        
        var trail_node: Node3D = _create_effect_from_template(effect_template, engine_pos)
        ship_node.add_child(trail_node)
        trail_node.position = engine_pos
        
        # Configure engine trail based on throttle
        _configure_engine_trail(trail_node, throttle_level)
        
        # Register persistent effect
        var visual_effect: VisualEffect = VisualEffect.new(effect_id, "engine_trail", trail_node, 5)
        visual_effect.is_looping = true
        active_effects[effect_id] = visual_effect
        
        effect_created.emit(effect_id, "engine_trail", ship_node.global_position + engine_pos)
        effect_ids.append(effect_id)
    
    return effect_ids

func create_shield_impact_effect(impact_pos: Vector3, shield_node: Node3D, 
                                impact_intensity: float = 1.0) -> String:
    var effect_id: String = _generate_effect_id()
    var effect_template: EffectTemplate = effect_templates.get("shield_impact")
    
    # Create impact ripple effect
    var ripple_node: Node3D = _create_effect_from_template(effect_template, impact_pos)
    shield_node.add_child(ripple_node)
    ripple_node.global_position = impact_pos
    
    # Create particle impact effects
    _create_shield_impact_particles(ripple_node, impact_intensity)
    
    # Register effect
    var visual_effect: VisualEffect = VisualEffect.new(effect_id, "shield_impact", ripple_node, 6)
    visual_effect.duration = 1.5
    active_effects[effect_id] = visual_effect
    
    effect_created.emit(effect_id, "shield_impact", impact_pos)
    
    return effect_id

func _create_effect_from_template(template: EffectTemplate, position: Vector3) -> Node3D:
    var effect_node: Node3D = Node3D.new()
    effect_node.name = template.template_name + "_effect"
    effect_node.global_position = position
    
    # Create particle systems from template
    for particle_config in template.particle_configs:
        var particle_system: GPUParticles3D = _create_particle_system(particle_config)
        effect_node.add_child(particle_system)
    
    # Apply shader effects
    for shader_name in template.shader_effects:
        var shader_material: ShaderMaterial = shader_manager.create_material_with_shader(shader_name)
        if shader_material:
            _apply_shader_to_effect(effect_node, shader_material)
    
    add_child(effect_node)
    return effect_node

func _create_particle_system(config: ParticleConfig) -> GPUParticles3D:
    var particles: GPUParticles3D = GPUParticles3D.new()
    particles.name = config.system_name
    particles.amount = config.emission_count
    particles.lifetime = config.lifetime
    particles.emitting = true
    
    # Create and configure material
    var material: ParticleProcessMaterial = ParticleProcessMaterial.new()
    material.direction = Vector3(0, 1, 0)
    material.initial_velocity_min = config.velocity_min.length()
    material.initial_velocity_max = config.velocity_max.length()
    material.scale_min = config.start_scale
    material.scale_max = config.end_scale
    material.color = config.start_color
    
    # Color animation
    var gradient: Gradient = Gradient.new()
    gradient.add_point(0.0, config.start_color)
    gradient.add_point(1.0, config.end_color)
    material.color_ramp = gradient
    
    particles.process_material = material
    
    # Load custom material if specified
    if not config.material_path.is_empty():
        var custom_material: Material = WCSAssetLoader.load_asset(config.material_path)
        if custom_material:
            particles.material_override = custom_material
    
    return particles

func _create_explosion_sequence(explosion_node: Node3D, explosion_type: String, scale: float) -> void:
    var sequences: Array[Dictionary] = []
    
    match explosion_type:
        "ship":
            sequences = [
                {"delay": 0.0, "phase": "flash", "intensity": 3.0 * scale, "duration": 0.2},
                {"delay": 0.2, "phase": "fire", "intensity": 2.0 * scale, "duration": 0.8},
                {"delay": 1.0, "phase": "smoke", "intensity": 1.0 * scale, "duration": 1.5},
                {"delay": 2.5, "phase": "dissipate", "intensity": 0.0, "duration": 1.0}
            ]
        "missile":
            sequences = [
                {"delay": 0.0, "phase": "flash", "intensity": 2.0 * scale, "duration": 0.1},
                {"delay": 0.1, "phase": "fire", "intensity": 1.5 * scale, "duration": 0.4},
                {"delay": 0.5, "phase": "smoke", "intensity": 0.5 * scale, "duration": 0.8}
            ]
        "capital_ship":
            sequences = [
                {"delay": 0.0, "phase": "initial", "intensity": 4.0 * scale, "duration": 0.5},
                {"delay": 0.5, "phase": "secondary", "intensity": 3.0 * scale, "duration": 1.0},
                {"delay": 1.5, "phase": "tertiary", "intensity": 2.0 * scale, "duration": 2.0},
                {"delay": 3.5, "phase": "final", "intensity": 0.0, "duration": 2.0}
            ]
    
    _animate_explosion_phases(explosion_node, sequences)

func _animate_explosion_phases(explosion_node: Node3D, sequences: Array[Dictionary]) -> void:
    var animation_player: AnimationPlayer = AnimationPlayer.new()
    explosion_node.add_child(animation_player)
    
    var animation: Animation = Animation.new()
    var total_duration: float = 0.0
    
    for sequence in sequences:
        var phase_end: float = sequence.delay + sequence.duration
        if phase_end > total_duration:
            total_duration = phase_end
        
        # Animate particle systems for this phase
        _add_phase_animation_tracks(animation, sequence, explosion_node)
    
    animation.length = total_duration
    var animation_library: AnimationLibrary = AnimationLibrary.new()
    animation_library.add_animation("explosion_sequence", animation)
    animation_player.add_animation_library("default", animation_library)
    
    animation_player.play("default/explosion_sequence")

func update_engine_trail_throttle(effect_ids: Array[String], throttle_level: float) -> void:
    for effect_id in effect_ids:
        if effect_id in active_effects:
            var visual_effect: VisualEffect = active_effects[effect_id]
            _configure_engine_trail(visual_effect.effect_node, throttle_level)

func destroy_effect(effect_id: String) -> void:
    if effect_id in active_effects:
        var visual_effect: VisualEffect = active_effects[effect_id]
        
        # Fade out before destruction
        _fade_out_effect(visual_effect.effect_node, 0.2)
        
        # Schedule cleanup
        get_tree().create_timer(0.3).timeout.connect(func():
            if visual_effect.effect_node:
                visual_effect.effect_node.queue_free()
            active_effects.erase(effect_id)
            effect_destroyed.emit(effect_id)
        )

func set_effect_quality(quality_level: int) -> void:
    current_quality_level = clamp(quality_level, 0, 3)
    
    # Adjust particle counts and complexity
    for effect_id in active_effects:
        var visual_effect: VisualEffect = active_effects[effect_id]
        _adjust_effect_quality(visual_effect, current_quality_level)
    
    effect_quality_adjusted.emit(current_quality_level)

func _adjust_effect_quality(visual_effect: VisualEffect, quality: int) -> void:
    var quality_multipliers: Array[float] = [0.3, 0.6, 0.8, 1.0]  # Low to Ultra
    var multiplier: float = quality_multipliers[quality]
    
    for particle_system in visual_effect.particle_systems:
        var original_amount: int = particle_system.amount
        particle_system.amount = int(original_amount * multiplier)
```

## Implementation Plan

### Phase 1: Core Effects System (2 days)
1. **Effects Manager Framework**
   - Create WCSEffectsManager with lifecycle management
   - Implement effect templates and loading system
   - Add effect pooling and performance optimization
   - Set up signal architecture and integration points

2. **Basic Effect Types**
   - Implement weapon impact effects
   - Create basic explosion effects
   - Add engine trail particle systems
   - Test effect creation and destruction

### Phase 2: Advanced Effects (2 days)
1. **Multi-Stage Explosions**
   - Implement ship destruction sequences
   - Create missile impact effects
   - Add capital ship explosion systems
   - Implement debris field generation

2. **Shield and Environmental Effects**
   - Create shield impact ripple effects
   - Add space dust and environmental particles
   - Implement atmospheric effects for nebulae
   - Add jump drive and warp effects

### Phase 3: Integration and Optimization (1 day)
1. **System Integration**
   - Integrate with lighting system for effect illumination
   - Coordinate with shader system for visual enhancement
   - Test with audio system for synchronized effects
   - Validate performance across quality settings

2. **Test Suite Implementation**
   - Write comprehensive unit tests for effects
   - Add visual validation tests with WCS references
   - Implement performance benchmarking
   - Test memory management and pooling

## Dependencies
- **GR-001**: Graphics Rendering Engine Core Framework (performance monitoring)
- **GR-003**: Shader System (effect shader integration)
- **GR-005**: Dynamic Lighting System (effect lighting coordination)
- **Godot Systems**: GPUParticles3D, ParticleProcessMaterial, AnimationPlayer

## Validation Criteria
- [ ] All weapon effects render with authentic WCS appearance
- [ ] Explosion sequences match WCS multi-stage progression
- [ ] Engine trail effects respond correctly to throttle changes
- [ ] Shield impact effects display proper ripple and energy effects
- [ ] Performance optimization maintains target frame rates with multiple effects
- [ ] Effect pooling prevents memory leaks during extended combat
- [ ] Quality scaling adjusts particle counts appropriately
- [ ] Integration with lighting and shader systems confirmed
- [ ] All unit tests pass with >90% coverage

## Definition of Done
- [ ] All acceptance criteria implemented and tested
- [ ] Complete visual effects library operational
- [ ] Multi-stage explosion and weapon effect systems functional
- [ ] Particle system integration with performance optimization
- [ ] Effect template system with reusable configurations
- [ ] Integration with lighting and shader systems confirmed
- [ ] Comprehensive test suite implemented and passing
- [ ] Performance monitoring and quality adjustment functional
- [ ] Visual validation confirms authentic WCS effects
- [ ] Code review completed and approved
- [ ] Documentation updated with effects system API
- [ ] System ready for integration with combat and object systems

## Notes
- Effects must maintain authentic WCS visual characteristics and timing
- Performance optimization critical for scenes with many simultaneous effects
- Effect pooling and lifecycle management prevent memory issues
- Multi-stage explosions essential for authentic ship destruction sequences
- Integration with lighting creates immersive visual experiences