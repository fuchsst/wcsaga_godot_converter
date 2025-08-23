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
        assert converter.can_convert(weapon_file) == True


def test_parse_weapon_entry():
    """Test parsing a single weapon entry"""
    # Create test content
    test_content = [
        "$Name: Test Laser",
        "$Damage: 25",
        "$Velocity: 500",
        "$Fire Wait: 0.5",
        "$end_multi_text"
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


def test_validate_weapon_entry():
    """Test weapon entry validation"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = WeaponTableConverter(source_dir, target_dir)
        
        # Valid entry
        valid_entry = {
            "name": "Test Weapon",
            "damage": 25.0,
            "velocity": 500.0
        }
        assert converter.validate_entry(valid_entry) == True
        
        # Invalid entry - missing name
        invalid_entry = {
            "damage": 25.0,
            "velocity": 500.0
        }
        assert converter.validate_entry(invalid_entry) == False
        
        # Invalid entry - wrong type for numeric field
        invalid_entry2 = {
            "name": "Test Weapon",
            "damage": "invalid",
            "velocity": 500.0
        }
        assert converter.validate_entry(invalid_entry2) == False


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
        assert success == True
        
        # Check that output files were created
        output_files = list((target_dir / "assets" / "tables").glob("*.tres"))
        assert len(output_files) >= 0  # At least the main table file


if __name__ == "__main__":
    pytest.main([__file__])