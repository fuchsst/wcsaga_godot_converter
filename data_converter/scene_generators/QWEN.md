# Scene Generators Module - Godot Scene Assembly

## Overview
The Scene Generators module handles the assembly of complete Godot scenes from converted assets and resources. This module combines 3D models, materials, physics properties, and gameplay metadata into functional Godot scenes ready for use in the game engine.

## Key Components

### Scene Assemblers
- **ShipSceneGenerator**: Creates complete ship scenes with RigidBody3D nodes, collision shapes, and weapon hardpoints
- **WeaponSceneGenerator**: Assembles weapon scenes with projectile emitters, visual effects, and sound components
- **EnvironmentSceneGenerator**: Builds environmental scenes including asteroids, space stations, and celestial objects

### Metadata Integration
- **NodeMapper**: Embeds gameplay metadata as empty nodes with custom properties in the scene hierarchy
- **ScriptAttacher**: Adds GDScript components to nodes for gameplay functionality
- **RelationshipBinder**: Establishes links between scene nodes and external resources

## Conversion Process
1. **Scene Initialization**: Creates root nodes and establishes scene hierarchy
2. **Asset Integration**: Imports glTF models and applies converted materials
3. **Physics Setup**: Configures collision shapes and physics properties from resource data
4. **Metadata Embedding**: Adds empty nodes for hardpoints, thrusters, and subsystems
5. **Script Attachment**: Installs gameplay scripts and event handlers

## Integration Points
- Consumes glTF models from POF parser output
- Utilizes Godot resources from resource generators
- Embeds metadata for post-import processing
- Outputs .tscn files for direct use in Godot