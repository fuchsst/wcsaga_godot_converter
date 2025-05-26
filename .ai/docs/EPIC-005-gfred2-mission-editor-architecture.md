# EPIC-005: GFRED2 Mission Editor - Architecture

**Document Version**: 1.1  
**Date**: 2025-01-25 (Updated: 2025-01-26)  
**Architect**: Mo (Godot Architect)  
**Epic**: EPIC-005 - GFRED2 Mission Editor  
**System**: Comprehensive mission editor as Godot plugin  
**Approval Status**: APPROVED (Progress: Phase 2 Complete)

---

## Architecture Philosophy (Mo's Principles)

> **"We're not porting C++ to GDScript - we're reimagining mission editing with Godot's strengths."**
> 
> This architecture leverages Godot's scene system, node composition, signal-driven communication, and built-in editor tools to create something BETTER than the original FRED2, not just equivalent.

### Core Design Principles

1. **Scene-Centric Design**: Every mission is a Godot scene with composable node hierarchy
2. **Signal-Driven Architecture**: Loose coupling through Godot's signal system
3. **Resource-Based Data**: Leverage Godot's resource system for data persistence
4. **Tool Script Integration**: Native editor extension using Godot's plugin architecture
5. **Node Composition Over Inheritance**: Prefer composition for flexible, maintainable systems
6. **Type Safety**: Static typing throughout for reliability and performance

## System Architecture Overview

```
WCS Mission Editor Plugin
├── addons/gfred2/                   # Godot plugin structure (mission editor)
│   ├── plugin.cfg                  # Plugin configuration
│   ├── plugin.gd                   # Main plugin entry point
│   ├── data/                       # Resource definitions for migrated data
│   ├── object_management/          # Mission object lifecycle management
│   ├── ui/                         # User interface components
│   ├── viewport/                   # 3D editing tools and gizmos
│   └── validation/                 # Validation and testing
│
├── migration_tools/                # Python-based data conversion (separate repo/tool)
│   ├── pof_converter.py           # POF → Godot model conversion
│   ├── mission_converter.py       # .fs2 → Godot Resource conversion
│   ├── save_migrator.py           # .PLR/.CSG → Godot Resource
│   ├── asset_pipeline.py          # Audio/video conversion with FFmpeg
│   └── godot_integration.py       # Integration with Godot import system
│
├── scripts/                        # Main game systems (separate from editor)
│   ├── globals/                    # Game autoloads
│   ├── core_systems/              # Physics, AI, weapons, etc.
│   └── ship/                       # Ship mechanics
│
└── resources/                      # Godot Resources created by migration tools
    ├── missions/                   # Converted mission data
    ├── ships/                      # Ship data and models
    ├── weapons/                    # Weapon definitions
    └── saves/                      # Player save data
```

## Core Architecture Components

### 1. Migration Tools Architecture (Python-Based)

**Philosophy**: Separate data conversion layer using Python tools with FFmpeg integration for comprehensive WCS data migration to Godot Resources.

```python
# Core migration tool architecture
class WCSMigrator:
    """Central coordinator for WCS data migration"""
    
    def __init__(self):
        self.pof_converter = POFConverter()
        self.mission_parser = MissionParser()
        self.save_migrator = SaveMigrator()
        self.asset_pipeline = AssetPipeline()
    
    def migrate_mission(self, fs2_path: str) -> str:
        """Convert .fs2 mission to Godot Resource"""
        mission_data = self.mission_parser.parse_fs2(fs2_path)
        return self.export_godot_resource(mission_data)
    
    def migrate_model(self, pof_path: str) -> str:
        """Convert .POF model to Godot .glb/.tscn"""
        return self.pof_converter.convert_to_godot(pof_path)

# Asset pipeline with FFmpeg integration
class AssetPipeline:
    """Handles audio/video conversion using FFmpeg"""
    
    def convert_audio(self, wav_path: str) -> str:
        """Convert WCS audio to OGG for Godot"""
        subprocess.run([
            'ffmpeg', '-i', wav_path,
            '-codec:a', 'libvorbis', output_path
        ])
    
    def convert_video(self, ani_path: str) -> str:
        """Convert ANI files to WebM for Godot"""
        # FFmpeg conversion logic
```

### 2. Mission Data Model (Resource-Based)

**Philosophy**: Use Godot's resource system for type-safe, serializable mission data that integrates seamlessly with the editor and works with migrated data.

