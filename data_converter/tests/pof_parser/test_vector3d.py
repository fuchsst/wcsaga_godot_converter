#!/usr/bin/env python3
"""
Vector3D Tests - pytest tests for Vector3D functionality.
"""

import struct

import pytest

from data_converter.pof_parser.pof_types import Vector3D, ZERO_VECTOR


def test_vector3d_creation():
    """Test creating Vector3D instances."""
    # Test default creation
    v = Vector3D()
    assert v.x == 0.0
    assert v.y == 0.0
    assert v.z == 0.0

    # Test creation with values
    v = Vector3D(1.0, 2.0, 3.0)
    assert v.x == 1.0
    assert v.y == 2.0
    assert v.z == 3.0

    # Test creation with negative values
    v = Vector3D(-1.0, -2.0, -3.0)
    assert v.x == -1.0
    assert v.y == -2.0
    assert v.z == -3.0


def test_vector3d_from_bytes():
    """Test creating Vector3D from bytes."""
    # Test normal case
    data = struct.pack("<fff", 1.0, 2.0, 3.0)
    v = Vector3D.from_bytes(data)
    assert v.x == 1.0
    assert v.y == 2.0
    assert v.z == 3.0

    # Test with offset
    data = b"prefix" + struct.pack("<fff", 1.0, 2.0, 3.0)
    v = Vector3D.from_bytes(data, offset=6)
    assert v.x == 1.0
    assert v.y == 2.0
    assert v.z == 3.0

    # Test insufficient data
    data = struct.pack("<ff", 1.0, 2.0)  # Only 8 bytes instead of 12
    with pytest.raises(ValueError):
        Vector3D.from_bytes(data)


def test_vector3d_to_list():
    """Test converting Vector3D to list."""
    v = Vector3D(1.0, 2.0, 3.0)
    result = v.to_list()
    assert result == [1.0, 2.0, 3.0]


def test_vector3d_to_tuple():
    """Test converting Vector3D to tuple."""
    v = Vector3D(1.0, 2.0, 3.0)
    result = v.to_tuple()
    assert result == (1.0, 2.0, 3.0)


def test_vector3d_repr():
    """Test Vector3D string representation."""
    v = Vector3D(1.0, 2.0, 3.0)
    result = repr(v)
    assert "Vector3D(x=1.0000" in result
    assert "y=2.0000" in result
    assert "z=3.0000" in result


def test_vector3d_addition():
    """Test Vector3D addition."""
    v1 = Vector3D(1.0, 2.0, 3.0)
    v2 = Vector3D(4.0, 5.0, 6.0)
    result = v1 + v2
    assert isinstance(result, Vector3D)
    assert result.x == 5.0
    assert result.y == 7.0
    assert result.z == 9.0

    # Test with non-Vector3D (should return NotImplemented)
    result = v1.__add__("not a vector")
    assert result is NotImplemented


def test_vector3d_subtraction():
    """Test Vector3D subtraction."""
    v1 = Vector3D(4.0, 5.0, 6.0)
    v2 = Vector3D(1.0, 2.0, 3.0)
    result = v1 - v2
    assert isinstance(result, Vector3D)
    assert result.x == 3.0
    assert result.y == 3.0
    assert result.z == 3.0

    # Test with non-Vector3D (should return NotImplemented)
    result = v1.__sub__("not a vector")
    assert result is NotImplemented


def test_vector3d_multiplication():
    """Test Vector3D multiplication."""
    v = Vector3D(1.0, 2.0, 3.0)

    # Test scalar multiplication
    result = v * 2.0
    assert isinstance(result, Vector3D)
    assert result.x == 2.0
    assert result.y == 4.0
    assert result.z == 6.0

    # Test reverse multiplication
    result = 2.0 * v
    assert isinstance(result, Vector3D)
    assert result.x == 2.0
    assert result.y == 4.0
    assert result.z == 6.0

    # Test with non-numeric (should return NotImplemented)
    result = v.__mul__("not a number")
    assert result is NotImplemented


def test_vector3d_division():
    """Test Vector3D division."""
    v = Vector3D(2.0, 4.0, 6.0)

    # Test scalar division
    result = v / 2.0
    assert isinstance(result, Vector3D)
    assert result.x == 1.0
    assert result.y == 2.0
    assert result.z == 3.0

    # Test division by zero
    with pytest.raises(ZeroDivisionError):
        v / 0.0

    # Test with non-numeric (should return NotImplemented)
    result = v.__truediv__("not a number")
    assert result is NotImplemented


def test_vector3d_magnitude():
    """Test Vector3D magnitude calculations."""
    # Test zero vector
    v = Vector3D(0.0, 0.0, 0.0)
    assert v.magnitude_squared() == 0.0
    assert v.magnitude() == 0.0

    # Test unit vector
    v = Vector3D(1.0, 0.0, 0.0)
    assert v.magnitude_squared() == 1.0
    assert v.magnitude() == 1.0

    # Test diagonal vector
    v = Vector3D(3.0, 4.0, 0.0)
    assert v.magnitude_squared() == 25.0
    assert v.magnitude() == 5.0


def test_vector3d_normalize():
    """Test Vector3D normalization."""
    # Test normalizing non-zero vector
    v = Vector3D(3.0, 4.0, 0.0)
    normalized = v.normalize()
    assert isinstance(normalized, Vector3D)
    magnitude = normalized.magnitude()
    assert abs(magnitude - 1.0) < 1e-6

    # Test normalizing zero vector
    v = Vector3D(0.0, 0.0, 0.0)
    normalized = v.normalize()
    assert isinstance(normalized, Vector3D)
    assert normalized.x == 0.0
    assert normalized.y == 0.0
    assert normalized.z == 0.0


def test_vector3d_dot_product():
    """Test Vector3D dot product."""
    v1 = Vector3D(1.0, 2.0, 3.0)
    v2 = Vector3D(4.0, 5.0, 6.0)

    # Test normal dot product
    result = v1.dot(v2)
    expected = 1 * 4 + 2 * 5 + 3 * 6  # 4 + 10 + 18 = 32
    assert result == expected

    # Test with non-Vector3D (should raise TypeError)
    with pytest.raises(TypeError):
        v1.dot("not a vector")


def test_vector3d_cross_product():
    """Test Vector3D cross product."""
    v1 = Vector3D(1.0, 0.0, 0.0)
    v2 = Vector3D(0.0, 1.0, 0.0)

    # Test cross product
    result = v1.cross(v2)
    assert isinstance(result, Vector3D)
    assert result.x == 0.0
    assert result.y == 0.0
    assert result.z == 1.0

    # Test with non-Vector3D (should raise TypeError)
    with pytest.raises(TypeError):
        v1.cross("not a vector")


def test_vector3d_equality():
    """Test Vector3D equality comparison."""
    v1 = Vector3D(1.0, 2.0, 3.0)
    v2 = Vector3D(1.0, 2.0, 3.0)
    v3 = Vector3D(1.0, 2.0, 3.1)

    # Test equal vectors
    assert v1 == v2

    # Test unequal vectors
    assert not (v1 == v3)

    # Test comparison with non-Vector3D
    assert not (v1 == "not a vector")


def test_zero_vector():
    """Test ZERO_VECTOR constant."""
    assert isinstance(ZERO_VECTOR, Vector3D)
    assert ZERO_VECTOR.x == 0.0
    assert ZERO_VECTOR.y == 0.0
    assert ZERO_VECTOR.z == 0.0
