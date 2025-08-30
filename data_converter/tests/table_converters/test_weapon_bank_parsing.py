#!/usr/bin/env python3
"""
Unit tests for weapon bank configuration parsing
"""

import tempfile
from pathlib import Path
import pytest

from data_converter.table_converters.ship_table_converter import ShipTableConverter
from data_converter.table_converters.base_converter import ParseState


def test_parse_weapon_bank_properties():
    """Test parsing weapon bank properties including dogfight modes"""
    test_content = [
        "$Name: Test Ship",
        '$Allowed PBanks: ( "Laser" ) ( "Ion" )',
        '$Allowed SBanks: ( "Spiculum IR" "Javelin HS" ) ( "Pilum FF" "Spiculum IR" )',
        '$Default PBanks: ( "Laser" "Ion" )',
        '$Default SBanks: ( "Javelin HS" "Spiculum IR" )',
        "$SBank Capacity: (20, 20)",
        '$Allowed Dogfight PBanks: ( "Laser" )',
        '$Allowed Dogfight SBanks: ( "Spiculum IR" "Javelin HS" )',
        "$Weapon Regeneration Rate: 0.14",
        "$Max Weapon Eng: 45.0",
        "$end_multi_text",
    ]

    state = ParseState(lines=test_content, current_line=0)
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ShipTableConverter(source_dir, target_dir)
        result = converter.parse_entry(state)

        assert result is not None
        assert result["name"] == "Test Ship"
        assert result["allowed_pbanks"] == [["Laser"], ["Ion"]]
        assert result["allowed_sbanks"] == [
            ["Spiculum IR", "Javelin HS"],
            ["Pilum FF", "Spiculum IR"],
        ]
        assert result["default_pbanks"] == [["Laser", "Ion"]]
        assert result["default_sbanks"] == [["Javelin HS", "Spiculum IR"]]
        assert result["sbank_capacity"] == [20, 20]
        assert result["allowed_dogfight_pbanks"] == [["Laser"]]
        assert result["allowed_dogfight_sbanks"] == [["Spiculum IR", "Javelin HS"]]
        assert result["weapon_regeneration_rate"] == 0.14
        assert result["max_weapon_energy"] == 45.0


def test_parse_weapon_banks_with_varied_formatting():
    """Test parsing weapon banks with different formatting styles"""
    test_content = [
        "$Name: Test Ship",
        '$Allowed PBanks: ("Laser") ("Ion" "Plasma")',
        '$Allowed SBanks: ( "Spiculum IR" "Javelin HS" ) ( "Pilum FF" )',
        "$SBank Capacity: ( 20, 15, 10 )",
        "$end_multi_text",
    ]

    state = ParseState(lines=test_content, current_line=0)
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ShipTableConverter(source_dir, target_dir)
        result = converter.parse_entry(state)

        assert result is not None
        assert result["name"] == "Test Ship"
        assert result["allowed_pbanks"] == [["Laser"], ["Ion", "Plasma"]]
        assert result["allowed_sbanks"] == [["Spiculum IR", "Javelin HS"], ["Pilum FF"]]
        assert result["sbank_capacity"] == [20, 15, 10]


def test_validate_weapon_entry():
    """Test validation of weapon properties"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ShipTableConverter(source_dir, target_dir)

        # Valid entry with weapon properties
        valid_entry = {
            "name": "Test Ship",
            "weapon_regeneration_rate": 0.14,
            "max_weapon_energy": 45.0,
        }
        assert converter.validate_entry(valid_entry)

        # Invalid entry - wrong type for numeric field
        invalid_entry = {
            "name": "Test Ship",
            "weapon_regeneration_rate": "invalid",
        }
        assert not converter.validate_entry(invalid_entry)


if __name__ == "__main__":
    pytest.main([__file__])
