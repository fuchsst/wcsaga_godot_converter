# STORY-005: Implement IFF Table Converter

## User Story
As an asset pipeline engineer, I want to convert iff_defs.tbl/.tbm files to Godot .tres resources so that IFF (Identification Friend or Foe) relationship definitions are available in the Godot engine.

## Epic Reference
[EPIC-001: Foundation Data Conversion (.tbl/.tbm → .tres)](../epics/EPIC-001-foundation-data-conversion.md)

## Godot Implementation
- Create an IFFTableConverter class that extends BaseTableConverter
- Parse IFF definitions with faction names, colors, and relationships
- Extract IFF properties (attitude, team names, color codes)
- Handle IFF relationship matrices (friendly, hostile, neutral states)
- Map parsed data to Godot Resource classes with exported variables
- Generate individual .tres files for each IFF definition following Godot conventions
- Organize output files in `/assets/campaigns/wing_commander_saga/factions/` directory

## Acceptance Criteria
- [ ] IFFTableConverter successfully parses iff_defs.tbl files with all properties
- [ ] TBM inheritance correctly merges with base IFF definitions
- [ ] All IFF properties and relationships are correctly extracted and validated
- [ ] IFF relationship matrices are properly maintained
- [ ] Individual .tres files are generated for each IFF definition
- [ ] Generated resources load correctly in Godot engine
- [ ] Cross-references to other table entries are maintained
- [ ] Format compliance with Godot .tres specifications is verified
- [ ] Unit tests cover all parsing and conversion functionality

## Definition of Done
- [ ] IFFTableConverter class implemented with full parsing capability
- [ ] Resource generation produces valid Godot .tres files
- [ ] Unit tests pass with >90% code coverage
- [ ] Integration tests verify end-to-end conversion process
- [ ] Documentation updated with usage examples
- [ ] Code reviewed and merged to main branch

## Agent Assignment
**asset-pipeline-engineer**: Implementation of table parsing and data extraction
**godot-systems-designer**: Resource mapping and Godot integration
**qa-engineer**: Testing and validation