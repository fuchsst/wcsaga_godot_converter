#!/usr/bin/env python3
"""
Binary Reader Tests - pytest tests for unified binary reader functionality.
"""

import struct
import unittest
from io import BytesIO

from data_converter.pof_parser.pof_binary_reader import (
    POFBinaryReader,
    create_reader,
    read_int,
    read_uint,
    read_float,
    read_vector,
    read_string_len,
)
from data_converter.pof_parser.pof_types import Vector3D


class TestPOFBinaryReader(unittest.TestCase):
    """Test POF binary reader functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Create test data buffer
        self.test_data = BytesIO()
        self.reader = POFBinaryReader(self.test_data)

    def test_create_reader(self):
        """Test creating a binary reader."""
        f = BytesIO(b"test")
        reader = create_reader(f)
        self.assertIsInstance(reader, POFBinaryReader)
        self.assertEqual(reader.file_handle, f)

    def test_read_int32(self):
        """Test reading signed 32-bit integers."""
        # Test positive value
        data = struct.pack("<i", 12345)
        f = BytesIO(data)
        reader = POFBinaryReader(f)
        result = reader.read_int32()
        self.assertEqual(result, 12345)

        # Test negative value
        data = struct.pack("<i", -12345)
        f = BytesIO(data)
        reader = POFBinaryReader(f)
        result = reader.read_int32()
        self.assertEqual(result, -12345)

        # Test zero
        data = struct.pack("<i", 0)
        f = BytesIO(data)
        reader = POFBinaryReader(f)
        result = reader.read_int32()
        self.assertEqual(result, 0)

    def test_read_uint32(self):
        """Test reading unsigned 32-bit integers."""
        # Test regular value
        data = struct.pack("<I", 12345)
        f = BytesIO(data)
        reader = POFBinaryReader(f)
        result = reader.read_uint32()
        self.assertEqual(result, 12345)

        # Test large value
        data = struct.pack("<I", 0xFFFFFFFF)
        f = BytesIO(data)
        reader = POFBinaryReader(f)
        result = reader.read_uint32()
        self.assertEqual(result, 0xFFFFFFFF)

    def test_read_float32(self):
        """Test reading 32-bit floats."""
        # Test positive float
        data = struct.pack("<f", 3.14159)
        f = BytesIO(data)
        reader = POFBinaryReader(f)
        result = reader.read_float32()
        self.assertAlmostEqual(result, 3.14159, places=5)

        # Test negative float
        data = struct.pack("<f", -2.71828)
        f = BytesIO(data)
        reader = POFBinaryReader(f)
        result = reader.read_float32()
        self.assertAlmostEqual(result, -2.71828, places=5)

        # Test zero
        data = struct.pack("<f", 0.0)
        f = BytesIO(data)
        reader = POFBinaryReader(f)
        result = reader.read_float32()
        self.assertEqual(result, 0.0)

    def test_read_vector3d(self):
        """Test reading Vector3D objects."""
        # Test regular vector
        data = struct.pack("<fff", 1.0, 2.0, 3.0)
        f = BytesIO(data)
        reader = POFBinaryReader(f)
        result = reader.read_vector3d()
        self.assertIsInstance(result, Vector3D)
        self.assertAlmostEqual(result.x, 1.0, places=5)
        self.assertAlmostEqual(result.y, 2.0, places=5)
        self.assertAlmostEqual(result.z, 3.0, places=5)

        # Test zero vector
        data = struct.pack("<fff", 0.0, 0.0, 0.0)
        f = BytesIO(data)
        reader = POFBinaryReader(f)
        result = reader.read_vector3d()
        self.assertIsInstance(result, Vector3D)
        self.assertEqual(result.x, 0.0)
        self.assertEqual(result.y, 0.0)
        self.assertEqual(result.z, 0.0)

        # Test negative vector
        data = struct.pack("<fff", -1.0, -2.0, -3.0)
        f = BytesIO(data)
        reader = POFBinaryReader(f)
        result = reader.read_vector3d()
        self.assertIsInstance(result, Vector3D)
        self.assertAlmostEqual(result.x, -1.0, places=5)
        self.assertAlmostEqual(result.y, -2.0, places=5)
        self.assertAlmostEqual(result.z, -3.0, places=5)

    def test_read_length_prefixed_string(self):
        """Test reading length-prefixed strings."""
        # Test regular string
        test_string = "Hello, World!"
        data = struct.pack("<I", len(test_string))
        data += test_string.encode("utf-8")
        f = BytesIO(data)
        reader = POFBinaryReader(f)
        result = reader.read_length_prefixed_string()
        self.assertEqual(result, test_string)

        # Test empty string
        data = struct.pack("<I", 0)
        f = BytesIO(data)
        reader = POFBinaryReader(f)
        result = reader.read_length_prefixed_string()
        self.assertEqual(result, "")

    def test_read_chunk_header(self):
        """Test reading chunk headers."""
        from data_converter.pof_parser.pof_chunks import ID_OHDR

        # Test regular chunk header
        data = struct.pack("<II", ID_OHDR, 100)
        f = BytesIO(data)
        reader = POFBinaryReader(f)
        chunk_id, chunk_len = reader.read_chunk_header()
        self.assertEqual(chunk_id, ID_OHDR)
        self.assertEqual(chunk_len, 100)

    def test_backward_compatibility_functions(self):
        """Test backward compatibility functions."""
        # Test read_int
        data = struct.pack("<i", 12345)
        f = BytesIO(data)
        result = read_int(f)
        self.assertEqual(result, 12345)

        # Test read_uint
        data = struct.pack("<I", 12345)
        f = BytesIO(data)
        result = read_uint(f)
        self.assertEqual(result, 12345)

        # Test read_float
        data = struct.pack("<f", 3.14159)
        f = BytesIO(data)
        result = read_float(f)
        self.assertAlmostEqual(result, 3.14159, places=5)

        # Test read_vector
        data = struct.pack("<fff", 1.0, 2.0, 3.0)
        f = BytesIO(data)
        result = read_vector(f)
        self.assertIsInstance(result, Vector3D)
        self.assertAlmostEqual(result.x, 1.0, places=5)
        self.assertAlmostEqual(result.y, 2.0, places=5)
        self.assertAlmostEqual(result.z, 3.0, places=5)

        # Test read_string_len
        test_string = "Hello, World!"
        data = struct.pack("<I", len(test_string))
        data += test_string.encode("utf-8")
        f = BytesIO(data)
        result = read_string_len(f, 1024)
        self.assertEqual(result, test_string)


if __name__ == "__main__":
    unittest.main()
