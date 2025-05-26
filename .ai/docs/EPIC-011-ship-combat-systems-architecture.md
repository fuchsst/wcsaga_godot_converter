# EPIC-011: Ship & Combat Systems Architecture

## Architecture Overview

The Ship & Combat Systems form the gameplay core of WCS-Godot, implementing authentic space combat mechanics through modular ship systems, sophisticated weapon mechanics, and integrated damage modeling that preserves the original WCS combat feel while leveraging Godot's capabilities.

## System Goals

- **Authenticity**: Faithful recreation of WCS ship handling and combat mechanics
- **Performance**: Smooth 60+ FPS combat with multiple ships and weapons
- **Modularity**: Component-based ship systems for easy customization
- **Depth**: Complex subsystem interactions and damage modeling
- **Balance**: Maintain WCS weapon balance and ship characteristics

## Core Architecture

### Ship Management Hierarchy

```
ShipManager (AutoLoad Singleton)
├── ShipRegistry (Resource)
├── WeaponSystem (Node)
├── DamageSystem (Node)
├── SubsystemManager (Node)
└── CombatEffectsManager (Node)
```

### Ship Foundation

**BaseShip Class**
```gdscript
class_name BaseShip
extends BaseSpaceObject

## Foundation for all ship types in WCS-Godot
## Integrates flight control, weapons, and damage systems

signal hull_damage_taken(damage: float, remaining_hull: float)
signal shield_hit(damage: float, shield_quadrant: int)
signal subsystem_damaged(subsystem_name: String, damage_percent: float)
signal weapon_fired(weapon_name: String, projectile_count: int)
signal ship_destroyed(destruction_cause: String)

@export var ship_class: ShipClass
@export var max_hull_strength: float = 100.0
@export var max_shield_strength: float = 100.0
@export var ship_template: ShipTemplate

var current_hull: float
var shield_quadrants: Array[float] = [100.0, 100.0, 100.0, 100.0]  # Front, Right, Aft, Left
var subsystems: Dictionary = {}
var weapon_banks: Array[WeaponBank] = []
var is_player_ship: bool = false
var pilot_name: String = ""
```

### Ship Templates and Classes

**ShipClass Resource**
```gdscript
class_name ShipClass
extends Resource

## Defines ship characteristics and capabilities

@export var class_name: String
@export var display_name: String
@export var ship_type: ShipType
@export var mass: float = 100.0
@export var max_velocity: float = 100.0
@export var max_afterburner_velocity: float = 150.0
@export var acceleration: float = 50.0
@export var maneuverability: Vector3 = Vector3(1.0, 1.0, 1.0)  # Pitch, Yaw, Roll
@export var armor_type: ArmorType
@export var shield_type: ShieldType
@export var subsystem_layout: Array[SubsystemDefinition] = []
@export var weapon_hardpoints: Array[WeaponHardpoint] = []
@export var cargo_capacity: float = 0.0
@export var fuel_capacity: float = 100.0

enum ShipType {
    FIGHTER,
    BOMBER,
    INTERCEPTOR,
    ASSAULT,
    STEALTH,
    TRANSPORT,
    CORVETTE,
    CRUISER,
    BATTLESHIP,
    CARRIER,
    SUPPORT,
    CARGO
}
```

**ShipTemplate Resource**
```gdscript
class_name ShipTemplate
extends Resource

## Complete ship configuration for spawning

@export var ship_class: ShipClass
@export var loadout: ShipLoadout
@export var ai_personality: AIPersonality
@export var squadron_assignment: String = ""
@export var mission_role: MissionRole
@export var initial_orders: String = ""

class ShipLoadout:
    var primary_weapons: Array[WeaponDefinition] = []
    var secondary_weapons: Array[WeaponDefinition] = []
    var countermeasures: Array[CountermeasureDefinition] = []
    var ship_upgrades: Array[UpgradeDefinition] = []
```

## Weapon Systems Architecture

### Weapon Management

