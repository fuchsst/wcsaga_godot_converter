# PlayerShip
# Represents a player-controlled spacecraft with movement, weapons, and health systems

class_name PlayerShip

extends Node2D

# ------------------------------------------------------------------------------
# Signals
# ------------------------------------------------------------------------------
signal health_changed(current_health: int, max_health: int)
signal destroyed()
signal weapon_fired(weapon_type: String, position: Vector2, direction: Vector2)

# ------------------------------------------------------------------------------
# Enums
# ------------------------------------------------------------------------------
enum WeaponType {
    LASER,
    MISSILE,
    PLASMA
}

enum ShipState {
    ACTIVE,
    DESTROYED,
    DOCKED
}

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
const MAX_HEALTH: int = 100
const MAX_SPEED: float = 300.0
const ACCELERATION: float = 500.0
const ROTATION_SPEED: float = 2.0

# ------------------------------------------------------------------------------
# Exported Variables
# ------------------------------------------------------------------------------
@export var starting_health: int = MAX_HEALTH
@export var ship_name: String = "Default Fighter"

# ------------------------------------------------------------------------------
# Public Variables
# ------------------------------------------------------------------------------
var current_health: int
var current_speed: float = 0.0
var ship_state: ShipState = ShipState.ACTIVE

# ------------------------------------------------------------------------------
# Private Variables
# ------------------------------------------------------------------------------
var _velocity: Vector2 = Vector2.ZERO
var _rotation_direction: int = 0
var _thrust_input: float = 0.0

# ------------------------------------------------------------------------------
# Onready Variables
# ------------------------------------------------------------------------------
@onready var sprite: Sprite2D = $Sprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var weapon_cooldown_timers: Dictionary = {
    WeaponType.LASER: $LaserCooldown,
    WeaponType.MISSILE: $MissileCooldown,
    WeaponType.PLASMA: $PlasmaCooldown
}

# ------------------------------------------------------------------------------
# Static Functions
# ------------------------------------------------------------------------------
static func calculate_damage(weapon_type: WeaponType, distance: float) -> float:
    """
    Calculate damage based on weapon type and distance to target
    @param weapon_type: Type of weapon being fired
    @param distance: Distance to target in meters
    @returns: Damage value as a float
    """
    var base_damage: float = 0.0
    match weapon_type:
        WeaponType.LASER:
            base_damage = 25.0
        WeaponType.MISSILE:
            base_damage = 50.0
        WeaponType.PLASMA:
            base_damage = 40.0
    
    # Damage falloff over distance
    var falloff: float = 1.0 - (distance / 1000.0)
    return base_damage * clamp(falloff, 0.1, 1.0)

# ------------------------------------------------------------------------------
# Built-in Virtual Methods
# ------------------------------------------------------------------------------
func _ready() -> void:
    """
    Initialize the player ship when the node enters the scene tree
    """
    current_health = starting_health
    ship_state = ShipState.ACTIVE

func _process(delta: float) -> void:
    """
    Handle continuous processing logic
    @param delta: Time since last frame in seconds
    """
    if ship_state != ShipState.ACTIVE:
        return
    
    _update_rotation(delta)
    _update_thrust(delta)

func _physics_process(delta: float) -> void:
    """
    Handle physics-related updates
    @param delta: Time since last frame in seconds
    """
    if ship_state != ShipState.ACTIVE:
        return
    
    _apply_movement(delta)

# ------------------------------------------------------------------------------
# Public Methods
# ------------------------------------------------------------------------------
func take_damage(damage: int) -> void:
    """
    Apply damage to the ship
    @param damage: Amount of damage to apply
    """
    if ship_state != ShipState.ACTIVE:
        return
    
    current_health = max(0, current_health - damage)
    emit_signal("health_changed", current_health, MAX_HEALTH)
    
    if current_health <= 0:
        _destroy()

func fire_weapon(weapon_type: WeaponType) -> bool:
    """
    Fire a weapon if it's ready
    @param weapon_type: Type of weapon to fire
    @returns: True if weapon was fired, false if on cooldown
    """
    if ship_state != ShipState.ACTIVE:
        return false
    
    if not weapon_cooldown_timers.has(weapon_type):
        return false
    
    var timer: Timer = weapon_cooldown_timers[weapon_type]
    if timer.is_stopped():
        # Fire the weapon
        emit_signal("weapon_fired", 
                   WeaponType.keys()[weapon_type], 
                   global_position, 
                   Vector2.RIGHT.rotated(rotation))
        
        # Start cooldown
        timer.start()
        return true
    
    return false

func get_ship_info() -> Dictionary:
    """
    Get comprehensive information about the ship's current state
    @returns: Dictionary with ship information
    """
    return {
        "name": ship_name,
        "health": current_health,
        "max_health": MAX_HEALTH,
        "speed": current_speed,
        "position": global_position,
        "state": ShipState.keys()[ship_state]
    }

# ------------------------------------------------------------------------------
# Private Methods
# ------------------------------------------------------------------------------
func _update_rotation(delta: float) -> void:
    """
    Update ship rotation based on input
    @param delta: Time since last frame in seconds
    """
    rotation += _rotation_direction * ROTATION_SPEED * delta

func _update_thrust(delta: float) -> void:
    """
    Update thrust based on input
    @param delta: Time since last frame in seconds
    """
    _velocity = _velocity.move_toward(
        Vector2.RIGHT.rotated(rotation) * (_thrust_input * MAX_SPEED),
        ACCELERATION * delta
    )
    current_speed = _velocity.length()

func _apply_movement(delta: float) -> void:
    """
    Apply movement to the ship's position
    @param delta: Time since last frame in seconds
    """
    position += _velocity * delta

func _destroy() -> void:
    """
    Handle ship destruction
    """
    ship_state = ShipState.DESTROYED
    emit_signal("destroyed")
    # Add visual effects, sounds, etc.

# ------------------------------------------------------------------------------
# Input Handlers
# ------------------------------------------------------------------------------
func _input(event: InputEvent) -> void:
    """
    Handle input events
    @param event: Input event to process
    """
    if ship_state != ShipState.ACTIVE:
        return
    
    # Rotation input
    if event.is_action_pressed("rotate_left"):
        _rotation_direction = -1
    elif event.is_action_pressed("rotate_right"):
        _rotation_direction = 1
    elif event.is_action_released("rotate_left") and _rotation_direction == -1:
        _rotation_direction = 0
    elif event.is_action_released("rotate_right") and _rotation_direction == 1:
        _rotation_direction = 0
    
    # Thrust input
    if event.is_action_pressed("thrust_forward"):
        _thrust_input = 1.0
    elif event.is_action_released("thrust_forward"):
        _thrust_input = 0.0
    
    # Weapon firing
    if event.is_action_pressed("fire_laser"):
        fire_weapon(WeaponType.LASER)
    elif event.is_action_pressed("fire_missile"):
        fire_weapon(WeaponType.MISSILE)
    elif event.is_action_pressed("fire_plasma"):
        fire_weapon(WeaponType.PLASMA)
