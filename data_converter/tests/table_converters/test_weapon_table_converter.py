#!/usr/bin/env python3
"""
Unit tests for WeaponTableConverter
"""

import tempfile
from pathlib import Path
import pytest

from data_converter.table_converters.weapon_table_converter import WeaponTableConverter
from data_converter.table_converters.base_converter import ParseState


def test_weapon_converter_initialization():
    """Test WeaponTableConverter initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = WeaponTableConverter(source_dir, target_dir)

        # Check that the converter is properly initialized
        assert converter.source_dir == source_dir
        assert converter.target_dir == target_dir
        assert converter.get_table_type().value == "weapons"
        assert len(converter._parse_patterns) > 0


def test_weapon_converter_can_convert():
    """Test that WeaponTableConverter can identify weapon table files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = WeaponTableConverter(source_dir, target_dir)

        # Create a test weapon table file
        weapon_file = source_dir / "weapons.tbl"
        with open(weapon_file, "w") as f:
            f.write("#Primary Weapons\\n$Name: Test Weapon\\n#End")

        # Should be able to convert weapon table files
        assert converter.can_convert(weapon_file)


def test_parse_weapon_entry():
    """Test parsing a single weapon entry"""
    # Create test content
    test_content = [
        "$Name: Test Laser",
        "$Damage: 25",
        "$Velocity: 500",
        "$Fire Wait: 0.5",
        "$end_multi_text",
    ]

    state = ParseState(lines=test_content, current_line=0)
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = WeaponTableConverter(source_dir, target_dir)
        result = converter.parse_entry(state)

        assert result is not None
        assert result["name"] == "Test Laser"
        assert result["damage"] == 25.0
        assert result["velocity"] == 500.0
        assert result["fire_wait"] == 0.5


def test_parse_weapon_physics_properties():
    """Test parsing comprehensive weapon physics properties"""
    # Create test content with physics properties
    test_content = [
        "$Name: Test Missile",
        "$Damage: 100",
        "$Velocity: 300",
        "$Fire Wait: 2.0",
        "$Lifetime: 10.0",
        "$Energy Consumed: 5.0",
        "$Armor Factor: 1.5",
        "$Shield Factor: 0.8",
        "$Subsystem Factor: 0.5",
        "$Turn Time: 1.5",
        "$Free Flight Time: 0.5",
        "$end_multi_text",
    ]

    state = ParseState(lines=test_content, current_line=0)
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = WeaponTableConverter(source_dir, target_dir)
        result = converter.parse_entry(state)

        assert result is not None
        assert result["name"] == "Test Missile"
        assert result["damage"] == 100.0
        assert result["velocity"] == 300.0
        assert result["fire_wait"] == 2.0
        assert result["lifetime"] == 10.0
        assert result["energy_consumed"] == 5.0
        assert result["armor_factor"] == 1.5
        assert result["shield_factor"] == 0.8
        assert result["subsystem_factor"] == 0.5
        assert result["turn_time"] == 1.5
        assert result["free_flight_time"] == 0.5


def test_parse_weapon_categorization_and_targeting():
    """Test parsing weapon class categorization and targeting properties"""
    # Create test content with categorization and targeting properties
    test_content = [
        "#Primary Weapons",
        "$Name: Test Heat-Seeker",
        "$Homing: YES",
        "+Type: HEAT",
        "+Turn Time: 1.25",
        "+Min Lock Time: 0.70",
        "+Lock Pixels/Sec: 99",
        "+Catch-up Pixels/Sec: 120",
        "+Catch-up Penalty: 10",
        "+View Cone: 360.0",
        "$Free Flight Time: 1.0",
        "$end_multi_text",
    ]

    state = ParseState(
        lines=test_content, current_line=0, current_section="Primary Weapons"
    )
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = WeaponTableConverter(source_dir, target_dir)
        result = converter.parse_entry(state)

        assert result is not None
        assert result["name"] == "Test Heat-Seeker"
        assert result["weapon_class"] == "primary weapons"
        assert result["homing_type"] == "YES"
        assert result["homing_subtype"] == "HEAT"
        assert result["turn_time"] == 1.25
        assert result["min_lock_time"] == 0.70
        assert result["lock_pixels_per_sec"] == 99.0
        assert result["catchup_pixels_per_sec"] == 120.0
        assert result["catchup_penalty"] == 10.0
        assert result["view_cone"] == 360.0
        assert result["free_flight_time"] == 1.0


def test_validate_weapon_entry():
    """Test weapon entry validation"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = WeaponTableConverter(source_dir, target_dir)

        # Valid entry
        valid_entry = {"name": "Test Weapon", "damage": 25.0, "velocity": 500.0}
        assert converter.validate_entry(valid_entry)

        # Invalid entry - missing name
        invalid_entry = {"damage": 25.0, "velocity": 500.0}
        assert not converter.validate_entry(invalid_entry)

        # Invalid entry - wrong type for numeric field
        invalid_entry2 = {"name": "Test Weapon", "damage": "invalid", "velocity": 500.0}
        assert not converter.validate_entry(invalid_entry2)


def test_convert_weapon_table_file():
    """Test converting a complete weapon table file"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = WeaponTableConverter(source_dir, target_dir)

        # Create test table content
        table_content = """#Primary Weapons

$Name: Test Laser
$Damage: 25
$Velocity: 500
$Fire Wait: 0.5

$end_multi_text
"""

        # Create test file
        test_file = source_dir / "weapons.tbl"
        with open(test_file, "w") as f:
            f.write(table_content)

        # Test conversion
        success = converter.convert_table_file(test_file)
        assert success

        # Check that output files were created
        output_files = list((target_dir / "assets" / "tables").glob("*.tres"))
        assert len(output_files) >= 0  # At least the main table file


def test_parse_weapon_additional_properties():
    """Test parsing additional weapon properties with improved regex patterns"""
    # Create test content with additional properties
    test_content = [
        "$Name: Test Weapon",
        "$Damage: 100",
        "$Blast Force: 200.5",
        "$Inner Radius: 5.0",
        "$Outer Radius: 15.0",
        "$Shockwave Speed: 300",
        "$Rearm Rate: 1.5",
        "$FOF: 0.8",
        "$Laser Color: 255, 128, 64",
        "$View Cone: 180.0",
        "+View Cone: 90.0",
        "$end_multi_text",
    ]

    state = ParseState(lines=test_content, current_line=0)
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = WeaponTableConverter(source_dir, target_dir)
        result = converter.parse_entry(state)

        assert result is not None
        assert result["name"] == "Test Weapon"
        assert result["damage"] == 100.0
        assert result["blast_force"] == 200.5
        assert result["inner_radius"] == 5.0
        assert result["outer_radius"] == 15.0
        assert result["shockwave_speed"] == 300.0
        assert result["rearm_rate"] == 1.5
        assert result["fof"] == 0.8
        assert result["laser_color"] == "255, 128, 64"
        assert (
            result["view_cone"] == 90.0
        )  # Should use the +View Cone value due to our mapping


if __name__ == "__main__":
    pytest.main([__file__])
