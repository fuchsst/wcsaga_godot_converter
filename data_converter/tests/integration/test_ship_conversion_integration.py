#!/usr/bin/env python3
"""
Integration test for ship table conversion to Godot resources
"""

import tempfile
import os
from pathlib import Path
import pytest

from data_converter.table_converters.ship_table_converter import ShipTableConverter
from data_converter.resource_generators.ship_class_generator import ShipClassGenerator
from data_converter.table_converters.base_converter import ParseState


def test_ship_conversion_integration():
    """Test integration between ShipTableConverter and ShipClassGenerator"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create source and target directories
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        # Create a test ships.tbl file
        ships_tbl_content = """
#Ship Classes

$Name: GTB Nova
$Species: Terran
$Type: Bomber
$Hitpoints: 150
$Shields: 100
$Mass: 50
$Max velocity: 75
$POF file: nova.pof
$Ship_icon: nova_icon.png
$Allowed PBanks: ( "Laser" ) ( "Ion" )
$Allowed SBanks: ( "Missile" )
$SBank Capacity: (20, 20)
#End

$Name: GTD Hekate
$Species: Terran
$Type: Capital
$Hitpoints: 1000
$Shields: 500
$Mass: 10000
$Max velocity: 30
$POF file: hekate.pof
$Ship_icon: hekate_icon.png
#End
"""

        # Write the test file
        ships_tbl_path = source_dir / "ships.tbl"
        with open(ships_tbl_path, "w") as f:
            f.write(ships_tbl_content)

        # Initialize converter and generator
        converter = ShipTableConverter(source_dir, target_dir)
        generator = ShipClassGenerator(str(target_dir))

        # Parse the ship table
        with open(ships_tbl_path, "r") as f:
            lines = [line.rstrip() for line in f.readlines()]

        state = ParseState(lines=lines, current_line=0)
        ship_entries = converter.parse_table(state)

        # Verify parsing worked
        assert len(ship_entries) == 2
        assert ship_entries[0]["name"] == "GTB Nova"
        assert ship_entries[1]["name"] == "GTD Hekate"

        # Generate Godot resources
        generated_files = generator.generate_ship_resources(ship_entries)

        # Should generate 3 files (2 ship resources + 1 registry)
        assert len(generated_files) == 3

        # Check that all files exist
        for file_path in generated_files:
            assert os.path.exists(file_path)

        # Check specific file paths
        fighter_files = [f for f in generated_files if "features/fighters/" in f]
        capital_files = [f for f in generated_files if "features/capital_ships/" in f]
        registry_files = [f for f in generated_files if "ship_registry.tres" in f]

        assert len(fighter_files) == 1  # GTB Nova
        assert len(capital_files) == 1  # GTD Hekate
        assert len(registry_files) == 1  # Registry file

        # Check content of generated files
        # Check fighter resource
        with open(fighter_files[0], "r") as f:
            fighter_content = f.read()
        assert "GTB Nova" in fighter_content
        assert "max_hull_strength = 150.0" in fighter_content
        assert 'allowed_primary_banks = [["Laser"], ["Ion"]]' in fighter_content

        # Check capital resource
        with open(capital_files[0], "r") as f:
            capital_content = f.read()
        assert "GTD Hekate" in capital_content
        assert "max_hull_strength = 1000.0" in capital_content

        # Check registry
        with open(registry_files[0], "r") as f:
            registry_content = f.read()
        assert "ShipRegistryData" in registry_content
        assert "gtb_nova" in registry_content
        assert "gtd_hekate" in registry_content


if __name__ == "__main__":
    pytest.main([__file__])
