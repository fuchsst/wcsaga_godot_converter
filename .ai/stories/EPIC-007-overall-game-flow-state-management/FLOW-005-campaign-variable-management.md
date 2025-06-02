# FLOW-005: Campaign Variable Management

**Epic**: EPIC-007 - Overall Game Flow & State Management  
**Phase**: 2 - Campaign and Mission Flow  
**Story ID**: FLOW-005  
**Story Name**: Campaign Variable Management  
**Assigned**: Dev (GDScript Developer)  
**Status**: Ready for Implementation  
**Story Points**: 5  
**Priority**: Medium  

---

## User Story

**As a** campaign designer and game system  
**I want** a robust campaign variable system that persists story state and mission data  
**So that** complex narrative conditions and game logic can be evaluated across missions and campaigns  

## Story Description

Implement a comprehensive campaign variable management system that handles persistent story variables, mission flags, and game state data that must persist across multiple missions and game sessions. This system provides the foundation for complex campaign logic and story branching.

## Acceptance Criteria

- [ ] **Variable Type System**: Support for multiple data types and validation
  - [ ] Integer, float, boolean, and string variable types
  - [ ] Array and dictionary variable support for complex data
  - [ ] Type validation and automatic conversion where appropriate
  - [ ] Variable scope management (campaign, mission, session)

- [ ] **Variable Persistence**: Reliable variable storage and retrieval
  - [ ] Automatic persistence with campaign save data
  - [ ] Variable change tracking and versioning
  - [ ] Import/export capabilities for debugging and modding
  - [ ] Data integrity validation and corruption recovery

- [ ] **Variable Access Control**: Proper scoping and access management
  - [ ] Read-only variables for system data
  - [ ] Write-protected variables for mission designers
  - [ ] Scoped variable access (global, campaign, mission-specific)
  - [ ] Variable namespace management to prevent conflicts

- [ ] **SEXP Integration**: Seamless integration with expression evaluation
  - [ ] Variable reference in SEXP expressions
  - [ ] Variable modification through SEXP functions
  - [ ] Type-safe variable operations in expressions
  - [ ] Performance-optimized variable lookup for SEXP evaluation

## Technical Requirements

### Architecture Reference
- **Architecture Document**: `EPIC-007-overall-game-flow-state-management/architecture.md` (campaign variables section)
- **WCS Analysis**: Campaign variable system across multiple mission files
- **Dependencies**: FLOW-004 (Campaign Progression), EPIC-004 (SEXP) integration required

### Implementation Specifications

