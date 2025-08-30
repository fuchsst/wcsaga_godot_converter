import pytest
import os
from data_converter.table_converters.scripting_table_converter import (
    ScriptingTableConverter,
)


class TestScriptingTableConverter:

    @pytest.fixture
    def converter(self):
        return ScriptingTableConverter("/tmp", "/tmp")

    @pytest.fixture
    def scripting_content(self):
        script_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "source_assets",
            "wcs_hermes_campaign",
            "hermes_core",
            "scripting.tbl",
        )
        with open(script_path, "r") as f:
            return f.read()

    def test_parse_scripting_table(self, converter, scripting_content):
        """Test parsing of scripting.tbl file"""
        state = converter._prepare_parse_state(scripting_content, "scripting.tbl")
        entries = converter.parse_table(state)

        assert (
            len(entries) >= 2
        ), f"Expected at least 2 script hooks, got {len(entries)}"

        hooks = [entry["hook"] for entry in entries]
        assert "GameInit" in hooks, "GameInit hook not found"
        assert "HUD" in hooks, "HUD hook not found"

        for entry in entries:
            assert "hook" in entry, "Hook field missing from entry"
            assert "script" in entry, "Script field missing from entry"
            assert len(entry["script"]) > 0, f"Empty script for hook {entry['hook']}"

    def test_convert_to_godot_resource(self, converter, scripting_content):
        """Test conversion to Godot resource format"""
        state = converter._prepare_parse_state(scripting_content, "scripting.tbl")
        entries = converter.parse_table(state)
        godot_resource = converter.convert_to_godot_resource(entries)

        assert godot_resource["resource_type"] == "WCSScriptingDatabase"
        assert "hooks" in godot_resource
        assert "hook_count" in godot_resource
        assert godot_resource["hook_count"] == len(entries)

        hooks = godot_resource["hooks"]
        assert len(hooks) == len(entries)

        for hook_name, script_content in hooks.items():
            assert len(script_content) > 0, f"Empty script content for hook {hook_name}"

    def test_validate_entries(self, converter, scripting_content):
        """Test entry validation"""
        state = converter._prepare_parse_state(scripting_content, "scripting.tbl")
        entries = converter.parse_table(state)

        for entry in entries:
            assert converter.validate_entry(
                entry
            ), f"Entry validation failed for hook {entry['hook']}"
