# EPIC-003: Data Migration & Conversion Tools - WCS Source Dependencies

**Epic**: EPIC-003 - Data Migration & Conversion Tools  
**Analyst**: Larry (WCS Analyst)  
**Analysis Date**: 2025-01-27  
**WCS Source**: /mnt/d/projects/wcsaga_godot_converter/source/code/  

## Executive Summary

This document maps the critical dependencies between WCS C++ source files that implement data format parsing, conversion utilities, and file I/O systems essential for EPIC-003. Understanding these relationships is crucial for building standalone migration tools and determining the order of implementation for conversion utilities.

**Dependency Analysis Focus**:
- File format parsing dependencies
- Data conversion pipeline relationships
- Shared utility dependencies
- Cross-format integration points

## Critical Foundation Dependencies

### 1. VP Archive System Dependencies (Migration Foundation)

#### `cfile/cfilearchive.h` → Core Dependencies
```cpp
// Primary EPIC-001 Dependencies
#include "cfile/cfile.h"               // Base file operations
#include "globalincs/pstypes.h"        // Standard data types
#include "globalincs/globals.h"        // Global constants

// No circular dependencies - Clean interface
```

**Dependency Impact**: VP archive system is foundational - no dependencies on other EPIC-003 systems
**Migration Priority**: Must implement first - all other tools depend on VP extraction

#### `cfile/cfilearchive.cpp` → Implementation Dependencies
```cpp
// Core Infrastructure (EPIC-001)
#include "cfile/cfilearchive.h"        // Own interface
#include "cfile/cfile.h"               // File I/O operations
#include "osapi/osapi.h"               // Platform abstraction
#include "parse/parselo.h"             // String parsing utilities

// Compression Dependencies
#include "globalincs/systemvars.h"     // System configuration
```

**Critical Path**: VP decompression algorithm is self-contained
**No External Format Dependencies**: VP extraction doesn't depend on other formats

### 2. Core File I/O Foundation

#### `cfile/cfile.h` → Universal Foundation
```cpp
// Minimal Dependencies (EPIC-001 only)
#include "globalincs/pstypes.h"        // Base types
#include "osapi/osapi.h"               // Platform abstraction
```

**Usage Pattern**: Used by ALL parsing and conversion systems
**Dependency Count**: 15+ files depend on cfile.h
- All image format utilities
- All parsing systems  
- Model loading system
- Mission file parser

#### `cfile/cfile.cpp` → Platform Integration
```cpp
// Platform-Specific Dependencies
#include "cfile/cfile.h"               // Own interface
#include "cfile/cfilearchive.h"        // VP archive support
#include "osapi/osregistry.h"          // Registry access (Windows)
#include "globalincs/systemvars.h"     // Configuration

// No Format-Specific Dependencies - Clean separation
```

**Architecture Benefit**: File I/O layer is format-agnostic
**Migration Advantage**: Can implement file operations independently

## Table Data Parsing Dependencies

### 3. Core Parsing Infrastructure

#### `parse/parselo.h` → Parsing Foundation
```cpp
// Minimal Dependencies (Clean Interface)
#include "globalincs/pstypes.h"        // Standard types
#include "cfile/cfile.h"               // File reading support
```

**Usage Pattern**: Universal dependency for all configuration parsing
**Files Depending on parselo.h**:
- ship/ship.cpp (ships.tbl parsing)
- weapon/weapons.cpp (weapons.tbl parsing)
- mission/missionparse.cpp (mission files)
- All specialized table parsers

#### `parse/parselo.cpp` → Advanced Parsing Features
```cpp
// Core Dependencies
#include "parse/parselo.h"             // Own interface
#include "cfile/cfile.h"               // File operations
#include "globalincs/globals.h"        // Constants and macros

// Error Handling
#include "osapi/outwnd.h"              // Debug output
#include "parse/encrypt.h"             // Encrypted file support
```

**Key Integration**: Links to encryption system for protected files
**No Format Dependencies**: Parser is format-agnostic

### 4. SEXP Parsing System (Complex Dependencies)