**WeaponBank System**
```gdscript
class_name WeaponBank
extends Node3D

## Manages a group of weapons that fire together

signal weapons_fired(bank_index: int, projectile_count: int)
signal weapons_depleted(bank_index: int)
signal weapon_malfunction(weapon_index: int)

@export var bank_type: WeaponBankType
@export var weapons: Array[Weapon] = []
@export var firing_pattern: FiringPattern
@export var convergence_distance: float = 500.0
@export var auto_target: bool = true

enum WeaponBankType {
    PRIMARY,
    SECONDARY,
    TERTIARY,
    TURRET,
    DEFENSIVE
}

enum FiringPattern {
    SIMULTANEOUS,   # All weapons fire at once
    SEQUENTIAL,     # Weapons fire in sequence
    ALTERNATING,    # Alternate between weapons
    LINKED          # Linked fire groups
}

func fire_weapons(target: Vector3 = Vector3.ZERO) -> Array[Projectile]:
    var projectiles: Array[Projectile] = []
    
    match firing_pattern:
        FiringPattern.SIMULTANEOUS:
            for weapon in weapons:
                if weapon.can_fire():
                    projectiles.append(weapon.fire(target))
        FiringPattern.SEQUENTIAL:
            var weapon_to_fire = get_next_sequential_weapon()
            if weapon_to_fire and weapon_to_fire.can_fire():
                projectiles.append(weapon_to_fire.fire(target))
    
    if projectiles.size() > 0:
        weapons_fired.emit(get_bank_index(), projectiles.size())
    
    return projectiles
```

### Individual Weapon Implementation

**Base Weapon Class**
```gdscript
class_name Weapon
extends Node3D

## Individual weapon implementation with WCS-authentic behavior

signal weapon_fired(projectile: Projectile)
signal weapon_overheated()
signal ammo_depleted()

@export var weapon_definition: WeaponDefinition
@export var muzzle_point: Node3D
@export var weapon_model: Node3D

var current_ammo: int
var heat_level: float = 0.0
var last_fire_time: float = 0.0
var is_overheated: bool = false
var target_lock: Node3D

func can_fire() -> bool:
    var current_time = Time.get_time_dict_from_system()
    var time_since_last_fire = current_time - last_fire_time
    
    return (not is_overheated and 
            current_ammo > 0 and 
            time_since_last_fire >= weapon_definition.fire_rate)

func fire(target_position: Vector3) -> Projectile:
    if not can_fire():
        return null
    
    # Create projectile
    var projectile = create_projectile(target_position)
    
    # Update weapon state
    current_ammo -= 1
    heat_level += weapon_definition.heat_generation
    last_fire_time = Time.get_time_dict_from_system()
    
    # Check overheating
    if heat_level >= weapon_definition.overheat_threshold:
        is_overheated = true
        weapon_overheated.emit()
    
    # Visual and audio effects
    play_firing_effects()
    
    weapon_fired.emit(projectile)
    return projectile
```

### Projectile System

**Projectile Base Class**
```gdscript
class_name Projectile
extends BaseSpaceObject

## Base class for all weapon projectiles

signal projectile_hit(target: Node3D, hit_point: Vector3)
signal projectile_expired()

@export var weapon_definition: WeaponDefinition
@export var damage_amount: float
@export var projectile_speed: float
@export var lifetime: float = 10.0
@export var tracking_capability: float = 0.0  # 0 = dumb, 1 = perfect tracking

var target: Node3D
var creation_time: float
var owner_ship: BaseShip
var damage_type: DamageType

func _ready() -> void:
    creation_time = Time.get_time_dict_from_system()
    set_linear_velocity(transform.basis.z * projectile_speed)
    
    # Set up collision detection
    body_entered.connect(_on_collision_detected)

func _physics_process(delta: float) -> void:
    # Check lifetime
    if Time.get_time_dict_from_system() - creation_time > lifetime:
        expire_projectile()
        return
    
    # Apply tracking if capable
    if tracking_capability > 0.0 and target:
        apply_tracking_correction(delta)

func apply_tracking_correction(delta: float) -> void:
    if not target:
        return
    
    var direction_to_target = (target.global_position - global_position).normalized()
    var current_direction = -transform.basis.z
    var correction = current_direction.lerp(direction_to_target, tracking_capability * delta)
    
    look_at(global_position + correction, Vector3.UP)
    set_linear_velocity(correction * projectile_speed)
```

## Damage and Subsystem Architecture

### Damage System

