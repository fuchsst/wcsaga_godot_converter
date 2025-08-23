#!/usr/bin/env python3
"""
POF Type Definitions - Comprehensive data structures for POF parsing.

Based on Rust reference implementation with proper type safety and validation.
"""

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import List, Optional, Tuple, Dict, Any


class POFVersion(IntEnum):
    """POF version enumeration matching Rust reference."""
    VERSION_1800 = 1800  # FS1 format
    VERSION_2100 = 2100  # FS2 format
    VERSION_2112 = 2112  # FS2 with enhancements
    VERSION_2117 = 2117  # Current WCS format
    
    MIN_COMPATIBLE = 1800
    MAX_COMPATIBLE = 2117


class BSPNodeType(IntEnum):
    """BSP node types matching Rust reference."""
    SPLIT = 0  # Split node with front/back children
    LEAF = 1   # Leaf node with polygon
    EMPTY = 2  # Empty node


class BSPChunkType(IntEnum):
    """BSP chunk types matching Rust reference."""
    ENDOFBRANCH = 0
    DEFFPOINTS = 1
    FLATPOLY = 2
    TMAPPOLY = 3
    SORTNORM = 4
    BOUNDBOX = 5
    TMAPPOLY2 = 6
    SORTNORM2 = 7


class MovementType(IntEnum):
    """Subobject movement types."""
    NONE = 0
    ROTATION = 1
    TRANSLATION = 2
    BOTH = 3


class MovementAxis(IntEnum):
    """Movement axis enumeration."""
    X = 0
    Y = 1
    Z = 2


class ModelType(Enum):
    """Model type classification."""
    SHIP = "ship"
    STATION = "station" 
    DEBRIS = "debris"
    WEAPON = "weapon"
    EFFECT = "effect"
    UNKNOWN = "unknown"


@dataclass
class Vector3D:
    """3D vector with proper validation and operations."""
    x: float
    y: float
    z: float
    
    def __post_init__(self):
        """Validate vector components."""
        if not all(isinstance(v, (int, float)) for v in [self.x, self.y, self.z]):
            raise ValueError("Vector components must be numeric")
    
    def to_list(self) -> List[float]:
        """Convert to list format."""
        return [self.x, self.y, self.z]
    
    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float) -> 'Vector3D':
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def length(self) -> float:
        """Calculate vector length."""
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5
    
    def normalize(self) -> 'Vector3D':
        """Normalize vector to unit length."""
        length = self.length()
        if length == 0:
            return Vector3D(0, 0, 0)
        return self * (1.0 / length)


@dataclass
class BoundingBox:
    """Axis-aligned bounding box."""
    min: Vector3D
    max: Vector3D
    
    def __post_init__(self):
        """Validate bounding box."""
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


@dataclass
class BSPPolygon:
    """BSP polygon with vertices and plane information."""
    vertices: List[Vector3D]
    normal: Vector3D
    plane_distance: float
    texture_index: int
    
    def __post_init__(self):
        """Validate polygon data."""
        if len(self.vertices) < 3:
            raise ValueError("Polygon must have at least 3 vertices")
        if not isinstance(self.normal, Vector3D):
            raise ValueError("Normal must be a Vector3D")
        if not isinstance(self.plane_distance, (int, float)):
            raise ValueError("Plane distance must be numeric")
        if not isinstance(self.texture_index, int):
            raise ValueError("Texture index must be integer")


@dataclass
class BSPNode:
    """BSP tree node matching Rust reference structure."""
    node_type: BSPNodeType
    bbox: Optional[BoundingBox] = None
    front_child: Optional['BSPNode'] = None
    back_child: Optional['BSPNode'] = None
    polygon: Optional[BSPPolygon] = None  # For LEAF nodes
    
    def __post_init__(self):
        """Validate BSP node."""
        if not isinstance(self.node_type, BSPNodeType):
            raise ValueError("Node type must be BSPNodeType")
        if self.node_type == BSPNodeType.LEAF and self.polygon is None:
            raise ValueError("LEAF nodes must have a polygon")
        if self.node_type == BSPNodeType.SPLIT and (self.front_child is None or self.back_child is None):
            raise ValueError("SPLIT nodes must have both front and back children")


@dataclass
class POFHeader:
    """Complete POF header data structure."""
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
        """Validate header data."""
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


@dataclass
class SubObject:
    """Subobject data structure with proper validation."""
    number: int
    radius: float
    parent: int
    offset: Vector3D
    geometric_center: Vector3D
    bounding_box: BoundingBox
    name: str
    properties: str
    movement_type: int
    movement_axis: int
    bsp_data_size: int
    bsp_data_offset: int
    bsp_tree: Optional[BSPNode] = None
    
    def __post_init__(self):
        """Validate subobject data."""
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


@dataclass
class POFModelData:
    """Complete POF model data structure."""
    filename: str
    version: POFVersion
    header: POFHeader
    textures: List[str]
    subobjects: List[SubObject]
    special_points: List[Dict[str, Any]]
    paths: List[Dict[str, Any]]
    gun_points: List[Dict[str, Any]]
    missile_points: List[Dict[str, Any]]
    docking_points: List[Dict[str, Any]]
    thrusters: List[Dict[str, Any]]
    shield_mesh: Optional[Dict[str, Any]]
    eye_points: List[Dict[str, Any]]
    insignia: List[Dict[str, Any]]
    autocenter: Optional[Dict[str, Any]]
    glow_banks: List[Dict[str, Any]]
    shield_collision_tree: Optional[Dict[str, Any]]
    
    def validate(self) -> List[str]:
        """Validate complete model data and return list of issues."""
        issues = []
        
        # Check version compatibility
        if self.version < POFVersion.MIN_COMPATIBLE:
            issues.append(f"Version {self.version} is below minimum compatible version {POFVersion.MIN_COMPATIBLE}")
        if self.version > POFVersion.MAX_COMPATIBLE:
            issues.append(f"Version {self.version} may have compatibility issues")
        
        # Check subobject consistency
        if len(self.subobjects) != self.header.num_subobjects:
            issues.append(f"Header reports {self.header.num_subobjects} subobjects but found {len(self.subobjects)}")
        
        # Check texture references
        for i, subobj in enumerate(self.subobjects):
            if subobj.bsp_tree:
                # Validate that all texture indices are valid
                texture_indices = self._get_texture_indices_from_bsp(subobj.bsp_tree)
                for tex_idx in texture_indices:
                    if tex_idx >= len(self.textures):
                        issues.append(f"Subobject {i} references invalid texture index {tex_idx}")
        
        return issues
    
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