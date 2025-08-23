#!/usr/bin/env python3
"""
Simple BSP Parser Test

Test basic BSP parsing functionality.
"""

import struct
import tempfile
import unittest
from pathlib import Path

from data_converter.pof_parser.pof_bsp_parser import BSPParser
from data_converter.pof_parser.pof_enhanced_types import BSPNode, BSPNodeType, BSPPolygon, Vector3D


class TestSimpleBSPParsing(unittest.TestCase):
    """Test simple BSP parsing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = BSPParser()

    def test_simple_deffpoints(self):
        """Test parsing simple DEFFPOINTS chunk."""
        # Create simple DEFFPOINTS chunk
        bsp_data = bytearray()
        
        # DEFFPOINTS header
        bsp_data.extend(struct.pack("<I", 1))  # chunk type (DEFFPOINTS)
        bsp_data.extend(struct.pack("<I", 32)) # chunk size (4+4+12+12 = 32)
        bsp_data.extend(struct.pack("<I", 1))  # num vertices
        bsp_data.extend(struct.pack("<I", 1))  # num normals
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))  # vertex (12 bytes)
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal (12 bytes)
        
        result = self.parser.parse_bsp_tree(bytes(bsp_data), 2117)
        
        # Should return empty node since there's no tree structure after DEFFPOINTS
        self.assertIsNotNone(result)
        self.assertEqual(result.node_type, BSPNodeType.EMPTY)

    def test_simple_polygon(self):
        """Test parsing simple polygon data."""
        # Create BSP data with DEFFPOINTS and simple polygon
        bsp_data = bytearray()
        
        # DEFFPOINTS chunk
        bsp_data.extend(struct.pack("<I", 1))   # chunk type (DEFFPOINTS)
        bsp_data.extend(struct.pack("<I", 56))  # chunk size (4+4+3*12+1*12 = 56)
        bsp_data.extend(struct.pack("<I", 3))   # num vertices
        bsp_data.extend(struct.pack("<I", 1))   # num normals
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))  # vertex 0
        bsp_data.extend(struct.pack("<fff", 1.0, 0.0, 0.0))  # vertex 1
        bsp_data.extend(struct.pack("<fff", 0.0, 1.0, 0.0))  # vertex 2
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal
        
        # BOUNDBOX chunk
        bsp_data.extend(struct.pack("<I", 5))   # chunk type (BOUNDBOX)
        bsp_data.extend(struct.pack("<I", 24))  # chunk size (6*4 = 24)
        bsp_data.extend(struct.pack("<fff", -1.0, -1.0, -1.0))  # min
        bsp_data.extend(struct.pack("<fff", 1.0, 1.0, 1.0))     # max
        
        # TMAPPOLY chunk
        bsp_data.extend(struct.pack("<I", 3))   # chunk type (TMAPPOLY)
        bsp_data.extend(struct.pack("<I", 72))  # chunk size
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))     # normal (12 bytes)
        bsp_data.extend(struct.pack("<fff", 0.33, 0.33, 0.0))   # center (12 bytes)
        bsp_data.extend(struct.pack("<f", 0.5))                 # radius (4 bytes)
        bsp_data.extend(struct.pack("<I", 3))                   # num vertices (4 bytes)
        bsp_data.extend(struct.pack("<H", 0))                   # vertex 0 index (2 bytes)
        bsp_data.extend(struct.pack("<H", 1))                   # vertex 1 index (2 bytes)
        bsp_data.extend(struct.pack("<H", 2))                   # vertex 2 index (2 bytes)
        # Pad to 4-byte boundary
        bsp_data.extend(struct.pack("<H", 0))                   # padding (2 bytes)
        bsp_data.extend(struct.pack("<I", 0))                   # texture index (4 bytes)
        bsp_data.extend(struct.pack("<ff", 0.0, 1.0))           # uv0 (8 bytes)
        bsp_data.extend(struct.pack("<ff", 1.0, 1.0))           # uv1 (8 bytes)
        bsp_data.extend(struct.pack("<ff", 0.0, 0.0))           # uv2 (8 bytes)
        
        # ENDOFBRANCH
        bsp_data.extend(struct.pack("<I", 0))   # chunk type (ENDOFBRANCH)
        bsp_data.extend(struct.pack("<I", 0))   # chunk size
        
        result = self.parser.parse_bsp_tree(bytes(bsp_data), 2117)
        
        # Should parse successfully
        self.assertIsNotNone(result)
        # Note: This might return EMPTY because we don't have a complete BSP structure
        # but it should at least not crash


def run_tests():
    """Run simple BSP parsing tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSimpleBSPParsing))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)