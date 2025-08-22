"""
Tests for the Codebase Analyst Agent
"""

import json
import os
import tempfile
import unittest

from converter.analyst.codebase_analyst import CodebaseAnalyst


class TestCodebaseAnalyst(unittest.TestCase):
    """Test cases for the Codebase Analyst agent."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyst = CodebaseAnalyst()

    def test_analyze_entity_with_empty_files(self):
        """Test analyzing an entity with no source files."""
        result = self.analyst.analyze_entity("TestEntity", [])

        self.assertEqual(result["entity_name"], "TestEntity")
        self.assertEqual(result["source_files"], [])
        self.assertEqual(result["components"]["data"], [])
        self.assertEqual(result["components"]["behavior"], [])
        self.assertEqual(result["components"]["visuals"], [])
        self.assertEqual(result["components"]["physics"], [])

    def test_analyze_entity_with_nonexistent_files(self):
        """Test analyzing an entity with nonexistent source files."""
        result = self.analyst.analyze_entity("TestEntity", ["nonexistent/file.txt"])

        self.assertEqual(result["entity_name"], "TestEntity")
        self.assertEqual(len(result["source_files"]), 1)
        self.assertEqual(result["source_files"][0], "nonexistent/file.txt")

    def test_file_type_detection(self):
        """Test file type detection."""
        self.assertEqual(self.analyst._get_file_type("test.txt"), ".txt")
        self.assertEqual(self.analyst._get_file_type("path/to/file.cpp"), ".cpp")
        self.assertEqual(self.analyst._get_file_type("file"), "")

    def test_caching_mechanism(self):
        """Test that analysis results are cached."""
        # First call
        result1 = self.analyst.analyze_entity("TestEntity", [])

        # Second call with same parameters should return cached result
        result2 = self.analyst.analyze_entity("TestEntity", [])

        self.assertIs(result1, result2)

    def test_parse_cpp_classes(self):
        """Test parsing C++ classes from a file."""
        # Create a temporary C++ file for testing
        with tempfile.NamedTemporaryFile(mode="w", suffix=".cpp", delete=False) as f:
            f.write(
                """
            class Ship {
            public:
                void fly();
            };
            
            class Weapon {
            public:
                void fire();
            };
            """
            )
            temp_file = f.name

        try:
            classes = self.analyst._parse_cpp_classes(temp_file)
            self.assertEqual(len(classes), 2)
            self.assertEqual(classes[0]["name"], "Ship")
            self.assertEqual(classes[1]["name"], "Weapon")
        finally:
            os.unlink(temp_file)

    def test_parse_cpp_includes(self):
        """Test parsing C++ includes from a file."""
        # Create a temporary C++ file for testing
        with tempfile.NamedTemporaryFile(mode="w", suffix=".h", delete=False) as f:
            f.write(
                """
            #include <iostream>
            #include "ship.h"
            #include "weapon.h"
            """
            )
            temp_file = f.name

        try:
            includes = self.analyst._parse_cpp_includes(temp_file)
            self.assertEqual(len(includes), 3)
            self.assertIn("#include <iostream>", includes)
            self.assertIn('#include "ship.h"', includes)
            self.assertIn('#include "weapon.h"', includes)
        finally:
            os.unlink(temp_file)


if __name__ == "__main__":
    unittest.main()
