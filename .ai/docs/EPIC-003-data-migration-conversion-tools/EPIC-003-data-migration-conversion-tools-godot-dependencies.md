# EPIC-003: Data Migration & Conversion Tools - Godot Dependencies

**Epic**: EPIC-003 - Data Migration & Conversion Tools  
**Architect**: Mo (Godot Architect)  
**Version**: 2.0 (Simplified based on clean WCS architecture analysis)  
**Date**: 2025-01-27  

## Overview

Dependencies for the data migration and conversion tools system. **Architectural Insight**: Analysis of 27 WCS conversion files reveals **exceptionally clean architecture** with minimal dependencies, dramatically simplifying the dependency mapping.

**Key Discovery**: WCS format parsers are self-contained and independent, eliminating the need for complex dependency management.

## Simplified Dependency Architecture

### Python Scripts (Standalone - Minimal Dependencies)

#### Level 1: Core Extractors (No Dependencies)

##### `conversion_tools/vp_extractor.py`
```python
# DEPENDENCIES: Python standard library only
import struct  # For binary parsing
import os      # For file operations
import shutil  # For directory operations

# WCS DEPENDENCIES: Based on cfilearchive.cpp (self-contained)
# NO EXTERNAL DEPENDENCIES: VP extraction algorithm is standalone

# USED BY: All other conversion tools (foundation)
```

##### `conversion_tools/image_converter.py`
```python
# DEPENDENCIES: Python standard library + PIL (optional)
import struct     # For binary parsing
from PIL import Image  # For image processing (optional - can use raw parsing)

# WCS DEPENDENCIES: Based on *utils.cpp files (5 identical patterns)
# MINIMAL EXTERNAL DEPENDENCIES: Can be pure Python if needed

# USED BY: POF converter (for texture conversion), batch processor
```

#### Level 2: Format Converters (Extractor Dependencies)

##### `conversion_tools/pof_converter.py`
```python
# DEPENDENCIES:
import sys
sys.path.append('.')
from vp_extractor import VPExtractor  # For extracting POF files from VP
from image_converter import ImageConverter  # For texture conversion

# WCS DEPENDENCIES: Based on modelread.cpp (isolated system)
# NO COMPLEX DEPENDENCIES: POF parsing is self-contained

# USED BY: Batch processor, Godot import plugins
```

##### `conversion_tools/table_converter.py`
```python
# DEPENDENCIES:
import json  # For output format
import re    # For text parsing

# WCS DEPENDENCIES: Based on parselo.cpp (simple text parsing)
# NO EXTERNAL DEPENDENCIES: Table parsing is pure text processing

# USED BY: Asset structure generation, batch processor
```

##### `conversion_tools/mission_converter.py`
```python
# DEPENDENCIES:
from table_converter import TableConverter  # For parsing mission tables
import json  # For structured output

# WCS DEPENDENCIES: Based on missionparse.cpp (text-based)
# MINIMAL DEPENDENCIES: Mission files are text-based

# USED BY: Mission system, batch processor
```

#### Level 3: Orchestration (All Converter Dependencies)

##### `conversion_tools/batch_converter.py`
```python
# DEPENDENCIES:
from vp_extractor import VPExtractor
from image_converter import ImageConverter
from pof_converter import POFConverter
from table_converter import TableConverter
from mission_converter import MissionConverter

# ORCHESTRATION ONLY: No WCS-specific dependencies
# USED BY: CLI interface, Godot import system
```

### Godot Import Plugins (Minimal Godot Integration)

#### Level 1: Plugin Foundation

##### `addons/wcs_importers/plugin.gd`
```gdscript
# DEPENDENCIES:
extends EditorPlugin  # Godot built-in

# NO EPIC-001 DEPENDENCIES: Import plugins are independent
# NO EPIC-002 DEPENDENCIES: Import creates assets, doesn't consume them

# USED BY: Godot editor automatically
```

#### Level 2: Format Import Plugins

##### `addons/wcs_importers/vp_import_plugin.gd`
```gdscript
# DEPENDENCIES:
extends EditorImportPlugin  # Godot built-in

# EXTERNAL TOOL DEPENDENCY:
# Calls Python: python conversion_tools/vp_extractor.py

# NO GODOT EPIC DEPENDENCIES: Standalone import operation
# USED BY: Godot import system when .vp files are added
```

##### `addons/wcs_importers/pof_import_plugin.gd`
```gdscript
# DEPENDENCIES:
extends EditorImportPlugin  # Godot built-in

# EXTERNAL TOOL DEPENDENCY:
# Calls Python: python conversion_tools/pof_converter.py

# OUTPUT DEPENDENCIES (after conversion):
const ModelData = preload("res://addons/wcs_assets/resources/models/model_data.gd")

# USED BY: Godot import system when .pof files are added
```

##### `addons/wcs_importers/table_import_plugin.gd`
```gdscript
# DEPENDENCIES:
extends EditorImportPlugin  # Godot built-in

# EXTERNAL TOOL DEPENDENCY:
# Calls Python: python conversion_tools/table_converter.py

# OUTPUT DEPENDENCIES (after conversion):
const BaseAssetData = preload("res://addons/wcs_assets/resources/base/base_asset_data.gd")

# USED BY: Godot import system when .tbl files are added
```

## EPIC Dependencies (Clean Separation)

