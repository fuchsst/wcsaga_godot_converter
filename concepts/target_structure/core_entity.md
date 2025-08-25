# Core Entity Module (Godot Implementation)

## Purpose
The Core Entity Module forms the foundational layer of the Godot implementation, providing a flexible and extensible base for all game objects. Unlike the original C++ implementation which used a custom object system, this module leverages Godot's node-based architecture to create a robust entity-component system following feature-based organization principles with the hybrid model approach.

## Components
- **Entity Base Class**: Inheriting from Godot's Node3D for 3D spatial functionality
- **Entity Manager**: Singleton for entity lifecycle management and global operations
- **Component System**: Modular components that can be attached to entities
- **Resource System Integration**: Data-driven entity definitions using Godot resources
- **Pooling System**: Efficient entity creation/destruction through object pooling

## Dependencies
- None (this is the foundational module)

## Godot Implementation Details

### Native GDScript Classes
```gdscript
# Base entity class that all game objects inherit from
class Entity extends Node3D:
    # Unique identifier for this entity instance
    var entityId: int
    
    # Entity type for classification and filtering
    var entityType: String
    
    # Reference to the entity class/template that defines base properties
    var entityClass: EntityClass
    
    # Active state - determines if entity should be processed
    var isActive: bool = true
    
    # Pooling state - determines if entity is available for reuse
    var isInPool: bool = false
    
    # Event signals for entity lifecycle
    signal entity_created(entity)
    signal entity_destroyed(entity_id)
    signal entity_activated(entity)
    signal entity_deactivated(entity)
    
    func _ready():
        # Called when entity enters the scene tree
        emit_signal("entity_created", self)
        
    func _process(delta):
        # Called every frame if entity is active
        if isActive:
            update_entity(delta)
            
    func update_entity(delta):
        # Override in subclasses for entity-specific behavior
        pass
        
    func activate():
        # Activate the entity
        isActive = true
        emit_signal("entity_activated", self)
        
    func deactivate():
        # Deactivate the entity
        isActive = false
        emit_signal("entity_deactivated", self)
        
    func destroy():
        # Prepare entity for destruction or pooling
        emit_signal("entity_destroyed", entityId)
        if isInPool:
            # Return to pool instead of freeing
            EntityManager.return_to_pool(self)
        else:
            # Free the entity
            queue_free()

# Entity manager singleton for global entity operations
class EntityManager:
    # Singleton instance
    static var instance: EntityManager
    
    # Entity registry - maps entity IDs to entity instances
    var entities: Dictionary = {}
    
    # Entity pools for different entity types
    var entity_pools: Dictionary = {}
    
    # Next available entity ID
    var nextEntityId: int = 1
    
    func _ready():
        # Initialize singleton
        instance = self
        
    func create_entity(entity_class: EntityClass, position: Vector3 = Vector3.ZERO) -> Entity:
        # Create or retrieve entity from pool
        var entity: Entity
        
        if entity_pools.has(entity_class.name) and not entity_pools[entity_class.name].is_empty():
            # Retrieve from pool
            entity = entity_pools[entity_class.name].pop_back()
            entity.isInPool = false
        else:
            # Create new entity
            entity = load(entity_class.scene_path).instantiate()
            
        # Initialize entity
        entity.entityId = nextEntityId
        nextEntityId += 1
        entity.entityClass = entity_class
        entity.entityType = entity_class.entityType
        entity.global_position = position
        
        # Register entity
        entities[entity.entityId] = entity
        
        # Add to scene tree
        get_tree().root.add_child(entity)
        
        return entity
        
    func destroy_entity(entity_id: int):
        # Destroy entity by ID
        if entities.has(entity_id):
            var entity = entities[entity_id]
            entity.destroy()
            entities.erase(entity_id)
            
    func get_entity(entity_id: int) -> Entity:
        # Retrieve entity by ID
        return entities.get(entity_id, null)
        
    func get_entities_by_type(entity_type: String) -> Array:
        # Retrieve all entities of a specific type
        var result = []
        for entity in entities.values():
            if entity.entityType == entity_type:
                result.append(entity)
        return result
        
    func return_to_pool(entity: Entity):
        # Return entity to pool for reuse
        entity.hide()  # Hide entity visually
        entity.set_process(false)  # Stop processing
        
        var pool_key = entity.entityClass.name
        if not entity_pools.has(pool_key):
            entity_pools[pool_key] = []
            
        entity_pools[pool_key].append(entity)
        
    func update_entities(delta):
        # Update all active entities
        for entity in entities.values():
            if entity.isActive:
                entity.update_entity(delta)

# Base entity class template defining shared properties
class EntityClass extends Resource:
    # Name of the entity class
    @export var name: String
    
    # Type classification for the entity
    @export var entityType: String
    
    # Path to the scene file that represents this entity
    @export var scene_path: String
    
    # Maximum number of instances to keep in pool
    @export var max_pool_size: int = 50
    
    # Health properties
    @export var max_health: float = 100.0
    @export var max_shield: float = 50.0
    
    # Physics properties
    @export var mass: float = 1.0
    @export var max_velocity: Vector3 = Vector3(100, 100, 100)
    
    # Visual properties
    @export var model_path: String = ""
    @export var icon_path: String = ""
    
    func _init():
        resource_name = name
```

