# Mission System Analysis

## Purpose
The mission system handles all mission-related data, parsing, loading, and execution. It manages mission objectives, events, ships, wings, and the overall mission flow from briefing to debriefing.

## Main Public Interfaces
- `mission` - Structure containing overall mission properties
- `p_object` - Parse object representing ships/wings before creation
- `parse_main()` - Main mission parsing function
- `mission_parse_get_parse_object()` - Gets parse object by name/signature
- `parse_create_object()` - Creates game object from parse object
- `mission_parse_eval_stuff()` - Evaluates mission events and directives
- `get_mission_info()` - Gets basic mission information without loading

## Key Components
- **Mission Parsing**: Reads .fs2 files and creates game entities
- **Parse Objects**: Intermediate representation of ships/wings before instantiation
- **Mission Events**: Scripted events and triggers based on sexp conditions
- **Wing Management**: Grouped ships with coordinated behavior
- **Mission Goals**: Primary, secondary, and bonus objectives
- **Reinforcements**: Dynamic ship arrival system
- **Support Ships**: Repair/rearm functionality
- **Mission Flow**: State management from briefing to debriefing

## Dependencies
- `object.h` - Missions create and manage game objects
- `ship.h` - Missions define ship properties and behaviors
- `weapon.h` - Missions specify weapon loadouts
- `ai.h` - Missions set AI directives and goals
- `gamesequence.h` - Missions integrate with game state management

## Game Logic Integration
The mission system orchestrates the entire gameplay experience:
- Loads and parses mission files (.fs2)
- Manages mission objectives and success/failure conditions
- Controls story progression and campaign flow
- Handles player progression and scoring
- Integrates with AI for mission-specific behaviors
- Manages multiplayer mission synchronization
- Controls briefing/debriefing UI flow