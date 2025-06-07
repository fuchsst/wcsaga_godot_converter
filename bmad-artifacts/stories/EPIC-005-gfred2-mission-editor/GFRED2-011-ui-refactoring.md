# User Story: GFRED2 UI Component Refactoring to Scene-Based Architecture

**Epic**: EPIC-005 - GFRED2 Mission Editor  
**Story ID**: GFRED2-011  
**Created**: 2025-05-30  
**Status**: Completed

## Story Definition
**As a**: Godot developer working with the GFRED2 mission editor  
**I want**: UI components to be defined as reusable Godot scenes (.tscn) with properly attached scripts  
**So that**: The editor UI is more maintainable, follows Godot best practices, and enables visual design workflows

## Acceptance Criteria
- [x] **AC1**: All gizmo components are converted from code-generated UI to scene-based UI (.tscn files)
- [x] **AC2**: All dock UI components are refactored to use scene composition instead of programmatic UI creation
- [x] **AC3**: All dialog components are converted to scene-based architecture with proper script attachment
- [x] **AC4**: Complex UI components in `ui/`, `dialogs/`, `viewport/`, `sexp_editor/`, and `validation/` folders are composed using scene hierarchies rather than code construction
- [x] **AC5**: All scripts are properly attached to scene nodes rather than building UI elements programmatically
- [x] **AC6**: Visual design workflow is enabled through Godot's scene editor for all UI components
- [x] **AC7**: UI component reusability is improved through scene instancing and inheritance
- [x] **AC8**: Performance is maintained or improved through scene-based UI architecture
- [x] **AC9**: Folder structure is consolidated and consistent across `ui/`, `dialogs/`, `viewport/`, `sexp_editor/`, and `validation/` directories
- [x] **AC10**: Clear naming conventions established for scene files (.tscn) vs logic scripts (.gd)

## Technical Requirements
- **Architecture Reference**: `bmad-artifacts/docs/epic-005-gfred2-mission-editor/architecture.md` Section 3 (Editor UI Architecture) **ENHANCED 2025-05-30**
- **MANDATORY ARCHITECTURE COMPLIANCE**: Implement 100% scene-based UI as specified in May 30th architecture
- **Centralized Scene Structure**: ALL UI components MUST be organized under `addons/gfred2/scenes/` only
- **Folder Elimination**: DEPRECATE and consolidate `ui/`, `dialogs/`, `viewport/ui/`, `sexp_editor/` (UI parts), `validation/` (UI parts)
- **Godot Components**: 
  - Scene files (.tscn) for ALL UI components (NO programmatic UI allowed)
  - Scripts attached ONLY to scene root nodes as controllers
  - UI composition through scene hierarchies and inheritance
  - Scene instancing for reusable components with base scene patterns
- **Performance Requirements**:
  - Scene instantiation: < 16ms per component (MANDATORY)
  - Maximum 3 levels of scene inheritance
  - Direct signal connections only (no call_group())
  - Batched UI updates at 60 FPS
- **Integration Points**: 
  - GFRED2 plugin system integration with scene-based registration
  - Editor dock registration using scene instances
  - Gizmo plugin architecture with scene-based components
  - Signal-based communication between scene components

## Implementation Notes
- **CRITICAL VIOLATIONS TO CORRECT**:
  - `dialog_manager.gd`: Uses `preload().new()` for UI instantiation (VIOLATION of scene-based architecture)
  - Mixed `.tscn` and programmatic approaches across folders (ARCHITECTURAL INCONSISTENCY)
  - No centralized scene structure (VIOLATION of May 30th architecture)
  - Hybrid UI approaches causing technical debt (MAINTENANCE NIGHTMARE)
- **Existing Code to Change**: 
  - `target/addons/gfred2/ui/` - ELIMINATE: All dock and panel components using programmatic UI creation
  - `target/addons/gfred2/dialogs/` - ELIMINATE: Dialog classes building UI through code
  - `target/addons/gfred2/viewport/ui/` - ELIMINATE: 3D viewport gizmos and tools with code-based UI
  - `target/addons/gfred2/sexp_editor/` - ELIMINATE: SEXP visual editor components with programmatic UI
  - `target/addons/gfred2/validation/` - ELIMINATE: Validation UI components built programmatically
  - `target/addons/gfred2/plugin.gd` - REFACTOR: Main plugin to use scene-based registration
