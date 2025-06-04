# Godot System: Object & Physics System - Proposed Dependencies

## Overview
This document details the proposed interactions and dependencies between Godot files for the Object & Physics System, including scene composition, script attachments, signal connections, and integration points with existing systems.

## Core Management Dependencies

### Autoload: `res://autoload/object_manager.gd` (✅ EXISTING - EPIC-001)
**Current Implementation:**
- ✅ **ALREADY REFERENCES**: `res://scripts/core/wcs_object.gd` (WCSObject class)
- ✅ **ALREADY REFERENCES**: `res://scripts/core/wcs_object_data.gd` (WCSObjectData class)
- ✅ **ALREADY IMPLEMENTS**: Object pooling with type-based pools
- ✅ **ALREADY IMPLEMENTS**: Update frequency groups and lifecycle management

**New Enhancements for EPIC-009:**
- `res://scripts/core/objects/foundation/space_object_registry.gd` (Enhanced registry for space objects)
- `res://scripts/core/objects/foundation/space_object_factory.gd` (Factory for space-specific objects)
- `res://scripts/core/objects/optimization/spatial_hash.gd` (SpatialHash for spatial queries)
- Enhanced coordination with existing PhysicsManager autoload

**Signals Emitted:**
- `object_created(object: BaseSpaceObject, object_id: int)`
- `object_destroyed(object: BaseSpaceObject, object_id: int)`
- `spatial_query_ready(query_id: int, results: Array[BaseSpaceObject])`

**Signals Connected To:**
- `PhysicsManager.physics_step_completed` → `_on_physics_step_completed(delta: float)`
- `GameStateManager.game_state_changed` → `_on_game_state_changed(new_state: String)`

### Autoload: `res://autoload/physics_manager.gd` (✅ EXISTING - EPIC-001)
**Current Implementation:**
- ✅ **ALREADY REFERENCES**: `res://scripts/core/wcs_object.gd` (WCSObject class)
- ✅ **ALREADY REFERENCES**: `res://scripts/core/custom_physics_body.gd` (CustomPhysicsBody class)
- ✅ **ALREADY IMPLEMENTS**: Fixed timestep physics at 60Hz
- ✅ **ALREADY IMPLEMENTS**: Collision detection and response
- ✅ **ALREADY IMPLEMENTS**: Custom physics body registration and management

**New Enhancements for EPIC-009:**
- `res://scripts/core/objects/physics/physics_integration.gd` (Enhanced Godot physics coordination)
- `res://scripts/core/objects/physics/force_application.gd` (WCS-style physics behaviors)
- `res://scripts/core/objects/types/physics_profiles.gd` (PhysicsProfile resource definitions)

**Signals Emitted:**
- `physics_step_completed(delta: float)`
- `collision_detected(object_a: BaseSpaceObject, object_b: BaseSpaceObject, collision_info: Dictionary)`

**Signals Connected To:**
- `ObjectManager.object_created` → `_on_object_created(object: BaseSpaceObject)`
- `ObjectManager.object_destroyed` → `_on_object_destroyed(object: BaseSpaceObject)`

## Core Object Framework Dependencies

### Scene: `res://scenes/core/WCSObject.tscn`
**Instances/Uses:**
- Root Node: `RigidBody3D` with `res://scripts/core/wcs_object.gd` attached
- Child Nodes:
  - `MeshInstance3D` (for 3D model rendering)
  - `CollisionShape3D` (for collision detection)
  - `AudioSource3D` (for object audio effects)

**Signals Connected (Emitted by this scene/scripts):**
- `object_initialized` (from `wcs_object.gd`) → `ObjectManager.on_object_ready`
- `collision_detected` (from `wcs_object.gd`) → `PhysicsManager.on_collision_detected`
- `state_changed` (from `wcs_object.gd`) → `SexpManager.on_object_state_changed`

**Signals Connected (Listened to by this scene/scripts):**
- `ObjectManager.spatial_query_ready` → `wcs_object.gd._on_spatial_query_result`
- `PhysicsManager.physics_step_completed` → `wcs_object.gd._on_physics_step`

### Scene: `res://scenes/core/PhysicsBody.tscn`
**Instances/Uses:**
- Root Node: `RigidBody3D` with `res://scripts/core/custom_physics_body.gd` attached
- `res://scripts/core/objects/physics/rigid_body_physics.gd` (component script)

**Signals Connected (Emitted):**
- `physics_state_changed` (from `custom_physics_body.gd`) → `PhysicsManager.on_physics_state_change`
- `force_applied` (from `custom_physics_body.gd`) → `DebugManager.on_force_visualization`

**Signals Connected (Listened to):**
- `PhysicsManager.force_application_request` → `custom_physics_body.gd._on_force_request`

## Object Type Dependencies

