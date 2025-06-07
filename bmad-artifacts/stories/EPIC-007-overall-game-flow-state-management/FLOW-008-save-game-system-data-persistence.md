# FLOW-008: Save Game System and Data Persistence

**Epic**: EPIC-007 - Overall Game Flow & State Management  
**Phase**: 3 - Player Data and Persistence  
**Story ID**: FLOW-008  
**Story Name**: Save Game System and Data Persistence  
**Assigned**: Dev (GDScript Developer)  
**Status**: COMPLETED ✅  
**Story Points**: 9  
**Priority**: Critical  

---

## User Story

**As a** player  
**I want** a reliable save/load system that preserves all my game progress and never loses data  
**So that** I can safely pause my game at any time and resume exactly where I left off without fear of losing progress  

## Story Description

Leverage and extend the existing SaveGameManager autoload (`target/autoload/SaveGameManager.gd`) to support additional game flow save/load functionality. The existing SaveGameManager already provides comprehensive save/load operations with PlayerProfile and CampaignState resources, atomic operations, backup management, auto-save, and corruption detection. This story focuses on integrating the save system with new game flow states and adding any missing campaign-specific functionality.

## Acceptance Criteria

- [ ] **Enhanced Save Operations**: Integrate existing SaveGameManager with game flow states
  - [ ] Use existing `save_player_profile()` and `load_player_profile()` methods
  - [ ] Use existing `save_campaign_state()` and `load_campaign_state()` methods  
  - [ ] Leverage existing atomic save operations and backup management
  - [ ] Integrate save operations with new GameState transitions from FLOW-001

- [ ] **Extended Save Data Structure**: Use existing comprehensive resources
  - [ ] Use existing PlayerProfile (`addons/wcs_asset_core/resources/player/player_profile.gd`) with pilot statistics
  - [ ] Use existing CampaignState (`addons/wcs_asset_core/resources/save_system/campaign_state.gd`) with mission tracking
  - [ ] Use existing SaveSlotInfo (`addons/wcs_asset_core/resources/save_system/save_slot_info.gd`) for metadata
  - [ ] Integrate mission context data via existing resource extension patterns

- [ ] **Data Integrity System**: Use existing comprehensive validation
  - [ ] Leverage existing save file checksums and validation in SaveGameManager
  - [ ] Use existing data structure integrity checking from PlayerProfile.validate_profile()
  - [ ] Use existing corruption detection and repair mechanisms
  - [ ] Use existing save file version tracking and compatibility

- [ ] **Backup and Recovery**: Use existing comprehensive backup system
  - [ ] Use existing automatic backup creation (SaveGameManager.backup_count = 3)
  - [ ] Use existing multiple backup retention with rotation
  - [ ] Use existing manual backup creation (create_save_backup()) and restoration (restore_save_backup())
  - [ ] Use existing recovery from corrupted save files (validate_save_slot(), repair_save_slot())

## Technical Requirements

### Architecture Reference
- **Architecture Document**: `EPIC-007-overall-game-flow-state-management/architecture.md` (lines 136-235)
- **WCS Analysis**: Save/load systems across multiple WCS components
- **Existing Resource**: `target/autoload/SaveGameManager.gd` (already comprehensive with all save/load functionality)
- **Integration**: Use existing SaveGameManager methods and extend with game flow coordination

### Implementation Specifications

