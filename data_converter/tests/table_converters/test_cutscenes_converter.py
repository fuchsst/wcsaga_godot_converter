#!/usr/bin/env python3

from data_converter.table_converters.cutscenes_table_converter import CutscenesTableConverter

def test_cutscenes_converter_can_parse_content():
    """Test that cutscenes converter can parse table content"""
    with open('source_assets/wcs_hermes_campaign/hermes_core/cutscenes.tbl', 'r') as f:
        content = f.read()
    
    converter = CutscenesTableConverter('/tmp', '/tmp')
    state = converter._prepare_parse_state(content, 'cutscenes.tbl')
    
    entries = converter.parse_table(state)
    
    assert len(entries) > 0, "Should parse at least one entry"
    assert 'name' in entries[0], "First entry should have a name"
    assert 'filename' in entries[0], "First entry should have a filename"


def test_cutscenes_converter_converts_to_godot_resource():
    """Test that cutscenes converter can convert to Godot resource format"""
    with open('source_assets/wcs_hermes_campaign/hermes_core/cutscenes.tbl', 'r') as f:
        content = f.read()
    
    converter = CutscenesTableConverter('/tmp', '/tmp')
    state = converter._prepare_parse_state(content, 'cutscenes.tbl')
    entries = converter.parse_table(state)
    
    godot_resource = converter.convert_to_godot_resource(entries)
    
    assert 'cutscenes' in godot_resource
    assert len(godot_resource['cutscenes']) > 0, "Should convert to cutscene resources"


def test_cutscenes_converter_parses_cutscene_properties():
    """Test that cutscenes converter parses specific cutscene properties"""
    with open('source_assets/wcs_hermes_campaign/hermes_core/cutscenes.tbl', 'r') as f:
        content = f.read()
    
    converter = CutscenesTableConverter('/tmp', '/tmp')
    state = converter._prepare_parse_state(content, 'cutscenes.tbl')
    entries = converter.parse_table(state)
    
    # Check that first cutscene has expected properties
    first_cutscene = entries[0]
    assert 'name' in first_cutscene
    assert 'filename' in first_cutscene
    assert 'cd' in first_cutscene or 'description' in first_cutscene

