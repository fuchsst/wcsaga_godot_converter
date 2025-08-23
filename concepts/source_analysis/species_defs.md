# Species Definitions System Analysis

## Purpose
The species definitions system handles the configuration and properties of different alien species, including their visual styles, behaviors, and faction relationships.

## Main Public Interfaces
- `species_info` - Structure defining species properties
- `species_info_lookup()` - Find species by name
- `species_init()` - Initialize species system
- Species property access functions

## Key Components
- **Species Properties**: Visual, behavioral, and gameplay characteristics
- **Faction Relationships**: Alliance and enemy configurations
- **Thruster Effects**: Species-specific engine visuals
- **Debris Behavior**: Species-specific destruction patterns
- **Animation Settings**: Species-specific movement and effects

## Dependencies
- `ship.h` - Ship species assignments
- `model.h` - Species-specific visual elements
- `weapon.h` - Species-specific weapons
- `iff_defs.h` - Identification, Friend or Foe relationships

## Game Logic Integration
The species system enables faction-based gameplay:
- Defines distinct alien civilizations with unique characteristics
- Supports story and narrative through visual distinction
- Integrates with IFF system for targeting and diplomacy
- Provides gameplay variety through species-specific properties
- Enables modding through configurable species definitions