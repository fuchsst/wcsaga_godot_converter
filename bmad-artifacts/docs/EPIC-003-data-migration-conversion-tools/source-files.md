# EPIC-003: Data Migration & Conversion Tools - WCS Source Files

**Epic**: EPIC-003 - Data Migration & Conversion Tools  
**Analyst**: Larry (WCS Analyst)  
**Analysis Date**: 2025-01-27  
**WCS Source**: /mnt/d/projects/wcsaga_godot_converter/source/code/  

## Executive Summary

This document catalogs WCS C++ source files that implement data format parsing, file I/O, and conversion utilities essential for building migration tools. These files contain the algorithms and data structures needed to understand WCS proprietary formats and convert them to Godot-compatible formats.

**Migration Tool Focus**:
- **Included**: Format parsers, file readers, data extractors, conversion utilities
- **Excluded**: Runtime game systems (covered in other epics)
- **Purpose**: Foundation for building standalone conversion tools and Godot import plugins

## VP Archive System Files (Critical Foundation)

### 1. Core Archive Management

#### `cfile/cfilearchive.h` ⭐⭐⭐ (CRITICAL)
- **Lines**: ~200 lines
- **Purpose**: VP (Volition Package) archive system interface
- **Key Structures**:
  - VP file header definitions
  - Archive mounting and management
  - Virtual file system abstraction
- **Migration Use**: Core VP archive extraction logic
- **Conversion Priority**: Critical - All WCS assets are in VP files

#### `cfile/cfilearchive.cpp` ⭐⭐⭐ (CRITICAL)
- **Lines**: ~800+ lines
- **Purpose**: VP archive implementation and file extraction
- **Key Functions**:
  - `cf_open_read_compressed()` - Compressed file reading
  - `cf_get_file_list()` - Archive file enumeration
  - `cf_decompress()` - Proprietary decompression
- **Migration Use**: VP file extraction algorithms
- **Conversion Priority**: Critical - Must reverse-engineer compression

#### `cfile/cfile.h` ⭐⭐⭐ (CRITICAL)
- **Lines**: ~300 lines
- **Purpose**: Core file I/O abstraction layer
- **Key Features**:
  - Virtual file system support
  - Cross-platform file operations
  - Buffered I/O for performance
- **Migration Use**: File handling foundation
- **Conversion Priority**: Critical - Base for all file operations

#### `cfile/cfile.cpp` ⭐⭐⭐ (CRITICAL)
- **Lines**: ~2,000+ lines
- **Purpose**: File I/O implementation
- **Key Functions**:
  - File reading with VP archive support
  - Binary data parsing utilities
  - Error handling and logging
- **Migration Use**: Core file reading for all formats
- **Conversion Priority**: Critical - Foundation file operations

### 2. File System Integration

#### `cfile/cfilesystem.h` ⭐⭐ (HIGH)
- **Lines**: ~150 lines
- **Purpose**: File system abstraction interface
- **Key Features**:
  - Directory enumeration
  - Path manipulation utilities
  - Platform-specific file operations
- **Migration Use**: Directory structure preservation
- **Conversion Priority**: High - Required for proper file organization

#### `cfile/cfilesystem.cpp` ⭐⭐ (HIGH)
- **Lines**: ~800+ lines
- **Purpose**: File system operations implementation
- **Key Functions**:
  - Directory creation and traversal
  - File existence checking
  - Path resolution and validation
- **Migration Use**: Output directory management
- **Conversion Priority**: High - Essential for organized output

#### `cfile/cfilelist.cpp` ⭐⭐ (HIGH)
- **Lines**: ~400+ lines
- **Purpose**: File list management and enumeration
- **Key Functions**:
  - File filtering and sorting
  - Pattern matching for file selection
  - Recursive directory scanning
- **Migration Use**: Batch processing file discovery
- **Conversion Priority**: High - Required for batch operations

## Table Data Parsing System (Configuration Migration)

### 3. Core Parsing Infrastructure

#### `parse/parselo.h` ⭐⭐⭐ (CRITICAL)
- **Lines**: ~200 lines
- **Purpose**: Table data parsing interface
- **Key Functions**:
  - `required_string()` - Required table entries
  - `stuff_string()` - String value extraction
  - `stuff_float()`, `stuff_int()` - Numeric parsing
