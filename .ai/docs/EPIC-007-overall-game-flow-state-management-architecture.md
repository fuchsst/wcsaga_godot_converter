# EPIC-007: Overall Game Flow & State Management - Architecture

**Document Version**: 1.0  
**Date**: 2025-01-26  
**Architect**: Mo (Godot Architect)  
**Epic**: EPIC-007 - Overall Game Flow & State Management  
**System**: Game state management, campaign progression, save/load, session control  
**Approval Status**: PENDING (SallySM)  

---

## Architecture Philosophy (Mo's Principles)

> **"Game state is the spine of WCS - it must be robust, predictable, and never lose player progress."**
> 
> This architecture creates a bulletproof state management system using finite state machines, robust persistence, and comprehensive error recovery to ensure players never lose progress.

### Core Design Principles

1. **State Machine Driven**: Clear state definitions with validated transitions
2. **Atomic Operations**: Save operations are atomic - they succeed completely or fail safely
3. **Progressive Backup**: Multiple save layers prevent data loss
4. **Error Recovery**: Graceful handling of corruption and unexpected shutdowns
5. **Event-Driven Design**: State changes trigger events for loose system coupling
6. **Performance Monitored**: State operations are fast and non-blocking

## System Architecture Overview

```
Game Flow & State Management
├── Core State Machine                 # Central game state control
│   ├── GameStateManager              # Main state machine coordination
│   ├── StateDefinitions              # State enumeration and validation
│   ├── TransitionManager             # State transition logic and rules
│   └── StateValidator                # State consistency checking
├── Session Management                 # Game session lifecycle
│   ├── GameSession                   # Current session data and control
│   ├── SessionPersistence            # Session save/load operations
│   ├── CrashRecovery                 # Recovery from unexpected shutdowns
│   └── AutoSaveManager               # Automatic save coordination
├── Campaign System                    # Campaign progression and branching
│   ├── CampaignManager               # Campaign state and progression
│   ├── CampaignParser                # Campaign file parsing and validation
│   ├── MissionUnlocking              # Mission availability logic
│   ├── BranchingLogic                # Story branching and choice handling
│   └── CampaignVariables             # Campaign-wide variable management
├── Player Data System                 # Pilot and player management
│   ├── PilotManager                  # Pilot creation and management
│   ├── PilotStatistics               # Statistics tracking and calculation
│   ├── PilotPersistence              # Pilot file save/load operations
│   ├── ProgressionTracker            # Skill and career progression
│   └── MedalSystem                   # Medal and achievement management
├── Save System                        # Data persistence framework
│   ├── SaveGameManager               # Save game creation and loading
│   ├── DataSerialization             # Data format and versioning
│   ├── BackupManager                 # Backup creation and management
│   └── IntegrityChecker              # Save file validation and repair
└── Performance & Monitoring           # System monitoring and optimization
    ├── StatePerformanceMonitor       # State operation performance tracking
    ├── MemoryManager                 # Memory usage optimization
    ├── ErrorReporter                 # Comprehensive error reporting
    └── AnalyticsCollector            # Usage analytics and metrics
```

## State Machine Architecture