#### `parse/sexp.h` → Mission Scripting Dependencies
```cpp
// Core Dependencies
#include "globalincs/pstypes.h"        // Base types
#include "parse/parselo.h"             // Table parsing foundation

// Game System Dependencies (Heavy)
#include "ship/ship.h"                 // Ship class references
#include "weapon/weapon.h"             // Weapon references
#include "mission/missionparse.h"      // Mission object references
```

**Circular Dependency Warning**: SEXP system creates complex interdependencies
**Migration Challenge**: SEXP → GDScript conversion requires understanding of all game systems

#### `parse/sexp.cpp` → Extensive Game Integration
```cpp
// Massive Dependency List (50+ includes)
#include "parse/sexp.h"                // Own interface
#include "ai/ai.h"                     // AI system integration
#include "hud/hud.h"                   // HUD system integration
#include "mission/missiongoals.h"      // Mission objective system
#include "ship/ship.h"                 // Ship management
#include "weapon/weapon.h"             // Weapon system
// ... many more game system dependencies
```

**Conversion Complexity**: SEXP requires understanding of entire game codebase
**Migration Strategy**: Extract SEXP expressions separately from game logic

### 5. Encryption System Dependencies

#### `parse/encrypt.h` → Minimal Interface
```cpp
// Clean Interface - No dependencies beyond standard types
#include "globalincs/pstypes.h"        // Basic types only
```

**Design Benefit**: Encryption is self-contained utility
**Usage Pattern**: Used by parselo.cpp for encrypted table files

#### `parse/encrypt.cpp` → Standalone Implementation
```cpp
#include "parse/encrypt.h"             // Own interface
#include "globalincs/pstypes.h"        // Type definitions

// No external dependencies - Self-contained decryption
```

**Migration Advantage**: Can implement decryption independently
**Algorithm Isolation**: Encryption logic doesn't depend on game systems

## 3D Model Format Dependencies

### 6. POF Model System Dependencies

#### `model/model.h` → Limited Dependencies
```cpp
// Foundation Dependencies (EPIC-001)
#include "globalincs/pstypes.h"        // Base types
#include "math/vecmat.h"               // Vector mathematics
#include "cfile/cfile.h"               // File I/O

// Graphics Dependencies (Future EPIC-009)
#include "graphics/2d.h"               // Texture binding (weak dependency)
```

**Migration Benefit**: Model structure definitions are mostly independent
**Weak Graphics Coupling**: Can extract model data without graphics system

#### `model/modelread.cpp` → File Format Parsing
```cpp
// Core Dependencies
#include "model/model.h"               // Model structures
#include "cfile/cfile.h"               // POF file reading
#include "parse/parselo.h"             // String parsing utilities

// Mathematics
#include "math/vecmat.h"               // 3D mathematics
#include "math/fvi.h"                  // Collision detection

// No Asset Dependencies - Self-contained format parser
```

**Conversion Advantage**: POF parser is self-contained
**No External Asset Dependencies**: Can parse POF files independently

### 7. Model Animation Dependencies

#### `model/modelanim.h` → Animation Structure
```cpp
// Minimal Dependencies
#include "globalincs/pstypes.h"        // Base types
#include "model/model.h"               // Model structure integration
```

**Clean Integration**: Animation extends model system cleanly
**No Game Logic Dependencies**: Animation data is purely structural

#### `model/modelanim.cpp` → Animation Implementation
```cpp
#include "model/modelanim.h"           // Own interface
#include "model/model.h"               // Model system integration
#include "math/vecmat.h"               // Mathematical operations

// No External Format Dependencies
```

**Migration Benefit**: Animation system is self-contained
**Format Independence**: Can extract animation data separately

## Image Format Conversion Dependencies

### 8. Image Format Utility Dependencies

#### Individual Format Utilities (Clean Architecture)
```cpp
// PCX Format (pcxutils/pcxutils.h)
#include "globalincs/pstypes.h"        // Base types
#include "cfile/cfile.h"               // File I/O

// TGA Format (tgautils/tgautils.h)  
#include "globalincs/pstypes.h"        // Base types
#include "cfile/cfile.h"               // File I/O

// JPEG Format (jpgutils/jpgutils.h)
#include "globalincs/pstypes.h"        // Base types
#include "cfile/cfile.h"               // File I/O

// PNG Format (pngutils/pngutils.h)
#include "globalincs/pstypes.h"        // Base types  
#include "cfile/cfile.h"               // File I/O

// DDS Format (ddsutils/ddsutils.h)
#include "globalincs/pstypes.h"        // Base types
#include "cfile/cfile.h"               // File I/O
```

