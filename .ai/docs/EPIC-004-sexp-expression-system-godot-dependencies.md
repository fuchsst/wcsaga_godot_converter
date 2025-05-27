# EPIC-004: SEXP Expression System - Godot Dependencies

## Overview
SEXP (S-Expression) system dependency mapping showing integration with core infrastructure and asset management while providing mission scripting capabilities to gameplay systems.

## Core Dependencies (EPIC-001 & EPIC-002 Requirements)

### Required Autoloads from EPIC-001:
- `CoreManager` - System registration and error handling
- `MathUtilities` - Mathematical operations for SEXP expressions
- `FileSystemManager` - Mission file loading and parsing

### Required from EPIC-002:
- `AssetManager` - Ship, weapon, and mission asset queries
- Asset Resource definitions for SEXP object references

### Required Core Scripts from EPIC-001:
- `res://systems/core/parsing/config_parser.gd` - For mission file parsing
- `res://systems/core/utilities/error_handler.gd` - For SEXP error reporting
- `res://systems/core/utilities/performance_tracker.gd` - For expression profiling

## SEXP Manager Singleton Dependencies

### Script: `res://addons/sexp/sexp_manager.gd`
**Autoload Registration**: Registered with `CoreManager` as "SexpManager"
**Initialization Priority**: After EPIC-001 core systems and EPIC-002 asset system

**Signals Connected To**:
- `CoreManager.core_systems_initialized.connect(_on_core_ready)`
- `AssetManager.asset_system_ready.connect(_register_asset_functions)`

**References/Uses**:
- `res://addons/sexp/sexp_parser.gd`
- `res://addons/sexp/sexp_evaluator.gd`
- `res://addons/sexp/runtime/function_registry.gd`
- `res://addons/sexp/runtime/variable_manager.gd`
- `AssetManager` for asset queries

**Signals Emitted**:
- `sexp_system_ready()`
- `expression_evaluated(expression_id: String, result: Variant)`
- `variable_changed(variable_name: String, old_value: Variant, new_value: Variant)`
- `function_registered(function_name: String, category: String)`
- `mission_event_triggered(event_name: String, parameters: Dictionary)`

**Functions Called By Other Systems**:
- `SexpManager.register_function(name: String, callback: Callable, category: String)`
- `SexpManager.evaluate_expression(expression: String, context: Dictionary) -> Variant`
- `SexpManager.set_variable(name: String, value: Variant, scope: String)`
- `SexpManager.get_variable(name: String, scope: String) -> Variant`
- `SexpManager.compile_expression(expression: String) -> SexpExpression`

## Expression System Dependencies

### Script: `res://addons/sexp/sexp_parser.gd` (Enhanced with External Analysis)
**Used By**: SexpManager, GFRED2 editor, mission loading systems
**References/Uses**:
- `res://addons/sexp/sexp_tokenizer.gd` for enhanced RegEx tokenization
- `res://addons/sexp/data/sexp_token.gd` for token representation with position tracking
- `res://addons/sexp/data/sexp_node.gd` for tree construction
- `res://addons/sexp/data/sexp_result.gd` for enhanced error reporting
- `res://systems/core/utilities/error_handler.gd` for parse errors

**Functions Called By SexpManager**:
- `parse_expression(expression_text: String) -> SexpNode`
- `parse_with_validation(expression_text: String) -> ParseResult` (NEW)
- `validate_syntax(expression_text: String) -> ValidationResult` (Enhanced)

### Script: `res://addons/sexp/sexp_tokenizer.gd` (NEW from External Analysis)
**Used By**: SexpParser, GFRED2 syntax highlighting, validation tools
**References/Uses**:
- `RegEx` class for optimized pattern matching
- `res://addons/sexp/data/sexp_token.gd` for token creation
- Compiled regex patterns for performance

**Functions Called By SexpParser**:
- `tokenize_with_validation(sexp_text: String) -> Array[SexpToken]`
- `get_validation_result() -> ValidationResult`
- `get_tokenization_errors() -> Array[String]`

### Script: `res://addons/sexp/sexp_evaluator.gd` (Enhanced with Godot Expression Integration)
**References/Uses**:
- `res://addons/sexp/runtime/execution_context.gd`
- `res://addons/sexp/runtime/function_registry.gd`
- `res://addons/sexp/runtime/variable_manager.gd`
- `res://addons/sexp/data/sexp_result.gd` for enhanced error handling
- `Expression` class (Godot built-in) for complex evaluations (External Analysis)
- `MathUtilities` for mathematical operations

**Functions Called By SexpManager**:
- `evaluate_node(node: SexpNode, context: ExecutionContext) -> SexpResult` (Enhanced)
- `evaluate_compiled_expression(expression: SexpExpression, context: Dictionary) -> SexpResult`
- `evaluate_with_context_hints(expression: SexpExpression, context: ExecutionContext, hints: Dictionary) -> SexpResult` (NEW)
- `pre_validate_expression(sexp_text: String) -> ValidationResult` (NEW)

