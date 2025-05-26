# EPIC-001: Core Foundation & Infrastructure - Godot Dependencies

## Overview
Foundation infrastructure dependency mapping. This epic has NO external dependencies and provides critical services to ALL other epics. Dependency relationships are internal to the foundation layer only.

## Autoload Initialization Sequence

### Autoload: `res://autoloads/core_manager.gd`
**Initialization Priority**: 1 (First to load)
**Dependencies**: None (foundation singleton)
**Initializes**:
- Global error handling system
- System registry for other autoloads
- Core configuration loading

**Signals Emitted**:
- `core_systems_initialized()` - All foundation systems ready
- `system_registered(system_name: String)` - New system registered
- `shutdown_requested()` - Clean shutdown initiated

**References/Uses**:
- `res://systems/core/utilities/error_handler.gd` for global error handling
- `res://systems/core/utilities/debug_logger.gd` for system logging
- `res://resources/core/core_settings.tres` for configuration

### Autoload: `res://autoloads/platform_abstraction.gd`
**Initialization Priority**: 2 (After core manager)
**Dependencies**: `CoreManager` registration
**Signals Connected To**:
- `CoreManager.shutdown_requested.connect(_on_shutdown_requested)`

**References/Uses**:
- `res://systems/core/platform/os_abstraction.gd`
- `res://systems/core/platform/directory_services.gd`
- `res://resources/core/platform_config.tres`

**Signals Emitted**:
- `platform_initialized(os_name: String, architecture: String)`
- `directory_services_ready()`

### Autoload: `res://autoloads/file_system_manager.gd`
**Initialization Priority**: 3 (After platform)
**Dependencies**: `PlatformAbstraction.directory_services_ready()`
**Signals Connected To**:
- `PlatformAbstraction.platform_initialized.connect(_on_platform_ready)`

**References/Uses**:
- `res://systems/core/file_system/file_path_resolver.gd`
- `res://systems/core/file_system/vp_archive_reader.gd`
- `res://systems/core/file_system/resource_locator.gd`
- `res://resources/core/file_system_config.tres`

**Signals Emitted**:
- `file_system_initialized()`
- `vp_archives_mounted(archive_count: int)`
- `file_load_completed(file_path: String, success: bool)`

### Autoload: `res://autoloads/vp_archive_manager.gd`
**Initialization Priority**: 4 (After file system)
**Dependencies**: `FileSystemManager.file_system_initialized()`
**Signals Connected To**:
- `FileSystemManager.file_system_initialized.connect(_mount_vp_archives)`

**References/Uses**:
- `res://systems/core/file_system/vp_archive_reader.gd`
- `res://systems/core/file_system/file_validator.gd`

**Signals Emitted**:
- `vp_archive_mounted(archive_name: String, file_count: int)`
- `vp_file_extracted(archive: String, file_path: String)`

### Autoload: `res://autoloads/math_utilities.gd`
**Initialization Priority**: 5 (Independent - can load anytime)
**Dependencies**: `CoreManager` registration only
**References/Uses**:
- `res://systems/core/math/vector_math.gd`
- `res://systems/core/math/matrix_math.gd`
- `res://systems/core/math/physics_math.gd`
- `res://resources/core/space_constants.tres`

**Signals Emitted**:
- `math_systems_initialized()`

## Core Infrastructure Dependencies

### Script: `res://systems/core/file_system/vp_archive_reader.gd`
**Used By**: 
- `FileSystemManager` autoload
- `VPArchiveManager` autoload
- All epics requiring WCS asset loading

**References/Uses**:
- `res://systems/core/file_system/file_path_resolver.gd` for path operations
- `res://systems/core/utilities/error_handler.gd` for error reporting
- `res://systems/core/data_structures/ring_buffer.gd` for streaming reads

**Functions Called By Other Systems**:
- `read_vp_header(file_path: String) -> Dictionary`
- `extract_file_from_vp(archive_path: String, internal_path: String) -> PackedByteArray`
- `list_vp_contents(archive_path: String) -> Array[String]`

### Script: `res://systems/core/math/vector_math.gd`
**Used By**: Physics systems, AI systems, rendering systems, combat systems
**References/Uses**:
- `res://resources/core/space_constants.tres` for scale factors
- `res://resources/core/conversion_factors.tres` for unit conversions

**Functions Called By Other Systems**:
- `space_distance_3d(pos1: Vector3, pos2: Vector3) -> float`
- `calculate_intercept_point(target_pos: Vector3, target_vel: Vector3, projectile_speed: float) -> Vector3`
- `normalize_space_vector(vector: Vector3) -> Vector3`
- `angular_difference(angle1: float, angle2: float) -> float`