**Excellent Architecture**: All image utilities have identical, minimal dependencies
**Migration Advantage**: Can implement format converters independently
**No Cross-Format Dependencies**: Each utility is self-contained

#### Image Format Implementation Pattern
```cpp
// All *utils/*.cpp files follow same pattern:
#include "[format]utils/[format]utils.h"  // Own interface
#include "cfile/cfile.h"                   // File operations
#include "globalincs/pstypes.h"            // Standard types

// Format-specific libraries (e.g., libjpeg, libpng)
// No dependencies on other image formats
```

**Clean Separation**: No image format depends on another
**Library Integration**: External libraries handled cleanly
**Migration Strategy**: Convert all formats to PNG pipeline

## Mission and Gameplay Data Dependencies

### 9. Mission File Parsing Dependencies

#### `mission/missionparse.h` → Complex Game Integration
```cpp
// Core Dependencies
#include "globalincs/pstypes.h"        // Base types
#include "parse/parselo.h"             // Table parsing

// Heavy Game System Dependencies
#include "ship/ship.h"                 // Ship definitions
#include "ai/ai.h"                     // AI behaviors
#include "parse/sexp.h"                // Scripting system
#include "object/object.h"             // Game objects
```

**Complex Dependencies**: Mission files reference all game systems
**Migration Challenge**: Requires understanding of complete game architecture

#### `mission/missionparse.cpp` → Massive Integration
```cpp
// Extensive dependency list (30+ includes)
#include "mission/missionparse.h"      // Own interface
#include "ship/ship.h"                 // Ship data
#include "weapon/weapon.h"             // Weapon data
#include "ai/ai.h"                     // AI configuration
#include "parse/sexp.h"                // Mission scripting
#include "asteroid/asteroid.h"         // Environmental objects
// ... many more game systems
```

**Conversion Complexity**: Mission files are tightly coupled to game systems
**Migration Strategy**: Extract mission structure separately from game logic

### 10. Specialized Parsing Dependencies

#### HUD Configuration Dependencies
```cpp
// hud/hudparse.h → HUD System Integration
#include "globalincs/pstypes.h"        // Base types
#include "parse/parselo.h"             // Parsing foundation
#include "hud/hud.h"                   // HUD system definitions

// hud/hudparse.cpp → Implementation
#include "hud/hudparse.h"              // Own interface
#include "hud/hud.h"                   // HUD system
#include "graphics/2d.h"               // Graphics integration
```

**Game System Coupling**: HUD parsing requires HUD system understanding
**Migration Approach**: Extract configuration data, convert UI separately

## Conversion Tool Implementation Dependencies

### 11. Standalone Tool Dependency Analysis

#### VP Extraction Tool Dependencies (Minimal)
```
Core Requirements:
- cfile/cfilearchive.* (VP format parsing)
- cfile/cfile.* (basic file I/O)  
- parse/encrypt.* (decryption support)
- globalincs/pstypes.h (basic types)

Optional Dependencies:
- osapi/* (platform abstraction)
- parse/parselo.* (string utilities)
```

**Implementation Strategy**: Can build minimal VP extractor with 6-8 source files
**No Game Dependencies**: VP extraction is completely independent

#### POF Conversion Tool Dependencies (Moderate)  
```
Core Requirements:
- model/model.h (POF structure definitions)
- model/modelread.cpp (POF parsing logic)
- model/modelanim.* (animation data)
- cfile/cfile.* (file I/O)
- math/vecmat.* (3D mathematics)

Optional Dependencies:
- parse/parselo.* (string parsing)
- globalincs/* (utilities)
```

**Implementation Strategy**: Can build POF converter with 10-12 source files
**No Asset Dependencies**: POF conversion doesn't require other assets

