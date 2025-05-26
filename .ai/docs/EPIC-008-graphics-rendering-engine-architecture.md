# EPIC-008: Graphics & Rendering Engine Architecture

## Architecture Overview

The Graphics & Rendering Engine provides high-fidelity visual rendering for WCS-Godot, implementing authentic WCS visual effects through modern Godot 4 rendering features while maintaining performance and visual consistency with the original game's aesthetic.

## System Goals

- **Visual Fidelity**: Faithful recreation of WCS visual style and effects
- **Performance**: Smooth 60+ FPS rendering with complex scenes
- **Scalability**: Adjustable quality settings for different hardware
- **Authenticity**: Preserve WCS lighting, materials, and effect characteristics
- **Modularity**: Component-based rendering system supporting customization

## Core Architecture

### Rendering Management Hierarchy

```
RenderingManager (AutoLoad Singleton)
├── MaterialSystem (Node)
├── ShaderManager (Node) 
├── LightingController (Node)
├── EffectsManager (Node)
├── TextureStreamer (Node)
├── ModelRenderer (Node)
└── PerformanceMonitor (Node)
```

### Rendering Foundation

**RenderingManager (Singleton)**
```gdscript
class_name RenderingManager
extends Node

## Central management for all rendering systems and visual effects

signal material_loaded(material_name: String)
signal shader_compiled(shader_name: String)
signal render_quality_changed(quality_level: int)
signal performance_warning(system: String, metric: float)

var material_system: MaterialSystem
var shader_manager: ShaderManager
var lighting_controller: LightingController
var effects_manager: EffectsManager
var texture_streamer: TextureStreamer
var model_renderer: ModelRenderer
var performance_monitor: PerformanceMonitor

var render_quality: RenderQuality = RenderQuality.HIGH
var target_framerate: float = 60.0
var current_scene_complexity: float = 0.0

enum RenderQuality {
    LOW,
    MEDIUM,
    HIGH,
    ULTRA
}

func _ready() -> void:
    initialize_rendering_systems()
    configure_godot_rendering()
    load_wcs_visual_profiles()

func initialize_rendering_systems() -> void:
    material_system = MaterialSystem.new()
    shader_manager = ShaderManager.new()
    lighting_controller = LightingController.new()
    effects_manager = EffectsManager.new()
    texture_streamer = TextureStreamer.new()
    model_renderer = ModelRenderer.new()
    performance_monitor = PerformanceMonitor.new()
    
    add_child(material_system)
    add_child(shader_manager)
    add_child(lighting_controller)
    add_child(effects_manager)
    add_child(texture_streamer)
    add_child(model_renderer)
    add_child(performance_monitor)

func configure_godot_rendering() -> void:
    # Configure Godot's rendering server for WCS-style visuals
    var rs = RenderingServer
    
    # Set up space rendering parameters
    rs.environment_set_bg(Environment.BG_SKY)
    rs.environment_set_sky_custom_fov(Environment, 75.0)
    
    # Configure lighting for space environment
    rs.directional_light_set_shadow_mode(
        Environment.LIGHT_DIRECTIONAL_SHADOW_ORTHOGONAL
    )
    
    # Set up post-processing pipeline
    configure_post_processing()

func set_render_quality(quality: RenderQuality) -> void:
    render_quality = quality
    apply_quality_settings(quality)
    render_quality_changed.emit(quality)
```

## Material System Architecture

### WCS Material Conversion

