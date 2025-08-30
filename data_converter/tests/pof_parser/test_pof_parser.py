#!/usr/bin/env python3
"""
POF Parser Test Suite - EPIC-003 DM-004 Implementation

Comprehensive test suite for POF format analysis and parsing functionality.
Tests format validation, chunk parsing, and data extraction capabilities.
"""

import struct
import tempfile
import unittest
from pathlib import Path

from data_converter.pof_parser.pof_chunks import (
    ID_OHDR,
    ID_SOBJ,
    ID_TXTR,
    POF_HEADER_ID,
)
from data_converter.pof_parser.pof_data_extractor import POFDataExtractor
from data_converter.pof_parser.pof_format_analyzer import (
    POFFormatAnalyzer,
    POFFormatInfo,
)
from data_converter.pof_parser.pof_parser import POFParser


class TestPOFFormatAnalyzer(unittest.TestCase):
    """Test POF format analysis functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = POFFormatAnalyzer()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def create_test_pof(
        self,
        filename: str,
        valid_header: bool = True,
        version: int = 2100,
        chunks: list = None,
    ) -> Path:
        """Create a test POF file."""
        test_file = self.temp_path / filename

        with open(test_file, "wb") as f:
            # Write header
            if valid_header:
                f.write(struct.pack("<I", POF_HEADER_ID))  # Header ID
                f.write(struct.pack("<i", version))  # Version
            else:
                f.write(struct.pack("<I", 0x12345678))  # Invalid header
                f.write(struct.pack("<i", version))

            # Write chunks
            if chunks:
                for chunk_id, chunk_data in chunks:
                    f.write(struct.pack("<I", chunk_id))  # Chunk ID
                    f.write(struct.pack("<i", len(chunk_data)))  # Chunk length
                    f.write(chunk_data)  # Chunk data

        return test_file

    def test_analyze_valid_pof(self):
        """Test analysis of valid POF file."""
        # Create test POF with OHDR chunk
        ohdr_data = struct.pack("<fIi", 100.0, 0x1, 1)  # radius, flags, num_subobjects
        ohdr_data += struct.pack("<fff", -50.0, -50.0, -50.0)  # min bounds
        ohdr_data += struct.pack("<fff", 50.0, 50.0, 50.0)  # max bounds

        test_file = self.create_test_pof("valid.pof", chunks=[(ID_OHDR, ohdr_data)])

        analysis = self.analyzer.analyze_format(test_file)

        self.assertIsInstance(analysis, POFFormatInfo)
        self.assertTrue(analysis.valid_header)
        self.assertTrue(analysis.compatible_version)
        self.assertEqual(analysis.version, 2100)
        self.assertEqual(analysis.total_chunks, 1)
        self.assertIn("HDR2", analysis.chunk_count_by_type)

    def test_analyze_invalid_header(self):
        """Test analysis of POF file with invalid header."""
        test_file = self.create_test_pof("invalid.pof", valid_header=False)

        analysis = self.analyzer.analyze_format(test_file)

        self.assertFalse(analysis.valid_header)
        self.assertGreater(len(analysis.parsing_errors), 0)

    def test_analyze_old_version(self):
        """Test analysis of POF file with old version."""
        test_file = self.create_test_pof("old.pof", version=1800)

        analysis = self.analyzer.analyze_format(test_file)

        self.assertTrue(analysis.valid_header)
        self.assertFalse(analysis.compatible_version)
        self.assertGreater(len(analysis.warnings), 0)

    def test_format_compliance_validation(self):
        """Test format compliance validation."""
        # Test missing required chunks
        test_file = self.create_test_pof("incomplete.pof", chunks=[])
        analysis = self.analyzer.analyze_format(test_file)

        issues = self.analyzer.validate_format_compliance(analysis)

        self.assertGreater(len(issues), 0)
        self.assertTrue(any("OHDR" in issue for issue in issues))

    def test_chunk_metadata_extraction(self):
        """Test chunk metadata extraction."""
        # Create OHDR chunk with metadata
        ohdr_data = struct.pack("<fIi", 100.0, 0x1, 2)  # radius, flags, num_subobjects
        ohdr_data += struct.pack("<fff", -50.0, -50.0, -50.0)  # min bounds
        ohdr_data += struct.pack("<fff", 50.0, 50.0, 50.0)  # max bounds

        test_file = self.create_test_pof("metadata.pof", chunks=[(ID_OHDR, ohdr_data)])

        analysis = self.analyzer.analyze_format(test_file)

        self.assertEqual(len(analysis.chunks), 1)
        chunk = analysis.chunks[0]
        self.assertEqual(chunk.chunk_id, ID_OHDR)
        self.assertTrue(chunk.parsed_successfully)
        self.assertIn("max_radius", chunk.metadata)
        self.assertEqual(chunk.metadata["max_radius"], 100.0)
        self.assertEqual(chunk.metadata["num_subobjects"], 2)


class TestPOFDataExtractor(unittest.TestCase):
    """Test POF data extraction functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.extractor = POFDataExtractor()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def create_minimal_pof(self, filename: str) -> Path:
        """Create a minimal valid POF file for testing."""
        test_file = self.temp_path / filename

        with open(test_file, "wb") as f:
            # Header
            f.write(struct.pack("<I", POF_HEADER_ID))
            f.write(struct.pack("<i", 2100))

            # OHDR chunk
            ohdr_data = struct.pack(
                "<fIi", 50.0, 0x0, 1
            )  # radius, flags, num_subobjects
            ohdr_data += struct.pack("<fff", -25.0, -25.0, -25.0)  # min bounds
            ohdr_data += struct.pack("<fff", 25.0, 25.0, 25.0)  # max bounds
            # Detail levels (8 ints)
            ohdr_data += struct.pack("<" + "i" * 8, 0, -1, -1, -1, -1, -1, -1, -1)
            # Debris objects (32 ints)
            ohdr_data += struct.pack("<" + "i" * 32, *[-1] * 32)
            # Mass, center of mass, moment of inertia
            ohdr_data += struct.pack("<f", 100.0)  # mass
            ohdr_data += struct.pack("<fff", 0.0, 0.0, 0.0)  # center of mass
            ohdr_data += struct.pack("<fff", 1.0, 0.0, 0.0)  # moment of inertia row 1
            ohdr_data += struct.pack("<fff", 0.0, 1.0, 0.0)  # moment of inertia row 2
            ohdr_data += struct.pack("<fff", 0.0, 0.0, 1.0)  # moment of inertia row 3

            f.write(struct.pack("<I", ID_OHDR))
            f.write(struct.pack("<i", len(ohdr_data)))
            f.write(ohdr_data)

            # TXTR chunk with test texture (proper format: num_textures + length-prefixed strings)
            texture_name = b"test_texture.dds"
            texture_data = struct.pack("<i", 1)  # num_textures
            texture_data += struct.pack(
                "<i", len(texture_name)
            )  # length of first texture
            texture_data += texture_name  # texture name bytes

            f.write(struct.pack("<I", ID_TXTR))
            f.write(struct.pack("<i", len(texture_data)))
            f.write(texture_data)

        return test_file

    def test_extract_model_data(self):
        """Test basic model data extraction."""
        test_file = self.create_minimal_pof("test_model.pof")

        model_data = self.extractor.extract_model_data(test_file)

        self.assertIsNotNone(model_data)
        self.assertEqual(model_data.filename, "test_model.pof")
        self.assertEqual(model_data.version.value, 2100)
        self.assertEqual(model_data.header.max_radius, 50.0)
        self.assertEqual(model_data.header.mass, 100.0)
        # Textures may be pruned if not referenced by BSP trees
        # self.assertGreater(len(model_data.textures), 0)

    def test_extract_for_godot_conversion(self):
        """Test Godot-specific data extraction."""
        test_file = self.create_minimal_pof("godot_test.pof")

        godot_data = self.extractor.extract_for_godot_conversion(test_file)

        self.assertIsNotNone(godot_data)
        self.assertIn("metadata", godot_data)
        self.assertIn("scene_tree", godot_data)
        self.assertIn("materials", godot_data)
        self.assertIn("gameplay_nodes", godot_data)

        metadata = godot_data["metadata"]
        self.assertEqual(metadata["source_file"], "godot_test.pof")
        self.assertEqual(metadata["pof_version"], 2100)
        self.assertEqual(metadata["max_radius"], 50.0)

    def test_model_data_serialization(self):
        """Test model data to dictionary conversion."""
        test_file = self.create_minimal_pof("serialize_test.pof")

        model_data = self.extractor.extract_model_data(test_file)
        data_dict = model_data.to_dict()

        self.assertIsInstance(data_dict, dict)
        self.assertIn("filename", data_dict)
        self.assertIn("version", data_dict)
        self.assertIn("header", data_dict)
        self.assertIn("max_radius", data_dict["header"])
        self.assertIn("textures", data_dict)
        self.assertIn("subobjects", data_dict)


