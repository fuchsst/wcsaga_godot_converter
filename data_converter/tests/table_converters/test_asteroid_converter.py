#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from data_converter.table_converters.asteroid_table_converter import AsteroidTableConverter
from data_converter.table_converters.base_converter import ParseState

def test_asteroid_converter_can_parse_content():
    """Test that asteroid converter can parse table content"""
    with open('source_assets/wcs_hermes_campaign/hermes_core/asteroid.tbl', 'r') as f:
        content = f.read()
    
    converter = AsteroidTableConverter('/tmp', '/tmp')
    state = converter._prepare_parse_state(content, 'asteroid.tbl')
    
    entries = converter.parse_table(state)
    
    assert len(entries) > 0, "Should parse at least one entry"
    
    asteroids = [e for e in entries if e.get('type') == 'asteroid']
    impact_data = [e for e in entries if e.get('type') == 'impact_data']
    
    assert len(asteroids) > 0, "Should find asteroid entries"
    assert len(impact_data) > 0, "Should find impact data entries"


def test_asteroid_converter_converts_to_godot_resource():
    """Test that asteroid converter can convert to Godot resource format"""
    with open('source_assets/wcs_hermes_campaign/hermes_core/asteroid.tbl', 'r') as f:
        content = f.read()
    
    converter = AsteroidTableConverter('/tmp', '/tmp')
    state = converter._prepare_parse_state(content, 'asteroid.tbl')
    entries = converter.parse_table(state)
    
    godot_resource = converter.convert_to_godot_resource(entries)
    
    assert 'individual_resources' in godot_resource
    assert 'impact_data' in godot_resource
    
    individual_resources = godot_resource['individual_resources']
    impact_data = godot_resource['impact_data']
    
    assert len(individual_resources) > 0, "Should convert to individual resources"
    assert 'impact_explosion' in impact_data, "Should have impact explosion data"


def test_asteroid_converter_parses_asteroid_properties():
    """Test that asteroid converter parses specific asteroid properties"""
    with open('source_assets/wcs_hermes_campaign/hermes_core/asteroid.tbl', 'r') as f:
        content = f.read()
    
    converter = AsteroidTableConverter('/tmp', '/tmp')
    state = converter._prepare_parse_state(content, 'asteroid.tbl')
    entries = converter.parse_table(state)
    
    asteroids = [e for e in entries if e.get('type') == 'asteroid']
    
    # Check that first asteroid has expected properties
    first_asteroid = asteroids[0]
    assert 'name' in first_asteroid
    assert 'hitpoints' in first_asteroid
    assert 'pof_file1' in first_asteroid or 'pof_file2' in first_asteroid