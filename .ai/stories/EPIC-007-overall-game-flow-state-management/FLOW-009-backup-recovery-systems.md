# FLOW-009: Backup and Recovery Systems

**Epic**: EPIC-007 - Overall Game Flow & State Management  
**Phase**: 3 - Player Data and Persistence  
**Story ID**: FLOW-009  
**Story Name**: Backup and Recovery Systems  
**Assigned**: Dev (GDScript Developer)  
**Status**: Ready for Implementation  
**Story Points**: 4  
**Priority**: Medium  

---

## User Story

**As a** player  
**I want** comprehensive backup and recovery systems that protect my game progress  
**So that** I can recover from data corruption, accidental deletions, or system failures without losing my game progress  

## Story Description

Enhance the existing backup and recovery systems already implemented in SaveGameManager (`target/autoload/SaveGameManager.gd`) with additional user interface and automation features. The SaveGameManager already provides comprehensive backup functionality including automatic backup creation, 3-level rolling backups, corruption detection, and recovery mechanisms. This story focuses on exposing these capabilities through user interfaces and adding enhanced automation.

## Acceptance Criteria

- [ ] **Enhanced Automated Backup System**: Extend existing SaveGameManager backup functionality
  - [ ] Use existing automatic backup creation (SaveGameManager.backup_count = 3)
  - [ ] Extend existing auto-save system (SaveGameManager.auto_save_enabled) with event triggers
  - [ ] Use existing backup retention policies with automatic cleanup
  - [ ] Use existing background save operations (SaveGameManager.background_saving)

- [ ] **Enhanced Manual Backup Tools**: UI for existing backup functionality
  - [ ] UI for existing manual backup creation (SaveGameManager.create_save_backup())
  - [ ] UI for existing backup browsing and management
  - [ ] UI for existing restore options (SaveGameManager.restore_save_backup())
  - [ ] UI for backup export/import using existing save/load methods

- [ ] **Enhanced Recovery Assistant**: UI for existing recovery functionality
  - [ ] UI for existing corruption detection (SaveGameManager.corruption_detected signal)
  - [ ] Recovery wizard using existing validate_save_slot() and repair_save_slot() methods
  - [ ] UI for existing data integrity reporting
  - [ ] UI for existing recovery validation and verification

- [ ] **Enhanced Backup Validation**: UI for existing validation functionality
  - [ ] UI for existing backup file integrity verification (validate_save_slot())
  - [ ] UI for periodic backup health checks using existing validation
  - [ ] UI for existing backup corruption detection
  - [ ] UI for existing backup repair attempts (repair_save_slot())

## Technical Requirements

### Architecture Reference
- **Architecture Document**: `EPIC-007-overall-game-flow-state-management/architecture.md` (backup and recovery sections)
- **WCS Analysis**: Data recovery and backup mechanisms
- **Existing Resource**: `target/autoload/SaveGameManager.gd` (already has comprehensive backup/recovery)
- **Dependencies**: Leverage existing SaveGameManager backup functionality

### Implementation Specifications

