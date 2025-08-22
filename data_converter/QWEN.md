# WCS Data Migration & Conversion Tools - Qwen Context

## Project Overview

This project is a comprehensive data migration and conversion pipeline for the Wing Commander Saga (WCS) mod, designed to convert original WCS assets into Godot-compatible formats. The pipeline processes table files (ships, weapons, armor, species, factions), discovers related assets (models, textures, sounds), and generates Godot resource files.

The system is implemented as a Godot plugin with a unified wizard interface, following the architecture defined in EPIC-003.

## Key Components

### 1. Table Data Converter (`table_data_converter.py`)
Converts WCS table files (.tbl) to Godot resource formats (.tres) with complete fidelity to the original C++ parsing implementation. Handles:
- Ship classes with full physics, weapons, and visual properties
- Weapon definitions with damage, effects, and sound properties
- Armor types with damage type modifiers
- Species definitions with thruster animations
- IFF (faction) definitions with colors and relationships

### 2. Asset Discovery Engine (`core/asset_discovery.py`)
Discovers all related assets for WCS entities by scanning the Hermes campaign structure. Features:
- Faction-based asset categorization (Terran, Kilrathi, Pirate, Border Worlds)
- Audio classification (pilot voices, engine sounds, weapon sounds, etc.)
- Material completeness validation (diffuse, normal, specular, emission maps)
- Mission reference detection

### 3. Data Structures (`data_structures.py`)
Defines core data structures for asset relationship mapping:
- `AssetRelationship`: Represents a relationship between source asset and target conversion
- `AssetMapping`: Complete asset mapping with all relationships

### 4. Godot Plugin (`ui_components/plugin.gd`)
Implements the Godot editor plugin with a unified wizard interface for the conversion pipeline.

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

### Running the Converter
```bash
# Convert specific table file
./run_script.sh table_data_converter --source /path/to/wcs/source --target /path/to/godot/project --file ships.tbl

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

### Godot Integration
- Plugin architecture following Godot editor plugin guidelines
- Resource files in Godot's .tres format
- Preloaded scenes and scripts for UI components

## Directory Structure
```
data_converter/
├── core/                 # Core conversion modules
├── mission_converter/    # Mission conversion tools
├── pof_parser/           # POF model parser
├── resource_generators/  # Godot resource generators
├── scene_generators/     # Scene file generators
├── scene_templates/      # Scene templates
├── table_converters/     # Table file converters
├── tests/                # Unit tests
├── tools/                # Utility tools
├── ui_components/        # Godot UI components
├── data_structures.py    # Core data structures
├── table_data_converter.py  # Main table converter
├── plugin.cfg            # Godot plugin configuration
├── requirements.txt      # Python dependencies
├── run_script.sh         # Script runner
├── run_tests.sh          # Test runner
```