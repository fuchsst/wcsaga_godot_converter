# task-005: Implement TBM inheritance and override system

## Status
pending

## Description
Create TBM inheritance and override system to properly merge base weapon definitions with modular TBM overrides. Handle inheritance chains and property merging with proper precedence rules.

## Dependencies
- task-001
- task-002
- task-003
- task-004

## Agent Assignment
**code-analyst**: Implementation of inheritance and override logic

## Complexity
High

## Files to Modify
- `data_converter/table_converters/weapon_table_converter.py`
- `data_converter/utils/tbm_merger.py`

## Validation Criteria
- [ ] TBM inheritance correctly merges with base weapon definitions
- [ ] Property precedence rules are properly implemented
- [ ] Circular inheritance is detected and prevented
- [ ] Unit tests validate inheritance merging logic

## Estimated Hours
4