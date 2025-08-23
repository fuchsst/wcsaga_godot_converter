# Core Entity Module

## Purpose
The Core Entity Module represents the fundamental building blocks of the game world. In the original C++ code, this was implemented through the `object` system, which provided a common interface for all game entities. This module defines the basic entity-component structure that all other gameplay systems build upon.

## Components
- **Object System** (`object/`): Base entity management framework
- **Math Library** (`math/`): Vector and matrix mathematics for spatial calculations
- **Physics Properties** (`physics.h`): Movement and physical properties for entities

## Dependencies
- None (this is the foundational module)

## C++ Components
- `object.h`: Base structure for all game entities
- `obj_create()`, `obj_delete()`: Entity lifecycle management
- `obj_move_all()`, `obj_render_all()`: Frame update functions
- `vec3d`, `matrix`: Mathematical structures for positioning
- `physics_info`: Physics properties for objects

## Godot Equivalent Mapping

### Native GDScript Classes
```gdscript
# Base entity class that all game objects inherit from
class Entity extends Node3D:
    var entity_id: int
    var entityType: String
    var physicsProperties: PhysicsProperties
    var isActive: bool = true
    
    func _ready():
        pass
        
    func _process(delta):
        pass

# Physics properties component
class PhysicsProperties:
    var mass: float
    var velocity: Vector3
    var acceleration: Vector3
    var rotation: Vector3
    var angular_velocity: Vector3
```

### TRES Resources
```ini
[gd_resource type="Resource" load_steps=3 format=2]

[ext_resource path="res://resources/physics_properties.tres" type="Resource" id=1]

[resource]
mass = 1.0
drag_coefficient = 0.1
max_velocity = Vector3(100, 100, 100)
```

### TSCN Scenes
```ini
[gd_scene load_steps=3 format=2]

[ext_resource path="res://scripts/entity.gd" type="Script" id=1]
[ext_resource path="res://resources/physics_properties.tres" type="Resource" id=2]

[node name="Entity" type="Node3D"]
script = ExtResource(1)
physics_properties = ExtResource(2)
```

### Implementation Notes
In Godot, entities are represented as Node3D instances with attached scripts and resources. The component-based approach is achieved through:
1. Inheritance for shared behavior
2. Script attachments for specific functionality
3. Resource files for data-driven properties
4. Scene files for complete entity composition

This replaces the C++ linked list management with Godot's scene tree, and the object pooling with Godot's node management.