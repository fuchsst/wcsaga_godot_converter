# task-005: Implement WeaponResourceGenerator and Godot .tres file generation

## Status
pending

## Description
Create WeaponResourceGenerator to map parsed data to Godot Resource classes with exported variables. Generate individual .tres files for each weapon type following Godot feature-based organization in /features/weapons/{weapon_name}/ directories.

## Dependencies
- task-002
- task-003
- task-004

## Agent Assignment
**godot-integration-specialist**: Implementation of Godot resource generation

## Complexity
Medium

## Files to Modify
- `data_converter/resource_generators/weapon_resource_generator.py`
- `data_converter/table_converters/weapon_table_converter.py`

## Validation Criteria
- [ ] WeaponResourceGenerator properly maps data to Godot Resource format
- [ ] Individual .tres files are generated for each weapon type
- [ ] File organization follows /features/weapons/{weapon_name}/ structure
- [ ] Generated resources load correctly in Godot engine
- [ ] Format compliance with Godot .tres specifications is verified

## Estimated Hours
3