#### Table Migration Tool Dependencies (Complex)
```
Core Requirements:
- parse/parselo.* (table parsing)
- parse/encrypt.* (decryption)
- cfile/cfile.* (file I/O)

Game System Dependencies (For Validation):
- ship/ship.h (ship table structure)
- weapon/weapon.h (weapon table structure)
- Various other table definitions

SEXP Dependencies (For Mission Files):
- parse/sexp.* (expression parsing)
- All game system headers (for reference validation)
```

**Implementation Strategy**: Build basic table parser first, add validation later
**Validation Complexity**: Full validation requires game system understanding

### 12. Godot Import Plugin Dependencies

#### VP Import Plugin Strategy
```
WCS Dependencies:
- VP extraction logic (cfilearchive.*)
- File enumeration (cfilelist.cpp)

Godot Integration:
- EditorImportPlugin base class
- ResourceSaver for extracted assets
- Directory creation utilities
```

**Clean Integration**: VP plugin can be self-contained
**Batch Processing**: Can handle multiple VP files independently

#### POF Import Plugin Strategy
```  
WCS Dependencies:
- POF parsing logic (modelread.cpp)
- Model structures (model.h)
- Animation data (modelanim.*)

Godot Integration:
- EditorImportPlugin base class
- Scene creation and node hierarchy
- Mesh and collision shape generation
```

**Moderate Complexity**: Requires understanding of POF format and Godot scene system
**Asset Dependencies**: May need texture resolution during import

## Critical Conversion Sequencing

### 13. Implementation Order (Dependency-Driven)

#### Phase 1: Foundation Tools (Minimal Dependencies)
1. **VP Extractor**: cfilearchive.* + cfile.* + encrypt.*
2. **Image Converters**: *utils.* (independent)
3. **Basic Table Parser**: parselo.* + encrypt.*

#### Phase 2: Format-Specific Tools (Moderate Dependencies)
1. **POF Converter**: model/modelread.cpp + math/*
2. **Enhanced Table Parser**: Add validation logic
3. **File System Tools**: cfilesystem.* utilities

#### Phase 3: Complex Integration Tools (Heavy Dependencies)
1. **Mission File Converter**: missionparse.* + all game systems
2. **SEXP Converter**: sexp.* + complete game understanding
3. **HUD Configuration**: hudparse.* + UI systems

### 14. Dependency Isolation Strategies

#### Clean Extraction Patterns
1. **Copy Core Logic**: Extract parsing algorithms to standalone functions
2. **Remove Game Dependencies**: Replace game system references with data structures
3. **Mock Validation**: Create lightweight validation without full game systems
4. **Format Focus**: Concentrate on file format, not game logic

#### Conversion Tool Architecture
```
Migration Tool Structure:
├── core/
│   ├── file_io.py          (based on cfile.*)
│   ├── vp_extractor.py     (based on cfilearchive.*)
│   └── encryption.py       (based on encrypt.*)
├── formats/
│   ├── pof_parser.py       (based on modelread.cpp)
│   ├── table_parser.py     (based on parselo.*)
│   └── image_converters.py (based on *utils.*)
└── godot/
    ├── import_plugins/
    └── validation_tools/
```

## Performance and Scalability Considerations

### 15. Conversion Pipeline Dependencies

#### Batch Processing Order
```
1. VP Extraction (Independent - Can parallelize)
   ↓
2. Image Conversion (Independent - Can parallelize)
   ↓  
3. POF Conversion (Independent - Can parallelize)
   ↓
4. Table Parsing (Some interdependencies)
   ↓
5. Mission Conversion (Heavy dependencies)
```

**Parallelization Opportunities**: Steps 1-3 can run in parallel
**Dependency Bottlenecks**: Mission conversion requires all other data

#### Memory and Performance Dependencies
- **VP Extraction**: Streaming I/O, minimal memory
- **POF Conversion**: Moderate memory for model data
- **Mission Parsing**: High memory for complete game state
- **Image Conversion**: Parallel processing friendly

---

**Dependency Analysis Complete**: EPIC-003 conversion tool dependencies mapped with clear implementation sequencing and architectural isolation strategies defined