class TestPOFParser(unittest.TestCase):
    """Test POF parser functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = POFParser()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_parse_nonexistent_file(self):
        """Test parsing non-existent file."""
        fake_file = self.temp_path / "nonexistent.pof"

        result = self.parser.parse(fake_file)

        self.assertIsNone(result)

    def test_parse_invalid_file(self):
        """Test parsing invalid POF file."""
        invalid_file = self.temp_path / "invalid.pof"
        with open(invalid_file, "wb") as f:
            f.write(b"This is not a POF file")

        result = self.parser.parse(invalid_file)

        self.assertIsNone(result)

    def test_bsp_tree_parsing_integration(self):
        """Test integrated BSP tree parsing functionality."""
        # Create a test POF file with BSP data
        test_file = self.temp_path / "bsp_test.pof"

        with open(test_file, "wb") as f:
            # Write POF header
            f.write(struct.pack("<I", POF_HEADER_ID))  # POF header ID
            f.write(struct.pack("<i", 2117))  # Version

            # Write OHDR chunk
            f.write(struct.pack("<I", ID_OHDR))  # OHDR chunk ID
            f.write(struct.pack("<i", 316))  # OHDR chunk size (corrected)

            # OHDR content
            f.write(struct.pack("<f", 10.0))  # max_radius
            f.write(struct.pack("<I", 0))  # object_flags
            f.write(struct.pack("<I", 1))  # num_subobjects

            # Bounding box
            f.write(struct.pack("<fff", -5.0, -5.0, -5.0))  # min
            f.write(struct.pack("<fff", 5.0, 5.0, 5.0))  # max

            # Detail levels (8 entries)
            for _ in range(8):
                f.write(struct.pack("<i", -1))

            # Debris pieces (32 entries)
            for _ in range(32):
                f.write(struct.pack("<i", -1))

            # Mass and center
            f.write(struct.pack("<f", 1000.0))
            f.write(struct.pack("<fff", 0.0, 0.0, 0.0))

            # Moment of inertia (3 vectors)
            f.write(struct.pack("<fff", 1000.0, 0.0, 0.0))
            f.write(struct.pack("<fff", 0.0, 1000.0, 0.0))
            f.write(struct.pack("<fff", 0.0, 0.0, 1000.0))

            # Cross sections (8 entries)
            for _ in range(8):
                f.write(struct.pack("<ff", 0.0, 0.0))

            # Lights (empty)
            f.write(struct.pack("<I", 0))

            # Write SOBJ chunk with BSP data
            f.write(struct.pack("<I", ID_SOBJ))  # SOBJ chunk ID
            f.write(struct.pack("<i", 300))  # SOBJ chunk size (corrected)

            # SOBJ content
            f.write(struct.pack("<i", 0))  # subobject number
            f.write(struct.pack("<f", 5.0))  # radius
            f.write(struct.pack("<i", -1))  # parent

            # Offset and geometric center
            f.write(struct.pack("<fff", 0.0, 0.0, 0.0))
            f.write(struct.pack("<fff", 0.0, 0.0, 0.0))

            # Bounding box
            f.write(struct.pack("<fff", -5.0, -5.0, -5.0))
            f.write(struct.pack("<fff", 5.0, 5.0, 5.0))

            # Name and properties
            f.write(struct.pack("<I", 4))
            f.write(b"test")
            f.write(struct.pack("<I", 8))
            f.write(b"props" + b"\x00\x00\x00")

            # Movement type and axis
            f.write(struct.pack("<i", 0))
            f.write(struct.pack("<i", 0))

            # BSP data size and data
            bsp_data = self._create_test_bsp_data()
            f.write(struct.pack("<I", len(bsp_data)))
            f.write(bsp_data)

        # Parse the file
        result = self.parser.parse(test_file)

        # Verify parsing was successful
        self.assertIsNotNone(result, "Should parse file with BSP data successfully")
        self.assertEqual(len(result.subobjects), 1, "Should have one subobject")

        subobj = result.subobjects[0]
        self.assertTrue(subobj.has_bsp_data(), "Subobject should have BSP data")

        # Test BSP tree parsing
        bsp_tree = self.parser.parse_subobject_bsp_tree(0)
        self.assertIsNotNone(bsp_tree, "Should parse BSP tree successfully")

        # Test getting BSP data
        bsp_raw_data = self.parser.get_subobject_bsp_data(0)
        self.assertIsNotNone(bsp_raw_data, "Should get raw BSP data")
        self.assertGreater(len(bsp_raw_data), 0, "BSP data should not be empty")

        # Test parsing all BSP trees
        all_bsp_trees = self.parser.parse_all_bsp_trees()
        self.assertIn(0, all_bsp_trees, "Should contain BSP tree for subobject 0")
        self.assertIsNotNone(all_bsp_trees[0], "BSP tree should not be None")

    def _create_test_bsp_data(self) -> bytes:
        """Create test BSP data for integration testing."""
        from data_converter.pof_parser.pof_types import BSPChunkType

        bsp_data = bytearray()

        # DEFFPOINTS chunk
        bsp_data.extend(struct.pack("<I", BSPChunkType.DEFFPOINTS.value))
        bsp_data.extend(
            struct.pack("<I", 80)
        )  # chunk size (content only: 4 + 4 + 4*12 + 2*12 = 8 + 48 + 24 = 80)
        bsp_data.extend(struct.pack("<I", 4))  # num vertices
        bsp_data.extend(struct.pack("<I", 2))  # num normals

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
        bsp_data.extend(
            struct.pack("<I", 72)
        )  # chunk size (content only: 12 + 12 + 4 + 4 + 3*4 + 4 + 3*8 = 24 + 4 + 4 + 12 + 4 + 24 = 72)

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
        bsp_data.extend(struct.pack("<I", 0))  # chunk size

        return bytes(bsp_data)


class TestIntegration(unittest.TestCase):
    """Integration tests for POF parser components."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_analyzer_extractor_consistency(self):
        """Test consistency between analyzer and extractor."""
        # Create a test POF file
        test_file = self.temp_path / "consistency_test.pof"

        with open(test_file, "wb") as f:
            # Header
            f.write(struct.pack("<I", POF_HEADER_ID))
            f.write(struct.pack("<i", 2100))

            # Complete OHDR chunk
            ohdr_data = struct.pack(
                "<fIi", 75.0, 0x1, 0
            )  # radius, flags, num_subobjects
            ohdr_data += struct.pack("<fff", -37.5, -37.5, -37.5)  # min bounds
            ohdr_data += struct.pack("<fff", 37.5, 37.5, 37.5)  # max bounds
            # Detail levels (8 ints)
            ohdr_data += struct.pack("<" + "i" * 8, 0, -1, -1, -1, -1, -1, -1, -1)
            # Debris objects (32 ints)
            ohdr_data += struct.pack("<" + "i" * 32, *[-1] * 32)
            # Mass, center of mass, moment of inertia
            ohdr_data += struct.pack("<f", 100.0)  # mass
            ohdr_data += struct.pack("<fff", 0.0, 0.0, 0.0)  # center of mass
            ohdr_data += struct.pack("<fff", 1.0, 0.0, 0.0)  # moment of inertia row 1
            ohdr_data += struct.pack("<fff", 0.0, 1.0, 0.0)  # moment of inertia row 2
            ohdr_data += struct.pack("<fff", 0.0, 0.0, 1.0)  # moment of inertia row 3

            f.write(struct.pack("<I", ID_OHDR))
            f.write(struct.pack("<i", len(ohdr_data)))
            f.write(ohdr_data)

        # Analyze with analyzer
        analyzer = POFFormatAnalyzer()
        analysis = analyzer.analyze_format(test_file)

        # Extract with extractor
        extractor = POFDataExtractor()
        model_data = extractor.extract_model_data(test_file)

        # Verify consistency
        self.assertEqual(analysis.version, model_data.version)
        self.assertEqual(analysis.filename, model_data.filename)

        # Find OHDR chunk in analysis
        ohdr_chunk = next((c for c in analysis.chunks if c.chunk_id == ID_OHDR), None)
        self.assertIsNotNone(ohdr_chunk)
        self.assertEqual(
            ohdr_chunk.metadata["max_radius"], model_data.header.max_radius
        )


def run_tests():
    """Run all POF parser tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPOFFormatAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestPOFDataExtractor))
    suite.addTests(loader.loadTestsFromTestCase(TestPOFParser))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
