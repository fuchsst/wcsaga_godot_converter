# FLOW-007: Pilot Management and Statistics

**Epic**: EPIC-007 - Overall Game Flow & State Management  
**Phase**: 3 - Player Data and Persistence  
**Story ID**: FLOW-007  
**Story Name**: Pilot Management and Statistics  
**Assigned**: Dev (GDScript Developer)  
**Status**: COMPLETED ✅  
**Story Points**: 7  
**Priority**: High  

---

## User Story

**As a** player  
**I want** comprehensive pilot profiles with detailed statistics and career progression tracking  
**So that** I can monitor my performance, achievements, and progress across campaigns and missions  

## Story Description

Enhance the existing pilot management and statistics system using the comprehensive PlayerProfile resource (`addons/wcs_asset_core/resources/player/player_profile.gd`) and PilotStatistics resource (`addons/wcs_asset_core/resources/player/pilot_statistics.gd`) already implemented. This story focuses on extending the existing resources with additional performance tracking features and integrating with the established SaveGameManager system for reliable data persistence.

## Acceptance Criteria

- [ ] **Enhanced Pilot Profile Management**: Extend existing PlayerProfile resource system
  - [ ] Leverage existing PlayerProfile from `addons/wcs_asset_core/resources/player/player_profile.gd`
  - [ ] Extend existing PilotStatistics from `addons/wcs_asset_core/resources/player/pilot_statistics.gd`
  - [ ] Integrate with existing SaveGameManager from `addons/wcs_asset_core/autoload/save_game_manager.gd`
  - [ ] Use established validation patterns from existing resources

- [ ] **Statistics Tracking**: Comprehensive performance and career statistics
  - [ ] Mission-level statistics (kills, deaths, accuracy, score)
  - [ ] Career-level statistics (total missions, campaigns completed, flight time)
  - [ ] Real-time statistics updates during mission gameplay
  - [ ] Historical statistics with mission-by-mission breakdown

- [ ] **Achievement and Medal System**: Progress recognition and awards
  - [ ] Medal earning based on performance criteria
  - [ ] Achievement tracking for specific accomplishments
  - [ ] Rank progression based on experience and performance
  - [ ] Achievement notification and award ceremonies

- [ ] **Data Persistence**: Reliable pilot data storage and retrieval
  - [ ] Atomic save operations with backup and recovery
  - [ ] Data integrity validation and corruption detection
  - [ ] Export/import capabilities for pilot sharing or backup
  - [ ] Migration support for save format updates

## Technical Requirements

### Architecture Reference
- **Architecture Document**: `EPIC-007-overall-game-flow-state-management/architecture.md` (lines 46-52, Player Data System)
- **WCS Analysis**: `playerman/managepilot.cpp` - Comprehensive pilot management system
- **Existing Resources**: PlayerProfile (`addons/wcs_asset_core/resources/player/player_profile.gd`), PilotStatistics (`addons/wcs_asset_core/resources/player/pilot_statistics.gd`)
- **Integration**: Extend existing SaveGameManager autoload and PlayerProfile resource patterns

### Implementation Specifications