**MaterialSystem**
```gdscript
class_name MaterialSystem
extends Node

## Manages conversion and runtime handling of WCS materials

var material_cache: Dictionary = {}
var wcs_material_database: WCSMaterialDatabase
var material_conversion_rules: Dictionary = {}

class WCSMaterial:
    var name: String
    var diffuse_texture: String
    var normal_texture: String
    var specular_texture: String
    var glow_texture: String
    var reflectance: float = 0.0
    var shininess: float = 1.0
    var alpha_test: float = 0.0
    var blend_mode: String = "OPAQUE"
    var double_sided: bool = false
    var wcs_flags: int = 0

func load_wcs_material_database() -> void:
    wcs_material_database = WCSMaterialDatabase.new()
    wcs_material_database.load_from_resources()
    
    # Set up conversion rules for different material types
    material_conversion_rules = {
        "hull": _create_hull_material_rule(),
        "cockpit": _create_cockpit_material_rule(),
        "engine": _create_engine_material_rule(),
        "weapon": _create_weapon_material_rule(),
        "thruster": _create_thruster_material_rule(),
        "shield": _create_shield_material_rule(),
        "space": _create_space_material_rule()
    }

func convert_wcs_material(wcs_mat: WCSMaterial) -> StandardMaterial3D:
    var godot_material = StandardMaterial3D.new()
    
    # Basic properties
    godot_material.resource_name = wcs_mat.name
    godot_material.albedo_color = Color.WHITE
    
    # Texture assignment
    if not wcs_mat.diffuse_texture.is_empty():
        var diffuse_tex = texture_streamer.load_texture(wcs_mat.diffuse_texture)
        godot_material.albedo_texture = diffuse_tex
    
    if not wcs_mat.normal_texture.is_empty():
        var normal_tex = texture_streamer.load_texture(wcs_mat.normal_texture)
        godot_material.normal_texture = normal_tex
        godot_material.normal_enabled = true
    
    # Material properties conversion
    godot_material.metallic = _convert_wcs_reflectance(wcs_mat.reflectance)
    godot_material.roughness = _convert_wcs_shininess(wcs_mat.shininess)
    
    # Alpha handling
    if wcs_mat.alpha_test > 0.0:
        godot_material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
        godot_material.alpha_scissor_threshold = wcs_mat.alpha_test
    elif wcs_mat.blend_mode == "ALPHA":
        godot_material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
    
    # Glow effects
    if not wcs_mat.glow_texture.is_empty():
        var glow_tex = texture_streamer.load_texture(wcs_mat.glow_texture)
        godot_material.emission_texture = glow_tex
        godot_material.emission_enabled = true
        godot_material.emission_energy = 1.0
    
    # Special WCS flags handling
    _apply_wcs_flags(godot_material, wcs_mat.wcs_flags)
    
    # Cache the converted material
    material_cache[wcs_mat.name] = godot_material
    
    return godot_material

func _convert_wcs_reflectance(wcs_reflectance: float) -> float:
    # Convert WCS reflectance (0-1) to Godot metallic (0-1)
    # WCS uses different reflection model, adjust accordingly
    return clamp(wcs_reflectance * 0.8, 0.0, 1.0)

func _convert_wcs_shininess(wcs_shininess: float) -> float:
    # Convert WCS shininess to Godot roughness (inverted relationship)
    return clamp(1.0 - (wcs_shininess / 128.0), 0.0, 1.0)

func _apply_wcs_flags(material: StandardMaterial3D, flags: int) -> void:
    # WCS material flags interpretation
    const FLAG_ADDITIVE = 1 << 0
    const FLAG_NO_LIGHTING = 1 << 1
    const FLAG_FULLBRIGHT = 1 << 2
    const FLAG_ANIMATED = 1 << 3
    
    if flags & FLAG_ADDITIVE:
        material.blend_mode = BaseMaterial3D.BLEND_ADD
    
    if flags & FLAG_NO_LIGHTING:
        material.flags_unshaded = true
    
    if flags & FLAG_FULLBRIGHT:
        material.emission_enabled = true
        material.emission_energy = 1.0
    
    if flags & FLAG_ANIMATED:
        # Set up animated texture support
        _setup_animated_material(material)
```

## Shader Management System

### WCS Shader Conversion