```gdscript
# Main Game State Manager
class_name GameStateManager
extends Node

# Game states enumeration
enum GameState {
    STARTUP,                    # Initial game loading
    MAIN_MENU,                 # Main menu and navigation
    PILOT_SELECTION,           # Pilot management
    CAMPAIGN_SELECTION,        # Campaign browsing
    MISSION_BRIEFING,          # Pre-mission briefing
    SHIP_SELECTION,            # Ship and loadout selection
    MISSION_LOADING,           # Mission initialization
    IN_MISSION,                # Active mission gameplay
    MISSION_PAUSED,            # Mission paused state
    MISSION_COMPLETE,          # Mission completion processing
    MISSION_DEBRIEFING,        # Post-mission debriefing
    CAMPAIGN_COMPLETE,         # Campaign completion
    OPTIONS,                   # Settings and configuration
    SHUTDOWN                   # Game exit and cleanup
}

# State management
var current_state: GameState = GameState.STARTUP
var previous_state: GameState = GameState.STARTUP
var state_history: Array[GameState] = []

# State transition system
func transition_to_state(new_state: GameState, data: Dictionary = {}) -> bool:
    if not _is_valid_transition(current_state, new_state):
        push_error("Invalid state transition: %s -> %s" % [GameState.keys()[current_state], GameState.keys()[new_state]])
        return false
    
    # Execute transition
    var transition_result = _execute_state_transition(current_state, new_state, data)
    if transition_result.success:
        _update_state(new_state)
        state_changed.emit(previous_state, current_state, data)
        return true
    else:
        push_error("State transition failed: " + transition_result.error_message)
        return false

signal state_changed(from_state: GameState, to_state: GameState, data: Dictionary)

# State validation and transition rules
func _is_valid_transition(from_state: GameState, to_state: GameState) -> bool:
    # Define valid state transitions
    var valid_transitions = {
        GameState.STARTUP: [GameState.MAIN_MENU],
        GameState.MAIN_MENU: [GameState.PILOT_SELECTION, GameState.OPTIONS, GameState.SHUTDOWN],
        GameState.PILOT_SELECTION: [GameState.MAIN_MENU, GameState.CAMPAIGN_SELECTION],
        GameState.CAMPAIGN_SELECTION: [GameState.PILOT_SELECTION, GameState.MISSION_BRIEFING],
        GameState.MISSION_BRIEFING: [GameState.CAMPAIGN_SELECTION, GameState.SHIP_SELECTION],
        GameState.SHIP_SELECTION: [GameState.MISSION_BRIEFING, GameState.MISSION_LOADING],
        GameState.MISSION_LOADING: [GameState.IN_MISSION, GameState.MAIN_MENU],  # Allow fallback on load failure
        GameState.IN_MISSION: [GameState.MISSION_PAUSED, GameState.MISSION_COMPLETE, GameState.MAIN_MENU],
        GameState.MISSION_PAUSED: [GameState.IN_MISSION, GameState.MAIN_MENU],
        GameState.MISSION_COMPLETE: [GameState.MISSION_DEBRIEFING],
        GameState.MISSION_DEBRIEFING: [GameState.CAMPAIGN_SELECTION, GameState.CAMPAIGN_COMPLETE],
        GameState.CAMPAIGN_COMPLETE: [GameState.MAIN_MENU],
        GameState.OPTIONS: [previous_state],  # Return to previous state
        GameState.SHUTDOWN: []  # No transitions from shutdown
    }
    
    return to_state in valid_transitions.get(from_state, [])
```

## Save System Architecture

```gdscript
# Save Game Manager
class_name SaveGameManager
extends RefCounted

# Save game structure
class_name SaveGameData
extends Resource

@export var save_version: int = 1
@export var creation_timestamp: int
@export var pilot_profile: PilotProfile
@export var campaign_state: CampaignState
@export var mission_progress: MissionProgress
@export var game_settings: GameSettings
@export var session_data: SessionData

# Save operations
func save_game(pilot: PilotProfile, save_slot: int = -1) -> SaveResult:
    var save_data = SaveGameData.new()
    save_data.creation_timestamp = Time.get_unix_time_from_system()
    save_data.pilot_profile = pilot
    save_data.campaign_state = CampaignManager.get_current_state()
    save_data.mission_progress = MissionManager.get_progress()
    save_data.game_settings = OptionsManager.get_current_settings()
    save_data.session_data = SessionManager.get_session_data()
    
    # Determine save path
    var save_path: String
    if save_slot >= 0:
        save_path = "user://saves/slot_%d.save" % save_slot
    else:
        save_path = "user://saves/autosave.save"
    
    # Atomic save operation
    return _perform_atomic_save(save_data, save_path)

func _perform_atomic_save(save_data: SaveGameData, save_path: String) -> SaveResult:
    var result = SaveResult.new()
    
    # Create backup of existing save
    if FileAccess.file_exists(save_path):
        var backup_path = save_path + ".backup"
        _copy_file(save_path, backup_path)
    
    # Write to temporary file first
    var temp_path = save_path + ".tmp"
    var save_error = ResourceSaver.save(save_data, temp_path)
    
    if save_error == OK:
        # Verify the save file
        var verification_result = _verify_save_file(temp_path)
        if verification_result.is_valid:
            # Atomic move from temp to final location
            var dir = DirAccess.open("user://saves/")
            var move_error = dir.rename(temp_path, save_path)
            if move_error == OK:
                result.success = true
                result.save_path = save_path
            else:
                result.error_message = "Failed to finalize save file"
        else:
            result.error_message = "Save file verification failed: " + verification_result.error_message
    else:
        result.error_message = "Failed to write save file: " + error_string(save_error)
    
    # Cleanup temp file if it exists
    if FileAccess.file_exists(temp_path):
        DirAccess.remove_absolute(temp_path)
    
    return result

# Save file verification
func _verify_save_file(file_path: String) -> VerificationResult:
    var result = VerificationResult.new()
    
    # Load and verify the save file
    var save_data = load(file_path)
    if not save_data:
        result.error_message = "Cannot load save file"
        return result
    
    if not save_data is SaveGameData:
        result.error_message = "Save file is not valid SaveGameData"
        return result
    
    # Verify required fields
    if not save_data.pilot_profile:
        result.error_message = "Save file missing pilot profile"
        return result
    
    if not save_data.campaign_state:
        result.error_message = "Save file missing campaign state"
        return result
    
    result.is_valid = true
    return result
```

