# Resource Generators Module - Godot Resource Creation

## Overview
The Resource Generators module handles the creation of Godot-specific resource files (.tres) from the intermediate data structures. This module focuses on generating data-only resources that encapsulate gameplay properties, physics parameters, and asset relationships for use in Godot scenes.

## Key Components

### Resource Creators
- **ShipClassGenerator**: Creates Godot resources from parsed ship data, including physics properties, weapon compatibility, and subsystem definitions
- **WeaponResourceGenerator**: Generates weapon resources with damage profiles, firing behaviors, and visual effects parameters
- **ArmorTypeGenerator**: Produces armor type resources with damage resistance modifiers and material properties
- **SpeciesGenerator**: Creates species-specific resources for thruster animations and debris behavior

### Output Handlers
- **ResourceSerializer**: Handles the serialization of Godot resource files with proper formatting and validation
- **DependencyManager**: Manages resource relationships and ensures all linked assets are properly referenced
- **VersionController**: Tracks resource versions and handles backward compatibility for asset updates

## Conversion Process
1. **Data Ingestion**: Receives intermediate data structures from table converters
2. **Resource Mapping**: Translates WCS properties to Godot resource properties
3. **File Generation**: Creates .tres files with appropriate Godot resource syntax
4. **Validation**: Ensures resource integrity and functional correctness

## Integration Points
- Consumes intermediate data from core module structures
- Outputs Godot resources for use in scene assembly
- Works alongside scene generators for complete asset pipeline