#### Enhanced PilotStatistics (Extend Existing Resource)
```gdscript
# Extension of existing PilotStatistics from addons/wcs_asset_core/resources/player/pilot_statistics.gd
# The existing resource already provides comprehensive statistics tracking
# Focus on extending with additional mission performance history and weapon accuracy

# New methods to add to existing PilotStatistics resource:
func get_mission_performance_history() -> Array[Dictionary]:
    # Return array of mission performance data for historical tracking
    return mission_scores.map(func(score): return {"score": score, "timestamp": Time.get_unix_time_from_system()})

func get_weapon_accuracy_breakdown() -> Dictionary:
    # Calculate detailed accuracy statistics
    return {
        "overall_accuracy": get_accuracy_percentage(),
        "shots_fired": shots_fired,
        "shots_hit": shots_hit,
        "damage_per_shot": damage_dealt / max(1, shots_fired)
    }

# Integration with existing PlayerProfile from addons/wcs_asset_core/resources/player/player_profile.gd
func update_pilot_performance(mission_result: MissionResult) -> void:
    # Use existing pilot_stats.record_mission_performance() method
    # The PlayerProfile already has comprehensive statistics tracking

# Pilot management using existing PlayerProfile resource
func create_pilot_profile(pilot_name: String, callsign: String) -> PlayerProfile:
    # Use existing PlayerProfile from addons/wcs_asset_core/resources/player/player_profile.gd
    var pilot_profile: PlayerProfile = PlayerProfile.new()
    
    # Set callsign using existing method
    pilot_profile.set_callsign(callsign)
    
    # The PlayerProfile already handles:
    # - pilot_stats (PilotStatistics resource)
    # - campaigns (Array of CampaignProgress)
    # - hotkey_config (HotkeyConfiguration)
    # - player_configuration (PlayerConfiguration)
    # - Validation via validate_profile()
    
    # Save using existing SaveGameManager
    var success: bool = SaveGameManager.save_player_profile(pilot_profile)
    if not success:
        push_error("Failed to save pilot profile: %s" % callsign)
        return null
    
    return pilot_profile

func load_pilot_profile(save_slot: int) -> PlayerProfile:
    # Use existing SaveGameManager to load PlayerProfile
    var pilot_profile: PlayerProfile = SaveGameManager.load_player_profile(save_slot)
    if not pilot_profile:
        push_error("Failed to load pilot profile from slot: %d" % save_slot)
        return null
    
    # Validate using existing PlayerProfile validation
    var validation_result: Dictionary = pilot_profile.validate_profile()
    if not validation_result.is_valid:
        push_error("Pilot profile validation failed: %s" % validation_result.error)
        return null
    
    # The PlayerProfile already handles all necessary data and validation
    return pilot_profile

func save_pilot_profile(pilot_profile: PlayerProfile, save_slot: int) -> bool:
    # Use existing SaveGameManager for atomic save operations
    var success: bool = SaveGameManager.save_player_profile(pilot_profile, save_slot)
    if not success:
        push_error("Failed to save pilot profile to slot: %d" % save_slot)
        return false
    
    # SaveGameManager already handles:
    # - Atomic save operations
    # - Backup creation
    # - Validation
    # - Error recovery
    
    return true

# Statistics management using existing PilotStatistics
func update_mission_statistics(pilot_profile: PlayerProfile, mission_result: MissionResult, save_slot: int) -> void:
    if not pilot_profile or not pilot_profile.pilot_stats:
        push_warning("No pilot profile or statistics available")
        return
    
    # Use existing PilotStatistics.record_mission_performance() method
    pilot_profile.pilot_stats.record_mission_performance(mission_result)
    
    # Update experience and rank using existing PlayerProfile methods
    pilot_profile.add_experience(mission_result.get("experience_points", 0))
    
    # Save using existing SaveGameManager
    var success: bool = save_pilot_profile(pilot_profile, save_slot)
    if success:
        statistics_updated.emit(pilot_profile, mission_result)

# Signals for pilot management events
signal pilot_profile_created(pilot_profile: PlayerProfile)
signal pilot_profile_loaded(pilot_profile: PlayerProfile)
signal pilot_profile_saved(pilot_profile: PlayerProfile, save_slot: int)
signal statistics_updated(pilot_profile: PlayerProfile, mission_result: MissionResult)
```

#### Using Existing PlayerProfile Resource
```gdscript
# The PlayerProfile resource already exists at:
# addons/wcs_asset_core/resources/player/player_profile.gd
# 
# It provides comprehensive functionality including:
# - callsign management with set_callsign() method
# - pilot_stats (PilotStatistics resource) for all statistics tracking
# - campaigns (Array[CampaignProgress]) for campaign progression
# - hotkey_config (HotkeyConfiguration) for control customization
# - player_configuration (PlayerConfiguration) for game settings
# - validate_profile() method for data integrity checking
# - Signals: profile_changed, campaign_changed, statistics_updated

# Usage example:
func create_new_pilot(callsign: String) -> PlayerProfile:
    var profile: PlayerProfile = PlayerProfile.new()
    profile.set_callsign(callsign)
    
    # PlayerProfile automatically initializes:
    # - pilot_stats with PilotStatistics resource
    # - campaigns array for campaign tracking
    # - hotkey_config with default controls
    # - player_configuration with default settings
    
    return profile

func update_pilot_statistics(profile: PlayerProfile, mission_data: Dictionary) -> void:
    # Use existing PilotStatistics methods
    if profile.pilot_stats:
        profile.pilot_stats.record_mission_performance(mission_data)
        # PilotStatistics already tracks:
        # - total_score, missions_completed, campaigns_completed
        # - kills, deaths, accuracy, flight_time
        # - detailed performance metrics
```

