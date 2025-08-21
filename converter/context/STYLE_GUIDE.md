# Godot/GDScript Style Guide for Wing Commander Saga Migration

This document provides architectural style guidelines for the Wing Commander Saga to Godot migration project. All generated code should adhere to these principles to ensure consistency and maintainability.

## General Principles

1. **Idiomatic Godot Design**: All code should follow Godot's architectural patterns and best practices
2. **Performance Conscious**: Prioritize efficient code that maintains the game's performance characteristics
3. **Maintainability**: Write clear, well-documented code that can be easily understood and modified
4. **Consistency**: Follow established patterns throughout the codebase

## GDScript Coding Standards

### Naming Conventions

- **Classes/Nodes**: Use PascalCase (`PlayerShip`, `WeaponSystem`)
- **Variables**: Use snake_case (`player_ship`, `current_health`)
- **Constants**: Use CONSTANT_CASE (`MAX_SPEED`, `DEFAULT_WEAPON`)
- **Methods**: Use snake_case (`fire_weapon`, `calculate_damage`)
- **Signals**: Use snake_case with past tense (`health_depleted`, `target_acquired`)

### File Organization

```
# Preferred file structure
# 1. Tool declaration (if needed)
# 2. Class documentation
# 3. Class name
# 4. Extends statement
# 5. Signals
# 6. Enums
# 7. Constants
# 8. Exported variables
# 9. Public variables
# 10. Private variables (prefixed with _)
# 11. Onready variables
# 12. Static functions
# 13. Built-in virtual methods (_ready, _process, etc.)
# 14. Public methods
# 15. Private methods (prefixed with _)
```

### Documentation

- Use docstring comments for all public classes and methods
- Include parameter descriptions and return value information
- Document complex logic with inline comments

```gdscript
# Calculate damage based on weapon type and distance to target
# @param weapon_type: Type of weapon being fired
# @param distance: Distance to target in meters
# @returns: Damage value as a float
func calculate_damage(weapon_type: String, distance: float) -> float:
    # Implementation here
    pass
```

## Architecture Patterns

### Component-Based Design

Follow Godot's node-based component system:
- Use nodes to represent components
- Prefer composition over inheritance
- Leverage Godot's scene system for object composition

### State Management

- Use state machines for complex entity behavior
- Implement states as separate nodes or scripts
- Centralize state transitions through a state manager

### Event-Driven Communication

- Use Godot signals for inter-node communication
- Avoid tight coupling between components
- Implement observer patterns where appropriate

## Performance Guidelines

### Memory Management

- Reuse objects when possible
- Use object pooling for frequently created/destroyed objects
- Avoid unnecessary node creation/deletion in performance-critical sections

### Processing Efficiency

- Use `_physics_process` only for physics-related updates
- Use `_process` for non-physics game logic
- Implement frame skipping or interpolation for expensive operations

### Resource Handling

- Preload resources when possible
- Use resource caching to avoid duplicate loading
- Implement proper resource cleanup

## Migration-Specific Considerations

### C++ to GDScript Translation

1. **Data Types**:
   - Map C++ primitives to GDScript equivalents
   - Use Godot's built-in types (Vector3, Color, etc.) where appropriate
   - Implement custom classes for complex data structures

2. **Memory Management**:
   - Leverage GDScript's garbage collection
   - Remove explicit memory management code from C++
   - Use Godot's reference counting for resources

3. **Inheritance**:
   - Flatten deep inheritance hierarchies where possible
   - Use composition to replace multiple inheritance
   - Leverage Godot's node inheritance system

### Legacy System Integration

1. **Data Formats**:
   - Maintain compatibility with existing data files where possible
   - Implement converters for proprietary formats
   - Validate data during loading

2. **Game Logic Preservation**:
   - Ensure mathematical calculations produce identical results
   - Maintain timing-sensitive behaviors
   - Preserve random number generation sequences where critical

## Testing Standards

### Unit Testing

- Write tests for all public methods
- Use gdUnit4 framework for test implementation
- Include edge case testing
- Maintain high test coverage for core systems

### Integration Testing

- Test component interactions
- Validate scene compositions
- Verify signal connections and data flow

## Code Review Checklist

Before merging any generated code, ensure it meets these criteria:

- [ ] Follows naming conventions
- [ ] Includes appropriate documentation
- [ ] Uses Godot's architectural patterns
- [ ] Passes all unit tests
- [ ] Demonstrates acceptable performance
- [ ] Contains no hardcoded values (use constants)
- [ ] Handles errors gracefully
- [ ] Avoids code duplication
