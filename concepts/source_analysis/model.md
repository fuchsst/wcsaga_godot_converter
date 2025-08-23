# Model System Analysis

## Purpose
The model system handles 3D model loading, rendering, and interaction. It manages POF (Parallax Object Format) files, submodels, textures, and all visual aspects of game entities.

## Main Public Interfaces
- `polymodel` - Structure representing loaded 3D models
- `bsp_info` - Structure for submodel information
- `model_subsystem` - Structure for model subsystem definitions
- `model_load()` - Loads a model from file
- `model_render()` - Renders a model
- `model_collide()` - Performs collision detection with models
- `model_get()` - Retrieves loaded model by index
- `submodel_render()` - Renders a specific submodel

## Key Components
- **Model Loading**: POF file parsing and loading
- **Submodel System**: Hierarchical model components with relative positioning
- **Texture Management**: Multi-layer texture mapping (base, glow, specular, normal, height)
- **Animation Support**: Rotating submodels and triggered animations
- **Collision Detection**: Polygon-level collision with bounding box optimization
- **Special Points**: Gun points, missile points, docking points, thrusters
- **Shield Mesh**: Special collision mesh for shield interactions
- **Detail Levels**: Multiple LODs for performance optimization

## Dependencies
- `object.h` - Models are associated with game objects
- `2d.h` - Rendering functions and bitmap management
- `physics.h` - Model physical properties
- `ai.h` - Subsystems are used by AI for targeting

## Game Logic Integration
The model system provides core visual functionality:
- Renders all 3D assets in the game world
- Enables detailed damage modeling through submodels
- Supports weapon firing through gun point positioning
- Implements docking through docking point management
- Provides collision geometry for gameplay interactions
- Enables visual effects through thruster and glow point systems
- Supports performance optimization through LOD systems