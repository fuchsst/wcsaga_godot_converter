# Physics System Analysis

## Purpose
The physics system handles movement, rotation, acceleration, and all physical behaviors of game objects. It implements space flight dynamics with customizable properties for different ship types.

## Main Public Interfaces
- `physics_info` - Structure containing physics properties for objects
- `physics_sim()` - Main physics simulation function
- `physics_read_flying_controls()` - Processes control input
- `physics_init()` - Initializes physics properties
- `physics_apply_whack()` - Applies impulse forces
- `physics_collide_whack()` - Applies collision forces

## Key Components
- **Movement Simulation**: Position and velocity integration
- **Rotation Simulation**: Angular velocity and orientation integration
- **Control Input Processing**: Translation from controls to physics forces
- **Thrust Management**: Forward, side, and vertical thrusters
- **Damping Systems**: Velocity reduction over time
- **Acceleration Models**: Time-based acceleration to maximum velocity
- **Impulse Handling**: Force application for collisions and weapons
- **Special Flight Modes**: Afterburner, gliding, and warping

## Dependencies
- `object.h` - Physics properties are part of object data
- `vecmat.h` - Vector and matrix mathematics
- `ship.h` - Ship-specific physics properties

## Game Logic Integration
The physics system enables realistic space combat:
- Implements Newtonian physics for space movement
- Supports different flight models for various ship types
- Handles player and AI control inputs
- Integrates with collision system for response forces
- Manages special effects like afterburners and gliding
- Supports warp in/warp out sequences
- Enables weapon knockback and explosion effects