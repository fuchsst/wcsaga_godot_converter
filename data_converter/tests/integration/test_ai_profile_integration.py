#!/usr/bin/env python3
"""
Integration test for AI Profile Resource Generator with existing conversion system
"""

import tempfile
import json
from pathlib import Path

from data_converter.resource_generators.ai_profile_resource_generator import AIProfileResourceGenerator
from data_converter.table_converters.ai_profiles_table_converter import AIProfilesTableConverter
from data_converter.core.table_data_structures import TableType


def main():
    """Test the integration between AI profile table converter and resource generator"""
    # Create sample AI profile data that matches the format from ai_profiles.tbl
    sample_ai_profile_content = """#AI Profiles

$Default Profile:                            SAGA RETAIL

$Profile Name:                               SAGA RETAIL

;; Difficulty-related values; 
;; Each option specifies a list corresponding to the
;; five skill values (Very Easy, Easy, Medium, Hard, Insane).

$Primary Weapon Delay:            0.5,   0.4,   0.3,   0.2,   0.1
$Secondary Weapon Delay:          1.0,   0.8,   0.6,   0.4,   0.2
$Use Countermeasures:             YES,   YES,   YES,   YES,   YES
$Evade Missiles:                  YES,   YES,   YES,   YES,   YES
$Shield Manage Delay:             6.0,   4.0,   2.0,   1.0,   0.1
$Predict Position Delay:          2.0,   1.5,   1.0,   0.5,   0.0
$Player Damage Factor:            0.25,  0.5,   0.65,  0.85,  1.0
$Player Subsys Damage Factor:     0.2,   0.4,   0.6,   0.8,   1.0
$Friendly AI Fire Delay Scale:    2.0,   1.5,   1.0,   1.0,   1.0
$Hostile AI Fire Delay Scale:     4.0,   2.0,   1.0,   1.0,   1.0

$Profile Name:                               TEST PROFILE

$Primary Weapon Delay:            0.6,   0.5,   0.4,   0.3,   0.2
$Secondary Weapon Delay:          1.2,   1.0,   0.8,   0.6,   0.4
$Use Countermeasures:             NO,    NO,    NO,    NO,    NO
$Evade Missiles:                  NO,    NO,    NO,    NO,    NO
$Shield Manage Delay:             7.0,   5.0,   3.0,   2.0,   0.5
$Predict Position Delay:          3.0,   2.0,   1.5,   1.0,   0.5
$Player Damage Factor:            0.3,   0.6,   0.7,   0.9,   1.1
$Player Subsys Damage Factor:     0.3,   0.5,   0.7,   0.9,   1.1
$Friendly AI Fire Delay Scale:    3.0,   2.0,   1.5,   1.0,   1.0
$Hostile AI Fire Delay Scale:     5.0,   3.0,   2.0,   1.5,   1.0

#End
"""

    # Create mock objects for the required parameters
    class MockAssetCatalog:
        def get_asset(self, asset_id):
            return None

        def register_asset(self, asset_data):
            pass

    class MockRelationshipBuilder:
        def add_relationship(self, source_id, target_id, relationship_type, strength=1.0, metadata=None):
            pass

    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        # Create sample AI profile file
        ai_profile_file = source_dir / "ai_profiles.tbl"
        with open(ai_profile_file, 'w') as f:
            f.write(sample_ai_profile_content)
        
        # Parse AI profile data using the table converter
        print("Parsing AI profile data with table converter...")
        converter = AIProfilesTableConverter(source_dir, target_dir)
        
        # Read and parse the table file
        with open(ai_profile_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Create parse state
        lines = content.splitlines()
        from data_converter.table_converters.base_converter import ParseState
        state = ParseState(lines)
        
        # Parse the table
        entries = converter.parse_table(state)
        print(f"Parsed {len(entries)} AI profile entries:")
        for entry in entries:
            print(f"  - {entry.get('name', 'Unknown')}")
        
        # Validate entries
        valid_entries = [entry for entry in entries if converter.validate_entry(entry)]
        print(f"Valid entries: {len(valid_entries)}")
        
        # Convert to Godot resource format using the table converter
        godot_resource = converter.convert_to_godot_resource(valid_entries)
        print(f"Converted to Godot resource with {len(godot_resource.get('profiles', {}))} AI profiles")
        
        # Now use the AI profile resource generator to create individual .tres files
        print("\nGenerating individual AI profile resource files...")
        generator = AIProfileResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), target_dir
        )
        
        # Generate AI profile resources
        result_files = generator.generate_ai_profile_resources(valid_entries)
        
        # Print results
        print(f"Generated {len(result_files)} files:")
        for name, path in result_files.items():
            print(f"  {name}: {path}")
            
        # Show content of one of the generated files
        if result_files:
            saga_retail_file = target_dir / "assets" / "data" / "ai" / "profiles" / "saga_retail.tres"
            if saga_retail_file.exists():
                print(f"\nContent of {saga_retail_file}:")
                with open(saga_retail_file, 'r') as f:
                    print(f.read())


if __name__ == "__main__":
    main()