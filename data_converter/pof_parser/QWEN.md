# POF Parser Component - Model Conversion

## Component Purpose

This component provides comprehensive POF (Parallax Object Format) file analysis, parsing, mesh conversion, and optimization for the Wing Commander Saga to Godot conversion pipeline. It handles .POF model conversion to glTF 2.0 format with preservation of all visual, structural, and gameplay-relevant metadata.

The POF parser operates within the unified conversion architecture:
- **Table Processing**: Handles .tbl file conversion to structured Godot resources
- **Model Processing**: This component handles .POF to glTF conversion  
- **Mission Processing**: Handles FS2 mission file conversion
- **Scene Assembly**: Final phase combines all components into complete Godot scenes

## Original C++ Implementation

### Key WCS Source Files

- **`source/code/model/modelread.cpp`**: Complete POF format implementation and chunk parsing
- **`source/code/model/modelsinc.h`**: POF chunk definitions and data structures
- **`source/code/model/model.h`**: Model data structures and type definitions
- **`source/code/model/modelinterp.cpp`**: BSP data interpretation and geometry processing

### POF Format Specification

```cpp
// POF File Structure
POF_HEADER_ID (0x4f505350 = 'OPSP')
Version (int32)
[Chunks...]

// Major Chunk Types
ID_OHDR (0x32524448 = 'HDR2'): Object header with model properties
ID_SOBJ (0x324a424f = 'OBJ2'): Subobject with geometry and hierarchy
ID_TXTR (0x52545854 = 'TXTR'): Texture filename list
ID_SPCL (0x4c435053 = 'SPCL'): Special points (engines, sensors, etc.)
ID_GPNT (0x544e5047 = 'GPNT'): Gun hardpoints
ID_MPNT (0x544e504d = 'MPNT'): Missile hardpoints
ID_DOCK (0x4b434f44 = 'DOCK'): Docking points
ID_FUEL (0x4c455546 = 'FUEL'): Thruster points
ID_SHLD (0x444c4853 = 'SHLD'): Shield mesh geometry
```

## Core Classes

### POFParser
Core POF file parser that handles chunk-based parsing.
- **Purpose**: Parse POF binary files into structured data dictionaries
- **Key Methods**: `parse()`, `get_subobject_bsp_data()`
- **Architecture**: Chunk reader system with specialized parsers for each chunk type

### POFFormatAnalyzer
Comprehensive POF format analysis and validation.
- **Purpose**: Analyze POF file structure, validate format compliance, extract metadata
- **Key Methods**: `analyze_format()`, `validate_format_compliance()` 
- **Features**: Chunk detection, version compatibility checking, format validation

### POFDataExtractor
Structured data extraction for conversion workflows.
- **Purpose**: Extract geometry, materials, and gameplay data for Godot conversion
- **Key Methods**: `extract_model_data()`, `extract_for_godot_conversion()`
- **Output**: POFModelData objects with complete model information

### POFMeshConverter
Complete POF to glTF conversion pipeline.
- **Purpose**: Manage the complete conversion from POF → glTF with metadata preservation
- **Key Methods**: `convert_pof_to_glb()`, `convert_directory()`
- **Output**: glTF files with minimal extras for visual data

### POFOBJConverter
POF to intermediate format converter.
- **Purpose**: Convert POF geometry to intermediate format with material files
- **Key Methods**: `convert_pof_to_obj()`, coordinate/UV conversion functions
- **Features**: Coordinate system conversion, polygon triangulation, material mapping

### POFLODProcessor
LOD (Level of Detail) hierarchy processor for performance optimization.
- **Purpose**: Create multiple detail levels for distance-based rendering optimization
- **Key Methods**: `create_lod_hierarchy()`, `generate_lod_variants()`, `validate_lod_hierarchy()`
- **Features**: Progressive vertex/triangle reduction, texture resolution scaling

### GodotMaterialConverter
WCS to Godot material conversion with StandardMaterial3D optimization.
- **Purpose**: Convert WCS materials to Godot equivalents with proper shader assignment
- **Key Methods**: `convert_material()`, `convert_material_batch()`
- **Features**: Render mode mapping, texture path conversion, transparency handling

### CollisionMeshGenerator
Optimized physics collision mesh generator.
- **Purpose**: Create efficient collision shapes for physics interaction
- **Key Methods**: `generate_collision_mesh()`, support for various collision shapes
- **Features**: Subsystem collision preservation, performance-targeted optimization

## Usage Examples

