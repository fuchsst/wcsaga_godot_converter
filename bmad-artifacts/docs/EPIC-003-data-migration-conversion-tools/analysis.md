# EPIC-003: Data Migration & Conversion Tools - WCS Analysis

**Epic**: EPIC-003 - Data Migration & Conversion Tools  
**Analyst**: Larry (WCS Analyst)  
**Analysis Date**: 2025-01-27  
**WCS Source**: /mnt/d/projects/wcsaga_godot_converter/source/code/  

## Executive Summary

EPIC-003 focuses on creating tools to migrate and convert Wing Commander Saga data formats to Godot-compatible formats. This analysis examines the WCS C++ source code that handles file format parsing, data extraction, and format conversion. These systems will serve as the foundation for building migration tools including VP archive extractors, POF model converters, table data parsers, and mission file converters.

**Critical Mission**: Enable seamless conversion of WCS assets and data to Godot while preserving data integrity and supporting automated batch processing.

## System Overview

### 1. Core Data Migration Components

The WCS codebase contains several critical data format handling systems that must be understood to build effective migration tools:

1. **VP Archive System** - Container format for all WCS assets
2. **POF Model Format Parser** - 3D model format (Parallax Object File)
3. **Table Data Parser** - Configuration files (.tbl format)
4. **Image Format Utilities** - Multi-format image loading/conversion
5. **Mission File Parser** - Mission definition format
6. **Encryption/Compression** - Data protection and size optimization

### 2. Migration Tool Architecture Strategy

Based on WCS code analysis, the migration tools should be implemented as:

- **Standalone Python Scripts** - For batch VP archive extraction
- **Godot Import Plugins** - For runtime asset conversion during development
- **CLI Utilities** - For automated build pipeline integration
- **Format Validation Tools** - For data integrity verification

## Detailed System Analysis

### 3. VP Archive System (Critical Foundation)

#### Core Files: `cfile/cfilearchive.*`

The VP (Volition Package) archive system is the foundation of all WCS asset storage. Understanding this format is critical for data migration.

**Key Structures from `cfilearchive.h`:**
```cpp
// VP file header structure
typedef struct vp_header {
    char id[4];                    // "VPVP" identifier
    int version;                   // Format version
    int index_offset;              // Offset to file index
    int num_files;                 // Number of files in archive
} vp_header;

// Individual file entry in VP
typedef struct vp_file {
    int offset;                    // File data offset
    int size;                      // Uncompressed file size
    char filename[32];             // Null-terminated filename
    int timestamp;                 // File modification time
} vp_file;
```

**Critical Analysis from `cfilearchive.cpp`:**
- VP files use hierarchical directory structure
- Files can be compressed using proprietary compression
- Archive supports file verification via CRC checksums
- Multiple VP files can be mounted simultaneously
- File lookup uses hash tables for performance

**Migration Tool Requirements:**
- Extract all files from VP archives to directory structure
- Preserve original directory hierarchy
- Handle compressed file decompression
- Validate extracted files against checksums
- Support batch processing of multiple VP archives

#### Implementation Insights from WCS Code:

```cpp
// File extraction process (from cf_open_read_compressed)
int cf_decompress(char *dest, char *src, int size) {
    // Proprietary decompression algorithm
    // Must be reverse-engineered for migration tool
}

// File enumeration (from cf_get_file_list)
int cf_get_file_list(int max, char **list, int pathtype) {
    // Builds list of all files in mounted VP archives
    // Critical for batch extraction tools
}
```

### 4. POF Model Format Parser (3D Asset Migration)

#### Core Files: `model/modelread.cpp`

The POF (Parallax Object File) format is WCS's proprietary 3D model format. Migration tools must convert POF to Godot-compatible formats.

**Key Structures from Analysis:**
```cpp
// POF file structure (reverse-engineered from modelread.cpp)
typedef struct pof_header {
    char id[4];                    // "PSPO" identifier  
    int version;                   // Format version
    int max_radius;                // Bounding sphere radius
    int obj_flags;                 // Model properties flags
    int n_models;                  // Number of submodels
    int n_textures;                // Number of textures
} pof_header;

// Submodel structure
typedef struct pof_submodel {
    int parent;                    // Parent submodel index (-1 for root)
    float offset[3];               // Position offset from parent
    float geometric_center[3];     // Geometric center point
    int bsp_data_size;             // BSP tree data size
    // BSP tree data follows...
} pof_submodel;
```

**Critical Migration Requirements:**
- Parse hierarchical submodel structure
- Convert BSP collision data to Godot collision shapes
- Extract texture mapping information
- Preserve animation attachment points
- Convert coordinate system (WCS uses different handedness)

**Algorithm Analysis from `model_read()`:**
1. Read POF header and validate format
2. Parse submodel hierarchy and build tree structure
3. Load BSP collision geometry for each submodel
4. Extract texture coordinates and material assignments
5. Build bounding box and sphere data
6. Parse special points (weapon mounts, engine points, etc.)