**ShaderManager**
```gdscript
class_name ShaderManager
extends Node

## Manages shader conversion and compilation from WCS to Godot

var shader_cache: Dictionary = {}
var wcs_shader_database: Dictionary = {}
var custom_shaders: Dictionary = {}

func load_wcs_shaders() -> void:
    # Load WCS shader definitions and convert to Godot shaders
    _load_ship_hull_shaders()
    _load_weapon_effect_shaders()
    _load_shield_shaders()
    _load_thruster_shaders()
    _load_explosion_shaders()
    _load_nebula_shaders()

func _load_ship_hull_shaders() -> void:
    # WCS-style ship hull shader with damage mapping
    var hull_shader_code = """
shader_type canvas_item;

uniform sampler2D diffuse_texture : source_color;
uniform sampler2D normal_texture : hint_normal;
uniform sampler2D damage_texture : source_color;
uniform float damage_level : hint_range(0.0, 1.0) = 0.0;
uniform float hull_metallic : hint_range(0.0, 1.0) = 0.3;
uniform float hull_roughness : hint_range(0.0, 1.0) = 0.7;
uniform vec3 hull_tint : source_color = vec3(1.0);

varying vec3 world_normal;
varying vec3 world_position;

void vertex() {
    world_position = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
    world_normal = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz);
}

void fragment() {
    vec4 diffuse = texture(diffuse_texture, UV);
    vec4 damage = texture(damage_texture, UV);
    vec3 normal = texture(normal_texture, UV).rgb * 2.0 - 1.0;
    
    // Apply damage blending
    vec3 final_color = mix(diffuse.rgb * hull_tint, damage.rgb, damage_level * damage.a);
    
    // WCS-style metal reflection
    float fresnel = 1.0 - dot(normalize(world_normal), normalize(CAMERA_POSITION_WORLD - world_position));
    final_color += vec3(hull_metallic * fresnel * 0.5);
    
    ALBEDO = final_color;
    METALLIC = hull_metallic;
    ROUGHNESS = hull_roughness;
    NORMAL_MAP = normal;
    ALPHA = diffuse.a;
}
"""
    
    var hull_shader = Shader.new()
    hull_shader.code = hull_shader_code
    custom_shaders["ship_hull"] = hull_shader

func _load_weapon_effect_shaders() -> void:
    # Laser beam shader
    var laser_shader_code = """
shader_type spatial;
render_mode additive, vertex_lighting, shadows_disabled;

uniform float beam_intensity : hint_range(0.0, 10.0) = 2.0;
uniform vec3 beam_color : source_color = vec3(1.0, 0.0, 0.0);
uniform float beam_width : hint_range(0.1, 2.0) = 1.0;
uniform float flicker_speed : hint_range(0.0, 10.0) = 5.0;
uniform sampler2D noise_texture : source_color;

varying float distance_from_center;
varying vec2 beam_uv;

void vertex() {
    beam_uv = UV;
    
    // Calculate distance from beam center for tapering
    distance_from_center = abs(UV.y - 0.5) * 2.0;
    
    VERTEX = VERTEX;
}

void fragment() {
    float time_factor = TIME * flicker_speed;
    vec4 noise = texture(noise_texture, beam_uv + vec2(time_factor * 0.1, 0.0));
    
    // Beam intensity falloff from center
    float intensity_falloff = 1.0 - pow(distance_from_center / beam_width, 2.0);
    intensity_falloff = max(0.0, intensity_falloff);
    
    // Add noise for energy effect
    float final_intensity = beam_intensity * intensity_falloff * (0.8 + 0.2 * noise.r);
    
    ALBEDO = beam_color;
    EMISSION = beam_color * final_intensity;
    ALPHA = intensity_falloff;
}
"""
    
    var laser_shader = Shader.new()
    laser_shader.code = laser_shader_code
    custom_shaders["laser_beam"] = laser_shader

func _load_shield_shaders() -> void:
    # WCS-style energy shield shader
    var shield_shader_code = """
shader_type spatial;
render_mode cull_front, depth_draw_opaque, depth_test_disabled, shadows_disabled, ambient_light_disabled;

uniform float shield_strength : hint_range(0.0, 1.0) = 1.0;
uniform vec3 shield_color : source_color = vec3(0.0, 0.5, 1.0);
uniform float pulse_speed : hint_range(0.0, 10.0) = 3.0;
uniform float impact_intensity : hint_range(0.0, 5.0) = 0.0;
uniform vec3 impact_position : source_color;
uniform float impact_radius : hint_range(0.0, 2.0) = 0.5;

varying vec3 world_position;
varying vec3 world_normal;
varying float fresnel;

void vertex() {
    world_position = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
    world_normal = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz);
    
    vec3 camera_dir = normalize(CAMERA_POSITION_WORLD - world_position);
    fresnel = 1.0 - dot(world_normal, camera_dir);
}

void fragment() {
    float time_pulse = sin(TIME * pulse_speed) * 0.5 + 0.5;
    
    // Calculate impact effect
    float impact_distance = distance(world_position, impact_position);
    float impact_effect = 1.0 - smoothstep(0.0, impact_radius, impact_distance);
    impact_effect *= impact_intensity;
    
    // Shield visibility based on strength and fresnel
    float shield_alpha = shield_strength * fresnel * (0.3 + 0.2 * time_pulse);
    shield_alpha += impact_effect;
    
    ALBEDO = shield_color;
    EMISSION = shield_color * (0.5 + impact_effect);
    ALPHA = clamp(shield_alpha, 0.0, 0.8);
}
"""
    
    var shield_shader = Shader.new()
    shield_shader.code = shield_shader_code
    custom_shaders["energy_shield"] = shield_shader

func get_shader(shader_name: String) -> Shader:
    if shader_name in custom_shaders:
        return custom_shaders[shader_name]
    
    # Fallback to default shaders
    return null
```

