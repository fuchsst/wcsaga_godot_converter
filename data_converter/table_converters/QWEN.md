# Table Converters Module - WCS Table Data Processing

## Overview
The Table Converters module handles the parsing and conversion of WCS table files (.tbl) into structured intermediate data. This module consists of specialized converters for each table type, following a modular architecture that ensures complete fidelity to the original WCS data while preparing it for Godot integration.

## Key Components

### Specialized Converters
- **ShipTableConverter**: Processes ship classes with full physics, weapons, and visual properties from ships.tbl
- **WeaponTableConverter**: Handles weapon definitions with damage, effects, and sound properties from weapons.tbl
- **ArmorTableConverter**: Manages armor types with damage type modifiers from armor.tbl
- **SpeciesTableConverter**: Processes species definitions with thruster animations from species_defs.tbl
- **IFFTableConverter**: Handles IFF (faction) definitions with colors and relationships from iff_defs.tbl

### Core Infrastructure
- **ConverterFactory**: Dynamically selects the appropriate converter based on table file content
- **BaseConverter**: Abstract base class providing common parsing utilities and error handling
- **TableTypeRegistry**: Maintains metadata about supported table types and their handlers

## Conversion Process
1. **File Identification**: Determines table type through content analysis and filename patterns
2. **Modular Parsing**: Delegates to specialized converter for table-specific parsing logic
3. **Data Transformation**: Converts parsed data into intermediate structures for resource generation
4. **Relationship Mapping**: Establishes connections between entities for scene assembly

## Integration Points
- Populates core intermediate data structures with parsed table data
- Provides input for resource generators to create Godot resources
- Maintains entity registries for cross-reference during scene assembly
- Supports both .tbl base files and .tbm modular override files
