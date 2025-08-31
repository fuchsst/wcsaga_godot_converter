#!/usr/bin/env python3
"""
Test for Lightning table converter
"""

import tempfile
from pathlib import Path

from data_converter.table_converters.lightning_table_converter import (
    LightningTableConverter,
)
from data_converter.table_converters.base_converter import ParseState


def test_lightning_converter_can_parse_content():
    """Test lightning converter can parse content"""
    lightning_content = """
#Bolts begin
$Bolt:		b_standard
	+b_scale:					0.5
	+b_shrink:					0.3
	+b_poly_pct:				0.002
	+b_rand:						0.24
	+b_add:						2.0
	+b_strikes:					2
	+b_lifetime:				280
	+b_noise:					0.015
	+b_emp:						0.0 0.0
	+b_texture:					lightning
	+b_glow:						beam-dblue
	+b_bright:					0.3
#Bolts end

#Storms begin
$Storm:							s_standard
	+bolt:						b_standard
	+bolt:						b_standard
	+bolt:						b_red
	+flavor:						0.0 0.0 0.0
	+random_freq:				1500 1750
	+random_count:				1 2
#Storms end
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = LightningTableConverter(temp_path, temp_path)

        state = ParseState(
            lines=lightning_content.split("\n"), filename="test_lightning.tbl"
        )
        entries = converter.parse_table(state)

        assert len(entries) == 2, f"Expected 2 entries, got {len(entries)}"
        
        # Find the bolt entry
        bolt_entries = [e for e in entries if "scale" in e]
        storm_entries = [e for e in entries if "bolts" in e]
        
        assert len(bolt_entries) == 1, "Should have 1 bolt entry"
        assert len(storm_entries) == 1, "Should have 1 storm entry"
        
        bolt = bolt_entries[0]
        storm = storm_entries[0]
        
        assert bolt["name"] == "b_standard"
        assert bolt["scale"] == 0.5
        assert bolt["shrink"] == 0.3
        assert bolt["poly_pct"] == 0.002
        assert bolt["rand"] == 0.24
        assert bolt["add"] == 2.0
        assert bolt["strikes"] == 2
        assert bolt["lifetime"] == 280
        assert bolt["noise"] == 0.015
        assert bolt["emp"] == [0.0, 0.0]
        assert bolt["texture"] == "lightning"
        assert bolt["glow"] == "beam-dblue"
        assert bolt["bright"] == 0.3
        
        assert storm["name"] == "s_standard"
        assert "b_standard" in storm["bolts"]
        assert "b_red" in storm["bolts"]
        assert storm["flavor"] == [0.0, 0.0, 0.0]
        assert storm["random_freq"] == [1500, 1750]
        assert storm["random_count"] == [1, 2]


def test_lightning_converter_validates_entries():
    """Test lightning converter validates entries properly"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = LightningTableConverter(temp_path, temp_path)

        # Valid entry with name
        valid_entry = {"name": "test_bolt", "scale": 0.5}
        assert converter.validate_entry(valid_entry) == True

        # Invalid entry - missing name
        invalid_entry = {"scale": 0.5}
        assert converter.validate_entry(invalid_entry) == False


def test_lightning_converter_converts_to_godot_resource():
    """Test lightning converter can convert to Godot resource"""
    entries = [
        {
            "name": "test_bolt",
            "scale": 0.5,
            "shrink": 0.3,
            "poly_pct": 0.002,
            "rand": 0.24,
            "add": 2.0,
            "strikes": 2,
            "lifetime": 280,
            "noise": 0.015,
            "emp": [0.0, 0.0],
            "texture": "lightning",
            "glow": "beam-dblue",
            "bright": 0.3
        },
        {
            "name": "test_storm",
            "bolts": ["test_bolt"],
            "flavor": [0.0, 0.0, 0.0],
            "random_freq": [1500, 1750],
            "random_count": [1, 2]
        }
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = LightningTableConverter(temp_path, temp_path)

        godot_resource = converter.convert_to_godot_resource(entries)

        assert "resource_type" in godot_resource
        assert godot_resource["resource_type"] == "WCSLightningDatabase"
        assert "bolts" in godot_resource
        assert "storms" in godot_resource
        assert len(godot_resource["bolts"]) == 1
        assert len(godot_resource["storms"]) == 1
        assert "test_bolt" in godot_resource["bolts"]
        assert "test_storm" in godot_resource["storms"]


def test_lightning_converter_with_actual_file():
    """Test lightning converter with actual source content"""
    # Read the actual lightning.tbl file content
    with open("/home/fuchsst/projects/personal/wcsaga_godot_converter/source_assets/wcs_hermes_campaign/hermes_core/lightning.tbl", "r") as f:
        lightning_content = f.read()

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = LightningTableConverter(temp_path, temp_path)

        state = ParseState(
            lines=lightning_content.split("\n"), filename="lightning.tbl"
        )
        entries = converter.parse_table(state)

        # Should have multiple bolt and storm entries
        bolt_entries = [e for e in entries if "scale" in e]
        storm_entries = [e for e in entries if "bolts" in e]
        
        assert len(bolt_entries) > 0, "Should have bolt entries"
        assert len(storm_entries) > 0, "Should have storm entries"
        
        # Check that we have the expected bolt types
        bolt_names = [b["name"] for b in bolt_entries]
        expected_bolts = ["b_standard", "b_red", "b_green", "b_emp"]
        for expected_bolt in expected_bolts:
            assert expected_bolt in bolt_names, f"Should have {expected_bolt} bolt"
        
        # Check that we have the expected storm types
        storm_names = [s["name"] for s in storm_entries]
        expected_storms = ["s_standard", "s_active", "s_emp", "s_medium"]
        for expected_storm in expected_storms:
            assert expected_storm in storm_names, f"Should have {expected_storm} storm"