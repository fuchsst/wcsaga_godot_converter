"""
Test for AI Profiles table converter
"""

import tempfile
from pathlib import Path

from data_converter.table_converters.ai_profiles_table_converter import (
    AIProfilesTableConverter,
)
from data_converter.table_converters.base_converter import ParseState


def test_ai_profiles_converter_can_parse_content():
    """Test AI profiles converter can parse content"""
    ai_profiles_content = """
#AI Profiles

$Profile Name: SAGA RETAIL
  $Default Profile: SAGA RETAIL
  $Primary Weapon Delay: 0.5, 0.4, 0.3, 0.2, 0.1
  $Secondary Weapon Delay: 1.0, 0.8, 0.6, 0.4, 0.2
  $Use Countermeasures: YES
  $Evade Missiles: YES

$Profile Name: TEST PROFILE
  $Default Profile: SAGA RETAIL
  $Primary Weapon Delay: 0.6, 0.5, 0.4, 0.3, 0.2
  $Secondary Weapon Delay: 1.2, 1.0, 0.8, 0.6, 0.4
  $Use Countermeasures: NO
  $Evade Missiles: NO
#End
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = AIProfilesTableConverter(temp_path, temp_path)

        state = ParseState(
            lines=ai_profiles_content.split("\n"), filename="test_ai_profiles.tbl"
        )
        entries = converter.parse_table(state)

        assert len(entries) == 2, f"Expected 2 AI profile entries, got {len(entries)}"
        assert (
            entries[0]["name"] == "SAGA RETAIL"
        ), "First profile should be SAGA RETAIL"
        assert (
            entries[1]["name"] == "TEST PROFILE"
        ), "Second profile should be TEST PROFILE"
        assert (
            "difficulty_scales" in entries[0]
        ), "Profile should have difficulty scales"
        assert "flags" in entries[0], "Profile should have flags"


def test_ai_profiles_converter_validates_entries():
    """Test AI profiles converter validates entries properly"""
    ai_profiles_content = """
#AI Profiles

$Profile Name: INVALID PROFILE
  $Primary Weapon Delay: 0.5, 0.4  ; Missing values - should fail validation
#End
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = AIProfilesTableConverter(temp_path, temp_path)

        state = ParseState(
            lines=ai_profiles_content.split("\n"), filename="test_ai_profiles.tbl"
        )
        entries = converter.parse_table(state)

        # Should return empty list due to validation failure
        assert len(entries) == 0, "Should return empty list for invalid entries"


def test_ai_profiles_converter_converts_to_godot_resource():
    """Test AI profiles converter can convert to Godot resource"""
    ai_profiles_content = """
#AI Profiles

$Profile Name: TEST PROFILE
  $Default Profile: SAGA RETAIL
  $Primary Weapon Delay: 0.5, 0.4, 0.3, 0.2, 0.1
  $Secondary Weapon Delay: 1.0, 0.8, 0.6, 0.4, 0.2
  $Use Countermeasures: YES
#End
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = AIProfilesTableConverter(temp_path, temp_path)

        state = ParseState(
            lines=ai_profiles_content.split("\n"), filename="test_ai_profiles.tbl"
        )
        entries = converter.parse_table(state)

        godot_resource = converter.convert_to_godot_resource(entries)

        assert "resource_type" in godot_resource
        assert godot_resource["resource_type"] == "WCSAIProfileDatabase"
        assert "profiles" in godot_resource
        assert "profile_count" in godot_resource
        assert "default_profile" in godot_resource
        assert len(godot_resource["profiles"]) == 1
        assert "TEST PROFILE" in godot_resource["profiles"]


def test_ai_profiles_converter_handles_skill_levels():
    """Test AI profiles converter properly handles skill levels"""
    ai_profiles_content = """
#AI Profiles

$Profile Name: TEST PROFILE
  $Primary Weapon Delay: 0.5, 0.4, 0.3, 0.2, 0.1
#End
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = AIProfilesTableConverter(temp_path, temp_path)

        state = ParseState(
            lines=ai_profiles_content.split("\n"), filename="test_ai_profiles.tbl"
        )
        entries = converter.parse_table(state)

        godot_resource = converter.convert_to_godot_resource(entries)
        profile = godot_resource["profiles"]["TEST PROFILE"]

        # Should have skill level properties
        assert "primary_weapon_delay_very_easy" in profile
        assert "primary_weapon_delay_easy" in profile
        assert "primary_weapon_delay_medium" in profile
        assert "primary_weapon_delay_hard" in profile
        assert "primary_weapon_delay_insane" in profile