- **Migration Use**: All .tbl file parsing
- **Conversion Priority**: Critical - Foundation for configuration migration

#### `parse/parselo.cpp` ⭐⭐⭐ (CRITICAL)
- **Lines**: ~3,000+ lines
- **Purpose**: Table parsing implementation
- **Key Functions**:
  - Token parsing and validation
  - Comment handling and whitespace
  - Error reporting and recovery
- **Migration Use**: Complete table parsing logic
- **Conversion Priority**: Critical - Must understand all parsing rules

### 4. Advanced Parsing Features

#### `parse/sexp.h` ⭐⭐⭐ (CRITICAL)
- **Lines**: ~300 lines
- **Purpose**: S-expression parser for mission scripting
- **Key Structures**:
  - SEXP tree node definitions
  - Operator and operand types
  - Expression evaluation framework
- **Migration Use**: Mission script conversion
- **Conversion Priority**: Critical - Required for mission data

#### `parse/sexp.cpp` ⭐⭐⭐ (CRITICAL)
- **Lines**: ~8,000+ lines
- **Purpose**: SEXP parser and evaluator implementation
- **Key Functions**:
  - Expression tree parsing
  - Type validation and checking
  - Operator implementation
- **Migration Use**: Convert SEXP to GDScript
- **Conversion Priority**: Critical - Complex conversion required

#### `parse/scripting.h` ⭐⭐ (HIGH)
- **Lines**: ~150 lines
- **Purpose**: Lua scripting integration interface
- **Key Features**:
  - Lua state management
  - Function registration
  - Script execution environment
- **Migration Use**: Understanding script integration
- **Conversion Priority**: High - May need GDScript conversion

#### `parse/scripting.cpp` ⭐⭐ (HIGH)
- **Lines**: ~1,200+ lines
- **Purpose**: Lua scripting implementation
- **Key Functions**:
  - Lua VM initialization
  - Function binding and calls
  - Error handling and debugging
- **Migration Use**: Script conversion strategies
- **Conversion Priority**: High - Complex scripting migration

### 5. Data Encryption/Decryption

#### `parse/encrypt.h` ⭐⭐ (HIGH)
- **Lines**: ~50 lines
- **Purpose**: Data encryption/decryption interface
- **Key Functions**:
  - Encryption detection
  - Decryption key management
  - Scrambled data handling
- **Migration Use**: Decrypt protected files
- **Conversion Priority**: High - Required for some data files

#### `parse/encrypt.cpp` ⭐⭐ (HIGH)
- **Lines**: ~200+ lines
- **Purpose**: Encryption implementation
- **Key Functions**:
  - `is_encrypted()` - Detection algorithm
  - `unencrypt()` - Decryption process
  - Key derivation and validation
- **Migration Use**: Decryption algorithms
- **Conversion Priority**: High - Must preserve data integrity

## 3D Model Format Parsing (POF Conversion)

### 6. Model Loading System

#### `model/model.h` ⭐⭐⭐ (CRITICAL)
- **Lines**: ~600 lines
- **Purpose**: 3D model structure definitions
- **Key Structures**:
  - `polymodel` - Complete model container
  - `bsp_info` - Submodel hierarchy
  - Collision and physics data
- **Migration Use**: POF format understanding
- **Conversion Priority**: Critical - Foundation for 3D conversion

#### `model/modelread.cpp` ⭐⭐⭐ (CRITICAL)
- **Lines**: ~3,000+ lines
- **Purpose**: POF file format parsing and loading
- **Key Functions**:
  - POF header parsing
  - BSP tree construction
  - Texture coordinate extraction
- **Migration Use**: Complete POF parsing algorithm
- **Conversion Priority**: Critical - Complex format conversion

#### `model/modelanim.h` ⭐⭐ (HIGH)
- **Lines**: ~200 lines
- **Purpose**: Model animation data structures
- **Key Features**:
  - Keyframe animation definitions
  - Submodel animation sequences
  - Trigger and event systems
- **Migration Use**: Animation data preservation
- **Conversion Priority**: High - Animation system conversion

#### `model/modelanim.cpp` ⭐⭐ (HIGH)
- **Lines**: ~800+ lines
- **Purpose**: Animation system implementation
- **Key Functions**:
  - Animation data loading
  - Keyframe interpolation
  - Animation state management
- **Migration Use**: Animation conversion algorithms
- **Conversion Priority**: High - Complex animation migration

