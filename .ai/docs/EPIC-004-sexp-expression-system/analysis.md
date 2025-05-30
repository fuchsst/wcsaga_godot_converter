# EPIC-004: SEXP Expression System - WCS Analysis

**Epic**: EPIC-004 - SEXP Expression System  
**Analyst**: Larry (WCS Analyst)  
**Analysis Date**: 2025-01-27  
**WCS Source**: /mnt/d/projects/wcsaga_godot_converter/source/code/  

## Executive Summary

EPIC-004 focuses on converting WCS's SEXP (S-Expression) system into a GDScript-based mission scripting engine. SEXP is the absolute heart of WCS mission functionality - it's a complete domain-specific language with **444 operators** that controls everything from simple triggers to complex campaign branching logic. This analysis reveals a sophisticated Lisp-like system that touches virtually every WCS subsystem.

**Critical Mission**: Create a GDScript-based mission scripting system that can parse, execute, and maintain compatibility with existing WCS mission files while leveraging Godot's event-driven architecture.

## System Overview

### 1. SEXP Architecture Components

The WCS SEXP system consists of several interconnected components:

1. **Core Expression Engine** - S-Expression parser and evaluator (`parse/sexp.*`)
2. **Variable System** - Dynamic variable management (`variables/variables.*`)
3. **Mission Integration** - Integration with mission parsing and execution
4. **FRED2 Integration** - Visual editor support (`fred2/sexp_tree.*`)
5. **Multiplayer Support** - Network synchronization (`network/multi_sexp.*`)

### 2. SEXP System Scale and Complexity

From WCS source analysis:
- **444 total operators** across 10 major categories
- **52 different argument types** for type checking
- **Dynamic expression tree** with runtime evaluation
- **Variable persistence** across missions and campaigns
- **Event-driven triggers** with precise timing control

## Detailed System Analysis

### 3. Core SEXP Node Structure

#### Key Structure from `sexp.h`:
```cpp
typedef struct sexp_node {
    char text[TOKEN_LENGTH];        // 32-character operator/value text
    int op_index;                   // Index in Operators array (-1 if not operator)
    int type;                       // SEXP_ATOM, SEXP_LIST, or SEXP_NOT_USED
    int subtype;                    // Specific atom/list type
    int first;                      // Index to first parameter (if SEXP)
    int rest;                       // Index to rest of parameters
    int value;                      // Evaluation result (true/false/unknown)
    int flags;                      // Additional node flags
} sexp_node;
```

**Critical Analysis:**
- SEXP uses linked-list structure through `first` and `rest` pointers
- Dynamic memory allocation with `MAX_SEXP_NODES` (originally 4000, now dynamic)
- Supports lazy evaluation with cached `value` field
- Tree structure allows for complex nested expressions

### 4. Operator Category System

#### From `sexp.h` analysis - 10 major categories:

```cpp
#define OP_CATEGORY_OBJECTIVE    0x0400  // Mission objectives and goals
#define OP_CATEGORY_TIME         0x0500  // Time-based functions
#define OP_CATEGORY_LOGICAL      0x0600  // Boolean logic operations
#define OP_CATEGORY_ARITHMETIC   0x0700  // Mathematical operations
#define OP_CATEGORY_STATUS       0x0800  // Ship/object status queries
#define OP_CATEGORY_CHANGE       0x0900  // State modification functions
#define OP_CATEGORY_CONDITIONAL  0x0a00  // Conditional execution
#define OP_CATEGORY_AI           0x0b00  // AI goal management
#define OP_CATEGORY_TRAINING     0x0c00  // Training mission support
#define OP_CATEGORY_GOAL_EVENT   0x0f00  // Goal and event management
```

**Conversion Implications:**
- Each category maps to different GDScript subsystems
- CHANGE category operators require careful state management
- AI category needs integration with Godot's behavior systems
- STATUS category requires real-time game state queries

### 5. Sample Operator Analysis

#### Arithmetic Operators (OP_CATEGORY_ARITHMETIC):
```cpp
#define OP_PLUS     (0x0000 | OP_CATEGORY_ARITHMETIC)  // Addition
#define OP_MINUS    (0x0001 | OP_CATEGORY_ARITHMETIC)  // Subtraction
#define OP_MUL      (0x0003 | OP_CATEGORY_ARITHMETIC)  // Multiplication
#define OP_DIV      (0x0004 | OP_CATEGORY_ARITHMETIC)  // Division
#define OP_RAND     (0x0005 | OP_CATEGORY_ARITHMETIC)  // Random number
#define OP_ABS      (0x0006 | OP_CATEGORY_ARITHMETIC)  // Absolute value
```

