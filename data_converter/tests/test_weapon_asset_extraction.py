#!/usr/bin/env python3
"""
Test script to verify weapon asset reference extraction and save output for inspection
"""

from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from data_converter.table_converters.weapon_table_converter import WeaponTableConverter


def test_weapon_asset_extraction():
    """Test weapon asset reference extraction and save output"""
    weapons_tbl_path = Path("source_assets/wcs_hermes_campaign/hermes_core/weapons.tbl")
    output_dir = Path("data_converter/tests/output")
    output_dir.mkdir(exist_ok=True)

    if not weapons_tbl_path.exists():
        print(f"weapons.tbl not found at {weapons_tbl_path}")
        return

    # Create converter
    converter = WeaponTableConverter(Path("."), output_dir)

    # Test conversion of the actual file
    success = converter.convert_table_file(weapons_tbl_path)
    print(f"Conversion success: {success}")

    # Check what was generated
    if output_dir.exists():
        print("\nGenerated files:")
        for file in output_dir.rglob("*"):
            if file.is_file():
                print(f"  {file.relative_to(output_dir)}")

    # Let's also manually parse and check some entries
    with open(weapons_tbl_path, "r") as f:
        content = f.read()

    state = converter._prepare_parse_state(content, str(weapons_tbl_path))
    entries = converter._parse_all_entries(state)

    print(f"\nFound {len(entries)} weapon entries")

    # Check the first few entries for asset references
    for i, entry in enumerate(entries[:3]):
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
                    "launch",
                    "impact",
                    "muzzle",
                    "effect",
                    "explosion",
                ]
            )
        ]
        for key in sorted(asset_keys):
            print(f"  {key}: {entry[key]}")

    # Show some specific examples
    print("\n=== ASSET REFERENCE SUMMARY ===")
    total_model_files = sum(1 for entry in entries if entry.get("model_file"))
    total_laser_bitmaps = sum(1 for entry in entries if entry.get("laser_bitmap"))
    total_icons = sum(1 for entry in entries if entry.get("icon"))
    total_launch_sounds = sum(1 for entry in entries if entry.get("launch_sound"))
    total_impact_sounds = sum(1 for entry in entries if entry.get("impact_sound"))

    print(f"Entries with model files: {total_model_files}")
    print(f"Entries with laser bitmaps: {total_laser_bitmaps}")
    print(f"Entries with icons: {total_icons}")
    print(f"Entries with launch sounds: {total_launch_sounds}")
    print(f"Entries with impact sounds: {total_impact_sounds}")


if __name__ == "__main__":
    test_weapon_asset_extraction()
