# task-002: Implement comprehensive weapon physics and damage property parsing

## Status
pending

## Description
Add parsing logic for all weapon physics properties including damage statistics (hull, armor, shield damage factors), firing properties (rate of fire, energy consumption, heat generation), and projectile characteristics (muzzle velocity, lifetime, range). Ensure proper type conversion and validation.

## Dependencies
- task-001

## Agent Assignment
**code-analyst**: Implementation of physics property parsing logic

## Complexity
High

## Files to Modify
- `data_converter/table_converters/weapon_table_converter.py`

## Validation Criteria
- [ ] All damage properties are correctly extracted from weapons.tbl files
- [ ] Type conversion is properly handled for numeric values
- [ ] Projectile characteristics are parsed accurately
- [ ] Unit tests validate physics parsing with sample weapon data

## Estimated Hours
5