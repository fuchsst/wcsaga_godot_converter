# EPIC-001: Core Foundation & Infrastructure - Godot Files

**Epic**: EPIC-001 - Core Foundation & Infrastructure  
**Architect**: Mo (Godot Architect)  
**Version**: 2.0 (Based on source code analysis and Godot-native approach)  
**Date**: 2025-01-27  

## Overview

Foundation infrastructure providing platform abstraction, file I/O, mathematical utilities, and data parsing frameworks. **Architectural Revolution**: Based on comprehensive WCS source analysis, this epic leverages Godot's built-in systems instead of porting WCS complexity, dramatically simplifying implementation.

**Key Insight**: Most WCS foundation complexity (58+ files, 100+ dependencies) can be replaced with Godot's native capabilities.

## Godot Project Structure

### Core Constants and Types (Minimal Custom Code)

#### `res://scripts/core/constants/`
- `wcs_constants.gd`: Global game constants as static class
- `wcs_types.gd`: Enums and type definitions
- `wcs_paths.gd`: Standard game directory paths

**Implementation Note**: These replace WCS's `globalincs/pstypes.h` and complex type system with simple GDScript classes.

### Configuration System (Resource-Based)

#### `res://resources/config/`
- `game_config.tres`: Main game configuration (extends Resource)
- `player_profile.tres`: Player data and settings (extends Resource)
- `control_settings.tres`: Input mapping configuration (extends Resource)

#### `res://scripts/core/config/`
- `game_config.gd`: GameConfig resource class
- `player_profile.gd`: PlayerProfile resource class  
- `control_settings.gd`: ControlSettings resource class

**Implementation Note**: Replaces WCS's complex configuration parsing with Godot's built-in Resource system.

### Asset Management (Godot-Native)

#### `res://scripts/core/assets/`
- `wcs_resource_loader.gd`: Custom ResourceLoader for WCS formats (only if needed)
- `asset_registry.gd`: Light asset discovery system (AUTOLOAD - only if truly needed)

**Implementation Note**: Most asset loading uses Godot's native ResourceLoader. Custom loader only for specialized WCS formats.

### Utilities (Wrapper Functions)

#### `res://scripts/core/utils/`
- `math_utils.gd`: Wrapper functions for Godot's Vector3/Transform3D operations
- `file_utils.gd`: Simple file operation helpers using FileAccess
- `debug_utils.gd`: Debug output and logging helpers

**Implementation Note**: These provide WCS-compatible API while using Godot's built-in math and file systems.

## Autoload Singletons (MINIMAL - Only When Necessary)

### `res://autoloads/asset_registry.gd` (ONLY IF NEEDED)
```gdscript
# ONLY create this autoload if asset discovery is truly needed
# Most cases should use direct ResourceLoader.load() calls
```

**Mo's Opinion**: Resist the temptation to create autoloads. Most "global" systems can be handled with static classes or dependency injection.

## Testing Infrastructure

#### `res://tests/core/`
- `test_wcs_constants.gd`: Constants validation tests
- `test_game_config.gd`: Configuration system tests
- `test_math_utils.gd`: Mathematical operation accuracy tests
- `test_file_utils.gd`: File operation tests

## Scene Files (Minimal)

#### `res://scenes/core/`
- `debug_overlay.tscn`: Debug information display (Control node tree)

**Note**: Most foundation systems are pure scripts, not scenes. Keep scene count minimal.

## Project Configuration Files

#### `res://`
- `project.godot`: Updated with custom resource types and settings
- `export_presets.cfg`: Export configurations for different platforms

#### `.godot/` (Generated)
- Godot's generated files - do not modify directly

## Resource Definition Files

#### `res://scripts/core/resources/`
- `base_wcs_resource.gd`: Base class for all WCS data resources
- `wcs_data_validator.gd`: Validation utilities for converted data

## File Count Summary

**Total Implementation Files**: ~15-20 files (compared to 58+ WCS files)
- **Core Scripts**: 8-10 files
- **Resource Classes**: 3-5 files  
- **Utilities**: 3-4 files
- **Test Files**: 4-5 files
- **Autoloads**: 0-1 files (only if absolutely necessary)

## Implementation Priority

### Phase 1: Essential Foundation (Week 1)
1. `wcs_constants.gd` - Core constants
2. `wcs_types.gd` - Type definitions
3. `game_config.gd` - Configuration system

### Phase 2: Utilities (Week 2)
1. `math_utils.gd` - Mathematical wrappers
2. `file_utils.gd` - File operation helpers
3. `debug_utils.gd` - Debug utilities

### Phase 3: Asset Integration (Week 3-4)
1. `wcs_resource_loader.gd` - Custom resource loading (if needed)
2. `asset_registry.gd` - Asset discovery (only if required)
3. Testing and validation

## Mo's Architectural Notes

**Godot Strengths Leveraged**:
- **FileAccess**: Replaces WCS's complex file I/O system
- **Vector3/Transform3D**: Replaces custom mathematical libraries
- **Resource System**: Replaces custom configuration parsing
- **Built-in Caching**: Eliminates need for custom cache management
- **Cross-Platform**: Native Godot capabilities replace platform abstraction

**WCS Complexity Eliminated**:
- No custom memory management (Godot handles it)
- No platform-specific code (Godot abstracts it)
- No custom file parsing (Resource system handles it)
- No performance optimization needed (15+ year old game)

**Quality Standards**:
- 100% static typing in all scripts
- Every public function has docstring documentation
- All Resource classes use @export for Godot editor integration
- Comprehensive test coverage for mathematical accuracy

**Warning**: Resist the urge to over-engineer. If Godot provides it natively, use Godot's solution.

---

**Implementation Confidence**: This simplified architecture is achievable in 4-6 weeks and provides a robust foundation for all subsequent epics.