## Lighting System

### Space Environment Lighting

**LightingController**
```gdscript
class_name LightingController
extends Node

## Manages dynamic lighting for space environments

var main_star_light: DirectionalLight3D
var ambient_space_light: Environment
var nebula_lighting: Array[Light3D] = []
var dynamic_lights: Array[Light3D] = []

var lighting_profile: SpaceLightingProfile

class SpaceLightingProfile:
    var star_color: Color = Color(1.0, 0.95, 0.8)
    var star_intensity: float = 1.0
    var ambient_color: Color = Color(0.1, 0.1, 0.2)
    var ambient_intensity: float = 0.3
    var nebula_ambient: Color = Color(0.3, 0.1, 0.4)
    var shadow_softness: float = 0.5

func setup_space_lighting() -> void:
    create_main_star_light()
    configure_ambient_lighting()
    setup_dynamic_lighting_system()

func create_main_star_light() -> void:
    main_star_light = DirectionalLight3D.new()
    main_star_light.name = "MainStarLight"
    
    # Configure for space environment
    main_star_light.light_color = lighting_profile.star_color
    main_star_light.light_energy = lighting_profile.star_intensity
    main_star_light.shadow_enabled = true
    main_star_light.directional_shadow_mode = DirectionalLight3D.SHADOW_ORTHOGONAL
    main_star_light.directional_shadow_max_distance = 10000.0
    
    # Position like a distant star
    main_star_light.rotation_degrees = Vector3(-45, 30, 0)
    
    add_child(main_star_light)

func configure_ambient_lighting() -> void:
    ambient_space_light = Environment.new()
    
    # Space-appropriate ambient lighting
    ambient_space_light.background_mode = Environment.BG_COLOR
    ambient_space_light.background_color = Color.BLACK
    ambient_space_light.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
    ambient_space_light.ambient_light_color = lighting_profile.ambient_color
    ambient_space_light.ambient_light_energy = lighting_profile.ambient_intensity
    
    # Add subtle reflection for metal surfaces
    var star_sky = Sky.new()
    star_sky.sky_material = create_star_field_material()
    ambient_space_light.sky = star_sky
    ambient_space_light.background_mode = Environment.BG_SKY

func create_weapon_muzzle_flash(position: Vector3, color: Color, intensity: float) -> void:
    var flash_light = OmniLight3D.new()
    flash_light.global_position = position
    flash_light.light_color = color
    flash_light.light_energy = intensity
    flash_light.omni_range = 50.0
    
    add_child(flash_light)
    dynamic_lights.append(flash_light)
    
    # Animate flash
    var tween = create_tween()
    tween.tween_property(flash_light, "light_energy", 0.0, 0.2)
    tween.tween_callback(func(): _remove_dynamic_light(flash_light))

func create_engine_glow(ship: Node3D, engine_points: Array[Vector3]) -> void:
    for point in engine_points:
        var engine_light = OmniLight3D.new()
        engine_light.position = point
        engine_light.light_color = Color.CYAN
        engine_light.light_energy = 2.0
        engine_light.omni_range = 30.0
        
        ship.add_child(engine_light)

func update_nebula_lighting(nebula_color: Color, density: float) -> void:
    lighting_profile.ambient_color = lighting_profile.ambient_color.lerp(nebula_color, density * 0.3)
    lighting_profile.ambient_intensity *= (1.0 + density * 0.5)
    
    configure_ambient_lighting()
```

## Effects Management

### Visual Effects System

