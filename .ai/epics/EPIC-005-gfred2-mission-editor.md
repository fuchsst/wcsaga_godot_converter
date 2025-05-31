# EPIC-005: GFRED2 Mission Editor

## Epic Overview
**Epic ID**: EPIC-005  
**Epic Name**: GFRED2 Mission Editor  
**Epic Owner**: Larry (WCS Analyst)  
**Priority**: High  
**Status**: Stories Refined - Ready for Implementation  
**Created**: 2025-01-25 (Original), Updated: 2025-01-26  
**Position**: 4 (Development Tools Phase)  
**Duration**: 9.6 weeks (48 days) - Updated with Additional High-Priority Features  

## Epic Description
Create a comprehensive mission editor as a Godot plugin that recreates and enhances the functionality of the original WCS FRED2 (FReespace EDitor version 2) tool. This editor will allow mission creators to design, script, and test missions using modern Godot editor integration while maintaining full compatibility with WCS mission standards and exceeding the original editor's capabilities.

## Progress Summary
**Current Status**: Architecture Refined - Critical Implementation Issues Addressed
- ✅ **Foundation Dependencies**: EPICs 001-004 complete and stable
- ✅ **Phase 1 - Core Framework**: All core integrations complete (GFRED2-001 through GFRED2-004)
- ✅ **Phase 2 - User Experience**: UI modernization complete (GFRED2-005) - May 30, 2025
- ⚡ **CRITICAL ARCHITECTURAL REFINEMENT**: Stories GFRED2-006A through GFRED2-011 refined (May 31, 2025)
- 🔄 **Phase 3 - Advanced Capabilities**: Ready for implementation with corrected architecture
- **URGENT PRIORITY**: UI refactoring to scene-based architecture (GFRED2-011) - ARCHITECTURAL VIOLATION CORRECTION
- **Updated Timeline**: 44 days remaining (8.8 weeks) with mandatory architectural compliance
- **Progress**: 4 of 11 stories complete, 7 stories refined for architectural compliance

## WCS FRED2 System Analysis

### **Core Editor Framework**
- **WCS Systems**: `fred2/fred.cpp`, `fred2/fredview.cpp`, `fred2/freddoc.cpp`
- **Purpose**: Main application framework, document management, view coordination
- **Key Features**:
  - Multi-document interface with tabbed editing
  - Undo/redo system for all operations
  - Real-time 3D preview and manipulation
  - Comprehensive keyboard shortcuts and workflow

### **Object Management System**
- **WCS Systems**: `fred2/management.cpp`, `fred2/ship_select.cpp`, `fred2/wing_editor.cpp`
- **Purpose**: Ship placement, wing formation, object hierarchy management
- **Key Features**:
  - Drag-and-drop object placement
  - Property-based object editing
  - Wing and formation management
  - Object grouping and selection tools

### **Mission Scripting Interface**
- **WCS Systems**: `fred2/sexp_tree.cpp`, `fred2/eventeditor.cpp`, `fred2/missiongoalsdlg.cpp`
- **Purpose**: Visual SEXP editing, event management, mission objectives
- **Key Features**:
  - Tree-based SEXP expression editor
  - Event timeline and trigger management
  - Goal and objective definition
  - Variable management and debugging

### **Asset Integration System**
- **WCS Systems**: `fred2/shipclasseditordlg.cpp`, `fred2/weaponeditordlg.cpp`, `fred2/backgroundchooser.cpp`
- **Purpose**: Asset browser, ship/weapon configuration, environment setup
- **Key Features**:
  - Comprehensive asset browser with filtering
  - Ship class and loadout configuration
  - Weapon and subsystem editing
  - Background and environment selection

## Epic Goals

### Primary Goals
1. **Modern Mission Editing**: Intuitive, powerful mission creation within Godot editor
2. **Enhanced Workflow**: Improved UX over original FRED2 with modern UI patterns
3. **Asset Integration**: Seamless integration with EPIC-003 asset management system
4. **SEXP Visual Editing**: Advanced visual scripting using EPIC-SEXP-001 system
5. **Real-time Testing**: Immediate mission testing and validation within editor