#### Campaign Variables Manager
```gdscript
# target/scripts/core/game_flow/campaign_system/campaign_variables.gd
class_name CampaignVariables
extends RefCounted

# Variable storage
var _variables: Dictionary = {}
var _variable_metadata: Dictionary = {}
var _change_history: Array[VariableChange] = []

enum VariableScope {
    GLOBAL,      # Persists across all campaigns
    CAMPAIGN,    # Persists within current campaign
    MISSION,     # Valid only for current mission
    SESSION      # Valid only for current session
}

enum VariableType {
    INTEGER,
    FLOAT,
    BOOLEAN,
    STRING,
    ARRAY,
    DICTIONARY
}

# Variable management
func set_variable(name: String, value: Variant, scope: VariableScope = VariableScope.CAMPAIGN) -> bool:
    # Validate variable name
    if not _is_valid_variable_name(name):
        push_error("Invalid variable name: %s" % name)
        return false
    
    # Check write permissions
    if not _can_write_variable(name):
        push_error("Variable is write-protected: %s" % name)
        return false
    
    # Validate and convert value
    var validated_value = _validate_and_convert_value(name, value)
    if validated_value == null and value != null:
        push_error("Invalid value type for variable %s: %s" % [name, typeof(value)])
        return false
    
    # Store previous value for change tracking
    var previous_value = _variables.get(name, null)
    
    # Set the variable
    _variables[name] = validated_value
    _update_variable_metadata(name, scope, typeof(validated_value))
    
    # Record change
    _record_variable_change(name, previous_value, validated_value, scope)
    
    # Emit change signal
    variable_changed.emit(name, validated_value, previous_value, scope)
    
    return true

func get_variable(name: String, default_value: Variant = null) -> Variant:
    # Check read permissions
    if not _can_read_variable(name):
        push_warning("Variable access denied: %s" % name)
        return default_value
    
    return _variables.get(name, default_value)

# Typed variable accessors
func get_int(name: String, default_value: int = 0) -> int:
    var value = get_variable(name, default_value)
    return int(value) if value != null else default_value

func get_float(name: String, default_value: float = 0.0) -> float:
    var value = get_variable(name, default_value)
    return float(value) if value != null else default_value

func get_bool(name: String, default_value: bool = false) -> bool:
    var value = get_variable(name, default_value)
    return bool(value) if value != null else default_value

func get_string(name: String, default_value: String = "") -> String:
    var value = get_variable(name, default_value)
    return str(value) if value != null else default_value

# Variable introspection
func has_variable(name: String) -> bool:
    return name in _variables

func get_variable_type(name: String) -> VariableType:
    if not has_variable(name):
        return -1
    
    var metadata = _variable_metadata.get(name, {})
    return metadata.get("type", VariableType.STRING)

func get_variable_scope(name: String) -> VariableScope:
    if not has_variable(name):
        return -1
    
    var metadata = _variable_metadata.get(name, {})
    return metadata.get("scope", VariableScope.CAMPAIGN)

# Variable operations
func increment_variable(name: String, amount: float = 1.0) -> bool:
    var current_value = get_variable(name, 0)
    if typeof(current_value) == TYPE_INT:
        return set_variable(name, int(current_value) + int(amount))
    elif typeof(current_value) == TYPE_FLOAT:
        return set_variable(name, float(current_value) + amount)
    else:
        push_error("Cannot increment non-numeric variable: %s" % name)
        return false

func append_to_array(name: String, value: Variant) -> bool:
    var current_array = get_variable(name, [])
    if typeof(current_array) != TYPE_ARRAY:
        push_error("Variable is not an array: %s" % name)
        return false
    
    current_array.append(value)
    return set_variable(name, current_array)

# Signals
signal variable_changed(name: String, new_value: Variant, old_value: Variant, scope: VariableScope)
signal variable_deleted(name: String, scope: VariableScope)
```

#### Variable Metadata and Validation
```gdscript
# Variable metadata management
func _update_variable_metadata(name: String, scope: VariableScope, value_type: int) -> void:
    if name not in _variable_metadata:
        _variable_metadata[name] = {}
    
    var metadata = _variable_metadata[name]
    metadata["scope"] = scope
    metadata["type"] = _godot_type_to_variable_type(value_type)
    metadata["created_time"] = Time.get_unix_time_from_system()
    metadata["modified_time"] = Time.get_unix_time_from_system()
    metadata["access_count"] = metadata.get("access_count", 0) + 1

# Variable validation
func _is_valid_variable_name(name: String) -> bool:
    # Check basic naming rules
    if name.length() == 0 or name.length() > 64:
        return false
    
    # Check for valid characters (alphanumeric, underscore, dash)
    var regex = RegEx.new()
    regex.compile("^[a-zA-Z][a-zA-Z0-9_-]*$")
    return regex.search(name) != null

func _validate_and_convert_value(name: String, value: Variant) -> Variant:
    # Check if variable already exists and has a type constraint
    if name in _variable_metadata:
        var expected_type = _variable_metadata[name].get("type", VariableType.STRING)
        return _convert_to_expected_type(value, expected_type)
    
    # New variable - accept as-is but validate
    if typeof(value) in [TYPE_INT, TYPE_FLOAT, TYPE_BOOL, TYPE_STRING, TYPE_ARRAY, TYPE_DICTIONARY]:
        return value
    
    # Try to convert to string as fallback
    return str(value)

# Access control
func _can_read_variable(name: String) -> bool:
    # Check read permissions based on variable metadata
    var metadata = _variable_metadata.get(name, {})
    var read_only = metadata.get("read_only", false)
    
    # Always allow reading (restriction would be on UI level)
    return true

func _can_write_variable(name: String) -> bool:
    # Check write permissions
    var metadata = _variable_metadata.get(name, {})
    var write_protected = metadata.get("write_protected", false)
    
    # System variables are write-protected
    if name.begins_with("_system_"):
        return false
    
    return not write_protected
```