#### Backup Scheduler
```gdscript
# target/scripts/core/game_flow/persistence/backup_scheduler.gd
class_name BackupScheduler
extends RefCounted

enum BackupTrigger {
    MANUAL,
    TIMER_INTERVAL,
    GAME_EVENT,
    SHUTDOWN,
    ACHIEVEMENT,
    CAMPAIGN_COMPLETE
}

enum BackupFrequency {
    DISABLED,
    EVERY_HOUR,
    DAILY,
    WEEKLY,
    MONTHLY
}

# Scheduler configuration
var _backup_frequency: BackupFrequency = BackupFrequency.DAILY
var _backup_enabled: bool = true
var _max_automated_backups: int = 30
var _backup_on_events: bool = true

# Scheduling management
func initialize_scheduler() -> void:
    # Set up automatic backup timer
    _setup_backup_timer()
    
    # Connect to game events for smart triggers
    _connect_game_event_triggers()
    
    # Perform startup backup health check
    _perform_backup_health_check()
    
    scheduler_initialized.emit()

func schedule_backup(trigger: BackupTrigger, delay_seconds: float = 0.0) -> void:
    if not _backup_enabled:
        return
    
    if delay_seconds > 0.0:
        # Schedule delayed backup
        var timer = Timer.new()
        timer.wait_time = delay_seconds
        timer.one_shot = true
        timer.timeout.connect(func(): _execute_scheduled_backup(trigger))
        add_child(timer)
        timer.start()
    else:
        # Execute immediately
        _execute_scheduled_backup(trigger)

func _execute_scheduled_backup(trigger: BackupTrigger) -> void:
    var current_pilot = PilotManager.get_current_pilot()
    if not current_pilot:
        return
    
    # Create backup with trigger information
    var backup_name = _generate_backup_name(trigger)
    var backup_result = BackupManager.create_automated_backup(current_pilot, backup_name, trigger)
    
    if backup_result.success:
        backup_created.emit(backup_result.backup_path, trigger)
        print("Automated backup created: %s (trigger: %s)" % [backup_result.backup_path, BackupTrigger.keys()[trigger]])
        
        # Clean up old automated backups
        _cleanup_old_automated_backups()
    else:
        backup_failed.emit(backup_result.error_message, trigger)
        push_warning("Automated backup failed: %s" % backup_result.error_message)

# Smart backup triggers
func _connect_game_event_triggers() -> void:
    if not _backup_on_events:
        return
    
    # Connect to game events
    CampaignManager.campaign_completed.connect(func(campaign): schedule_backup(BackupTrigger.CAMPAIGN_COMPLETE))
    PilotAchievements.major_achievement_earned.connect(func(achievement): schedule_backup(BackupTrigger.ACHIEVEMENT))
    GameStateManager.state_changed.connect(_on_state_changed)

func _on_state_changed(from_state: GameStateManager.GameState, to_state: GameStateManager.GameState, data: Dictionary) -> void:
    # Backup on certain critical state transitions
    if to_state == GameStateManager.GameState.SHUTDOWN:
        schedule_backup(BackupTrigger.SHUTDOWN)

signal scheduler_initialized()
signal backup_created(backup_path: String, trigger: BackupTrigger)
signal backup_failed(error_message: String, trigger: BackupTrigger)
```