#### Status Query Operators (OP_CATEGORY_STATUS):
```cpp
#define OP_SHIELDS_LEFT         (0x0000 | OP_CATEGORY_STATUS)  // Ship shield %
#define OP_HITS_LEFT            (0x0001 | OP_CATEGORY_STATUS)  // Ship hull %
#define OP_DISTANCE             (0x0004 | OP_CATEGORY_STATUS)  // Distance between objects
#define OP_NUM_PLAYERS          (0x0007 | OP_CATEGORY_STATUS)  // Multiplayer count
#define OP_SKILL_LEVEL_AT_LEAST (0x0008 | OP_CATEGORY_STATUS)  // Difficulty check
```

#### Mission Control Operators (OP_CATEGORY_CHANGE):
```cpp
#define OP_ADD_GOAL             // Add mission objective
#define OP_SEND_MESSAGE         // Display message to player
#define OP_CHANGE_SHIP_CLASS    // Transform ship type
#define OP_DESTROY_SHIP         // Remove ship from mission
#define OP_SET_SHIP_FLAG        // Modify ship behavior flags
```

### 6. Argument Type System

#### From `sexp.h` - 52 argument type definitions:

**Core Types:**
```cpp
#define OPF_BOOL            3   // Boolean true/false
#define OPF_NUMBER          4   // Numeric value
#define OPF_SHIP            5   // Ship name/reference
#define OPF_WING            6   // Wing name/reference
#define OPF_SUBSYSTEM       7   // Ship subsystem name
#define OPF_POINT           8   // 3D point or waypoint
#define OPF_MESSAGE         13  // Message text reference
#define OPF_VARIABLE_NAME   35  // SEXP variable reference
```

**Advanced Types:**
```cpp
#define OPF_SHIP_CLASS_NAME     30  // Ship class (e.g., "GTF Ulysses")
#define OPF_WEAPON_NAME         29  // Weapon type reference
#define OPF_AI_ORDER            26  // Squadron command
#define OPF_SOUNDTRACK_NAME     45  // Music track reference
#define OPF_NAV_POINT          49  // Navigation waypoint
```

**Conversion Strategy:**
- Map to Godot's type system with static typing
- Use Resource references for complex objects
- Implement validation at parse time
- Support autocomplete in FRED2 editor equivalent

### 7. Variable System Analysis

#### Core Variable Engine from `variables/variables.h`:

```cpp
// Variable types supported
enum variable_type {
    VAR_BASE,      // Base variable class
    VAR_CONSTANT,  // Constant value
    VAR_OPP,       // Operator variable
    VAR_EXP,       // Expression variable
    VAR_GAME       // Game state variable
};

// Variable call data structure
struct variable_call_data {
    object* obj;                    // Current object context
    texture_variable_data texture;  // Texture context
};
```

**Variable Scope System:**
- **Global Variables**: Campaign-wide persistence
- **Mission Variables**: Per-mission scope
- **Local Variables**: Temporary expression scope
- **Object Variables**: Per-ship/object context

**Expression Evaluation Features:**
- Mathematical expressions with operator precedence
- Trigonometric functions (sin, cos, tan, etc.)
- Game state access (:object.shield_strength:)
- Conditional evaluation and branching

**Critical Insight**: The variable system is essentially a complete expression evaluator that can access any game state. This needs to be replicated in GDScript with similar flexibility.

### 8. Mission Integration Points

#### From `mission/missionparse.h` analysis:

```cpp
// Mission object structure with SEXP integration
typedef struct p_object {
    char name[NAME_LENGTH];
    int ship_class;
    float pos[3];
    float orient[9];
    int arrival_cue;        // SEXP index for arrival conditions
    int departure_cue;      // SEXP index for departure conditions
    int ai_goals;           // SEXP index for AI behavior goals
    // ... additional fields
} p_object;
```

**Mission Event Integration:**
- **Arrival/Departure Cues**: SEXP expressions that determine when ships appear/leave
- **AI Goals**: SEXP-driven behavior trees for NPC ships
- **Mission Goals**: SEXP expressions that define win/lose conditions
- **Trigger Events**: SEXP expressions that activate on game state changes

