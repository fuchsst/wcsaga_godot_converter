"""
Test for Help table converter
"""

import tempfile
from pathlib import Path

from data_converter.table_converters.help_table_converter import HelpTableConverter
from data_converter.table_converters.base_converter import ParseState


def test_help_converter_can_parse_content():
    """Test Help converter can parse content"""
    help_content = """
# Help Overlay Definitions

$briefing
+text 100 200 300 400 XSTR("Briefing Text", -1)
+text 150 250 350 450 XSTR("Another Text", -1)
+pline 4 10 20 30 40 50 60 70 80
+right_bracket 5 10 15 20
+left_bracket 25 30 35 40
$end

$ship
+text 50 100 150 200 XSTR("Ship Help Text", -1)
+pline 3 5 10 15 20 25
$end
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = HelpTableConverter(temp_path, temp_path)
        state = ParseState(lines=help_content.split('\n'), filename="test_help.tbl")
        
        entries = converter.parse_table(state)
        
        assert len(entries) == 2
        assert entries[0]["name"] == "briefing"
        assert entries[1]["name"] == "ship"
        assert len(entries[0]["texts"]) == 2
        assert len(entries[0]["lines"]) == 1
        assert len(entries[0]["right_brackets"]) == 1
        assert len(entries[0]["left_brackets"]) == 1


def test_help_converter_validation():
    """Test Help converter validation"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = HelpTableConverter(temp_path, temp_path)
        
        # Valid entry with name
        valid_entry = {
            "name": "test",
            "texts": [],
            "lines": [],
            "right_brackets": [],
            "left_brackets": []
        }
        assert converter.validate_entry(valid_entry) is True
        
        # Invalid entry without name
        invalid_entry = {
            "texts": [],
            "lines": [],
            "right_brackets": [],
            "left_brackets": []
        }
        assert converter.validate_entry(invalid_entry) is False


def test_help_converter_godot_conversion():
    """Test Help converter Godot resource conversion"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = HelpTableConverter(temp_path, temp_path)
        
        entries = [
            {
                "name": "briefing",
                "texts": [{"x": 100, "y": 200, "x1024": 300, "y1024": 400, "string": "Briefing Text"}],
                "lines": [{"point_count": 4, "points": [(10, 20), (30, 40), (50, 60), (70, 80)]}],
                "right_brackets": [{"x1": 5, "y1": 10, "x2": 15, "y2": 20}],
                "left_brackets": [{"x1": 25, "y1": 30, "x2": 35, "y2": 40}]
            }
        ]
        
        godot_resource = converter.convert_to_godot_resource(entries)
        
        assert godot_resource["resource_type"] == "WCSHelpOverlayDatabase"
        assert godot_resource["overlay_count"] == 1
        assert "briefing" in godot_resource["overlays"]
        assert godot_resource["overlays"]["briefing"]["name"] == "briefing"
        assert len(godot_resource["overlays"]["briefing"]["texts"]) == 1


def test_help_converter_with_actual_file():
    """Test Help converter with actual help.tbl file"""
    help_tbl_path = Path("source_assets/wcs_hermes_campaign/hermes_core/help.tbl")
    
    if not help_tbl_path.exists():
        # Skip test if file doesn't exist
        return
    
    # Read the file content
    with open(help_tbl_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = HelpTableConverter(temp_path, temp_path)
        state = ParseState(lines=content.split('\n'), filename=help_tbl_path.name)
        
        # Test parsing
        entries = converter.parse_table(state)
        
        # Should parse at least some entries
        assert len(entries) > 0
        
        # All entries should have names
        for entry in entries:
            assert "name" in entry
            assert converter.validate_entry(entry)
        
        # Test conversion to Godot format
        godot_resource = converter.convert_to_godot_resource(entries)
        
        assert godot_resource["resource_type"] == "WCSHelpOverlayDatabase"
        assert godot_resource["overlay_count"] == len(entries)
        assert len(godot_resource["overlays"]) == len(entries)