#### Recovery Assistant
```gdscript
# target/scripts/core/game_flow/persistence/recovery_assistant.gd
class_name RecoveryAssistant
extends RefCounted

enum RecoveryScenario {
    CORRUPTED_SAVE,
    MISSING_SAVE,
    PILOT_DATA_LOSS,
    CAMPAIGN_CORRUPTION,
    SETTINGS_RESET,
    COMPLETE_DATA_LOSS
}

# Recovery analysis and assistance
func analyze_recovery_situation() -> RecoveryAnalysis:
    var analysis = RecoveryAnalysis.new()
    
    # Check for current pilot and save data
    var current_pilot = PilotManager.get_current_pilot()
    analysis.has_current_pilot = current_pilot != null
    
    if current_pilot:
        # Check save file integrity
        var save_path = SaveGameManager.get_current_save_path()
        analysis.save_file_status = _analyze_save_file(save_path)
        
        # Check backup availability
        analysis.available_backups = BackupManager.find_backup_files(save_path)
        analysis.backup_count = analysis.available_backups.size()
    
    # Check for orphaned pilot files
    analysis.orphaned_pilots = _find_orphaned_pilot_files()
    
    # Determine recovery scenario
    analysis.primary_scenario = _determine_recovery_scenario(analysis)
    
    # Generate recovery recommendations
    analysis.recommendations = _generate_recovery_recommendations(analysis)
    
    return analysis

func start_recovery_wizard(scenario: RecoveryScenario) -> RecoveryWizard:
    var wizard = RecoveryWizard.new()
    wizard.scenario = scenario
    
    match scenario:
        RecoveryScenario.CORRUPTED_SAVE:
            wizard.steps = _create_corrupted_save_recovery_steps()
        RecoveryScenario.MISSING_SAVE:
            wizard.steps = _create_missing_save_recovery_steps()
        RecoveryScenario.PILOT_DATA_LOSS:
            wizard.steps = _create_pilot_recovery_steps()
        RecoveryScenario.CAMPAIGN_CORRUPTION:
            wizard.steps = _create_campaign_recovery_steps()
        RecoveryScenario.COMPLETE_DATA_LOSS:
            wizard.steps = _create_complete_recovery_steps()
        _:
            wizard.steps = _create_generic_recovery_steps()
    
    wizard.current_step = 0
    wizard.total_steps = wizard.steps.size()
    
    recovery_wizard_started.emit(wizard)
    return wizard

# Recovery operations
func attempt_automatic_recovery(save_path: String) -> RecoveryResult:
    var result = RecoveryResult.new()
    
    # Try backup recovery first
    var backup_result = BackupManager.restore_from_backup(save_path)
    if backup_result.success:
        result.success = true
        result.recovery_method = "backup_restore"
        result.recovered_from = backup_result.restored_from
        return result
    
    # Try save file repair
    var repair_result = _attempt_save_file_repair(save_path)
    if repair_result.success:
        result.success = true
        result.recovery_method = "file_repair"
        result.recovery_notes = repair_result.repair_notes
        return result
    
    # Try partial data recovery
    var partial_result = _attempt_partial_data_recovery(save_path)
    if partial_result.success:
        result.success = true
        result.recovery_method = "partial_recovery"
        result.recovery_notes = partial_result.recovered_components
        result.data_loss_warning = "Some data may have been lost during recovery"
        return result
    
    result.error_message = "All automatic recovery attempts failed"
    return result

func perform_guided_recovery(wizard: RecoveryWizard, user_choices: Dictionary) -> RecoveryResult:
    var result = RecoveryResult.new()
    
    # Execute recovery steps based on user choices
    for i in range(wizard.steps.size()):
        var step = wizard.steps[i]
        var choice = user_choices.get("step_%d" % i, "")
        
        var step_result = _execute_recovery_step(step, choice)
        if not step_result.success:
            result.error_message = "Recovery failed at step %d: %s" % [i + 1, step_result.error_message]
            return result
        
        result.recovery_notes += step_result.notes + "\n"
    
    result.success = true
    result.recovery_method = "guided_recovery"
    return result

signal recovery_wizard_started(wizard: RecoveryWizard)
signal recovery_completed(result: RecoveryResult)
signal recovery_failed(error_message: String)
```