### Script: `res://scripts/object/asteroid.gd` (✅ PARTIALLY EXISTING)
**Current Implementation:**
- ✅ **ALREADY EXTENDS**: `RigidBody3D` (will be enhanced to extend BaseSpaceObject)
- ✅ **ALREADY IMPLEMENTS**: Basic collision detection with `body_entered` signal
- ✅ **ALREADY IMPLEMENTS**: Hull strength and destruction logic
- ✅ **ALREADY IMPLEMENTS**: Hit damage calculation

**New Enhancements for EPIC-009:**
- Upgrade to extend `BaseSpaceObject` instead of direct RigidBody3D
- `res://scripts/core/objects/types/environmental_types.gd` (AsteroidType definitions)
- `res://scripts/core/objects/types/debris_types.gd` (for destruction debris)
- Integration with `res://addons/wcs_asset_core/loaders/asset_loader.gd` (for asteroid configuration)

**Signals Emitted:**
- `asteroid_destroyed(debris_pieces: Array[BaseSpaceObject])`
- `collision_damage_calculated(damage: float)`

**Signals Connected To:**
- `parent.collision_detected` → `_on_collision_with_other(other: BaseSpaceObject)`

### Script: `res://scripts/object/debris.gd`
**References/Uses:**
- `BaseSpaceObject` (extends from `res://scripts/core/wcs_object.gd`)
- `res://scripts/core/objects/types/debris_types.gd` (DebrisType definitions)
- `res://scripts/core/objects/optimization/lod_manager.gd` (LOD system integration)

**Signals Emitted:**
- `debris_expired()`
- `debris_state_changed(new_state: String)`

### Script: `res://scripts/object/weapon_base.gd`
**References/Uses:**
- `BaseSpaceObject` (extends from `res://scripts/core/wcs_object.gd`)
- `res://scripts/core/objects/types/weapon_types.gd` (WeaponType definitions)
- `EPIC-002.AssetManager.get_weapon_data()` (for weapon configuration)
- `EPIC-008.GraphicsManager.create_weapon_trail()` (for visual effects)

**Signals Emitted:**
- `weapon_impact(target: BaseSpaceObject, damage: float)`
- `weapon_expired()`

**Signals Connected To:**
- `parent.collision_detected` → `_on_weapon_collision(other: BaseSpaceObject)`

## Collision System Dependencies

### Script: `res://systems/objects/collision/collision_detector.gd`
**References/Uses:**
- `res://systems/objects/collision/collision_shapes.gd` (CollisionShape management)
- `res://systems/objects/collision/spatial_partitioning.gd` (SpatialPartitioning for optimization)
- `res://systems/objects/types/collision_categories.gd` (collision layer definitions)

**Signals Emitted:**
- `collision_pair_detected(object_a: BaseSpaceObject, object_b: BaseSpaceObject)`
- `collision_resolved(collision_id: int, resolution_data: Dictionary)`

**Signals Connected To:**
- `PhysicsManager.physics_step_completed` → `_on_physics_step_collision_check(delta: float)`

### Script: `res://systems/objects/collision/collision_response.gd`
**References/Uses:**
- `res://systems/objects/collision/damage_calculator.gd` (DamageCalculator for impact effects)
- `res://scripts/core/objects/physics/force_application.gd` (ForceApplication for collision response)
- `EPIC-008.GraphicsManager.create_collision_effect()` (for visual impact effects)

**Signals Emitted:**
- `collision_damage_applied(target: BaseSpaceObject, damage: float)`
- `collision_effect_triggered(position: Vector3, effect_type: String)`

**Signals Connected To:**
- `CollisionDetector.collision_pair_detected` → `_on_collision_pair(object_a, object_b)`

## Performance Optimization Dependencies

### Script: `res://systems/objects/optimization/lod_manager.gd`
**References/Uses:**
- `res://systems/objects/optimization/distance_culler.gd` (DistanceCuller for visibility management)
- `res://systems/objects/types/update_frequencies.gd` (UpdateFrequency definitions)
- `EPIC-008.GraphicsManager.set_lod_level()` (for rendering LOD integration)

**Signals Emitted:**
- `lod_level_changed(object: BaseSpaceObject, new_level: int)`
- `object_culled(object: BaseSpaceObject)`
- `object_unculled(object: BaseSpaceObject)`

**Signals Connected To:**
- `ObjectManager.object_created` → `_on_new_object_registered(object: BaseSpaceObject)`
- `CameraManager.camera_moved` → `_on_camera_position_changed(position: Vector3)`

### Script: `res://systems/objects/optimization/spatial_hash.gd`
**References/Uses:**
- `res://systems/objects/queries/spatial_query.gd` (SpatialQuery for search operations)
- No direct signal dependencies (used through direct method calls)

