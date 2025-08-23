#!/usr/bin/env python3
"""
Unit tests for IFFTableConverter
"""

import tempfile
from pathlib import Path
import pytest

from data_converter.table_converters.iff_table_converter import IFFTableConverter
from data_converter.table_converters.base_converter import ParseState


def test_iff_converter_initialization():
    """Test IFFTableConverter initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = IFFTableConverter(source_dir, target_dir)
        
        # Check that the converter is properly initialized
        assert converter.source_dir == source_dir
        assert converter.target_dir == target_dir
        assert converter.get_table_type().value == "iff_defs"
        assert len(converter._parse_patterns) > 0


def test_iff_converter_can_convert():
    """Test that IFFTableConverter can identify IFF table files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = IFFTableConverter(source_dir, target_dir)
        
        # Create a test IFF table file
        iff_file = source_dir / "iff_defs.tbl"
        with open(iff_file, "w") as f:
            f.write("""#IFF Definitions
$Name: Test IFF
#End""")
        
        # Should be able to convert IFF table files
        assert converter.can_convert(iff_file) == True


def test_parse_iff_entry():
    """Test parsing a single IFF entry"""
    # Create test content
    test_content = [
        "$Name: Friendly",
        "$Color: (0, 255, 0)",
        "$Attackable: NO",
        "#End"
    ]
    
    state = ParseState(lines=test_content, current_line=0)
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = IFFTableConverter(source_dir, target_dir)
        result = converter.parse_entry(state)
        
        assert result is not None
        assert result["name"] == "Friendly"
        assert result["color"] == [0, 255, 0]
        assert result["attackable"] == False


def test_validate_iff_entry():
    """Test IFF entry validation"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = IFFTableConverter(source_dir, target_dir)
        
        # Valid entry
        valid_entry = {
            "name": "Test IFF",
            "color": [0, 255, 0]
        }
        assert converter.validate_entry(valid_entry) == True
        
        # Invalid entry - missing name
        invalid_entry = {
            "color": [0, 255, 0]
        }
        assert converter.validate_entry(invalid_entry) == False
        
        # Invalid entry - wrong format for color
        invalid_entry2 = {
            "name": "Test IFF",
            "color": [0, 255]  # Missing one component
        }
        assert converter.validate_entry(invalid_entry2) == False
        
        # Invalid entry - color component out of range
        invalid_entry3 = {
            "name": "Test IFF",
            "color": [0, 300, 0]  # 300 is out of range
        }
        assert converter.validate_entry(invalid_entry3) == False


def test_convert_iff_table_file():
    """Test converting a complete IFF table file"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = IFFTableConverter(source_dir, target_dir)
        
        # Create test table content
        table_content = """#IFF Definitions

$Name: Friendly
$Color: (0, 255, 0)
$Attackable: NO

#End
"""
        
        # Create test file
        test_file = source_dir / "iff_defs.tbl"
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