### Success Metrics
- Mission creators can replicate any WCS mission functionality
- 50% faster mission creation workflow compared to original FRED2
- Zero learning curve for experienced FRED2 users
- Real-time validation prevents 90% of common mission errors
- Comprehensive asset discovery and integration capabilities

## Technical Architecture

### GFRED2 Plugin Structure
```
target/addons/gfred2/
├── plugin.cfg                       # Plugin configuration
├── GFRED2Plugin.gd                  # Main plugin class
├── ui/                              # User interface components
│   ├── main_dock/                   # Main editor dock
│   │   ├── mission_editor_dock.gd   # Primary editing interface
│   │   ├── object_hierarchy.gd      # Object tree view
│   │   ├── property_inspector.gd    # Object property editing
│   │   └── mission_toolbar.gd       # Tool buttons and actions
│   ├── asset_browser/               # Asset browsing and selection
│   │   ├── asset_browser_dock.gd    # Asset browser dock
│   │   ├── asset_category_tree.gd   # Categorized asset tree
│   │   ├── asset_preview_panel.gd   # Asset preview and info
│   │   └── asset_search_filter.gd   # Search and filtering
│   ├── sexp_editor/                 # SEXP visual editing
│   │   ├── sexp_editor_dock.gd      # SEXP editing interface
│   │   ├── sexp_tree_view.gd        # Visual expression tree
│   │   ├── sexp_function_palette.gd # Function browser and insertion
│   │   └── sexp_validator.gd        # Real-time SEXP validation
│   ├── mission_settings/            # Mission configuration
│   │   ├── mission_settings_dock.gd # Mission properties panel
│   │   ├── background_editor.gd     # Environment and background
│   │   ├── briefing_editor.gd       # Mission briefing creation
│   │   └── campaign_integration.gd  # Campaign linking and progression
│   └── dialogs/                     # Modal dialogs and wizards
│       ├── object_creation_dialog.gd # Object creation wizard
│       ├── wing_formation_dialog.gd # Wing setup and formation
│       ├── event_creation_dialog.gd # Event and trigger creation
│       └── mission_validation_dialog.gd # Mission validation results
├── core/                            # Core editing functionality
│   ├── mission_document.gd          # Mission data model
│   ├── editor_state_manager.gd      # Editor state and undo/redo
│   ├── object_manager.gd            # Object creation and manipulation
│   ├── selection_manager.gd         # Object selection and grouping
│   ├── camera_controller.gd         # 3D viewport camera control
│   └── grid_manager.gd              # Grid display and snapping
├── tools/                           # Editing tools and utilities
│   ├── placement_tools.gd           # Object placement and positioning
│   ├── transformation_tools.gd      # Move, rotate, scale operations
│   ├── measurement_tools.gd         # Distance and angle measurement
│   ├── alignment_tools.gd           # Object alignment and distribution
│   └── validation_tools.gd          # Mission validation and checking
├── integration/                     # System integration
│   ├── asset_integration.gd         # EPIC-003 asset system integration
│   ├── sexp_integration.gd          # EPIC-SEXP-001 integration
│   ├── migration_integration.gd     # EPIC-MIG-001 conversion support
│   └── game_testing_integration.gd  # Real-time mission testing
└── data/                            # Editor data and configuration
    ├── editor_settings.gd           # Editor configuration and preferences
    ├── template_missions.gd         # Mission templates and examples
    ├── keyboard_shortcuts.gd        # Customizable keyboard shortcuts
    └── user_preferences.gd          # User customization and workflow
```

### Integration Points
- **EPIC-003**: Asset Structures and Management Addon (asset browsing and integration)
- **EPIC-MIG-001**: Data Migration Tools (import existing missions)
- **EPIC-SEXP-001**: SEXP Expression System (visual scripting and validation)
- **Godot Editor**: Native integration with Godot's editor plugin system
- **Main Game**: Real-time mission testing and validation