#### Backup Health Monitor
```gdscript
# target/scripts/core/game_flow/persistence/backup_health_monitor.gd
class_name BackupHealthMonitor
extends RefCounted

# Health monitoring
func perform_comprehensive_health_check() -> HealthCheckReport:
    var report = HealthCheckReport.new()
    report.check_time = Time.get_unix_time_from_system()
    
    # Check all backup files
    var all_backups = _find_all_backup_files()
    report.total_backups = all_backups.size()
    
    for backup_path in all_backups:
        var backup_health = _check_backup_health(backup_path)
        report.backup_health_results.append(backup_health)
        
        match backup_health.status:
            BackupHealth.Status.HEALTHY:
                report.healthy_backups += 1
            BackupHealth.Status.CORRUPTED:
                report.corrupted_backups += 1
            BackupHealth.Status.SUSPICIOUS:
                report.suspicious_backups += 1
    
    # Generate health recommendations
    report.recommendations = _generate_health_recommendations(report)
    
    # Check backup coverage
    report.coverage_analysis = _analyze_backup_coverage()
    
    health_check_completed.emit(report)
    return report

func _check_backup_health(backup_path: String) -> BackupHealth:
    var health = BackupHealth.new()
    health.backup_path = backup_path
    health.file_size = _get_file_size(backup_path)
    health.modification_time = FileAccess.get_modified_time(backup_path)
    
    # Basic file accessibility
    if not FileAccess.file_exists(backup_path):
        health.status = BackupHealth.Status.MISSING
        health.issues.append("File does not exist")
        return health
    
    # File size validation
    if health.file_size < 1024:  # Suspiciously small
        health.status = BackupHealth.Status.SUSPICIOUS
        health.issues.append("File size unusually small: %d bytes" % health.file_size)
    
    # Load and validate backup data
    var save_data = load(backup_path)
    if not save_data:
        health.status = BackupHealth.Status.CORRUPTED
        health.issues.append("Cannot load backup data")
        return health
    
    if not save_data is SaveGameData:
        health.status = BackupHealth.Status.CORRUPTED
        health.issues.append("Invalid backup data format")
        return health
    
    # Data integrity validation
    if not save_data.is_valid():
        health.status = BackupHealth.Status.CORRUPTED
        health.issues.append("Backup data failed integrity validation")
        return health
    
    # All checks passed
    health.status = BackupHealth.Status.HEALTHY
    return health

# Backup repair attempts
func attempt_backup_repair(backup_path: String) -> RepairResult:
    var result = RepairResult.new()
    
    # Try to load backup with error tolerance
    var save_data = _load_backup_with_tolerance(backup_path)
    if not save_data:
        result.error_message = "Cannot load backup data for repair"
        return result
    
    # Attempt to repair data inconsistencies
    var repair_count = 0
    
    # Repair missing or invalid components
    if not save_data.pilot_profile:
        save_data.pilot_profile = _create_minimal_pilot_profile()
        repair_count += 1
        result.repairs_performed.append("Created minimal pilot profile")
    
    if not save_data.campaign_state:
        save_data.campaign_state = _create_minimal_campaign_state()
        repair_count += 1
        result.repairs_performed.append("Created minimal campaign state")
    
    # Recalculate checksums
    save_data._calculate_checksums()
    repair_count += 1
    result.repairs_performed.append("Recalculated data checksums")
    
    # Save repaired backup
    var repaired_path = backup_path + ".repaired"
    var save_error = ResourceSaver.save(save_data, repaired_path)
    
    if save_error == OK:
        result.success = true
        result.repaired_path = repaired_path
        result.total_repairs = repair_count
    else:
        result.error_message = "Failed to save repaired backup: " + error_string(save_error)
    
    return result

signal health_check_completed(report: HealthCheckReport)
signal backup_repaired(original_path: String, repaired_path: String, repairs: Array[String])
```

#### Manual Backup Tools
```gdscript
# target/scripts/core/game_flow/persistence/manual_backup_tools.gd
class_name ManualBackupTools
extends RefCounted

# Manual backup operations
func create_manual_backup(pilot: PilotProfile, backup_name: String, description: String = "") -> ManualBackupResult:
    var result = ManualBackupResult.new()
    
    # Validate inputs
    if not pilot or backup_name.is_empty():
        result.error_message = "Invalid pilot or backup name"
        return result
    
    # Create backup metadata
    var backup_metadata = BackupMetadata.new()
    backup_metadata.backup_name = backup_name
    backup_metadata.description = description
    backup_metadata.creation_time = Time.get_unix_time_from_system()
    backup_metadata.backup_type = "manual"
    backup_metadata.pilot_name = pilot.pilot_name
    backup_metadata.campaign_progress = _summarize_campaign_progress(pilot)
    
    # Create the backup
    var backup_result = BackupManager.create_backup_with_metadata(pilot, backup_metadata)
    if not backup_result.success:
        result.error_message = backup_result.error_message
        return result
    
    result.success = true
    result.backup_path = backup_result.backup_path
    result.metadata = backup_metadata
    
    manual_backup_created.emit(result)
    return result

func export_backup(backup_path: String, export_path: String) -> ExportResult:
    var result = ExportResult.new()
    
    # Validate backup file
    var validation_result = BackupValidator.validate_backup(backup_path)
    if not validation_result.is_valid:
        result.error_message = "Backup file is invalid or corrupted"
        return result
    
    # Create export package with metadata
    var export_data = {
        "backup_data": load(backup_path),
        "metadata": BackupManager.get_backup_metadata(backup_path),
        "export_time": Time.get_unix_time_from_system(),
        "export_version": "1.0"
    }
    
    # Save export package
    var save_error = ResourceSaver.save(export_data, export_path)
    if save_error != OK:
        result.error_message = "Failed to create export file: " + error_string(save_error)
        return result
    
    result.success = true
    result.export_path = export_path
    result.file_size = _get_file_size(export_path)
    
    backup_exported.emit(backup_path, export_path)
    return result

func import_backup(import_path: String) -> ImportResult:
    var result = ImportResult.new()
    
    # Load import package
    var import_data = load(import_path)
    if not import_data:
        result.error_message = "Cannot load import file"
        return result
    
    # Validate import data structure
    if not import_data.has("backup_data") or not import_data.has("metadata"):
        result.error_message = "Invalid import file format"
        return result
    
    # Install the backup
    var install_result = _install_imported_backup(import_data)
    if not install_result.success:
        result.error_message = install_result.error_message
        return result
    
    result.success = true
    result.installed_path = install_result.backup_path
    result.metadata = import_data["metadata"]
    
    backup_imported.emit(import_path, result.installed_path)
    return result

signal manual_backup_created(result: ManualBackupResult)
signal backup_exported(backup_path: String, export_path: String)
signal backup_imported(import_path: String, installed_path: String)
```