**Godot Conversion Strategy:**
- POF → Godot `.tscn` scene files with `MeshInstance3D` nodes
- Submodel hierarchy → Godot node tree structure
- BSP collision → `CollisionShape3D` with `ConvexPolygonShape3D`
- Texture mapping → Godot material resources
- Animation points → `Marker3D` nodes for attachment

### 5. Table Data Parser (Configuration Migration)

#### Core Files: `parse/parselo.*`

The table data parser handles all WCS configuration files (ships.tbl, weapons.tbl, etc.). This is critical for migrating game balance and configuration data.

**Key Functions from `parselo.cpp`:**
```cpp
// Core table parsing functions
char *required_string(char *pstr);     // Find required table entry
void stuff_string(char *pstr, int type, char *terminators);
void stuff_float(float *f);            // Parse floating point values
void stuff_int(int *i);                // Parse integer values
void stuff_boolean(int *i);            // Parse boolean flags

// Advanced parsing utilities
int optional_string(char *pstr);       // Optional table entries
void advance_to_eoln();                // Skip to end of line
void ignore_white_space();             // Skip whitespace and comments
```

**Table Format Analysis:**
- Uses human-readable text format with structured sections
- Supports comments with // and /* */ delimiters
- Case-insensitive keyword matching
- Hierarchical data with nested sections
- Default value inheritance and overrides

**Critical Migration Requirements:**
- Parse all .tbl files into structured data
- Convert to Godot Resource (.tres) format
- Preserve inheritance relationships
- Validate data integrity during conversion
- Support modding by maintaining text-based editing

**Example Table Structure (ships.tbl):**
```
$Name: GTF Ulysses
$Short name: Ulysses  
$Species: Terran
$Type: Fighter
$Max velocity: 65.0, 75.0, 65.0
$Max afterburner velocity: 150.0
$Hitpoints: 220
$Model file: fighter2t-01.pof
$Mass: 4.0
$Density: 1.0
// ... many more fields
$end_multi_text
```

**Godot Conversion Strategy:**
- .tbl files → Godot Resource scripts (.gd)
- Table entries → `@export` class properties
- Hierarchical data → Resource inheritance
- Validation → Built-in type checking
- Modding → JSON or .tres resource files

### 6. Image Format Conversion System

#### Core Files: `*utils/*utils.*` (pcxutils, tgautils, jpgutils, pngutils, ddsutils)

WCS supports multiple image formats through dedicated utility modules. Migration tools need unified image conversion.

**Supported Input Formats:**
- **PCX**: Legacy format, paletted images
- **TGA**: Uncompressed RGB/RGBA
- **JPEG**: Compressed photos
- **PNG**: Compressed with transparency
- **DDS**: DirectX compressed textures

**Format Analysis from Utils Code:**
```cpp
// PCX format structure (pcxutils.cpp)
typedef struct pcx_header {
    char manufacturer;
    char version;
    char encoding;               // RLE compression flag
    char bits_per_pixel;
    short xmin, ymin, xmax, ymax;
    short hdpi, vdpi;
    char colormap[48];
    // ... more fields
} pcx_header;

// TGA format support (tgautils.cpp)  
int targa_read_header(char *real_filename, int *w, int *h, int *bpp);
int targa_read_bitmap(char *real_filename, ubyte *image_data);
```

