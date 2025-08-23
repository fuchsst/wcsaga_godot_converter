#!/usr/bin/env python3
"""
Enhanced POF Type Definitions - Strongly typed data structures for POF parsing.

Replaces dictionary-based structures with proper dataclasses for type safety
and validation, matching Rust reference implementation patterns.
"""

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime


class POFVersion(IntEnum):
    """POF version enumeration with enhanced validation."""
    VERSION_1800 = 1800  # FS1 format
    VERSION_2100 = 2100  # FS2 format
    VERSION_2112 = 2112  # FS2 with enhancements
    VERSION_2117 = 2117  # Current WCS format
    
    MIN_COMPATIBLE = 1800
    MAX_COMPATIBLE = 2117
    
    @classmethod
    def from_int(cls, version: int) -> 'POFVersion':
        """Convert integer version to enum with validation."""
        try:
            return cls(version)
        except ValueError:
            # Find closest valid version
            valid_versions = [v.value for v in cls]
            closest = min(valid_versions, key=lambda x: abs(x - version))
            return cls(closest)


class BSPNodeType(IntEnum):
    """BSP node types with enhanced documentation."""
    NODE = 0      # Internal node with splitting plane
    LEAF = 1      # Leaf node containing polygons
    EMPTY = 2     # Empty node (no geometry)


class ModelType(Enum):
    """Model type classification with gameplay context."""
    SHIP = "ship"
    STATION = "station" 
    DEBRIS = "debris"
    WEAPON = "weapon"
    EFFECT = "effect"
    ASTEROID = "asteroid"
    UNKNOWN = "unknown"


class MovementType(IntEnum):
    """Subobject movement types."""
    STATIC = 0        # No movement
    ROTATION = 1      # Rotates around axis
    TRANSLATION = 2   # Moves along axis
    COMPLEX = 3       # Complex movement


class MovementAxis(IntEnum):
    """Movement axes for subobjects."""
    X = 0
    Y = 1  
    Z = 2
    NONE = 3


@dataclass
class Vector3D:
    """Enhanced 3D vector with comprehensive validation and operations."""
    x: float
    y: float
    z: float
    
    def __post_init__(self):
        """Validate vector components and ensure numeric values."""
        if not all(isinstance(v, (int, float)) for v in [self.x, self.y, self.z]):
            raise ValueError("Vector components must be numeric")
        
        # Check for NaN or infinity
        if any(not isinstance(v, (int, float)) or not abs(v) < float('inf') for v in [self.x, self.y, self.z]):
            raise ValueError("Vector components must be finite numbers")
    
    def to_list(self) -> List[float]:
        """Convert to list format for serialization."""
        return [self.x, self.y, self.z]
    
    def to_tuple(self) -> Tuple[float, float, float]:
        """Convert to tuple format."""
        return (self.x, self.y, self.z)
    
    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float) -> 'Vector3D':
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __rmul__(self, scalar: float) -> 'Vector3D':
        return self.__mul__(scalar)
    
    def length(self) -> float:
        """Calculate vector length."""
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5
    
    def normalize(self) -> 'Vector3D':
        """Normalize vector to unit length."""
        length = self.length()
        if length == 0:
            return Vector3D(0, 0, 0)
        return self * (1.0 / length)
    
    def dot(self, other: 'Vector3D') -> float:
        """Dot product with another vector."""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other: 'Vector3D') -> 'Vector3D':
        """Cross product with another vector."""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector3D):
            return False
        return (abs(self.x - other.x) < 1e-6 and 
                abs(self.y - other.y) < 1e-6 and 
                abs(self.z - other.z) < 1e-6)


