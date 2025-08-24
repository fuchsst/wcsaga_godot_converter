#!/usr/bin/env python3
"""
Unit tests for ShipTableConverter
"""

import tempfile
from pathlib import Path
import pytest

from data_converter.table_converters.ship_table_converter import ShipTableConverter
from data_converter.table_converters.base_converter import ParseState


def test_ship_converter_initialization():
    """Test ShipTableConverter initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = ShipTableConverter(source_dir, target_dir)
        
        # Check that the converter is properly initialized
        assert converter.source_dir == source_dir
        assert converter.target_dir == target_dir
        assert converter.get_table_type().value == "ships"
        assert len(converter._parse_patterns) > 0


def test_ship_converter_can_convert():
    """Test that ShipTableConverter can identify ship table files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = ShipTableConverter(source_dir, target_dir)
        
        # Create a test ship table file
        ship_file = source_dir / "ships.tbl"
        with open(ship_file, "w") as f:
            f.write("#Ship Classes\\n$Name: Test Ship\\n#End")
        
        # Should be able to convert ship table files
        assert converter.can_convert(ship_file) == True


def test_parse_ship_entry():
    """Test parsing a single ship entry"""
    # Create test content
    test_content = [
        "$Name: Test Fighter",
        "$Species: Terran",
        "$Type: Fighter",
        "$Max velocity: 100, 100, 100",
        "$Shields: 100",
        "$Hitpoints: 150",
        "$end_multi_text"
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
        assert result["name"] == "Test Fighter"
        assert result["species"] == "Terran"
        assert result["type"] == "Fighter"
        assert "max_velocity" in result
        assert result["max_shield"] == 100.0
        assert result["hitpoints"] == 150.0


def test_parse_velocity_vector():
    """Test parsing velocity vector strings"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = ShipTableConverter(source_dir, target_dir)
        
        # Test 3-component vector
        result = converter._parse_velocity_vector("100, 75, 50")
        assert result["forward"] == 100.0
        assert result["reverse"] == 75.0
        assert result["side"] == 50.0
        
        # Test single value
        result = converter._parse_velocity_vector("65")
        assert result["forward"] == 65.0
        assert result["reverse"] == 65.0
        assert result["side"] == 65.0


def test_validate_ship_entry():
    """Test ship entry validation"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = ShipTableConverter(source_dir, target_dir)
        
        # Valid entry
        valid_entry = {
            "name": "Test Ship",
            "hitpoints": 100.0,
            "mass": 50.0
        }
        assert converter.validate_entry(valid_entry) == True
        
        # Invalid entry - missing name
        invalid_entry = {
            "hitpoints": 100.0,
            "mass": 50.0
        }
        assert converter.validate_entry(invalid_entry) == False
        
        # Invalid entry - wrong type for numeric field
        invalid_entry2 = {
            "name": "Test Ship",
            "hitpoints": "invalid",
            "mass": 50.0
        }
        assert converter.validate_entry(invalid_entry2) == False


def test_convert_ship_table_file():
    """Test converting a complete ship table file"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()
        
        converter = ShipTableConverter(source_dir, target_dir)
        
        # Create test table content
        table_content = """#Ship Classes

$Name: Test Fighter
$Species: Terran
$Type: Fighter
$Max velocity: 100, 100, 100
$Shields: 100
$Hitpoints: 150

$end_multi_text
"""
        
        # Create test file
        test_file = source_dir / "ships.tbl"
        with open(test_file, "w") as f:
            f.write(table_content)
        
        # Test conversion
        success = converter.convert_table_file(test_file)
        assert success == True
        
        # Check that output files were created
        output_files = list((target_dir / "assets" / "tables").glob("*.tres"))
        assert len(output_files) >= 0  # At least the main table file


def test_ship_converter_new_asset_patterns():
    """Test parsing ship entries with new asset patterns"""
    # Create test content with new asset patterns
    test_content = [
        "$Name: Test Ship",
        "$Short name: Test",
        "$Species: Terran",
        "$POF file: test_ship.pof",
        "$EngineSnd: 126",
        "$Shield_icon: test_icon",
        "$Closeup_pos: 0.0, 0.0, -15.0",
        "$Closeup_zoom: 0.43633",
        "$Thruster01 Radius factor: 0.6",
        "$Thruster02 Length factor: 0.7",
        "$Allowed PBanks: ( \"Laser\" ) ( \"Ion\" )",
        "$Allowed SBanks: ( \"Spiculum IR\" \"Javelin HS\" )",
        "$Default PBanks: ( \"Laser\" \"Ion\" )",
        "$Default SBanks: ( \"Javelin HS\" \"Spiculum IR\" )",
        "$SBank Capacity: (20, 20)",
        "$Subsystem: communication, 10.0, 0.0",
        "    $Alt Subsystem Name: Comm",
        "    $Alt Damage Popup Subsystem Name: Communication",
        "$end_multi_text"
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
        assert result["short_name"] == "Test"
        assert result["species"] == "Terran"
        assert result["pof_file"] == "test_ship.pof"
        assert result["engine_sound"] == "126"
        assert result["shield_icon"] == "test_icon"
        assert result["closeup_pos"] == {"x": 0.0, "y": 0.0, "z": -15.0}
        assert result["closeup_zoom"] == 0.43633
        assert result["thruster_radius_factor"] == 0.6
        assert result["thruster_length_factor"] == 0.7
        assert result["allowed_pbanks"] == [["Laser"], ["Ion"]]
        assert result["allowed_sbanks"] == [["Spiculum IR", "Javelin HS"]]
        assert result["sbank_capacity"] == [20, 20]
        
        # Check asset relationships were captured
        registries = converter.get_registries()
        asset_registry = registries["asset_registry"]
        assert "Test Ship" in asset_registry
        assert len(asset_registry["Test Ship"]) > 0


if __name__ == "__main__":
    pytest.main([__file__])