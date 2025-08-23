#!/usr/bin/env python3
"""
Unit tests for OP_FLATPOLY chunk parsing in BSP data.
"""
import struct
import unittest
from pathlib import Path

from .pof_misc_parser import _BSPGeometryParser


class TestBSPFlatPoly(unittest.TestCase):
    """Test OP_FLATPOLY chunk parsing functionality."""

    def test_flatpoly_parsing_basic(self):
        """Test basic OP_FLATPOLY parsing with valid data."""
        # Create a mock BSP data stream with DEFPOINTS and FLATPOLY chunks
        # DEFPOINTS chunk first
        defpoints_data = bytearray()
        
        # DEFPOINTS header: chunk ID + size
        defpoints_data.extend(struct.pack("<I", 1))  # OP_DEFPOINTS = 1
        defpoints_data.extend(struct.pack("<I", 95))  # total chunk size including header (95 bytes)
        
        # DEFPOINTS content: nverts, n_norms, data_offset
        defpoints_data.extend(struct.pack("<i", 3))   # nverts
        defpoints_data.extend(struct.pack("<i", 0))   # n_norms (unused)
        defpoints_data.extend(struct.pack("<i", 23))  # data_offset (from chunk start to vertex data)
        
        # norm_counts for 3 vertices (each has 1 normal)
        defpoints_data.extend(struct.pack("<BBB", 1, 1, 1))
        
        # Vertex data (3 vertices) starts at offset 15 from chunk start
        # Position 15: vertex 0
        defpoints_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))   # vertex 0
        defpoints_data.extend(struct.pack("<fff", 0.0, 1.0, 0.0))   # normal for vertex 0
        defpoints_data.extend(struct.pack("<fff", 1.0, 0.0, 0.0))   # vertex 1
        defpoints_data.extend(struct.pack("<fff", 0.0, 1.0, 0.0))   # normal for vertex 1
        defpoints_data.extend(struct.pack("<fff", 0.0, 1.0, 0.0))   # vertex 2
        defpoints_data.extend(struct.pack("<fff", 0.0, 1.0, 0.0))   # normal for vertex 2

        # FLATPOLY chunk
        flatpoly_data = bytearray()
        
        # FLATPOLY header: chunk ID + size
        flatpoly_data.extend(struct.pack("<I", 2))  # OP_FLATPOLY = 2
        flatpoly_data.extend(struct.pack("<I", 34))  # total chunk size including header (34 bytes)
        
        # FLATPOLY content: normal, color, nv, vertex indices
        flatpoly_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal
        flatpoly_data.extend(struct.pack("<i", 0xFF0000))         # color (red)
        flatpoly_data.extend(struct.pack("<i", 3))               # nv (3 vertices)
        
        # Vertex indices (shorts)
        flatpoly_data.extend(struct.pack("<hhh", 0, 1, 2))  # vertex indices

        # Combine into full BSP data
        bsp_data = defpoints_data + flatpoly_data
        
        # Parse the BSP data
        parser = _BSPGeometryParser(pof_version=2100)
        result = parser.parse(bsp_data)
        
        # Verify results
        self.assertEqual(len(result["vertices"]), 3, "Should have 3 vertices")
        self.assertEqual(len(result["normals"]), 3, "Should have 3 normals")
        self.assertEqual(len(result["uvs"]), 3, "Should have 3 UV sets")
        self.assertEqual(len(result["polygons"]), 1, "Should have 1 polygon")
        
        # Check that all UVs are (0, 0) for flat polygons
        for uv in result["uvs"]:
            self.assertEqual(uv, [0.0, 0.0], "Flat polygons should have default UVs (0, 0)")
        
        # Check polygon texture index is -1 for flat polygons
        self.assertEqual(result["polygons"][0]["texture_index"], -1, "Flat polygons should have texture index -1")

    def test_flatpoly_invalid_vertex_index(self):
        """Test OP_FLATPOLY parsing with invalid vertex indices."""
        # Create minimal DEFPOINTS with only 1 vertex
        defpoints_data = bytearray()
        defpoints_data.extend(struct.pack("<I", 1))  # OP_DEFPOINTS
        defpoints_data.extend(struct.pack("<I", 43))  # total chunk size including header (43 bytes)
        defpoints_data.extend(struct.pack("<i", 1))   # nverts
        defpoints_data.extend(struct.pack("<i", 0))   # n_norms
        defpoints_data.extend(struct.pack("<i", 21))  # data_offset (from chunk start to vertex data)
        defpoints_data.extend(struct.pack("<B", 1))   # norm_counts
        # Vertex data starts at offset 21
        defpoints_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))  # vertex
        defpoints_data.extend(struct.pack("<fff", 0.0, 1.0, 0.0))  # normal

        # FLATPOLY with invalid vertex index (index 1, but only vertex 0 exists)
        flatpoly_data = bytearray()
        flatpoly_data.extend(struct.pack("<I", 2))  # OP_FLATPOLY = 2
        flatpoly_data.extend(struct.pack("<I", 34))  # total chunk size including header (34 bytes)
        flatpoly_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal
        flatpoly_data.extend(struct.pack("<i", 0xFF0000))         # color
        flatpoly_data.extend(struct.pack("<i", 3))               # nv
        flatpoly_data.extend(struct.pack("<hhh", 0, 1, 2))       # vertex indices (1 is invalid)

        bsp_data = defpoints_data + flatpoly_data
        
        parser = _BSPGeometryParser(pof_version=2100)
        result = parser.parse(bsp_data)
        
        # Should still parse but skip the invalid triangle
        self.assertEqual(len(result["polygons"]), 0, "Should skip polygon with invalid vertex indices")

    def test_flatpoly_insufficient_data(self):
        """Test OP_FLATPOLY parsing with insufficient data."""
        # Create FLATPOLY chunk that's too short - chunk size is 10 but we write more data
        flatpoly_data = bytearray()
        flatpoly_data.extend(struct.pack("<I", 2))  # OP_FLATPOLY = 2
        flatpoly_data.extend(struct.pack("<I", 10))  # chunk size too small (only 10 bytes total)
        # Write normal data (12 bytes) which exceeds the chunk size
        flatpoly_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal (12 bytes)
        # This should cause a parsing error since chunk size is only 10 bytes
        
        parser = _BSPGeometryParser(pof_version=2100)
        
        # The parser should handle the error gracefully and return empty geometry
        result = parser.parse(flatpoly_data)
        self.assertEqual(len(result["vertices"]), 0, "Should return empty geometry on parse error")
        self.assertEqual(len(result["polygons"]), 0, "Should return empty geometry on parse error")


if __name__ == "__main__":
    unittest.main()
