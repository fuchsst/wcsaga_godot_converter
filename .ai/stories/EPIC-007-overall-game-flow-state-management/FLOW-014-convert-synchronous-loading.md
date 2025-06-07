# STORY-FLOW-014: Convert Synchronous Loading to Asynchronous in Game Flow Systems

## Story Overview
**Story ID**: FLOW-014
**Epic**: EPIC-007: Overall Game Flow & State Management
**User Story**: As a developer, I want to convert all synchronous resource loading operations within the game flow and state management systems to asynchronous methods, so that the game avoids freezes and stutters during transitions and asset loading, providing a smooth user experience.
**Priority**: Critical
**Estimate**: 4-6 days
**Status**: READY
**Created**: 2025-06-07
**Updated**: 2025-06-07
**Depends On**: Stable EPIC-001, FLOW-013 (as lifecycle issues can complicate async logic).
**Blocks**: Achieving smooth game performance during state transitions.

## Acceptance Criteria
1.  All instances of `load()` or `preload()` for non-trivial assets (scenes, large textures, models, audio resources) within EPIC-007 scripts are replaced with asynchronous loading mechanisms.
2.  Scene transitions managed by the game's state machine utilize asynchronous scene loading.
3.  Appropriate loading indicators (e.g., loading screens, progress bars) are displayed during asynchronous loading periods if the load time is potentially noticeable.
4.  The game remains responsive (e.g., UI animations on a loading screen continue smoothly) while assets are being loaded in the background.
5.  Error handling for failed asynchronous loads is implemented (e.g., log error, show error message, attempt fallback).
6.  Performance testing confirms the absence of game freezes or stutters previously caused by synchronous loading during state transitions.

## Technical Requirements
1.  Identify all synchronous `load()` and `preload()` calls in scripts related to EPIC-007.
2.  Refactor these calls to use `ResourceLoader.load_threaded_request()`, `ResourceLoader.load_threaded_get()`, and associated signals or `await`.
3.  Implement or integrate with a loading screen system that can be activated during async loads.
4.  Ensure that game logic correctly waits for resources to be fully loaded before attempting to use them.
5.  Evaluate and potentially refactor the core `GameStateManager` to use a LimboAI State Machine or Behavior Tree for managing game states, as per architectural direction.

## Implementation Details
-   Focus on scripts like `GameStateManager.gd`, `StateTransitionManager.gd`, and any scripts responsible for loading scenes or major assets for different game states.
-   **State Machine Integration**: If `GameStateManager` is refactored to use LimboAI, the asynchronous loading logic will be implemented as custom LimboAI `BTAction` nodes. For example, a `BTActionLoadSceneAsync` node would be created.
-   For scene loading, the `SceneTree.change_scene_to_packed()` method can be combined with asynchronous loading of the `PackedScene` resource itself.
-   Loading screens can be implemented as separate scenes or UI elements within a persistent `CanvasLayer`.
-   Use `await resource_loader.load_threaded_get_status(path) == ResourceLoader.THREAD_LOAD_LOADED` or connect to `ResourceLoader.load_threaded_completed` signal.

## Test Cases
1.  **TC-FLOW014-01**: Trigger transitions between all major game states. Verify no game freezes occur.
2.  **TC-FLOW014-02**: If loading screens are implemented, verify they display correctly and the game remains responsive during the loading process.
3.  **TC-FLOW014-03**: Simulate a slow loading scenario (e.g., by adding a delay or loading a very large placeholder asset). Verify loading indicators work and the game doesn't appear frozen.
4.  **TC-FLOW014-04**: Test error handling by attempting to load a non-existent resource asynchronously. Verify graceful failure.
5.  **TC-FLOW014-05**: Profile the game during scene transitions to confirm the main thread is not blocked by loading operations.

## WCS Reference
-   Smoothness of transitions in the original WCS, aiming to match or exceed this with modern hardware capabilities.

## Godot Implementation Approach
-   **State Machine**: Evaluate using a LimboAI `BTStateMachine` to manage the main game flow states (e.g., `MAIN_MENU`, `IN_MISSION`). This would replace or wrap the existing logic in `GameStateManager`.
-   **Asynchronous Loading**: Utilize `ResourceLoader` for asynchronous loading. Create custom `BTAction` nodes in LimboAI to handle these operations (e.g., `LoadResource`, `ChangeScene`, `WaitForLoad`). These actions will return `RUNNING` while loading, and `SUCCESS` or `FAILURE` upon completion.
-   **Loading UI**: Implement loading screens as `Control` nodes, possibly in an autoloaded scene or a `CanvasLayer`, controlled by the state machine.
-   **Resource Handling**: Ensure any scripts interacting with asynchronously loaded resources check for load completion before use, potentially by checking a Blackboard variable set by the loading action.

## Definition of Done
-   All identified synchronous loading points in EPIC-007 refactored to asynchronous.
-   The game state machine's implementation (either custom or LimboAI) is confirmed and drives the async loading.
-   Loading indicators implemented where necessary.
-   Robust error handling for async loads in place.
-   All acceptance criteria met.
-   Performance validated to ensure no loading-related hitches.
-   Story validated by QA.

## Notes
-   This story directly addresses a critical issue identified in the QA review of EPIC-007. It's crucial for user experience.
-   The decision to use LimboAI for the game flow state machine should be confirmed and implemented as part of this story or a prerequisite story, as it directly impacts how asynchronous loading is triggered and managed.
