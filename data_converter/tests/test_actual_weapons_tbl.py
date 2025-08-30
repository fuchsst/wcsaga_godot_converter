#!/usr/bin/env python3
"""
Test script to verify weapon asset reference extraction from actual weapons.tbl file
"""

import tempfile
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from data_converter.table_converters.weapon_table_converter import WeaponTableConverter


def test_actual_weapons_tbl():
    """Test parsing actual weapons.tbl file"""
    weapons_tbl_path = Path("source_assets/wcs_hermes_campaign/hermes_core/weapons.tbl")

    if not weapons_tbl_path.exists():
        print(f"weapons.tbl not found at {weapons_tbl_path}")
        return

    # Create converter with temporary directories
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = WeaponTableConverter(source_dir, target_dir)

        # Test conversion of the actual file
        success = converter.convert_table_file(weapons_tbl_path)
        print(f"Conversion success: {success}")

        # Let's also manually parse and check some entries
        with open(weapons_tbl_path, "r") as f:
            content = f.read()

        state = converter._prepare_parse_state(content, str(weapons_tbl_path))
        entries = converter._parse_all_entries(state)

        print(f"Found {len(entries)} weapon entries")

        # Check the first few entries for asset references
        for i, entry in enumerate(entries[:5]):
            print(f"\nWeapon {i+1}: {entry.get('name', 'Unknown')}")
            # Print all keys that contain asset reference information
            asset_keys = [
                k
                for k in entry.keys()
                if any(
                    asset_term in k.lower()
                    for asset_term in [
                        "model",
                        "laser",
                        "bitmap",
                        "glow",
                        "icon",
                        "anim",
                        "sound",
                        "snd",
                        "muzzle",
                        "impact",
                        "effect",
                        "explosion",
                    ]
                )
            ]
            for key in sorted(asset_keys):
                print(f"  {key}: {entry[key]}")


if __name__ == "__main__":
    test_actual_weapons_tbl()