#### Variable Change Tracking
```gdscript
# target/scripts/core/game_flow/campaign_system/variable_change.gd
class_name VariableChange
extends Resource

@export var variable_name: String
@export var old_value: Variant
@export var new_value: Variant
@export var change_time: int
@export var scope: CampaignVariables.VariableScope
@export var source: String  # What caused the change (SEXP, script, etc.)

# Change tracking
func _record_variable_change(name: String, old_value: Variant, new_value: Variant, scope: VariableScope) -> void:
    var change = VariableChange.new()
    change.variable_name = name
    change.old_value = old_value
    change.new_value = new_value
    change.change_time = Time.get_unix_time_from_system()
    change.scope = scope
    change.source = _get_change_source()
    
    _change_history.append(change)
    
    # Limit history size
    if _change_history.size() > 1000:
        _change_history.pop_front()

# Variable persistence
func export_variables_to_dict() -> Dictionary:
    return {
        "variables": _variables,
        "metadata": _variable_metadata,
        "change_history": _serialize_change_history()
    }

func import_variables_from_dict(data: Dictionary) -> bool:
    if not data.has("variables") or not data.has("metadata"):
        push_error("Invalid variable data format")
        return false
    
    _variables = data["variables"]
    _variable_metadata = data["metadata"]
    
    if data.has("change_history"):
        _change_history = _deserialize_change_history(data["change_history"])
    
    variables_imported.emit(_variables.size())
    return true

signal variables_imported(count: int)
```

#### SEXP Integration Interface
```gdscript
# target/scripts/core/game_flow/campaign_system/sexp_variable_interface.gd
class_name SEXPVariableInterface
extends RefCounted

# SEXP function implementations for variable access
static func sexp_get_variable(args: Array) -> SEXPResult:
    if args.size() != 1:
        return SEXPResult.error("get-variable requires exactly 1 argument")
    
    var variable_name = str(args[0])
    var value = CampaignVariables.get_variable(variable_name)
    
    return SEXPResult.success(value)

static func sexp_set_variable(args: Array) -> SEXPResult:
    if args.size() != 2:
        return SEXPResult.error("set-variable requires exactly 2 arguments")
    
    var variable_name = str(args[0])
    var value = args[1]
    
    var success = CampaignVariables.set_variable(variable_name, value)
    return SEXPResult.success(success)

static func sexp_increment_variable(args: Array) -> SEXPResult:
    if args.size() < 1 or args.size() > 2:
        return SEXPResult.error("increment-variable requires 1-2 arguments")
    
    var variable_name = str(args[0])
    var amount = float(args[1]) if args.size() > 1 else 1.0
    
    var success = CampaignVariables.increment_variable(variable_name, amount)
    return SEXPResult.success(success)

static func sexp_has_variable(args: Array) -> SEXPResult:
    if args.size() != 1:
        return SEXPResult.error("has-variable requires exactly 1 argument")
    
    var variable_name = str(args[0])
    var has_var = CampaignVariables.has_variable(variable_name)
    
    return SEXPResult.success(has_var)

# Register SEXP functions
static func register_sexp_functions() -> void:
    SEXPRegistry.register_function("get-variable", sexp_get_variable)
    SEXPRegistry.register_function("set-variable", sexp_set_variable)
    SEXPRegistry.register_function("increment-variable", sexp_increment_variable)
    SEXPRegistry.register_function("has-variable", sexp_has_variable)
    SEXPRegistry.register_function("get-int", func(args): return SEXPResult.success(CampaignVariables.get_int(str(args[0]), int(args[1]) if args.size() > 1 else 0)))
    SEXPRegistry.register_function("get-float", func(args): return SEXPResult.success(CampaignVariables.get_float(str(args[0]), float(args[1]) if args.size() > 1 else 0.0)))
    SEXPRegistry.register_function("get-bool", func(args): return SEXPResult.success(CampaignVariables.get_bool(str(args[0]), bool(args[1]) if args.size() > 1 else false)))
    SEXPRegistry.register_function("get-string", func(args): return SEXPResult.success(CampaignVariables.get_string(str(args[0]), str(args[1]) if args.size() > 1 else "")))
```