## Integration Story Breakdown (REFINED BY BMAD TEAM)

### Phase 1: Foundation Integration (2 weeks) - IN PROGRESS ⚡
- **GFRED2-004**: Core Infrastructure Integration with EPIC-001 (2 days) ⏳ **READY**
- **GFRED2-001**: Asset System Integration with EPIC-002 (3 days) ⏳ **READY**
- **GFRED2-003**: Mission File Conversion Integration with EPIC-003 (3 days) ✅ **COMPLETED** (Review: [GFRED2-003-review.md](.ai/reviews/EPIC-005-gfred2-mission-editor/GFRED2-003-review.md))
- **GFRED2-002**: SEXP System Integration with EPIC-004 (5 days) ✅ **COMPLETED** (Review: [GFRED2-002-review.md](.ai/reviews/EPIC-005-gfred2-mission-editor/GFRED2-002-review.md))

### Phase 2: User Experience Enhancement (1 week) - READY
- **GFRED2-005**: UI Modernization and Polish (4 days) ✅ **COMPLETED** (Date: May 30, 2025)

### Phase 3: Advanced Capabilities (2.5 weeks) - IN PROGRESS
- **GFRED2-006A**: Real-time Validation and Dependency Tracking (3 days) ✅ **COMPLETED** (Date: May 31, 2025)
- **GFRED2-006B**: Advanced SEXP Debugging Integration (3 days) ✅ **COMPLETED** (Date: May 31, 2025)
- **GFRED2-006C**: Mission Templates and Pattern Library (4 days) ⏳ **READY**
- **GFRED2-006D**: Performance Profiling and Optimization Tools (3 days) ⏳ **READY**

### Phase 4: Critical Feature Parity (3.6 weeks) - NEW HIGH-PRIORITY ⚡
- **GFRED2-007**: Briefing Editor System (5 days) ⏳ **NEW CRITICAL**
- **GFRED2-008**: Campaign Editor Integration (4 days) ⏳ **NEW CRITICAL**
- **GFRED2-009**: Advanced Ship Configuration (4 days) ⏳ **NEW CRITICAL**
- **GFRED2-010**: Mission Component Editors (5 days) ⏳ **NEW CRITICAL**

**FEATURE PARITY ANALYSIS**: Larry's analysis identified critical gaps preventing complete FRED2 functionality. Phase 4 addresses these gaps to achieve 95%+ feature parity.

### Legacy Implementation Status (To Be Refactored)
- ✅ **Basic Framework**: Mission data, 3D viewport, object management 
- ✅ **Property System**: Object property inspector
- 🔄 **Asset System**: Custom implementation → Will be replaced by EPIC-002 integration
- 🔄 **SEXP System**: Basic implementation → Will be replaced by EPIC-004 integration
- 🔄 **File System**: Custom parser → Will be replaced by EPIC-003 integration

## Acceptance Criteria

### Epic-Level Acceptance Criteria
1. **Complete Mission Editing**: Create and edit all types of WCS missions
2. **Asset Integration**: Seamless browsing and integration of all game assets
3. **SEXP Visual Editing**: Comprehensive visual scripting without text editing
4. **Real-time Validation**: Immediate feedback on mission errors and issues
5. **Workflow Efficiency**: Faster mission creation than original FRED2
6. **Godot Integration**: Native feel and behavior within Godot editor

### Quality Gates
- Workflow design review by Mo (Godot Architect)
- Feature parity validation by Larry (WCS Analyst)
- User experience testing by mission creators
- Performance and stability testing by QA
- Final approval by SallySM (Story Manager)

## Dependencies

