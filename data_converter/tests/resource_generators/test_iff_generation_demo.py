#!/usr/bin/env python3
"""
Test script for IFF Resource Generator
"""

import tempfile
import json
from pathlib import Path

from data_converter.resource_generators.iff_resource_generator import IFFResourceGenerator


def main():
    """Test the IFF resource generator with sample data"""
    # Create sample IFF data that matches the format from iff_defs.tbl
    sample_iff_data = [
        {
            "name": "Friendly",
            "color": [24, 72, 232],
            "attacks": ["Hostile", "Neutral", "Traitor"],
            "flags": ["orders hidden"],
            "default_ship_flags": ["cargo-known"],
            "default_ship_flags2": ["no-subspace-drive"]
        },
        {
            "name": "Hostile",
            "color": [236, 56, 24],
            "attacks": ["Friendly", "Neutral", "Traitor"],
            "sees_as": {
                "Friendly": [236, 56, 24],
                "Hostile": [24, 72, 232]
            },
            "flags": ["orders hidden", "wing name hidden"],
            "default_ship_flags2": ["no-subspace-drive"]
        },
        {
            "name": "Neutral",
            "color": [236, 56, 24],
            "attacks": ["Friendly", "Traitor"],
            "sees_as": {
                "Friendly": [236, 56, 24],
                "Hostile": [24, 72, 232],
                "Neutral": [24, 72, 232]
            },
            "flags": ["orders hidden", "wing name hidden"],
            "default_ship_flags2": ["no-subspace-drive"]
        }
    ]

    # Create mock objects for the required parameters
    class MockAssetCatalog:
        def get_asset(self, asset_id):
            return None

    class MockRelationshipBuilder:
        pass

    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = Path(temp_dir)
        
        # Create the IFF resource generator
        generator = IFFResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), output_dir
        )
        
        # Generate IFF resources
        print("Generating IFF resources...")
        result_files = generator.generate_iff_resources(sample_iff_data)
        
        # Print results
        print(f"Generated {len(result_files)} files:")
        for name, path in result_files.items():
            print(f"  {name}: {path}")
            
        # Show content of one of the generated files
        if result_files:
            first_iff_file = list(result_files.values())[0]
            print(f"\nContent of {first_iff_file}:")
            with open(first_iff_file, 'r') as f:
                print(f.read())


if __name__ == "__main__":
    main()