### File Structure
```
target/scripts/core/game_flow/campaign_system/
├── campaign_variables.gd       # Main variable management
├── variable_change.gd          # Change tracking structure
├── sexp_variable_interface.gd  # SEXP integration functions
└── variable_validator.gd       # Variable validation utilities
```

## Definition of Done

- [ ] **Code Quality**: All code follows GDScript static typing standards
  - [ ] 100% static typing with comprehensive type annotations
  - [ ] Efficient variable lookup and storage mechanisms
  - [ ] Proper error handling and validation
  - [ ] Memory-efficient change tracking

- [ ] **Testing**: Comprehensive test coverage
  - [ ] Variable type validation testing
  - [ ] Variable persistence testing (save/load cycles)
  - [ ] SEXP integration testing
  - [ ] Access control and permissions testing

- [ ] **Documentation**: Complete system documentation
  - [ ] Variable naming conventions and best practices
  - [ ] SEXP function reference for variables
  - [ ] Performance considerations and optimization guide
  - [ ] Debugging and troubleshooting guide

- [ ] **Integration**: Seamless integration with dependent systems
  - [ ] Campaign progression system integration
  - [ ] SEXP expression system integration
  - [ ] Save system integration for persistence
  - [ ] Debug UI integration for variable inspection

## Implementation Notes

### Variable Storage Strategy
- Use Dictionary for primary storage with metadata tracking
- Implement efficient lookup mechanisms for frequent access
- Support variable aliasing and references
- Include variable deprecation and migration support

### Performance Considerations
- Cache frequently accessed variables
- Use lazy evaluation for expensive variable operations
- Implement variable pooling for temporary variables
- Profile variable access patterns and optimize

### SEXP Integration
- Provide type-safe variable access functions
- Support variable references in expressions
- Implement variable modification tracking
- Ensure consistent variable state across evaluations

## Dependencies

### Prerequisite Stories
- **FLOW-004**: Campaign Progression and Mission Unlocking
- **EPIC-004**: SEXP Expression System (for integration)

### Dependent Stories
- **FLOW-006**: Mission Flow Integration (uses campaign variables)
- **FLOW-008**: Save Game System (persists variables)

## Testing Strategy

### Unit Tests
```gdscript
# test_campaign_variables.gd
func test_variable_type_validation():
    # Test type validation and conversion
    
func test_variable_access_control():
    # Test read/write permissions
    
func test_variable_persistence():
    # Test save/load functionality

# test_sexp_variable_interface.gd
func test_sexp_variable_functions():
    # Test SEXP function implementations
    
func test_variable_expressions():
    # Test variables in SEXP expressions
```

### Integration Tests
- End-to-end variable persistence testing
- SEXP expression evaluation with variables
- Campaign progression using variables
- Performance testing with large variable sets

---

**Story Ready for Implementation**: ✅  
**Architecture Reference**: Approved EPIC-007 architecture document  
**WCS Source Reference**: Campaign variable management across mission systems  
**Integration Complexity**: Medium - SEXP integration and persistence requirements  
**Estimated Development Time**: 2-3 days for experienced GDScript developer