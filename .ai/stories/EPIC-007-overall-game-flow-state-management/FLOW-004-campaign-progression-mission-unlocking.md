# FLOW-004: Campaign Progression and Mission Unlocking

**Epic**: EPIC-007 - Overall Game Flow & State Management  
**Phase**: 2 - Campaign and Mission Flow  
**Story ID**: FLOW-004  
**Story Name**: Campaign Progression and Mission Unlocking  
**Assigned**: Dev (GDScript Developer)  
**Status**: COMPLETED ✅  
**Story Points**: 8  
**Priority**: High  

---

## User Story

**As a** player  
**I want** campaign progression that tracks my mission completion and unlocks appropriate content  
**So that** I can experience the story progression and access new missions based on my performance and choices  

## Story Description

Implement a comprehensive campaign progression system that manages mission completion tracking, unlocks missions based on prerequisite completion and story choices, and maintains campaign state across game sessions. This system replicates the WCS campaign branching logic with mission dependencies and conditional unlocking.

## Acceptance Criteria

- [ ] **Campaign State Management**: Complete campaign progression tracking
  - [ ] Campaign loading and initialization from campaign files
  - [ ] Mission completion status tracking with detailed results
  - [ ] Campaign progress percentage calculation and display
  - [ ] Support for multiple concurrent campaigns per pilot

- [ ] **Mission Unlocking Logic**: Sophisticated mission availability system
  - [ ] Prerequisite-based mission unlocking (linear and branching)
  - [ ] Performance-based unlocking (mission score thresholds)
  - [ ] Choice-based branching (story decision consequences)
  - [ ] Dynamic mission availability recalculation

- [ ] **Story Branching System**: Complex narrative branching support
  - [ ] Story choice recording and persistence
  - [ ] Branch evaluation using SEXP-like conditions
  - [ ] Multiple story path support with branch convergence
  - [ ] Branch state validation and consistency checking

- [ ] **Campaign Integration**: Seamless integration with game systems
  - [ ] Mission briefing data provision for unlocked missions
  - [ ] Campaign-specific variables and flags management
  - [ ] Save system integration for campaign persistence
  - [ ] UI integration for campaign selection and progress display

## Technical Requirements

### Architecture Reference
- **Architecture Document**: `EPIC-007-overall-game-flow-state-management/architecture.md` (lines 237-300)
- **WCS Analysis**: `mission/missioncampaign.cpp` - Complex campaign management system
- **Dependencies**: FLOW-001, FLOW-002, FLOW-003 must be complete; EPIC-004 (SEXP) integration required

### Implementation Specifications

#### Campaign Manager
```gdscript
# target/scripts/core/game_flow/campaign_system/campaign_manager.gd
class_name CampaignManager
extends RefCounted

# Current campaign state
var current_campaign: CampaignState
var available_campaigns: Array[CampaignDefinition] = []

# Campaign management
func load_campaign(campaign_id: String, pilot: PilotProfile) -> bool:
    var campaign_def = _find_campaign_definition(campaign_id)
    if not campaign_def:
        push_error("Campaign not found: %s" % campaign_id)
        return false
    
    # Load or create campaign state
    var campaign_state = _load_campaign_state(campaign_id, pilot)
    if not campaign_state:
        campaign_state = _create_new_campaign_state(campaign_def, pilot)
    
    current_campaign = campaign_state
    _initialize_campaign_systems()
    
    campaign_loaded.emit(current_campaign)
    print("Campaign loaded: %s (%.1f%% complete)" % [campaign_id, current_campaign.completion_percentage])
    return true

# Mission completion processing
func complete_mission(mission_id: String, mission_result: MissionResult) -> void:
    if not current_campaign or mission_id in current_campaign.missions_completed:
        return
    
    # Record mission completion
    current_campaign.missions_completed.append(mission_id)
    current_campaign.mission_results[mission_id] = mission_result
    
    # Process mission result for campaign variables
    _process_mission_result(mission_id, mission_result)
    
    # Recalculate available missions
    var newly_available = _calculate_newly_available_missions(mission_id, mission_result)
    for new_mission_id in newly_available:
        if new_mission_id not in current_campaign.missions_available:
            current_campaign.missions_available.append(new_mission_id)
    
    # Update completion percentage
    _update_completion_percentage()
    
    # Trigger events
    mission_completed.emit(mission_id, mission_result, newly_available)
    
    print("Mission completed: %s -> %d new missions available" % [mission_id, newly_available.size()])

signal campaign_loaded(campaign: CampaignState)
signal mission_completed(mission_id: String, result: MissionResult, newly_available: Array[String])
signal campaign_completed(campaign: CampaignState)
```

