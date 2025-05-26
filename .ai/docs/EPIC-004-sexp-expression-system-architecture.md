# EPIC-004: SEXP Expression System - Architecture

**Document Version**: 1.0  
**Date**: 2025-01-26  
**Architect**: Mo (Godot Architect)  
**Epic**: EPIC-004 - SEXP Expression System  
**System**: Mission scripting engine (SEXP → GDScript conversion)  
**Approval Status**: PENDING (SallySM)  

---

## Architecture Philosophy (Mo's Principles)

> **"SEXP isn't just scripting - it's the DNA of WCS missions. We preserve its power while embracing GDScript's elegance."**
> 
> This architecture transforms WCS's prefix-notation SEXP language into a modern, type-safe GDScript system that maintains the expressiveness and power of the original while leveraging Godot's signal system and resource management.

### Core Design Principles

1. **Expression Tree Fidelity**: Maintain SEXP's nested expression structure
2. **Type Safety**: Static typing throughout with proper error handling  
3. **Signal-Driven Events**: Use Godot signals for mission event communication
4. **Performance Optimized**: Cached expression evaluation with smart re-evaluation
5. **Visual Integration**: Support for visual editing in FRED2 editor
6. **Debug Transparency**: Clear debugging and error reporting for mission creators

## System Architecture Overview

```
SEXP Expression System
├── Core Engine                        # Expression parsing and evaluation
│   ├── SexpEvaluator                 # Main expression evaluator
│   ├── SexpParser                    # SEXP → Expression Tree conversion
│   ├── ExpressionTree                # Internal expression representation
│   └── EvaluationContext             # Runtime context and variable management
├── Function Library                   # SEXP function implementations
│   ├── LogicFunctions                # Boolean logic (and, or, not, etc.)
│   ├── ComparisonFunctions           # Comparison operators
│   ├── ObjectFunctions               # Ship/object manipulation
│   ├── MissionFunctions              # Mission control and objectives
│   ├── VariableFunctions             # Variable manipulation
│   └── UtilityFunctions              # Math, string, utility functions
├── Runtime System                     # Execution environment
│   ├── MissionEventManager           # Event triggering and management
│   ├── VariableManager               # Mission and campaign variables
│   ├── ConditionalEvaluator          # Condition checking and triggers
│   └── PerformanceMonitor            # SEXP execution monitoring
├── Integration Layer                  # External system integration
│   ├── MissionObjective              # Goal and objective integration
│   ├── ShipSystemInterface           # Ship and object manipulation
│   ├── CampaignInterface             # Campaign variable integration
│   └── EditorInterface               # FRED2 visual editing support
└── Debug & Validation                 # Development and debugging tools
    ├── SexpValidator                 # Expression validation
    ├── DebugEvaluator                # Step-by-step debugging
    ├── PerformanceProfiler           # Performance analysis
    └── ErrorReporter                 # Comprehensive error reporting
```

## Detailed Component Architecture

### Core Expression Engine

```gdscript
# Main SEXP Evaluator
class_name SexpEvaluator
extends RefCounted

# Singleton for global access
static var instance: SexpEvaluator

# Expression evaluation interface
func evaluate_expression(expression: SexpExpression, context: EvaluationContext) -> SexpResult
func evaluate_condition(condition: SexpExpression, context: EvaluationContext) -> bool
func evaluate_action(action: SexpExpression, context: EvaluationContext) -> void

# Cached evaluation for performance
var _expression_cache: Dictionary = {}
var _cache_hits: int = 0
var _cache_misses: int = 0

# Expression Tree Structure
class_name SexpExpression
extends Resource

enum ExpressionType {
    LITERAL_NUMBER,
    LITERAL_STRING,
    VARIABLE_REFERENCE,
    FUNCTION_CALL,
    OPERATOR_CALL
}

@export var expression_type: ExpressionType
@export var function_name: String
@export var arguments: Array[SexpExpression] = []
@export var literal_value: Variant
@export var variable_name: String

# Expression validation
func is_valid() -> bool
func get_validation_errors() -> Array[String]
func get_argument_count() -> int
func get_expected_return_type() -> SexpResult.Type
```

### Function Implementation Architecture