- **MANDATORY FOLDER RESTRUCTURE**: 
  - CREATE: Centralized `addons/gfred2/scenes/` with sub-folders (docks/, dialogs/, components/, overlays/)
  - DEPRECATE: Top-level `ui/`, `dialogs/`, `viewport/ui/` folders
  - CONSOLIDATE: All UI components into centralized scene structure
  - ESTABLISH: Consistent naming convention (.tscn for UI, .gd for logic only)
  - ENFORCE: Clear separation between UI scenes (.tscn) and business logic scripts (.gd)
- **Godot Approach**: 
  - Convert all UI classes to scene-based architecture with attached scripts
  - Use Godot's scene system for UI composition and inheritance
  - Attach scripts to scene root nodes instead of building UI programmatically
  - Leverage scene inheritance for UI component hierarchies
  - Use UI signals for component communication
- **Key Challenges**: 
  - Migrating existing programmatic UI without breaking functionality
  - Maintaining proper signal connections between components
  - Ensuring compatibility with existing GFRED2 systems
  - Consolidating overlapping UI approaches across different folders
- **Success Metrics**: 
  - All UI components accessible through scene editor
  - Reduced code complexity in UI-related scripts
  - Improved designer workflow and component reusability
  - Consistent UI architecture across all GFRED2 components

## Dependencies
- **Prerequisites**: 
  - GFRED2-001 (Asset System Integration) - **COMPLETED**
  - GFRED2-002 (SEXP System Integration) - **COMPLETED**
  - GFRED2-003 (Mission File Conversion Integration) - **COMPLETED**
  - GFRED2-004 (Core Infrastructure Integration) - **COMPLETED**
  - GFRED2-005 (UI Modernization and Polish) - **COMPLETED**
- **Blockers**: None identified
- **Related Stories**: 
  - GFRED2-006A (Real-time Validation) - Enhanced UI integration needed
  - GFRED2-007 (Briefing Editor System) - Will benefit from scene-based architecture
  - GFRED2-008 (Campaign Editor Integration) - Will use refactored UI patterns

## Definition of Done
- [x] All acceptance criteria met and verified through testing
- [x] Code follows GDScript standards (static typing, documentation)
- [x] Unit tests written and passing for UI component functionality
- [x] Integration testing completed successfully with existing GFRED2 systems
- [x] Code reviewed and approved by team
- [x] Documentation updated (scene structure, UI component guide, integration notes)
- [x] Feature validated against original UI functionality with improved maintainability
- [x] Performance benchmarks verify no regression in UI responsiveness

## Estimation
- **Complexity**: Medium
- **Effort**: 5 days (as defined in epic)
- **Risk Level**: Medium
- **Confidence**: High

## Implementation Tasks
Break down the story into specific implementation tasks:
- [x] **Task 1**: Audit existing GFRED2 folders (`ui/`, `dialogs/`, `viewport/`, `sexp_editor/`, `validation/`) and catalog programmatic UI usage
- [x] **Task 2**: Review and consolidate folder structure to establish consistent UI architecture approach
- [x] **Task 3**: Create scene files (.tscn) for viewport gizmo components in `addons/gfred2/viewport/`
- [x] **Task 4**: Convert dock UI components in `addons/gfred2/ui/` from programmatic to scene-based architecture
- [x] **Task 5**: Refactor dialog components in `addons/gfred2/dialogs/` to use scene composition and inheritance
- [x] **Task 6**: Refactor SEXP editor components in `addons/gfred2/sexp_editor/` to scene-based architecture
- [x] **Task 7**: Update validation UI components in `addons/gfred2/validation/` to scene-based architecture
- [x] **Task 8**: Migrate all UI scripts from programmatic construction to scene attachment patterns
- [x] **Task 9**: Implement scene instancing for reusable UI components across all folders
- [x] **Task 10**: Update `addons/gfred2/plugin.gd` to work with scene-based UI registration
- [x] **Task 11**: Establish consistent naming conventions and folder organization for scenes vs scripts
- [x] **Task 12**: Test and validate all UI functionality after refactoring
- [x] **Task 13**: Create documentation for consistent scene-based UI component development approach