**EffectsManager**
```gdscript
class_name EffectsManager
extends Node

## Manages all visual effects including explosions, weapons, and environmental effects

var effect_pools: Dictionary = {}
var active_effects: Array[Node3D] = []
var particle_systems: Dictionary = {}

func _ready() -> void:
    setup_effect_pools()
    load_wcs_effect_templates()

func setup_effect_pools() -> void:
    # Pre-create pools for common effects
    create_effect_pool("explosion_small", 20)
    create_effect_pool("explosion_large", 10)
    create_effect_pool("laser_impact", 50)
    create_effect_pool("muzzle_flash", 30)
    create_effect_pool("engine_trail", 20)
    create_effect_pool("shield_impact", 15)

func create_weapon_impact_effect(impact_point: Vector3, impact_normal: Vector3, 
                                weapon_type: String, target_material: String) -> void:
    var effect_name = "impact_" + weapon_type + "_" + target_material
    var effect = get_pooled_effect(effect_name)
    
    if not effect:
        effect = create_impact_effect_template(weapon_type, target_material)
    
    effect.global_position = impact_point
    effect.look_at(impact_point + impact_normal, Vector3.UP)
    
    # Configure effect based on weapon and material
    configure_impact_effect(effect, weapon_type, target_material)
    
    effect.restart()
    active_effects.append(effect)

func create_explosion_effect(position: Vector3, explosion_type: String, 
                           scale_factor: float = 1.0) -> void:
    var explosion = get_pooled_effect("explosion_" + explosion_type)
    
    explosion.global_position = position
    explosion.scale = Vector3.ONE * scale_factor
    
    # WCS-style explosion sequence
    match explosion_type:
        "ship":
            create_ship_explosion_sequence(explosion, scale_factor)
        "missile":
            create_missile_explosion_effect(explosion, scale_factor)
        "capital_ship":
            create_capital_explosion_sequence(explosion, scale_factor)

func create_ship_explosion_sequence(explosion_node: Node3D, scale: float) -> void:
    # Multi-stage explosion like WCS
    var stages = [
        {"delay": 0.0, "color": Color.ORANGE, "intensity": 2.0},
        {"delay": 0.3, "color": Color.RED, "intensity": 1.5},
        {"delay": 0.6, "color": Color.DARK_RED, "intensity": 1.0},
        {"delay": 1.0, "color": Color.BLACK, "intensity": 0.0}
    ]
    
    for stage in stages:
        var timer = get_tree().create_timer(stage.delay)
        timer.timeout.connect(func(): _update_explosion_stage(explosion_node, stage))

func create_laser_beam_effect(start_pos: Vector3, end_pos: Vector3, 
                             beam_color: Color, beam_width: float) -> void:
    var beam = MeshInstance3D.new()
    var beam_mesh = QuadMesh.new()
    
    # Create beam geometry
    var beam_length = start_pos.distance_to(end_pos)
    beam_mesh.size = Vector2(beam_width, beam_length)
    beam.mesh = beam_mesh
    
    # Apply laser shader
    var beam_material = ShaderMaterial.new()
    beam_material.shader = shader_manager.get_shader("laser_beam")
    beam_material.set_shader_parameter("beam_color", beam_color)
    beam_material.set_shader_parameter("beam_width", beam_width)
    beam_material.set_shader_parameter("beam_intensity", 3.0)
    
    beam.material_override = beam_material
    
    # Position and orient beam
    beam.global_position = (start_pos + end_pos) * 0.5
    beam.look_at(end_pos, Vector3.UP)
    
    add_child(beam)
    
    # Animate beam lifetime
    var tween = create_tween()
    tween.tween_property(beam_material, "shader_parameter/beam_intensity", 0.0, 0.1)
    tween.tween_callback(func(): beam.queue_free())

func create_engine_trail_effect(ship: Node3D, engine_positions: Array[Vector3]) -> void:
    for pos in engine_positions:
        var trail = GPUParticles3D.new()
        
        # Configure particle system for engine trail
        var material = ParticleProcessMaterial.new()
        material.direction = Vector3(0, 0, -1)  # Behind ship
        material.initial_velocity_min = 20.0
        material.initial_velocity_max = 40.0
        material.scale_min = 0.5
        material.scale_max = 1.5
        material.color = Color.CYAN
        
        trail.process_material = material
        trail.amount = 100
        trail.lifetime = 2.0
        trail.emitting = true
        
        trail.position = pos
        ship.add_child(trail)

func create_shield_hit_effect(impact_point: Vector3, shield_node: Node3D) -> void:
    # Create shield impact ripple effect
    var ripple = MeshInstance3D.new()
    var ripple_mesh = SphereMesh.new()
    ripple_mesh.radius = 0.1
    ripple_mesh.height = 0.2
    ripple.mesh = ripple_mesh
    
    # Apply shield impact shader
    var shield_material = ShaderMaterial.new()
    shield_material.shader = shader_manager.get_shader("energy_shield")
    shield_material.set_shader_parameter("impact_position", impact_point)
    shield_material.set_shader_parameter("impact_intensity", 3.0)
    shield_material.set_shader_parameter("impact_radius", 0.5)
    
    shield_node.material_override = shield_material
    
    # Animate impact effect
    var tween = create_tween()
    tween.parallel().tween_property(shield_material, "shader_parameter/impact_intensity", 0.0, 1.0)
    tween.parallel().tween_property(shield_material, "shader_parameter/impact_radius", 2.0, 1.0)
```