### Completed Dependencies ✅
- **EPIC-001**: Core Foundation Infrastructure (utilities, math, validation)
- **EPIC-002**: Asset Structures and Management Addon (asset browsing and integration)
- **EPIC-003**: Data Migration & Conversion Tools (mission import/export)
- **EPIC-004**: SEXP Expression System (visual scripting and validation)
- **Godot Editor Plugin System**: Core plugin development framework

### Integration Opportunities
- **Enhanced Asset Management**: Leverage EPIC-002's comprehensive asset system
- **Advanced SEXP Editing**: Use EPIC-004's debugging and validation features
- **Robust File Handling**: Utilize EPIC-003's conversion and validation tools
- **Consistent Infrastructure**: Apply EPIC-001's utilities and patterns

### Downstream Dependencies (Enables)
- **Mission Creation**: Professional mission development workflow
- **Campaign Development**: Campaign creation and testing tools
- **Community Content**: User-generated mission support with full validation
- **Quality Assurance**: Comprehensive mission testing and validation tools

### Integration Benefits
- **Reduced Code Duplication**: Eliminate custom implementations
- **Enhanced Features**: Gain advanced capabilities from integrated systems
- **Improved Quality**: Leverage tested and validated foundation systems
- **Faster Development**: Build on proven infrastructure

## Risks and Mitigation

### Technical Risks
1. **Godot Plugin Limitations**: Editor plugin system may have constraints
   - *Mitigation*: Early prototyping, work within Godot's plugin framework
2. **Performance with Complex Missions**: Large missions may impact editor performance
   - *Mitigation*: Efficient data structures, LOD for preview, background processing
3. **SEXP Integration Complexity**: Visual SEXP editing is inherently complex
   - *Mitigation*: Incremental development, extensive user testing

### Project Risks
1. **Feature Creep**: Tendency to add features beyond original FRED2
   - *Mitigation*: Focus on core functionality first, defer enhancements
2. **User Experience Complexity**: FRED2 is inherently complex
   - *Mitigation*: User-centered design, workflow optimization, modern UX patterns

### User Adoption Risks
1. **Learning Curve**: New interface may confuse existing FRED2 users
   - *Mitigation*: Familiar workflow patterns, comprehensive documentation, tutorials
2. **Compatibility Issues**: Missions created may not work in original WCS
   - *Mitigation*: Strict compatibility mode, validation against WCS standards

## Success Validation

### Functional Validation
- Create representative WCS missions successfully
- Import and edit existing WCS missions without data loss
- Validate SEXP expressions and mission logic correctly
- Export missions compatible with game runtime

### User Experience Validation
- Mission creators can complete tasks faster than original FRED2
- New users can learn mission creation efficiently
- Complex missions can be created and maintained
- Error recovery and debugging is intuitive

### Integration Validation
- Seamless integration with asset management system
- Proper integration with SEXP expression system
- Real-time testing works correctly with game runtime
- Mission files export in correct format for game use

## Timeline Estimate
- **Phase 1**: Core Editor Framework (4 weeks)
- **Phase 2**: Object Editing and Manipulation (3 weeks)
- **Phase 3**: Asset Integration and Browsing (3 weeks)
- **Phase 4**: SEXP and Mission Logic (3 weeks)
- **Phase 5**: Advanced Features and Polish (3-4 weeks)
- **Total**: 12-16 weeks with comprehensive testing and polish

## User Experience Goals

### Modern Editor Experience
- **Familiar Workflow**: Maintain FRED2 concepts while improving usability
- **Contextual Help**: Integrated help and documentation system
- **Customizable Interface**: Dockable panels, customizable layouts
- **Keyboard Shortcuts**: Comprehensive and customizable shortcuts

### Enhanced Productivity
- **Smart Defaults**: Intelligent defaults for common operations
- **Batch Operations**: Efficient multi-object editing capabilities
- **Template System**: Mission templates and common patterns
- **Real-time Feedback**: Immediate validation and error reporting