**DamageManager**
```gdscript
class_name DamageManager
extends Node

## Handles damage calculation and application

func apply_damage(target: BaseShip, damage_info: DamageInfo) -> DamageResult:
    var result = DamageResult.new()
    
    # Determine impact location and shield quadrant
    var impact_quadrant = calculate_shield_quadrant(damage_info.impact_point, target)
    
    # Apply shield damage first
    if target.shield_quadrants[impact_quadrant] > 0:
        var shield_damage = calculate_shield_damage(damage_info, target)
        target.shield_quadrants[impact_quadrant] -= shield_damage
        result.shield_damage = shield_damage
        
        # Shield absorption may reduce hull damage
        damage_info.damage *= calculate_shield_bleedthrough(shield_damage, target.shield_type)
    
    # Apply hull damage if any remains
    if damage_info.damage > 0:
        var hull_damage = calculate_hull_damage(damage_info, target)
        target.current_hull -= hull_damage
        result.hull_damage = hull_damage
        
        # Check for subsystem damage
        var damaged_subsystems = apply_subsystem_damage(damage_info, target)
        result.subsystem_damage = damaged_subsystems
    
    # Check for destruction
    if target.current_hull <= 0:
        result.ship_destroyed = true
        trigger_ship_destruction(target, damage_info.source)
    
    return result

class DamageInfo:
    var damage: float
    var damage_type: DamageType
    var impact_point: Vector3
    var impact_direction: Vector3
    var source: Node3D
    var weapon_type: String

enum DamageType {
    LASER,
    PARTICLE,
    MISSILE,
    BEAM,
    COLLISION,
    INTERNAL
}
```

### Subsystem Management

**SubsystemManager**
```gdscript
class_name SubsystemManager
extends Node

## Manages ship subsystems and their interactions

var subsystems: Dictionary = {}
var subsystem_dependencies: Dictionary = {}

class Subsystem:
    var name: String
    var max_health: float
    var current_health: float
    var operational_threshold: float = 0.5
    var repair_rate: float = 1.0
    var is_critical: bool = false
    var dependent_systems: Array[String] = []
    
    func get_efficiency() -> float:
        return current_health / max_health
    
    func is_operational() -> bool:
        return current_health >= (max_health * operational_threshold)

func create_subsystem(definition: SubsystemDefinition) -> Subsystem:
    var subsystem = Subsystem.new()
    subsystem.name = definition.name
    subsystem.max_health = definition.max_health
    subsystem.current_health = definition.max_health
    subsystem.operational_threshold = definition.operational_threshold
    subsystem.is_critical = definition.is_critical
    subsystem.dependent_systems = definition.dependencies
    
    return subsystem

func apply_subsystem_damage(subsystem_name: String, damage: float) -> void:
    if not subsystems.has(subsystem_name):
        return
    
    var subsystem = subsystems[subsystem_name]
    subsystem.current_health = max(0.0, subsystem.current_health - damage)
    
    # Check for cascading failures
    if not subsystem.is_operational():
        trigger_subsystem_failure(subsystem_name)
        check_dependent_systems(subsystem_name)
```

## Flight Control Integration

### Ship Flight Controller

**ShipFlightController**
```gdscript
class_name ShipFlightController
extends FlightController

## Ship-specific flight control with combat maneuvering

var ship: BaseShip
var combat_mode: bool = false
var evasion_active: bool = false
var afterburner_fuel: float = 100.0

func _ready() -> void:
    ship = get_parent() as BaseShip
    configure_flight_characteristics()

func configure_flight_characteristics() -> void:
    if not ship or not ship.ship_class:
        return
    
    var ship_class = ship.ship_class
    max_velocity = ship_class.max_velocity
    max_afterburner_velocity = ship_class.max_afterburner_velocity
    acceleration = ship_class.acceleration
    
    # Apply maneuverability to rotation rates
    pitch_rate = base_pitch_rate * ship_class.maneuverability.x
    yaw_rate = base_yaw_rate * ship_class.maneuverability.y
    roll_rate = base_roll_rate * ship_class.maneuverability.z

func engage_afterburners() -> bool:
    if afterburner_fuel <= 0:
        return false
    
    is_afterburner_active = true
    current_max_velocity = max_afterburner_velocity
    afterburner_fuel -= afterburner_consumption_rate
    
    # Visual and audio effects
    activate_afterburner_effects()
    return true

func execute_evasive_maneuvers(threat_direction: Vector3) -> void:
    evasion_active = true
    var evasion_vector = calculate_evasion_direction(threat_direction)
    
    # Apply evasive thrust
    apply_thrust(evasion_vector)
    
    # Random jinking maneuvers
    add_random_rotation_input()
```

## Combat Effects and Feedback

### Visual Effects Manager

