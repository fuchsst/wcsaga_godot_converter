# WCS Table Data Converter Tests - Testing Framework

## Test Suite Overview

The Table Data Converter tests validate the conversion of Wing Commander Saga (WCS) table files (.tbl) to Godot-compatible resource formats within the modular conversion pipeline. This test suite focuses on ensuring data fidelity, error handling, and integration readiness for all table processing components.

## Test Implementation

### Core Test Components

**1. Modular Converter Tests**
- **ShipTableConverter tests** for ship class parsing and resource generation
- **WeaponTableConverter tests** for weapon definition validation
- **ArmorTableConverter tests** for damage type modifier processing
- **SpeciesTableConverter tests** for species-specific properties
- **IFFTableConverter tests** for faction relationship handling

**2. Orchestrator Integration Tests**
- **TableDataConverter validation** for proper delegation to modular converters
- **Conversion statistics tracking** for accurate progress reporting
- **Error handling integration** across all converter types
- **Asset relationship mapping** for cross-component compatibility

**3. Godot Resource Validation**
- **`.tres` resource compatibility** with Godot's import system
- **Type safety verification** for all generated resources
- **Data structure integrity** against original WCS specifications
- **Scene assembly readiness** for output data structure

### Test Coverage

**Complete coverage for all table types:**

**Ship Table Tests**
- Ship class parsing with comprehensive property validation
- Physics and movement characteristic testing
- Weapon bank compatibility and subsystem verification
- Error handling for malformed ship data

**Weapon Table Tests**
- Weapon specification parsing and validation
- Damage and effect property accuracy
- Firing characteristics and ballistics testing
- Shockwave and particle effect verification

**Armor Table Tests**
- Damage type modifier parsing and matrix validation
- Resistance property accuracy testing
- Flags and special property verification

**Species Table Tests**
- Thruster animation parsing and validation
- Debris behavior property testing
- Species-specific visual effects verification

**IFF Table Tests**
- Faction relationship parsing and validation
- Color management and tactical behavior testing
- Relationship mapping accuracy verification

## Testing Framework

### pytest Integration
- **Custom test runner** (`run_tests.sh`) for easy execution
- **Virtual environment integration** matching project standards
- **Automated test discovery** and comprehensive reporting
- **Performance benchmarking** for conversion efficiency

### Test Data Management
- **Sample table files** for all supported types and edge cases
- **Regression test suites** for bug prevention and validation
- **Performance test scenarios** for efficiency monitoring
- **Integration test data** for pipeline validation

## Test File Structure

```
data_converter/tests/
├── test_table_parsing.py          # Core parsing functionality tests
├── test_ship_converter.py         # Ship-specific converter tests
├── test_weapon_converter.py       # Weapon-specific converter tests
├── test_armor_converter.py        # Armor-specific converter tests
├── test_species_converter.py      # Species-specific converter tests
├── test_iff_converter.py          # IFF/faction converter tests
├── test_integration.py            # Pipeline integration tests
├── test_error_handling.py         # Error and edge case tests
├── test_performance.py            # Performance benchmarking tests
└── conftest.py                    # Test configuration and fixtures
```

## Key Test Features

### Data Fidelity Validation
- **Exact field mapping** between WCS structures and Godot resources
- **Numerical precision** matching original WCS implementation
- **Parsing behavior consistency** with C++ source code
- **Complete validation logic** preservation from original

### Error Handling Excellence
- **Line-by-line error reporting** with precise location tracking
- **Graceful degradation** for malformed input handling
- **Recovery mechanism** validation for common parsing issues
- **Comprehensive error messaging** and logging

### Performance Characteristics
- **Efficient parsing validation** within performance targets
- **Memory usage optimization** for large file processing
- **Parallel processing support** for concurrent operations
- **Progress reporting accuracy** for user feedback

### Integration Readiness
- **Scene assembly compatibility** with structured output data
- **Entity name consistency** for cross-component matching
- **Resource format compliance** with Godot specifications
- **Cross-reference integrity** for relationship mapping

## Test Execution

**Running the Test Suite:**

```bash
# Run all tests
./run_tests.sh

# Run specific test categories
./run_tests.sh test_ship_converter.py
./run_tests.sh test_weapon_converter.py
./run_tests.sh test_integration.py

# Run with verbose output
./run_tests.sh -v

# Run with coverage reporting
./run_tests.sh --cov=table_data_converter
```

**Test Output Includes:**
- **Detailed pass/fail reports** for each test case
- **Error location information** for debugging
- **Performance metrics** for conversion efficiency
- **Coverage analysis** for code quality assessment

## Quality Assurance

### Test Coverage Achievement
- **Comprehensive line coverage** for core parsing functionality
- **Edge case coverage** for robust error handling
- **Integration test completeness** for pipeline validation
- **Performance benchmark validation** for efficiency standards

### Architecture Compliance
- **Modular design validation** for converter components
- **Orchestrator functionality** testing for proper delegation
- **Resource generation accuracy** for Godot compatibility
- **Pipeline integration readiness** for scene assembly

## Test Validation Summary

The test suite successfully validates the WCS table data conversion with complete data fidelity, comprehensive relationship mapping, and seamless integration with the modular conversion pipeline.

**Key Test Achievements:**
- **Modular converter validation** for all table types
- **Orchestrator integration testing** for proper workflow management
- **Godot resource compatibility** ensuring production readiness
- **Performance optimization** for efficient processing
- **Error handling robustness** for reliable operation

The test suite is production-ready and provides solid validation for the WCS table data conversion in the Godot migration project.