```gdscript
# Core mission resource - replaces C++ mission struct
class_name MissionData
extends Resource

## Central mission data structure using Godot's resource system
## Provides serialization, type safety, and editor integration

@export var mission_info: MissionInfo
@export var objects: Array[MissionObject] = []
@export var wings: Array[WingFormation] = []
@export var events: Array[MissionEvent] = []
@export var goals: Array[MissionGoal] = []
@export var briefing: BriefingData
@export var background: BackgroundData

signal data_changed(property: String, old_value: Variant, new_value: Variant)

func validate() -> ValidationResult:
    # Comprehensive mission validation
    pass

func export_to_fs2() -> String:
    # Export to legacy .fs2 format
    pass
```

```gdscript
# Individual mission object - composable and type-safe
class_name MissionObject
extends Resource

@export var object_name: String = ""
@export var object_type: ObjectType
@export var position: Vector3 = Vector3.ZERO
@export var rotation: Vector3 = Vector3.ZERO
@export var ship_class: String = ""
@export var team: int = 0
@export var ai_behavior: AIBehavior
@export var arrival_cue: SexpNode
@export var departure_cue: SexpNode
@export var special_properties: Dictionary = {}

signal property_changed(property: String, value: Variant)
```

### 2. SEXP System Architecture (Node-Based)

**Philosophy**: Replace C++ tree structures with Godot's scene nodes for visual editing and intuitive manipulation.

```gdscript
# Base SEXP node - uses Godot's node system
class_name SexpNode
extends Node

## Base class for all SEXP operations
## Leverages Godot's node tree for visual representation

@export var operator_type: String = ""
@export var parameters: Array[Variant] = []
@export var return_type: SexpType

signal value_changed(new_value: Variant)
signal validation_changed(is_valid: bool, errors: Array[String])

func evaluate(context: MissionContext) -> Variant:
    # Override in subclasses
    pass

func validate() -> ValidationResult:
    # Type checking and dependency validation
    pass

func get_visual_representation() -> Control:
    # Return UI node for visual editor
    pass
```

```gdscript
# Specific SEXP operator implementation
class_name SexpIsDestroyed
extends SexpNode

## SEXP operator: (is-destroyed "ship_name" [delay])
## Type-safe implementation with validation

@export var ship_name: String = ""
@export var delay: float = 0.0

func _init():
    operator_type = "is-destroyed"
    return_type = SexpType.BOOLEAN

func evaluate(context: MissionContext) -> bool:
    var ship = context.get_ship(ship_name)
    if not ship:
        return false
    return ship.is_destroyed_for_time(delay)

func validate() -> ValidationResult:
    var result = ValidationResult.new()
    if ship_name.is_empty():
        result.add_error("Ship name cannot be empty")
    return result
```

### 3. Editor UI Architecture (Dockable Panels)

**Philosophy**: Leverage Godot's built-in editor dock system for familiar, professional UI that integrates seamlessly with the main editor.

```gdscript
# Main mission editor dock
class_name MissionEditorDock
extends EditorPlugin

## Primary editor interface integrated into Godot's editor
## Uses familiar dock patterns for professional workflow

var main_panel: MissionEditorPanel
var object_inspector: ObjectInspectorDock
var sexp_editor: SexpEditorDock
var asset_browser: AssetBrowserDock
var validation_panel: ValidationDock

func _enter_tree():
    # Register editor docks
    main_panel = preload("res://addons/mission_editor/ui/MissionEditorPanel.tscn").instantiate()
    add_control_to_dock(DOCK_SLOT_LEFT_UL, main_panel)
    
    object_inspector = preload("res://addons/mission_editor/ui/ObjectInspectorDock.tscn").instantiate()
    add_control_to_dock(DOCK_SLOT_LEFT_BL, object_inspector)
    
    # Connect signals for coordinated updates
    _connect_editor_signals()

func _exit_tree():
    # Clean up docks
    remove_control_from_docks(main_panel)
    remove_control_from_docks(object_inspector)
```

```gdscript
# 3D viewport integration
class_name MissionViewport3D
extends SubViewport

## Custom 3D viewport for mission editing
## Integrates with Godot's built-in 3D editor tools

@onready var camera: Camera3D = $Camera3D
@onready var gizmo_plugin: MissionGizmoPlugin

signal object_selected(mission_object: MissionObject)
signal objects_transformed(objects: Array[MissionObject])

func _ready():
    # Setup 3D environment
    setup_environment()
    setup_camera_controls()
    setup_object_gizmos()

func add_mission_object(object_data: MissionObject) -> Node3D:
    var object_node = MissionObjectNode3D.new()
    object_node.setup_from_data(object_data)
    add_child(object_node)
    return object_node

func setup_object_gizmos():
    gizmo_plugin = MissionGizmoPlugin.new()
    EditorInterface.get_editor_main_screen().add_child(gizmo_plugin)
```