### Basic POF File Analysis
```python
from pof_parser import POFFormatAnalyzer

analyzer = POFFormatAnalyzer()
analysis = analyzer.analyze_format(Path('ship.pof'))

print(f"POF Version: {analysis.version}")
print(f"Valid Header: {analysis.valid_header}")
print(f"Total Chunks: {analysis.total_chunks}")
print(f"Chunk Types: {analysis.chunk_count_by_type}")

# Validate format compliance
issues = analyzer.validate_format_compliance(analysis)
if not issues:
    print("✓ Format compliance: PASSED")
```

### Data Extraction for Conversion
```python
from pof_parser import POFDataExtractor

extractor = POFDataExtractor()

# Extract complete model data
model_data = extractor.extract_model_data(Path('fighter.pof'))
print(f"Subobjects: {len(model_data.subobjects)}")
print(f"Textures: {len(model_data.textures)}")
print(f"Weapon Points: {len(model_data.weapon_points)}")

# Extract conversion-ready format
conversion_data = extractor.extract_for_conversion(Path('fighter.pof'))
```

### POF to glTF Conversion
```python
from pathlib import Path
from pof_parser import POFMeshConverter

# Initialize converter
converter = POFMeshConverter()

# Convert single POF to glTF
report = converter.convert_pof_to_glb(
    pof_path=Path('fighter.pof'),
    glb_path=Path('fighter.glb'),
    texture_dir=Path('textures/'),
    model_type='ship'
)

if report.success:
    print(f"✓ Conversion successful: {report.conversion_time:.2f}s")
    print(f"  Vertices: {report.obj_vertices:,}")
    print(f"  Faces: {report.obj_faces:,}")
    print(f"  Materials: {report.obj_materials}")
else:
    print("✗ Conversion failed:")
    for error in report.errors:
        print(f"  {error}")

# Batch convert directory
reports = converter.convert_directory(
    input_dir=Path('pof_models/'),
    output_dir=Path('glb_models/'),
    texture_dir=Path('textures/')
)
```

### Command-Line Interface
```bash
# Analyze POF format
python -m pof_parser.cli analyze ship.pof

# Extract data for conversion  
python -m pof_parser.cli extract ship.pof --output ship_data.json

# Convert POF to glTF format
python -m pof_parser.cli convert ship.pof --output ship.glb --textures textures/

# Batch convert POF models to glTF
python -m pof_parser.cli convert models/ --output-dir glb_models/ --textures textures/
```

## Integration with Conversion Pipeline

### Data Flow
1. **Format Analysis**: Validate POF structure and extract metadata
2. **Chunk Parsing**: Parse individual chunks into structured data
3. **Data Extraction**: Transform parsed data into conversion-ready format
4. **glTF Generation**: Convert to glTF format with minimal extras for visual data

### Scene Assembly Preparation
- Outputs glTF files with proper node hierarchy
- Preserves all metadata points (weapon mounts, thrusters, etc.)
- Uses minimal extras to avoid duplication with table data
- Ready for final scene assembly with table data integration

### Asset Management
- References converted texture assets from separate processing
- Follows standardized directory organization
- Maintains compatibility with Godot's import system

## Performance Characteristics

### Memory Management
- **Streaming Parsing**: Large POF files parsed without loading entire file into memory
- **BSP Caching**: On-demand BSP data loading with intelligent caching
- **Chunk Skipping**: Unknown chunks skipped efficiently without memory allocation

### Processing Efficiency
- **Single-Pass Parsing**: Complete model data extracted in one file read
- **Lazy Evaluation**: Complex geometry processing deferred until needed
- **Parallel-Ready**: Data structures designed for concurrent processing

### Scalability
- **Large Model Support**: Handles complex models with 100+ subobjects
- **Batch Processing**: CLI supports directory-level batch operations
- **Memory Limits**: Graceful handling of memory-constrained environments

## Testing

### Unit Testing
```python
# Run comprehensive test suite
python -m pof_parser.test_pof_parser

# Test individual components
python -m unittest pof_parser.test_pof_parser.TestPOFFormatAnalyzer
```

### Integration Testing
- **Format Validation**: Tests with various POF versions and chunk combinations
- **Data Consistency**: Validates consistency between analyzer and extractor outputs
- **Error Handling**: Tests with corrupted, incomplete, and invalid POF files

### Quality Assurance
**Production-ready** with:
- Full error handling and data consistency checks
- Optimized for large model collections with parallel processing
- Seamless integration with conversion pipeline workflow
- Comprehensive validation and testing coverage
