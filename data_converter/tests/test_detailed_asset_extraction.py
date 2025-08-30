#!/usr/bin/env python3
"""
Detailed test to show specific asset references being extracted
"""

from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from data_converter.table_converters.weapon_table_converter import WeaponTableConverter


def test_detailed_asset_extraction():
    """Test detailed asset reference extraction"""
    weapons_tbl_path = Path("source_assets/wcs_hermes_campaign/hermes_core/weapons.tbl")

    if not weapons_tbl_path.exists():
        print(f"weapons.tbl not found at {weapons_tbl_path}")
        return

    # Create converter
    converter = WeaponTableConverter(Path("."), Path("data_converter/tests/output"))

    # Parse the content
    with open(weapons_tbl_path, "r") as f:
        content = f.read()

    state = converter._prepare_parse_state(content, str(weapons_tbl_path))
    entries = converter._parse_all_entries(state)

    print(f"Found {len(entries)} weapon entries")

    # Show detailed information for the first few entries
    print("\n=== DETAILED ASSET REFERENCE EXTRACTION ===")
    for i, entry in enumerate(entries[:5]):
        print(f"\nWeapon {i+1}: {entry.get('name', 'Unknown')}")

        # Show all asset-related fields
        asset_fields = [
            "model_file",
            "pof_file",
            "external_model_file",
            "laser_bitmap",
            "laser_glow",
            "laser_color",
            "laser_length",
            "icon",
            "anim",
            "launch_sound",
            "impact_sound",
            "flyby_sound",
            "muzzleflash",
            "impact_effect",
            "impact_explosion_radius",
        ]

        found_assets = False
        for field in asset_fields:
            if field in entry and entry[field]:
                print(f"  {field}: {entry[field]}")
                found_assets = True

        if not found_assets:
            print("  No asset references found")

    # Show summary statistics
    print("\n=== SUMMARY STATISTICS ===")
    asset_stats = {}
    asset_fields = [
        "model_file",
        "pof_file",
        "external_model_file",
        "laser_bitmap",
        "laser_glow",
        "laser_color",
        "icon",
        "anim",
        "launch_sound",
        "impact_sound",
        "flyby_sound",
        "muzzleflash",
        "impact_effect",
        "impact_explosion_radius",
    ]

    for field in asset_fields:
        count = sum(1 for entry in entries if entry.get(field))
        if count > 0:
            asset_stats[field] = count

    for field, count in sorted(asset_stats.items()):
        print(f"  {field}: {count}")

    # Show some example values
    print("\n=== EXAMPLE ASSET VALUES ===")
    for field in asset_fields:
        values = list(set(entry[field] for entry in entries if entry.get(field)))
        if values:
            print(f"  {field}: {values[:3]}{'...' if len(values) > 3 else ''}")


if __name__ == "__main__":
    test_detailed_asset_extraction()