### 4. Asset Integration System

**Philosophy**: Seamless integration with Godot's asset pipeline while maintaining WCS compatibility.

```gdscript
# Asset registry for WCS-specific assets
class_name WCSAssetRegistry
extends RefCounted

## Central registry for all WCS assets (ships, weapons, textures)
## Bridges WCS formats with Godot's resource system

signal asset_loaded(asset_id: String, asset: Resource)
signal asset_registry_updated()

var ship_classes: Dictionary = {}  # String -> ShipClassResource
var weapon_types: Dictionary = {}  # String -> WeaponResource
var textures: Dictionary = {}      # String -> Texture2D

func register_ship_class(class_id: String, resource_path: String):
    var ship_resource = load(resource_path) as ShipClassResource
    ship_classes[class_id] = ship_resource
    asset_loaded.emit(class_id, ship_resource)

func get_ship_preview(class_id: String) -> PackedScene:
    # Return 3D preview scene for mission editor
    var ship_data = ship_classes.get(class_id)
    if ship_data:
        return ship_data.get_preview_scene()
    return null

func validate_asset_references(mission: MissionData) -> ValidationResult:
    # Check all mission objects reference valid assets
    pass
```

```gdscript
# Ship class resource - bridges WCS ship data with Godot
class_name ShipClassResource
extends Resource

## WCS ship class converted to Godot resource
## Provides all ship properties in type-safe format

@export var class_name: String = ""
@export var display_name: String = ""
@export var model_path: String = ""
@export var texture_path: String = ""
@export var max_hull: float = 100.0
@export var max_shields: float = 100.0
@export var max_speed: float = 50.0
@export var weapons: Array[WeaponSlot] = []
@export var subsystems: Array[SubsystemData] = []

func get_preview_scene() -> PackedScene:
    # Generate 3D preview for mission editor
    var scene = PackedScene.new()
    var model_node = preload(model_path).instantiate()
    # Configure for editor preview
    return scene

func export_to_fs2_format() -> Dictionary:
    # Convert back to FS2 ship class format
    pass
```

### 5. Import/Export Architecture

**Philosophy**: Robust file format handling with clear separation of concerns and comprehensive error handling.

```gdscript
# FS2 mission file importer
class_name FS2MissionImporter
extends RefCounted

## Imports legacy .fs2 mission files to MissionData resources
## Handles all format variations and error conditions

signal import_progress(percentage: float, message: String)
signal import_complete(mission_data: MissionData)
signal import_error(error: String, line_number: int)

func import_mission(file_path: String) -> MissionData:
    var file = FileAccess.open(file_path, FileAccess.READ)
    if not file:
        push_error("Cannot open mission file: " + file_path)
        return null
    
    var mission_data = MissionData.new()
    var parser = FS2Parser.new()
    
    import_progress.emit(0.0, "Reading mission file...")
    
    # Parse each section of the .fs2 file
    while not file.eof_reached():
        var line = file.get_line().strip_edges()
        if line.begins_with("#"):
            _parse_section(parser, line, file, mission_data)
        import_progress.emit(file.get_position() / file.get_length() * 100.0, "Parsing...")
    
    file.close()
    import_progress.emit(100.0, "Import complete")
    import_complete.emit(mission_data)
    return mission_data

func _parse_section(parser: FS2Parser, section_header: String, file: FileAccess, mission_data: MissionData):
    match section_header:
        "#Mission Info":
            parser.parse_mission_info(file, mission_data.mission_info)
        "#Objects":
            parser.parse_objects(file, mission_data.objects)
        "#Events":
            parser.parse_events(file, mission_data.events)
        "#Goals":
            parser.parse_goals(file, mission_data.goals)
        _:
            push_warning("Unknown section: " + section_header)
```

```gdscript
# FS2 mission file exporter
class_name FS2MissionExporter
extends RefCounted

## Exports MissionData resources to .fs2 format
## Maintains compatibility with original FRED2 and WCS runtime

func export_mission(mission_data: MissionData, file_path: String) -> Error:
    var file = FileAccess.open(file_path, FileAccess.WRITE)
    if not file:
        return ERR_FILE_CANT_WRITE
    
    # Write mission sections in correct order
    _write_mission_info(file, mission_data.mission_info)
    _write_objects(file, mission_data.objects)
    _write_wings(file, mission_data.wings)
    _write_events(file, mission_data.events)
    _write_goals(file, mission_data.goals)
    _write_briefing(file, mission_data.briefing)
    
    file.close()
    return OK

func _write_mission_info(file: FileAccess, info: MissionInfo):
    file.store_line("#Mission Info")
    file.store_line("$Version: " + str(info.version))
    file.store_line("$Name: " + info.name)
    file.store_line("$Author: " + info.author)
    # ... continue with all mission info fields
```