### Community Features
- **Sharing Support**: Easy mission export and sharing
- **Version Control**: Integration with version control systems
- **Collaboration**: Multi-user editing support (future)
- **Asset Repository**: Community asset sharing (future)

## Related Artifacts
- **WCS FRED2 Analysis**: Complete analysis of original editor functionality
- **Architecture Design**: To be created by Mo
- **Story Definitions**: To be created by SallySM
- **Implementation**: To be handled by Dev
- **Validation**: To be performed by QA

## BMAD Team Refinement Summary (May 30, 2025)

### Collaborative Analysis Completed
**BMAD Team**: Larry (WCS Analyst), Mo (Godot Architect), SallySM (Story Manager)  
**Analysis Date**: May 30, 2025  
**Refinement Scope**: Complete story enhancement based on C++ source analysis, existing Godot code review, and integration requirements

### Key Improvements Made
1. **Story Scope Refinement**: Split oversized GFRED2-006 into 4 focused stories (006A-D)
2. **Performance Requirements**: Added specific benchmarks and optimization criteria
3. **Integration Strategy**: Enhanced integration points with EPICs 001-004
4. **Accessibility Standards**: Added comprehensive accessibility requirements
5. **Migration Planning**: Detailed migration strategies for existing code
6. **Risk Mitigation**: Identified and addressed technical and project risks

### Timeline Accuracy
- **Original Estimate**: 12-16 weeks (unrealistic based on integration complexity)
- **Refined Estimate**: 6 weeks / 30 days (based on detailed story analysis)
- **Implementation Sequence**: Optimized for dependency management and risk reduction

### Quality Standards Enhanced
- Performance benchmarks for all stories
- Comprehensive integration validation requirements
- Accessibility compliance standards
- Migration and compatibility testing requirements

---

**Original Analysis By**: Larry (WCS Analyst) - January 26, 2025  
**Story Refinement By**: BMAD Team (Larry, Mo, SallySM) - May 30, 2025  
**Current Status**: Ready for Implementation  
**Dependencies**: All EPICs 001-004 complete and stable  
**BMAD Workflow Status**: Analysis → Stories → **READY FOR IMPLEMENTATION**

---

## SallySM Story Integration Summary (May 30, 2025)

### Critical Gap Analysis & Story Creation
**Analysis Source**: Larry (WCS Analyst) findings - GFRED2 coverage only 60-65% of FRED2 capabilities  
**Story Manager**: SallySM  
**Integration Date**: May 30, 2025

### New High-Priority Stories Created
1. **GFRED2-007: Briefing Editor System** (5 days) - CRITICAL GAP ⚡
   - Complete absence of briefing creation capabilities
   - Multi-stage briefing, camera positioning, voice integration
   - Essential for mission storytelling and player orientation

2. **GFRED2-008: Campaign Editor Integration** (4 days) - CRITICAL GAP ⚡
   - Complete absence of campaign creation capabilities
   - Mission flow, branching logic, campaign-wide variables
   - Essential for multi-mission campaign development

3. **GFRED2-009: Advanced Ship Configuration** (4 days) - HIGH PRIORITY ⚡
   - Missing sophisticated ship configuration options
   - Advanced AI, damage systems, texture replacement
   - Required for complex mission scenarios

4. **GFRED2-010: Mission Component Editors** (5 days) - HIGH PRIORITY ⚡
   - Missing reinforcements, goals, messages, waypoints editors
   - Environment configuration, variable management
   - Foundation components for sophisticated missions

- **GFRED2-011**: UI Component Refactoring to Scene-Based Architecture (5 days) ⚡ **CRITICAL** 
   - Scene-based UI architecture for all components (gizmos, docks, dialogs)
   - Script attachment to scene nodes instead of programmatic UI construction
   - Scene composition and inheritance for complex UI components
   - Specific code targets: `ui/`, `dialogs/`, `viewport/`, `sexp_editor/`, `validation/` folders
   - Folder structure consolidation and consistent naming conventions
   - **CRITICAL VIOLATIONS TO CORRECT**: `dialog_manager.gd` programmatic UI, hybrid UI approaches
   - Story Created: 2025-05-30 by SallySM (Enhanced with specific code references)
   - **Architecture Enhanced**: 2025-05-30 by Mo (Comprehensive scene-based architecture added)
   - **Stories Refined**: 2025-05-31 by SallySM (7 stories refined for architectural compliance)

