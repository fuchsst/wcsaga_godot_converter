#!/usr/bin/env python3
"""
POF Types Tests - pytest tests for enhanced POF type definitions.
"""


from data_converter.pof_parser.pof_types import (
    Vector3D,
    BoundingBox,
    POFVersion,
    BSPNodeType,
    MovementType,
    MovementAxis,
    BSPPolygon,
    BSPNode,
    POFHeader,
    SubObject,
)


def test_pof_version_enum():
    """Test POFVersion enumeration."""
    # Test known versions
    assert POFVersion.VERSION_1800.value == 1800
    assert POFVersion.VERSION_2100.value == 2100
    assert POFVersion.VERSION_2112.value == 2112
    assert POFVersion.VERSION_2117.value == 2117

    # Test compatibility constants
    assert POFVersion.MIN_COMPATIBLE.value == 1800
    assert POFVersion.MAX_COMPATIBLE.value == 2117

    # Test from_int method
    version = POFVersion.from_int(2117)
    assert version == POFVersion.VERSION_2117

    # Test fallback for unknown version
    version = POFVersion.from_int(9999)
    # Should return closest valid version
    assert isinstance(version, POFVersion)


def test_vector3d_enhanced():
    """Test enhanced Vector3D functionality."""
    # Test basic creation
    v = Vector3D(1.0, 2.0, 3.0)
    assert v.x == 1.0
    assert v.y == 2.0
    assert v.z == 3.0

    # Test arithmetic operations
    v1 = Vector3D(1.0, 2.0, 3.0)
    v2 = Vector3D(4.0, 5.0, 6.0)

    # Addition
    result = v1 + v2
    assert result.x == 5.0
    assert result.y == 7.0
    assert result.z == 9.0

    # Subtraction
    result = v2 - v1
    assert result.x == 3.0
    assert result.y == 3.0
    assert result.z == 3.0

    # Scalar multiplication
    result = v1 * 2.0
    assert result.x == 2.0
    assert result.y == 4.0
    assert result.z == 6.0

    # Length calculation
    v = Vector3D(3.0, 4.0, 0.0)
    assert abs(v.length() - 5.0) < 1e-6

    # Normalization
    v = Vector3D(3.0, 4.0, 0.0)
    normalized = v.normalize()
    assert abs(normalized.length() - 1.0) < 1e-6

    # Dot product
    v1 = Vector3D(1.0, 2.0, 3.0)
    v2 = Vector3D(4.0, 5.0, 6.0)
    dot_product = v1.dot(v2)
    assert dot_product == 32.0  # 1*4 + 2*5 + 3*6

    # Cross product
    v1 = Vector3D(1.0, 0.0, 0.0)
    v2 = Vector3D(0.0, 1.0, 0.0)
    cross_product = v1.cross(v2)
    assert cross_product.x == 0.0
    assert cross_product.y == 0.0
    assert cross_product.z == 1.0


def test_bounding_box():
    """Test BoundingBox functionality."""
    min_vec = Vector3D(-1.0, -2.0, -3.0)
    max_vec = Vector3D(1.0, 2.0, 3.0)
    bbox = BoundingBox(min=min_vec, max=max_vec)

    # Test properties
    assert bbox.min == min_vec
    assert bbox.max == max_vec

    # Test center calculation
    center = bbox.center()
    assert center.x == 0.0
    assert center.y == 0.0
    assert center.z == 0.0

    # Test size calculation
    size = bbox.size()
    assert size.x == 2.0
    assert size.y == 4.0
    assert size.z == 6.0

    # Test volume calculation
    volume = bbox.volume()
    assert volume == 48.0  # 2 * 4 * 6

    # Test point containment
    inside_point = Vector3D(0.0, 0.0, 0.0)
    outside_point = Vector3D(2.0, 0.0, 0.0)
    assert bbox.contains_point(inside_point)
    assert not bbox.contains_point(outside_point)

    # Test intersection
    other_min = Vector3D(0.0, 0.0, 0.0)
    other_max = Vector3D(2.0, 2.0, 2.0)
    other_bbox = BoundingBox(min=other_min, max=other_max)
    assert bbox.intersects(other_bbox)

    non_intersecting_min = Vector3D(5.0, 5.0, 5.0)
    non_intersecting_max = Vector3D(6.0, 6.0, 6.0)
    non_intersecting_bbox = BoundingBox(
        min=non_intersecting_min, max=non_intersecting_max
    )
    assert not bbox.intersects(non_intersecting_bbox)