## Image Format Conversion Utilities

### 7. Multi-Format Image Support

#### `pcxutils/pcxutils.h` ⭐⭐⭐ (CRITICAL)
- **Lines**: ~100 lines
- **Purpose**: PCX image format support interface
- **Key Features**:
  - PCX header structure definitions
  - Palette and RLE compression support
  - Color depth conversion
- **Migration Use**: PCX to PNG conversion
- **Conversion Priority**: Critical - Legacy format migration

#### `pcxutils/pcxutils.cpp` ⭐⭐⭐ (CRITICAL)
- **Lines**: ~800+ lines
- **Purpose**: PCX format implementation
- **Key Functions**:
  - PCX header parsing
  - RLE decompression
  - Palette conversion to RGB
- **Migration Use**: Complete PCX conversion logic
- **Conversion Priority**: Critical - Complex format handling

#### `tgautils/tgautils.h` ⭐⭐ (HIGH)
- **Lines**: ~80 lines
- **Purpose**: TGA image format support interface
- **Key Features**:
  - TGA header definitions
  - RLE and uncompressed support
  - Alpha channel handling
- **Migration Use**: TGA to PNG conversion
- **Conversion Priority**: High - Common texture format

#### `tgautils/tgautils.cpp` ⭐⭐ (HIGH)
- **Lines**: ~600+ lines
- **Purpose**: TGA format implementation
- **Key Functions**:
  - TGA header parsing
  - Pixel data extraction
  - Alpha channel preservation
- **Migration Use**: TGA conversion algorithms
- **Conversion Priority**: High - Straightforward conversion

#### `jpgutils/jpgutils.h` ⭐⭐ (HIGH)
- **Lines**: ~60 lines
- **Purpose**: JPEG image format support interface
- **Key Features**:
  - JPEG library integration
  - Quality settings
  - Error handling
- **Migration Use**: JPEG processing
- **Conversion Priority**: High - Photo texture support

#### `jpgutils/jpgutils.cpp` ⭐⭐ (HIGH)
- **Lines**: ~400+ lines
- **Purpose**: JPEG format implementation
- **Key Functions**:
  - JPEG decompression
  - Quality assessment
  - Memory management
- **Migration Use**: JPEG conversion logic
- **Conversion Priority**: High - Standard format

#### `pngutils/pngutils.h` ⭐⭐ (HIGH)
- **Lines**: ~70 lines
- **Purpose**: PNG image format support interface
- **Key Features**:
  - PNG library integration
  - Transparency support
  - Compression settings
- **Migration Use**: PNG processing (target format)
- **Conversion Priority**: High - Godot's preferred format

#### `pngutils/pngutils.cpp` ⭐⭐ (HIGH)
- **Lines**: ~500+ lines
- **Purpose**: PNG format implementation
- **Key Functions**:
  - PNG decompression and compression
  - Alpha channel handling
  - Metadata preservation
- **Migration Use**: PNG generation logic
- **Conversion Priority**: High - Output format

#### `ddsutils/ddsutils.h` ⭐⭐ (HIGH)
- **Lines**: ~100 lines
- **Purpose**: DDS texture format support interface
- **Key Features**:
  - DirectX texture support
  - Compressed texture formats
  - Mipmap handling
- **Migration Use**: DDS conversion support
- **Conversion Priority**: High - Advanced texture features

#### `ddsutils/ddsutils.cpp` ⭐⭐ (HIGH)
- **Lines**: ~700+ lines
- **Purpose**: DDS format implementation
- **Key Functions**:
  - DDS header parsing
  - Compressed format decompression
  - Mipmap extraction
- **Migration Use**: DDS conversion algorithms
- **Conversion Priority**: High - Complex format conversion

## Mission and Gameplay Data Parsing

### 8. Mission File System

#### `mission/missionparse.h` ⭐⭐⭐ (CRITICAL)
- **Lines**: ~400 lines
- **Purpose**: Mission file format definitions
- **Key Structures**:
  - Mission metadata
  - Object placement data
  - Objective definitions
- **Migration Use**: Mission file structure understanding
- **Conversion Priority**: Critical - Mission data conversion

#### `mission/missionparse.cpp` ⭐⭐⭐ (CRITICAL)
- **Lines**: ~4,000+ lines
- **Purpose**: Mission file parsing implementation
- **Key Functions**:
  - Complete mission file parsing
  - Object placement processing
  - SEXP integration
