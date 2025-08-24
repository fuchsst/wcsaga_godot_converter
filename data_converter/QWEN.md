# WCS Data Migration & Conversion Tools - Qwen Context

Use `uv` to run tests

## Project Overview

This project implements a comprehensive data migration and conversion pipeline for the Wing Commander Saga (WCS) mod, designed to convert original WCS assets into Godot-compatible formats through a modular, multi-stage process. The pipeline processes table files (.tbl) into structured Godot resources, while model files (.POF) are handled separately, with a final scene assembly step that combines both data streams into complete, game-ready Godot scenes.

The system follows a separation of concerns architecture where table data conversion, model conversion, and scene assembly are distinct phases, enabling better maintainability and flexibility. The table conversion component is implemented as a Godot plugin with a unified wizard interface, following the architecture defined in EPIC-003.

## Key Components

### 1. Table Data Converter Orchestrator (`table_data_converter.py`)
Orchestrates the conversion of WCS table files (.tbl) to Godot resource formats (.tres) by delegating to specialized converter modules. Provides:
- Unified interface for table file processing
- Conversion statistics tracking
- Asset relationship mapping
- Error handling and reporting

### 2. Modular Table Converters (`table_converters/`)
Specialized converters for each table type that handle parsing and resource generation:
- **ShipTableConverter**: Processes ship classes with full physics, weapons, and visual properties
- **WeaponTableConverter**: Handles weapon definitions with damage, effects, and sound properties  
- **ArmorTableConverter**: Manages armor types with damage type modifiers
- **SpeciesTableConverter**: Processes species definitions with thruster animations
- **IFFTableConverter**: Handles IFF (faction) definitions with colors and relationships

### 3. Model Converter (Separate Component)
Handles conversion of .POF model files to glTF 2.0 format with preservation of all metadata points (gun mounts, thrusters, subsystems, etc.). This component operates independently and outputs glTF files with minimal extras for visual data.

### 4. Scene Assembly System
A follow-up process that combines outputs from both table and model converters. Uses entity names as matching keys to:
- Import glTF models as root nodes
- Apply physics properties from table data to RigidBody3D nodes
- Attach weapon mounts, thrusters, and other metadata as child nodes with appropriate scripts
- Configure materials and visual properties based on table data
- Output complete Godot scenes (.tscn) ready for gameplay

### 5. Asset Discovery Engine (`core/asset_discovery.py`)
Discovers all related assets for WCS entities by scanning the Hermes campaign structure. Features:
- Faction-based asset categorization (Terran, Kilrathi, Pirate, Border Worlds)
- Audio classification (pilot voices, engine sounds, weapon sounds, etc.)
- Material completeness validation (diffuse, normal, specular, emission maps)
- Mission reference detection

### 6. Data Structures (`core/table_data_structures.py`)
Defines core data structures for asset relationship mapping and scene assembly:
- `ShipClassData`: Complete ship class definition with all properties
- `WeaponData`: Weapon specifications and behavior data
- `ArmorTypeData`: Armor type definitions with damage modifiers
- `SpeciesData`: Species-specific properties and animations
- `IFFData`: Faction definitions and relationships

### 7. Godot Plugin (`ui_components/plugin.gd`)
Implements the Godot editor plugin with a unified wizard interface for the conversion pipeline, focusing on table data processing with hooks for scene assembly integration.

## Conversion Pipeline Architecture

The system follows a modular Load→Transform→Save pattern:

1. **Table Processing Phase**: 
   - Orchestrator identifies table type and delegates to appropriate converter
   - Modular converters parse .tbl files using dedicated logic for each table type
   - Output Godot resources (.tres) with complete gameplay properties
   - Maintain entity registry for later scene assembly

2. **Model Processing Phase**:
   - Convert .POF files to glTF 2.0 format
   - Preserve all metadata points as empty nodes in glTF hierarchy
   - Handle texture and material conversion with PBR approximation

3. **Scene Assembly Phase**:
   - Match table data with corresponding models using entity names
   - Create complete Godot scenes with physics, weapons, and visual properties
   - Generate collision shapes and configure gameplay components

## Building and Running

### Prerequisites
- Python 3.7+
- Godot 4.x
- Virtual environment (recommended)

### Dependencies
Listed in `requirements.txt`:
- numpy
- pytest
- pillow
- psutil

### Scripts
- `run_script.sh`: Runs Python modules within the conversion tools directory using the virtual environment
- `run_tests.sh`: Runs pytest within the conversion tools directory using the virtual environment

### Running the Table Converter
```bash
# Convert specific table file using the CLI tool
./run_script.sh tools.table_conversion_cli --source /path/to/wcs/source --target /path/to/godot/project --file ships.tbl

# Convert all table files
./run_script.sh tools.table_conversion_cli --source /path/to/wcs/source --target /path/to/godot/project

# Run all tests
./run_tests.sh
```

## Development Conventions

### Python Code Style
- Follows PEP 8 style guidelines
- Uses type hints for all function parameters and return values
- Data classes for structured data
- Comprehensive logging for debugging and monitoring

### Testing
- Uses pytest for unit testing
- Tests located in `tests/` directory
- Validates parsing functionality and data structure integrity
- Includes integration tests for scene assembly process

### Godot Integration
- Plugin architecture following Godot editor plugin guidelines
- Resource files in Godot's .tres format for table data
- Preloaded scenes and scripts for UI components
- Scene assembly outputs standard .tscn files

## Directory Structure
```
data_converter/
├── core/                 # Core conversion modules and data structures
├── mission_converter/    # Mission conversion tools
├── pof_parser/           # POF model parser (integration points)
├── resource_generators/  # Godot resource generators
├── scene_generators/     # Scene file generators for assembly
├── scene_templates/      # Scene templates for assembly
├── table_converters/     # Modular table file converters
├── tests/                # Unit tests
├── tools/                # Utility tools and CLI interface
├── table_data_converter.py  # Main orchestrator
├── plugin.cfg            # Godot plugin configuration
├── requirements.txt      # Python dependencies
├── run_script.sh         # Script runner
├── run_tests.sh          # Test runner
```

## Output Structure
- `assets/tables/`: Converted table data as Godot resources
- `assets/models/`: Converted glTF models (from separate model converter)
- `assets/scenes/`: Assembled Godot scenes combining table and model data

The pipeline ensures that all original WCS data is preserved and correctly mapped to Godot's systems, with entity names serving as the consistent key throughout the conversion and assembly process.