### 9. FRED2 Editor Integration

#### From `fred2/sexp_tree.*` analysis:

The FRED2 mission editor includes a sophisticated visual SEXP editor:
- **Tree View**: Visual representation of SEXP expressions
- **Drag-and-Drop**: Visual construction of complex expressions
- **Type Validation**: Real-time argument type checking
- **Autocomplete**: Context-aware operator suggestions
- **Syntax Highlighting**: Color-coded expression display

**Conversion Requirements:**
- Godot equivalent needs similar visual editing capabilities
- Integration with Godot's scene editor
- Real-time validation and error reporting
- Export to GDScript format for runtime execution

### 10. Multiplayer Synchronization

#### From `network/multi_sexp.*` analysis:

WCS SEXP system includes network synchronization for multiplayer missions:
- **State Synchronization**: Variable changes broadcast to all clients
- **Event Coordination**: Mission events trigger simultaneously
- **Authority Management**: Server controls critical mission state
- **Lag Compensation**: Delayed evaluation for network latency

**Godot Conversion Strategy:**
- Use Godot's multiplayer RPC system
- Implement deterministic evaluation
- Server-authoritative mission state
- Client prediction for responsiveness

## Performance and Optimization Analysis

### 11. SEXP Evaluation Performance

**Critical Performance Insights from WCS Code:**

1. **Expression Caching**: SEXP nodes cache evaluation results in `value` field
2. **Lazy Evaluation**: Only re-evaluate when dependent state changes
3. **Tree Pruning**: Remove constant subexpressions at parse time
4. **Batch Processing**: Group related evaluations together

**Performance Characteristics:**
- **Parse Time**: O(n) for expression parsing where n = expression length
- **Evaluation Time**: O(d) where d = tree depth (typically shallow)
- **Memory Usage**: ~48 bytes per SEXP node (WCS uses dynamic allocation)
- **Cache Efficiency**: High hit rate due to state locality

### 12. Optimization Strategies for Godot

**GDScript Performance Optimizations:**
1. **Static Analysis**: Pre-compile expressions to optimized GDScript
2. **Signal Integration**: Use Godot signals for event-driven evaluation
3. **Type Safety**: Leverage GDScript static typing for performance
4. **Batched Updates**: Group evaluations in single frame
5. **Memory Pooling**: Reuse expression objects to reduce GC pressure

## Critical Conversion Challenges

### 13. SEXP to GDScript Translation

**Syntax Conversion Examples:**

**WCS SEXP:**
```lisp
(and 
  (> (shield-strength "Alpha 1") 50)
  (< (distance "Alpha 1" "Beta 1") 1000)
  (not (is-destroyed "Gamma 1"))
)
```

**Godot GDScript Equivalent:**
```gdscript
func evaluate_condition() -> bool:
    var alpha1_shields = get_ship("Alpha 1").get_shield_strength()
    var distance = get_ship("Alpha 1").global_position.distance_to(get_ship("Beta 1").global_position)
    var gamma1_alive = not get_ship("Gamma 1").is_destroyed()
    
    return alpha1_shields > 50 and distance < 1000 and gamma1_alive
```

### 14. Dynamic Function Resolution

**Challenge**: SEXP functions are resolved at runtime by name lookup
**WCS Implementation**: Function pointer table with string matching
**Godot Solution**: 
- Pre-compile to method calls where possible
- Use `call()` method for dynamic resolution
- Function registry with type validation

### 15. State Management and Persistence

**Challenge**: Variables must persist across missions and save games
**WCS Implementation**: Global variable arrays with save/load serialization
**Godot Solution**:
- Resource-based variable storage
- Integration with Godot's save system
- Hierarchical scoping (Global → Campaign → Mission → Local)

### 16. Event Timing and Synchronization

**Challenge**: Precise timing control for mission events
**WCS Implementation**: Frame-based evaluation with priority queuing
**Godot Solution**:
- Signal-based event system
- Timer nodes for delayed execution
- Event queue with priority management

## Godot Integration Architecture

### 17. SEXP Engine Design for Godot

**Core Architecture Components:**

