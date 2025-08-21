# TestPlayerShip
# Unit tests for the PlayerShip class

extends "res://addons/gdUnit4/src/GdUnit4"

# ------------------------------------------------------------------------------
# Test Setup
# ------------------------------------------------------------------------------
var player_ship: PlayerShip

func before_all():
    # Setup code that runs once before all tests
    pass

func after_all():
    # Teardown code that runs once after all tests
    pass

func before_each():
    # Setup code that runs before each test
    player_ship = PlayerShip.new()
    # Add to scene tree to initialize
    add_child(player_ship)
    player_ship._ready()

func after_each():
    # Teardown code that runs after each test
    if player_ship != null and is_instance_valid(player_ship):
        player_ship.queue_free()

# ------------------------------------------------------------------------------
# Test Cases
# ------------------------------------------------------------------------------
func test_initialization():
    # Test that the player ship initializes with correct default values
    assert_that(player_ship.current_health).is_equal(100)
    assert_that(player_ship.ship_state).is_equal(PlayerShip.ShipState.ACTIVE)
    assert_that(player_ship.current_speed).is_equal(0.0)

func test_take_damage():
    # Test that taking damage reduces health correctly
    player_ship.take_damage(25)
    assert_that(player_ship.current_health).is_equal(75)
    
    # Test that health doesn't go below zero
    player_ship.take_damage(100)
    assert_that(player_ship.current_health).is_equal(0)

func test_fire_weapon():
    # Test that weapons can be fired when not on cooldown
    var result = player_ship.fire_weapon(PlayerShip.WeaponType.LASER)
    assert_that(result).is_true()
    
    # Test that weapons cannot be fired when on cooldown
    result = player_ship.fire_weapon(PlayerShip.WeaponType.LASER)
    assert_that(result).is_false()

func test_get_ship_info():
    # Test that ship info is returned correctly
    var info = player_ship.get_ship_info()
    assert_that(info).is_not_null()
    assert_that(info.name).is_equal("Default Fighter")
    assert_that(info.health).is_equal(100)
    assert_that(info.max_health).is_equal(100)
    assert_that(info.speed).is_equal(0.0)
    assert_that(info.state).is_equal("ACTIVE")

func test_destroy():
    # Test that the ship is destroyed when health reaches zero
    # Connect to the destroyed signal
    var destroyed_emitted = false
    player_ship.connect("destroyed", func(): destroyed_emitted = true)
    
    # Reduce health to zero
    player_ship.take_damage(100)
    
    # Check that the ship is destroyed
    assert_that(player_ship.ship_state).is_equal(PlayerShip.ShipState.DESTROYED)
    assert_that(destroyed_emitted).is_true()

# ------------------------------------------------------------------------------
# Helper Methods
# ------------------------------------------------------------------------------
func create_mock_timer() -> Timer:
    """
    Create a mock timer for testing
    @returns: Configured Timer node
    """
    var timer = Timer.new()
    timer.one_shot = true
    timer.autostart = false
    add_child(timer)
    return timer

func simulate_input(action: String, pressed: bool):
    """
    Simulate an input action for testing
    @param action: Name of the action to simulate
    @param pressed: Whether the action is pressed or released
    """
    var event = InputEventAction.new()
    event.action = action
    event.pressed = pressed
    Input.parse_input_event(event)
