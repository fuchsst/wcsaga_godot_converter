# STORY-006: Implement AI Profiles Table Converter

## User Story
As an asset pipeline engineer, I want to convert ai_profiles.tbl/.tbm files to Godot .tres resources so that AI behavior characteristics and combat parameters are available in the Godot engine.

## Epic Reference
[EPIC-001: Foundation Data Conversion (.tbl/.tbm → .tres)](../epics/EPIC-001-foundation-data-conversion.md)

## Godot Implementation
- Create an AIProfilesTableConverter class that extends BaseTableConverter
- Parse AI profile definitions with behavior characteristics and parameters
- Extract AI properties (combat aggressiveness, tactical preferences, skill levels)
- Handle AI profile categorization and species associations
- Map parsed data to Godot Resource classes with exported variables
- Generate individual .tres files for each AI profile following Godot conventions
- Organize output files in `/assets/campaigns/wing_commander_saga/ai/` directory

## Acceptance Criteria
- [ ] AIProfilesTableConverter successfully parses ai_profiles.tbl files with all properties
- [ ] TBM inheritance correctly merges with base AI profile definitions
- [ ] All AI behavior characteristics are correctly extracted and validated
- [ ] AI profile categorization and species associations are properly maintained
- [ ] Individual .tres files are generated for each AI profile
- [ ] Generated resources load correctly in Godot engine
- [ ] Cross-references to other table entries are maintained
- [ ] Format compliance with Godot .tres specifications is verified
- [ ] Unit tests cover all parsing and conversion functionality

## Definition of Done
- [ ] AIProfilesTableConverter class implemented with full parsing capability
- [ ] Resource generation produces valid Godot .tres files
- [ ] Unit tests pass with >90% code coverage
- [ ] Integration tests verify end-to-end conversion process
- [ ] Documentation updated with usage examples
- [ ] Code reviewed and merged to main branch

## Agent Assignment
**asset-pipeline-engineer**: Implementation of table parsing and data extraction
**godot-systems-designer**: Resource mapping and Godot integration
**qa_engineer**: Testing and validation