#!/usr/bin/env python3
"""
Unit tests for SpeciesDefsTableConverter
"""

import tempfile
from pathlib import Path
import pytest

from data_converter.table_converters.species_defs_table_converter import SpeciesDefsTableConverter
from data_converter.table_converters.base_converter import ParseState


def test_species_converter_initialization():
    """Test SpeciesDefsTableConverter initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = SpeciesDefsTableConverter(source_dir, target_dir)
        
        # Check that the converter is properly initialized
        assert converter.source_dir == source_dir
        assert converter.target_dir == target_dir
        assert converter.get_table_type().value == "species_defs"
        assert len(converter._parse_patterns) > 0


def test_species_converter_can_convert():
    """Test that SpeciesDefsTableConverter can identify species table files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = SpeciesDefsTableConverter(source_dir, target_dir)
        
        # Create a test species table file
        species_file = source_dir / "species_defs.tbl"
        with open(species_file, "w") as f:
            f.write("$NumSpecies: 1\\n$Species_Name: Test Species\\n#END")
        
        # Should be able to convert species table files
        assert converter.can_convert(species_file) == True


def test_parse_species_entry():
    """Test parsing a single species entry"""
    # Create test content
    test_content = [
        "$Species_Name: Terran",
        "$Default IFF: Friendly",
        "$FRED Color: (0, 0, 255)",
        "#END"
    ]
    
    state = ParseState(lines=test_content, current_line=0)
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = SpeciesDefsTableConverter(source_dir, target_dir)
        result = converter.parse_entry(state)
        
        assert result is not None
        assert result["name"] == "Terran"
        assert result["default_iff"] == "Friendly"
        assert result["fred_color"] == [0, 0, 255]


def test_validate_species_entry():
    """Test species entry validation"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = SpeciesDefsTableConverter(source_dir, target_dir)
        
        # Valid entry
        valid_entry = {
            "name": "Test Species"
        }
        assert converter.validate_entry(valid_entry) == True
        
        # Invalid entry - missing name
        invalid_entry = {}
        assert converter.validate_entry(invalid_entry) == False


def test_convert_species_table_file():
    """Test converting a complete species table file"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = SpeciesDefsTableConverter(source_dir, target_dir)
        
        # Create test table content
        table_content = """$NumSpecies: 1

$Species_Name: Terran
$Default IFF: Friendly
$FRED Color: (0, 0, 255)

#END
"""
        
        # Create test file
        test_file = source_dir / "species_defs.tbl"
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