**Critical Migration Requirements:**
- Convert all texture formats to PNG (Godot's preferred format)
- Preserve transparency information
- Handle palette conversion for PCX files
- Maintain texture quality during conversion
- Support batch processing for large texture sets

**Godot Conversion Strategy:**
- All formats → PNG for import pipeline
- Preserve original resolution and aspect ratio
- Convert palettes to full-color when needed
- Maintain transparency channels
- Generate mipmaps for 3D textures

### 7. Mission File Parser (Gameplay Data Migration)

#### Core Files: `mission/missionparse.*`

Mission files contain complete level definitions including ship placements, objectives, scripting, and triggers.

**Key Structures from `missionparse.h`:**
```cpp
// Mission header information
typedef struct mission {
    char name[NAME_LENGTH];
    char author[NAME_LENGTH];
    char created[DATE_TIME_LENGTH];
    char modified[DATE_TIME_LENGTH];
    char description[MISSION_DESC_LENGTH];
    int game_type;                 // Mission type flags
    int num_players;               // Multiplayer support
    // ... mission metadata
} mission;

// Ship/object placement data
typedef struct p_object {
    char name[NAME_LENGTH];
    int ship_class;                // Ship type index
    float pos[3];                  // World position
    float orient[9];               // Rotation matrix
    int flags;                     // Object behavior flags
    // ... object properties
} p_object;
```

**Mission File Format Analysis:**
- Text-based format similar to table files
- Contains object placement data
- Includes SEXP (S-expression) scripting
- Supports waypoints and navigation data
- Mission briefing and debriefing text

**Critical Migration Requirements:**
- Parse complete mission structure
- Convert object placements to Godot scene format
- Migrate SEXP scripts to GDScript
- Preserve waypoint and navigation data
- Maintain mission metadata and descriptions

### 8. Encryption and Compression Systems

#### Core Files: `parse/encrypt.*`

WCS uses proprietary encryption for sensitive data files.

**Encryption Analysis from `encrypt.cpp`:**
```cpp
// File encryption detection
int is_enrypted(char *filename);

// Decryption process
void unencrypt(char *text, int text_len, char *scrambled_text);
```

**Critical Requirements:**
- Decrypt protected configuration files
- Preserve data integrity during decryption
- Handle multiple encryption schemes
- Support batch decryption for migration

## Performance and Optimization Analysis

### 9. File I/O Performance Patterns

**Critical Performance Insights from WCS Code:**

1. **Bulk Loading**: WCS loads assets in batches during level transitions
2. **Caching Strategy**: Aggressive caching with LRU eviction
3. **Streaming**: Large files are streamed rather than loaded entirely
4. **Compression**: Trade CPU time for reduced I/O bandwidth

**Migration Tool Performance Requirements:**
- Support parallel processing for batch conversion
- Implement progress reporting for large conversions
- Use streaming for large asset files
- Minimize memory usage during conversion

### 10. Error Handling and Validation

**Error Patterns from WCS Code Analysis:**
- File format validation before processing
- Graceful degradation for missing assets
- Detailed error logging for debugging
- Recovery mechanisms for corrupted data

**Migration Tool Error Handling:**
- Validate input formats before conversion
- Provide detailed error reporting
- Support partial conversion recovery
- Generate conversion logs for debugging

## Godot Integration Architecture

### 11. Import Plugin Design

Based on WCS format analysis, Godot import plugins should:

**VP Archive Plugin:**
- Import VP files as directory structures
- Extract individual assets for other importers
- Maintain asset dependency relationships

**POF Model Plugin:**
- Convert POF directly to Godot scenes
- Generate collision shapes automatically
- Preserve submodel hierarchy and attachment points

**Table Data Plugin:**
- Convert .tbl files to Resource scripts
- Validate data types and ranges
- Support inheritance and composition

### 12. CLI Tool Architecture

**Batch Conversion Tools:**
```bash
# VP archive extraction
wcs-extract-vp --input root_fs2.vp --output assets/

# POF model conversion  
wcs-convert-pof --input models/ --output godot://models/

# Table data migration
wcs-convert-tables --input data/tables/ --output resources/config/
```

**Features Required:**
- Progress reporting
- Error logging
- Batch processing
- Format validation
- Dependency tracking

## Critical Migration Challenges

### 13. Data Integrity Challenges

1. **Coordinate System Conversion**: WCS uses right-handed, Godot uses left-handed
2. **Scale Differences**: WCS units vs Godot units
3. **Material System**: WCS shaders vs Godot materials
4. **Animation Data**: Different animation systems
5. **Physics Properties**: Different physics engines

### 14. Legacy Compatibility Issues

1. **Deprecated Formats**: Some WCS formats are legacy
2. **Version Differences**: Multiple WCS versions with format changes
3. **Missing Documentation**: Proprietary formats lack documentation
4. **Platform Dependencies**: Some code has platform-specific paths

### 15. Quality Assurance Requirements

1. **Round-trip Testing**: Convert and verify data integrity
2. **Visual Comparison**: Compare original vs converted assets
3. **Performance Validation**: Ensure converted assets perform well
4. **Modding Support**: Maintain modding capability after conversion

## Conversion Implementation Strategy

### 16. Phase 1: Core Format Parsers
- Implement VP archive extractor
- Build POF format parser
- Create table data reader
- Develop image format converters

### 17. Phase 2: Godot Integration
- Create import plugins for each format
- Implement batch conversion CLI tools
- Add validation and error reporting
- Build dependency tracking system

### 18. Phase 3: Quality Assurance
- Comprehensive format testing
- Performance optimization
- Documentation and user guides
- Modding tool integration

## Success Metrics

### 19. Conversion Quality Targets
- **100% Asset Coverage**: All WCS assets must be convertible
- **Data Integrity**: Zero data loss during conversion
- **Performance Parity**: Converted assets perform as well as originals
- **Automation**: Batch processing for entire WCS installation
- **Validation**: Comprehensive error detection and reporting

### 20. Developer Experience Goals
- **One-Command Setup**: Single command to convert entire WCS data
- **Incremental Updates**: Support for partial re-conversion
- **Clear Documentation**: Step-by-step conversion guides
- **Error Recovery**: Graceful handling of conversion failures
- **Progress Feedback**: Real-time conversion progress reporting

---

**Analysis Complete**: EPIC-003 migration tools foundation established through comprehensive WCS format analysis. Ready for Godot implementation architecture design.