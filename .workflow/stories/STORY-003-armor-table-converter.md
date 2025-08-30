# STORY-003: Implement Armor Table Converter

## User Story
As an asset pipeline engineer, I want to convert armor.tbl/.tbm files to Godot .tres resources so that armor type definitions are available in the Godot engine with damage reduction properties.

## Epic Reference
[EPIC-001: Foundation Data Conversion (.tbl/.tbm → .tres)](../epics/EPIC-001-foundation-data-conversion.md)

## Godot Implementation
- Create an ArmorTableConverter class that extends BaseTableConverter
- Parse armor type definitions with damage type reduction values
- Extract armor properties for different damage types (hull, shield, etc.)
- Handle armor type naming and categorization
- Map parsed data to Godot Resource classes with exported variables
- Generate individual .tres files for each armor type following Godot conventions
- Organize output files in `/assets/campaigns/wing_commander_saga/armor/` directory

## Acceptance Criteria
- [ ] ArmorTableConverter successfully parses armor.tbl files with all properties
- [ ] TBM inheritance correctly merges with base armor definitions
- [ ] All damage reduction properties are correctly extracted and validated
- [ ] Armor type categorization is properly maintained
- [ ] Individual .tres files are generated for each armor type
- [ ] Generated resources load correctly in Godot engine
- [ ] Cross-references to other table entries are maintained
- [ ] Format compliance with Godot .tres specifications is verified
- [ ] Unit tests cover all parsing and conversion functionality

## Definition of Done
- [ ] ArmorTableConverter class implemented with full parsing capability
- [ ] Resource generation produces valid Godot .tres files
- [ ] Unit tests pass with >90% code coverage
- [ ] Integration tests verify end-to-end conversion process
- [ ] Documentation updated with usage examples
- [ ] Code reviewed and merged to main branch

## Agent Assignment
**asset-pipeline-engineer**: Implementation of table parsing and data extraction
**godot-systems-designer**: Resource mapping and Godot integration
**qa_engineer**: Testing and validation