### 6. Validation and Testing Architecture

**Philosophy**: Real-time validation with comprehensive error checking and performance analysis.

```gdscript
# Mission validation system
class_name MissionValidator
extends RefCounted

## Comprehensive mission validation with real-time feedback
## Checks logic, references, performance, and compatibility

signal validation_started()
signal validation_progress(percentage: float, current_check: String)
signal validation_complete(result: ValidationResult)

var asset_registry: WCSAssetRegistry
var sexp_validator: SexpValidator

func validate_mission(mission_data: MissionData) -> ValidationResult:
    validation_started.emit()
    
    var result = ValidationResult.new()
    var checks = [
        _validate_mission_info,
        _validate_objects,
        _validate_events,
        _validate_sexp_trees,
        _validate_asset_references,
        _validate_performance
    ]
    
    for i in range(checks.size()):
        var check_func = checks[i]
        validation_progress.emit(float(i) / checks.size() * 100.0, check_func.get_method())
        var check_result = check_func.call(mission_data)
        result.merge(check_result)
    
    validation_complete.emit(result)
    return result

func _validate_objects(mission_data: MissionData) -> ValidationResult:
    var result = ValidationResult.new()
    
    for obj in mission_data.objects:
        # Validate ship class exists
        if not asset_registry.ship_classes.has(obj.ship_class):
            result.add_error("Unknown ship class: " + obj.ship_class, obj)
        
        # Validate team assignments
        if obj.team < 0 or obj.team > 3:
            result.add_warning("Invalid team assignment: " + str(obj.team), obj)
        
        # Validate position bounds
        if obj.position.length() > 100000:
            result.add_warning("Object very far from origin", obj)
    
    return result

func _validate_sexp_trees(mission_data: MissionData) -> ValidationResult:
    var result = ValidationResult.new()
    
    for event in mission_data.events:
        if event.condition:
            var condition_result = sexp_validator.validate_tree(event.condition)
            result.merge(condition_result)
        
        for action in event.actions:
            var action_result = sexp_validator.validate_tree(action)
            result.merge(action_result)
    
    return result
```

## Implementation Architecture by Phase

### Phase 1: Foundation (Core Data + Basic UI)

**Target**: Basic mission loading, object placement, and file saving

```gdscript
# Phase 1 core classes (minimal viable editor)
class_name Phase1MissionEditor
extends EditorPlugin

## Minimal viable mission editor for Phase 1
## Focus: Load missions, place objects, save files

var mission_data: MissionData
var viewport_3d: MissionViewport3D
var object_inspector: SimpleObjectInspector

func _enter_tree():
    add_tool_menu_item("Open Mission", _open_mission)
    add_tool_menu_item("Save Mission", _save_mission)
    
    # Simple 3D viewport for object placement
    viewport_3d = MissionViewport3D.new()
    EditorInterface.get_editor_main_screen().add_child(viewport_3d)

func _open_mission():
    var file_dialog = EditorFileDialog.new()
    file_dialog.file_mode = EditorFileDialog.FILE_MODE_OPEN_FILE
    file_dialog.add_filter("*.fs2", "FreeSpace 2 Mission Files")
    file_dialog.file_selected.connect(_load_mission)
    get_viewport().add_child(file_dialog)
    file_dialog.popup_centered(Vector2i(800, 600))

func _load_mission(path: String):
    var importer = FS2MissionImporter.new()
    mission_data = importer.import_mission(path)
    if mission_data:
        _populate_viewport()

func _populate_viewport():
    # Create 3D representations of mission objects
    for obj in mission_data.objects:
        var node_3d = _create_object_node(obj)
        viewport_3d.add_child(node_3d)
```

### Phase 2: Essential Editing (SEXP + Properties)

**Target**: Visual SEXP editor, property editing, asset integration

