#!/usr/bin/env python3
"""
Comprehensive POF Parser Stability Tests

Tests the robustness and correctness of the POF parser implementation
against the Rust reference implementation patterns.
"""

import struct
import tempfile
import unittest
from pathlib import Path
from typing import List

from data_converter.pof_parser.pof_bsp_parser import BSPParser, parse_bsp_data
from data_converter.pof_parser.pof_types import BSPNode, BSPNodeType, BSPPolygon, Vector3D, BoundingBox
from data_converter.pof_parser.pof_parser import POFParser
from data_converter.pof_parser.pof_chunks import POF_HEADER_ID, ID_OHDR, ID_SOBJ, ID_TXTR


class TestBSPNodeStructure(unittest.TestCase):
    """Test BSP node structure and validation."""

    def test_bsp_node_creation(self):
        """Test BSP node creation with proper validation."""
        # Test empty node
        empty_node = BSPNode(
            node_type=BSPNodeType.EMPTY,
            normal=Vector3D(0, 0, 1),
            plane_distance=0.0
        )
        self.assertTrue(empty_node.is_empty())
        self.assertFalse(empty_node.is_leaf())

        # Test leaf node with polygon
        polygon = BSPPolygon(
            vertices=[Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(0, 1, 0)],
            normal=Vector3D(0, 0, 1),
            plane_distance=0.0,
            texture_index=0
        )
        leaf_node = BSPNode(
            node_type=BSPNodeType.LEAF,
            normal=Vector3D(0, 0, 1),
            plane_distance=0.0,
            polygons=[polygon]
        )
        self.assertTrue(leaf_node.is_leaf())
        self.assertEqual(len(leaf_node.polygons), 1)

    def test_bsp_node_validation(self):
        """Test BSP node validation."""
        # Test invalid normal (not unit length)
        with self.assertRaises(ValueError):
            BSPNode(
                node_type=BSPNodeType.NODE,
                normal=Vector3D(0, 0, 2),  # Not unit length
                plane_distance=0.0
            )

        # Test invalid polygon (less than 3 vertices)
        with self.assertRaises(ValueError):
            BSPPolygon(
                vertices=[Vector3D(0, 0, 0), Vector3D(1, 0, 0)],  # Only 2 vertices
                normal=Vector3D(0, 0, 1),
                plane_distance=0.0,
                texture_index=0
            )