### Existing Story Enhancements
- **GFRED2-002**: Added variable management UI and SEXP tools palette
- **GFRED2-001**: Added advanced ship configuration support and 3D previews
- **GFRED2-006A**: Added mission statistics dashboard and validation tools

### Timeline Impact
- **Original Estimate**: 30 days (6 weeks)
- **Updated Estimate**: 48 days (9.6 weeks)
- **Additional Development**: 18 days for critical feature parity
- **Feature Parity**: Achieves 95%+ FRED2 functionality vs previous 60-65%

### Implementation Strategy
- **Phase 1-3**: Existing refined stories (30 days) - Foundation and core features
- **Phase 4**: New critical stories (18 days) - Feature parity and professional capabilities
- **Integration Approach**: Systematic dependency management with quality gates
- **Risk Mitigation**: Clear separation of foundation vs advanced features

### Success Validation
- **Feature Coverage**: 95%+ FRED2 capability parity
- **Professional Workflow**: Complete WCS mission development pipeline
- **Quality Standards**: All BMAD quality gates and performance benchmarks
- **User Experience**: Intuitive for experienced FRED2 users, accessible for new users

**DELIVERABLE ACHIEVED**: Complete set of GFRED2 stories for full FRED2 feature parity with modern Godot implementation.

---

## SallySM Architectural Compliance Review (May 31, 2025)

### Critical Implementation Issue Resolution
**Review Triggered By**: Comprehensive feedback analysis identifying architectural violations in current implementation  
**Story Manager**: SallySM  
**Review Date**: May 31, 2025

### Issues Identified & Resolved
1. **VIOLATION**: Current implementation uses hybrid UI approaches (programmatic + scene-based)
2. **VIOLATION**: No centralized scene structure as mandated by May 30th architecture
3. **VIOLATION**: `dialog_manager.gd` uses programmatic UI construction violating Godot best practices
4. **VIOLATION**: Mixed UI approaches across 5+ folders creating technical debt

### Stories Refined for Architectural Compliance
- **GFRED2-006A**: Enhanced with mandatory scene-based validation components
- **GFRED2-006B**: Refined with centralized scene structure requirements
- **GFRED2-006C**: Updated to eliminate mixed UI approaches
- **GFRED2-006D**: Enhanced with scene-based architecture mandates
- **GFRED2-007**: Refined with briefing editor scene requirements
- **GFRED2-011**: CRITICALLY enhanced with specific violation corrections

### Architectural Requirements Enforced
1. **100% Scene-Based UI**: NO programmatic UI construction allowed
2. **Centralized Structure**: ALL UI in `addons/gfred2/scenes/` exclusively
3. **Performance Standards**: < 16ms scene instantiation, 60+ FPS UI updates
4. **Folder Elimination**: DEPRECATE `ui/`, `dialogs/`, `viewport/ui/` folders
5. **Clear Migration Strategy**: Specific steps to correct architectural violations

### Implementation Impact
- **BEFORE**: Architectural chaos with mixed approaches
- **AFTER**: Definitive scene-based architecture with clear compliance requirements
- **RESULT**: Stories now provide specific guidance to eliminate architectural violations

**CRITICAL SUCCESS FACTOR**: Implementation of GFRED2-011 (UI refactoring) is now **MANDATORY** to resolve architectural violations before proceeding with other stories.

---

**Architectural Compliance Verification**: ✅ **COMPLETE**  
**Stories Refined**: 7 stories updated with architectural requirements  
**Implementation Ready**: ✅ **YES - with mandatory architecture compliance**