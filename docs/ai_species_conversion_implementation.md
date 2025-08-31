# AI Profiles, AI Behaviors, and Species Conversion Implementation

## Overview

This document describes the implementation of the conversion system for AI profiles, AI behaviors, and species definitions from Wing Commander Saga TBL files to Godot-compatible resource files. The implementation includes:

1. Data structures for AI profiles and AI behaviors
2. Resource generators for AI profiles, AI behaviors, and species
3. Comprehensive test suites for all components
4. Integration tests for end-to-end conversion workflows

## Components Implemented

### 1. Data Structures

Added new data structures to `data_converter/core/table_data_structures.py`:

- **AIProfileData**: Represents AI profile definitions with difficulty scaling parameters
- **AIBehaviorData**: Represents AI behavior definitions with combat parameters

### 2. Resource Generators

Created three new resource generators in `data_converter/resource_generators/`:

- **ai_profile_resource_generator.py**: Generates `.tres` files for AI profiles in `/assets/data/ai/profiles/`
- **ai_behavior_resource_generator.py**: Generates `.tres` files for AI behaviors in `/assets/data/ai/`
- **species_resource_generator.py**: Generates `.tres` files for species definitions in `/assets/data/species/`

### 3. Test Suites

Created comprehensive test suites:

- **Unit tests**: Individual component tests for each resource generator
- **Integration tests**: End-to-end conversion workflow tests

### 4. Integration Tests

Created integration tests that verify the complete conversion workflow:

- **test_ai_profile_integration.py**: Tests AI profile conversion from `ai_profiles.tbl` to Godot resources
- **test_ai_behavior_integration.py**: Tests AI behavior conversion from `ai.tbl` to Godot resources
- **test_species_integration.py**: Tests species definition conversion from `Species_defs.tbl` to Godot resources

## File Structure

```
data_converter/
├── core/
│   └── table_data_structures.py          # Added AIProfileData and AIBehaviorData
├── resource_generators/
│   ├── ai_profile_resource_generator.py   # New AI profile resource generator
│   ├── ai_behavior_resource_generator.py  # New AI behavior resource generator
│   └── species_resource_generator.py      # New species resource generator
└── tests/
    ├── resource_generators/
    │   ├── test_ai_profile_resource_generator.py
    │   ├── test_ai_behavior_resource_generator.py
    │   └── test_species_resource_generator.py
    └── integration/
        ├── test_ai_profile_integration.py
        ├── test_ai_behavior_integration.py
        └── test_species_integration.py
```

## Target Godot Structure

The generated resources follow the target Godot project structure:

```
assets/
├── data/
│   ├── ai/
│   │   ├── profiles/                      # AI profile resources
│   │   │   ├── saga_retail.tres
│   │   │   ├── test_profile.tres
│   │   │   └── ai_profile_registry.tres
│   │   ├── coward_behavior.tres           # AI behavior resources
│   │   ├── aggressive_behavior.tres
│   │   └── ai_behavior_registry.tres
│   └── species/                           # Species resources
│       ├── terran.tres
│       ├── kilrathi.tres
│       ├── vasudan.tres
│       └── species_registry.tres
```

## Usage

### Running Unit Tests

```bash
# Run all new resource generator tests
uv run python -m pytest data_converter/tests/resource_generators/test_ai_profile_resource_generator.py data_converter/tests/resource_generators/test_ai_behavior_resource_generator.py data_converter/tests/resource_generators/test_species_resource_generator.py -v

# Run individual test suites
uv run python -m pytest data_converter/tests/resource_generators/test_ai_profile_resource_generator.py -v
uv run python -m pytest data_converter/tests/resource_generators/test_ai_behavior_resource_generator.py -v
uv run python -m pytest data_converter/tests/resource_generators/test_species_resource_generator.py -v
```

### Running Integration Tests

```bash
# Run integration tests
uv run python data_converter/tests/integration/test_ai_profile_integration.py
uv run python data_converter/tests/integration/test_ai_behavior_integration.py
uv run python data_converter/tests/integration/test_species_integration.py
```

### Conversion Workflow

The conversion workflow follows these steps:

1. **Parsing**: TBL files are parsed by the appropriate table converters
2. **Validation**: Parsed data is validated for correctness
3. **Conversion**: Valid data is converted to Godot resource format
4. **Generation**: Resource generators create `.tres` files in the appropriate directory structure
5. **Registry Creation**: Registry files are generated to reference all resources

## Key Features

### AI Profiles
- Support for 5 difficulty levels (Very Easy, Easy, Medium, Hard, Insane)
- Difficulty scaling for weapon delays, shield management, and other parameters
- Boolean flags for countermeasures, missile evasion, and targeting behavior

### AI Behaviors
- Support for 5 skill levels (Trainee, Rookie, Hotshot, Ace, Insane)
- Combat behavior parameters (accuracy, evasion, courage, patience)
- Additional behavior parameters (afterburner use, shockwave evasion, etc.)

### Species Definitions
- Basic species properties (name, default IFF, default armor)
- AI behavior characteristics (aggression, caution, accuracy)
- Visual properties (debris textures, shield hit animations, thrust animations)

## Validation

All components include comprehensive validation:

- **Data validation**: Ensures required fields are present and correctly formatted
- **Resource validation**: Verifies generated `.tres` files are correctly formatted
- **Integration validation**: Confirms end-to-end conversion workflows work correctly

## Testing Results

All tests are passing:
- 15 new resource generator unit tests
- 3 integration tests
- All existing tests continue to pass

## Future Improvements

Potential areas for future enhancement:

1. **Enhanced Data Structures**: Add more detailed properties as needed
2. **Performance Optimization**: Optimize resource generation for large datasets
3. **Extended Validation**: Add more comprehensive validation rules
4. **Documentation**: Create detailed API documentation for all components