### File Structure
```
target/scripts/core/game_flow/persistence/
├── backup_scheduler.gd         # Automated backup scheduling
├── recovery_assistant.gd       # Recovery guidance and automation
├── backup_health_monitor.gd    # Backup integrity monitoring
├── manual_backup_tools.gd      # Manual backup operations
├── backup_metadata.gd          # Backup metadata structure
└── recovery_structures.gd      # Recovery-related data structures
```

## Definition of Done

- [ ] **Code Quality**: All code follows GDScript static typing standards
  - [ ] 100% static typing with comprehensive type annotations
  - [ ] Efficient backup processing with minimal performance impact
  - [ ] Robust error handling and user-friendly error messages
  - [ ] Background operations that don't block gameplay

- [ ] **Testing**: Comprehensive test coverage
  - [ ] Automated backup scheduling testing
  - [ ] Recovery scenario simulation and testing
  - [ ] Backup health monitoring validation
  - [ ] Manual backup tool functionality testing

- [ ] **Documentation**: Complete system documentation
  - [ ] Backup and recovery procedure documentation
  - [ ] Recovery wizard guide and troubleshooting
  - [ ] Backup health monitoring interpretation guide
  - [ ] Manual backup tool usage documentation

- [ ] **Integration**: Seamless integration with save system
  - [ ] Save game system integration for backup triggers
  - [ ] UI integration for recovery assistant
  - [ ] Settings integration for backup configuration
  - [ ] Error reporting integration

## Implementation Notes

### Backup Strategy Design
- Implement intelligent backup scheduling based on game events
- Provide multiple backup retention policies
- Support both automated and manual backup operations
- Include backup health monitoring and repair capabilities

### Recovery System Design
- Create user-friendly recovery wizards for common scenarios
- Implement automatic recovery detection and suggestions
- Support partial data recovery for maximum data preservation
- Provide clear recovery status and progress reporting

### Performance Considerations
- Use background operations for backup creation
- Implement incremental backup strategies where possible
- Monitor backup storage usage and provide cleanup recommendations
- Optimize backup validation for minimal performance impact

## Dependencies

### Prerequisite Stories
- **FLOW-008**: Save Game System and Data Persistence

### Dependent Stories
- None (this is an enhancement to the core save system)

## Testing Strategy

### Unit Tests
```gdscript
# test_backup_scheduler.gd
func test_automated_backup_scheduling():
    # Test backup scheduling and trigger mechanisms
    
func test_backup_cleanup():
    # Test automatic cleanup of old backups

# test_recovery_assistant.gd
func test_recovery_scenario_detection():
    # Test recovery scenario analysis
    
func test_guided_recovery():
    # Test recovery wizard functionality

# test_backup_health_monitor.gd
func test_backup_validation():
    # Test backup integrity checking
    
func test_health_reporting():
    # Test health check reporting
```

### Integration Tests
- End-to-end backup and recovery testing
- Recovery scenario simulation with corrupted data
- Backup health monitoring under various conditions
- Manual backup tool integration testing

---

**Story Ready for Implementation**: ✅  
**Architecture Reference**: Approved EPIC-007 architecture document  
**WCS Source Reference**: Data backup and recovery mechanisms  
**Integration Complexity**: Medium - Extends save system with additional protection  
**Estimated Development Time**: 2-3 days for experienced GDScript developer