## Campaign Progression Architecture

```gdscript
# Campaign Manager
class_name CampaignManager
extends RefCounted

# Campaign state tracking
class_name CampaignState
extends Resource

@export var campaign_id: String
@export var current_mission: String
@export var missions_completed: Array[String] = []
@export var missions_available: Array[String] = []
@export var campaign_variables: Dictionary = {}
@export var story_branch_choices: Dictionary = {}
@export var completion_percentage: float = 0.0

# Mission unlocking logic
func update_mission_availability(completed_mission: String) -> void:
    if completed_mission in missions_completed:
        return  # Already processed
    
    missions_completed.append(completed_mission)
    
    # Check which missions become available
    var newly_available = _calculate_newly_available_missions(completed_mission)
    for mission_id in newly_available:
        if mission_id not in missions_available:
            missions_available.append(mission_id)
    
    # Update completion percentage
    _update_completion_percentage()
    
    # Trigger progression events
    mission_completed.emit(completed_mission, newly_available)

func _calculate_newly_available_missions(completed_mission: String) -> Array[String]:
    var newly_available: Array[String] = []
    var campaign_data = _get_campaign_data()
    
    for mission_def in campaign_data.missions:
        if mission_def.id in missions_available:
            continue  # Already available
        
        # Check if prerequisites are met
        if _are_prerequisites_met(mission_def.prerequisites):
            newly_available.append(mission_def.id)
    
    return newly_available

# Story branching system
func record_story_choice(choice_id: String, choice_value: Variant) -> void:
    story_branch_choices[choice_id] = choice_value
    
    # Check if this choice affects mission availability
    _evaluate_story_branches()
    
    story_choice_made.emit(choice_id, choice_value)

signal mission_completed(mission_id: String, newly_available: Array[String])
signal story_choice_made(choice_id: String, choice_value: Variant)
```

## Session Management Architecture

```gdscript
# Game Session Manager
class_name GameSession
extends RefCounted

# Session data structure
class_name SessionData
extends Resource

@export var session_id: String
@export var start_time: int
@export var last_save_time: int
@export var current_mission_state: MissionState
@export var temp_variables: Dictionary = {}
@export var ui_state: Dictionary = {}

# Session lifecycle
var current_session: SessionData

func start_new_session(pilot: PilotProfile) -> void:
    current_session = SessionData.new()
    current_session.session_id = _generate_session_id()
    current_session.start_time = Time.get_unix_time_from_system()
    current_session.last_save_time = current_session.start_time
    
    # Initialize session state
    _initialize_session_state(pilot)
    
    session_started.emit(current_session)

func end_session() -> void:
    if current_session:
        # Perform final save
        _perform_session_cleanup()
        session_ended.emit(current_session)
        current_session = null

# Auto-save management
func setup_autosave(interval_minutes: float = 5.0) -> void:
    var timer = Timer.new()
    timer.wait_time = interval_minutes * 60.0
    timer.timeout.connect(_perform_autosave)
    timer.autostart = true
    add_child(timer)

func _perform_autosave() -> void:
    if current_session and _should_autosave():
        var pilot = PilotManager.get_current_pilot()
        var save_result = SaveGameManager.save_game(pilot, -1)  # -1 for autosave
        if save_result.success:
            current_session.last_save_time = Time.get_unix_time_from_system()
            autosave_completed.emit(save_result.save_path)
        else:
            autosave_failed.emit(save_result.error_message)

signal session_started(session: SessionData)
signal session_ended(session: SessionData)
signal autosave_completed(save_path: String)
signal autosave_failed(error_message: String)
```