```gdscript
# Phase 2 enhanced editor with SEXP support
class_name Phase2MissionEditor
extends Phase1MissionEditor

## Enhanced editor with visual SEXP editing and properties
## Focus: Full editing workflow with validation

var sexp_editor: VisualSexpEditor
var property_panel: ObjectPropertyPanel
var asset_browser: AssetBrowserPanel

func _enter_tree():
    super._enter_tree()
    
    # Add visual SEXP editor
    sexp_editor = preload("res://addons/mission_editor/ui/VisualSexpEditor.tscn").instantiate()
    add_control_to_dock(DOCK_SLOT_LEFT_BR, sexp_editor)
    
    # Add property panel
    property_panel = preload("res://addons/mission_editor/ui/ObjectPropertyPanel.tscn").instantiate()
    add_control_to_dock(DOCK_SLOT_RIGHT_UL, property_panel)
    
    # Connect for coordinated editing
    viewport_3d.object_selected.connect(_on_object_selected)

func _on_object_selected(mission_object: MissionObject):
    # Update property panel
    property_panel.edit_object(mission_object)
    
    # Update SEXP editor if object has conditions
    if mission_object.arrival_cue:
        sexp_editor.edit_sexp_tree(mission_object.arrival_cue)
```

### Phase 3: Advanced Features (Complete SEXP + Validation)

**Target**: Full SEXP operator set, comprehensive validation, briefing editor

```gdscript
# Phase 3 complete editor with all features
class_name Phase3MissionEditor
extends Phase2MissionEditor

## Complete mission editor with all FRED2 features
## Focus: Professional workflow and validation

var validation_panel: ValidationPanel
var briefing_editor: BriefingEditor
var campaign_manager: CampaignManager

func _enter_tree():
    super._enter_tree()
    
    # Add validation panel
    validation_panel = ValidationPanel.new()
    add_control_to_dock(DOCK_SLOT_LEFT_BR, validation_panel)
    
    # Real-time validation
    mission_data.data_changed.connect(_validate_mission_realtime)

func _validate_mission_realtime():
    # Background validation without blocking UI
    var validator = MissionValidator.new()
    validator.validate_mission.call_deferred(mission_data)
```

## Performance Considerations

### Memory Management
- **Object Pooling**: Reuse 3D nodes for mission objects to avoid allocation overhead
- **LOD System**: Level-of-detail for complex ship models in viewport
- **Lazy Loading**: Load assets on-demand rather than preloading entire asset library

### Rendering Optimization
- **Frustum Culling**: Only render objects visible in viewport
- **Instancing**: Use MultiMeshInstance3D for multiple identical objects
- **Shader Optimization**: Simplified shaders for editor preview

### Real-time Validation
- **Background Processing**: Validation runs in separate thread
- **Incremental Validation**: Only re-validate changed portions
- **Caching**: Cache validation results until dependencies change

## Security and Reliability

### File Handling
- **Sandboxed Operations**: All file operations use Godot's secure file access
- **Validation**: Comprehensive input validation for .fs2 files
- **Backup System**: Automatic backups before any destructive operations

### Error Recovery
- **Graceful Degradation**: Editor continues functioning with partial data
- **Undo/Redo**: Complete operation history using Godot's undo/redo system
- **Crash Recovery**: Auto-save and recovery mechanisms

## Integration Points

### Godot Editor Integration
- **Native Docks**: Use Godot's built-in dock system for familiar UI
- **Tool Scripts**: Leverage Godot's @tool annotation for editor scripts
- **Resource System**: Full integration with Godot's resource management
- **Plugin Architecture**: Proper EditorPlugin implementation

### WCS-Godot Runtime Integration
- **Scene Export**: Export missions as .tscn scenes for runtime
- **Resource References**: Seamless asset references between editor and runtime
- **Compatibility Layer**: Maintain .fs2 format compatibility

## Conclusion

This architecture creates a modern, maintainable mission editor that:

1. **Leverages Godot's Strengths**: Scene system, signals, resources, built-in editor
2. **Maintains Compatibility**: Full .fs2 format support for existing missions
3. **Provides Superior UX**: Modern interface with real-time validation
4. **Enables Extensibility**: Plugin architecture for community development
5. **Ensures Performance**: Optimized for large missions and real-time editing

The phased approach allows incremental delivery of value while building toward a comprehensive professional tool.

**Next Step**: Story creation for Phase 1 implementation (Foundation layer).

---

**Approval Required**: This architecture requires approval from SallySM (Story Manager) before proceeding to story creation.

**Architecture Review**: Larry (WCS Analyst) and Dev (GDScript Developer) review recommended.

**Document Control**:
- **Architect**: Mo (Godot Architect)
- **Created**: 2025-01-25
- **Status**: PENDING APPROVAL