#### Campaign State Structure
```gdscript
# target/scripts/core/game_flow/campaign_system/campaign_state.gd
class_name CampaignState
extends Resource

@export var campaign_id: String
@export var pilot_name: String
@export var current_mission: String
@export var missions_completed: Array[String] = []
@export var missions_available: Array[String] = []
@export var mission_results: Dictionary = {}  # mission_id -> MissionResult
@export var campaign_variables: Dictionary = {}
@export var story_branch_choices: Dictionary = {}
@export var completion_percentage: float = 0.0
@export var campaign_start_time: int
@export var last_played_time: int

# Mission availability checking
func is_mission_available(mission_id: String) -> bool:
    return mission_id in missions_available

func is_mission_completed(mission_id: String) -> bool:
    return mission_id in missions_completed

# Campaign variable management
func set_campaign_variable(variable_name: String, value: Variant) -> void:
    campaign_variables[variable_name] = value
    variable_changed.emit(variable_name, value)

func get_campaign_variable(variable_name: String, default_value: Variant = null) -> Variant:
    return campaign_variables.get(variable_name, default_value)

# Story choice management
func record_story_choice(choice_id: String, choice_value: Variant) -> void:
    story_branch_choices[choice_id] = choice_value
    story_choice_made.emit(choice_id, choice_value)

signal variable_changed(variable_name: String, value: Variant)
signal story_choice_made(choice_id: String, choice_value: Variant)
```

#### Mission Unlocking System
```gdscript
# target/scripts/core/game_flow/campaign_system/mission_unlocking.gd
class_name MissionUnlocking
extends RefCounted

# Calculate newly available missions after completion
func calculate_newly_available_missions(completed_mission: String, mission_result: MissionResult, campaign_state: CampaignState) -> Array[String]:
    var newly_available: Array[String] = []
    var campaign_def = CampaignRegistry.get_campaign_definition(campaign_state.campaign_id)
    
    for mission_def in campaign_def.missions:
        if mission_def.id in campaign_state.missions_available:
            continue  # Already available
        
        if _are_prerequisites_met(mission_def, campaign_state, mission_result):
            newly_available.append(mission_def.id)
    
    return newly_available

# Prerequisites validation
func _are_prerequisites_met(mission_def: MissionDefinition, campaign_state: CampaignState, recent_result: MissionResult) -> bool:
    # Check completed mission prerequisites
    for prerequisite in mission_def.prerequisite_missions:
        if prerequisite not in campaign_state.missions_completed:
            return false
    
    # Check performance prerequisites
    if mission_def.has_performance_requirements():
        if not _check_performance_requirements(mission_def, campaign_state, recent_result):
            return false
    
    # Check story branch prerequisites
    if mission_def.has_story_requirements():
        if not _check_story_requirements(mission_def, campaign_state):
            return false
    
    # Check campaign variable conditions
    if mission_def.has_variable_conditions():
        if not _evaluate_variable_conditions(mission_def, campaign_state):
            return false
    
    return true

# Performance-based unlocking
func _check_performance_requirements(mission_def: MissionDefinition, campaign_state: CampaignState, recent_result: MissionResult) -> bool:
    for requirement in mission_def.performance_requirements:
        var mission_id = requirement.mission_id
        var required_score = requirement.minimum_score
        
        # Check if we have a result for this mission
        if mission_id in campaign_state.mission_results:
            var result = campaign_state.mission_results[mission_id]
            if result.final_score < required_score:
                return false
        else:
            # Mission not completed yet
            return false
    
    return true

# Story choice-based unlocking
func _check_story_requirements(mission_def: MissionDefinition, campaign_state: CampaignState) -> bool:
    for requirement in mission_def.story_requirements:
        var choice_id = requirement.choice_id
        var required_value = requirement.required_value
        
        if choice_id not in campaign_state.story_branch_choices:
            return false
        
        var actual_value = campaign_state.story_branch_choices[choice_id]
        if actual_value != required_value:
            return false
    
    return true
```