### EPIC-001 Dependencies (Minimal)
```python
# Python conversion tools have NO EPIC-001 dependencies
# Self-contained Python scripts with minimal external requirements

# Only Godot integration uses EPIC-001:
# - File path utilities (optional)
# - Debug output (optional)
```

### EPIC-002 Dependencies (Output Only)
```gdscript
# Conversion tools CREATE assets for EPIC-002, don't depend on it
# Import plugins generate Resource files that EPIC-002 can load

# After conversion:
# ship.pof → ship_data.tres (EPIC-002 ShipData resource)
# weapon.tbl → weapon_data.tres (EPIC-002 WeaponData resource)
```

### Cross-Epic Output Flow
```
EPIC-003 Conversion Tools
  ↓ generates
EPIC-002 Asset Resources
  ↓ consumed by
All Game Systems
```

## Dependency Chain Summary

```
Level 1: Python Extractors (No Dependencies)
  ├── vp_extractor.py (self-contained)
  ├── image_converter.py (minimal deps)
  └── table_converter.py (pure Python)

Level 2: Python Converters (Extractor Dependencies)
  ├── pof_converter.py (uses VP + image)
  └── mission_converter.py (uses table)

Level 3: Python Orchestration (All Converter Dependencies)
  └── batch_converter.py (orchestrates all)

Level 4: Godot Import Plugins (External Tool Dependencies)
  ├── vp_import_plugin.gd (calls Python tools)
  ├── pof_import_plugin.gd (calls Python tools)
  └── table_import_plugin.gd (calls Python tools)
```

## Implementation Order (Dependency-Driven)

### Week 1: Foundation Python Tools (Parallel Development)
1. `vp_extractor.py` (no dependencies - can start immediately)
2. `image_converter.py` (no dependencies - parallel with VP)
3. `table_converter.py` (no dependencies - parallel with both)

### Week 2: Advanced Python Converters (Foundational Dependencies)
1. `pof_converter.py` (depends on VP + image converters)
2. `mission_converter.py` (depends on table converter)
3. `batch_converter.py` (orchestration)

### Week 3: Godot Integration (External Tool Dependencies)
1. Godot import plugin framework
2. VP import plugin (calls Python VP extractor)
3. POF import plugin (calls Python POF converter)
4. Table import plugin (calls Python table converter)

### Week 4: Integration and Testing (All Dependencies)
1. End-to-end conversion testing
2. Godot editor integration validation
3. Performance optimization and error handling

## External Dependencies (Minimal)

### Python Dependencies
```python
# Required (Python standard library):
import struct, os, shutil, json, re

# Optional (for enhanced image processing):
from PIL import Image  # Can be replaced with raw binary parsing

# No other external dependencies required
```

### System Dependencies
```bash
# Python 3.8+ (for conversion tools)
# Godot 4.4+ (for import plugins)
# No other system dependencies
```

## Performance and Scalability

### Dependency Loading Impact
- **Python Tools**: Zero Godot dependencies - run independently
- **Import Plugins**: Minimal Godot overhead - just wrapper calls
- **Asset Generation**: Creates EPIC-002 resources efficiently
- **Memory Footprint**: Conversion tools are stateless - minimal memory usage

### Parallel Processing Opportunities
```python
# Independent conversion operations can run in parallel:
def convert_assets_parallel():
    # VP extraction (independent)
    # Image conversion (independent) 
    # POF conversion (depends on VP + images)
    # Table conversion (independent)
    pass
```

## Quality Assurance

### Dependency Validation
```python
# test_dependencies.py - Validate clean dependencies
def test_no_circular_dependencies():
    # Verify conversion tools have clean dependency chain
    assert VPExtractor().has_no_external_deps()
    assert ImageConverter().has_minimal_deps()
    
def test_standalone_operation():
    # Verify tools can run without Godot
    assert run_conversion_standalone() == SUCCESS
```

### Integration Testing
```gdscript
# test_import_integration.gd - Validate Godot integration
func test_pof_import():
    # Test POF import plugin integration
    var result = EditorInterface.get_resource_filesystem().import_file("test.pof")
    assert_true(result is PackedScene)
```

## Mo's Architectural Notes

**Clean Architecture Benefits**:
- **Minimal Dependencies**: 27 WCS files with clean separation enable simple implementation
- **Parallel Development**: Independent converters can be developed simultaneously
- **No Circular Dependencies**: Clean one-way flow from extraction to conversion to import
- **External Tool Strategy**: Python tools are completely independent of Godot

**WCS Analysis Advantages**:
- **Self-Contained Parsers**: VP, POF, image, and table parsers are isolated
- **Identical Patterns**: Image format utilities follow the same pattern (trivial to implement)
- **Direct Implementation**: WCS source provides exact algorithms - no guesswork
- **No Reverse Engineering**: Complete understanding of all formats from source analysis

**Implementation Strategy**:
- **Python-First**: Complex logic in Python scripts (easier to debug and test)
- **Godot-Minimal**: Import plugins are simple wrappers calling Python tools
- **Output-Focused**: Generate EPIC-002 resources, don't depend on them
- **Quality-Assured**: Clean dependencies enable comprehensive testing

---

**Architectural Confidence**: This dependency structure leverages the exceptionally clean WCS architecture to deliver robust conversion tools with minimal complexity and maximum reliability.