**Methods Called By:**
- `ObjectManager.get_objects_in_radius()` → `get_objects_in_area(center: Vector3, radius: float)`
- `CollisionDetector.get_potential_collisions()` → `get_nearby_objects(object: BaseSpaceObject)`

## Query System Dependencies

### Script: `res://systems/objects/queries/spatial_query.gd`
**References/Uses:**
- `res://systems/objects/queries/type_filter.gd` (TypeFilter for object filtering)
- `res://systems/objects/queries/query_cache.gd` (QueryCache for performance)

**Signals Emitted:**
- `query_completed(query_id: int, results: Array[BaseSpaceObject])`
- `query_failed(query_id: int, error_message: String)`

**Signals Connected To:**
- `ObjectManager.object_created` → `_on_object_added_to_world(object: BaseSpaceObject)`
- `ObjectManager.object_destroyed` → `_on_object_removed_from_world(object: BaseSpaceObject)`

### Script: `res://systems/objects/queries/proximity_detector.gd`
**References/Uses:**
- `res://systems/objects/queries/spatial_hash.gd` (SpatialHash for efficient proximity checks)
- `res://systems/objects/events/proximity_events.gd` (ProximityEvent definitions)

**Signals Emitted:**
- `object_entered_proximity(watcher: BaseSpaceObject, target: BaseSpaceObject)`
- `object_exited_proximity(watcher: BaseSpaceObject, target: BaseSpaceObject)`

**Signals Connected To:**
- `ObjectManager.object_created` → `_on_object_registered(object: BaseSpaceObject)`
- `PhysicsManager.physics_step_completed` → `_on_physics_step_proximity_check(delta: float)`

## Event System Dependencies

### Script: `res://systems/objects/events/object_events.gd`
**References/Uses:**
- `res://systems/objects/events/event_dispatcher.gd` (EventDispatcher for event routing)
- `EPIC-004.SexpManager.trigger_event()` (for SEXP system integration)

**Signals Emitted:**
- `object_lifecycle_event(event_type: String, object: BaseSpaceObject)`
- `object_property_changed(object: BaseSpaceObject, property_name: String, old_value: Variant, new_value: Variant)`

**Signals Connected To:**
- `ObjectManager.object_created` → `_on_object_created_event(object: BaseSpaceObject)`
- `ObjectManager.object_destroyed` → `_on_object_destroyed_event(object: BaseSpaceObject)`

### Script: `res://systems/objects/events/collision_events.gd`
**References/Uses:**
- `res://systems/objects/collision/collision_response.gd` (CollisionResponse for event data)
- `EPIC-004.SexpManager.trigger_collision_event()` (for mission scripting)

**Signals Emitted:**
- `collision_event_processed(event_data: Dictionary)`

**Signals Connected To:**
- `CollisionResponse.collision_damage_applied` → `_on_collision_damage_event(target, damage)`
- `CollisionResponse.collision_effect_triggered` → `_on_collision_effect_event(position, effect_type)`

## Integration Bridge Dependencies

### Script: `res://systems/objects/integration/rendering_bridge.gd`
**References/Uses:**
- `EPIC-008.GraphicsManager` (for rendering system integration)
- `EPIC-008.MaterialManager` (for material and texture management)
- `res://systems/objects/optimization/lod_manager.gd` (LODManager for rendering optimization)

**Methods Provided:**
- `update_object_rendering(object: BaseSpaceObject, render_data: Dictionary)`
- `set_object_visibility(object: BaseSpaceObject, visible: bool)`
- `apply_material_to_object(object: BaseSpaceObject, material: Material)`

**Signals Connected To:**
- `LODManager.lod_level_changed` → `_on_lod_change(object, new_level)`

### Script: `res://systems/objects/integration/ai_bridge.gd`
**References/Uses:**
- `EPIC-010.AIManager` (when implemented - AI system integration)
- `res://systems/objects/queries/spatial_query.gd` (SpatialQuery for AI object awareness)

**Methods Provided:**
- `get_ai_targets(ai_object: BaseSpaceObject) -> Array[BaseSpaceObject]`
- `register_ai_object(object: BaseSpaceObject, ai_data: Dictionary)`

**Signals Emitted:**
- `ai_target_acquired(ai_object: BaseSpaceObject, target: BaseSpaceObject)`
- `ai_target_lost(ai_object: BaseSpaceObject, target: BaseSpaceObject)`

### Script: `res://systems/objects/integration/sexp_bridge.gd`
**References/Uses:**
- `EPIC-004.SexpManager` (for SEXP system integration)
- `res://systems/objects/queries/spatial_query.gd` (SpatialQuery for SEXP object queries)

**Methods Provided (for SEXP system):**
- `sexp_get_object_position(object_id: int) -> Vector3`
- `sexp_get_object_health(object_id: int) -> float`
- `sexp_destroy_object(object_id: int) -> bool`
- `sexp_get_objects_in_area(center: Vector3, radius: float) -> Array[int]`