#### Using Existing PilotStatistics Resource
```gdscript
# The PilotStatistics resource already exists at:
# addons/wcs_asset_core/resources/player/pilot_statistics.gd
# 
# It provides comprehensive statistics tracking including:
# - Mission statistics: total_score, missions_completed, campaigns_completed
# - Combat tracking: kills, deaths, accuracy calculations  
# - Performance metrics: flight_time, scores, rankings
# - Achievement integration with kill tracking and performance analysis
# - record_mission_performance() method for updating statistics

# Usage with existing resource:
func update_pilot_performance(pilot_profile: PlayerProfile, mission_result: Dictionary) -> void:
    if not pilot_profile.pilot_stats:
        push_error("No pilot statistics available")
        return
    
    # Use existing PilotStatistics.record_mission_performance()
    pilot_profile.pilot_stats.record_mission_performance(mission_result)
    
    # The existing PilotStatistics already provides:
    # - All mission and combat statistics tracking
    # - Score calculations and averaging
    # - Performance analysis methods
    # - Integration with achievement system
    
    # Emit statistics update signal
    pilot_profile.statistics_updated.emit()

# Extended methods to add to existing PilotStatistics:
func get_detailed_performance_summary() -> Dictionary:
    return {
        "accuracy": get_accuracy_percentage(),
        "survival_rate": get_survival_percentage(), 
        "average_score": get_average_score(),
        "total_flight_time": get_total_flight_time(),
        "kill_breakdown": get_kill_breakdown(),
        "mission_completion": get_completion_percentage()
    }
```

#### Achievement Integration with Existing Systems
```gdscript
# Achievement tracking can integrate with existing PilotStatistics resource
# Create achievement manager that works with existing pilot data

class_name AchievementManager
extends Node

# Achievement tracking for pilot progression
signal achievement_earned(achievement_id: String, pilot_profile: PlayerProfile)
signal medal_awarded(medal_id: String, pilot_profile: PlayerProfile)

# Check achievements using existing PilotStatistics data
func check_pilot_achievements(pilot_profile: PlayerProfile) -> Array[String]:
    var new_achievements: Array[String] = []
    
    if not pilot_profile.pilot_stats:
        return new_achievements
    
    var stats: PilotStatistics = pilot_profile.pilot_stats
    
    # Use existing statistics methods for achievement checking
    if stats.get_total_kills() >= 100:
        new_achievements.append("centurion")
    
    if stats.get_missions_completed() >= 50:
        new_achievements.append("veteran_pilot")
    
    if stats.get_accuracy_percentage() >= 85.0:
        new_achievements.append("marksman")
    
    if stats.get_survival_percentage() >= 95.0:
        new_achievements.append("survivor")
    
    # Check against existing achievements to avoid duplicates
    # This could be stored in PlayerProfile as additional data
    var existing_achievements: Array = pilot_profile.get_meta("achievements", [])
    
    for achievement in new_achievements:
        if achievement not in existing_achievements:
            existing_achievements.append(achievement)
            pilot_profile.set_meta("achievements", existing_achievements)
            achievement_earned.emit(achievement, pilot_profile)
    
    return new_achievements

# Medal system based on comprehensive performance
func check_pilot_medals(pilot_profile: PlayerProfile) -> Array[String]:
    var stats: PilotStatistics = pilot_profile.pilot_stats
    if not stats:
        return []
    
    var new_medals: Array[String] = []
    var existing_medals: Array = pilot_profile.get_meta("medals", [])
    
    # Use existing statistical methods for medal criteria
    if stats.get_total_score() >= 50000 and "ace_pilot" not in existing_medals:
        new_medals.append("ace_pilot")
    
    if stats.get_campaigns_completed() >= 3 and "campaign_veteran" not in existing_medals:
        new_medals.append("campaign_veteran")
    
    # Award new medals
    for medal in new_medals:
        existing_medals.append(medal)
        pilot_profile.set_meta("medals", existing_medals)
        medal_awarded.emit(medal, pilot_profile)
    
    return new_medals
```