### TRES Resources
```ini
[gd_resource type="Resource" load_steps=2 format=2]

[resource]
resource_name = "Generic_Entity_Class"
name = "GenericEntity"
entity_type = "GENERIC"
scene_path = "res://features/templates/generic_entity.tscn"
max_pool_size = 25
max_health = 100.0
max_shield = 0.0
mass = 1.0
max_velocity = Vector3(100, 100, 100)
model_path = "res://features/templates/generic_entity.glb"
icon_path = "res://features/templates/generic_entity_icon.png"
```

### TSCN Scenes
```ini
[gd_scene load_steps=3 format=2]

[ext_resource path="res://scripts/entities/entity.gd" type="Script" id=1]
[ext_resource path="res://features/templates/generic_entity.tres" type="Resource" id=2]

[node name="GenericEntity" type="Node3D"]
script = ExtResource(1)
entity_class = ExtResource(2)

[node name="Model" type="Node3D" parent="."]
# Placeholder for 3D model
```

### Implementation Notes
The Core Entity Module in Godot leverages several key features following feature-based organization with the hybrid model approach:

1. **Node3D Inheritance**: All entities inherit from Node3D, providing built-in 3D transformation capabilities
2. **Singleton Pattern**: EntityManager uses Godot's singleton/autoload system for global access, located in `/autoload/` as `entity_manager.gd`
3. **Resource System**: EntityClass definitions use Godot's resource system for data-driven design, stored as .tres files in feature-specific directories following the self-contained feature organization principle
4. **Scene System**: Entities are implemented as Godot scenes organized by feature in `/features/templates/` for generic templates, with each feature having its own self-contained directory
5. **Signal System**: Lifecycle events use Godot's built-in signal system for decoupled communication
6. **Object Pooling**: Efficient memory management through entity pooling
7. **Component Architecture**: Components can be added as child nodes or scripts for modular functionality

This approach replaces the C++ linked list management with Godot's scene tree and the custom object system with Godot's node-based architecture, while maintaining the same core functionality of entity creation, management, and destruction. The implementation follows Godot's best practices for feature-based organization using the hybrid model where:

- Truly global assets are organized in `/assets/` (following the "Global Litmus Test": "If I delete three random features, is this asset still needed?")
- Feature-specific assets are co-located within `/features/` directories in self-contained modules
- Reusable base scripts are located in `/scripts/entities/` as abstract components
- Singleton managers are located in `/autoload/` for global access
- Generic templates are stored in `/features/templates/` for reuse across different entity types

Each feature folder treats each feature as a self-contained module or component, aligning perfectly with Godot's design philosophy of creating self-contained scenes that encapsulate their own logic and resources. This modularity enhances team collaboration and simplifies long-term maintenance by ensuring all files related to a single feature are grouped together in a single, predictable place.