```gdscript
# Core SEXP evaluation engine
class_name SEXPEvaluator
extends RefCounted

# SEXP parser for converting text to executable format
class_name SEXPParser
extends RefCounted

# Variable management system
class_name SEXPVariableManager
extends Node

# Mission event coordinator
class_name MissionEventManager
extends Node

# Function registry for SEXP operators
class_name SEXPFunctionRegistry
extends RefCounted
```

### 18. Integration with Godot Systems

**Signal Integration:**
```gdscript
# Ship destruction event
signal ship_destroyed(ship_name: String)

# Mission objective completion
signal objective_completed(objective_id: String)

# Variable value changed
signal variable_changed(var_name: String, new_value: Variant)
```

**Scene Tree Integration:**
- SEXP nodes as children of MissionManager
- Event triggers connected to ship/object signals
- Variable watchers using Godot's property system

### 19. FRED2 Integration Strategy

**Visual SEXP Editor Components:**
- Custom Control node for expression tree display
- Drag-and-drop interface for expression building
- Real-time validation with error highlighting
- Export to both SEXP text and GDScript formats

## Implementation Roadmap

### 20. Phase 1: Core SEXP Engine (3 weeks)

**Week 1: Parser and Expression Tree**
- SEXP text parser with proper tokenization
- Expression tree data structure
- Basic arithmetic and logical operators
- Unit testing framework

**Week 2: Evaluation Engine**
- Tree evaluation algorithm
- Context management system
- Function dispatch mechanism
- Performance optimization

**Week 3: Variable System**
- Variable scope management
- Type validation system
- Persistence integration
- Expression caching

### 21. Phase 2: Function Implementation (3 weeks)

**Week 1: Core Functions**
- Arithmetic operators (+, -, *, /, etc.)
- Logical operators (and, or, not)
- Comparison operators (=, <, >, etc.)
- Basic control flow (if-then-else)

**Week 2: Game State Functions**
- Ship status queries (shields, hull, etc.)
- Position and distance functions
- Object detection and filtering
- Mission state queries

**Week 3: Action Functions**
- Ship spawning and removal
- Message display system
- Objective management
- State modification functions

### 22. Phase 3: Mission Integration (2-3 weeks)

**Week 1: Mission Event System**
- Event trigger framework
- Timer-based events
- Condition evaluation
- Event chaining and priorities

**Week 2: Mission Loading**
- SEXP expression parsing from mission files
- Integration with mission object system
- Arrival/departure cue processing
- AI goal assignment

**Week 3: Testing and Validation**
- Load representative WCS missions
- Verify expression compatibility
- Performance benchmarking
- Error handling validation

### 23. Phase 4: Advanced Features (2 weeks)

**Week 1: Optimization and Polish**
- Expression compilation optimization
- Memory usage optimization
- Error reporting improvements
- Debug visualization tools

**Week 2: FRED2 Integration Preparation**
- SEXP export format definition
- Visual editor interface specification
- Validation rule framework
- Documentation and examples

## Success Metrics and Validation

### 24. Functional Validation Targets

**Expression Compatibility:**
- 95%+ of common SEXP operators implemented
- 100% of training missions execute correctly
- Complex branching campaigns work properly
- Variable persistence across mission boundaries

**Performance Targets:**
- Expression evaluation <1ms for typical mission events
- Memory usage <50MB for large missions
- Frame rate impact <5% during intensive scripting
- Load times comparable to original WCS

### 25. Quality Assurance Strategy

**Testing Approach:**
1. **Unit Testing**: Individual SEXP operator validation
2. **Integration Testing**: Complete mission execution
3. **Performance Testing**: Large mission stress testing
4. **Compatibility Testing**: Real WCS mission files
5. **Regression Testing**: Automated test suite

**Validation Criteria:**
- Zero data loss during SEXP conversion
- Identical behavior compared to WCS reference
- Graceful error handling for malformed expressions
- Clear debugging information for failed expressions

## Risk Assessment and Mitigation

### 26. Technical Risks

**High-Risk Areas:**
1. **Expression Complexity**: Some SEXP expressions are extremely complex
   - *Mitigation*: Incremental implementation with real mission testing
2. **Performance Impact**: GDScript may be slower than optimized C++
   - *Mitigation*: Strategic use of compiled expressions and caching
3. **State Synchronization**: Maintaining consistency across systems
   - *Mitigation*: Centralized state management with validation

### 27. Integration Risks

**System Dependencies:**
1. **Mission System**: SEXP depends on mission object definitions
   - *Mitigation*: Mock objects for testing, clear interface contracts