class TestBSPParsingRobustness(unittest.TestCase):
    """Test BSP parsing robustness and error handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = BSPParser()

    def test_empty_bsp_data(self):
        """Test parsing empty BSP data."""
        result = self.parser.parse_bsp_tree(b"", 2117)
        self.assertIsNone(result)

    def test_malformed_chunk_header(self):
        """Test parsing malformed chunk headers."""
        # Buffer too short for header
        short_data = b"\x01\x00\x00"
        result = self.parser.parse_bsp_tree(short_data, 2117)
        self.assertIsNone(result)

    def test_invalid_chunk_size(self):
        """Test parsing chunks with invalid sizes."""
        # DEFFPOINTS with size larger than buffer
        malformed_data = struct.pack("<II", 1, 1000)  # chunk type 1 (DEFFPOINTS), size 1000
        malformed_data += b"\x00" * 100  # Only 100 bytes of data
        result = self.parser.parse_bsp_tree(malformed_data, 2117)
        self.assertIsNone(result)

    def test_invalid_vertex_index(self):
        """Test parsing with invalid vertex indices."""
        # Create BSP data with invalid vertex index
        bsp_data = bytearray()
        
        # DEFFPOINTS chunk
        bsp_data.extend(struct.pack("<II", 1, 24))  # DEFFPOINTS, 24 bytes
        bsp_data.extend(struct.pack("<II", 1, 0))   # 1 vertex, 0 normals
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))  # vertex 0
        
        # TMAPPOLY with invalid vertex index
        bsp_data.extend(struct.pack("<II", 3, 36))  # TMAPPOLY, 36 bytes
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))  # normal
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))  # center
        bsp_data.extend(struct.pack("<f", 1.0))             # radius
        bsp_data.extend(struct.pack("<I", 3))               # 3 vertices (but we only have 1)
        bsp_data.extend(struct.pack("<III", 0, 1, 2))       # vertex indices (1 and 2 are invalid)
        bsp_data.extend(struct.pack("<I", 0))               # texture
        bsp_data.extend(struct.pack("<ff", 0.0, 0.0))       # uv0
        bsp_data.extend(struct.pack("<ff", 1.0, 0.0))       # uv1
        bsp_data.extend(struct.pack("<ff", 0.0, 1.0))       # uv2
        
        result = self.parser.parse_bsp_tree(bytes(bsp_data), 2117)
        # Should handle gracefully with warnings
        self.assertIsNotNone(result)


class TestComplexBSPTrees(unittest.TestCase):
    """Test parsing of complex BSP tree structures."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = BSPParser()

    def create_complex_bsp_tree(self) -> bytes:
        """Create a complex BSP tree for testing."""
        bsp_data = bytearray()
        
        # DEFFPOINTS chunk with multiple vertices and normals
        bsp_data.extend(struct.pack("<II", 1, 104))  # DEFFPOINTS, 104 bytes
        bsp_data.extend(struct.pack("<II", 4, 2))    # 4 vertices, 2 normals
        # Vertices
        bsp_data.extend(struct.pack("<fff", -1.0, -1.0, 0.0))  # vertex 0
        bsp_data.extend(struct.pack("<fff", 1.0, -1.0, 0.0))   # vertex 1
        bsp_data.extend(struct.pack("<fff", 1.0, 1.0, 0.0))    # vertex 2
        bsp_data.extend(struct.pack("<fff", -1.0, 1.0, 0.0))   # vertex 3
        # Normals
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))    # normal 0
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, -1.0))   # normal 1
        
        # BOUNDBOX chunk
        bsp_data.extend(struct.pack("<II", 5, 24))  # BOUNDBOX, 24 bytes
        bsp_data.extend(struct.pack("<fff", -1.0, -1.0, -1.0))  # min
        bsp_data.extend(struct.pack("<fff", 1.0, 1.0, 1.0))     # max
        
        # TMAPPOLY chunk (first polygon)
        bsp_data.extend(struct.pack("<II", 3, 72))  # TMAPPOLY, 72 bytes
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))     # normal
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))     # center
        bsp_data.extend(struct.pack("<f", 1.414))               # radius
        bsp_data.extend(struct.pack("<I", 4))                   # 4 vertices
        bsp_data.extend(struct.pack("<IIII", 0, 1, 2, 3))       # vertex indices
        bsp_data.extend(struct.pack("<I", 0))                   # texture
        bsp_data.extend(struct.pack("<ff", 0.0, 1.0))           # uv0
        bsp_data.extend(struct.pack("<ff", 1.0, 1.0))           # uv1
        bsp_data.extend(struct.pack("<ff", 1.0, 0.0))           # uv2
        bsp_data.extend(struct.pack("<ff", 0.0, 0.0))           # uv3
        
        # Second TMAPPOLY chunk
        bsp_data.extend(struct.pack("<II", 3, 72))  # TMAPPOLY, 72 bytes
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, -1.0))    # normal
        bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))     # center
        bsp_data.extend(struct.pack("<f", 1.414))               # radius
        bsp_data.extend(struct.pack("<I", 4))                   # 4 vertices
        bsp_data.extend(struct.pack("<IIII", 3, 2, 1, 0))       # vertex indices (reversed)
        bsp_data.extend(struct.pack("<I", 1))                   # texture
        bsp_data.extend(struct.pack("<ff", 0.0, 0.0))           # uv0
        bsp_data.extend(struct.pack("<ff", 1.0, 0.0))           # uv1
        bsp_data.extend(struct.pack("<ff", 1.0, 1.0))           # uv2
        bsp_data.extend(struct.pack("<ff", 0.0, 1.0))           # uv3
        
        # ENDOFBRANCH
        bsp_data.extend(struct.pack("<II", 0, 0))   # ENDOFBRANCH, 0 bytes
        
        return bytes(bsp_data)

    def test_complex_bsp_tree_parsing(self):
        """Test parsing of complex BSP tree structures."""
        bsp_data = self.create_complex_bsp_tree()
        result = self.parser.parse_bsp_tree(bsp_data, 2117)
        
        # Should parse successfully
        self.assertIsNotNone(result)
        self.assertEqual(result.node_type, BSPNodeType.LEAF)
        self.assertEqual(len(result.polygons), 2)
        
        # Check first polygon
        poly1 = result.polygons[0]
        self.assertEqual(len(poly1.vertices), 4)
        self.assertEqual(poly1.texture_index, 0)
        
        # Check second polygon
        poly2 = result.polygons[1]
        self.assertEqual(len(poly2.vertices), 4)
        self.assertEqual(poly2.texture_index, 1)

    def test_parse_bsp_data_function(self):
        """Test the main parse_bsp_data function."""
        bsp_data = self.create_complex_bsp_tree()
        result = parse_bsp_data(bsp_data, 2117)
        
        self.assertIsNotNone(result)
        self.assertIn('bsp_tree', result)
        self.assertIn('vertices', result)
        self.assertIn('normals', result)
        self.assertIn('polygons', result)
        self.assertIn('parsing_stats', result)
        
        # Check parsing stats
        stats = result['parsing_stats']
        self.assertIn('error_count', stats)
        self.assertIn('vertex_count', stats)
        self.assertIn('normal_count', stats)
        self.assertEqual(stats['vertex_count'], 4)
        self.assertEqual(stats['normal_count'], 2)


