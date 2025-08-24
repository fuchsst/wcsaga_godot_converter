#!/usr/bin/env python3
"""
Unit tests for the new BSP tree parser based on Rust reference implementation.

Tests comprehensive BSP tree reconstruction with proper node hierarchy,
chunk parsing, and error handling.
"""

import struct
import unittest
from pathlib import Path
from typing import List

from data_converter.pof_parser.pof_bsp_parser import BSPParser, parse_bsp_data, BSPChunkType
from data_converter.pof_parser.pof_types import BSPNode, BSPNodeType, BSPPolygon, Vector3D, BoundingBox


class TestBSPTreeParser(unittest.TestCase):
    """Test comprehensive BSP tree parsing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = BSPParser()

    def test_deffpoints_parsing(self):
        """Test DEFFPOINTS chunk parsing with vertices and normals."""
        # Create DEFFPOINTS chunk
        bsp_data = bytearray()
        
        # DEFFPOINTS header
        bsp_data.extend(struct.pack("<I", BSPChunkType.DEFFPOINTS.value))  # chunk type
        bsp_data.extend(struct.pack("<I", 68))  # chunk size (content only: 4 + 4 + 3*12 + 2*12 = 8 + 36 + 24 = 68)
        
        # DEFFPOINTS content
        bsp_data.extend(struct.pack("<I", 3))   # num vertices
        bsp_data.extend(struct.pack("<I", 2))   # num normals
        
        # Vertex data
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))  # vertex 0
        bsp_data.extend(struct.pack("<fff", 1.0, 0.0, 0.0))  # vertex 1
        bsp_data.extend(struct.pack("<fff", 0.0, 1.0, 0.0))  # vertex 2
        
        # Normal data
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal 0
        bsp_data.extend(struct.pack("<fff", 0.0, 1.0, 0.0))  # normal 1
        
        # Parse the BSP data
        bsp_tree = self.parser.parse_bsp_tree(bytes(bsp_data), 2117)
        
        # Verify parsing stats
        stats = self.parser.get_parsing_stats()
        self.assertEqual(stats["vertex_count"], 3, "Should parse 3 vertices")
        self.assertEqual(stats["normal_count"], 2, "Should parse 2 normals")
        self.assertEqual(stats["error_count"], 0, "Should have no parsing errors")
        
        # Tree should be EMPTY since we only have DEFFPOINTS without tree structure
        self.assertEqual(bsp_tree.node_type, BSPNodeType.EMPTY, "Should return EMPTY node for DEFFPOINTS-only data")

    def test_tmappoly_parsing(self):
        """Test TMAPPOLY chunk parsing with texture coordinates."""
        # Create complete BSP data with DEFFPOINTS and TMAPPOLY
        bsp_data = bytearray()
        
        # DEFFPOINTS chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.DEFFPOINTS.value))
        bsp_data.extend(struct.pack("<I", 63))  # chunk size (content only: 4 + 4 + 3*12 + 1*12 = 8 + 36 + 12 = 56)
        bsp_data.extend(struct.pack("<I", 3))   # num vertices
        bsp_data.extend(struct.pack("<I", 1))   # num normals
        
        # Vertices
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 1.0, 0.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 0.0, 1.0, 0.0))
        
        # Normals
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))
        
        # TMAPPOLY chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.TMAPPOLY.value))
        bsp_data.extend(struct.pack("<I", 64))  # chunk size (content only: 12 + 12 + 4 + 4 + 3*4 + 4 + 3*8 = 24 + 4 + 4 + 12 + 4 + 24 = 72)
        
        # Polygon data
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal
        bsp_data.extend(struct.pack("<fff", 0.5, 0.5, 0.0))  # center
        bsp_data.extend(struct.pack("<f", 1.0))              # radius
        bsp_data.extend(struct.pack("<I", 3))                # num vertices
        
        # Vertex indices
        bsp_data.extend(struct.pack("<I", 0))
        bsp_data.extend(struct.pack("<I", 1))
        bsp_data.extend(struct.pack("<I", 2))
        
        # Texture index
        bsp_data.extend(struct.pack("<I", 5))  # texture index
        
        # UV coordinates
        bsp_data.extend(struct.pack("<ff", 0.0, 0.0))  # uv0
        bsp_data.extend(struct.pack("<ff", 1.0, 0.0))  # uv1
        bsp_data.extend(struct.pack("<ff", 0.0, 1.0))  # uv2
        
        # Parse the BSP data
        bsp_tree = self.parser.parse_bsp_tree(bytes(bsp_data), 2117)
        
        # Should parse successfully
        self.assertIsNotNone(bsp_tree, "Should parse TMAPPOLY data successfully")
        stats = self.parser.get_parsing_stats()
        self.assertEqual(stats["error_count"], 0, "Should have no parsing errors")

    def test_boundbox_with_polygons(self):
        """Test BOUNDBOX chunk with polygon list."""
        bsp_data = bytearray()
        
        # DEFFPOINTS chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.DEFFPOINTS.value))
        bsp_data.extend(struct.pack("<I", 56))  # chunk size (content only: 4 + 4 + 3*12 + 1*12 = 8 + 36 + 12 = 56)
        bsp_data.extend(struct.pack("<I", 3))   # num vertices
        bsp_data.extend(struct.pack("<I", 1))   # num normals
        
        # Vertices and normals
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 1.0, 0.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 0.0, 1.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))
        
        # BOUNDBOX chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.BOUNDBOX.value))
        bsp_data.extend(struct.pack("<I", 24))  # chunk size (content only: 6*4 = 24)
        
        # Bounding box
        bsp_data.extend(struct.pack("<fff", -1.0, -1.0, -1.0))  # min
        bsp_data.extend(struct.pack("<fff", 1.0, 1.0, 1.0))     # max
        
        # TMAPPOLY chunk (polygon in the box)
        bsp_data.extend(struct.pack("<I", BSPChunkType.TMAPPOLY.value))
        bsp_data.extend(struct.pack("<I", 72))  # chunk size (content only: 12 + 12 + 4 + 4 + 3*4 + 4 + 3*8 = 24 + 4 + 4 + 12 + 4 + 24 = 72)
        
        # Polygon data
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal
        bsp_data.extend(struct.pack("<fff", 0.5, 0.5, 0.0))  # center
        bsp_data.extend(struct.pack("<f", 1.0))              # radius
        bsp_data.extend(struct.pack("<I", 3))                # num vertices
        
        # Vertex indices, texture, UVs
        bsp_data.extend(struct.pack("<I", 0))
        bsp_data.extend(struct.pack("<I", 1))
        bsp_data.extend(struct.pack("<I", 2))
        bsp_data.extend(struct.pack("<I", 5))  # texture
        bsp_data.extend(struct.pack("<ff", 0.0, 0.0))
        bsp_data.extend(struct.pack("<ff", 1.0, 0.0))
        bsp_data.extend(struct.pack("<ff", 0.0, 1.0))
        
        # ENDOFBRANCH to terminate polygon list
        bsp_data.extend(struct.pack("<I", BSPChunkType.ENDOFBRANCH.value))
        bsp_data.extend(struct.pack("<I", 0))  # chunk size
        
        # Parse the BSP data
        bsp_tree = self.parser.parse_bsp_tree(bytes(bsp_data), 2117)
        
        # Should parse successfully with BOUNDBOX structure
        self.assertIsNotNone(bsp_tree, "Should parse BOUNDBOX data successfully")
        self.assertEqual(bsp_tree.node_type, BSPNodeType.LEAF, "Should create LEAF node")
        self.assertIsNotNone(bsp_tree.bbox, "Should have bounding box")
        self.assertGreater(len(bsp_tree.polygons), 0, "Should have polygons")

    def test_empty_data(self):
        """Test parsing empty BSP data."""
        bsp_tree = self.parser.parse_bsp_tree(b"", 2117)
        self.assertIsNone(bsp_tree, "Should return None for empty data")
        
        stats = self.parser.get_parsing_stats()
        self.assertEqual(stats["error_count"], 0, "Should handle empty data gracefully")

    def test_invalid_chunk_order(self):
        """Test parsing with invalid chunk order (missing DEFFPOINTS)."""
        bsp_data = bytearray()
        
        # Start with TMAPPOLY without DEFFPOINTS (invalid)
        bsp_data.extend(struct.pack("<I", BSPChunkType.TMAPPOLY.value))
        bsp_data.extend(struct.pack("<I", 72))  # chunk size (content only: 12 + 12 + 4 + 4 + 3*4 + 4 + 3*8 = 24 + 4 + 4 + 12 + 4 + 24 = 72)
        
        # Minimal polygon data
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))
        bsp_data.extend(struct.pack("<fff", 0.5, 0.5, 0.0))
        bsp_data.extend(struct.pack("<f", 1.0))
        bsp_data.extend(struct.pack("<I", 3))
        bsp_data.extend(struct.pack("<I", 0))
        bsp_data.extend(struct.pack("<I", 1))
        bsp_data.extend(struct.pack("<I", 2))
        bsp_data.extend(struct.pack("<I", 5))
        bsp_data.extend(struct.pack("<ff", 0.0, 0.0))
        bsp_data.extend(struct.pack("<ff", 1.0, 0.0))
        bsp_data.extend(struct.pack("<ff", 0.0, 1.0))
        
        bsp_tree = self.parser.parse_bsp_tree(bytes(bsp_data), 2117)
        
        # Should fail gracefully
        self.assertIsNone(bsp_tree, "Should return None for invalid chunk order")
        stats = self.parser.get_parsing_stats()
        self.assertGreater(stats["error_count"], 0, "Should record parsing errors")

    def test_parse_bsp_data_function(self):
        """Test the main parse_bsp_data function interface."""
        # Create simple BSP data
        bsp_data = bytearray()
        
        # DEFFPOINTS chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.DEFFPOINTS.value))
        bsp_data.extend(struct.pack("<I", 56))  # chunk size (content only: 4 + 4 + 3*12 + 1*12 = 8 + 36 + 12 = 56)
        bsp_data.extend(struct.pack("<I", 3))   # num vertices
        bsp_data.extend(struct.pack("<I", 1))   # num normals
        
        # Vertices and normals
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 1.0, 0.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 0.0, 1.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))
        
        # TMAPPOLY chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.TMAPPOLY.value))
        bsp_data.extend(struct.pack("<I", 72))  # chunk size (content only: 12 + 12 + 4 + 4 + 3*4 + 4 + 3*8 = 24 + 4 + 4 + 12 + 4 + 24 = 72)
        
        # Polygon data
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))
        bsp_data.extend(struct.pack("<fff", 0.5, 0.5, 0.0))
        bsp_data.extend(struct.pack("<f", 1.0))
        bsp_data.extend(struct.pack("<I", 3))
        bsp_data.extend(struct.pack("<I", 0))
        bsp_data.extend(struct.pack("<I", 1))
        bsp_data.extend(struct.pack("<I", 2))
        bsp_data.extend(struct.pack("<I", 5))
        bsp_data.extend(struct.pack("<ff", 0.0, 0.0))
        bsp_data.extend(struct.pack("<ff", 1.0, 0.0))
        bsp_data.extend(struct.pack("<ff", 0.0, 1.0))
        
        # Parse using the main function
        result = parse_bsp_data(bytes(bsp_data), 2117)
        
        # Should return structured data
        self.assertIsNotNone(result, "Should return result dictionary")
        self.assertIn("bsp_tree", result, "Should contain BSP tree")
        self.assertIn("vertices", result, "Should contain vertices")
        self.assertIn("normals", result, "Should contain normals")
        self.assertIn("polygons", result, "Should contain polygons")
        self.assertIn("parsing_stats", result, "Should contain parsing stats")


def create_test_bsp_data() -> bytes:
    """Create test BSP data for integration testing."""
    bsp_data = bytearray()
    
    # DEFFPOINTS chunk
    bsp_data.extend(struct.pack("<I", BSPChunkType.DEFFPOINTS.value))
    bsp_data.extend(struct.pack("<I", 80))  # chunk size (content only: 4 + 4 + 4*12 + 2*12 = 8 + 48 + 24 = 80)
    bsp_data.extend(struct.pack("<I", 4))   # num vertices
    bsp_data.extend(struct.pack("<I", 2))   # num normals
    
    # Vertices
    bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))
    bsp_data.extend(struct.pack("<fff", 1.0, 0.0, 0.0))
    bsp_data.extend(struct.pack("<fff", 0.0, 1.0, 0.0))
    bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))
    
    # Normals
    bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))
    bsp_data.extend(struct.pack("<fff", 0.0, 1.0, 0.0))
    
    # BOUNDBOX chunk with polygon
    bsp_data.extend(struct.pack("<I", BSPChunkType.BOUNDBOX.value))
    bsp_data.extend(struct.pack("<I", 24))  # chunk size (content only: 6*4 = 24)
    
    # Bounding box
    bsp_data.extend(struct.pack("<fff", -1.0, -1.0, -1.0))
    bsp_data.extend(struct.pack("<fff", 1.0, 1.0, 1.0))
    
    # TMAPPOLY chunk
    bsp_data.extend(struct.pack("<I", BSPChunkType.TMAPPOLY.value))
    bsp_data.extend(struct.pack("<I", 72))  # chunk size (content only: 12 + 12 + 4 + 4 + 3*4 + 4 + 3*8 = 24 + 4 + 4 + 12 + 4 + 24 = 72)
    
    # Polygon data
    bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))
    bsp_data.extend(struct.pack("<fff", 0.5, 0.5, 0.0))
    bsp_data.extend(struct.pack("<f", 1.0))
    bsp_data.extend(struct.pack("<I", 3))
    
    # Vertex indices
    bsp_data.extend(struct.pack("<I", 0))
    bsp_data.extend(struct.pack("<I", 1))
    bsp_data.extend(struct.pack("<I", 2))
    
    # Texture and UVs
    bsp_data.extend(struct.pack("<I", 3))  # texture index
    bsp_data.extend(struct.pack("<ff", 0.0, 0.0))
    bsp_data.extend(struct.pack("<ff", 1.0, 0.0))
    bsp_data.extend(struct.pack("<ff", 0.0, 1.0))
    
    # ENDOFBRANCH
    bsp_data.extend(struct.pack("<I", BSPChunkType.ENDOFBRANCH.value))
    bsp_data.extend(struct.pack("<I", 0))
    
    return bytes(bsp_data)


if __name__ == "__main__":
    unittest.main()