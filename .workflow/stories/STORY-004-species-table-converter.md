# STORY-004: Implement Species Table Converter

## User Story
As an asset pipeline engineer, I want to convert species.tbl/.tbm files to Godot .tres resources so that species definitions and relationships are available in the Godot engine.

## Epic Reference
[EPIC-001: Foundation Data Conversion (.tbl/.tbm → .tres)](../epics/EPIC-001-foundation-data-conversion.md)

## Godot Implementation
- Create a SpeciesTableConverter class that extends BaseTableConverter
- Parse species definitions with naming, IFF relationships, and characteristics
- Extract species properties (government, weapon preferences, AI behavior modifiers)
- Handle species categorization and relationships to IFF definitions
- Map parsed data to Godot Resource classes with exported variables
- Generate individual .tres files for each species following Godot conventions
- Organize output files in `/assets/campaigns/wing_commander_saga/species/` directory

## Acceptance Criteria
- [ ] SpeciesTableConverter successfully parses species.tbl files with all properties
- [ ] TBM inheritance correctly merges with base species definitions
- [ ] All species properties are correctly extracted and validated
- [ ] Species relationships to IFF definitions are properly maintained
- [ ] Individual .tres files are generated for each species
- [ ] Generated resources load correctly in Godot engine
- [ ] Cross-references to other table entries are maintained
- [ ] Format compliance with Godot .tres specifications is verified
- [ ] Unit tests cover all parsing and conversion functionality

## Definition of Done
- [ ] SpeciesTableConverter class implemented with full parsing capability
- [ ] Resource generation produces valid Godot .tres files
- [ ] Unit tests pass with >90% code coverage
- [ ] Integration tests verify end-to-end conversion process
- [ ] Documentation updated with usage examples
- [ ] Code reviewed and merged to main branch

## Agent Assignment
**asset-pipeline-engineer**: Implementation of table parsing and data extraction
**godot-systems-designer**: Resource mapping and Godot integration
**qa_engineer**: Testing and validation