class TestPOFParserIntegration(unittest.TestCase):
    """Test integration of BSP parsing with main POF parser."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.parser = POFParser()

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def create_test_pof_with_bsp(self) -> Path:
        """Create a test POF file with BSP data."""
        test_file = self.temp_path / "test_bsp.pof"
        
        with open(test_file, "wb") as f:
            # POF header
            f.write(struct.pack("<I", POF_HEADER_ID))  # POF header ID
            f.write(struct.pack("<i", 2117))           # Version
            
            # OHDR chunk
            ohdr_data = bytearray()
            ohdr_data.extend(struct.pack("<f", 10.0))      # max_radius
            ohdr_data.extend(struct.pack("<I", 0))         # object_flags
            ohdr_data.extend(struct.pack("<I", 1))         # num_subobjects
            ohdr_data.extend(struct.pack("<fff", -5.0, -5.0, -5.0))  # min bounds
            ohdr_data.extend(struct.pack("<fff", 5.0, 5.0, 5.0))     # max bounds
            # Detail levels (8 entries)
            for _ in range(8):
                ohdr_data.extend(struct.pack("<i", -1))
            # Debris pieces (32 entries)
            for _ in range(32):
                ohdr_data.extend(struct.pack("<i", -1))
            # Mass and center
            ohdr_data.extend(struct.pack("<f", 1000.0))  # mass
            ohdr_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))  # center of mass
            # Moment of inertia (3 vectors)
            ohdr_data.extend(struct.pack("<fff", 1000.0, 0.0, 0.0))
            ohdr_data.extend(struct.pack("<fff", 0.0, 1000.0, 0.0))
            ohdr_data.extend(struct.pack("<fff", 0.0, 0.0, 1000.0))
            # Cross sections (8 entries)
            for _ in range(8):
                ohdr_data.extend(struct.pack("<ff", 0.0, 0.0))
            # Lights (empty)
            ohdr_data.extend(struct.pack("<I", 0))
            
            f.write(struct.pack("<I", ID_OHDR))  # OHDR chunk ID
            f.write(struct.pack("<I", len(ohdr_data)))  # OHDR chunk size
            f.write(ohdr_data)
            
            # SOBJ chunk with BSP data
            sobj_data = bytearray()
            sobj_data.extend(struct.pack("<I", 0))         # subobject number
            sobj_data.extend(struct.pack("<f", 5.0))       # radius
            sobj_data.extend(struct.pack("<I", 0xFFFFFFFF)) # parent (-1)
            sobj_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))  # offset
            sobj_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))  # geometric center
            sobj_data.extend(struct.pack("<fff", -5.0, -5.0, -5.0))  # min bounds
            sobj_data.extend(struct.pack("<fff", 5.0, 5.0, 5.0))     # max bounds
            
            # Name and properties
            name_bytes = b"test_subobj"
            sobj_data.extend(struct.pack("<I", len(name_bytes)))
            sobj_data.extend(name_bytes)
            prop_bytes = b""
            sobj_data.extend(struct.pack("<I", len(prop_bytes)))
            sobj_data.extend(prop_bytes)
            
            # Movement type and axis
            sobj_data.extend(struct.pack("<I", 0))  # movement_type
            sobj_data.extend(struct.pack("<I", 3))  # movement_axis (NONE)
            
            # BSP data (using the complex BSP from above)
            bsp_data = bytearray()
            bsp_data.extend(struct.pack("<II", 1, 104))  # DEFFPOINTS, 104 bytes
            bsp_data.extend(struct.pack("<II", 4, 2))    # 4 vertices, 2 normals
            # Vertices
            bsp_data.extend(struct.pack("<fff", -1.0, -1.0, 0.0))  # vertex 0
            bsp_data.extend(struct.pack("<fff", 1.0, -1.0, 0.0))   # vertex 1
            bsp_data.extend(struct.pack("<fff", 1.0, 1.0, 0.0))    # vertex 2
            bsp_data.extend(struct.pack("<fff", -1.0, 1.0, 0.0))   # vertex 3
            # Normals
            bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))    # normal 0
            bsp_data.extend(struct.pack("<fff", 0.0, 0.0, -1.0))   # normal 1
            
            # BOUNDBOX chunk
            bsp_data.extend(struct.pack("<II", 5, 24))  # BOUNDBOX, 24 bytes
            bsp_data.extend(struct.pack("<fff", -1.0, -1.0, -1.0))  # min
            bsp_data.extend(struct.pack("<fff", 1.0, 1.0, 1.0))     # max
            
            # TMAPPOLY chunk (first polygon)
            bsp_data.extend(struct.pack("<II", 3, 72))  # TMAPPOLY, 72 bytes
            bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 1.0))     # normal
            bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))     # center
            bsp_data.extend(struct.pack("<f", 1.414))               # radius
            bsp_data.extend(struct.pack("<I", 4))                   # 4 vertices
            bsp_data.extend(struct.pack("<IIII", 0, 1, 2, 3))       # vertex indices
            bsp_data.extend(struct.pack("<I", 0))                   # texture
            bsp_data.extend(struct.pack("<ff", 0.0, 1.0))           # uv0
            bsp_data.extend(struct.pack("<ff", 1.0, 1.0))           # uv1
            bsp_data.extend(struct.pack("<ff", 1.0, 0.0))           # uv2
            bsp_data.extend(struct.pack("<ff", 0.0, 0.0))           # uv3
            
            # Second TMAPPOLY chunk
            bsp_data.extend(struct.pack("<II", 3, 72))  # TMAPPOLY, 72 bytes
            bsp_data.extend(struct.pack("<fff", 0.0, 0.0, -1.0))    # normal
            bsp_data.extend(struct.pack("<fff", 0.0, 0.0, 0.0))     # center
            bsp_data.extend(struct.pack("<f", 1.414))               # radius
            bsp_data.extend(struct.pack("<I", 4))                   # 4 vertices
            bsp_data.extend(struct.pack("<IIII", 3, 2, 1, 0))       # vertex indices (reversed)
            bsp_data.extend(struct.pack("<I", 1))                   # texture
            bsp_data.extend(struct.pack("<ff", 0.0, 0.0))           # uv0
            bsp_data.extend(struct.pack("<ff", 1.0, 0.0))           # uv1
            bsp_data.extend(struct.pack("<ff", 1.0, 1.0))           # uv2
            bsp_data.extend(struct.pack("<ff", 0.0, 1.0))           # uv3
            
            # ENDOFBRANCH
            bsp_data.extend(struct.pack("<II", 0, 0))   # ENDOFBRANCH, 0 bytes
            
            sobj_data.extend(struct.pack("<I", len(bsp_data)))  # BSP data size
            sobj_data.extend(bsp_data)  # BSP data
            
            f.write(struct.pack("<I", ID_SOBJ))  # SOBJ chunk ID
            f.write(struct.pack("<I", len(sobj_data)))  # SOBJ chunk size
            f.write(sobj_data)
            
            # TXTR chunk
            texture_name = b"test_texture.dds"
            txtr_data = struct.pack("<I", 1)  # num_textures
            txtr_data += struct.pack("<I", len(texture_name))  # length of first texture
            txtr_data += texture_name  # texture name bytes
            
            f.write(struct.pack("<I", ID_TXTR))  # TXTR chunk ID
            f.write(struct.pack("<I", len(txtr_data)))  # TXTR chunk size
            f.write(txtr_data)
        
        return test_file

    def test_pof_parsing_with_bsp(self):
        """Test complete POF parsing with BSP data."""
        test_file = self.create_test_pof_with_bsp()
        result = self.parser.parse(test_file)
        
        # Should parse successfully
        self.assertIsNotNone(result)
        self.assertEqual(len(result.subobjects), 1)
        
        subobj = result.subobjects[0]
        self.assertTrue(subobj.has_bsp_data())
        
        # Test BSP tree parsing
        bsp_tree = self.parser.parse_subobject_bsp_tree(0)
        self.assertIsNotNone(bsp_tree)
        self.assertEqual(bsp_tree.node_type, BSPNodeType.LEAF)
        self.assertEqual(len(bsp_tree.polygons), 2)


def run_tests():
    """Run all POF stability tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBSPNodeStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestBSPParsingRobustness))
    suite.addTests(loader.loadTestsFromTestCase(TestComplexBSPTrees))
    suite.addTests(loader.loadTestsFromTestCase(TestPOFParserIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)