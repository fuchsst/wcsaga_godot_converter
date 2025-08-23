# Animation System Analysis

## Purpose
The animation system handles sprite-based animations, including texture animations, effect sequences, and animated UI elements.

## Main Public Interfaces
- `anim_load()` - Load animation files
- `anim_render()` - Render current animation frame
- `anim_get_frame()` - Get specific animation frame
- Animation timing and control functions

## Key Components
- **Frame Animation**: Sequential image-based animation
- **Timing Control**: Frame rate and playback control
- **Looping**: Repeating and non-repeating animations
- **Blending**: Smooth transitions between frames
- **Resource Management**: Loading and caching animation data
- **Effect Integration**: Particle and visual effect timing

## Dependencies
- `bmpman.h` - Bitmap loading and management
- `graphics.h` - Rendering functions
- `parse.h` - Animation definition parsing

## Game Logic Integration
The animation system provides visual dynamism:
- Enables animated UI elements and feedback
- Supports special effects through animated textures
- Integrates with weapon and explosion effects
- Provides character and interface animations
- Enables modding through external animation files