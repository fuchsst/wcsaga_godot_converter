# GFRED2 Implementation & Cleanup Plan

**As Dev (GDScript Developer)**

## IMMEDIATE PRIORITIES

### 1. Core Infrastructure Integration (GFRED2-004) - 2 days
**Status**: READY FOR IMPLEMENTATION

#### Task 1.1: Fix Math Operations Integration
- [ ] Replace custom math in `viewport/mission_camera_3d.gd` with core utilities
- [ ] Update `object_management/` math operations 
- [ ] Integrate with core Vector3D and Matrix4x4 utilities

#### Task 1.2: File Operations Migration  
- [ ] Update `mission/` directory file operations to use core VP archive access
- [ ] Replace custom file handling with core abstraction
- [ ] Ensure cross-platform compatibility

#### Task 1.3: Error Handling Standardization
- [ ] Update all dialogs to use core validation patterns
- [ ] Implement standardized error reporting
- [ ] Add consistent validation and recovery patterns

#### Task 1.4: Configuration System Integration
- [ ] Integrate user preferences with core configuration
- [ ] Setup editor settings management
- [ ] Implement keyboard shortcuts system

### 2. SEXP System Integration (GFRED2-002) - 5 days  
**Status**: PARTIALLY IMPLEMENTED - NEEDS COMPLETION

#### Task 2.1: Complete SEXP Manager Integration
- [ ] Fix SexpManager integration in `sexp_editor_dock_controller.gd`
- [ ] Implement missing debug functionality
- [ ] Add real-time validation with proper error reporting

#### Task 2.2: Advanced SEXP Debugging
- [ ] Implement SEXP debugging functionality (TODOs in controller)
- [ ] Add breakpoint management
- [ ] Implement variable watch system

#### Task 2.3: SEXP Function Palette
- [ ] Complete function palette filtering
- [ ] Add function documentation display  
- [ ] Implement drag-and-drop function insertion

### 3. Asset System Integration (GFRED2-001) - 3 days
**Status**: WELL IMPLEMENTED - NEEDS OPTIMIZATION

#### Task 3.1: Asset Preview System
- [ ] Complete `_display_asset_preview()` implementation in asset browser
- [ ] Add 3D model preview for ships
- [ ] Implement texture and audio previews

#### Task 3.2: Asset Performance Optimization
- [ ] Add asset caching system
- [ ] Implement background asset loading
- [ ] Add asset validation and error reporting

## MISSING FEATURES (HIGH PRIORITY)

### 4. Missing Scene Files
**Current gaps identified in scenes/docks/:**

#### Task 4.1: Performance Profiler Dock Scene
- [ ] Create `performance_profiler_dock.tscn` (referenced in plugin.gd but missing)
- [ ] Implement performance monitoring components
- [ ] Add profiling data visualization

#### Task 4.2: Missing Dialog Scenes
- [ ] Create briefing editor dialog scenes (`scenes/dialogs/briefing_editor/`)
- [ ] Create campaign editor dialog scenes (`scenes/dialogs/campaign_editor/`)
- [ ] Create template library dialog scenes (partially implemented)

### 5. Complete Template System (GFRED2-006C)
**Status**: BASIC STRUCTURE EXISTS - NEEDS IMPLEMENTATION

#### Task 5.1: Mission Template System
- [ ] Complete `template_library_manager.gd` implementation
- [ ] Add template validation system
- [ ] Implement template insertion and customization

#### Task 5.2: Pattern Library
- [ ] Complete asset pattern browser functionality
- [ ] Implement SEXP pattern browser
- [ ] Add pattern insertion manager

### 6. Campaign Editor Components (GFRED2-008)
**Status**: BASIC STUBS - NEEDS FULL IMPLEMENTATION

#### Task 6.1: Campaign Editor Dialog
- [ ] Implement `campaign_editor_dialog.gd` functionality
- [ ] Add campaign flow diagram component
- [ ] Implement campaign validation system

#### Task 6.2: Campaign Management
- [ ] Complete `campaign_progression_manager.gd`
- [ ] Add campaign export functionality
- [ ] Implement campaign testing integration

## TESTING REQUIREMENTS

### 7. Add Missing gdUnit4 Tests
**Current test coverage is incomplete**

#### Task 7.1: Integration Tests
- [ ] Create comprehensive SEXP addon integration tests
- [ ] Add WCS Asset Core integration tests  
- [ ] Add core infrastructure integration tests

#### Task 7.2: Performance Tests
- [ ] Add scene instantiation performance tests
- [ ] Add UI responsiveness tests (60 FPS requirement)
- [ ] Add large mission handling tests

#### Task 7.3: UI Component Tests
- [ ] Add dock scene instantiation tests
- [ ] Add dialog functionality tests
- [ ] Add component interaction tests

## CODE CLEANUP TASKS

### 8. Remove Duplicate/Unused Code
**Identified cleanup areas:**

#### Task 8.1: Asset Browser Cleanup
- [ ] Remove any remaining AssetRegistryWrapper remnants
- [ ] Clean up duplicate asset browser dock files
- [ ] Consolidate asset preview functionality

#### Task 8.2: Dialog System Cleanup
- [ ] Ensure all dialogs use scene-based architecture
- [ ] Remove any programmatic UI construction
- [ ] Consolidate dialog management

#### Task 8.3: Performance Code Cleanup
- [ ] Remove duplicate performance monitoring code
- [ ] Consolidate profiling systems
- [ ] Clean up unused performance scripts

## IMPLEMENTATION SEQUENCE

### Week 1: Foundation (Days 1-2)
1. **Day 1**: Core Infrastructure Integration (Tasks 1.1-1.4)
2. **Day 2**: SEXP System Integration (Tasks 2.1-2.3)

### Week 1: Asset System (Days 3-5)  
3. **Day 3**: Asset System Integration (Tasks 3.1-3.2)
4. **Day 4**: Missing Scene Files (Tasks 4.1-4.2)
5. **Day 5**: Template System (Tasks 5.1-5.2)

### Week 2: Advanced Features (Days 6-10)
6. **Day 6-7**: Campaign Editor Components (Tasks 6.1-6.2)
7. **Day 8-9**: Testing Implementation (Tasks 7.1-7.3)
8. **Day 10**: Code Cleanup (Tasks 8.1-8.3)

## SUCCESS CRITERIA

### Quality Gates
- [ ] All gdUnit4 tests pass
- [ ] Scene instantiation < 16ms
- [ ] UI updates maintain 60+ FPS
- [ ] No programmatic UI construction
- [ ] Complete WCS Asset Core integration
- [ ] Full SEXP addon integration
- [ ] Zero duplicate utility code

### Functional Requirements
- [ ] Mission loading/saving works
- [ ] Asset browsing and preview works
- [ ] SEXP editing with validation works
- [ ] Object placement and manipulation works
- [ ] Real-time validation works
- [ ] Performance profiling works

### Integration Requirements  
- [ ] Direct WCS Asset Core integration
- [ ] Direct SEXP addon integration
- [ ] Core infrastructure integration
- [ ] Cross-platform compatibility

---

**Next Action**: Begin Task 1.1 - Fix Math Operations Integration