@dataclass
class BoundingBox:
    """Axis-aligned bounding box with comprehensive validation."""
    min: Vector3D
    max: Vector3D
    
    def __post_init__(self):
        """Validate bounding box consistency."""
        if not (isinstance(self.min, Vector3D) and isinstance(self.max, Vector3D)):
            raise ValueError("Bounding box requires Vector3D objects")
        
        # Ensure min <= max for all components
        if (self.min.x > self.max.x or 
            self.min.y > self.max.y or 
            self.min.z > self.max.z):
            raise ValueError("Bounding box min must be <= max for all components")
    
    def center(self) -> Vector3D:
        """Calculate center point."""
        return Vector3D(
            (self.min.x + self.max.x) / 2,
            (self.min.y + self.max.y) / 2,
            (self.min.z + self.max.z) / 2
        )
    
    def size(self) -> Vector3D:
        """Calculate size vector."""
        return Vector3D(
            self.max.x - self.min.x,
            self.max.y - self.min.y,
            self.max.z - self.min.z
        )
    
    def volume(self) -> float:
        """Calculate volume of bounding box."""
        size = self.size()
        return size.x * size.y * size.z
    
    def contains_point(self, point: Vector3D) -> bool:
        """Check if point is inside bounding box."""
        return (self.min.x <= point.x <= self.max.x and
                self.min.y <= point.y <= self.max.y and
                self.min.z <= point.z <= self.max.z)
    
    def intersects(self, other: 'BoundingBox') -> bool:
        """Check if two bounding boxes intersect."""
        return not (other.max.x < self.min.x or
                   other.min.x > self.max.x or
                   other.max.y < self.min.y or
                   other.min.y > self.max.y or
                   other.max.z < self.min.z or
                   other.min.z > self.max.z)


@dataclass
class BSPPolygon:
    """BSP polygon with comprehensive validation."""
    vertices: List[Vector3D]
    normal: Vector3D
    plane_distance: float
    texture_index: int
    
    def __post_init__(self):
        """Validate polygon data integrity."""
        if len(self.vertices) < 3:
            raise ValueError("Polygon must have at least 3 vertices")
        if not isinstance(self.normal, Vector3D):
            raise ValueError("Normal must be a Vector3D")
        if not isinstance(self.plane_distance, (int, float)):
            raise ValueError("Plane distance must be numeric")
        if not isinstance(self.texture_index, int):
            raise ValueError("Texture index must be integer")
        if self.texture_index < 0:
            raise ValueError("Texture index cannot be negative")
        
        # Validate normal is unit length
        normal_length = self.normal.length()
        if abs(normal_length - 1.0) > 1e-3:
            raise ValueError(f"Normal must be unit length, got {normal_length}")
    
    def area(self) -> float:
        """Calculate polygon area."""
        if len(self.vertices) < 3:
            return 0.0
        
        # Use shoelace formula for area calculation
        total = Vector3D(0, 0, 0)
        for i in range(len(self.vertices)):
            j = (i + 1) % len(self.vertices)
            total += self.vertices[i].cross(self.vertices[j])
        
        return abs(total.dot(self.normal)) / 2.0


@dataclass
class BSPNode:
    """BSP tree node with plane and children."""
    node_type: BSPNodeType
    normal: Vector3D
    plane_distance: float
    front_child: Optional['BSPNode'] = None
    back_child: Optional['BSPNode'] = None
    polygons: List[BSPPolygon] = field(default_factory=list)
    bbox: Optional[BoundingBox] = None
    
    def __post_init__(self):
        """Validate BSP node consistency."""
        if not isinstance(self.node_type, BSPNodeType):
            raise ValueError("Node type must be BSPNodeType")
        if not isinstance(self.normal, Vector3D):
            raise ValueError("Normal must be a Vector3D")
        if not isinstance(self.plane_distance, (int, float)):
            raise ValueError("Plane distance must be numeric")
        if self.bbox is not None and not isinstance(self.bbox, BoundingBox):
            raise ValueError("Bounding box must be BoundingBox or None")
        
        # Validate normal is unit length for splitting nodes
        if self.node_type == BSPNodeType.NODE:
            normal_length = self.normal.length()
            if abs(normal_length - 1.0) > 1e-3:
                raise ValueError(f"Splitting normal must be unit length, got {normal_length}")
    
    def is_leaf(self) -> bool:
        """Check if this is a leaf node."""
        return self.node_type == BSPNodeType.LEAF
    
    def is_empty(self) -> bool:
        """Check if this is an empty node."""
        return self.node_type == BSPNodeType.EMPTY


