# EPIC-004: SEXP Expression System

## Epic Overview
**Epic ID**: EPIC-004  
**Epic Name**: SEXP Expression System  
**Epic Owner**: Larry (WCS Analyst)  
**Priority**: Critical  
**Status**: Analysis Complete  
**Created**: 2025-01-26  
**Position**: 3 (Data Pipeline Phase)  
**Duration**: 8-10 weeks  

## Epic Description
Create a comprehensive mission scripting system that converts WCS SEXP (S-Expression) language into GDScript-based mission logic. SEXP is the heart of WCS mission scripting, controlling everything from triggers and events to complex mission branching and dynamic storytelling. This epic provides the foundation for all mission-based functionality in the Godot conversion.

## WCS SEXP System Analysis

### **SEXP Expression Engine**
- **WCS Systems**: `parse/sexp.cpp`, `parse/sexp.h`, `mission/missionparse.cpp`
- **Purpose**: S-Expression based scripting language for mission logic
- **Key Features**: 
  - Nested expression evaluation
  - Event-driven triggers and conditions
  - Variable management and manipulation
  - Complex boolean logic and arithmetic
  - Mission state tracking and branching

### **Mission Integration**
- **WCS Systems**: `mission/missiongoals.cpp`, `mission/missionmessage.cpp`, `mission/missiontraining.cpp`
- **Purpose**: Integration of SEXP with mission objectives, messages, and training
- **Key Features**:
  - Dynamic objective creation and modification
  - Conditional message systems
  - Training scenario scripting
  - Campaign progression logic

### **Variable System**
- **WCS Systems**: `variables/variables.cpp`, `variables/variables.h`
- **Purpose**: Dynamic variable storage and manipulation within missions
- **Key Features**:
  - String and numeric variable types
  - Persistent variables across missions
  - Runtime variable creation and modification
  - Complex variable operations and comparisons

### **Event System**
- **WCS Systems**: Event handling throughout mission systems
- **Purpose**: Time-based and condition-based event triggering
- **Key Features**:
  - Timer-based events
  - Object-based triggers (ship destroyed, area entered, etc.)
  - Chain reactions and cascading events
  - Priority and ordering management

## Epic Goals

### Primary Goals
1. **SEXP to GDScript Translation**: Convert SEXP expressions to equivalent GDScript logic
2. **Mission Event System**: Event-driven architecture using Godot signals
3. **Variable Management**: Dynamic variable system with persistence
4. **Objective Tracking**: Mission goal and objective management
5. **Campaign Integration**: Support for campaign-wide scripting and progression

### Success Metrics
- 100% of core SEXP functions converted and functional
- Mission events trigger correctly with proper timing
- Variable system maintains state across missions and saves
- Complex missions (training, branching campaigns) work correctly
- Performance matches or exceeds original WCS SEXP system

## Technical Architecture

### SEXP System Structure
```
target/scripts/mission/sexp/
├── core/                            # Core SEXP engine
│   ├── sexp_evaluator.gd           # Main expression evaluator
│   ├── sexp_parser.gd              # SEXP expression parser
│   ├── sexp_context.gd             # Execution context management
│   └── sexp_cache.gd               # Expression caching system
├── functions/                       # SEXP function implementations
│   ├── logic_functions.gd          # Boolean logic (and, or, not, etc.)
│   ├── arithmetic_functions.gd     # Mathematical operations
│   ├── comparison_functions.gd     # Comparison operators
│   ├── object_functions.gd         # Object-related functions
│   ├── mission_functions.gd        # Mission control functions
│   ├── variable_functions.gd       # Variable manipulation
│   ├── event_functions.gd          # Event triggering functions
│   └── utility_functions.gd        # Utility and helper functions
├── variables/                       # Variable management
│   ├── variable_manager.gd         # Central variable management
│   ├── variable_types.gd           # Variable type definitions
│   ├── variable_persistence.gd     # Save/load variable state
│   └── variable_validation.gd      # Variable validation and conversion
├── events/                          # Event system
│   ├── mission_event_manager.gd    # Event coordination and dispatch
│   ├── event_trigger.gd            # Event trigger definitions
│   ├── event_conditions.gd         # Condition evaluation
│   └── event_scheduler.gd          # Time-based event scheduling
└── integration/                     # System integration
    ├── mission_objectives.gd       # Mission goal management
    ├── campaign_state.gd           # Campaign progression tracking
    ├── message_system.gd           # Mission message integration
    └── training_system.gd          # Training scenario support
```

