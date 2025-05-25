Guide the GDScript implementation of an approved user story for WCS-Godot conversion.

You are initiating implementation for the story: $ARGUMENTS

## Implementation Process

### 1. Load BMAD Framework
- Load the GDScript Developer persona (Dev) from `.bmad/personas/gdscript-developer.md`
- Reference the story file from `.ai/stories/[story-name].md`
- Review the architecture document for technical specifications

### 2. Prerequisites Check (CRITICAL - MUST FOLLOW)
Before starting ANY implementation, verify:
- [ ] Story exists and is approved in `.ai/stories/[story-name].md`
- [ ] Architecture document exists and is approved
- [ ] All story dependencies are completed
- [ ] Story has clear, testable acceptance criteria
- [ ] Technical requirements are well-defined
- [ ] Original C++ source code has been identified and analyzed

**VIOLATION CHECK**: If any prerequisite is missing, STOP and complete required phase first.

### 3. Implementation Steps
Follow Dev's methodical approach:

1. **C++ Source Code Analysis** (MANDATORY)
   - Read and analyze the original C++ implementation from `source/code/` directory
   - Document all functions, classes, and data structures involved
   - Identify key algorithms, logic flows, and behavioral patterns
   - Note performance characteristics and optimization techniques
   - Extract configuration parameters, constants, and default values
   - Understand edge cases and error handling in original code
   - Document findings in implementation notes for reference

2. **Architecture First**
   - Always understand the architectural design before coding
   - Reference specific architecture components and patterns
   - Ensure implementation aligns with approved design
   - Validate technical approach against architecture
   - Map C++ components to Godot architecture patterns

3. **Type Everything**
   - Start with proper type declarations and work from there
   - ALL variables, parameters, and return types must be explicitly typed
   - Use `class_name` declarations for reusable classes
   - Follow snake_case for variables/functions, PascalCase for classes

4. **Test-Driven Development**
   - Write GUT tests before or alongside implementation
   - Ensure tests cover all acceptance criteria
   - Test edge cases and error scenarios identified in C++ analysis
   - Aim for 80% test coverage minimum

5. **Incremental Implementation**
   - Build and test small pieces at a time
   - Validate each component against original C++ behavior
   - Follow story tasks in order
   - Document implementation decisions and deviations from original

6. **Final check against C++ source code**
   - Compare the Godot implementation in the target forlder to the equivalent C++ code in the source folder
   - Give feedback on the current feature coverage in Godot
   

### 4. GDScript Coding Standards (NON-NEGOTIABLE)
- **Static Typing Always**: Every variable, parameter, and return type must be explicitly typed
- **Class Names**: Always use `class_name` declarations for reusable classes
- **Documentation**: Every public function MUST have a docstring
- **Error Handling**: Proper error checking and graceful failure handling
- **Resource Management**: Proper use of preload vs load, and resource cleanup
- **Signal Declarations**: Properly typed signal declarations with clear documentation

### 5. Godot Implementation Patterns
```gdscript
class_name WCSSystemComponent
extends Node

## Brief description of the component's purpose and role in WCS conversion.
## Handles [specific functionality] while maintaining WCS gameplay feel.

signal component_ready()
signal state_changed(new_state: String)

@export var max_value: float = 100.0
@export var update_rate: float = 60.0

var current_state: String = "idle"
var is_initialized: bool = false

func _ready() -> void:
    _initialize_component()
    component_ready.emit()

func _initialize_component() -> void:
    # Implementation with proper error handling
    pass
```

### 6. Quality Validation
Run the Definition of Done checklist:
- [ ] All acceptance criteria met and verified
- [ ] Code follows GDScript standards (static typing, documentation)
- [ ] Unit tests written and passing with adequate coverage
- [ ] Performance targets achieved and validated
- [ ] Integration testing completed successfully
- [ ] Code reviewed and approved
- [ ] Documentation updated (code comments, API docs)
- [ ] Feature validated against original WCS behavior (if applicable)

### 7. Testing Requirements
- **Unit Tests**: Test individual functions and methods in isolation
- **Integration Tests**: Test how components work together
- **Performance Tests**: Verify code meets performance requirements
- **Edge Case Testing**: Test boundary conditions and error scenarios

### 8. Output Requirements
Produce production-ready GDScript:
- **Location**: `target/` submodule following Godot project structure
- **Quality**: All code meets static typing and documentation standards
- **Testing**: Comprehensive test coverage using GUT framework
- **Documentation**: Clear docstrings and implementation notes
- **Package Documentation**: Create `CLAUDE.md` file for significant code packages/modules

### 9. Package Documentation Requirements
For each significant code package/module created in `target/`, create a `CLAUDE.md` file containing:
- **Package Purpose**: What this package does and why it exists
- **Original C++ Analysis**: Summary of original WCS C++ code analyzed and key findings
- **Key Classes**: Main classes and their responsibilities  
- **Usage Examples**: How other developers should use this package
- **Architecture Notes**: Important design decisions and patterns
- **C++ to Godot Mapping**: How original C++ components map to Godot implementation
- **Integration Points**: How this package connects with other systems
- **Performance Considerations**: Any performance-critical aspects
- **Testing Notes**: How to test this package and any special considerations
- **Implementation Deviations**: Any intentional differences from original C++ behavior and justifications

## Critical Reminders (Dev's Standards)
- You're not just writing code - you're crafting maintainable, performant, and elegant GDScript
- Every line matters for the WCS-Godot conversion foundation
- No untyped variables or functions allowed
- Test coverage is mandatory, not optional
- Code must feel natural in Godot ecosystem
- Performance implications must be considered

## BMAD Workflow Compliance
- **Prerequisites**: Story must be approved before implementation
- **Quality Gates**: All Definition of Done criteria must be met
- **Testing**: Unit tests are mandatory for all public methods
- **Documentation**: Code documentation must be complete
- **Review**: Code review required before story completion

## WCS-Specific Implementation Guidelines
- **Feature Parity**: Maintain WCS gameplay feel and behavior
- **Performance**: Meet or exceed original WCS performance
- **Architecture**: Follow approved Godot-native design patterns
- **Integration**: Ensure compatibility with other converted systems
- **Quality**: Code must be maintainable and extensible

Begin implementation for story: $ARGUMENTS

Remember: You're crafting the foundation for the entire WCS-Godot conversion. Every line of code must meet the highest standards of quality, performance, and maintainability.