#### Game Flow Save Integration
```gdscript
# Integration coordinator for existing SaveGameManager
# target/scripts/core/game_flow/save_flow_coordinator.gd
class_name SaveFlowCoordinator
extends Node

# The SaveGameManager already provides all necessary functionality:
# - save_player_profile(profile: PlayerProfile, slot: int, save_type: SaveSlotInfo.SaveType)
# - load_player_profile(slot: int) -> PlayerProfile
# - save_campaign_state(state: CampaignState, slot: int) -> bool
# - load_campaign_state(slot: int) -> CampaignState
# - Auto-save functionality with configurable intervals
# - Backup management with 3-level rolling backups
# - Corruption detection and recovery
# - Performance tracking and optimization

# Coordinate save operations with game state transitions
func save_current_game_state(save_slot: int) -> bool:
    # Use existing SaveGameManager methods
    var current_profile: PlayerProfile = _get_current_player_profile()
    var current_campaign: CampaignState = _get_current_campaign_state()
    
    # Save using existing comprehensive system
    var profile_saved: bool = SaveGameManager.save_player_profile(current_profile, save_slot)
    var campaign_saved: bool = SaveGameManager.save_campaign_state(current_campaign, save_slot)
    
    return profile_saved and campaign_saved
        result.error_message = "Invalid pilot profile for save"
        return result
    
    # Create save data structure
    var save_data = _create_save_data(pilot, save_name)
    if not save_data:
        result.error_message = "Failed to create save data"
        return result
    
    # Determine save path
    var save_path = _get_save_path(save_slot, pilot.pilot_id)
    
    # Perform atomic save
    result = _perform_atomic_save(save_data, save_path)
    result.save_duration_ms = Time.get_ticks_msec() - start_time
    
    if result.success:
        save_completed.emit(save_path, save_slot, result.save_duration_ms)
        print("Save completed: %s (%.1fms)" % [save_path, result.save_duration_ms])
    else:
        save_failed.emit(result.error_message, save_path)
        push_error("Save failed: %s" % result.error_message)
    
    return result

func load_game(save_path: String) -> LoadResult:
    var result = LoadResult.new()
    var start_time = Time.get_ticks_msec()
    
    # Verify save file exists
    if not FileAccess.file_exists(save_path):
        result.error_message = "Save file not found: %s" % save_path
        return result
    
    # Load and validate save data
    var save_data = _load_and_validate_save_data(save_path)
    if not save_data:
        # Try to recover from backup
        save_data = _attempt_backup_recovery(save_path)
        if not save_data:
            result.error_message = "Failed to load save data and no valid backup found"
            return result
        result.recovered_from_backup = true
    
    # Apply save data to game systems
    var apply_result = _apply_save_data(save_data)
    if not apply_result.success:
        result.error_message = "Failed to apply save data: " + apply_result.error_message
        return result
    
    result.success = true
    result.save_data = save_data
    result.load_duration_ms = Time.get_ticks_msec() - start_time
    
    load_completed.emit(save_path, result.load_duration_ms, result.recovered_from_backup)
    print("Load completed: %s (%.1fms)" % [save_path, result.load_duration_ms])
    
    return result

# Quick save/load operations
func quick_save() -> SaveResult:
    var current_pilot = PilotManager.get_current_pilot()
    if not current_pilot:
        var result = SaveResult.new()
        result.error_message = "No current pilot for quick save"
        return result
    
    return save_game(current_pilot, QUICKSAVE_SLOT, "Quick Save")

func quick_load() -> LoadResult:
    var current_pilot = PilotManager.get_current_pilot()
    if not current_pilot:
        var result = LoadResult.new()
        result.error_message = "No current pilot for quick load"
        return result
    
    var save_path = _get_save_path(QUICKSAVE_SLOT, current_pilot.pilot_id)
    return load_game(save_path)

signal save_completed(save_path: String, save_slot: int, duration_ms: float)
signal save_failed(error_message: String, save_path: String)
signal load_completed(save_path: String, duration_ms: float, recovered_from_backup: bool)
signal load_failed(error_message: String, save_path: String)
```

#### Save Data Structure
```gdscript
# target/scripts/core/game_flow/persistence/save_game_data.gd
class_name SaveGameData
extends Resource

# Save file metadata
@export var save_version: int = 1
@export var creation_timestamp: int
@export var game_version: String
@export var save_name: String
@export var save_type: String  # "manual", "quick", "auto"

# Core game data
@export var pilot_profile: PilotProfile
@export var campaign_state: CampaignState
@export var mission_context: MissionContext  # null if not in mission
@export var game_settings: GameSettings
@export var session_data: SessionData

# Data integrity
@export var data_checksum: String
@export var component_checksums: Dictionary = {}

# Save data creation
static func create_save_data(pilot: PilotProfile, save_name: String, save_type: String = "manual") -> SaveGameData:
    var save_data = SaveGameData.new()
    
    # Metadata
    save_data.save_version = 1
    save_data.creation_timestamp = Time.get_unix_time_from_system()
    save_data.game_version = ProjectSettings.get_setting("application/config/version", "1.0.0")
    save_data.save_name = save_name
    save_data.save_type = save_type
    
    # Core data
    save_data.pilot_profile = pilot.duplicate()
    save_data.campaign_state = CampaignManager.get_current_state()
    save_data.mission_context = MissionContextManager.get_current_context()
    save_data.game_settings = SettingsManager.get_current_settings()
    save_data.session_data = SessionManager.get_current_session_data()
    
    # Calculate checksums
    save_data._calculate_checksums()
    
    return save_data

# Data validation
func is_valid() -> bool:
    # Basic structure validation
    if not pilot_profile or not campaign_state:
        return false
    
    # Checksum validation
    if not _validate_checksums():
        return false
    
    # Version compatibility check
    if not _is_version_compatible():
        return false
    
    return true

func _calculate_checksums() -> void:
    # Calculate individual component checksums
    component_checksums["pilot_profile"] = _calculate_resource_checksum(pilot_profile)
    component_checksums["campaign_state"] = _calculate_resource_checksum(campaign_state)
    
    if mission_context:
        component_checksums["mission_context"] = _calculate_resource_checksum(mission_context)
    
    if game_settings:
        component_checksums["game_settings"] = _calculate_resource_checksum(game_settings)
    
    # Calculate overall checksum
    var combined_data = str(pilot_profile) + str(campaign_state) + str(mission_context) + str(game_settings)
    data_checksum = combined_data.sha256_text()

func _validate_checksums() -> bool:
    # Validate individual components
    for component_name in component_checksums:
        var stored_checksum = component_checksums[component_name]
        var component = get(component_name)
        if component:
            var calculated_checksum = _calculate_resource_checksum(component)
            if stored_checksum != calculated_checksum:
                push_error("Checksum mismatch for component: %s" % component_name)
                return false
    
    # Validate overall checksum
    var combined_data = str(pilot_profile) + str(campaign_state) + str(mission_context) + str(game_settings)
    var calculated_checksum = combined_data.sha256_text()
    
    return data_checksum == calculated_checksum
```