2. **Ship System**: Many operators query ship state
   - *Mitigation*: Abstraction layer for ship data access
3. **AI System**: AI goals defined through SEXP expressions
   - *Mitigation*: Coordinate with AI epic development

### 28. Scope Management Risks

**Feature Creep Risks:**
1. **Operator Coverage**: Temptation to implement every SEXP operator
   - *Mitigation*: Focus on commonly used operators first
2. **Performance Optimization**: Over-engineering optimization
   - *Mitigation*: Profile-guided optimization based on real usage

## Dependencies and Integration Points

### 29. Upstream Dependencies

**Required Systems:**
- **EPIC-001**: Core Foundation & Infrastructure (parsing, file I/O)
- **EPIC-002**: Asset Structures and Management (ship/weapon references)
- **EPIC-003**: Data Migration & Conversion Tools (mission file conversion)

**Development Dependencies:**
- Mission file format documentation
- WCS object reference system
- Godot GDScript performance characteristics

### 30. Downstream Integration

**Systems Enabled by SEXP:**
- **EPIC-005**: GFRED2 Mission Editor (visual SEXP editing)
- **Mission System**: All mission-based gameplay
- **Campaign System**: Campaign progression logic
- **Training System**: Interactive training missions
- **AI System**: SEXP-driven behavior trees

**Critical Integration Points:**
- Ship object system for status queries
- Message system for player communication
- Objective system for mission goals
- Variable system for state persistence

## Operator Implementation Analysis

### 31. Detailed Operator Function Analysis

**Analysis Date**: 2025-05-30  
**Analyst**: Larry (WCS Analyst)  
**Focus**: Operator implementation details from `source/code/parse/sexp.cpp`

#### 31.1 Logical Operators Implementation

**Core Logical Functions:**

1. **`sexp_or(int n)` (Lines 6171-6214)**
   ```cpp
   int sexp_or(int n) {
       int all_false = 1, result = 0;
       // Evaluates all arguments using is_sexp_true()
       // Returns SEXP_KNOWN_TRUE if any argument is SEXP_KNOWN_TRUE
       // Uses short-circuit logic but evaluates all for mission log purposes
       // Returns SEXP_KNOWN_FALSE if all arguments are SEXP_KNOWN_FALSE
   }
   ```

2. **`sexp_and(int n)` (Lines 6219-6265)**
   ```cpp
   int sexp_and(int n) {
       int all_true = 1, result = -1;
       // Returns SEXP_KNOWN_FALSE if any argument is SEXP_KNOWN_FALSE
       // Uses bitwise AND (&=) for result combination
       // Evaluates all arguments despite short-circuit potential for mission logging
   }
   ```

3. **`sexp_not(int n)` (Lines 6327-6350)**
   ```cpp
   int sexp_not(int n) {
       // Handles special SEXP values:
       // not KNOWN_FALSE == KNOWN_TRUE
       // not KNOWN_TRUE == KNOWN_FALSE  
       // not NAN == TRUE (special case)
       // not NAN_FOREVER == TRUE
   }
   ```

**Key Implementation Insights:**
- All logical operators handle special SEXP values (KNOWN_TRUE, KNOWN_FALSE, NAN, NAN_FOREVER)
- Mission logging requires full evaluation even when short-circuiting would be possible
- Uses `is_sexp_true()` helper for consistent boolean evaluation

#### 31.2 Comparison Operators Implementation

**Number Comparison - `sexp_number_compare(int n, int op)` (Lines 6353-6419)**
```cpp
int sexp_number_compare(int n, int op) {
    int first_number = eval_sexp(first_node);
    // Compares first argument against all subsequent arguments
    switch (op) {
        case OP_EQUALS:
            if (first_number != current_number) return SEXP_FALSE;
        case OP_GREATER_THAN:
            if (first_number <= current_number) return SEXP_FALSE;
        case OP_LESS_THAN:
            if (first_number >= current_number) return SEXP_FALSE;
    }
    // Returns SEXP_TRUE only if ALL comparisons satisfy the operator
}
```

**String Comparison - `sexp_string_compare(int n, int op)` (Lines 6422-6456)**
```cpp
int sexp_string_compare(int n, int op) {
    char* first_string = CTEXT(first_node);
    int val = strcmp(first_string, CTEXT(current_node));
    switch (op) {
        case OP_STRING_EQUALS: if (val != 0) return SEXP_FALSE;
        case OP_STRING_GREATER_THAN: if (val <= 0) return SEXP_FALSE;
        case OP_STRING_LESS_THAN: if (val >= 0) return SEXP_FALSE;
    }
}
```

