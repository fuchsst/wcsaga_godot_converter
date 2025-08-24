"""
Test for Fireball table converter
"""

import tempfile
from pathlib import Path

from data_converter.table_converters.fireball_table_converter import FireballTableConverter
from data_converter.table_converters.base_converter import ParseState


def test_fireball_converter_can_parse_content():
    """Test fireball converter can parse content"""
    fireball_content = """
#Start
$Name: Explosion01
  $LOD: 1
#End

#Start
$Name: Explosion02
  $LOD: 0
#End
"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = FireballTableConverter(temp_path, temp_path)
        
        state = ParseState(lines=fireball_content.split('\n'), filename="test_fireball.tbl")
        entries = converter.parse_table(state)
        
        assert len(entries) == 2, f"Expected 2 fireball entries, got {len(entries)}"
        assert entries[0]['name'] == 'Explosion01', "First fireball should be Explosion01"
        assert entries[1]['name'] == 'Explosion02', "Second fireball should be Explosion02"
        assert entries[0]['lod'] == 1, "First fireball LOD should be 1"
        assert entries[1]['lod'] == 0, "Second fireball LOD should be 0"


def test_fireball_converter_validates_entries():
    """Test fireball converter validates entries properly"""
    fireball_content = """
#Start
$Name: InvalidFireball
  # Missing LOD - should fail validation
#End
"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = FireballTableConverter(temp_path, temp_path)
        
        state = ParseState(lines=fireball_content.split('\n'), filename="test_fireball.tbl")
        entries = converter.parse_table(state)
        
        # Should return empty list due to validation failure
        assert len(entries) == 0, "Should return empty list for invalid entries"


def test_fireball_converter_converts_to_godot_resource():
    """Test fireball converter can convert to Godot resource"""
    fireball_content = """
#Start
$Name: TestExplosion
  $LOD: 1
#End
"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = FireballTableConverter(temp_path, temp_path)
        
        state = ParseState(lines=fireball_content.split('\n'), filename="test_fireball.tbl")
        entries = converter.parse_table(state)
        
        godot_resource = converter.convert_to_godot_resource(entries)
        
        assert 'resource_type' in godot_resource
        assert godot_resource['resource_type'] == 'WCSFireballDatabase'
        assert 'fireballs' in godot_resource
        assert 'fireball_count' in godot_resource
        assert len(godot_resource['fireballs']) == 1
        assert 'TestExplosion' in godot_resource['fireballs']


def test_fireball_converter_handles_invalid_lod():
    """Test fireball converter handles invalid LOD values"""
    fireball_content = """
#Start
$Name: BadExplosion
  $LOD: 99  # Invalid LOD value
#End
"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = FireballTableConverter(temp_path, temp_path)
        
        state = ParseState(lines=fireball_content.split('\n'), filename="test_fireball.tbl")
        entries = converter.parse_table(state)
        
        # Should return empty list due to validation failure
        assert len(entries) == 0, "Should return empty list for invalid LOD values"