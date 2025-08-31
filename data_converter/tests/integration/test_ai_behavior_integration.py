#!/usr/bin/env python3
"""
Integration test for AI Behavior Resource Generator with existing conversion system
"""

import tempfile
import json
from pathlib import Path

from data_converter.resource_generators.ai_behavior_resource_generator import AIBehaviorResourceGenerator
from data_converter.table_converters.ai_table_converter import AITableConverter
from data_converter.core.table_data_structures import TableType


def main():
    """Test the integration between AI behavior table converter and resource generator"""
    # Create sample AI behavior data that matches the format from ai.tbl
    sample_ai_behavior_content = """;    ai.tbl

; This file specifies AI class behavior for each skill level.
; We have five skill levels: Trainee, Rookie, Hotshot, Ace, Insane.

#AI Classes

;$accuracy:         0.0 ..   1.0    how accurately this ship fires its lasers
;$evasion:          0.0 .. 100.0    how effective this ship is at evading
;$courage:          0.0 .. 100.0    how likely to chance danger to accomplish goal
;$patience:         0.0 .. 100.0    how willing to wait for advantage before pursuing goal

;                                       TRAINEE     ROOKIE      HOTSHOT     ACE         INSANE

$Name:                                  Coward
$accuracy:                                0.8,        0.85,       0.9,        0.95,       1.0
$evasion:                                40.0,       50.0,       60.0,       80.0,      100.0
$courage:                                50.0,       50.0,       50.0,       50.0,       50.0
$patience:                               40.0,       50.0,       60.0,       80.0,      100.0
$Autoscale by AI Class Index:             NO
$AI Countermeasure Firing Chance:         0.0,        0.0,        0.0,        0.0,        0.0

$Name:                                  Aggressive
$accuracy:                                0.9,        0.92,       0.94,       0.96,       0.98
$evasion:                                20.0,       30.0,       40.0,       60.0,       80.0
$courage:                                80.0,       85.0,       90.0,       95.0,      100.0
$patience:                               10.0,       15.0,       20.0,       25.0,       30.0
$Autoscale by AI Class Index:             YES
$AI Countermeasure Firing Chance:         0.1,        0.2,        0.3,        0.4,        0.5

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
        
        # Create sample AI behavior file
        ai_behavior_file = source_dir / "ai.tbl"
        with open(ai_behavior_file, 'w') as f:
            f.write(sample_ai_behavior_content)
        
        # Parse AI behavior data using the table converter
        print("Parsing AI behavior data with table converter...")
        converter = AITableConverter(source_dir, target_dir)
        
        # Read and parse the table file
        with open(ai_behavior_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Create parse state
        lines = content.splitlines()
        from data_converter.table_converters.base_converter import ParseState
        state = ParseState(lines)
        
        # Parse the table
        entries = converter.parse_table(state)
        print(f"Parsed {len(entries)} AI behavior entries:")
        for entry in entries:
            print(f"  - {entry.get('name', 'Unknown')}")
        
        # Validate entries
        valid_entries = [entry for entry in entries if converter.validate_entry(entry)]
        print(f"Valid entries: {len(valid_entries)}")
        
        # Convert to Godot resource format using the table converter
        godot_resource = converter.convert_to_godot_resource(valid_entries)
        print(f"Converted to Godot resource with {len(godot_resource.get('ai_classes', {}))} AI behaviors")
        
        # Now use the AI behavior resource generator to create individual .tres files
        print("\nGenerating individual AI behavior resource files...")
        generator = AIBehaviorResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), target_dir
        )
        
        # Generate AI behavior resources
        result_files = generator.generate_ai_behavior_resources(valid_entries)
        
        # Print results
        print(f"Generated {len(result_files)} files:")
        for name, path in result_files.items():
            print(f"  {name}: {path}")
            
        # Show content of one of the generated files
        if result_files:
            coward_file = target_dir / "assets" / "data" / "ai" / "coward_behavior.tres"
            if coward_file.exists():
                print(f"\nContent of {coward_file}:")
                with open(coward_file, 'r') as f:
                    print(f.read())


if __name__ == "__main__":
    main()