```gdscript
# Base SEXP Function Interface
class_name BaseSexpFunction
extends RefCounted

# Function metadata
@export var function_name: String
@export var argument_count: int = -1  # -1 for variable arguments
@export var return_type: SexpResult.Type
@export var description: String

# Function execution interface
func execute(args: Array[SexpResult], context: EvaluationContext) -> SexpResult
func validate_arguments(args: Array[SexpExpression]) -> ValidationResult
func get_help_text() -> String

# Example: Logic Function Implementation
class_name AndFunction
extends BaseSexpFunction

func _init():
    function_name = "and"
    argument_count = -1  # Variable arguments
    return_type = SexpResult.Type.BOOLEAN
    description = "Returns true if all arguments are true"

func execute(args: Array[SexpResult], context: EvaluationContext) -> SexpResult:
    for arg in args:
        if not arg.get_boolean_value():
            return SexpResult.create_boolean(false)
    return SexpResult.create_boolean(true)

func validate_arguments(args: Array[SexpExpression]) -> ValidationResult:
    var result = ValidationResult.new()
    if args.size() < 2:
        result.add_error("'and' function requires at least 2 arguments")
    for arg in args:
        if arg.get_expected_return_type() != SexpResult.Type.BOOLEAN:
            result.add_warning("Argument may not evaluate to boolean")
    return result
```

### Variable Management System

```gdscript
# Variable Manager for Mission and Campaign Variables
class_name VariableManager
extends RefCounted

# Variable scopes
enum VariableScope {
    LOCAL,      # Current mission only
    CAMPAIGN,   # Persistent across campaign
    GLOBAL      # Persistent across all campaigns
}

# Variable storage by scope
var _local_variables: Dictionary = {}
var _campaign_variables: Dictionary = {}
var _global_variables: Dictionary = {}

# Variable operations
func set_variable(name: String, value: Variant, scope: VariableScope = VariableScope.LOCAL) -> void
func get_variable(name: String, scope: VariableScope = VariableScope.LOCAL) -> Variant
func has_variable(name: String, scope: VariableScope = VariableScope.LOCAL) -> bool
func delete_variable(name: String, scope: VariableScope = VariableScope.LOCAL) -> void

# Variable persistence
func save_campaign_variables() -> Dictionary
func load_campaign_variables(data: Dictionary) -> void
func save_global_variables() -> Dictionary
func load_global_variables(data: Dictionary) -> void

# Variable type safety
class_name SexpVariable
extends Resource

enum VariableType {
    NUMBER,
    STRING,
    BOOLEAN,
    OBJECT_REFERENCE
}

@export var variable_name: String
@export var variable_type: VariableType
@export var current_value: Variant
@export var default_value: Variant
@export var is_persistent: bool = false

func set_value(value: Variant) -> bool:
    if _validate_type(value):
        current_value = value
        variable_changed.emit(variable_name, value)
        return true
    return false

signal variable_changed(var_name: String, new_value: Variant)
```

### Event System Integration

```gdscript
# Mission Event Manager for SEXP-driven events
class_name MissionEventManager
extends Node

# Event registration and triggering
func register_event_trigger(condition: SexpExpression, action: SexpExpression) -> int
func remove_event_trigger(trigger_id: int) -> void
func check_event_triggers() -> void

# Event trigger structure
class_name EventTrigger
extends Resource

@export var trigger_id: int
@export var condition_expression: SexpExpression
@export var action_expression: SexpExpression
@export var trigger_count: int = 0
@export var max_triggers: int = -1  # -1 for unlimited
@export var is_enabled: bool = true

# Frame-based evaluation
var _active_triggers: Array[EventTrigger] = []
var _evaluation_context: EvaluationContext

func _process(_delta: float) -> void:
    _check_active_triggers()

func _check_active_triggers() -> void:
    for trigger in _active_triggers:
        if trigger.is_enabled and _should_evaluate_trigger(trigger):
            var condition_result = SexpEvaluator.evaluate_condition(
                trigger.condition_expression, 
                _evaluation_context
            )
            if condition_result:
                _execute_trigger_action(trigger)
```

### Performance Optimization Architecture

```gdscript
# Expression Caching System
class_name ExpressionCache
extends RefCounted

# Cache structure for expression results
class_name CacheEntry
extends RefCounted
var expression_hash: int
var result: SexpResult
var context_hash: int
var last_access: int
var access_count: int

# Cache management
const MAX_CACHE_ENTRIES: int = 1000
const CACHE_CLEANUP_INTERVAL: float = 30.0

var _cache_entries: Dictionary = {}
var _lru_order: Array[int] = []

func get_cached_result(expression: SexpExpression, context: EvaluationContext) -> SexpResult:
    var expr_hash = _hash_expression(expression)
    var ctx_hash = _hash_context(context)
    var cache_key = _create_cache_key(expr_hash, ctx_hash)
    
    if _cache_entries.has(cache_key):
        var entry = _cache_entries[cache_key]
        entry.last_access = Time.get_ticks_msec()
        entry.access_count += 1
        _update_lru(cache_key)
        return entry.result
    
    return null

func cache_result(expression: SexpExpression, context: EvaluationContext, result: SexpResult) -> void:
    if _should_cache_result(expression, result):
        var cache_key = _create_cache_key(_hash_expression(expression), _hash_context(context))
        var entry = CacheEntry.new()
        entry.expression_hash = _hash_expression(expression)
        entry.result = result
        entry.context_hash = _hash_context(context)
        entry.last_access = Time.get_ticks_msec()
        entry.access_count = 1
        
        _ensure_cache_space()
        _cache_entries[cache_key] = entry
        _lru_order.push_back(cache_key)
```

