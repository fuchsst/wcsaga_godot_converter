# EPIC-003: Data Migration & Conversion Tools - Godot Files

**Epic**: EPIC-003 - Data Migration & Conversion Tools  
**Architect**: Mo (Godot Architect)  
**Version**: 2.0 (Simplified based on WCS source analysis)  
**Date**: 2025-01-27  

## Overview

Data migration and conversion tools for transforming WCS assets into Godot-native formats. **Architectural Insight**: Analysis of 27 WCS conversion-related files reveals **exceptionally clean architecture** with minimal dependencies, enabling dramatically simplified implementation.

**Key Discovery**: WCS format parsers are self-contained and independent, allowing parallel development and eliminating complex dependency management.

## Simplified Implementation Structure

### Total Files: ~20-25 (vs original estimate of 67)

**Reduction Rationale**: Clean WCS architecture eliminates need for complex dependency resolution, validation pipelines, and custom tooling.

## Core Conversion Scripts (Python-Based)

### `conversion_tools/` (Standalone Python Scripts)

#### VP Archive Extraction
- `vp_extractor.py`: VP archive extraction (self-contained, based on WCS cfilearchive.cpp)
- `vp_format_parser.py`: VP file format definitions and parsing

```python
# vp_extractor.py - Direct from WCS source implementation
class VPExtractor:
    """VP archive extractor based on WCS cfilearchive.cpp analysis"""
    
    def extract_vp_archive(self, vp_path: str, output_dir: str) -> bool:
        # Direct implementation of WCS decompression algorithm
        # Self-contained - no external dependencies
        pass
```

#### Image Format Conversion  
- `image_converter.py`: Unified converter for all 5 WCS image formats
- `image_format_parsers.py`: Format-specific parsers (PCX, TGA, JPEG, PNG, DDS)

```python
# image_converter.py - Unified converter (identical patterns identified)
class ImageConverter:
    """Converts all WCS image formats to PNG using identical parsing patterns"""
    
    def convert_pcx_to_png(self, pcx_path: str) -> str:
        # Based on WCS pcxutils.cpp analysis
        pass
    
    def convert_tga_to_png(self, tga_path: str) -> str:
        # Based on WCS tgautils.cpp analysis
        pass
    
    # Similar methods for JPEG, PNG, DDS (all follow identical pattern)
```

#### POF Model Conversion
- `pof_converter.py`: POF to Godot scene converter (based on WCS modelread.cpp)
- `pof_format_parser.py`: POF file format definitions and parsing

```python
# pof_converter.py - Complex but isolated (from WCS analysis)
class POFConverter:
    """POF model converter based on WCS modelread.cpp analysis"""
    
    def convert_pof_to_tscn(self, pof_path: str) -> str:
        # Direct implementation of WCS POF parsing algorithm
        # Isolated system - no external dependencies
        pass
```

#### Table Data Conversion  
- `table_converter.py`: WCS .tbl files to Godot resources
- `table_parser.py`: Table parsing utilities (based on WCS parselo.cpp)

```python
# table_converter.py - Simple text parsing (from WCS analysis)
class TableConverter:
    """Converts WCS .tbl files to Godot .tres resources"""
    
    def convert_ships_tbl(self, tbl_path: str) -> str:
        # Based on WCS parselo.cpp analysis
        # Simple text parsing - no complex dependencies
        pass
```

#### Mission File Conversion
- `mission_converter.py`: Mission file to Godot scene converter
- `sexp_parser.py`: SEXP expression parsing (text-based)

#### Batch Processing
- `batch_converter.py`: Orchestrates all conversion operations
- `conversion_manager.py`: Progress tracking and error handling

## Godot Import Plugins (Minimal Integration)

### `addons/wcs_importers/` (Native Godot Integration)

#### Plugin Configuration  
- `plugin.cfg`: Import plugin metadata
- `plugin.gd`: Main import plugin registration

#### Import Plugins (Self-Contained)
- `vp_import_plugin.gd`: VP archive import plugin
- `pof_import_plugin.gd`: POF model import plugin  
- `table_import_plugin.gd`: Table data import plugin