#### Branching Logic System
```gdscript
# target/scripts/core/game_flow/campaign_system/branching_logic.gd
class_name BranchingLogic
extends RefCounted

# Evaluate story branch conditions
func evaluate_story_branches(campaign_state: CampaignState) -> void:
    var campaign_def = CampaignRegistry.get_campaign_definition(campaign_state.campaign_id)
    
    for branch_point in campaign_def.branch_points:
        if _should_evaluate_branch(branch_point, campaign_state):
            _evaluate_branch_conditions(branch_point, campaign_state)

# Story choice processing
func process_story_choice(choice_id: String, choice_value: Variant, campaign_state: CampaignState) -> void:
    # Record the choice
    campaign_state.record_story_choice(choice_id, choice_value)
    
    # Check if this choice affects mission availability
    _evaluate_choice_consequences(choice_id, choice_value, campaign_state)
    
    # Update campaign variables based on choice
    _update_variables_from_choice(choice_id, choice_value, campaign_state)
    
    print("Story choice processed: %s = %s" % [choice_id, str(choice_value)])

# Branch condition evaluation using SEXP integration
func _evaluate_branch_conditions(branch_point: BranchDefinition, campaign_state: CampaignState) -> void:
    # This will integrate with EPIC-004 SEXP system
    var sexp_context = SEXPContext.new()
    sexp_context.set_campaign_state(campaign_state)
    
    for condition in branch_point.conditions:
        var result = SEXPEvaluator.evaluate(condition.expression, sexp_context)
        if result.success and result.value:
            _apply_branch_consequences(condition.consequences, campaign_state)

# Apply branch consequences
func _apply_branch_consequences(consequences: Array[BranchConsequence], campaign_state: CampaignState) -> void:
    for consequence in consequences:
        match consequence.type:
            BranchConsequence.Type.UNLOCK_MISSION:
                if consequence.mission_id not in campaign_state.missions_available:
                    campaign_state.missions_available.append(consequence.mission_id)
            
            BranchConsequence.Type.SET_VARIABLE:
                campaign_state.set_campaign_variable(consequence.variable_name, consequence.variable_value)
            
            BranchConsequence.Type.LOCK_MISSION:
                campaign_state.missions_available.erase(consequence.mission_id)
```

### File Structure
```
target/scripts/core/game_flow/campaign_system/
├── campaign_manager.gd          # Main campaign coordination
├── campaign_state.gd            # Campaign state data structure
├── campaign_definition.gd       # Campaign file structure
├── mission_unlocking.gd         # Mission availability logic
├── branching_logic.gd           # Story branching system
├── mission_result.gd            # Mission completion data
└── campaign_registry.gd         # Campaign discovery and loading
```

## Definition of Done

- [ ] **Code Quality**: All code follows GDScript static typing standards
  - [ ] 100% static typing with comprehensive type annotations
  - [ ] Complex logic properly commented and documented
  - [ ] Efficient algorithms for mission dependency resolution
  - [ ] Resource management with proper cleanup

- [ ] **Testing**: Comprehensive test coverage
  - [ ] Campaign progression testing (linear and branching scenarios)
  - [ ] Mission unlocking logic testing (all prerequisite types)
  - [ ] Story branching testing (choice consequences)
  - [ ] Performance testing with large campaign files

- [ ] **Documentation**: Complete system documentation
  - [ ] Campaign file format specification
  - [ ] Mission unlocking rules documentation
  - [ ] Story branching system guide
  - [ ] Integration guide for campaign designers

- [ ] **Integration**: Seamless integration with dependent systems
  - [ ] SEXP system integration for condition evaluation
  - [ ] Save system integration for campaign persistence
  - [ ] UI integration for campaign progress display
  - [ ] Mission system integration for mission data

## Implementation Notes

### Campaign File Format
- Use JSON or Godot resources for campaign definitions
- Support inheritance and includes for modular campaign design
- Include validation for campaign consistency
- Support hot-reloading for development

### Performance Considerations
- Cache mission dependency graphs for fast unlocking calculations
- Use lazy evaluation for complex branch conditions
- Implement incremental progress updates
- Profile campaign loading and processing performance

### Story Branching Design
- Support complex condition expressions through SEXP integration
- Allow multiple story paths with convergence points
- Implement branch validation to prevent dead ends
- Support dynamic story generation based on player performance

## Dependencies

### Prerequisite Stories
- **FLOW-001**: Game State Manager Core Implementation
- **FLOW-002**: State Transition Validation System  
- **FLOW-003**: Session Management and Lifecycle
- **EPIC-004**: SEXP Expression System (for condition evaluation)

### Dependent Stories
- **FLOW-005**: Campaign Variable Management (closely related)
- **FLOW-007**: Pilot Management and Statistics (for progression tracking)

## Testing Strategy

### Unit Tests
```gdscript
# test_campaign_manager.gd
func test_campaign_loading():
    # Test campaign initialization and loading
    
func test_mission_completion():
    # Test mission completion processing

# test_mission_unlocking.gd
func test_prerequisite_checking():
    # Test various prerequisite validation scenarios
    
func test_performance_requirements():
    # Test score-based mission unlocking
    
func test_story_requirements():
    # Test choice-based mission unlocking

# test_branching_logic.gd
func test_story_choice_processing():
    # Test story choice recording and consequences
    
func test_branch_condition_evaluation():
    # Test complex branching conditions
```

### Integration Tests
- End-to-end campaign progression testing
- Complex branching scenario testing
- Performance testing with realistic campaign data
- Save/load integration testing with campaign state

---

**Story Ready for Implementation**: ✅  
**Architecture Reference**: Approved EPIC-007 architecture document  
**WCS Source Reference**: `mission/missioncampaign.cpp` campaign management logic  
**Integration Complexity**: High - Complex logic with multiple system dependencies  
**Estimated Development Time**: 3-4 days for experienced GDScript developer