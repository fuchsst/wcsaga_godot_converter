# Tools Module - Conversion Pipeline Utilities

## Overview
The Tools module provides command-line interfaces and utility scripts for operating the WCS to Godot conversion pipeline. This module offers user-friendly access to the conversion system, handling asset discovery, batch processing, and integration with the Godot editor plugin.

## Key Components

### Command-Line Interfaces
- **TableConversionCLI**: Main command-line tool for converting table files with support for specific files or batch processing
- **VPExtractor**: Utility for extracting assets from WCS .vp package files for conversion
- **AssetMapper**: Tool for scanning and mapping asset relationships across the campaign structure

### Utility Scripts
- **RunScript**: Unified script runner that handles virtual environment activation and module execution
- **RunTests**: Test execution script for running pytest within the conversion tools directory
- **ConfigMigrator**: Handles configuration migration and project setup tasks

## Usage Examples

### Converting Table Files
```bash
# Convert specific table file
./run_script.sh tools.table_conversion_cli --source /path/to/wcs/source --target /path/to/godot/project --file ships.tbl

# Convert all table files in directory
./run_script.sh tools.table_conversion_cli --source /path/to/wcs/source --target /path/to/godot/project

# Extract assets from VP files
./run_script.sh tools.vp_extractor --input /path/to/data.vp --output /path/to/extracted/assets
```

### Running Tests
```bash
# Run all tests
./run_tests.sh

# Run specific test module
./run_tests.sh tests/table_converters/
```

## Integration Points
- Provides user-facing access to the conversion pipeline
- Integrates with virtual environment for dependency management
- Supports both interactive and batch processing modes
- Works with Godot editor plugin for seamless workflow integration