#### Atomic Save Operations
```gdscript
# Atomic save implementation
func _perform_atomic_save(save_data: SaveGameData, save_path: String) -> SaveResult:
    var result = SaveResult.new()
    
    # Create backup of existing save
    if FileAccess.file_exists(save_path):
        var backup_result = _create_backup(save_path)
        if not backup_result.success:
            result.error_message = "Failed to create backup: " + backup_result.error_message
            return result
    
    # Write to temporary file first
    var temp_path = save_path + ".tmp"
    var save_error = ResourceSaver.save(save_data, temp_path)
    
    if save_error != OK:
        result.error_message = "Failed to write save file: " + error_string(save_error)
        _cleanup_temp_file(temp_path)
        return result
    
    # Verify the temporary save file
    var verification_result = _verify_save_file(temp_path)
    if not verification_result.is_valid:
        result.error_message = "Save file verification failed: " + verification_result.error_message
        _cleanup_temp_file(temp_path)
        return result
    
    # Atomic move from temp to final location
    var dir = DirAccess.open("user://saves/")
    if not dir:
        result.error_message = "Failed to access save directory"
        _cleanup_temp_file(temp_path)
        return result
    
    var move_error = dir.rename(temp_path, save_path)
    if move_error != OK:
        result.error_message = "Failed to finalize save file: " + error_string(move_error)
        _cleanup_temp_file(temp_path)
        return result
    
    # Success
    result.success = true
    result.save_path = save_path
    result.file_size = _get_file_size(save_path)
    
    return result

# Save file verification
func _verify_save_file(file_path: String) -> VerificationResult:
    var result = VerificationResult.new()
    
    # Load the save file
    var save_data = load(file_path)
    if not save_data:
        result.error_message = "Cannot load save file"
        return result
    
    if not save_data is SaveGameData:
        result.error_message = "Save file is not valid SaveGameData"
        return result
    
    # Validate save data
    if not save_data.is_valid():
        result.error_message = "Save file failed validation checks"
        return result
    
    result.is_valid = true
    return result
```