### Visual Editor Integration

```gdscript
# FRED2 Visual SEXP Editor Integration
class_name VisualSexpEditor
extends Control

# Visual representation of SEXP expressions
@onready var expression_tree: Tree = $ExpressionTree
@onready var function_palette: ItemList = $FunctionPalette
@onready var property_panel: Control = $PropertyPanel

# SEXP to visual conversion
func display_expression(expression: SexpExpression) -> void:
    expression_tree.clear()
    _build_expression_tree(expression, expression_tree.create_item())

func _build_expression_tree(expr: SexpExpression, tree_item: TreeItem) -> void:
    match expr.expression_type:
        SexpExpression.ExpressionType.FUNCTION_CALL:
            tree_item.set_text(0, expr.function_name)
            tree_item.set_icon(0, _get_function_icon(expr.function_name))
            for arg in expr.arguments:
                var child_item = tree_item.create_child()
                _build_expression_tree(arg, child_item)
        
        SexpExpression.ExpressionType.LITERAL_NUMBER:
            tree_item.set_text(0, str(expr.literal_value))
            tree_item.set_icon(0, _get_literal_icon("number"))
        
        SexpExpression.ExpressionType.VARIABLE_REFERENCE:
            tree_item.set_text(0, expr.variable_name)
            tree_item.set_icon(0, _get_variable_icon())

# Visual editing interface
func _on_function_selected(function_name: String) -> void:
    var selected_item = expression_tree.get_selected()
    if selected_item:
        _insert_function_at_selection(function_name, selected_item)

func _on_expression_tree_item_selected() -> void:
    var selected_item = expression_tree.get_selected()
    if selected_item:
        _display_item_properties(selected_item)

# Real-time validation display
func _validate_current_expression() -> void:
    var expression = _build_expression_from_tree()
    var validation = SexpValidator.validate_expression(expression)
    _display_validation_results(validation)
```

## Integration Patterns

### Mission System Integration

```gdscript
# Mission objective integration
func _on_mission_loaded(mission_data: MissionData) -> void:
    # Parse mission SEXP expressions
    for objective in mission_data.objectives:
        var condition_expr = SexpParser.parse(objective.condition_sexp)
        var action_expr = SexpParser.parse(objective.completion_action_sexp)
        
        MissionEventManager.register_event_trigger(condition_expr, action_expr)
    
    # Initialize mission variables
    for var_def in mission_data.variable_definitions:
        VariableManager.set_variable(var_def.name, var_def.default_value, VariableScope.LOCAL)

# Ship system integration
func execute_ship_action(ship_ref: String, action: String, parameters: Array) -> SexpResult:
    var ship_node = _get_ship_by_reference(ship_ref)
    if not ship_node:
        return SexpResult.create_error("Ship not found: " + ship_ref)
    
    match action:
        "set-hull-strength":
            ship_node.set_hull_strength(parameters[0])
            return SexpResult.create_boolean(true)
        "destroy-ship":
            ship_node.destroy()
            return SexpResult.create_boolean(true)
        "ship-distance":
            var target_ship = _get_ship_by_reference(parameters[0])
            if target_ship:
                var distance = ship_node.global_position.distance_to(target_ship.global_position)
                return SexpResult.create_number(distance)
            return SexpResult.create_error("Target ship not found")
```

### Campaign Variable Persistence

```gdscript
# Campaign integration for persistent variables
func save_campaign_state() -> Dictionary:
    return {
        "sexp_variables": VariableManager.save_campaign_variables(),
        "mission_completion_flags": _get_mission_completion_state(),
        "story_branch_choices": _get_story_branch_state()
    }

func load_campaign_state(save_data: Dictionary) -> void:
    if save_data.has("sexp_variables"):
        VariableManager.load_campaign_variables(save_data["sexp_variables"])
    
    # Restore mission completion and story state
    _restore_mission_completion_state(save_data.get("mission_completion_flags", {}))
    _restore_story_branch_state(save_data.get("story_branch_choices", {}))
```

## Error Handling & Debugging

### Comprehensive Error Management