## Texture Streaming System

### Dynamic Texture Loading

**TextureStreamer**
```gdscript
class_name TextureStreamer
extends Node

## Manages efficient loading and streaming of textures

var texture_cache: Dictionary = {}
var loading_queue: Array[String] = []
var cache_size_limit: int = 512 * 1024 * 1024  # 512 MB
var current_cache_size: int = 0

var texture_quality_settings: Dictionary = {
    RenderingManager.RenderQuality.LOW: 0.5,
    RenderingManager.RenderQuality.MEDIUM: 0.75,
    RenderingManager.RenderQuality.HIGH: 1.0,
    RenderingManager.RenderQuality.ULTRA: 1.0
}

func load_texture(texture_path: String, priority: int = 0) -> Texture2D:
    # Check cache first
    if texture_path in texture_cache:
        return texture_cache[texture_path]
    
    # Add to loading queue if not cached
    if texture_path not in loading_queue:
        loading_queue.append(texture_path)
        loading_queue.sort_custom(func(a, b): return get_texture_priority(a) > get_texture_priority(b))
    
    # Load immediately if high priority
    if priority > 5:
        return load_texture_immediate(texture_path)
    
    # Return placeholder while loading
    return get_placeholder_texture()

func load_texture_immediate(texture_path: String) -> Texture2D:
    var texture = load(texture_path) as Texture2D
    
    if texture:
        # Apply quality scaling
        var quality_scale = texture_quality_settings[RenderingManager.render_quality]
        if quality_scale < 1.0:
            texture = scale_texture(texture, quality_scale)
        
        # Add to cache
        add_to_cache(texture_path, texture)
    
    return texture

func _process(_delta: float) -> void:
    # Process loading queue
    if not loading_queue.is_empty():
        var texture_path = loading_queue.pop_front()
        var texture = load_texture_immediate(texture_path)
        
        if texture:
            # Notify systems that texture is ready
            texture_loaded.emit(texture_path, texture)

func add_to_cache(path: String, texture: Texture2D) -> void:
    var texture_size = estimate_texture_memory_size(texture)
    
    # Check if we need to free cache space
    while current_cache_size + texture_size > cache_size_limit and not texture_cache.is_empty():
        free_oldest_cached_texture()
    
    texture_cache[path] = texture
    current_cache_size += texture_size

func estimate_texture_memory_size(texture: Texture2D) -> int:
    if texture is ImageTexture:
        var image = texture.get_image()
        return image.get_width() * image.get_height() * 4  # Assume RGBA
    
    return 1024 * 1024  # Default estimate
```

## Model Rendering System

### POF Model Integration

