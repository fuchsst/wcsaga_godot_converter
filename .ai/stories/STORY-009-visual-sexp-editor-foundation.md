# User Story: Visual SEXP Editor Foundation

**Story ID**: STORY-009  
**Epic**: EPIC-002 (FRED2 Mission Editor)  
**Phase**: 2 (Essential Editing)  
**Priority**: Critical  
**Story Points**: 15  
**Assignee**: Dev (GDScript Developer)  
**Status**: Completed ✅  
**Completion Date**: 2025-01-25  

## User Story

**As a** mission creator  
**I want** a visual node-based editor for creating SEXP expressions  
**So that** I can build complex mission logic without writing text-based S-expressions manually

## Background Context

The SEXP (S-expression) system is the core scripting language for WCS missions, with over 1000 operators controlling everything from ship AI to mission events. The original FRED2 uses a text-based tree editor that's difficult for new users. A visual node-based editor similar to Godot's Visual Script or Blender's shader nodes will dramatically improve usability.

This foundation story establishes the core visual editing framework that will be extended with specific operators in later stories.

## Acceptance Criteria

### AC-009-1: Visual Node System Foundation
```gherkin
Given I have the FRED2 mission editor open
When I access the SEXP editor
Then I should see a node-based visual interface
And I should be able to create new nodes by right-clicking
And I should be able to connect nodes with visual connections
And I should be able to delete nodes and connections
And the interface should feel familiar to Godot users
```

### AC-009-2: Basic SEXP Operator Nodes
```gherkin
Given I'm in the visual SEXP editor
When I create a new operator node
Then I should have access to basic operators including:
  - Arithmetic: +, -, *, /, mod
  - Comparison: <, >, =, !=, <=, >=
  - Logic: and, or, not
  - Constants: true, false, numbers, strings
  - Variables: mission variables access
And each node should show appropriate input/output ports
And node types should be color-coded for easy identification
```

### AC-009-3: Connection System
```gherkin
Given I have SEXP operator nodes in the editor
When I drag from an output port to an input port
Then a connection should be created if types are compatible
And incompatible connections should be rejected with visual feedback
And connections should be drawn as smooth curves
And I should be able to delete connections by selecting and pressing delete
And connection points should highlight on hover
```

### AC-009-4: Type Safety and Validation
```gherkin
Given I'm building a SEXP expression with connected nodes
When I connect nodes together
Then the system should validate type compatibility
And type errors should be highlighted in red
And valid connections should use appropriate colors
And tooltip hints should show expected types for ports
And the expression should validate in real-time
```

### AC-009-5: Expression Output and Integration
```gherkin
Given I have a complete SEXP expression built visually
When I finish editing
Then the visual graph should generate valid SEXP text output
And the output should be compatible with WCS mission format
And I should be able to preview the generated SEXP code
And the expression should integrate with mission object properties
And changes should immediately affect the mission data
```

### AC-009-6: User Experience Features
```gherkin
Given I'm working in the visual SEXP editor
When I'm building expressions
Then I should have these UX features:
  - Pan and zoom with mouse wheel and middle-click drag
  - Box selection for multiple nodes
  - Copy/paste for node groups
  - Undo/redo for all operations
  - Search/filter for available operators
  - Minimap for navigation in large expressions
And the interface should maintain 60 FPS performance
```

## Technical Implementation Notes

### Core Classes Required
```gdscript
# Main visual SEXP editor interface
class_name VisualSexpEditor extends Control

# Individual SEXP operator nodes
class_name SexpOperatorNode extends GraphNode

# SEXP expression graph container
class_name SexpGraph extends GraphEdit

# SEXP operator registry and definitions
class_name SexpOperatorRegistry extends RefCounted

# Type system for SEXP validation
class_name SexpTypeSystem extends RefCounted

# SEXP code generation from visual graph
class_name SexpCodeGenerator extends RefCounted
```

