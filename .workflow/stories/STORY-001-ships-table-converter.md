# STORY-001: Implement Ships Table Converter

## User Story
As an asset pipeline engineer, I want to convert ships.tbl/.tbm files to Godot .tres resources so that ship definitions are available in the Godot engine with all their properties and relationships.

## Epic Reference
[EPIC-001: Foundation Data Conversion (.tbl/.tbm → .tres)](../epics/EPIC-001-foundation-data-conversion.md)

## Implementation Tasks
- [task-001](../tasks/task-001-refactor-shiptableconverter.md): Refactor ShipTableConverter class with SOLID principles
- [task-002](../tasks/task-002-physics-parsing.md): Implement comprehensive ship physics property parsing
- [task-003](../tasks/task-003-weapon-bank-parsing.md): Implement weapon bank configuration parsing
- [task-004](../tasks/task-004-asset-reference-mapping.md): Implement asset reference extraction and mapping
- [task-006](../tasks/task-006-godot-generation.md): Implement ShipClassGenerator and Godot .tres file generation

## Godot Implementation
- Create a ShipTableConverter class that extends BaseTableConverter following SOLID principles
- Parse ship class definitions with comprehensive properties (physics, weapons, models, audio, effects)
- Extract all physics properties (mass, density, max velocity, acceleration, afterburner stats)
- Process weapon bank configurations (primary/secondary weapon allocations and capacities)
- Handle 3D model references (POF files) and cockpit models with proper asset mapping
- Extract audio asset references (engine sounds, alive/dead sounds, warp sounds)
- Capture visual effect references (explosions, thrusters, warp animations, shockwaves)
- Process UI asset references (ship icons, overhead views, tech database assets)
- Map parsed data to Godot Resource classes with exported variables using ShipClassGenerator
- Generate individual .tres files for each ship class following Godot feature-based organization
- Organize output files in `/features/fighters/{faction}/{ship_name}/{ship_name}.tres` for fighters and `/features/capital_ships/{faction}/{ship_name}/{ship_name}.tres` for capital ships per concept guidelines

## Acceptance Criteria
- [x] ShipTableConverter successfully parses ships.tbl files with all properties following regex-based parsing
- [x] All physics properties are correctly extracted and validated with proper type conversion
- [x] Weapon bank configurations are properly parsed and stored as structured data
- [x] Model and audio asset references are captured for comprehensive asset mapping
- [x] Individual .tres files are generated for each ship class with proper directory structure
- [x] Generated resources load correctly in Godot engine with valid resource format
- [x] Cross-references to other table entries are maintained through relationship mapping
- [x] Format compliance with Godot .tres specifications is verified through validation
- [x] Unit tests cover all parsing and conversion functionality with >90% coverage

## Definition of Done
- [x] ShipTableConverter class implemented with full parsing capability following BaseTableConverter patterns
- [x] Resource generation produces valid Godot .tres files in feature-based directory structure
- [x] Asset relationship mapping created for all model, audio, and effect references
- [x] Unit tests pass with >90% code coverage using pytest framework
- [x] Integration tests verify end-to-end conversion process
- [x] Documentation updated with usage examples and implementation details
- [x] Code reviewed and merged to main branch following quality gates

## Agent Assignment
**asset-pipeline-engineer**: Implementation of table parsing and data extraction
**godot-systems-designer**: Resource mapping and Godot integration following feature-based organization
**qa-engineer**: Testing and validation with comprehensive test coverage