#### Backup Management System
```gdscript
# target/scripts/core/game_flow/persistence/backup_manager.gd
class_name BackupManager
extends RefCounted

const MAX_BACKUPS_PER_SLOT = 5

# Backup creation
func create_backup(save_path: String) -> BackupResult:
    var result = BackupResult.new()
    
    if not FileAccess.file_exists(save_path):
        result.error_message = "Source save file does not exist"
        return result
    
    # Generate backup path with timestamp
    var timestamp = Time.get_datetime_string_from_system().replace(":", "-").replace(" ", "_")
    var backup_name = save_path.get_file().get_basename() + "_backup_" + timestamp + ".save"
    var backup_path = _backup_base_path + backup_name
    
    # Ensure backup directory exists
    var dir = DirAccess.open("user://")
    dir.make_dir_recursive(_backup_base_path)
    
    # Copy file to backup location
    var copy_result = _copy_file(save_path, backup_path)
    if not copy_result:
        result.error_message = "Failed to copy save file to backup location"
        return result
    
    # Verify backup integrity
    var verification_result = _verify_save_file(backup_path)
    if not verification_result.is_valid:
        DirAccess.remove_absolute(backup_path)
        result.error_message = "Backup file failed verification"
        return result
    
    # Clean up old backups
    _cleanup_old_backups(save_path)
    
    result.success = true
    result.backup_path = backup_path
    return result

# Backup recovery
func restore_from_backup(save_path: String) -> RestoreResult:
    var result = RestoreResult.new()
    
    # Find most recent valid backup
    var backup_files = _find_backup_files(save_path)
    for backup_path in backup_files:
        var verification_result = _verify_save_file(backup_path)
        if verification_result.is_valid:
            # Restore from this backup
            var copy_result = _copy_file(backup_path, save_path)
            if copy_result:
                result.success = true
                result.restored_from = backup_path
                return result
    
    result.error_message = "No valid backup found for restoration"
    return result

# Backup file management
func _find_backup_files(save_path: String) -> Array[String]:
    var backup_files: Array[String] = []
    var save_name = save_path.get_file().get_basename()
    
    var dir = DirAccess.open(_backup_base_path)
    if not dir:
        return backup_files
    
    dir.list_dir_begin()
    var file_name = dir.get_next()
    
    while file_name != "":
        if file_name.begins_with(save_name + "_backup_") and file_name.ends_with(".save"):
            backup_files.append(_backup_base_path + file_name)
        file_name = dir.get_next()
    
    # Sort by modification time (newest first)
    backup_files.sort_custom(func(a, b): return FileAccess.get_modified_time(a) > FileAccess.get_modified_time(b))
    
    return backup_files

func _cleanup_old_backups(save_path: String) -> void:
    var backup_files = _find_backup_files(save_path)
    
    # Remove excess backups
    for i in range(MAX_BACKUPS_PER_SLOT, backup_files.size()):
        DirAccess.remove_absolute(backup_files[i])
```

### File Structure
```
target/scripts/core/game_flow/persistence/
├── save_game_manager.gd        # Main save/load coordination
├── save_game_data.gd           # Save data structure and validation
├── backup_manager.gd           # Backup creation and recovery
├── integrity_checker.gd        # Data integrity validation
├── save_result.gd              # Operation result structures
└── data_serialization.gd       # Custom serialization utilities
```

## Definition of Done

- [ ] **Code Quality**: All code follows GDScript static typing standards
  - [ ] 100% static typing with comprehensive type annotations
  - [ ] Atomic operations with proper transaction semantics
  - [ ] Comprehensive error handling with recovery mechanisms
  - [ ] Thread-safe operations for background saving

- [ ] **Testing**: Comprehensive test coverage
  - [ ] Atomic save operation testing (success and failure scenarios)
  - [ ] Data integrity validation testing
  - [ ] Backup and recovery testing
  - [ ] Save format version compatibility testing

- [ ] **Documentation**: Complete system documentation
  - [ ] Save file format specification
  - [ ] Data integrity and backup procedures
  - [ ] Recovery procedures for corrupted saves
  - [ ] Performance optimization guide

- [ ] **Integration**: Seamless integration with all game systems
  - [ ] Pilot management system integration
  - [ ] Campaign system integration for state persistence
  - [ ] Session management integration
  - [ ] Settings system integration

## Implementation Notes

### Save File Format Strategy
- Use Godot's resource system for native serialization
- Include version information for future compatibility
- Implement checksums for integrity validation
- Support compression for file size optimization

### Atomic Operations Design
- Use temporary files with atomic move operations
- Implement complete rollback on any failure
- Validate all data before finalizing saves
- Provide detailed error messages for debugging

### Backup Strategy
- Create automatic backups before each save
- Maintain multiple backup versions with rotation
- Support manual backup creation and restoration
- Include backup integrity validation

## Dependencies

### Prerequisite Stories
- **FLOW-003**: Session Management and Lifecycle
- **FLOW-007**: Pilot Management and Statistics

### Dependent Stories
- **FLOW-009**: Backup and Recovery Systems (extends this foundation)
- **All game systems**: Must integrate with save system for persistence

## Testing Strategy

### Unit Tests
```gdscript
# test_save_game_manager.gd
func test_atomic_save_operations():
    # Test save atomicity and rollback
    
func test_save_data_integrity():
    # Test data validation and checksums

# test_backup_manager.gd
func test_backup_creation():
    # Test automatic backup creation
    
func test_backup_recovery():
    # Test recovery from corrupted saves
    
func test_backup_rotation():
    # Test old backup cleanup
```

### Integration Tests
- End-to-end save/load testing with real game data
- Data corruption simulation and recovery testing
- Performance testing with large save files
- Version compatibility testing with save migration

---

**Story Ready for Implementation**: ✅  
**Architecture Reference**: Approved EPIC-007 architecture document  
**WCS Source Reference**: Save/load systems across multiple WCS components  
**Integration Complexity**: High - Critical system with complex data integrity requirements  
**Estimated Development Time**: 4-5 days for experienced GDScript developer