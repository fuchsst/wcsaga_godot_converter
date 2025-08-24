from data_converter.table_converters.sounds_table_converter import SoundsTableConverter
from data_converter.table_converters.music_table_converter import MusicTableConverter


def test_sounds_converter_can_parse_content():
    """Test that sounds converter can parse table content"""
    with open('source_assets/wcs_hermes_campaign/hermes_core/sounds.tbl', 'r') as f:
        content = f.read()
    
    converter = SoundsTableConverter('/tmp', '/tmp')
    state = converter._prepare_parse_state(content, 'sounds.tbl')
    
    entries = converter.parse_table(state)
    
    assert len(entries) > 0, "Should parse at least one sound entry"


def test_sounds_converter_converts_to_godot_resource():
    """Test that sounds converter can convert to Godot resource format"""
    with open('source_assets/wcs_hermes_campaign/hermes_core/sounds.tbl', 'r') as f:
        content = f.read()
    
    converter = SoundsTableConverter('/tmp', '/tmp')
    state = converter._prepare_parse_state(content, 'sounds.tbl')
    entries = converter.parse_table(state)
    
    godot_resource = converter.convert_to_godot_resource(entries)
    
    assert 'sounds' in godot_resource
    assert 'sound_count' in godot_resource


def test_music_converter_can_parse_content():
    """Test that music converter can parse table content"""
    with open('source_assets/wcs_hermes_campaign/hermes_core/music.tbl', 'r', encoding='latin-1') as f:
        content = f.read()
    
    converter = MusicTableConverter('/tmp', '/tmp')
    state = converter._prepare_parse_state(content, 'music.tbl')
    
    entries = converter.parse_table(state)
    
    assert len(entries) > 0, "Should parse at least one music entry"


def test_music_converter_converts_to_godot_resource():
    """Test that music converter can convert to Godot resource format"""
    with open('source_assets/wcs_hermes_campaign/hermes_core/music.tbl', 'r', encoding='latin-1') as f:
        content = f.read()
    
    converter = MusicTableConverter('/tmp', '/tmp')
    state = converter._prepare_parse_state(content, 'music.tbl')
    entries = converter.parse_table(state)
    
    godot_resource = converter.convert_to_godot_resource(entries)
    
    assert 'soundtracks' in godot_resource or 'menu_music' in godot_resource