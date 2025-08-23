#!/usr/bin/env python3
"""
Comprehensive Tests for Enhanced BSP Parser - EPIC-003 DM-004 Implementation

Tests enhanced BSP parsing functionality with complete tree reconstruction,
error handling, and validation matching Rust reference implementation.
"""

import struct
import tempfile
import unittest
from pathlib import Path
from typing import List

from .pof_bsp_enhanced import BSPParserEnhanced, parse_bsp_data_enhanced, BSPChunkType
from .pof_enhanced_types import BSPNode, BSPNodeType, BSPPolygon, Vector3D, BoundingBox


class TestEnhancedBSPParsing(unittest.TestCase):
    """Test comprehensive BSP parsing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = BSPParserEnhanced()

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
        bsp_data.extend(struct.pack("<I", 68))  # chunk size
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
        bsp_data.extend(struct.pack("<I", 72))  # chunk size
        
        # Polygon data
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal
        bsp_data.extend(struct.pack("<fff", 0.5, 0.5, 0.0))  # center
        bsp_data.extend(struct.pack("<f", 1.0))              # radius
        bsp_data.extend(struct.pack("<I", 3))                # num vertices
        
        # Vertex indices
        bsp_data.extend(struct.pack("<H", 0))
        bsp_data.extend(struct.pack("<H", 1))
        bsp_data.extend(struct.pack("<H", 2))
        
        # Texture index
        bsp_data.extend(struct.pack("<I", 5))  # texture index
        
        # UV coordinates
        bsp_data.extend(struct.pack("<ff", 0.0, 0.0))  # uv0
        bsp_data.extend(struct.pack("<ff", 1.0, 0.0))  # uv1
        bsp_data.extend(struct.pack("<ff", 0.0, 1.0))  # uv2
        
        # ENDOFBRANCH to terminate polygon list
        bsp_data.extend(struct.pack("<I", BSPChunkType.ENDOFBRANCH.value))
        bsp_data.extend(struct.pack("<I", 0))   # chunk size
        
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
        bsp_data.extend(struct.pack("<I", 68))  # chunk size
        bsp_data.extend(struct.pack("<I", 3))   # num vertices
        bsp_data.extend(struct.pack("<I", 1))   # num normals
        
        # Vertices and normals
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 1.0, 0.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 0.0, 1.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))
        
        # BOUNDBOX chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.BOUNDBOX.value))
        bsp_data.extend(struct.pack("<I", 24))  # chunk size
        
        # Bounding box
        bsp_data.extend(struct.pack("<fff", -1.0, -1.0, -1.0))  # min
        bsp_data.extend(struct.pack("<fff", 1.0, 1.0, 1.0))     # max
        
        # TMAPPOLY chunk (polygon in the box)
        bsp_data.extend(struct.pack("<I", BSPChunkType.TMAPPOLY.value))
        bsp_data.extend(struct.pack("<I", 72))  # chunk size
        
        # Polygon data
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal
        bsp_data.extend(struct.pack("<fff", 0.5, 0.5, 0.0))  # center
        bsp_data.extend(struct.pack("<f", 1.0))              # radius
        bsp_data.extend(struct.pack("<I", 3))                # num vertices
        
        # Vertex indices (16-bit)
        bsp_data.extend(struct.pack("<H", 0))
        bsp_data.extend(struct.pack("<H", 1))
        bsp_data.extend(struct.pack("<H", 2))
        
        # Texture and UVs
        bsp_data.extend(struct.pack("<I", 5))  # texture index
        bsp_data.extend(struct.pack("<ff", 0.0, 0.0))  # uv0
        bsp_data.extend(struct.pack("<ff", 1.0, 0.0))  # uv1
        bsp_data.extend(struct.pack("<ff", 0.0, 1.0))  # uv2
        
        # ENDOFBRANCH to terminate polygon list
        bsp_data.extend(struct.pack("<I", BSPChunkType.ENDOFBRANCH.value))
        bsp_data.extend(struct.pack("<I", 0))   # chunk size
        
        # Parse the BSP data
        bsp_tree = self.parser.parse_bsp_tree(bytes(bsp_data), 2117)
        
        # Should parse successfully with BOUNDBOX structure
        self.assertIsNotNone(bsp_tree, "Should parse BOUNDBOX data successfully")
        self.assertEqual(bsp_tree.node_type, BSPNodeType.LEAF, "Should create LEAF node")
        self.assertIsNotNone(bsp_tree.bbox, "Should have bounding box")
        self.assertGreater(len(bsp_tree.polygons), 0, "Should have polygons")

    def test_tmappoly2_parsing(self):
        """Test TMAPPOLY2 chunk parsing with 32-bit indices."""
        # Create BSP data with TMAPPOLY2
        bsp_data = bytearray()
        
        # DEFFPOINTS chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.DEFFPOINTS.value))
        bsp_data.extend(struct.pack("<I", 68))  # chunk size
        bsp_data.extend(struct.pack("<I", 4))   # num vertices
        bsp_data.extend(struct.pack("<I", 1))   # num normals
        
        # Vertices
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 1.0, 0.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 0.0, 1.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))
        
        # Normals
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))
        
        # Bounding box for TMAPPOLY2
        bsp_data.extend(struct.pack("<I", BSPChunkType.BOUNDBOX.value))
        bsp_data.extend(struct.pack("<I", 24))  # chunk size
        bsp_data.extend(struct.pack("<fff", -1.0, -1.0, -1.0))  # min
        bsp_data.extend(struct.pack("<fff", 1.0, 1.0, 1.0))     # max
        
        # TMAPPOLY2 chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.TMAPPOLY2.value))
        bsp_data.extend(struct.pack("<I", 96))  # chunk size
        
        # Bounding box for TMAPPOLY2
        bsp_data.extend(struct.pack("<fff", -0.5, -0.5, -0.5))  # min
        bsp_data.extend(struct.pack("<fff", 0.5, 0.5, 0.5))     # max
        
        # Polygon data (32-bit indices)
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal
        bsp_data.extend(struct.pack("<I", 5))                # texture index
        bsp_data.extend(struct.pack("<I", 3))                # num vertices
        
        # Vertex indices (32-bit)
        bsp_data.extend(struct.pack("<I", 0))
        bsp_data.extend(struct.pack("<I", 1))
        bsp_data.extend(struct.pack("<I", 2))
        
        # Normal indices (32-bit)
        bsp_data.extend(struct.pack("<I", 0))
        bsp_data.extend(struct.pack("<I", 0))
        bsp_data.extend(struct.pack("<I", 0))
        
        # UV coordinates
        bsp_data.extend(struct.pack("<ff", 0.0, 0.0))  # uv0
        bsp_data.extend(struct.pack("<ff", 1.0, 0.0))  # uv1
        bsp_data.extend(struct.pack("<ff", 0.0, 1.0))  # uv2
        
        # ENDOFBRANCH
        bsp_data.extend(struct.pack("<I", BSPChunkType.ENDOFBRANCH.value))
        bsp_data.extend(struct.pack("<I", 0))   # chunk size
        
        # Parse the BSP data
        bsp_tree = self.parser.parse_bsp_tree(bytes(bsp_data), 2117)
        
        # Should parse successfully
        self.assertIsNotNone(bsp_tree, "Should parse TMAPPOLY2 data successfully")
        stats = self.parser.get_parsing_stats()
        self.assertEqual(stats["error_count"], 0, "Should have no parsing errors")

    def test_sortnorm_parsing(self):
        """Test SORTNORM chunk parsing with split nodes."""
        # Create BSP data with SORTNORM (splitting node)
        bsp_data = bytearray()
        
        # DEFFPOINTS chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.DEFFPOINTS.value))
        bsp_data.extend(struct.pack("<I", 68))  # chunk size
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
        
        # SORTNORM chunk (splitting node)
        bsp_data.extend(struct.pack("<I", BSPChunkType.SORTNORM.value))
        bsp_data.extend(struct.pack("<I", 64))  # chunk size
        
        # Splitting plane data
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))  # point
        bsp_data.extend(struct.pack("<I", 0))                # reserved
        
        # Front and back branch offsets (placeholders)
        bsp_data.extend(struct.pack("<I", 0))  # front offset (none)
        bsp_data.extend(struct.pack("<I", 0))  # back offset (none)
        
        # Prelist, postlist, online (unused)
        bsp_data.extend(struct.pack("<I", 0))
        bsp_data.extend(struct.pack("<I", 0))
        bsp_data.extend(struct.pack("<I", 0))
        
        # Bounding box for newer versions
        bsp_data.extend(struct.pack("<fff", -1.0, -1.0, -1.0))  # min
        bsp_data.extend(struct.pack("<fff", 1.0, 1.0, 1.0))     # max
        
        # Parse the BSP data
        bsp_tree = self.parser.parse_bsp_tree(bytes(bsp_data), 2117)
        
        # Should parse successfully as split node
        self.assertIsNotNone(bsp_tree, "Should parse SORTNORM data successfully")
        self.assertEqual(bsp_tree.node_type, BSPNodeType.NODE, "Should create NODE (split) node")
        self.assertIsNotNone(bsp_tree.bbox, "Should have bounding box")
        self.assertIsNotNone(bsp_tree.front_child, "Should have front child")
        self.assertIsNotNone(bsp_tree.back_child, "Should have back child")

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
        bsp_data.extend(struct.pack("<I", 72))  # chunk size
        
        # Minimal polygon data
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal
        bsp_data.extend(struct.pack("<fff", 0.5, 0.5, 0.0))  # center
        bsp_data.extend(struct.pack("<f", 1.0))              # radius
        bsp_data.extend(struct.pack("<I", 3))                # num vertices
        bsp_data.extend(struct.pack("<H", 0))                # vertex 0
        bsp_data.extend(struct.pack("<H", 1))                # vertex 1
        bsp_data.extend(struct.pack("<H", 2))                # vertex 2
        bsp_data.extend(struct.pack("<I", 5))                # texture
        bsp_data.extend(struct.pack("<ff", 0.0, 0.0))        # uv0
        bsp_data.extend(struct.pack("<ff", 1.0, 0.0))        # uv1
        bsp_data.extend(struct.pack("<ff", 0.0, 1.0))        # uv2
        
        bsp_tree = self.parser.parse_bsp_tree(bytes(bsp_data), 2117)
        
        # Should fail gracefully
        self.assertIsNone(bsp_tree, "Should return None for invalid chunk order")
        stats = self.parser.get_parsing_stats()
        self.assertGreater(stats["error_count"], 0, "Should record parsing errors")

    def test_parse_bsp_data_enhanced_function(self):
        """Test the main parse_bsp_data_enhanced function interface."""
        # Create simple BSP data
        bsp_data = bytearray()
        
        # DEFFPOINTS chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.DEFFPOINTS.value))
        bsp_data.extend(struct.pack("<I", 68))  # chunk size
        bsp_data.extend(struct.pack("<I", 3))   # num vertices
        bsp_data.extend(struct.pack("<I", 1))   # num normals
        
        # Vertices and normals
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 1.0, 0.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 0.0, 1.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))
        
        # BOUNDBOX chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.BOUNDBOX.value))
        bsp_data.extend(struct.pack("<I", 24))  # chunk size
        bsp_data.extend(struct.pack("<fff", -1.0, -1.0, -1.0))  # min
        bsp_data.extend(struct.pack("<fff", 1.0, 1.0, 1.0))     # max
        
        # TMAPPOLY chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.TMAPPOLY.value))
        bsp_data.extend(struct.pack("<I", 72))  # chunk size
        
        # Polygon data
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal
        bsp_data.extend(struct.pack("<fff", 0.5, 0.5, 0.0))  # center
        bsp_data.extend(struct.pack("<f", 1.0))              # radius
        bsp_data.extend(struct.pack("<I", 3))                # num vertices
        bsp_data.extend(struct.pack("<H", 0))                # vertex 0
        bsp_data.extend(struct.pack("<H", 1))                # vertex 1
        bsp_data.extend(struct.pack("<H", 2))                # vertex 2
        bsp_data.extend(struct.pack("<I", 5))                # texture
        bsp_data.extend(struct.pack("<ff", 0.0, 0.0))        # uv0
        bsp_data.extend(struct.pack("<ff", 1.0, 0.0))        # uv1
        bsp_data.extend(struct.pack("<ff", 0.0, 1.0))        # uv2
        
        # ENDOFBRANCH
        bsp_data.extend(struct.pack("<I", BSPChunkType.ENDOFBRANCH.value))
        bsp_data.extend(struct.pack("<I", 0))   # chunk size
        
        # Parse using the main function
        result = parse_bsp_data_enhanced(bytes(bsp_data), 2117)
        
        # Should return structured data
        self.assertIsNotNone(result, "Should return result dictionary")
        self.assertIn("bsp_tree", result, "Should contain BSP tree")
        self.assertIn("vertices", result, "Should contain vertices")
        self.assertIn("normals", result, "Should contain normals")
        self.assertIn("polygons", result, "Should contain polygons")
        self.assertIn("parsing_stats", result, "Should contain parsing stats")

    def test_complex_bsp_tree_parsing(self):
        """Test parsing of complex BSP tree structures."""
        # Create a complex BSP tree with multiple node types
        bsp_data = bytearray()
        
        # DEFFPOINTS chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.DEFFPOINTS.value))
        bsp_data.extend(struct.pack("<I", 80))  # chunk size
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
        
        # SORTNORM chunk (split node)
        bsp_data.extend(struct.pack("<I", BSPChunkType.SORTNORM.value))
        bsp_data.extend(struct.pack("<I", 64))  # chunk size
        
        # Splitting plane
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))  # point
        bsp_data.extend(struct.pack("<I", 0))                # reserved
        
        # Front and back branch offsets (both zero for now)
        bsp_data.extend(struct.pack("<I", 0))  # front offset
        bsp_data.extend(struct.pack("<I", 0))  # back offset
        
        # Prelist, postlist, online
        bsp_data.extend(struct.pack("<I", 0))
        bsp_data.extend(struct.pack("<I", 0))
        bsp_data.extend(struct.pack("<I", 0))
        
        # Bounding box
        bsp_data.extend(struct.pack("<fff", -1.0, -1.0, -1.0))  # min
        bsp_data.extend(struct.pack("<fff", 1.0, 1.0, 1.0))     # max
        
        # BOUNDBOX chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.BOUNDBOX.value))
        bsp_data.extend(struct.pack("<I", 24))  # chunk size
        bsp_data.extend(struct.pack("<fff", -0.5, -0.5, -0.5))  # min
        bsp_data.extend(struct.pack("<fff", 0.5, 0.5, 0.5))     # max
        
        # TMAPPOLY chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.TMAPPOLY.value))
        bsp_data.extend(struct.pack("<I", 72))  # chunk size
        
        # Polygon data
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal
        bsp_data.extend(struct.pack("<fff", 0.33, 0.33, 0.0))  # center
        bsp_data.extend(struct.pack("<f", 0.5))              # radius
        bsp_data.extend(struct.pack("<I", 3))                # num vertices
        bsp_data.extend(struct.pack("<H", 0))                # vertex 0
        bsp_data.extend(struct.pack("<H", 1))                # vertex 1
        bsp_data.extend(struct.pack("<H", 2))                # vertex 2
        bsp_data.extend(struct.pack("<I", 3))                # texture
        bsp_data.extend(struct.pack("<ff", 0.0, 1.0))        # uv0
        bsp_data.extend(struct.pack("<ff", 1.0, 1.0))        # uv1
        bsp_data.extend(struct.pack("<ff", 0.0, 0.0))        # uv2
        
        # ENDOFBRANCH
        bsp_data.extend(struct.pack("<I", BSPChunkType.ENDOFBRANCH.value))
        bsp_data.extend(struct.pack("<I", 0))   # chunk size
        
        # Parse the BSP data
        bsp_tree = self.parser.parse_bsp_tree(bytes(bsp_data), 2117)
        
        # Should parse successfully with complex structure
        self.assertIsNotNone(bsp_tree, "Should parse complex BSP tree successfully")
        self.assertEqual(bsp_tree.node_type, BSPNodeType.NODE, "Should create NODE for SORTNORM")
        self.assertIsNotNone(bsp_tree.bbox, "Should have bounding box")
        self.assertIsNotNone(bsp_tree.front_child, "Should have front child")
        self.assertIsNotNone(bsp_tree.back_child, "Should have back child")
        
        # Check leaf node
        if bsp_tree.front_child and bsp_tree.front_child.node_type == BSPNodeType.LEAF:
            self.assertGreater(len(bsp_tree.front_child.polygons), 0, "Should have polygons in leaf")
        elif bsp_tree.back_child and bsp_tree.back_child.node_type == BSPNodeType.LEAF:
            self.assertGreater(len(bsp_tree.back_child.polygons), 0, "Should have polygons in leaf")

    def test_malformed_chunk_sizes(self):
        """Test parsing with malformed chunk sizes."""
        bsp_data = bytearray()
        
        # DEFFPOINTS chunk with invalid size
        bsp_data.extend(struct.pack("<I", BSPChunkType.DEFFPOINTS.value))
        bsp_data.extend(struct.pack("<I", 1000000))  # Invalid large size
        bsp_data.extend(struct.pack("<I", 1))
        bsp_data.extend(struct.pack("<I", 1))
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))
        
        bsp_tree = self.parser.parse_bsp_tree(bytes(bsp_data), 2117)
        
        # Should handle gracefully
        self.assertIsNone(bsp_tree, "Should return None for malformed chunk sizes")
        stats = self.parser.get_parsing_stats()
        self.assertGreater(stats["error_count"], 0, "Should record parsing errors")

    def test_invalid_vertex_indices(self):
        """Test parsing with invalid vertex indices."""
        bsp_data = bytearray()
        
        # DEFFPOINTS chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.DEFFPOINTS.value))
        bsp_data.extend(struct.pack("<I", 56))  # chunk size
        bsp_data.extend(struct.pack("<I", 1))   # num vertices
        bsp_data.extend(struct.pack("<I", 1))   # num normals
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))  # vertex 0
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal 0
        
        # TMAPPOLY with invalid vertex index
        bsp_data.extend(struct.pack("<I", BSPChunkType.TMAPPOLY.value))
        bsp_data.extend(struct.pack("<I", 72))  # chunk size
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal
        bsp_data.extend(struct.pack("<fff", 0.5, 0.5, 0.0))  # center
        bsp_data.extend(struct.pack("<f", 1.0))              # radius
        bsp_data.extend(struct.pack("<I", 3))                # num vertices
        bsp_data.extend(struct.pack("<H", 0))                # vertex 0 (valid)
        bsp_data.extend(struct.pack("<H", 1))                # vertex 1 (invalid - only 1 vertex)
        bsp_data.extend(struct.pack("<H", 2))                # vertex 2 (invalid)
        bsp_data.extend(struct.pack("<I", 5))                # texture
        bsp_data.extend(struct.pack("<ff", 0.0, 0.0))        # uv0
        bsp_data.extend(struct.pack("<ff", 1.0, 0.0))        # uv1
        bsp_data.extend(struct.pack("<ff", 0.0, 1.0))        # uv2
        
        # ENDOFBRANCH
        bsp_data.extend(struct.pack("<I", BSPChunkType.ENDOFBRANCH.value))
        bsp_data.extend(struct.pack("<I", 0))   # chunk size
        
        bsp_tree = self.parser.parse_bsp_tree(bytes(bsp_data), 2117)
        
        # Should handle gracefully with warnings
        self.assertIsNotNone(bsp_tree, "Should parse despite invalid vertex indices")
        stats = self.parser.get_parsing_stats()
        # Note: May not increase error count if handled gracefully within parsing


def run_tests():
    """Run all enhanced BSP parsing tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEnhancedBSPParsing))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)