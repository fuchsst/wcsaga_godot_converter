"""
Test for AI table converter
"""

import tempfile
from pathlib import Path

from data_converter.table_converters.ai_table_converter import AITableConverter
from data_converter.table_converters.base_converter import ParseState


def test_ai_converter_can_parse_content():
    """Test AI converter can parse content"""
    ai_content = """
#AI Classes

$Name: Default
  $Primary Weapon Delay: 0.5, 0.4, 0.3, 0.2, 0.1
  $Secondary Weapon Delay: 1.0, 0.8, 0.6, 0.4, 0.2
  $Use Countermeasures: YES
  $Evade Missiles: YES
$end

$Name: Aggressive
  $Primary Weapon Delay: 0.4, 0.3, 0.2, 0.1, 0.05
  $Secondary Weapon Delay: 0.8, 0.6, 0.4, 0.2, 0.1
  $Use Countermeasures: NO
  $Evade Missiles: NO
$end
#End
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = AITableConverter(temp_path, temp_path)

        state = ParseState(lines=ai_content.split("\n"), filename="test_ai.tbl")
        entries = converter.parse_table(state)

        assert len(entries) == 2, f"Expected 2 AI class entries, got {len(entries)}"
        assert entries[0]["name"] == "Default", "First AI class should be Default"
        assert (
            entries[1]["name"] == "Aggressive"
        ), "Second AI class should be Aggressive"
        assert "properties" in entries[0], "AI class should have properties"
        assert "flags" in entries[0], "AI class should have flags"


def test_ai_converter_validates_entries():
    """Test AI converter validates entries properly"""
    ai_content = """
#AI Classes

$Name: Invalid
  $Primary Weapon Delay: 0.5, 0.4  ; Missing values - should fail validation
$end
#End
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = AITableConverter(temp_path, temp_path)

        state = ParseState(lines=ai_content.split("\n"), filename="test_ai.tbl")
        entries = converter.parse_table(state)

        # Should return empty list due to validation failure
        assert len(entries) == 0, "Should return empty list for invalid entries"


def test_ai_converter_converts_to_godot_resource():
    """Test AI converter can convert to Godot resource"""
    ai_content = """
#AI Classes

$Name: TestAI
  $Primary Weapon Delay: 0.5, 0.4, 0.3, 0.2, 0.1
  $Secondary Weapon Delay: 1.0, 0.8, 0.6, 0.4, 0.2
  $Use Countermeasures: YES
$end
#End
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = AITableConverter(temp_path, temp_path)

        state = ParseState(lines=ai_content.split("\n"), filename="test_ai.tbl")
        entries = converter.parse_table(state)

        godot_resource = converter.convert_to_godot_resource(entries)

        assert "resource_type" in godot_resource
        assert godot_resource["resource_type"] == "WCSAIDatabase"
        assert "ai_classes" in godot_resource
        assert "ai_class_count" in godot_resource
        assert len(godot_resource["ai_classes"]) == 1
        assert "TestAI" in godot_resource["ai_classes"]


def test_ai_converter_handles_skill_levels():
    """Test AI converter properly handles skill levels"""
    ai_content = """
#AI Classes

$Name: TestAI
  $Primary Weapon Delay: 0.5, 0.4, 0.3, 0.2, 0.1
$end
#End
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = AITableConverter(temp_path, temp_path)

        state = ParseState(lines=ai_content.split("\n"), filename="test_ai.tbl")
        entries = converter.parse_table(state)

        godot_resource = converter.convert_to_godot_resource(entries)
        ai_class = godot_resource["ai_classes"]["TestAI"]

        # Should have skill level properties
        assert "primary_weapon_delay_trainee" in ai_class
        assert "primary_weapon_delay_rookie" in ai_class
        assert "primary_weapon_delay_hotshot" in ai_class
        assert "primary_weapon_delay_ace" in ai_class
        assert "primary_weapon_delay_insane" in ai_class