### SEXP Function Categories

#### **Core Logic Functions**
- **Boolean Operations**: `and`, `or`, `not`, `xor`
- **Conditional Logic**: `if-then`, `if-then-else`, `when`, `cond`
- **Looping**: `for-each`, `while`, `repeat`
- **Control Flow**: `sequence`, `parallel`, `random-choice`

#### **Object and Game State**
- **Ship Functions**: `is-ship-type`, `ship-health`, `ship-speed`
- **Wing Functions**: `wing-strength`, `wing-status`, `wing-formation`
- **Distance Functions**: `distance`, `is-in-range`, `closest-ship`
- **Status Functions**: `is-destroyed`, `is-disabled`, `is-docked`

#### **Mission Control**
- **Objective Functions**: `add-goal`, `remove-goal`, `goal-status`
- **Message Functions**: `send-message`, `display-text`, `popup-message`
- **Camera Functions**: `camera-set-position`, `camera-follow-ship`
- **Time Functions**: `mission-time`, `elapsed-time`, `timer-start`

#### **Variable Operations**
- **Assignment**: `set-variable`, `increment-variable`, `decrement-variable`
- **Retrieval**: `get-variable`, `variable-exists`, `variable-type`
- **Comparison**: `variable-equals`, `variable-greater-than`, `variable-less-than`
- **String Operations**: `string-concatenate`, `string-length`, `string-contains`

## Story Breakdown

### Phase 1: Core SEXP Engine (3 weeks)
- **STORY-SEXP-001**: SEXP Parser and Expression Tree Builder
- **STORY-SEXP-002**: Expression Evaluator and Context Management
- **STORY-SEXP-003**: Function Registry and Dynamic Dispatch
- **STORY-SEXP-004**: Error Handling and Debug System

### Phase 2: Function Implementation (3 weeks)
- **STORY-SEXP-005**: Core Logic and Arithmetic Functions
- **STORY-SEXP-006**: Object and Game State Functions
- **STORY-SEXP-007**: Mission Control and Objective Functions
- **STORY-SEXP-008**: Variable Management Functions

### Phase 3: Event and Integration Systems (2-3 weeks)
- **STORY-SEXP-009**: Mission Event System and Triggers
- **STORY-SEXP-010**: Variable Persistence and State Management
- **STORY-SEXP-011**: Mission Objective Integration
- **STORY-SEXP-012**: Campaign State and Progression

### Phase 4: Advanced Features and Validation (2 weeks)
- **STORY-SEXP-013**: Performance Optimization and Caching
- **STORY-SEXP-014**: Complex Mission Support (Training, Branching)
- **STORY-SEXP-015**: Validation and Testing Framework
- **STORY-SEXP-016**: FRED2 Editor Integration Support

## Acceptance Criteria

### Epic-Level Acceptance Criteria
1. **SEXP Parsing**: Parse and convert all standard WCS SEXP expressions
2. **Function Coverage**: Implement 95%+ of commonly used SEXP functions
3. **Mission Integration**: Seamlessly integrate with mission loading and execution
4. **Variable System**: Support all variable types with persistence
5. **Event System**: Event-driven architecture with proper timing and ordering
6. **Performance**: Execute complex missions without noticeable performance impact

### Quality Gates
- SEXP function coverage validation by Larry (WCS Analyst)
- Architecture review by Mo (Godot Architect)
- Performance testing with complex missions by QA
- Integration testing with mission system by Dev
- Final approval by SallySM (Story Manager)

## Technical Challenges

### **SEXP to GDScript Translation**
- **Challenge**: SEXP uses prefix notation, GDScript uses infix
- **Solution**: Expression tree evaluation with proper operator precedence
- **Example**: `(and (> health 50) (< distance 1000))` → `health > 50 and distance < 1000`