### Script: `res://systems/core/parsing/config_parser.gd`
**Used By**: Asset management, ship definitions, weapon definitions, mission loading
**References/Uses**:
- `res://systems/core/utilities/error_handler.gd` for parse error reporting
- `res://systems/core/parsing/data_validator.gd` for validation

**Functions Called By Other Systems**:
- `parse_config_file(file_path: String) -> Dictionary`
- `parse_table_file(file_path: String) -> Array[Dictionary]`
- `validate_config_structure(config_data: Dictionary, schema: Dictionary) -> bool`

## Resource Loading Dependencies

### Resource: `res://resources/core/core_settings.tres`
**Script Type**: `CoreSettings` (extends Resource)
**Loaded By**: `CoreManager` during initialization
**Properties Accessed**:
- `debug_mode: bool`
- `log_level: int`
- `performance_monitoring: bool`
- `error_recovery_mode: int`

### Resource: `res://resources/core/file_system_config.tres`
**Script Type**: `FileSystemConfig` (extends Resource)
**Loaded By**: `FileSystemManager` during initialization
**Properties Accessed**:
- `vp_archive_paths: Array[String]`
- `cache_size_limit: int`
- `preload_critical_files: bool`

### Resource: `res://resources/core/space_constants.tres`
**Script Type**: `SpaceConstants` (extends Resource)
**Loaded By**: `MathUtilities` during initialization
**Properties Accessed**:
- `wcs_to_godot_scale: float`
- `physics_time_step: float`
- `max_simulation_distance: float`

## Signal Flow Architecture

### Initialization Signal Chain
```
1. CoreManager._ready() → core_systems_initialized()
2. PlatformAbstraction._on_core_ready() → platform_initialized()
3. FileSystemManager._on_platform_ready() → file_system_initialized()
4. VPArchiveManager._on_file_system_ready() → vp_archives_mounted()
5. MathUtilities._ready() → math_systems_initialized()
```

### Cross-System Communication
**Error Handling Flow**:
```
Any System Error → ErrorHandler.report_error() → CoreManager.system_error → All Registered Systems
```

**File Loading Flow**:
```
System Request → FileSystemManager.load_file() → VPArchiveManager.extract_if_needed() → file_load_completed()
```

## External Integration Points (Provided to Other Epics)

### For EPIC-002 (Asset Management):
**Required Autoloads**: `FileSystemManager`, `VPArchiveManager`, `MathUtilities`
**Required Functions**: 
- `FileSystemManager.load_from_vp(archive: String, file_path: String) -> PackedByteArray`
- `VPArchiveManager.get_file_listing(archive: String) -> Array[String]`

### For EPIC-003 (Data Migration):
**Required Autoloads**: `FileSystemManager`, `PlatformAbstraction`
**Required Functions**:
- `PlatformAbstraction.execute_external_tool(command: String, args: Array) -> int`
- `FileSystemManager.validate_file_integrity(file_path: String) -> bool`

### For EPIC-004 (SEXP System):
**Required Autoloads**: `MathUtilities`, `CoreManager`
**Required Functions**:
- `MathUtilities.evaluate_math_expression(expression: String) -> float`
- `CoreManager.get_system_by_name(system_name: String) -> Node`

### For ALL Other Epics:
**Required Autoloads**: `CoreManager` (system registration and coordination)
**Required Functions**:
- `CoreManager.register_system(system_name: String, system_node: Node)`
- `CoreManager.is_system_ready(system_name: String) -> bool`

## Performance-Critical Paths

### High-Frequency Operations:
- `MathUtilities.space_distance_3d()` - Called every frame by physics/AI systems
- `FileSystemManager.file_exists()` - Called frequently by asset loading
- `VPArchiveManager.extract_file_from_vp()` - Called during asset streaming

### Memory-Sensitive Operations:
- VP archive file caching (configurable cache size limits)
- Mathematical operation result caching (for expensive calculations)
- Error handler message buffering (prevents memory leaks from error spam)

## Testing Dependencies

### Unit Test Structure:
```
res://tests/core/test_file_system.gd:
  Dependencies: None (isolated testing)
  Tests: VP archive reading, file path resolution, validation

res://tests/core/test_math_utilities.gd:
  Dependencies: SpaceConstants resource
  Tests: Vector operations, physics calculations, interpolation

res://tests/core/integration/test_core_systems_integration.gd:
  Dependencies: ALL core autoloads
  Tests: Full initialization sequence, cross-system communication
```

This foundation epic provides a robust, well-architected base that enables all subsequent epics to build upon solid, tested infrastructure while maintaining proper separation of concerns and optimal performance.