**CombatEffectsManager**
```gdscript
class_name CombatEffectsManager
extends Node

## Manages combat visual and audio effects

var effect_pools: Dictionary = {}
var audio_pools: Dictionary = {}

func create_weapon_fire_effect(weapon_type: String, muzzle_position: Vector3, muzzle_rotation: Vector3) -> void:
    var effect = get_pooled_effect("weapon_fire_" + weapon_type)
    effect.global_position = muzzle_position
    effect.global_rotation = muzzle_rotation
    effect.restart()
    
    # Muzzle flash
    var muzzle_flash = get_pooled_effect("muzzle_flash")
    muzzle_flash.global_position = muzzle_position
    muzzle_flash.restart()

func create_impact_effect(impact_point: Vector3, impact_normal: Vector3, damage_type: DamageType, target_material: String) -> void:
    var effect_name = "impact_" + DamageType.keys()[damage_type].to_lower() + "_" + target_material
    var effect = get_pooled_effect(effect_name)
    
    effect.global_position = impact_point
    effect.look_at(impact_point + impact_normal, Vector3.UP)
    effect.restart()
    
    # Screen shake for player ship hits
    if target_material == "player_hull":
        CameraManager.add_screen_shake(calculate_shake_intensity(damage_type))

func create_explosion_effect(position: Vector3, explosion_size: ExplosionSize, explosion_type: String) -> void:
    var effect = get_pooled_effect("explosion_" + explosion_type)
    effect.global_position = position
    effect.scale = Vector3.ONE * get_explosion_scale(explosion_size)
    effect.restart()
    
    # Camera shake for nearby explosions
    var distance_to_player = position.distance_to(PlayerManager.get_player_position())
    if distance_to_player < explosion_shake_range:
        var shake_intensity = calculate_explosion_shake(explosion_size, distance_to_player)
        CameraManager.add_screen_shake(shake_intensity)
```

## Integration Systems

### Object System Integration

**Ship-Object Interface**
```gdscript
func _on_collision_detected(collision_info: Dictionary) -> void:
    var other_object = collision_info.collider as BaseSpaceObject
    
    match other_object.object_type:
        ObjectType.OBJ_WEAPON:
            handle_weapon_impact(other_object, collision_info)
        ObjectType.OBJ_SHIP:
            handle_ship_collision(other_object, collision_info)
        ObjectType.OBJ_DEBRIS:
            handle_debris_impact(other_object, collision_info)
        ObjectType.OBJ_ASTEROID:
            handle_asteroid_collision(other_object, collision_info)

func handle_weapon_impact(weapon: Projectile, collision_info: Dictionary) -> void:
    var damage_info = DamageInfo.new()
    damage_info.damage = weapon.damage_amount
    damage_info.damage_type = weapon.damage_type
    damage_info.impact_point = collision_info.position
    damage_info.impact_direction = collision_info.normal
    damage_info.source = weapon.owner_ship
    damage_info.weapon_type = weapon.weapon_definition.name
    
    var damage_result = DamageManager.apply_damage(self, damage_info)
    process_damage_result(damage_result)
    
    # Destroy the weapon projectile
    weapon.on_impact_target(self)
```

### AI System Integration

**Combat AI Interface**
```gdscript
func get_combat_status() -> CombatStatus:
    if current_target and is_in_combat():
        return CombatStatus.ACTIVE_COMBAT
    elif get_threat_level() > 0.5:
        return CombatStatus.ALERT
    else:
        return CombatStatus.PATROL

func get_weapon_threat_level() -> float:
    var total_threat = 0.0
    for bank in weapon_banks:
        for weapon in bank.weapons:
            if weapon.can_fire():
                total_threat += weapon.weapon_definition.threat_rating
    return min(total_threat, 10.0)  # Cap at maximum threat level

func get_optimal_attack_range() -> float:
    var optimal_range = 0.0
    var weapon_count = 0
    
    for bank in weapon_banks:
        for weapon in bank.weapons:
            optimal_range += weapon.weapon_definition.optimal_range
            weapon_count += 1
    
    return optimal_range / max(weapon_count, 1)
```

## Performance Optimization

### Combat System Performance