**ModelRenderer**
```gdscript
class_name ModelRenderer
extends Node

## Handles rendering of converted WCS models with LOD and culling

var model_cache: Dictionary = {}
var lod_system: LODSystem
var frustum_culler: FrustumCuller

class ModelLOD:
    var distances: Array[float] = [100.0, 500.0, 2000.0]
    var meshes: Array[Mesh] = []
    var materials: Array[Material] = []

func _ready() -> void:
    lod_system = LODSystem.new()
    frustum_culler = FrustumCuller.new()
    add_child(lod_system)
    add_child(frustum_culler)

func load_wcs_model(model_path: String) -> Node3D:
    if model_path in model_cache:
        return model_cache[model_path].duplicate()
    
    # Load converted GLB model
    var scene = load(model_path) as PackedScene
    if not scene:
        return null
    
    var model_instance = scene.instantiate()
    
    # Apply WCS-specific model setup
    setup_wcs_model_properties(model_instance)
    
    # Cache the model
    model_cache[model_path] = scene
    
    return model_instance

func setup_wcs_model_properties(model: Node3D) -> void:
    # Apply WCS-specific rendering properties
    for child in model.get_children():
        if child is MeshInstance3D:
            var mesh_instance = child as MeshInstance3D
            
            # Set up LOD if multiple meshes available
            setup_model_lod(mesh_instance)
            
            # Apply WCS material properties
            apply_wcs_material_properties(mesh_instance)
            
            # Configure shadows and culling
            configure_rendering_properties(mesh_instance)

func setup_model_lod(mesh_instance: MeshInstance3D) -> void:
    # Check if LOD meshes are available
    var lod_meshes = find_lod_meshes(mesh_instance)
    
    if lod_meshes.size() > 1:
        var lod_component = LODComponent.new()
        lod_component.setup_lod_levels(lod_meshes)
        mesh_instance.add_child(lod_component)

func apply_wcs_material_properties(mesh_instance: MeshInstance3D) -> void:
    var material = mesh_instance.get_surface_override_material(0)
    
    if material is StandardMaterial3D:
        var std_material = material as StandardMaterial3D
        
        # WCS-specific material adjustments
        std_material.flags_use_point_size = false
        std_material.flags_transparent = false
        std_material.flags_emission_on_uv2 = false
        
        # Space-appropriate material settings
        std_material.rim_enabled = true
        std_material.rim_tint = 0.5
```

## Performance Monitoring

### Rendering Performance System

**PerformanceMonitor**
```gdscript
class_name PerformanceMonitor
extends Node

## Monitors rendering performance and adjusts quality dynamically

var frame_time_history: Array[float] = []
var draw_call_history: Array[int] = []
var memory_usage_history: Array[int] = []

var performance_targets: Dictionary = {
    "target_frametime": 16.67,  # 60 FPS
    "max_draw_calls": 2000,
    "max_memory_mb": 512
}

var auto_quality_adjustment: bool = true
var quality_adjustment_threshold: float = 5.0  # frames below target

func _ready() -> void:
    # Monitor performance every second
    var timer = Timer.new()
    timer.wait_time = 1.0
    timer.timeout.connect(_update_performance_metrics)
    timer.autostart = true
    add_child(timer)

func _update_performance_metrics() -> void:
    var current_frametime = 1.0 / Engine.get_frames_per_second()
    var current_draw_calls = RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TYPE_VISIBLE, RenderingServer.RENDERING_INFO_DRAW_CALLS_IN_FRAME)
    var current_memory = OS.get_static_memory_usage_by_type() / (1024 * 1024)
    
    # Add to history
    frame_time_history.append(current_frametime)
    draw_call_history.append(current_draw_calls)
    memory_usage_history.append(current_memory)
    
    # Keep only recent history
    if frame_time_history.size() > 60:  # 1 minute of history
        frame_time_history.pop_front()
        draw_call_history.pop_front()
        memory_usage_history.pop_front()
    
    # Check for performance issues
    check_performance_targets()

func check_performance_targets() -> void:
    var avg_frametime = calculate_average(frame_time_history)
    var avg_draw_calls = calculate_average(draw_call_history)
    var avg_memory = calculate_average(memory_usage_history)
    
    # Check frametime target
    if avg_frametime > performance_targets.target_frametime + quality_adjustment_threshold:
        if auto_quality_adjustment:
            request_quality_reduction()
        RenderingManager.performance_warning.emit("frametime", avg_frametime)
    
    # Check draw call target
    if avg_draw_calls > performance_targets.max_draw_calls:
        RenderingManager.performance_warning.emit("draw_calls", avg_draw_calls)
    
    # Check memory target
    if avg_memory > performance_targets.max_memory_mb:
        RenderingManager.performance_warning.emit("memory", avg_memory)

func request_quality_reduction() -> void:
    var current_quality = RenderingManager.render_quality
    
    match current_quality:
        RenderingManager.RenderQuality.ULTRA:
            RenderingManager.set_render_quality(RenderingManager.RenderQuality.HIGH)
        RenderingManager.RenderQuality.HIGH:
            RenderingManager.set_render_quality(RenderingManager.RenderQuality.MEDIUM)
        RenderingManager.RenderQuality.MEDIUM:
            RenderingManager.set_render_quality(RenderingManager.RenderQuality.LOW)
        _:
            # Already at lowest quality, can't reduce further
            pass
```