def test_bsp_polygon():
    """Test BSPPolygon functionality."""
    vertices = [
        Vector3D(0.0, 0.0, 0.0),
        Vector3D(1.0, 0.0, 0.0),
        Vector3D(1.0, 1.0, 0.0),
        Vector3D(0.0, 1.0, 0.0),
    ]
    normal = Vector3D(0.0, 0.0, 1.0)
    polygon = BSPPolygon(
        vertices=vertices, normal=normal, plane_distance=0.0, texture_index=0
    )

    # Test properties
    assert len(polygon.vertices) == 4
    assert polygon.normal == normal
    assert polygon.plane_distance == 0.0
    assert polygon.texture_index == 0

    # Test area calculation
    area = polygon.area()
    # For a unit square, area should be 1.0
    assert abs(area - 1.0) < 1e-6


def test_bsp_node():
    """Test BSPNode functionality."""
    normal = Vector3D(0.0, 0.0, 1.0)
    node = BSPNode(node_type=BSPNodeType.NODE, normal=normal, plane_distance=0.0)

    # Test properties
    assert node.node_type == BSPNodeType.NODE
    assert node.normal == normal
    assert node.plane_distance == 0.0
    assert node.front_child is None
    assert node.back_child is None
    assert node.polygons == []

    # Test type checking methods
    assert not node.is_leaf()
    assert not node.is_empty()

    # Test leaf node
    leaf_node = BSPNode(
        node_type=BSPNodeType.LEAF, normal=Vector3D(0.0, 0.0, 1.0), plane_distance=0.0
    )
    assert leaf_node.is_leaf()
    assert not leaf_node.is_empty()


def test_pof_header():
    """Test POFHeader functionality."""
    # Create required components
    bbox = BoundingBox(min=Vector3D(-1.0, -1.0, -1.0), max=Vector3D(1.0, 1.0, 1.0))

    moment_of_inertia = [
        Vector3D(1.0, 0.0, 0.0),
        Vector3D(0.0, 1.0, 0.0),
        Vector3D(0.0, 0.0, 1.0),
    ]

    header = POFHeader(
        version=POFVersion.VERSION_2117,
        max_radius=10.0,
        object_flags=0,
        num_subobjects=5,
        bounding_box=bbox,
        detail_levels=[0, 1, 2, -1, -1, -1, -1, -1],
        debris_pieces=[-1] * 32,
        mass=100.0,
        mass_center=Vector3D(0.0, 0.0, 0.0),
        moment_of_inertia=moment_of_inertia,
        cross_sections=[(0.0, 1.0), (1.0, 0.5)],
        lights=[],
    )

    # Test properties
    assert header.version == POFVersion.VERSION_2117
    assert header.max_radius == 10.0
    assert header.num_subobjects == 5
    assert header.bounding_box == bbox
    assert len(header.detail_levels) == 8
    assert len(header.debris_pieces) == 32
    assert header.mass == 100.0


def test_subobject():
    """Test SubObject functionality."""
    bbox = BoundingBox(min=Vector3D(-1.0, -1.0, -1.0), max=Vector3D(1.0, 1.0, 1.0))

    subobj = SubObject(
        number=1,
        radius=5.0,
        parent=-1,
        offset=Vector3D(0.0, 0.0, 0.0),
        geometric_center=Vector3D(0.0, 0.0, 0.0),
        bounding_box=bbox,
        name="TestSubobject",
        properties="",
        movement_type=MovementType.STATIC,
        movement_axis=MovementAxis.NONE,
        bsp_data_size=100,
        bsp_data_offset=2000,
    )

    # Test properties
    assert subobj.number == 1
    assert subobj.radius == 5.0
    assert subobj.parent == -1
    assert subobj.name == "TestSubobject"
    assert subobj.movement_type == MovementType.STATIC
    assert subobj.movement_axis == MovementAxis.NONE
    assert subobj.bsp_data_size == 100
    assert subobj.bsp_data_offset == 2000

    # Test BSP data check
    assert subobj.has_bsp_data()

    # Test subobject without BSP data
    subobj_no_bsp = SubObject(
        number=2,
        radius=3.0,
        parent=-1,
        offset=Vector3D(0.0, 0.0, 0.0),
        geometric_center=Vector3D(0.0, 0.0, 0.0),
        bounding_box=bbox,
        name="TestSubobject2",
        properties="",
        movement_type=MovementType.STATIC,
        movement_axis=MovementAxis.NONE,
        bsp_data_size=0,
        bsp_data_offset=-1,
    )
    assert not subobj_no_bsp.has_bsp_data()
