# Story ID: DM-016 - Deprecate Runtime VP Archive Loading

- **Epic**: [EPIC-003: Data Migration & Conversion Tools](../../../epics/EPIC-003-data-migration-conversion-tools.md)
- **Story Owner**: Mo (Godot Architect)
- **Developer**: Dev
- **QA**: QA
- **Story Point Estimate**: 5
- **Priority**: High
- **Status**: Ready for Implementation
- **Created**: 2025-06-10
- **Updated**: 2025-06-10

## User Story

As a developer, I want to remove the runtime dependency on legacy VP archive files so that the final game is fully Godot-native, loads faster, and has a simplified asset management pipeline.

## Description

The project currently includes a `VPResourceManager` autoload that allows the game engine to load assets directly from original WCS `.vp` files at runtime. While this is a useful transitional tool during development, it represents significant technical debt and goes against the "Godot-Native" architectural principle.

The core logic for reading VP files is essential for the `wcs_converter` addon (EPIC-003) to perform its function. This story involves refactoring the codebase to remove the *runtime* loading capability while ensuring the *conversion-time* capability is preserved and isolated within the converter tools. This is a critical step to finalize the asset pipeline and ensure the game is not dependent on legacy formats.

## Acceptance Criteria

1.  **Autoload Removed**: The `VPResourceManager` is removed from the project's autoload singletons in `project.godot`.
2.  **Runtime Code Removed**: All code related to loading assets from VP archives *at runtime* is removed from the main game scripts.
3.  **Conversion Tools Preserved**: The `wcs_converter` addon and any related tools retain the ability to read, parse, and extract data from `.vp` files for conversion purposes.
4.  **Code Relocation**: Any shared VP reading logic (e.g., from `scripts/core/archives/`) is moved to a location that is only included or depended upon by the conversion tools, such as `addons/wcs_converter/utils/`. It should not be part of the core runtime engine scripts.
5.  **No Runtime VP Access**: The game no longer attempts to access or load any `.vp` files during startup or gameplay. All assets must be loaded from Godot-native formats (`.tres`, `.tscn`, `.gltf`, etc.).
6.  **Full Game Functionality**: The game must be fully playable using only converted assets. This implies that 100% of necessary game assets have been successfully converted.
7.  **Tests Pass**: All unit and integration tests pass, especially those related to asset loading and scene initialization.

## Technical Implementation Notes

-   This story is dependent on the successful completion of all other asset conversion stories in EPIC-003. It should be one of the final stories tackled in this epic.
-   The `VPResourceManager.gd` script should be deleted or moved into the `addons/wcs_converter/` directory if it contains logic useful for the tools.
-   A global search for `VPResourceManager` and `cf_find_file_location` (or similar legacy file functions) will be needed to find and remove all runtime call sites.
-   The `project.godot` file must be edited to remove the autoload entry.
-   This change simplifies the overall engine architecture, making `FileSystemManager` and Godot's `ResourceLoader` the sole authorities for asset loading.

## Dependencies

-   **DM-001 to DM-015**: This story cannot be completed until all required WCS assets (models, missions, tables, textures, sounds) have been successfully converted to Godot-native formats.

## Risks

-   **Incomplete Asset Conversion**: If any critical asset was missed during the conversion process, removing the runtime VP loader will cause the game to break.
    -   **Mitigation**: A comprehensive audit of all loaded assets must be performed before starting this story. A script that logs all asset paths loaded during a full gameplay session could be used to generate a manifest for comparison against converted assets.

## Quality Assurance Checklist

-   [ ] **Code Review**: All changes reviewed by Mo to confirm the complete removal of runtime VP dependency.
-   [ ] **Full Playthrough**: QA performs a full playthrough of several missions and campaign segments to ensure no assets are missing.
-   [ ] **Startup Test**: Game startup time is measured and should be slightly faster.
-   [ ] **File Access Logs**: Monitor file access during gameplay to confirm no `.vp` files are being accessed.
-   [ ] **Converter Validation**: QA confirms that the `wcs_converter` addon still functions correctly after the refactor.