### File Structure (Using Existing Resources)
```
# Existing Resources (Already Implemented):
addons/wcs_asset_core/resources/player/
├── player_profile.gd           # Comprehensive pilot profile (EXISTING)
├── pilot_statistics.gd         # Complete statistics tracking (EXISTING)
├── hotkey_configuration.gd     # Control configuration (EXISTING)
└── player_configuration.gd     # Game settings (EXISTING)

addons/wcs_asset_core/autoload/
└── save_game_manager.gd        # Atomic save/load operations (EXISTING)

# New Extensions for FLOW-007:
target/scripts/core/game_flow/player_data/
├── achievement_manager.gd      # Achievement and medal system (NEW)
├── pilot_performance_tracker.gd # Extended performance analysis (NEW)
└── pilot_data_coordinator.gd   # Integration coordinator (NEW)
```

## Definition of Done

- [ ] **Code Quality**: All code follows GDScript static typing standards
  - [ ] 100% static typing with comprehensive type annotations
  - [ ] Efficient statistics calculation and storage
  - [ ] Proper error handling for data corruption
  - [ ] Memory-efficient data structures

- [ ] **Testing**: Comprehensive test coverage
  - [ ] Pilot creation and management testing
  - [ ] Statistics tracking and calculation testing
  - [ ] Achievement and medal earning testing
  - [ ] Data persistence and recovery testing

- [ ] **Documentation**: Complete system documentation
  - [ ] Pilot management API documentation
  - [ ] Statistics calculation documentation
  - [ ] Achievement system design documentation
  - [ ] Data recovery procedures

- [ ] **Integration**: Seamless integration with game systems
  - [ ] Session management integration for pilot tracking
  - [ ] Mission system integration for statistics
  - [ ] Save system integration for persistence
  - [ ] UI integration for pilot selection and display

## Implementation Notes

### Statistics Design
- Use efficient data structures for statistics tracking
- Implement real-time statistics updates during missions
- Support historical statistics with mission-by-mission breakdown
- Include performance metrics for analysis

### Achievement System Design
- Create flexible achievement criteria system
- Support both mission-based and career-based achievements
- Implement progressive achievements with multiple tiers
- Include special achievements for unique accomplishments

### Data Persistence Strategy
- Use atomic save operations to prevent corruption
- Implement backup and recovery mechanisms
- Support pilot data export/import for sharing
- Include data migration for save format updates

## Dependencies

### Prerequisite Stories
- **EPIC-001**: Data Migration Foundation (PlayerProfile and SaveGameManager already implemented)
- **FLOW-001**: Game State Manager Core Implementation
- **FLOW-003**: Session Management and Lifecycle

### Dependent Stories
- **FLOW-010**: Mission Scoring and Performance Tracking (statistics source)
- **FLOW-011**: Achievement and Medal System (achievement integration)

## Testing Strategy

### Unit Tests
```gdscript
# test_pilot_manager.gd
func test_pilot_creation():
    # Test pilot profile creation and validation
    
func test_pilot_loading():
    # Test pilot loading and data integrity

# test_pilot_statistics.gd
func test_mission_statistics_recording():
    # Test statistics updates from mission results
    
func test_calculated_statistics():
    # Test derived statistics calculations

# test_pilot_achievements.gd
func test_achievement_earning():
    # Test achievement criteria and earning
    
func test_medal_system():
    # Test medal earning and progression
```

### Integration Tests
- End-to-end pilot management testing
- Statistics integration with mission system
- Achievement system integration testing
- Data persistence and recovery testing

---

**Story Ready for Implementation**: ✅  
**Architecture Reference**: Approved EPIC-007 architecture document  
**WCS Source Reference**: `playerman/managepilot.cpp` pilot management system  
**Integration Complexity**: Medium-High - Multiple data systems coordination  
**Estimated Development Time**: 3-4 days for experienced GDScript developer