```gdscript
# pof_import_plugin.gd - Godot import integration
@tool
extends EditorImportPlugin

func _get_importer_name():
    return "wcs.pof"

func _get_visible_name():
    return "WCS POF Model"

func _import(source_file: String, save_path: String, options: Dictionary, platform_variants: Array, gen_files: Array) -> Error:
    # Call Python POF converter, load result as Godot scene
    # Simple wrapper - complex logic in Python script
    pass
```

## Validation and Utilities

### `validation/` (Lightweight Validation)
- `format_validator.py`: Basic format validation (minimal - WCS parsers are robust)
- `conversion_reporter.py`: Conversion results and statistics

### `utilities/` (Helper Functions)
- `path_utils.py`: File path and directory utilities
- `progress_tracker.py`: Conversion progress reporting

## Configuration and Data

### `config/` (Simple Configuration)
- `conversion_config.json`: Conversion settings and output paths
- `format_mappings.json`: WCS to Godot format mapping definitions

### `templates/` (Output Templates)
- `ship_resource_template.gd`: Template for ship resource generation
- `weapon_resource_template.gd`: Template for weapon resource generation

## Testing Infrastructure (Minimal)

### `tests/` (Essential Tests Only)
- `test_vp_extraction.py`: VP archive extraction validation
- `test_pof_conversion.py`: POF model conversion validation
- `test_image_conversion.py`: Image format conversion validation
- `test_table_parsing.py`: Table data parsing validation

## Implementation Priority

### Phase 1: Core Extractors (Week 1)
1. `vp_extractor.py` - VP archive extraction (foundational)
2. `image_converter.py` - Image format conversion (parallel development)
3. `batch_converter.py` - Basic orchestration

### Phase 2: Model and Data Conversion (Week 2)  
1. `pof_converter.py` - 3D model conversion
2. `table_converter.py` - Configuration data conversion
3. `conversion_manager.py` - Progress tracking

### Phase 3: Mission and Advanced Features (Week 3)
1. `mission_converter.py` - Mission file conversion
2. `sexp_parser.py` - Expression parsing
3. Godot import plugins integration

### Phase 4: Integration and Polish (Week 4)
1. Import plugin testing and refinement
2. Validation and error handling
3. Documentation and user guides

## File Count Comparison

### Original Estimate vs Reality
- **Original Estimate**: 67 files (complex dependency management)
- **Actual Implementation**: ~25 files (clean WCS architecture)
- **Reduction**: 63% fewer files needed

### Complexity Reduction
- **Eliminated**: Complex dependency resolution systems
- **Eliminated**: Custom validation pipelines  
- **Eliminated**: Format detection engines
- **Simplified**: Direct implementation from WCS source algorithms

## Mo's Architectural Notes

**WCS Analysis Benefits**:
- **Self-Contained Parsers**: Each format parser is independent (27 files, minimal dependencies)
- **Identical Patterns**: Image format utilities follow identical patterns (trivial to implement)
- **Clean Separation**: VP archives, POF parsing, table parsing are completely isolated
- **Direct Implementation**: WCS source provides exact algorithms - no reverse engineering needed

**Python Implementation Strategy**:
- **Standalone Scripts**: No complex framework needed - simple Python scripts
- **Parallel Development**: Independent converters can be developed simultaneously
- **Godot Integration**: Minimal import plugins for editor integration
- **No External Dependencies**: Most conversions can be pure Python

**Quality Standards**:
- Each converter is self-contained and testable
- Direct implementation from WCS source ensures accuracy
- Minimal external dependencies reduce complexity
- Godot import plugins provide seamless editor integration

**Performance Confidence**:
- Conversion is one-time operation - performance not critical
- Clean architecture enables efficient implementation
- Parallel processing possible for large asset sets
- No complex optimization needed

---

**Implementation Confidence**: This simplified architecture leverages the exceptionally clean WCS conversion codebase to deliver robust migration tools with minimal complexity. Achievable in 4-6 weeks with high reliability.