**Critical Implementation Details:**
- **Multi-argument comparison**: All comparisons check first argument against ALL remaining arguments
- **NAN handling**: Comprehensive NAN checking for numeric operations
- **String comparison**: Uses standard `strcmp()` for lexicographic ordering
- **Type coercion**: Uses `atoi()` for string-to-number conversion

#### 31.3 Arithmetic Operators Implementation

**Addition - `add_sexps(int n)` (Lines 5919-5950)**
```cpp
int add_sexps(int n) {
    int sum = 0, val;
    // First value: either eval_sexp(CAR(n)) or atoi(CTEXT(n))
    sum = eval_sexp(CAR(n));
    
    // NAN propagation check
    if (Sexp_nodes[CAR(n)].value == SEXP_NAN) return SEXP_NAN;
    if (Sexp_nodes[CAR(n)].value == SEXP_NAN_FOREVER) return SEXP_NAN_FOREVER;
    
    // Sum all remaining arguments
    while (CDR(n) != -1) {
        val = eval_sexp(CDR(n));
        // NAN checks for each operand
        sum += val;
        n = CDR(n);
    }
}
```

**Subtraction - `sub_sexps(int n)` (Lines 5954-5973)**
```cpp
int sub_sexps(int n) {
    // Takes first argument and subtracts all remaining arguments
    sum = eval_sexp(CAR(n));
    while (CDR(n) != -1) {
        sum -= eval_sexp(CDR(n));
        n = CDR(n);
    }
}
```

**Multiplication - `mul_sexps(int n)` (Lines 5975-5994)**
```cpp
int mul_sexps(int n) {
    // Multiplies all arguments together
    sum = eval_sexp(Sexp_nodes[n].first);
    while (Sexp_nodes[n].rest != -1) {
        sum *= eval_sexp(Sexp_nodes[n].rest);
        n = Sexp_nodes[n].rest;
    }
}
```

**Division - `div_sexps(int n)` (Lines 5996-6015)**
```cpp
int div_sexps(int n) {
    // Divides first argument by all remaining arguments
    sum = eval_sexp(Sexp_nodes[n].first);
    while (Sexp_nodes[n].rest != -1) {
        sum /= eval_sexp(Sexp_nodes[n].rest);  // No division by zero check!
        n = Sexp_nodes[n].rest;
    }
}
```

**Modulo - `mod_sexps(int n)` (Lines 6017-6036)**
```cpp
int mod_sexps(int n) {
    // Applies modulo operation sequentially
    sum = eval_sexp(Sexp_nodes[n].first);
    while (Sexp_nodes[n].rest != -1) {
        sum = sum % eval_sexp(Sexp_nodes[n].rest);  // No modulo by zero check!
        n = Sexp_nodes[n].rest;
    }
}
```

**Critical Arithmetic Implementation Issues:**
- **No error handling**: Division and modulo operations don't check for zero divisors
- **Integer-only arithmetic**: All operations use `int` type, no floating-point support
- **NAN propagation**: Addition has NAN checking, but other operations don't
- **Multi-argument operations**: All operations process variable number of arguments

#### 31.4 Operator Dispatch System

**Main Evaluation Switch (Lines 20670-20755)**
```cpp
switch (op_num) {
    // Arithmetic operators
    case OP_PLUS:    sexp_val = add_sexps(node); break;
    case OP_MINUS:   sexp_val = sub_sexps(node); break;
    case OP_MUL:     sexp_val = mul_sexps(node); break;
    case OP_DIV:     sexp_val = div_sexps(node); break;
    case OP_MOD:     sexp_val = mod_sexps(node); break;
    
    // Logical operators  
    case OP_OR:      sexp_val = sexp_or(node); break;
    case OP_AND:     sexp_val = sexp_and(node); break;
    case OP_NOT:     sexp_val = sexp_not(node); break;
    
    // Comparison operators
    case OP_GREATER_THAN:
    case OP_LESS_THAN:
    case OP_EQUALS:  sexp_val = sexp_number_compare(node, op_num); break;
    
    case OP_STRING_GREATER_THAN:
    case OP_STRING_LESS_THAN:
    case OP_STRING_EQUALS: sexp_val = sexp_string_compare(node, op_num); break;
}
```

