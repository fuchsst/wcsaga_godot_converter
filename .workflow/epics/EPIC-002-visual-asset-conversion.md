# EPIC-002: Visual Asset Conversion (POF/PCX/DDS → glTF/WebP)

## PRD Reference
[PRD-001: Data Converter System](../prds/PRD-001-data-converter-system.md)

## Technical Scope
Convert 3D ship models (POF), textures (PCX/DDS) to Godot-compatible formats (glTF for models, WebP for textures). This includes handling material properties, UV mapping, and texture compression optimization.

## Implementation Phases
### Phase 1: POF model parser with geometry and hierarchy extraction
- Implement POF format parser with complete geometry extraction
- Extract model hierarchy and hardpoint metadata for gameplay systems
- Handle animation data and subsystem information

### Phase 2: Texture format conversion (PCX/DDS → WebP) with quality preservation
- Convert PCX/DDS paletted/images to RGB/RGBA with transparency
- Generate optimized textures with mipmaps for performance
- Preserve texture quality while reducing file sizes

### Phase 3: Material property mapping to Godot StandardMaterial3D
- Map legacy material properties to Godot's material system
- Handle shader-specific properties and rendering flags
- Implement proper texture assignment and UV mapping

### Phase 4: glTF export with proper node structure and animations
- Generate glTF 2.0 files preserving model hierarchy
- Export animation data with proper timing information
- Ensure compatibility with Godot's glTF importer

## Acceptance Criteria
- All visual assets converted without quality degradation
- glTF models render correctly in Godot with proper materials
- WebP textures display with appropriate compression ratios
- LOD hierarchy preserved from original POF files
- Hardpoint and subsystem metadata properly extracted

## Agent Assignments
- **asset-pipeline-engineer**: POF/PCX/DDS parsing and conversion
- **godot-systems-designer**: Material mapping and glTF export
- **qa-engineer**: Visual quality validation and performance testing

## Success Metrics
- 95%+ of visual assets successfully converted
- <5% increase in file size compared to original assets
- 60 FPS rendering performance on target hardware
- Visual fidelity maintained indistinguishable from originals
- Metadata preservation for gameplay systems