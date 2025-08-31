#!/usr/bin/env python3
"""
Integration test for IFF Resource Generator with existing conversion system
"""

import tempfile
import json
from pathlib import Path

from data_converter.resource_generators.iff_resource_generator import IFFResourceGenerator
from data_converter.table_converters.iff_table_converter import IFFTableConverter
from data_converter.core.table_data_structures import TableType


def main():
    """Test the integration between IFF table converter and resource generator"""
    # Create sample IFF data that matches the format from iff_defs.tbl
    sample_iff_content = """#IFFs

$Traitor IFF: Traitor

;------------------------
; Friendly
;------------------------
$IFF Name: Friendly
$Color: ( 24, 72, 232 )
$Attacks: ( "Hostile" "Neutral" "Traitor" )
$Flags: ( "orders hidden" )
$Default Ship Flags: ( "cargo-known" )
$Default Ship Flags2: ( "no-subspace-drive" )

;------------------------
; Hostile
;------------------------
$IFF Name: Hostile
$Color: ( 236, 56, 24 )
$Attacks: ( "Friendly" "Neutral" "Traitor" )
+Sees Friendly As: ( 236, 56, 24 )
+Sees Hostile As: ( 24, 72, 232 )
$Flags: ( "orders hidden" "wing name hidden" )
$Default Ship Flags2: ( "no-subspace-drive" )

;------------------------
; Neutral
;------------------------
$IFF Name: Neutral
$Color: ( 236, 56, 24 ) ; DONE
$Attacks: ( "Friendly" "Traitor" )
+Sees Friendly As: ( 236, 56, 24 )
+Sees Hostile As: ( 24, 72, 232 )
+Sees Neutral As: ( 24, 72, 232 )
$Flags: ( "orders hidden" "wing name hidden" )
$Default Ship Flags2: ( "no-subspace-drive" )

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
        
        # Create sample IFF file
        iff_file = source_dir / "iff_defs.tbl"
        with open(iff_file, 'w') as f:
            f.write(sample_iff_content)
        
        # Parse IFF data using the table converter
        print("Parsing IFF data with table converter...")
        converter = IFFTableConverter(source_dir, target_dir)
        
        # Read and parse the table file
        with open(iff_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Create parse state
        lines = content.splitlines()
        from data_converter.table_converters.base_converter import ParseState
        state = ParseState(lines)
        
        # Parse the table
        entries = converter.parse_table(state)
        print(f"Parsed {len(entries)} IFF entries:")
        for entry in entries:
            print(f"  - {entry.get('name', 'Unknown')}")
        
        # Validate entries
        valid_entries = [entry for entry in entries if converter.validate_entry(entry)]
        print(f"Valid entries: {len(valid_entries)}")
        
        # Convert to Godot resource format using the table converter
        godot_resource = converter.convert_to_godot_resource(valid_entries)
        print(f"Converted to Godot resource with {len(godot_resource.get('iffs', {}))} IFFs")
        
        # Now use the IFF resource generator to create individual .tres files
        print("\nGenerating individual IFF resource files...")
        generator = IFFResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), target_dir
        )
        
        # Generate IFF resources
        result_files = generator.generate_iff_resources(valid_entries)
        
        # Print results
        print(f"Generated {len(result_files)} files:")
        for name, path in result_files.items():
            print(f"  {name}: {path}")
            
        # Show content of one of the generated files
        if result_files:
            friendly_file = target_dir / "assets" / "data" / "iff" / "friendly.tres"
            if friendly_file.exists():
                print(f"\nContent of {friendly_file}:")
                with open(friendly_file, 'r') as f:
                    print(f.read())


if __name__ == "__main__":
    main()