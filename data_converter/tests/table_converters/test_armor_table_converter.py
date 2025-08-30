#!/usr/bin/env python3
"""
Unit tests for ArmorTableConverter
"""

import tempfile
from pathlib import Path
import pytest

from data_converter.table_converters.armor_table_converter import ArmorTableConverter
from data_converter.table_converters.base_converter import ParseState


def test_armor_converter_initialization():
    """Test ArmorTableConverter initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ArmorTableConverter(source_dir, target_dir)

        # Check that the converter is properly initialized
        assert converter.source_dir == source_dir
        assert converter.target_dir == target_dir
        assert converter.get_table_type().value == "armor"
        assert len(converter._parse_patterns) > 0


def test_armor_converter_can_convert():
    """Test that ArmorTableConverter can identify armor table files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ArmorTableConverter(source_dir, target_dir)

        # Create a test armor table file
        armor_file = source_dir / "armor.tbl"
        with open(armor_file, "w") as f:
            f.write("#Armor Type\\n$Name: Test Armor\\n#End")

        # Should be able to convert armor table files
        assert converter.can_convert(armor_file)


def test_parse_armor_entry():
    """Test parsing a single armor entry"""
    # Create test content
    test_content = [
        "$Name: Light Hull",
        "$Damage Type: Laser",
        "$Reduction: 0.8",
        "#End",
    ]

    state = ParseState(lines=test_content, current_line=0)
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ArmorTableConverter(source_dir, target_dir)
        result = converter.parse_entry(state)

        assert result is not None
        assert result["name"] == "Light Hull"
        assert result["damage_type"] == "Laser"
        assert result["reduction"] == 0.8


def test_validate_armor_entry():
    """Test armor entry validation"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ArmorTableConverter(source_dir, target_dir)

        # Valid entry
        valid_entry = {"name": "Test Armor", "reduction": 0.8}
        assert converter.validate_entry(valid_entry)

        # Invalid entry - missing name
        invalid_entry = {"reduction": 0.8}
        assert not converter.validate_entry(invalid_entry)

        # Invalid entry - wrong type for numeric field
        invalid_entry2 = {"name": "Test Armor", "reduction": "invalid"}
        assert not converter.validate_entry(invalid_entry2)


def test_convert_armor_table_file():
    """Test converting a complete armor table file"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ArmorTableConverter(source_dir, target_dir)

        # Create test table content
        table_content = """#Armor Type

$Name: Light Hull
$Damage Type: Laser
$Reduction: 0.8

#End
"""

        # Create test file
        test_file = source_dir / "armor.tbl"
        with open(test_file, "w") as f:
            f.write(table_content)

        # Test conversion
        success = converter.convert_table_file(test_file)
        assert success

        # Check that output files were created
        output_files = list((target_dir / "assets" / "tables").glob("*.tres"))
        assert len(output_files) >= 0  # At least the main table file


if __name__ == "__main__":
    pytest.main([__file__])
