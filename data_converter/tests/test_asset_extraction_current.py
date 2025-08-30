#!/usr/bin/env python3
"""
Test to show current asset reference extraction from weapons.tbl
"""

from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from data_converter.table_converters.weapon_table_converter import WeaponTableConverter


def test_current_asset_extraction():
    """Test current asset reference extraction"""
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

    # Show all entries that have any asset references
    print("\n=== ENTRIES WITH ASSET REFERENCES ===")
    entries_with_assets = 0
    for i, entry in enumerate(entries[:10]):  # Just show first 10 for brevity
        # Check for any asset-related fields
        asset_fields = [
            "model_file",
            "pof_file",
            "external_model_file",
            "laser_bitmap",
            "laser_glow",
            "laser_color",
            "laser_length",
            "laser_head_radius",
            "laser_tail_radius",
            "icon",
            "anim",
            "launch_sound",
            "impact_sound",
            "flyby_sound",
            "muzzleflash",
            "impact_effect",
            "impact_explosion_radius",
        ]

        asset_values = {
            field: entry.get(field) for field in asset_fields if entry.get(field)
        }
        if asset_values:
            entries_with_assets += 1
            print(f"\nWeapon {i+1}: {entry.get('name', 'Unknown')}")
            for field, value in asset_values.items():
                print(f"  {field}: {value}")

    print(f"\nTotal entries with asset references: {entries_with_assets}")

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
        "laser_length",
        "laser_head_radius",
        "laser_tail_radius",
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
        values = list(set(str(entry[field]) for entry in entries if entry.get(field)))
        if values:
            print(f"  {field}: {values[:3]}{'...' if len(values) > 3 else ''}")


if __name__ == "__main__":
    test_current_asset_extraction()