@dataclass
class POFHeader:
    """Complete POF header data structure with validation."""
    version: POFVersion
    max_radius: float
    object_flags: int
    num_subobjects: int
    bounding_box: BoundingBox
    detail_levels: List[int]
    debris_pieces: List[int]
    mass: float
    mass_center: Vector3D
    moment_of_inertia: List[Vector3D]  # 3x3 matrix as vectors
    cross_sections: List[Tuple[float, float]]  # (depth, radius)
    lights: List[Dict[str, Any]]
    
    def __post_init__(self):
        """Validate header data integrity."""
        if not isinstance(self.version, POFVersion):
            raise ValueError("Version must be POFVersion")
        if self.max_radius < 0:
            raise ValueError("Max radius cannot be negative")
        if self.num_subobjects < 0:
            raise ValueError("Number of subobjects cannot be negative")
        if not isinstance(self.bounding_box, BoundingBox):
            raise ValueError("Bounding box must be BoundingBox")
        if len(self.moment_of_inertia) != 3:
            raise ValueError("Moment of inertia must be 3 vectors")
        if self.mass < 0:
            raise ValueError("Mass cannot be negative")
        
        # Validate detail levels
        if len(self.detail_levels) != 8:
            raise ValueError("Must have exactly 8 detail levels")
        
        # Validate debris pieces
        if len(self.debris_pieces) != 32:
            raise ValueError("Must have exactly 32 debris pieces")
        
        # Validate cross sections
        for depth, radius in self.cross_sections:
            if depth < 0 or radius < 0:
                raise ValueError("Cross section depth and radius cannot be negative")


@dataclass
class SubObject:
    """Subobject data structure with comprehensive validation."""
    number: int
    radius: float
    parent: int
    offset: Vector3D
    geometric_center: Vector3D
    bounding_box: BoundingBox
    name: str
    properties: str
    movement_type: MovementType
    movement_axis: MovementAxis
    bsp_data_size: int
    bsp_data_offset: int
    bsp_tree: Optional[BSPNode] = None
    
    def __post_init__(self):
        """Validate subobject data integrity."""
        if self.number < 0:
            raise ValueError("Subobject number cannot be negative")
        if self.radius < 0:
            raise ValueError("Radius cannot be negative")
        if not isinstance(self.offset, Vector3D):
            raise ValueError("Offset must be Vector3D")
        if not isinstance(self.geometric_center, Vector3D):
            raise ValueError("Geometric center must be Vector3D")
        if not isinstance(self.bounding_box, BoundingBox):
            raise ValueError("Bounding box must be BoundingBox")
        if not isinstance(self.movement_type, MovementType):
            raise ValueError("Movement type must be MovementType")
        if not isinstance(self.movement_axis, MovementAxis):
            raise ValueError("Movement axis must be MovementAxis")
        if self.bsp_data_size < 0:
            raise ValueError("BSP data size cannot be negative")
        if self.bsp_data_offset < -1:
            raise ValueError("BSP data offset cannot be less than -1")
    
    def has_bsp_data(self) -> bool:
        """Check if subobject has BSP data."""
        return self.bsp_data_size > 0 and self.bsp_data_offset >= 0


