# CF-002: Asset Pipeline Foundation

## User Story
**As a** developer converting WCS to Godot  
**I need** to load and convert WCS assets into Godot-compatible formats  
**So that** I can create ships, weapons, environments, and missions using original game data

## Epic
Core Foundation Systems

## Priority
High

## Complexity
High (3-4 days effort)

## Risk Level
Medium - File format reverse engineering required

## Dependencies
- CF-001: Core Manager Infrastructure Setup (✅ Completed)

## Technical Scope

### POF Model Importer
- Parse WCS POF (3D model) file format
- Convert to GLTF/Godot 3D scenes with materials
- Handle LOD levels and damage states
- Extract collision meshes and subsystem definitions
- Preserve WCS-specific metadata (hardpoints, turret mounts, etc.)

### VP Archive Extractor  
- Read WCS VP (archive) file format
- Extract files on-demand or batch processing
- Handle compression and encryption
- Maintain file path mapping for asset references
- Support multiple VP files with priority ordering

### Table File Parser
- Parse WCS table files (ships.tbl, weapons.tbl, ai_profiles.tbl, etc.)
- Convert to Godot Resource classes with proper typing
- Handle WCS scripting expressions and conditional logic
- Support modular table loading and overrides
- Validate data integrity and provide error reporting

### Asset Manager
- Coordinate asset loading pipeline
- Cache converted assets to avoid re-processing
- Handle asset dependencies and references
- Provide async loading for large assets
- Monitor memory usage and implement LRU eviction

## Acceptance Criteria

### ✅ POF Model Import
- [ ] Can load POF files and extract geometry data
- [ ] Convert meshes to Godot MeshInstance3D nodes
- [ ] Apply materials with proper texture mapping
- [ ] Extract subsystem locations and hardpoint data
- [ ] Generate collision shapes from model geometry
- [ ] Support multiple LOD levels
- [ ] Handle special WCS features (glowmaps, engine trails, etc.)

### ✅ VP Archive Handling
- [ ] Can read VP archive headers and file tables
- [ ] Extract individual files with correct paths
- [ ] Handle compressed data streams
- [ ] Support multiple VP files with precedence rules
- [ ] Provide file existence checking without extraction
- [ ] Cache archive metadata for performance

### ✅ Table File Processing
- [ ] Parse all major WCS table file formats
- [ ] Convert to strongly-typed Godot Resources
- [ ] Handle nested data structures and arrays
- [ ] Process conditional statements and expressions
- [ ] Support table inheritance and overrides
- [ ] Validate data consistency and report errors

### ✅ Asset Management
- [ ] AssetManager singleton coordinates all loading
- [ ] Cache system prevents duplicate processing
- [ ] Async loading doesn't block main thread
- [ ] Memory monitoring with configurable limits
- [ ] Debug interface shows loading status and statistics
- [ ] Error handling with graceful fallbacks

### ✅ Integration
- [ ] Integrates with existing ObjectManager for instantiation
- [ ] Compatible with Godot's resource system
- [ ] Works with scene loading and streaming
- [ ] Performance meets target benchmarks (<100ms for typical assets)
- [ ] Unit tests cover all major functionality

## Technical Implementation Plan

### Phase 1: VP Archive Foundation (Day 1)
1. Research WCS VP file format specification
2. Implement VPArchive class for reading file headers
3. Create file extraction and decompression
4. Add VPManager for handling multiple archives
5. Basic unit tests for archive functionality

### Phase 2: Table File Parser (Day 1-2)
1. Analyze WCS table file syntax and structure
2. Implement TableParser with lexical analysis
3. Create Resource classes for major data types (Ship, Weapon, etc.)
4. Handle expressions and conditional logic
5. Add validation and error reporting

### Phase 3: POF Model Importer (Day 2-3)
1. Reverse engineer POF file format structure
2. Implement POFImporter for geometry extraction
3. Convert to Godot mesh data with materials
4. Extract metadata (hardpoints, subsystems, collision)
5. Handle LOD levels and special features

### Phase 4: Asset Manager Integration (Day 3-4)
1. Create AssetManager singleton with caching
2. Implement async loading system
3. Add memory management and monitoring
4. Create debug interface and statistics
5. Integration testing with core managers

### Phase 5: Testing & Documentation (Day 4)
1. Comprehensive unit test suite
2. Performance benchmarking
3. Error handling validation
4. Package documentation
5. Integration with debug overlay

## File Structure
```
target/scripts/assets/
├── CLAUDE.md                 # Package documentation
├── asset_manager.gd          # Main asset coordinator
├── vp_archive.gd            # VP file format handler
├── vp_manager.gd            # Multiple archive management
├── table_parser.gd          # Table file parser
├── pof_importer.gd          # 3D model importer
├── resources/               # Godot Resource classes
│   ├── ship_data.gd
│   ├── weapon_data.gd
│   ├── ai_profile_data.gd
│   └── mission_data.gd
└── importers/               # Godot import plugins
    ├── pof_import_plugin.gd
    └── table_import_plugin.gd

target/tests/
└── test_asset_pipeline.gd   # Comprehensive test suite
```

## Performance Targets
- VP archive file access: <10ms per file
- Table file parsing: <50ms for typical files
- POF model conversion: <200ms for standard ship models
- Asset Manager cache hit: <1ms
- Memory usage: <100MB for typical asset set

## Error Handling
- Graceful fallback for missing assets
- Detailed error messages for malformed files
- Validation warnings for data inconsistencies
- Recovery mechanisms for partial loading failures
- Debug logging for troubleshooting

## Notes
- Consider using LimboAI suggestion for future AI behavior loading
- May need to update core managers to handle new asset types
- Performance optimization will be critical for large WCS campaigns
- Asset pipeline should support both development and runtime scenarios

## Definition of Done
- [ ] All acceptance criteria met and tested
- [ ] Unit tests achieve >90% code coverage
- [ ] Performance benchmarks meet targets
- [ ] Debug overlay shows asset pipeline statistics
- [ ] Package documentation complete
- [ ] Integration with core managers validated
- [ ] Code review completed
- [ ] Changes committed to repository