### Architecture Integration
```
addons/gfred2/sexp_editor/
├── visual_sexp_editor.gd       # Main editor interface
├── nodes/
│   ├── sexp_operator_node.gd   # Base operator node
│   ├── arithmetic_nodes.gd     # Math operator nodes
│   ├── logic_nodes.gd          # Boolean logic nodes
│   ├── comparison_nodes.gd     # Comparison operator nodes
│   ├── constant_nodes.gd       # Constant value nodes
│   └── variable_nodes.gd       # Mission variable nodes
├── graph/
│   ├── sexp_graph.gd           # Graph container
│   ├── connection_manager.gd   # Connection handling
│   └── type_validator.gd       # Type checking system
├── registry/
│   ├── operator_registry.gd    # Available operators
│   ├── operator_definitions.gd # Operator metadata
│   └── type_definitions.gd     # SEXP type system
└── generation/
    ├── code_generator.gd       # Visual → SEXP conversion
    ├── parser.gd               # SEXP → Visual conversion
    └── validator.gd            # Expression validation
```

### Key Operator Categories (Phase 1)
**Arithmetic Operators**:
- `+`, `-`, `*`, `/`, `mod`
- Input: Numbers, Output: Number

**Comparison Operators**:
- `<`, `>`, `=`, `!=`, `<=`, `>=`
- Input: Numbers/Strings, Output: Boolean

**Logic Operators**:
- `and`, `or`, `not`
- Input: Booleans, Output: Boolean

**Constants**:
- `true`, `false`, number literals, string literals
- Input: None, Output: Typed value

**Variables**:
- Mission variable access (`get-variable`, `set-variable`)
- Input/Output: Based on variable type

## Dependencies

### Technical Dependencies
- Mission Data Resource System (STORY-005) ✅
- Mission Object Management (STORY-008) ✅
- Godot's GraphEdit and GraphNode classes
- SEXP operator definitions from WCS analysis

### Design Dependencies
- SEXP operator analysis from `source/code/parse/sexp.cpp`
- Type system understanding from WCS SEXP documentation
- UI/UX patterns from modern node editors (Blender, Godot Visual Script)

## Definition of Done

- [ ] Visual node-based SEXP editor interface functional
- [ ] Core operator set (30+ operators) implemented as visual nodes
- [ ] Type-safe connection system with visual feedback
- [ ] Real-time expression validation and error highlighting
- [ ] Code generation produces valid SEXP output
- [ ] Integration with mission object properties working
- [ ] Performance targets met (60 FPS with 100+ nodes)
- [ ] User experience features complete (zoom, pan, undo/redo)
- [ ] Unit tests for core functionality (>90% coverage)
- [ ] Integration tests validate SEXP output compatibility
- [ ] Documentation updated with usage examples

## Success Metrics

**Functionality Metrics**:
- All basic operator types functional
- Type system catches 95% of invalid connections
- Generated SEXP code validates correctly
- Integration with mission data working

**Performance Metrics**:
- Editor maintains 60 FPS with 100+ nodes
- Expression evaluation <10ms for complex graphs
- Memory usage <50MB for large expressions

**User Experience Metrics**:
- New users can create basic expressions within 10 minutes
- Complex expressions 70% faster to create than text editing
- Error discovery rate improved 80% over text editing

## Risks and Mitigation

**High Risks**:
- SEXP operator complexity may overwhelm visual interface
- Performance issues with large expression graphs
- Type system complexity for WCS-specific data types

**Mitigation Strategies**:
- Progressive disclosure - start with core operators only
- Level-of-detail rendering for performance optimization
- Clear type visualization with color coding and tooltips

---

**Story Manager**: SallySM  
**Technical Reviewer**: Mo (Architecture validation)  
**Implementation**: Dev (GDScript Developer)  
**Created**: 2025-01-25  
**Story Dependencies**: STORY-005, STORY-008  
**Blocks**: STORY-013 (Complete SEXP Operator Set)