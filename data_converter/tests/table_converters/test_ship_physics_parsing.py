#!/usr/bin/env python3
"""
Unit tests for ship physics property parsing
"""

import tempfile
from pathlib import Path
import pytest

from data_converter.table_converters.ship_table_converter import ShipTableConverter
from data_converter.table_converters.base_converter import ParseState


def test_parse_acceleration_properties():
    """Test parsing acceleration properties"""
    test_content = [
        "$Name: Test Ship",
        "$Forward accel: 5.0",
        "$Forward decel: 4.0",
        "$Slide accel: 3.0",
        "$Slide decel: 2.0",
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
        assert result["forward_accel"] == 5.0
        assert result["forward_decel"] == 4.0
        assert result["slide_accel"] == 3.0
        assert result["slide_decel"] == 2.0


def test_parse_rotation_properties():
    """Test parsing rotation properties"""
    test_content = [
        "$Name: Test Ship",
        "$Rotation time: 3.0, 3.0, 3.0",
        "$Rotation accel: 2.0, 2.0, 2.0",
        "$Rotation decel: 1.0, 1.0, 1.0",
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

        # Check rotation time
        assert isinstance(result["rotation_time"], dict)
        assert result["rotation_time"]["pitch"] == 3.0
        assert result["rotation_time"]["bank"] == 3.0
        assert result["rotation_time"]["heading"] == 3.0

        # Check rotation accel
        assert isinstance(result["rotation_accel"], dict)
        assert result["rotation_accel"]["pitch"] == 2.0
        assert result["rotation_accel"]["bank"] == 2.0
        assert result["rotation_accel"]["heading"] == 2.0

        # Check rotation decel
        assert isinstance(result["rotation_decel"], dict)
        assert result["rotation_decel"]["pitch"] == 1.0
        assert result["rotation_decel"]["bank"] == 1.0
        assert result["rotation_decel"]["heading"] == 1.0


def test_parse_rotation_single_value():
    """Test parsing rotation properties with single value"""
    test_content = ["$Name: Test Ship", "$Rotation time: 3.0", "$end_multi_text"]

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

        # Check rotation time with single value
        assert isinstance(result["rotation_time"], dict)
        assert result["rotation_time"]["pitch"] == 3.0
        assert result["rotation_time"]["bank"] == 3.0
        assert result["rotation_time"]["heading"] == 3.0


def test_validate_physics_entry():
    """Test validation of physics properties"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ShipTableConverter(source_dir, target_dir)

        # Valid entry with physics properties
        valid_entry = {
            "name": "Test Ship",
            "mass": 100.0,
            "density": 0.5,
            "forward_accel": 5.0,
            "forward_decel": 4.0,
            "slide_accel": 3.0,
            "slide_decel": 2.0,
        }
        assert converter.validate_entry(valid_entry)

        # Invalid entry - wrong type for numeric field
        invalid_entry = {
            "name": "Test Ship",
            "mass": "invalid",
            "forward_accel": 5.0,
        }
        assert not converter.validate_entry(invalid_entry)


if __name__ == "__main__":
    pytest.main([__file__])
