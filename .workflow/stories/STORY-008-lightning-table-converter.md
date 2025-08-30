# STORY-008: Implement Lightning Table Converter

## User Story
As an asset pipeline engineer, I want to convert lightning.tbl/.tbm files to Godot .tres resources so that lightning/electrical effect definitions are available in the Godot engine.

## Epic Reference
[EPIC-001: Foundation Data Conversion (.tbl/.tbm → .tres)](../epics/EPIC-001-foundation-data-conversion.md)

## Godot Implementation
- Create a LightningTableConverter class that extends BaseTableConverter
- Parse lightning definitions with electrical effect characteristics and parameters
- Extract lightning properties (animation files, sound effects, damage parameters)
- Handle lightning categorization and effect associations
- Map parsed data to Godot Resource classes with exported variables
- Generate individual .tres files for each lightning type following Godot conventions
- Organize output files in `/assets/campaigns/wing_commander_saga/effects/lightning/` directory

## Acceptance Criteria
- [ ] LightningTableConverter successfully parses lightning.tbl files with all properties
- [ ] TBM inheritance correctly merges with base lightning definitions
- [ ] All lightning characteristics are correctly extracted and validated
- [ ] Lightning categorization and effect associations are properly maintained
- [ ] Individual .tres files are generated for each lightning type
- [ ] Generated resources load correctly in Godot engine
- [ ] Cross-references to other table entries are maintained
- [ ] Format compliance with Godot .tres specifications is verified
- [ ] Unit tests cover all parsing and conversion functionality

## Definition of Done
- [ ] LightningTableConverter class implemented with full parsing capability
- [ ] Resource generation produces valid Godot .tres files
- [ ] Unit tests pass with >90% code coverage
- [ ] Integration tests verify end-to-end conversion process
- [ ] Documentation updated with usage examples
- [ ] Code reviewed and merged to main branch

## Agent Assignment
**asset-pipeline-engineer**: Implementation of table parsing and data extraction
**godot-systems-designer**: Resource mapping and Godot integration
**qa_engineer**: Testing and validation