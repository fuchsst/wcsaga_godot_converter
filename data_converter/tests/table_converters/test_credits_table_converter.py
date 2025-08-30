"""
Test for Credits table converter
"""

import tempfile
from pathlib import Path

from data_converter.table_converters.credits_table_converter import (
    CreditsTableConverter,
)
from data_converter.table_converters.base_converter import ParseState


def test_credits_converter_can_parse_content():
    """Test credits converter can parse content"""
    credits_content = """
XSTR("Game Developer", -1)
XSTR("John Doe", -1)
XSTR("Lead Programmer", -1)
XSTR("Jane Smith", -1)
XSTR("Art Director", -1)
XSTR("Bob Johnson", -1)
#end
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = CreditsTableConverter(temp_path, temp_path)

        state = ParseState(
            lines=credits_content.split("\n"), filename="test_credits.tbl"
        )
        entries = converter.parse_table(state)

        assert len(entries) == 1, f"Expected 1 credits entry, got {len(entries)}"
        assert "credit_lines" in entries[0], "Credits entry should have credit_lines"
        assert (
            len(entries[0]["credit_lines"]) == 6
        ), f"Expected 6 credit lines, got {len(entries[0]['credit_lines'])}"
        assert (
            entries[0]["credit_lines"][0] == "Game Developer"
        ), "First credit line should be 'Game Developer'"
        assert (
            entries[0]["credit_lines"][1] == "John Doe"
        ), "Second credit line should be 'John Doe'"


def test_credits_converter_handles_empty_content():
    """Test credits converter handles empty content"""
    credits_content = """
# Just comments and empty lines

; This is a comment

#end
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = CreditsTableConverter(temp_path, temp_path)

        state = ParseState(
            lines=credits_content.split("\n"), filename="test_credits.tbl"
        )
        entries = converter.parse_table(state)

        # Should return empty list since no XSTR entries found
        assert (
            len(entries) == 0
        ), f"Expected 0 entries for empty content, got {len(entries)}"


def test_credits_converter_converts_to_godot_resource():
    """Test credits converter can convert to Godot resource"""
    credits_content = """
XSTR("Test Credits", -1)
XSTR("Line 1", -1)
XSTR("Line 2", -1)
#end
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = CreditsTableConverter(temp_path, temp_path)

        state = ParseState(
            lines=credits_content.split("\n"), filename="test_credits.tbl"
        )
        entries = converter.parse_table(state)

        godot_resource = converter.convert_to_godot_resource(entries)

        assert "resource_type" in godot_resource
        assert godot_resource["resource_type"] == "WCSCreditsDatabase"
        assert "credit_lines" in godot_resource
        assert "line_count" in godot_resource
        assert len(godot_resource["credit_lines"]) == 3
        assert godot_resource["line_count"] == 3
        assert godot_resource["credit_lines"][0] == "Test Credits"


def test_credits_converter_handles_missing_end_marker():
    """Test credits converter handles missing #end marker"""
    credits_content = """
XSTR("Test Line", -1)
XSTR("Another Line", -1)
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        converter = CreditsTableConverter(temp_path, temp_path)

        state = ParseState(
            lines=credits_content.split("\n"), filename="test_credits.tbl"
        )
        entries = converter.parse_table(state)

        # Should still parse all XSTR entries even without #end
        assert len(entries) == 1, f"Expected 1 entry, got {len(entries)}"
        assert (
            len(entries[0]["credit_lines"]) == 2
        ), f"Expected 2 credit lines, got {len(entries[0]['credit_lines'])}"
