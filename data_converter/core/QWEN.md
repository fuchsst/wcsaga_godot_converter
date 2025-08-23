# Core Module - WCS Data Conversion Pipeline

## Overview
The Core module provides the foundational data structures and utilities that power the entire WCS to Godot conversion pipeline. This module defines the engine-agnostic intermediate representation that bridges the gap between legacy WCS formats and modern Godot resources.

## Key Components

### Intermediate Data Structures
- **IntermediateModel**: Represents 3D model data extracted from .POF files, including geometry, sub-object hierarchies, and metadata points
- **IntermediateMaterial**: Contains material properties and texture mappings for PBR approximation
- **IntermediateShipStats**: Holds gameplay properties parsed from ships.tbl and weapons.tbl files
- **AssetRelationship**: Tracks relationships between source assets and their target conversions

### Common Utilities
- **ConversionUtils**: Provides shared parsing utilities for string extraction, type conversion, and value validation
- **FileSystemUtils**: Handles asset discovery and filesystem operations for texture variant detection
- **LoggingUtils**: Centralized logging configuration for the entire conversion pipeline

## Architecture Role
The Core module serves as the central data exchange format between the Loader and Transformer stages of the pipeline. All specialized converters populate these intermediate structures, which are then consumed by the resource and scene generators.

## Integration Points
- Used by all table converters for data structure definitions
- Consumed by resource generators for Godot resource creation
- Utilized by scene generators for scene assembly and metadata embedding
