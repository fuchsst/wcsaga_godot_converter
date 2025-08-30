# STORY-007: Implement Fireballs Table Converter

## User Story
As an asset pipeline engineer, I want to convert fireball.tbl/.tbm files to Godot .tres resources so that fireball/explosion effect definitions are available in the Godot engine.

## Epic Reference
[EPIC-001: Foundation Data Conversion (.tbl/.tbm → .tres)](../epics/EPIC-001-foundation-data-conversion.md)

## Godot Implementation
- Create a FireballTableConverter class that extends BaseTableConverter
- Parse fireball definitions with explosion characteristics and parameters
- Extract fireball properties (animation files, damage parameters, sound effects)
- Handle fireball categorization and effect associations
- Map parsed data to Godot Resource classes with exported variables
- Generate individual .tres files for each fireball type following Godot conventions
- Organize output files in `/assets/campaigns/wing_commander_saga/effects/fireballs/` directory

## Acceptance Criteria
- [ ] FireballTableConverter successfully parses fireball.tbl files with all properties
- [ ] TBM inheritance correctly merges with base fireball definitions
- [ ] All fireball characteristics are correctly extracted and validated
- [ ] Fireball categorization and effect associations are properly maintained
- [ ] Individual .tres files are generated for each fireball type
- [ ] Generated resources load correctly in Godot engine
- [ ] Cross-references to other table entries are maintained
- [ ] Format compliance with Godot .tres specifications is verified
- [ ] Unit tests cover all parsing and conversion functionality

## Definition of Done
- [ ] FireballTableConverter class implemented with full parsing capability
- [ ] Resource generation produces valid Godot .tres files
- [ ] Unit tests pass with >90% code coverage
- [ ] Integration tests verify end-to-end conversion process
- [ ] Documentation updated with usage examples
- [ ] Code reviewed and merged to main branch

## Agent Assignment
**asset-pipeline-engineer**: Implementation of table parsing and data extraction
**godot-systems-designer**: Resource mapping and Godot integration
**qa-engineer**: Testing and validation