#### 31.5 Type System and Coercion Rules

**SEXP Value Constants:**
```cpp
#define SEXP_TRUE           1
#define SEXP_FALSE          0  
#define SEXP_KNOWN_TRUE    -2147483646  // -2
#define SEXP_KNOWN_FALSE   -2147483647  // -1
#define SEXP_NAN           -2147483644  // -4 (ships not arrived yet)
#define SEXP_NAN_FOREVER   -2147483643  // -5 (permanent false condition)
```

**Type Coercion Rules:**
1. **String to Number**: Uses `atoi(CTEXT(n))` for immediate conversion
2. **Boolean Evaluation**: `is_sexp_true()` returns true for SEXP_TRUE or SEXP_KNOWN_TRUE
3. **Node Access**: `CAR(n)` = first child, `CDR(n)` = rest of list
4. **Text Access**: `CTEXT(n)` = string content of node

**Missing Conditional Operators:**
- No evidence of "when", "cond", or "if" operators in the examined code sections
- These may be handled by the mission event system rather than as direct SEXP operators
- Need further investigation in event processing code

#### 31.6 Performance Characteristics

**Optimization Patterns Found:**
1. **Cached Evaluation**: `Sexp_nodes[n].value` caches results
2. **Lazy Evaluation**: Only re-evaluates when state changes
3. **NAN Propagation**: Early returns for invalid states
4. **Mission Logging**: Full evaluation ensures all events are recorded

**Performance Issues Identified:**
1. **No Division by Zero Protection**: Could cause crashes
2. **Linear List Traversal**: O(n) for each argument list
3. **Repeated eval_sexp Calls**: No intermediate result caching
4. **String Operations**: strcmp() calls for every string comparison

## Final Analysis and Recommendations

### 32. System Complexity Assessment

**Complexity Score: 9/10 (Very High)**

The SEXP system is one of the most complex components in WCS conversion:
- 444 operators requiring individual implementation
- Deep integration with virtually every game system
- Complex state management and persistence requirements
- Performance-critical mission evaluation loops

### 32. Implementation Strategy Recommendations

**Critical Success Factors:**
1. **Incremental Development**: Implement operators in order of usage frequency
2. **Real Mission Testing**: Test with actual WCS missions throughout development
3. **Performance Focus**: Optimize early, profile constantly
4. **Clear Architecture**: Maintain separation between parser, evaluator, and functions
5. **Comprehensive Testing**: Extensive automated testing with edge cases

**Risk Mitigation Priorities:**
1. Start with simplest operators and build complexity gradually
2. Create mock systems for testing before full integration
3. Establish performance baselines early
4. Plan for partial implementation with graceful degradation

### 33. Conversion Feasibility

**Assessment: Challenging but Achievable**

While the SEXP system is extremely complex, the analysis reveals:
- **Clean Architecture**: WCS SEXP system is well-structured
- **Clear Interfaces**: Operator system is modular and extensible
- **Good Documentation**: Function categories and types are well-defined
- **Godot Compatibility**: GDScript provides necessary flexibility

**Recommended Timeline: 8-10 weeks** with experienced GDScript developer

### 34. Critical Path Impact

This epic is **absolutely critical** for mission functionality. No meaningful mission testing can occur until core SEXP engine is operational. Recommended to prioritize:
1. Core engine and common operators (Weeks 1-4)
2. Mission integration testing (Week 5)
3. Parallel development of remaining operators (Weeks 6-8)
4. Polish and optimization (Weeks 9-10)

---

**Analysis Complete**: EPIC-004 SEXP Expression System analysis reveals a sophisticated mission scripting system requiring careful architectural planning and incremental implementation. Ready for Godot architecture design phase.

**Key Findings:**
- 444 operators across 10 categories requiring implementation
- Complex variable system with mathematical expression evaluation
- Deep integration with all WCS game systems
- Performance-critical evaluation loops requiring optimization
- Sophisticated visual editing requirements for FRED2 integration

**Next Steps:**
1. **Architecture Design**: Mo (Godot Architect) to design GDScript integration
2. **Function Prioritization**: Identify most commonly used operators first
3. **Performance Baseline**: Establish performance requirements and testing
4. **Mock System Design**: Create test framework for isolated development