```gdscript
# SEXP Result with error handling
class_name SexpResult
extends RefCounted

enum Type {
    NUMBER,
    STRING,
    BOOLEAN,
    OBJECT_REFERENCE,
    ERROR,
    VOID
}

enum ErrorType {
    NONE,
    SYNTAX_ERROR,
    TYPE_MISMATCH,
    UNDEFINED_VARIABLE,
    UNDEFINED_FUNCTION,
    ARGUMENT_COUNT_MISMATCH,
    RUNTIME_ERROR,
    OBJECT_NOT_FOUND
}

var result_type: Type
var value: Variant
var error_type: ErrorType = ErrorType.NONE
var error_message: String = ""
var stack_trace: Array[String] = []

# Error creation helpers
static func create_error(error_msg: String, error_t: ErrorType = ErrorType.RUNTIME_ERROR) -> SexpResult:
    var result = SexpResult.new()
    result.result_type = Type.ERROR
    result.error_type = error_t
    result.error_message = error_msg
    result.stack_trace = _get_current_stack_trace()
    return result

# Debug information
func get_debug_string() -> String:
    if result_type == Type.ERROR:
        return "ERROR: " + error_message + "\nStack: " + str(stack_trace)
    else:
        return str(value) + " (" + Type.keys()[result_type] + ")"
```

### Performance Monitoring

```gdscript
# SEXP Performance Monitor
class_name SexpPerformanceMonitor
extends RefCounted

# Performance tracking
var _function_call_counts: Dictionary = {}
var _function_execution_times: Dictionary = {}
var _expression_evaluation_count: int = 0
var _total_evaluation_time_ms: float = 0.0

func track_function_call(function_name: String, execution_time_ms: float) -> void:
    _function_call_counts[function_name] = _function_call_counts.get(function_name, 0) + 1
    _function_execution_times[function_name] = _function_execution_times.get(function_name, 0.0) + execution_time_ms

func track_expression_evaluation(evaluation_time_ms: float) -> void:
    _expression_evaluation_count += 1
    _total_evaluation_time_ms += evaluation_time_ms

func get_performance_report() -> Dictionary:
    return {
        "total_expressions_evaluated": _expression_evaluation_count,
        "total_evaluation_time_ms": _total_evaluation_time_ms,
        "average_evaluation_time_ms": _total_evaluation_time_ms / max(1, _expression_evaluation_count),
        "function_call_counts": _function_call_counts.duplicate(),
        "function_execution_times": _function_execution_times.duplicate(),
        "slowest_functions": _get_slowest_functions()
    }
```

## Testing Architecture

### Unit Testing Framework

```gdscript
# SEXP Testing Framework
extends GutTest

func test_basic_arithmetic():
    var expr = SexpParser.parse("(+ 2 3)")
    var context = EvaluationContext.new()
    var result = SexpEvaluator.evaluate_expression(expr, context)
    
    assert_eq(result.result_type, SexpResult.Type.NUMBER)
    assert_eq(result.get_number_value(), 5.0)

func test_variable_assignment_and_retrieval():
    var context = EvaluationContext.new()
    
    # Set variable
    var set_expr = SexpParser.parse("(set-variable \"test_var\" 42)")
    SexpEvaluator.evaluate_expression(set_expr, context)
    
    # Get variable
    var get_expr = SexpParser.parse("(get-variable \"test_var\")")
    var result = SexpEvaluator.evaluate_expression(get_expr, context)
    
    assert_eq(result.get_number_value(), 42.0)

func test_conditional_logic():
    var context = EvaluationContext.new()
    var expr = SexpParser.parse("(if (> 5 3) \"greater\" \"not greater\")")
    var result = SexpEvaluator.evaluate_expression(expr, context)
    
    assert_eq(result.get_string_value(), "greater")

func test_ship_function_integration():
    # Test ship-related SEXP functions
    var context = EvaluationContext.new()
    _setup_test_ship(context, "TestShip", Vector3.ZERO)
    
    var expr = SexpParser.parse("(ship-health \"TestShip\")")
    var result = SexpEvaluator.evaluate_expression(expr, context)
    
    assert_eq(result.result_type, SexpResult.Type.NUMBER)
    assert_gt(result.get_number_value(), 0.0)
```

---

**Architecture Approval**: PENDING (SallySM)  
**Implementation Ready**: YES  
**Dependencies**: EPIC-001 (Core Foundation), EPIC-002 (Asset Structures)  
**Risk Level**: HIGH (Complex language conversion)

**Critical Performance Requirements:**
- Expression evaluation: <1ms for simple expressions
- Variable operations: <0.1ms per operation  
- Event checking: <5ms per frame for 100+ triggers
- Memory usage: <10MB for complex mission scripts

**Next Steps:**
1. SallySM approval of architecture
2. Function library specification and prioritization
3. Parser implementation with comprehensive testing
4. Integration with mission system and editor