- **Migration Use**: Mission conversion algorithms
- **Conversion Priority**: Critical - Complex mission data

### 9. Specialized Parsing Systems

#### `hud/hudparse.h` ⭐⭐ (HIGH)
- **Lines**: ~100 lines
- **Purpose**: HUD configuration parsing interface
- **Key Features**:
  - HUD element definitions
  - Layout and positioning data
  - Configuration validation
- **Migration Use**: UI configuration migration
- **Conversion Priority**: High - UI system data

#### `hud/hudparse.cpp` ⭐⭐ (HIGH)
- **Lines**: ~800+ lines
- **Purpose**: HUD configuration parsing implementation
- **Key Functions**:
  - HUD element parsing
  - Layout validation
  - Default value handling
- **Migration Use**: UI conversion logic
- **Conversion Priority**: High - HUD system migration

#### `object/parseobjectdock.h` ⭐⭐ (HIGH)
- **Lines**: ~80 lines
- **Purpose**: Object docking configuration parsing
- **Key Features**:
  - Docking bay definitions
  - Ship-to-ship docking parameters
  - Attachment point specifications
- **Migration Use**: Docking system migration
- **Conversion Priority**: High - Gameplay feature migration

#### `object/parseobjectdock.cpp` ⭐⭐ (HIGH)
- **Lines**: ~300+ lines
- **Purpose**: Docking configuration implementation
- **Key Functions**:
  - Docking bay parsing
  - Attachment validation
  - Configuration loading
- **Migration Use**: Docking conversion algorithms
- **Conversion Priority**: High - Complex gameplay feature

## Summary Statistics

### File Categories by Priority

**CRITICAL (⭐⭐⭐)**: 11 files
- VP archive system (4 files)
- Table parsing (3 files)
- Model format (1 file)
- Image formats (2 files)
- Mission parsing (1 file)

**HIGH (⭐⭐)**: 16 files
- File system utilities (3 files)
- Advanced parsing (4 files)
- Model animation (2 files)
- Image formats (5 files)
- Specialized parsing (2 files)

**Total Files**: 27 files covering all major conversion requirements

### Conversion Tool Coverage

1. **VP Archive Extraction**: cfilearchive.*, cfile.*
2. **POF Model Conversion**: model/modelread.cpp, model/model.h
3. **Table Data Migration**: parse/parselo.*, parse/sexp.*
4. **Image Format Conversion**: *utils/*utils.* (5 format pairs)
5. **Mission File Conversion**: mission/missionparse.*
6. **Specialized Data**: HUD, docking, scripting parsers

### Code Volume Analysis

- **Total Source Files**: 27 primary files
- **Estimated Code Volume**: ~35,000+ lines of conversion-related code
- **Most Complex**: missionparse.cpp (~4,000 lines), sexp.cpp (~8,000 lines)
- **Most Critical**: cfilearchive.cpp (VP access), modelread.cpp (3D assets)

### Implementation Complexity

1. **High Complexity**: VP decompression, POF parsing, SEXP conversion
2. **Medium Complexity**: Table parsing, mission files, image conversion
3. **Low Complexity**: File system utilities, basic format headers

## Migration Tool Architecture Mapping

### Standalone Python Tools

1. **VP Extractor**: Based on cfilearchive.* analysis
2. **POF Converter**: Based on modelread.cpp algorithms
3. **Table Migrator**: Based on parselo.* and sexp.* parsing
4. **Image Converter**: Based on *utils.* format handlers

### Godot Import Plugins

1. **VP Import Plugin**: Import VP files as asset directories
2. **POF Import Plugin**: Convert POF to .tscn scenes
3. **Table Resource Plugin**: Convert .tbl to .tres resources
4. **Image Import Pipeline**: Unified image format conversion

### Critical Conversion Challenges

1. **Format Complexity**: POF and SEXP require complex parsing
2. **Proprietary Compression**: VP decompression needs reverse engineering
3. **Data Validation**: Ensure conversion accuracy and completeness
4. **Performance**: Handle large asset sets efficiently
5. **Dependencies**: Maintain asset relationships during conversion

---

**Analysis Complete**: EPIC-003 source files catalogued with comprehensive conversion tool requirements identified