### **Dynamic Function Resolution**
- **Challenge**: SEXP functions are resolved at runtime
- **Solution**: Function registry with dynamic dispatch and type checking
- **Implementation**: Dictionary-based function lookup with parameter validation

### **Variable Scope and Persistence**
- **Challenge**: Variables persist across missions and save games
- **Solution**: Hierarchical variable scope with save/load integration
- **Scope Levels**: Global (campaign), Mission, Local (temporary)

### **Event Timing and Synchronization**
- **Challenge**: Events must trigger at precise times and conditions
- **Solution**: Frame-based event scheduler with priority queuing
- **Features**: Deferred execution, condition re-evaluation, event chaining

## Dependencies

### Upstream Dependencies
- **EPIC-CF-001**: Core Foundation & Infrastructure (parser, file system)
- **EPIC-003**: Asset Structures and Management Addon (object references)
- **EPIC-MIG-001**: Data Migration Tools (SEXP expression migration)

### Downstream Dependencies (Enables)
- **EPIC-FRED-001**: GFRED2 Mission Editor (SEXP editing and validation)
- **Mission System**: All mission-based gameplay functionality
- **Campaign System**: Campaign progression and branching logic
- **Training System**: Training mission scripting and guidance

### Integration Dependencies
- **Object System**: Ship, wing, and game object references
- **Game State**: Mission status, player progress, campaign state
- **UI System**: Message display, objective updates, HUD integration

## Risks and Mitigation

### Technical Risks
1. **SEXP Complexity**: Some SEXP expressions are extremely complex
   - *Mitigation*: Incremental implementation, extensive testing with real missions
2. **Performance Impact**: Complex expressions may impact frame rate
   - *Mitigation*: Expression caching, optimization, background evaluation
3. **State Synchronization**: Variable state must remain consistent
   - *Mitigation*: Centralized state management, atomic operations

### Project Risks
1. **Scope Expansion**: Tendency to implement every possible SEXP function
   - *Mitigation*: Focus on commonly used functions, defer exotic features
2. **Integration Complexity**: SEXP touches many game systems
   - *Mitigation*: Clear interfaces, modular design, extensive integration testing

## Success Validation

### Functional Validation
- Load and execute real WCS mission files
- Verify variable persistence across mission boundaries
- Test complex branching and conditional logic
- Validate event timing and trigger accuracy

### Performance Validation
- Benchmark expression evaluation performance
- Test memory usage with large mission scripts
- Validate frame rate impact during intensive scripting
- Measure save/load performance with large variable sets

### Integration Validation
- Seamless integration with mission loading system
- Proper integration with FRED2 editor for mission creation
- Correct interaction with all game systems
- Accurate reproduction of WCS mission behavior

## Timeline Estimate
- **Phase 1**: Core SEXP Engine (3 weeks)
- **Phase 2**: Function Implementation (3 weeks)
- **Phase 3**: Event and Integration Systems (2-3 weeks)
- **Phase 4**: Advanced Features and Validation (2 weeks)
- **Total**: 8-10 weeks with comprehensive testing

## Related Artifacts
- **WCS SEXP Documentation**: Complete function reference and examples
- **Architecture Design**: To be created by Mo
- **Story Definitions**: To be created by SallySM
- **Implementation**: To be handled by Dev
- **Validation**: To be performed by QA

## Critical Path Impact
This epic is **critical for mission functionality** - all mission-based features depend on SEXP system completion. No meaningful mission testing can occur until the core SEXP engine is functional.

## Next Steps
1. **SEXP Function Analysis**: Complete catalog of all WCS SEXP functions
2. **Architecture Design**: Mo to design GDScript integration architecture
3. **Story Creation**: SallySM to break down into implementable stories
4. **Mission Test Data**: Prepare representative WCS missions for testing

---

**Analysis Completed By**: Larry (WCS Analyst)  
**Analysis Date**: 2025-01-26  
**Ready for Architecture Phase**: Yes  
**Critical Path Status**: Required for all mission functionality  
**BMAD Workflow Status**: Analysis → Architecture (Next)