## Expression Category Dependencies

### Script: `res://addons/sexp/expressions/ship_expressions.gd`
**References/Uses**:
- `AssetManager.get_ship_by_name()` for ship queries
- Object system (when available) for ship state queries
- Ship management system (when available) for ship commands

**Functions Registered With SEXP Manager**:
```gdscript
func _register_ship_functions():
    SexpManager.register_function("ship-exists", _ship_exists, "Ship")
    SexpManager.register_function("ship-destroy", _ship_destroy, "Ship")
    SexpManager.register_function("ship-set-health", _ship_set_health, "Ship")
    SexpManager.register_function("ship-get-position", _ship_get_position, "Ship")
    SexpManager.register_function("ship-warp-out", _ship_warp_out, "Ship")
```

**Signals Connected To**:
- `AssetManager.asset_loaded.connect(_on_ship_asset_available)`
- Ship management system signals (when available)

### Script: `res://addons/sexp/expressions/math_expressions.gd`
**References/Uses**:
- `MathUtilities` for all mathematical operations
- `res://systems/core/math/vector_math.gd` for vector operations

**Functions Registered With SEXP Manager**:
```gdscript
func _register_math_functions():
    SexpManager.register_function("+", _add, "Math")
    SexpManager.register_function("-", _subtract, "Math")
    SexpManager.register_function("*", _multiply, "Math")
    SexpManager.register_function("/", _divide, "Math")
    SexpManager.register_function("distance", _calculate_distance, "Math")
    SexpManager.register_function("random", _random_number, "Math")
```

### Script: `res://addons/sexp/expressions/mission_expressions.gd`
**References/Uses**:
- Mission system (when available) for mission state queries
- `res://addons/sexp/runtime/variable_manager.gd` for mission variables

**Functions Registered With SEXP Manager**:
```gdscript
func _register_mission_functions():
    SexpManager.register_function("mission-end", _end_mission, "Mission")
    SexpManager.register_function("mission-set-objective", _set_objective, "Mission")
    SexpManager.register_function("mission-time", _get_mission_time, "Mission")
    SexpManager.register_function("directive-value", _get_directive_value, "Mission")
```

## Runtime System Dependencies

### Script: `res://addons/sexp/runtime/variable_manager.gd`
**References/Uses**:
- `res://addons/sexp/data/mission_variables.gd` for variable definitions
- Mission persistence system (when available) for variable saving

**Signals Connected To**:
- Mission save/load signals (when available)

**Signals Emitted**:
- `variable_created(name: String, value: Variant, scope: String)`
- `variable_updated(name: String, old_value: Variant, new_value: Variant)`
- `variable_deleted(name: String, scope: String)`

### Script: `res://addons/sexp/runtime/function_registry.gd`
**References/Uses**:
- All expression category scripts for function registration
- `res://addons/sexp/runtime/function_validator.gd` for signature validation

**Functions Called By Expression Categories**:
- `register_function(name: String, callback: Callable, category: String, signature: Array)`
- `get_function(name: String) -> Callable`
- `validate_function_call(name: String, args: Array) -> bool`

## Editor Integration Dependencies

### Script: `res://addons/sexp/editor/sexp_editor.gd`
**Attached To**: `res://addons/sexp/editor/sexp_editor.tscn`
**Editor Context**: Only active in editor mode

**References/Uses**:
- `res://addons/sexp/sexp_parser.gd` for syntax validation
- `res://addons/sexp/runtime/function_registry.gd` for function browsing
- `res://addons/sexp/utilities/syntax_highlighter.gd`

**Signals Connected To**:
- `SexpManager.function_registered.connect(_refresh_function_list)`
- `sexp_parser.syntax_error.connect(_highlight_error)`

### Script: `res://addons/sexp/editor/sexp_dock.gd`
**Attached To**: `res://addons/sexp/editor/sexp_dock.tscn`
**References/Uses**:
- `res://addons/sexp/editor/sexp_editor.gd`
- `res://addons/sexp/debug/sexp_debugger.gd`
- `EditorInterface` for file system integration

## External System Integration Points

### For EPIC-005 (GFRED2 Mission Editor):
**Functions Provided**:
```gdscript
# Mission editing support
SexpManager.validate_mission_expression(expression: String) -> bool
SexpManager.get_available_functions_by_category(category: String) -> Array[String]
SexpManager.auto_complete_expression(partial_text: String) -> Array[String]
```

**Signals Connected From GFRED2**:
- `MissionEditor.expression_edited.connect(SexpManager._validate_expression)`

### For EPIC-007 (Game Flow & State Management):
**Functions Provided**:
```gdscript
# Mission flow control
SexpManager.register_mission_events(mission_data: MissionTemplate)
SexpManager.process_mission_events(delta: float)
SexpManager.evaluate_mission_conditions() -> Array[String]
```