@dataclass
class SpecialPoint:
    """Special point data structure (gun points, missile points, etc.)."""
    name: str
    position: Vector3D
    normal: Vector3D
    point_type: str  # gun, missile, docking, thruster, etc.
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate special point data."""
        if not isinstance(self.position, Vector3D):
            raise ValueError("Position must be Vector3D")
        if not isinstance(self.normal, Vector3D):
            raise ValueError("Normal must be Vector3D")
        if not self.point_type:
            raise ValueError("Point type cannot be empty")


@dataclass
class PathNode:
    """Path node for animation paths."""
    position: Vector3D
    rotation: Vector3D  # Euler angles or quaternion components
    time: float
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnimationPath:
    """Complete animation path."""
    name: str
    nodes: List[PathNode]
    loop: bool
    duration: float


@dataclass
class ShieldMesh:
    """Shield mesh data structure."""
    vertices: List[Vector3D]
    normals: List[Vector3D]
    polygons: List[BSPPolygon]
    collision_tree: Optional[BSPNode] = None


@dataclass
class InsigniaData:
    """Ship insignia/logo data."""
    texture_index: int
    position: Vector3D
    size: Vector3D
    rotation: Vector3D


@dataclass
class GlowBank:
    """Glow bank/light data."""
    position: Vector3D
    normal: Vector3D
    radius: float
    color: Tuple[float, float, float, float]  # RGBA
    intensity: float


@dataclass
class POFModelDataEnhanced:
    """Complete enhanced POF model data structure."""
    filename: str
    version: POFVersion
    header: POFHeader
    textures: List[str]
    subobjects: List[SubObject]
    special_points: List[SpecialPoint]
    paths: List[AnimationPath]
    gun_points: List[SpecialPoint]
    missile_points: List[SpecialPoint]
    docking_points: List[SpecialPoint]
    thrusters: List[SpecialPoint]
    shield_mesh: Optional[ShieldMesh]
    eye_points: List[SpecialPoint]
    insignia: List[InsigniaData]
    autocenter: Optional[Vector3D]
    glow_banks: List[GlowBank]
    shield_collision_tree: Optional[BSPNode]
    
    def __post_init__(self):
        """Validate complete model data consistency."""
        # Check version compatibility
        if self.version < POFVersion.MIN_COMPATIBLE:
            raise ValueError(f"Version {self.version} is below minimum compatible version {POFVersion.MIN_COMPATIBLE}")
        
        # Check subobject consistency
        if len(self.subobjects) != self.header.num_subobjects:
            raise ValueError(f"Header reports {self.header.num_subobjects} subobjects but found {len(self.subobjects)}")
        
        # Check texture references
        texture_indices = set()
        for subobj in self.subobjects:
            if subobj.bsp_tree:
                texture_indices.update(self._get_texture_indices_from_bsp(subobj.bsp_tree))
        
        for tex_idx in texture_indices:
            if tex_idx >= len(self.textures):
                raise ValueError(f"Subobject references invalid texture index {tex_idx}")
    
    def _get_texture_indices_from_bsp(self, node: BSPNode) -> set:
        """Recursively get all texture indices from BSP tree."""
        indices = set()
        
        for polygon in node.polygons:
            indices.add(polygon.texture_index)
        
        if node.front_child:
            indices.update(self._get_texture_indices_from_bsp(node.front_child))
        if node.back_child:
            indices.update(self._get_texture_indices_from_bsp(node.back_child))
        
        return indices
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'filename': self.filename,
            'version': self.version.value,
            'header': {
                'max_radius': self.header.max_radius,
                'object_flags': self.header.object_flags,
                'num_subobjects': self.header.num_subobjects,
                'bounding_box': {
                    'min': self.header.bounding_box.min.to_list(),
                    'max': self.header.bounding_box.max.to_list()
                },
                'mass': self.header.mass,
                'mass_center': self.header.mass_center.to_list()
            },
            'textures': self.textures,
            'subobjects': [
                {
                    'number': so.number,
                    'name': so.name,
                    'radius': so.radius,
                    'parent': so.parent,
                    'offset': so.offset.to_list(),
                    'bounding_box': {
                        'min': so.bounding_box.min.to_list(),
                        'max': so.bounding_box.max.to_list()
                    }
                } for so in self.subobjects
            ]
        }


# Utility functions for type conversion

def dict_to_subobject(data: Dict[str, Any]) -> SubObject:
    """Convert dictionary to SubObject with validation."""
    return SubObject(
        number=data.get('number', 0),
        radius=data.get('radius', 0.0),
        parent=data.get('parent', -1),
        offset=Vector3D(*data.get('offset', [0, 0, 0])),
        geometric_center=Vector3D(*data.get('geometric_center', [0, 0, 0])),
        bounding_box=BoundingBox(
            Vector3D(*data.get('bounding_min', [0, 0, 0])),
            Vector3D(*data.get('bounding_max', [0, 0, 0]))
        ),
        name=data.get('name', ''),
        properties=data.get('properties', ''),
        movement_type=MovementType(data.get('movement_type', 0)),
        movement_axis=MovementAxis(data.get('movement_axis', 3)),
        bsp_data_size=data.get('bsp_data_size', 0),
        bsp_data_offset=data.get('bsp_data_offset', -1),
        bsp_tree=None  # BSP tree needs separate parsing
    )


def dict_to_header(data: Dict[str, Any], version: POFVersion) -> POFHeader:
    """Convert dictionary to POFHeader with validation."""
    return POFHeader(
        version=version,
        max_radius=data.get('max_radius', 0.0),
        object_flags=data.get('obj_flags', 0),
        num_subobjects=data.get('num_subobjects', 0),
        bounding_box=BoundingBox(
            Vector3D(*data.get('min_bounding', [0, 0, 0])),
            Vector3D(*data.get('max_bounding', [0, 0, 0]))
        ),
        detail_levels=data.get('detail_levels', [-1] * 8),
        debris_pieces=data.get('debris_pieces', [-1] * 32),
        mass=data.get('mass', 0.0),
        mass_center=Vector3D(*data.get('mass_center', [0, 0, 0])),
        moment_of_inertia=[
            Vector3D(*row) for row in data.get('moment_inertia', [
                [1, 0, 0],
                [0, 1, 0], 
                [0, 0, 1]
            ])
        ],
        cross_sections=data.get('cross_sections', []),
        lights=data.get('lights', [])
    )


def subobject_to_dict(subobj: SubObject) -> Dict[str, Any]:
    """Convert SubObject to dictionary for serialization."""
    return {
        'number': subobj.number,
        'radius': subobj.radius,
        'parent': subobj.parent,
        'offset': subobj.offset.to_list(),
        'geometric_center': subobj.geometric_center.to_list(),
        'bounding_min': subobj.bounding_box.min.to_list(),
        'bounding_max': subobj.bounding_box.max.to_list(),
        'name': subobj.name,
        'properties': subobj.properties,
        'movement_type': subobj.movement_type.value,
        'movement_axis': subobj.movement_axis.value,
        'bsp_data_size': subobj.bsp_data_size,
        'bsp_data_offset': subobj.bsp_data_offset
    }


def dict_to_special_point(data: Dict[str, Any], point_type: str) -> SpecialPoint:
    """Convert dictionary to SpecialPoint with validation."""
    return SpecialPoint(
        name=data.get('name', ''),
        position=Vector3D(*data.get('position', [0, 0, 0])),
        normal=Vector3D(*data.get('normal', [0, 0, 0])),
        point_type=point_type,
        properties=data.get('properties', {})
    )


def dict_to_animation_path(data: Dict[str, Any]) -> AnimationPath:
    """Convert dictionary to AnimationPath with validation."""
    nodes = []
    for node_data in data.get('nodes', []):
        nodes.append(PathNode(
            position=Vector3D(*node_data.get('position', [0, 0, 0])),
            rotation=Vector3D(*node_data.get('rotation', [0, 0, 0])),
            time=node_data.get('time', 0.0),
            properties=node_data.get('properties', {})
        ))
    
    return AnimationPath(
        name=data.get('name', ''),
        nodes=nodes,
        loop=data.get('loop', False),
        duration=data.get('duration', 0.0)
    )


def dict_to_insignia(data: Dict[str, Any]) -> InsigniaData:
    """Convert dictionary to InsigniaData with validation."""
    return InsigniaData(
        texture_index=data.get('texture_index', 0),
        position=Vector3D(*data.get('position', [0, 0, 0])),
        size=Vector3D(*data.get('size', [1, 1, 1])),
        rotation=Vector3D(*data.get('rotation', [0, 0, 0]))
    )


def dict_to_glow_bank(data: Dict[str, Any]) -> GlowBank:
    """Convert dictionary to GlowBank with validation."""
    return GlowBank(
        position=Vector3D(*data.get('position', [0, 0, 0])),
        normal=Vector3D(*data.get('normal', [0, 0, 0])),
        radius=data.get('radius', 1.0),
        color=tuple(data.get('color', (1.0, 1.0, 1.0, 1.0))),
        intensity=data.get('intensity', 1.0)
    )


def dict_to_shield_mesh(data: Dict[str, Any]) -> ShieldMesh:
    """Convert dictionary to ShieldMesh with validation."""
    vertices = [Vector3D(*v) for v in data.get('vertices', [])]
    normals = [Vector3D(*n) for n in data.get('normals', [])]
    polygons = []
    
    for poly_data in data.get('polygons', []):
        polygons.append(BSPPolygon(
            vertices=[Vector3D(*v) for v in poly_data.get('vertices', [])],
            normal=Vector3D(*poly_data.get('normal', [0, 0, 0])),
            plane_distance=poly_data.get('plane_distance', 0.0),
            texture_index=poly_data.get('texture_index', 0)
        ))
    
    return ShieldMesh(
        vertices=vertices,
        normals=normals,
        polygons=polygons,
        collision_tree=None  # Will be populated separately
    )


def list_to_vector3d(coords: List[float]) -> Vector3D:
    """Convert list of coordinates to Vector3D."""
    if len(coords) >= 3:
        return Vector3D(coords[0], coords[1], coords[2])
    elif len(coords) == 2:
        return Vector3D(coords[0], coords[1], 0.0)
    elif len(coords) == 1:
        return Vector3D(coords[0], 0.0, 0.0)
    else:
        return Vector3D(0.0, 0.0, 0.0)