## Testing Strategy

### Graphics System Tests

**Rendering Pipeline Tests**
```gdscript
func test_material_conversion():
    var wcs_material = WCSMaterial.new()
    wcs_material.name = "test_hull"
    wcs_material.diffuse_texture = "res://textures/test_hull_diffuse.png"
    wcs_material.reflectance = 0.5
    wcs_material.shininess = 64.0
    
    var converted = material_system.convert_wcs_material(wcs_material)
    
    assert(converted != null, "Material conversion should succeed")
    assert(converted.resource_name == "test_hull", "Material name should be preserved")
    assert(converted.metallic > 0.0, "Reflectance should convert to metallic")

func test_shader_compilation():
    var laser_shader = shader_manager.get_shader("laser_beam")
    assert(laser_shader != null, "Laser shader should be available")
    
    var material = ShaderMaterial.new()
    material.shader = laser_shader
    
    # Test shader parameters
    material.set_shader_parameter("beam_color", Color.RED)
    material.set_shader_parameter("beam_intensity", 2.0)
    
    assert(material.get_shader_parameter("beam_color") == Color.RED, "Shader parameters should be set correctly")

func test_performance_monitoring():
    var monitor = PerformanceMonitor.new()
    
    # Simulate performance data
    monitor.frame_time_history = [16.0, 17.0, 18.0, 19.0, 20.0]  # Declining performance
    
    monitor.check_performance_targets()
    
    # Should trigger quality reduction
    assert(RenderingManager.render_quality < RenderingManager.RenderQuality.HIGH, "Quality should be reduced for poor performance")
```

### Visual Validation Tests

**Effect System Tests**
```gdscript
func test_weapon_effects():
    var start_pos = Vector3(0, 0, 0)
    var end_pos = Vector3(10, 0, 0)
    
    effects_manager.create_laser_beam_effect(start_pos, end_pos, Color.RED, 0.1)
    
    # Check that beam was created
    var beam_count = count_children_with_shader(effects_manager, "laser_beam")
    assert(beam_count > 0, "Laser beam effect should be created")

func test_explosion_effects():
    var explosion_pos = Vector3(5, 5, 5)
    
    effects_manager.create_explosion_effect(explosion_pos, "ship", 2.0)
    
    # Check explosion sequence
    await get_tree().create_timer(1.5).timeout
    
    var explosion_stages = count_active_explosions(effects_manager)
    assert(explosion_stages >= 1, "Explosion should have multiple stages")
```

## Implementation Phases

### Phase 1: Core Rendering Systems (2 weeks)
- Material system and WCS material conversion
- Basic shader management and custom shaders
- Texture streaming infrastructure
- Performance monitoring foundation

### Phase 2: Visual Effects (2 weeks)
- Weapon effects (lasers, missiles, impacts)
- Explosion and destruction effects
- Shield and energy effects
- Engine trails and environmental effects

### Phase 3: Advanced Features (2 weeks)
- Advanced lighting system for space environments
- LOD system for models and effects
- Dynamic quality adjustment
- Post-processing pipeline

### Phase 4: Optimization & Polish (1 week)
- Performance optimization and profiling
- Memory usage optimization
- Visual quality validation
- Integration testing with other systems

## Success Criteria

- [ ] Faithful recreation of WCS visual style and effects
- [ ] Maintain 60+ FPS with complex space battles (20+ ships)
- [ ] Efficient texture streaming with < 512MB memory usage
- [ ] All WCS material types properly converted and rendered
- [ ] Complete weapon and explosion effect system
- [ ] Adaptive quality system maintaining target performance
- [ ] Proper space environment lighting and atmosphere
- [ ] LOD system reducing rendering load for distant objects
- [ ] Memory-efficient effect pooling and management
- [ ] Comprehensive visual validation and testing

## Integration Notes

**Dependency on EPIC-003**: Converted models and textures from migration tools
**Dependency on EPIC-002**: Asset management system for resource loading
**Integration with EPIC-009**: Object system for effect attachment and lifecycle
**Integration with EPIC-011**: Ship and combat systems for visual feedback
**Integration with EPIC-012**: HUD system for rendering overlays and interface
**Integration with EPIC-007**: Game state management for quality settings persistence

This architecture provides a comprehensive graphics and rendering system that delivers authentic WCS visuals while leveraging Godot 4's modern rendering capabilities and performance optimization features.