**Update Optimization**
```gdscript
func _physics_process(delta: float) -> void:
    # Use LOD-based update frequencies
    match get_update_frequency():
        UpdateFrequency.HIGH_FREQUENCY:
            update_all_systems(delta)
        UpdateFrequency.MEDIUM_FREQUENCY:
            update_critical_systems(delta)
        UpdateFrequency.LOW_FREQUENCY:
            update_essential_systems(delta)
        UpdateFrequency.MINIMAL_FREQUENCY:
            update_basic_systems(delta)

func update_all_systems(delta: float) -> void:
    update_weapons(delta)
    update_shields(delta)
    update_subsystems(delta)
    update_flight_control(delta)
    update_effects(delta)

func update_critical_systems(delta: float) -> void:
    update_weapons(delta)
    update_shields(delta)
    update_flight_control(delta)
```

### Memory Management

**Object Pooling for Combat Elements**
```gdscript
class_name CombatObjectPool
extends Node

var projectile_pools: Dictionary = {}
var effect_pools: Dictionary = {}

func get_projectile(weapon_type: String) -> Projectile:
    if not projectile_pools.has(weapon_type):
        projectile_pools[weapon_type] = []
    
    var pool = projectile_pools[weapon_type]
    if pool.is_empty():
        return create_new_projectile(weapon_type)
    else:
        var projectile = pool.pop_back()
        projectile.reset_state()
        return projectile
```

## Testing Strategy

### Combat System Tests

**Weapon System Testing**
```gdscript
func test_weapon_firing():
    var test_ship = create_test_ship_with_weapons()
    var weapon_bank = test_ship.weapon_banks[0]
    
    var projectiles = weapon_bank.fire_weapons()
    assert(projectiles.size() > 0, "Weapons should fire projectiles")
    
    await get_tree().create_timer(0.1).timeout
    
    # Test rate of fire limitation
    var second_shot = weapon_bank.fire_weapons()
    assert(second_shot.size() == 0, "Rate of fire should prevent immediate second shot")

func test_damage_system():
    var target_ship = create_test_ship()
    var initial_hull = target_ship.current_hull
    
    var damage_info = create_test_damage(50.0)
    var result = DamageManager.apply_damage(target_ship, damage_info)
    
    assert(target_ship.current_hull < initial_hull, "Ship should take hull damage")
    assert(result.hull_damage > 0, "Damage result should report hull damage")
```

### Performance Tests

**Combat Performance Benchmarks**
```gdscript
func test_combat_performance():
    # Create 20 ships in active combat
    var ships = []
    for i in range(20):
        var ship = create_test_combat_ship()
        ships.append(ship)
    
    # Measure frame time during intense combat
    for frame in range(300):  # 5 seconds at 60 FPS
        await get_tree().process_frame
    
    var average_frame_time = get_average_frame_time()
    assert(average_frame_time < 16.67, "Combat should maintain 60 FPS")
```

## Implementation Phases

### Phase 1: Ship Foundation (2 weeks)
- BaseShip class and ship templates
- Basic weapon system implementation
- Shield system and damage application
- Flight control integration

### Phase 2: Combat Mechanics (2 weeks)
- Advanced weapon behaviors and projectiles
- Subsystem damage modeling
- Combat effects and feedback
- AI combat integration

### Phase 3: WCS-Specific Features (2 weeks)
- Authentic WCS weapon characteristics
- Ship class specializations
- Advanced combat maneuvers
- Balance and tuning

### Phase 4: Polish & Integration (1 week)
- Performance optimization
- Visual and audio effects polish
- Integration testing with AI and HUD systems
- Final combat balance validation

## Success Criteria

- [ ] Authentic WCS ship handling and combat feel
- [ ] Support for 20+ ships in active combat at 60+ FPS
- [ ] Accurate damage modeling with subsystem interactions
- [ ] Complete weapon system with all WCS weapon types
- [ ] Responsive flight controls with ship-specific characteristics
- [ ] Integrated AI combat behaviors
- [ ] Rich visual and audio combat feedback
- [ ] Comprehensive testing coverage for all combat scenarios
- [ ] Performance optimization for complex combat situations
- [ ] Full integration with object, AI, and HUD systems

## Integration Notes

**Dependency on EPIC-009**: Object system for ship and projectile management
**Dependency on EPIC-002**: Asset structures for ship and weapon definitions
**Integration with EPIC-010**: AI system for automated combat behaviors
**Integration with EPIC-012**: HUD system for combat information display
**Integration with EPIC-008**: Graphics system for combat visual effects

This architecture delivers authentic WCS combat mechanics while leveraging Godot's strengths for performance and extensibility.