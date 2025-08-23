# Fireball System Analysis

## Purpose
The fireball system handles explosion effects, including visual effects, damage application, and particle generation. It provides visual feedback for weapon impacts and ship destruction.

## Main Public Interfaces
- `fireball_create()` - Creates fireball instances
- `fireball_process()` - Updates fireballs each frame
- `fireball_init()` - Initializes fireball system
- `fireball_level_init()` - Initializes fireballs for each level

## Key Components
- **Explosion Effects**: Visual representations of explosions
- **Damage Area**: Radius-based damage application
- **Particle Effects**: Smoke, sparks, and other visual elements
- **Animation**: Frame-based explosion animations
- **Sound Effects**: Audio accompanying explosions
- **Lighting Effects**: Dynamic lighting changes

## Dependencies
- `object.h` - Fireballs are object instances
- `weapon.h` - Weapon impacts create fireballs
- `ship.h` - Ship destruction creates fireballs
- `graphics.h` - Rendering functions

## Game Logic Integration
The fireball system enhances combat feedback:
- Provides visual and audio feedback for weapon hits
- Applies area-of-effect damage for explosions
- Creates dramatic visual effects for ship destruction
- Integrates with particle systems for rich effects
- Supports different explosion types for different weapons