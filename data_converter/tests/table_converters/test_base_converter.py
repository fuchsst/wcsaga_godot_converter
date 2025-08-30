#!/usr/bin/env python3
"""
Unit tests for BaseTableConverter
"""

import tempfile
from pathlib import Path
import pytest

from data_converter.table_converters.base_converter import (
    BaseTableConverter,
    ParseState,
)
from data_converter.core.table_data_structures import TableType


class ConcreteBaseConverter(BaseTableConverter):
    """Concrete implementation of BaseTableConverter for testing purposes"""

    TABLE_TYPE = TableType.SHIPS

    def _init_parse_patterns(self):
        return {}

    def parse_entry(self, state: ParseState):
        return {"name": "Test Entry"}

    def validate_entry(self, entry):
        return True

    def convert_to_godot_resource(self, entries):
        return {"test": "resource"}


def test_base_converter_initialization():
    """Test BaseTableConverter initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ConcreteBaseConverter(source_dir, target_dir)

        # Check that the converter is properly initialized
        assert converter.source_dir == source_dir
        assert converter.target_dir == target_dir
        assert converter.get_table_type() == TableType.SHIPS
        assert (target_dir / "assets" / "tables").exists()


def test_parse_state_functionality():
    """Test ParseState functionality"""
    lines = ["line1", "line2", "line3"]
    state = ParseState(lines=lines, filename="test.tbl")

    assert state.has_more_lines()
    assert state.peek_line() == "line1"
    assert state.next_line() == "line1"
    assert state.peek_line() == "line2"
    assert state.next_line() == "line2"
    assert state.next_line() == "line3"
    assert not state.has_more_lines()
    assert state.peek_line() is None
    assert state.next_line() is None


def test_should_skip_line():
    """Test line skipping functionality"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ConcreteBaseConverter(source_dir, target_dir)
        state = ParseState(lines=[], filename="test.tbl")

        # Test empty line
        assert converter._should_skip_line("", state)

        # Test comment lines
        assert converter._should_skip_line("; This is a comment", state)
        assert converter._should_skip_line("// This is a comment", state)

        # Test regular line
        assert not converter._should_skip_line("$Name: Test", state)

        # Test multi-line comments
        assert not converter._should_skip_line("/* Start of comment", state)
        assert state.in_multiline_comment
        assert converter._should_skip_line("Middle of comment", state)
        assert converter._should_skip_line("End of comment */", state)
        assert not state.in_multiline_comment
        assert not converter._should_skip_line("After comment", state)


def test_parse_value():
    """Test value parsing functionality"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ConcreteBaseConverter(source_dir, target_dir)

        # Test string parsing
        assert converter.parse_value("test string", str) == "test string"
        assert converter.parse_value('"quoted string"', str) == "quoted string"

        # Test integer parsing
        assert converter.parse_value("42", int) == 42
        assert converter.parse_value("0", int) == 0

        # Test float parsing
        assert converter.parse_value("3.14", float) == 3.14
        assert converter.parse_value("0.0", float) == 0.0

        # Test boolean parsing
        assert converter.parse_value("YES", bool)
        assert not converter.parse_value("NO", bool)
        assert converter.parse_value("true", bool)
        assert not converter.parse_value("false", bool)


if __name__ == "__main__":
    pytest.main([__file__])
