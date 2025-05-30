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

### `res://conversion_tools/` (Standalone Python Scripts)

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

### `res://addons/wcs_converter/` (Native Godot Integration)

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

## Validation Framework

### `res://validation_framework/` (Quality Validation System)
- `comprehensive_validation_manager.gd`: Central validation coordination
- `asset_integrity_validator.gd`: Asset validation and verification  
- `visual_fidelity_validator.gd`: Visual quality assessment
- `comprehensive_validator.py`: Python validation utilities
- `validation_report_generator.gd`: Validation reporting system

### `res://conversion_tools/` (Helper Functions)
- `conversion_manager.py`: Conversion coordination
- `asset_catalog.py`: Asset inventory management
- Python dependencies defined in `requirements.txt`

## Converted Assets and Resources

### `res://assets/` (Converted WCS Assets)
- `hermes_cbanims/`: Converted animation frames
- `hermes_core/`: Core squadron and pilot images  
- `hermes_effects/`: UI effects and HUD elements

### `res://resources/` (Generated by Migration Scripts)
- `game_sounds.tres`: Audio resource definitions
- `pilot_tips.tres`: Pilot tip database
- `brightness_test.gdshader`: Graphics testing shader

### Resource Templates (Located in Asset Core Addon)
- Ship and weapon templates in `addons/wcs_asset_core/resources/ship_weapon/`
- Mission templates in `addons/wcs_asset_core/resources/mission/`

## Testing Infrastructure

### `res://tests/` (GDUnit4 Integration)
- `test_config_migration.gd`: Configuration migration tests
- `test_mission_data_validation.gd`: Mission data validation tests
- `test_table_data_converter.gd`: Data conversion tests

### `res://conversion_tools/tests/` (Python Tests)
- Python unit tests for conversion utilities
- VP extraction and POF conversion validation
- Image format conversion testing
- Table data parsing validation

## Implementation Priority

### Phase 1: Core Conversion Pipeline (Week 1)
1. `convert_wcs_assets.py` - Main conversion script
2. `vp_extractor.py` - VP archive extraction (foundational)
3. `conversion_manager.py` - Conversion coordination

### Phase 2: Asset Processing (Week 2)
1. `table_data_converter.py` - Game table conversion
2. `config_migrator.py` - Configuration migration
3. `asset_catalog.py` - Asset inventory management

### Phase 3: Validation Framework (Week 3)
1. `comprehensive_validation_manager.gd` - Central validation
2. `asset_integrity_validator.gd` - Asset validation
3. `validation_report_generator.gd` - Reporting system

### Phase 4: Integration and Quality Assurance (Week 4)
1. Godot addon integration (`wcs_converter`)
2. Visual fidelity validation
3. Complete pipeline testing and optimization

## File Count Comparison

### Original Estimate vs Reality
- **Original Estimate**: 67 files (complex dependency management)
- **Actual Implementation**: ~20 files (clean WCS architecture)
- **Core Conversion Tools**: 6-8 Python scripts in `conversion_tools/`
- **Validation Framework**: 5-6 GDScript files in `validation_framework/`
- **Addon Integration**: 3-4 files in `addons/wcs_converter/`
- **Reduction**: 70% fewer files needed

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

**Implementation Status**: ✅ **IMPLEMENTED** - The conversion pipeline is operational with:
- Complete VP archive extraction system
- Asset catalog and inventory management
- Configuration migration utilities  
- Comprehensive validation framework
- Quality assurance automation
- Godot addon integration for seamless workflow

**Implementation Evidence**: Converted assets in `/assets/hermes_*` directories demonstrate successful operation of the conversion pipeline.