**Signals Connected To Game Flow**:
- `GameStateManager.mission_started.connect(_initialize_mission_context)`
- `GameStateManager.mission_ended.connect(_cleanup_mission_context)`

### For EPIC-010 (AI & Behavior Systems):
**Functions Provided**:
```gdscript
# AI command interface
SexpManager.register_ai_functions(ai_system: Node)
SexpManager.execute_ai_command(ship_name: String, command: String, parameters: Array)
```

**AI Functions Registered**:
```gdscript
# AI behavior functions
"ai-set-behavior" -> _set_ai_behavior(ship_name: String, behavior: String)
"ai-set-target" -> _set_ai_target(ship_name: String, target_name: String)
"ai-join-formation" -> _join_formation(ship_name: String, formation_id: String)
```

### For EPIC-011 (Ship & Combat Systems):
**Functions Provided**:
```gdscript
# Combat integration
SexpManager.register_combat_functions(combat_system: Node)
SexpManager.register_ship_events(ship: Node)
```

**Combat Functions Registered**:
```gdscript
# Ship and weapon functions
"ship-fire-weapon" -> _fire_weapon(ship_name: String, weapon_name: String)
"ship-set-invulnerable" -> _set_invulnerable(ship_name: String, invulnerable: bool)
"weapon-set-damage" -> _set_weapon_damage(weapon_name: String, damage: float)
```

## Performance-Critical Dependencies (Enhanced with External Analysis)

### Expression Evaluation Performance:
```gdscript
# Enhanced compiled expression caching with LRU strategy
sexp_evaluator.cache_compiled_expression(expression_id: String, compiled: SexpExpression)
sexp_evaluator.get_cached_expression(expression_id: String) -> SexpExpression
sexp_evaluator.get_cache_statistics() -> Dictionary  # NEW: Cache analytics

# Variable access optimization with context hints
variable_manager.cache_frequently_accessed_variables()
variable_manager.batch_variable_updates(updates: Dictionary)
variable_manager.get_access_patterns() -> Dictionary  # NEW: Access pattern analysis
```

### Function Call Optimization (External Analysis Recommendations):
```gdscript
# Enhanced function call caching with performance monitoring
function_registry.cache_function_result(function_name: String, args: Array, result: Variant)
function_registry.get_cached_result(function_name: String, args: Array) -> Variant
function_registry.track_function_performance(function_name: String, execution_time: float)  # NEW
function_registry.get_performance_report() -> Dictionary  # NEW: Performance analytics
```

### RegEx Compilation Optimization (NEW from External Analysis):
```gdscript
# Pre-compiled regex patterns for tokenization performance
sexp_tokenizer.compile_patterns_cache()
sexp_tokenizer.get_pattern_performance() -> Dictionary
sexp_tokenizer.optimize_tokenization_for_common_patterns()
```

## Signal Flow Architecture

### SEXP Expression Evaluation Flow:
```
1. System calls SexpManager.evaluate_expression(expression: String)
2. SexpManager.parse_expression() → sexp_parser.parse_expression()
3. SexpManager.evaluate_parsed() → sexp_evaluator.evaluate_node()
4. Function calls → function_registry.get_function() → expression_category.function()
5. Variable access → variable_manager.get_variable()
6. Result returned → SexpManager.expression_evaluated signal
```

### Mission Event Processing Flow:
```
1. Mission system registers events → SexpManager.register_mission_events()
2. Game loop processes → SexpManager.process_mission_events()
3. Event conditions evaluated → sexp_evaluator.evaluate_node()
4. Event triggered → SexpManager.mission_event_triggered signal
5. Game systems respond → Connected signal handlers
```

### Function Registration Flow:
```
1. System initializes → Expression category _ready()
2. Category registers functions → SexpManager.register_function()
3. Function stored → function_registry.register_function()
4. Function available → SexpManager.function_registered signal
5. Editor updates → sexp_editor._refresh_function_list()
```

This SEXP system provides authentic WCS mission scripting capabilities while maintaining clean integration boundaries and optimal performance for complex mission logic.

---

## External Analysis Integration Notes

**Enhanced with Insights from**: Godot SEXP Implementation Strategy (587 lines)  
**Integration Date**: 2025-01-27  
**Reviewer**: Mo (Godot Architect)

### Key External Analysis Integrations:
1. **Enhanced Tokenization**: Added separate `sexp_tokenizer.gd` with optimized RegEx patterns
2. **Godot Expression Class**: Integrated Godot's built-in Expression class for complex evaluations
3. **Performance Analytics**: Added comprehensive performance monitoring and cache analytics
4. **Enhanced Error Handling**: Contextual debugging with position tracking and suggestions
5. **Validation Integration**: Pre-parse validation with detailed error reporting

The dependency structure now incorporates all validated external analysis recommendations while maintaining the clean architectural boundaries established in the original design.