## Testing Strategy
- **Unit Tests**: 
  - UI component initialization and setup tests
  - Scene loading and instancing functionality tests
  - Script attachment and signal connection validation tests
- **Integration Tests**: 
  - GFRED2 plugin system integration with scene-based UI
  - Dock registration and lifecycle management tests
  - Cross-component communication and signal propagation tests
- **Manual Tests**: 
  - Visual design workflow verification through Godot scene editor
  - UI responsiveness and performance validation
  - Component reusability and inheritance testing

## Notes and Comments
This story focuses on improving the maintainability and design workflow of GFRED2 UI components by migrating from programmatic UI construction to Godot's scene-based architecture. This refactoring will enable visual UI design, improve component reusability, and follow Godot best practices for UI development.

**Critical Focus Areas**:
- **Existing Code Audit**: Comprehensive review of `addons/gfred2/ui/`, `addons/gfred2/dialogs/`, `addons/gfred2/viewport/`, `addons/gfred2/sexp_editor/`, and `addons/gfred2/validation/` folders
- **Architecture Consolidation**: Eliminate inconsistent UI approaches and establish unified scene-based patterns
- **Incremental Migration**: Refactor folder by folder to ensure no loss of functionality
- **Proper Testing**: Validate each component migration before proceeding to the next

The refactoring should be done incrementally to ensure no loss of functionality, with proper testing at each step to validate the migration. Special attention should be paid to consolidating the different UI approaches currently used across the various folders.

**ARCHITECTURAL GUIDANCE**: Implementing developer must follow the enhanced architecture in Section 3 of the architecture document, which provides:
- Mandatory scene-based UI patterns  
- Centralized scene structure (`addons/gfred2/scenes/`)
- Performance requirements (< 16ms scene instantiation)
- Signal architecture patterns
- Scene inheritance strategies

---

## Approval Checklist
- [x] Story follows template structure completely
- [x] All acceptance criteria are specific and testable
- [x] Technical requirements reference approved architecture
- [x] Dependencies are identified and documented
- [x] Story size is appropriate (5 days as specified in epic)
- [x] Definition of Done is complete and realistic
- [x] WCS reference material is clearly identified (existing GFRED2 code)
- [x] Godot implementation approach is well-defined (scene-based architecture)

**Approved by**: SallySM (Story Manager) **Date**: 2025-05-30  
**Role**: Story Manager (SallySM)

---

## Implementation Tracking
**Started**: 2025-05-31  
**Developer**: Dev (GDScript Developer)  
**Completed**: 2025-05-31  
**Reviewed by**: SallySM (Story Manager)  
**Final Approval**: SallySM (Story Manager) - 2025-05-31

## Completion Summary
**Completion Date**: 2025-05-31  
**Final Review**: Comprehensive cleanup completed including:
1. ✅ Removed duplicate AssetRegistryWrapper code (325 lines eliminated)
2. ✅ Removed old programmatic dialog_manager.gd violating scene-based architecture
3. ✅ Removed duplicate asset browser dock files
4. ✅ Renamed "scene_based" scripts to remove unnecessary suffix
5. ✅ Updated asset preview panel to use WCS Asset Core directly
6. ✅ Verified all code uses proper WCS Asset Core integration
7. ✅ All 13 implementation tasks completed successfully
8. ✅ Architecture violations corrected and compliance verified
9. ✅ Scene-based UI architecture fully implemented
10. ✅ Folder structure consolidated and naming conventions established

**Architectural Compliance**: ✅ **VERIFIED** - 100% scene-based UI implementation achieved  
**Performance**: ✅ **VALIDATED** - UI responsiveness maintained with improved maintainability  
**Integration**: ✅ **TESTED** - All GFRED2 systems working correctly with new architecture