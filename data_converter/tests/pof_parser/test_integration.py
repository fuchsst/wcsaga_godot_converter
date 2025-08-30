#!/usr/bin/env python3
"""
Integration Tests - pytest tests for integration between binary reader and POF types.
"""

import struct
from io import BytesIO

import pytest

from data_converter.pof_parser.pof_binary_reader import POFBinaryReader
from data_converter.pof_parser.pof_types import (
    BoundingBox,
    POFVersion,
    BSPNodeType,
    BSPPolygon,
    BSPNode,
    Vector3D,
)


def test_binary_reader_with_pof_types():
    """Test that binary reader correctly creates POF types."""
    # Test reading Vector3D
    data = struct.pack("<fff", 1.0, 2.0, 3.0)
    f = BytesIO(data)
    reader = POFBinaryReader(f)
    result = reader.read_vector3d()

    assert hasattr(result, "x")
    assert hasattr(result, "y")
    assert hasattr(result, "z")
    assert result.x == 1.0
    assert result.y == 2.0
    assert result.z == 3.0


def test_complex_bsp_node_creation():
    """Test creating complex BSP node structures."""
    # Create a simple BSP tree structure
    normal = Vector3D(0.0, 0.0, 1.0)

    # Create leaf node with polygon
    vertices = [
        Vector3D(0.0, 0.0, 0.0),
        Vector3D(1.0, 0.0, 0.0),
        Vector3D(1.0, 1.0, 0.0),
    ]

    polygon = BSPPolygon(
        vertices=vertices, normal=normal, plane_distance=0.0, texture_index=0
    )

    leaf_node = BSPNode(
        node_type=BSPNodeType.LEAF,
        normal=normal,
        plane_distance=0.0,
        polygons=[polygon],
    )

    # Create parent node
    parent_node = BSPNode(
        node_type=BSPNodeType.NODE,
        normal=normal,
        plane_distance=0.0,
        front_child=leaf_node,
        back_child=None,
    )

    # Verify structure
    assert parent_node.node_type == BSPNodeType.NODE
    assert parent_node.front_child is not None
    assert parent_node.front_child.node_type == BSPNodeType.LEAF
    assert len(parent_node.front_child.polygons) == 1
    assert parent_node.front_child.polygons[0].texture_index == 0


def test_bounding_box_with_vector3d():
    """Test BoundingBox integration with Vector3D."""
    min_vec = Vector3D(-5.0, -10.0, -15.0)
    max_vec = Vector3D(5.0, 10.0, 15.0)
    bbox = BoundingBox(min=min_vec, max=max_vec)

    # Test properties
    assert isinstance(bbox.min, Vector3D)
    assert isinstance(bbox.max, Vector3D)

    # Test calculations
    center = bbox.center()
    assert isinstance(center, Vector3D)
    assert center.x == 0.0
    assert center.y == 0.0
    assert center.z == 0.0

    size = bbox.size()
    assert isinstance(size, Vector3D)
    assert size.x == 10.0
    assert size.y == 20.0
    assert size.z == 30.0


def test_pof_version_compatibility():
    """Test POF version compatibility functionality."""
    # Test valid version
    version = POFVersion.from_int(2117)
    assert version == POFVersion.VERSION_2117

    # Test that version is within compatible range
    assert version.value >= POFVersion.MIN_COMPATIBLE.value
    assert version.value <= POFVersion.MAX_COMPATIBLE.value


def test_bsp_polygon_with_vectors():
    """Test BSPPolygon integration with Vector3D objects."""
    # Create vertices
    vertices = [
        Vector3D(0.0, 0.0, 0.0),
        Vector3D(1.0, 0.0, 0.0),
        Vector3D(1.0, 1.0, 0.0),
        Vector3D(0.0, 1.0, 0.0),
    ]

    # Create normal
    normal = Vector3D(0.0, 0.0, 1.0).normalize()

    # Create polygon
    polygon = BSPPolygon(
        vertices=vertices, normal=normal, plane_distance=0.0, texture_index=5
    )

    # Verify all vertices are Vector3D objects
    for vertex in polygon.vertices:
        assert isinstance(vertex, Vector3D)

    # Verify normal is Vector3D
    assert isinstance(polygon.normal, Vector3D)

    # Verify normal is normalized
    assert abs(polygon.normal.length() - 1.0) < 1e-6

    # Verify texture index
    assert polygon.texture_index == 5


def test_bsp_node_hierarchy():
    """Test BSP node hierarchy creation and traversal."""
    # Create a simple tree: root -> left_leaf, right_leaf
    normal = Vector3D(0.0, 0.0, 1.0)

    # Create leaf nodes
    left_leaf = BSPNode(node_type=BSPNodeType.LEAF, normal=normal, plane_distance=0.0)

    right_leaf = BSPNode(node_type=BSPNodeType.LEAF, normal=normal, plane_distance=0.0)

    # Create root node
    root = BSPNode(
        node_type=BSPNodeType.NODE,
        normal=normal,
        plane_distance=0.0,
        front_child=left_leaf,
        back_child=right_leaf,
    )

    # Verify hierarchy
    assert root.node_type == BSPNodeType.NODE
    assert root.front_child == left_leaf
    assert root.back_child == right_leaf
    assert left_leaf.is_leaf()
    assert right_leaf.is_leaf()
    assert not root.is_leaf()


if __name__ == "__main__":
    pytest.main([__file__])
