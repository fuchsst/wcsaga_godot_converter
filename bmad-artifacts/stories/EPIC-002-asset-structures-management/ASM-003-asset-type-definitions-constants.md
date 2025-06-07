# User Story: Asset Type Definitions and Constants

**Epic**: EPIC-002 - Asset Structures and Management Addon  
**Story ID**: ASM-003  
**Created**: January 29, 2025  
**Status**: Ready

## Story Definition
**As a**: Developer working with various WCS asset types  
**I want**: Centralized asset type definitions and shared constants for the asset management system  
**So that**: Asset types are consistently identified throughout the system and standardized paths and values are used across all components

## Acceptance Criteria
- [ ] **AC1**: `AssetTypes` enum class created with all WCS asset categories (SHIP, WEAPON, ARMOR, MODEL, TEXTURE, MISSION, etc.)
- [ ] **AC2**: `FolderPaths` constant class providing standardized directory paths for each asset type
- [ ] **AC3**: Asset type validation functions implemented to check type compatibility and conversions
- [ ] **AC4**: File extension mappings defined for each asset type (`.tres`, `.tscn`, `.gltf`, etc.)
- [ ] **AC5**: Asset naming conventions and validation patterns established
- [ ] **AC6**: Type registration system supporting custom asset types for extensibility

## Technical Requirements
- **Architecture Reference**: [Constants & Utilities](../../docs/EPIC-002-asset-structures-management-addon/architecture.md#constants--utilities)
- **Godot Components**: Enum classes, constant definitions, static utility functions
- **Integration Points**: Used by AssetLoader, RegistryManager, ValidationManager, and all asset structures

## Implementation Notes
- **WCS Reference**: Based on WCS asset organization and file structure patterns
- **Godot Approach**: Use Godot's class_name system with static methods for type-safe operations
- **Key Challenges**: Supporting both built-in and custom asset types while maintaining type safety
- **Success Metrics**: Consistent asset type identification across all components, no magic strings for types

## Dependencies
- **Prerequisites**: ASM-001 (Plugin Framework) and ASM-002 (Base Asset Data) completed
- **Blockers**: None
- **Related Stories**: All asset management stories depend on these definitions

## Definition of Done
- [ ] All acceptance criteria met and verified through testing
- [ ] Code follows GDScript standards (static typing, documentation)
- [ ] All asset types properly categorized and defined
- [ ] Path utilities provide consistent asset organization
- [ ] Type validation prevents invalid operations
- [ ] Extension system allows for custom asset types
- [ ] Documentation includes examples for adding new types

## Estimation
- **Complexity**: Simple
- **Effort**: 1 day
- **Risk Level**: Low
- **Confidence**: High

## Implementation Tasks
- [ ] **Task 1**: Create `AssetTypes` enum class in `constants/asset_types.gd`
- [ ] **Task 2**: Define all WCS asset categories with proper categorization
- [ ] **Task 3**: Implement `FolderPaths` class in `constants/folder_paths.gd`
- [ ] **Task 4**: Create asset type validation and conversion utilities
- [ ] **Task 5**: Define file extension mappings for each asset type
- [ ] **Task 6**: Implement custom type registration system
- [ ] **Task 7**: Add comprehensive documentation and usage examples

## Testing Strategy
- **Unit Tests**: Asset type validation, path generation, type conversions
- **Integration Tests**: Usage by other asset management components
- **Manual Tests**: Verify consistent paths and types across the system

## Notes and Comments
**FOUNDATIONAL CONSTANTS**: This story establishes the type system and organization structure that all other asset components will rely on. Must be comprehensive and extensible.

**EXTENSIBILITY FOCUS**: The type system should support both WCS built-in types and future custom asset types for modding and expansion.

---

## Approval Checklist
- [x] Story follows template structure completely
- [x] All acceptance criteria are specific and testable
- [x] Technical requirements reference approved architecture
- [x] Dependencies are identified and documented
- [x] Story size is appropriate (1 day maximum)
- [x] Definition of Done is complete and realistic
- [x] Constants and types provide system-wide consistency
- [x] Story enables all other asset management functionality

**Approved by**: SallySM (Story Manager) **Date**: January 29, 2025  
**Role**: Story Manager

---

## Implementation Tracking
**Started**: [Date]  
**Developer**: [Name]  
**Completed**: [Date]  
**Reviewed by**: [Name]  
**Final Approval**: [Date and approver]