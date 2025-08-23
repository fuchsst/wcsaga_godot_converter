# AI System Analysis

## Purpose
The AI system in FreeSpace/Kazan handles all non-player ship behavior, including combat tactics, navigation, movement, and decision-making. It provides different behavioral models for various ship types and handles both individual ship AI and coordinated wing tactics.

## Main Public Interfaces
- `ai_info` - Main AI state structure containing all AI-related data for a ship
- `ai_process()` - Main AI processing function called each frame
- `ai_attack_object()` - Sets a ship to attack another object
- `ai_evade_object()` - Sets a ship to evade another object
- `ai_ignore_object()` - Makes a ship ignore another object
- `ai_dock_with_object()` - Handles docking behavior between ships
- `ai_start_waypoints()` - Initiates waypoint following
- `ai_warp_out()` - Initiates warp out sequence
- `ai_chase()` - Chase behavior implementation
- `ai_evade()` - Evasion behavior implementation
- `ai_big_ship()` - Specialized AI for capital ships

## Key Components
- **Behavior Management**: AIM_* constants define different AI modes (chase, evade, guard, etc.)
- **Goal System**: AI goals with priorities and dynamic goal assignment
- **Pathfinding**: Global and local path following with waypoint management
- **Combat Tactics**: Subsystem targeting, weapon selection, and tactical positioning
- **Formation Flying**: Wing-based formation movement and coordinated attacks
- **Strafing**: Specialized attack patterns for capital ships
- **Docking**: Complex docking procedures for support and cargo operations

## Dependencies
- `object.h` - For object management and references
- `ship.h` - For ship-specific data and subsystems
- `weapon.h` - For weapon handling and firing decisions
- `physics.h` - For movement and physics calculations
- `model.h` - For model subsystem access and path information
- `mission.h` - For mission-specific AI directives

## Game Logic Integration
The AI system is central to FreeSpace's gameplay, handling:
- Enemy ship behavior in combat
- Friendly ship wing tactics
- Capital ship strategic movements
- Support ship operations (repair/rearm)
- Mission objective fulfillment through AI goals
- Dynamic difficulty scaling through AI profiles