## Error Recovery Architecture

```gdscript
# Crash Recovery System
class_name CrashRecoveryManager
extends RefCounted

# Recovery data structure
class_name RecoveryData
extends Resource

@export var crash_timestamp: int
@export var game_state: int  # GameState enum value
@export var pilot_profile: PilotProfile
@export var session_data: SessionData
@export var error_log: String

# Crash detection and recovery
func check_for_crash_recovery() -> bool:
    var recovery_file = "user://crash_recovery.dat"
    if FileAccess.file_exists(recovery_file):
        var recovery_data = load(recovery_file)
        if recovery_data and recovery_data is RecoveryData:
            _offer_crash_recovery(recovery_data)
            return true
    return false

func _offer_crash_recovery(recovery_data: RecoveryData) -> void:
    # Show recovery dialog to user
    var dialog = preload("res://scenes/ui/crash_recovery_dialog.tscn").instantiate()
    dialog.setup_recovery_data(recovery_data)
    dialog.recovery_accepted.connect(_perform_crash_recovery)
    dialog.recovery_declined.connect(_clear_recovery_data)
    get_tree().current_scene.add_child(dialog)

func _perform_crash_recovery(recovery_data: RecoveryData) -> void:
    # Restore game state
    GameStateManager.force_state(recovery_data.game_state)
    PilotManager.load_pilot_from_data(recovery_data.pilot_profile)
    SessionManager.restore_session(recovery_data.session_data)
    
    # Clear recovery data
    _clear_recovery_data()
    
    crash_recovery_completed.emit()

# Create recovery checkpoint
func create_recovery_checkpoint() -> void:
    var recovery_data = RecoveryData.new()
    recovery_data.crash_timestamp = Time.get_unix_time_from_system()
    recovery_data.game_state = GameStateManager.current_state
    recovery_data.pilot_profile = PilotManager.get_current_pilot()
    recovery_data.session_data = SessionManager.current_session
    
    var recovery_file = "user://crash_recovery.dat"
    ResourceSaver.save(recovery_data, recovery_file)

signal crash_recovery_completed()
```

## Performance Monitoring

```gdscript
# State Performance Monitor
class_name StatePerformanceMonitor
extends RefCounted

# Performance metrics
var _state_transition_times: Dictionary = {}
var _save_operation_times: Array[float] = []
var _load_operation_times: Array[float] = []

func track_state_transition(from_state: GameStateManager.GameState, to_state: GameStateManager.GameState, duration_ms: float) -> void:
    var transition_key = "%s->%s" % [GameStateManager.GameState.keys()[from_state], GameStateManager.GameState.keys()[to_state]]
    if not _state_transition_times.has(transition_key):
        _state_transition_times[transition_key] = []
    _state_transition_times[transition_key].append(duration_ms)

func track_save_operation(duration_ms: float) -> void:
    _save_operation_times.append(duration_ms)
    if _save_operation_times.size() > 100:  # Keep last 100 saves
        _save_operation_times.pop_front()

func get_performance_report() -> Dictionary:
    return {
        "average_state_transition_times": _calculate_average_transition_times(),
        "average_save_time_ms": _calculate_average(_save_operation_times),
        "average_load_time_ms": _calculate_average(_load_operation_times),
        "slowest_operations": _get_slowest_operations()
    }
```

---

**Critical Features:**
- **Robust State Machine**: Validated state transitions with error recovery
- **Atomic Saves**: Complete success or safe failure with backup systems
- **Campaign Progression**: Mission unlocking and story branching logic
- **Crash Recovery**: Automatic recovery from unexpected shutdowns

**Integration Points:**
- EPIC-006: Menu & Navigation System (state-driven navigation)
- EPIC-004: SEXP Expression System (campaign variables)
- EPIC-002: Asset Structures (pilot and campaign data)
- All Game Systems: State-aware initialization and cleanup

**Next Steps:**
1. State transition diagram and validation rules
2. Save file format specification and versioning
3. Campaign progression testing framework
4. Performance benchmarking and optimization