**Signals Connected To:**
- `ObjectManager.object_created` → `_on_object_created_for_sexp(object: BaseSpaceObject)`
- `ObjectManager.object_destroyed` → `_on_object_destroyed_for_sexp(object: BaseSpaceObject)`

## Testing Dependencies

### Script: `res://tests/objects/test_object_lifecycle.gd`
**References/Uses:**
- `res://scripts/core/wcs_object.gd` (BaseSpaceObject for testing)
- `res://autoload/object_manager.gd` (ObjectManager for lifecycle testing)
- GdUnit test framework

**Test Methods:**
- `test_object_creation_and_registration()`
- `test_object_destruction_and_cleanup()`
- `test_object_id_assignment_uniqueness()`

### Script: `res://tests/objects/test_collision_detection.gd`
**References/Uses:**
- `res://systems/objects/collision/collision_detector.gd` (CollisionDetector testing)
- `res://scripts/object/weapon_base.gd` (WeaponBase for collision testing)
- Mock objects for controlled testing scenarios

**Test Methods:**
- `test_collision_detection_accuracy()`
- `test_collision_response_calculation()`
- `test_collision_filtering_by_layer()`

## Configuration Dependencies

### Resource: `res://systems/objects/config/object_config.tres`
**Type**: `ObjectConfiguration` (extends Resource)
**References:**
- `res://systems/objects/types/physics_profiles.gd` (PhysicsProfile resources)
- `res://systems/objects/types/collision_categories.gd` (collision layer definitions)

**Used By:**
- `ObjectManager._ready()` (for system initialization)
- `ObjectFactory.create_object()` (for object creation parameters)

### Resource: `res://systems/objects/config/physics_config.tres`
**Type**: `PhysicsConfiguration` (extends Resource)
**Used By:**
- `PhysicsManager._ready()` (for physics system setup)
- `CustomPhysicsBody._physics_process()` (for physics behavior tuning)

## External Epic Dependencies

### EPIC-001 Dependencies (✅ EXISTING FOUNDATION)
- ✅ **IMPLEMENTED**: `ObjectManager` autoload (target/autoload/object_manager.gd)
- ✅ **IMPLEMENTED**: `PhysicsManager` autoload (target/autoload/physics_manager.gd)
- ✅ **IMPLEMENTED**: `WCSObject` base class (target/scripts/core/wcs_object.gd)
- ✅ **IMPLEMENTED**: `CustomPhysicsBody` class (target/scripts/core/custom_physics_body.gd)
- ✅ **IMPLEMENTED**: `ConfigurationManager` autoload (target/autoload/configuration_manager.gd)

### EPIC-002 Dependencies (✅ EXISTING ASSET SYSTEM)
- ✅ **IMPLEMENTED**: `AssetLoader` (addons/wcs_asset_core/loaders/asset_loader.gd)
- ✅ **IMPLEMENTED**: `RegistryManager` (addons/wcs_asset_core/loaders/registry_manager.gd)
- ✅ **IMPLEMENTED**: `MaterialData` resources (addons/wcs_asset_core/structures/material_data.gd)
- ✅ **IMPLEMENTED**: `ShipData` resources (addons/wcs_asset_core/structures/ship_data.gd)
- ✅ **IMPLEMENTED**: `WeaponData` resources (addons/wcs_asset_core/structures/weapon_data.gd)
- ✅ **IMPLEMENTED**: `ArmorData` resources (addons/wcs_asset_core/structures/armor_data.gd)

### EPIC-004 Dependencies
- `SexpManager.register_object_query_function()` (for SEXP object queries)
- `SexpManager.trigger_event()` (for mission event triggering)

### EPIC-008 Dependencies
- `GraphicsManager` autoload (for rendering integration)
- `MaterialManager` (for material management)
- Shader resources (for visual effects)
- Particle system integration (for object effects)

## Signal Flow Summary

**Primary Signal Chains:**
1. **Object Lifecycle**: `ObjectManager` → `PhysicsManager` → `GraphicsManager` → `SexpManager`
2. **Collision Processing**: `CollisionDetector` → `CollisionResponse` → `ObjectManager` → `SexpManager`
3. **Performance Optimization**: `LODManager` → `GraphicsManager` + `PhysicsManager`
4. **Query System**: `SpatialQuery` → `ObjectManager` → requesting systems

**Critical Signal Dependencies:**
- All object-related signals must route through `ObjectManager` for centralized coordination
- Physics signals coordinate between `PhysicsManager` and individual object physics components
- Integration bridges ensure proper communication with external systems (EPIC-004, EPIC-008)
- Event system provides SEXP integration and mission scripting support

This dependency structure ensures clear separation of concerns while maintaining efficient communication between all components of the Object & Physics System.