#!/usr/bin/env python3
"""
Test script for ShipTableConverter with new asset patterns
"""

import sys
import os

# Add the data_converter directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data_converter'))

from table_converters.ship_table_converter import ShipTableConverter
from table_converters.base_converter import ParseState

def test_ship_converter():
    """Test the ship table converter with sample data"""
    
    # Create a temporary converter instance
    converter = ShipTableConverter("/tmp", "/tmp")
    
    # Test data with the new patterns
    test_data = """
$Name: Test Ship
$Short name: Test
$Species: Terran
$POF file: test_ship.pof
$EngineSnd: 126
$Shield_icon: test_icon
$Closeup_pos: 0.0, 0.0, -15.0
$Closeup_zoom: 0.43633
$Thruster01 Radius factor: 0.6
$Thruster02 Length factor: 0.7
$Allowed PBanks: ( "Laser" ) ( "Ion" )
$Allowed SBanks: ( "Spiculum IR" "Javelin HS" )
$Default PBanks: ( "Laser" "Ion" )
$Default SBanks: ( "Javelin HS" "Spiculum IR" )
$SBank Capacity: (20, 20)
$Subsystem: communication, 10.0, 0.0
    $Alt Subsystem Name: Comm
    $Alt Damage Popup Subsystem Name: Communication
$end_multi_text
"""
    
    # Parse the test data
    lines = test_data.strip().split('\n')
    state = ParseState(lines)
    
    entry = converter.parse_entry(state)
    
    if entry:
        print("✓ Successfully parsed ship entry:")
        print(f"  Name: {entry.get('name')}")
        print(f"  POF file: {entry.get('pof_file')}")
        print(f"  EngineSnd: {entry.get('engine_sound')}")
        print(f"  Shield_icon: {entry.get('shield_icon')}")
        print(f"  Closeup_pos: {entry.get('closeup_pos')}")
        print(f"  Closeup_zoom: {entry.get('closeup_zoom')}")
        print(f"  Thruster factors: {entry.get('thruster_radius_factor')}, {entry.get('thruster_length_factor')}")
        print(f"  Allowed PBanks: {entry.get('allowed_pbanks')}")
        print(f"  Allowed SBanks: {entry.get('allowed_sbanks')}")
        print(f"  SBank Capacity: {entry.get('sbank_capacity')}")
        
        # Check asset relationships
        if hasattr(converter, '_asset_registry'):
            print(f"  Asset registry: {converter._asset_registry.get(entry['name'], [])}")
        
        # Validate the entry
        if converter.validate_entry(entry):
            print("✓ Entry validation passed")
        else:
            print("✗ Entry validation failed")
            
    else:
        print("✗ Failed to parse ship entry")

if __name__ == "__main__":
    test_ship_converter()