#!/usr/bin/env python3
"""
BSP Parser - Complete BSP tree reconstruction for POF files.

Based on Rust reference implementation with proper BSP tree handling.
"""

import logging
import struct
from typing import Any, BinaryIO, Dict, List, Optional, Tuple

from .pof_types import BSPNode, BSPNodeType, BSPPolygon, Vector3D

logger = logging.getLogger(__name__)


class BSPParser:
    """Parser for Binary Space Partitioning (BSP) tree data."""
    
    def __init__(self):
        """Initialize BSP parser."""
        self._current_pos = 0
        self._error_count = 0
    
    def parse_bsp_tree(self, bsp_data: bytes, version: int) -> Optional[BSPNode]:
        """
        Parse BSP tree data and reconstruct complete tree structure.
        
        Args:
            bsp_data: Raw BSP data bytes
            version: POF version for format-specific parsing
            
        Returns:
            Root BSPNode of the reconstructed tree, or None if parsing failed
        """
        if not bsp_data:
            logger.error("No BSP data provided")
            return None
        
        self._current_pos = 0
        self._error_count = 0
        
        try:
            # Parse based on version
            if version >= 2112:
                return self._parse_bsp_tree_v2112(bsp_data)
            else:
                return self._parse_bsp_tree_legacy(bsp_data)
        except Exception as e:
            logger.error(f"Failed to parse BSP tree: {e}", exc_info=True)
            return None
    
    def _parse_bsp_tree_v2112(self, bsp_data: bytes) -> Optional[BSPNode]:
        """Parse BSP tree for version 2112 and above."""
        try:
            # Read tree header
            num_nodes = self._read_int(bsp_data)
            num_polygons = self._read_int(bsp_data)
            
            if num_nodes <= 0 or num_polygons < 0:
                logger.error(f"Invalid BSP tree: {num_nodes} nodes, {num_polygons} polygons")
                return None
            
            # Parse nodes
            nodes = []
            for i in range(num_nodes):
                node = self._parse_bsp_node(bsp_data)
                if node is None:
                    logger.error(f"Failed to parse node {i}")
                    return None
                nodes.append(node)
            
            # Parse polygons and assign to nodes
            polygons = []
            for i in range(num_polygons):
                polygon = self._parse_bsp_polygon(bsp_data)
                if polygon is None:
                    logger.error(f"Failed to parse polygon {i}")
                    return None
                polygons.append(polygon)
            
            # Read polygon-node assignments
            for i in range(num_polygons):
                node_index = self._read_int(bsp_data)
                if node_index < 0 or node_index >= len(nodes):
                    logger.error(f"Invalid node index {node_index} for polygon {i}")
                    continue
                
                if polygons[i]:
                    nodes[node_index].polygons.append(polygons[i])
            
            # Build tree structure (node 0 is root)
            for i, node in enumerate(nodes):
                front_index = self._read_int(bsp_data)
                back_index = self._read_int(bsp_data)
                
                if front_index >= 0 and front_index < len(nodes):
                    node.front_child = nodes[front_index]
                if back_index >= 0 and back_index < len(nodes):
                    node.back_child = nodes[back_index]
            
            return nodes[0] if nodes else None
            
        except Exception as e:
            logger.error(f"Error parsing BSP tree v2112: {e}", exc_info=True)
            return None
    
    def _parse_bsp_tree_legacy(self, bsp_data: bytes) -> Optional[BSPNode]:
        """Parse legacy BSP tree format."""
        try:
            # Legacy format uses different structure
            num_polygons = self._read_int(bsp_data)
            
            if num_polygons <= 0:
                logger.error(f"Invalid legacy BSP: {num_polygons} polygons")
                return None
            
            # Parse polygons
            polygons = []
            for i in range(num_polygons):
                polygon = self._parse_bsp_polygon_legacy(bsp_data)
                if polygon is None:
                    logger.error(f"Failed to parse legacy polygon {i}")
                    return None
                polygons.append(polygon)
            
            # Create a simple flat node for legacy format
            root_node = BSPNode(
                node_type=BSPNodeType.NODE,
                normal=Vector3D(0, 0, 0),
                plane_distance=0.0,
                polygons=polygons
            )
            
            return root_node
            
        except Exception as e:
            logger.error(f"Error parsing legacy BSP tree: {e}", exc_info=True)
            return None
    
    def _parse_bsp_node(self, bsp_data: bytes) -> Optional[BSPNode]:
        """Parse a single BSP node."""
        try:
            node_type_val = self._read_int(bsp_data)
            try:
                node_type = BSPNodeType(node_type_val)
            except ValueError:
                logger.warning(f"Unknown node type {node_type_val}, using NODE")
                node_type = BSPNodeType.NODE
            
            normal = self._read_vector(bsp_data)
            plane_distance = self._read_float(bsp_data)
            
            return BSPNode(
                node_type=node_type,
                normal=normal,
                plane_distance=plane_distance
            )
            
        except Exception as e:
            logger.error(f"Failed to parse BSP node: {e}")
            self._error_count += 1
            return None
    
    def _parse_bsp_polygon(self, bsp_data: bytes) -> Optional[BSPPolygon]:
        """Parse a BSP polygon."""
        try:
            num_vertices = self._read_int(bsp_data)
            if num_vertices < 3:
                logger.error(f"Invalid polygon with {num_vertices} vertices")
                return None
            
            # Read vertices
            vertices = []
            for _ in range(num_vertices):
                vertex = self._read_vector(bsp_data)
                vertices.append(vertex)
            
            # Read plane information
            normal = self._read_vector(bsp_data)
            plane_distance = self._read_float(bsp_data)
            
            # Read texture index
            texture_index = self._read_int(bsp_data)
            
            return BSPPolygon(
                vertices=vertices,
                normal=normal,
                plane_distance=plane_distance,
                texture_index=texture_index
            )
            
        except Exception as e:
            logger.error(f"Failed to parse BSP polygon: {e}")
            self._error_count += 1
            return None
    
    def _parse_bsp_polygon_legacy(self, bsp_data: bytes) -> Optional[BSPPolygon]:
        """Parse legacy format BSP polygon."""
        try:
            num_vertices = self._read_int(bsp_data)
            if num_vertices < 3:
                logger.error(f"Invalid legacy polygon with {num_vertices} vertices")
                return None
            
            # Read vertices
            vertices = []
            for _ in range(num_vertices):
                vertex = self._read_vector(bsp_data)
                vertices.append(vertex)
            
            # Legacy format may not have proper plane information
            # Use first triangle to compute approximate normal
            if len(vertices) >= 3:
                v0, v1, v2 = vertices[0], vertices[1], vertices[2]
                edge1 = v1 - v0
                edge2 = v2 - v0
                normal = Vector3D(
                    edge1.y * edge2.z - edge1.z * edge2.y,
                    edge1.z * edge2.x - edge1.x * edge2.z,
                    edge1.x * edge2.y - edge1.y * edge2.x
                ).normalize()
                
                # Compute plane distance from first vertex
                plane_distance = -(normal.x * v0.x + normal.y * v0.y + normal.z * v0.z)
            else:
                normal = Vector3D(0, 0, 0)
                plane_distance = 0.0
            
            # Legacy format may not have explicit texture index
            texture_index = 0
            
            return BSPPolygon(
                vertices=vertices,
                normal=normal,
                plane_distance=plane_distance,
                texture_index=texture_index
            )
            
        except Exception as e:
            logger.error(f"Failed to parse legacy BSP polygon: {e}")
            self._error_count += 1
            return None
    
    def _read_int(self, bsp_data: bytes) -> int:
        """Read 4-byte integer from BSP data."""
        if self._current_pos + 4 > len(bsp_data):
            raise EOFError("Unexpected end of BSP data while reading int")
        
        value = struct.unpack_from('<i', bsp_data, self._current_pos)[0]
        self._current_pos += 4
        return value
    
    def _read_float(self, bsp_data: bytes) -> float:
        """Read 4-byte float from BSP data."""
        if self._current_pos + 4 > len(bsp_data):
            raise EOFError("Unexpected end of BSP data while reading float")
        
        value = struct.unpack_from('<f', bsp_data, self._current_pos)[0]
        self._current_pos += 4
        return value
    
    def _read_vector(self, bsp_data: bytes) -> Vector3D:
        """Read 3D vector (3 floats) from BSP data."""
        if self._current_pos + 12 > len(bsp_data):
            raise EOFError("Unexpected end of BSP data while reading vector")
        
        x = struct.unpack_from('<f', bsp_data, self._current_pos)[0]
        y = struct.unpack_from('<f', bsp_data, self._current_pos + 4)[0]
        z = struct.unpack_from('<f', bsp_data, self._current_pos + 8)[0]
        self._current_pos += 12
        
        return Vector3D(x, y, z)
    
    def get_parsing_stats(self) -> Dict[str, int]:
        """Get parsing statistics including error count."""
        return {
            'error_count': self._error_count,
            'position': self._current_pos
        }


def parse_bsp_data(bsp_data: bytes, version: int) -> Optional[Dict[str, Any]]:
    """
    Parse BSP data and return structured information.
    
    This is the main entry point for BSP parsing, maintaining compatibility
    with existing code while providing enhanced BSP tree functionality.
    """
    parser = BSPParser()
    bsp_tree = parser.parse_bsp_tree(bsp_data, version)
    
    if bsp_tree is None:
        return None
    
    # Extract flat geometry data for backward compatibility
    vertices, normals, uvs, polygons = _extract_flat_geometry(bsp_tree)
    
    return {
        'bsp_tree': bsp_tree,
        'vertices': vertices,
        'normals': normals,
        'uvs': uvs,
        'polygons': polygons,
        'parsing_stats': parser.get_parsing_stats()
    }


def _extract_flat_geometry(bsp_tree: BSPNode) -> Tuple[List, List, List, List]:
    """Extract flat geometry data from BSP tree for backward compatibility."""
    vertices = []
    normals = []
    uvs = []  # Note: UVs not stored in BSP, will be empty
    polygons = []
    
    def traverse_node(node: BSPNode):
        for polygon in node.polygons:
            # Add vertices and normals
            for vertex in polygon.vertices:
                vertices.append(vertex.to_list())
                normals.append(polygon.normal.to_list())
            
            # Create polygon entry
            start_idx = len(vertices) - len(polygon.vertices)
            poly_indices = list(range(start_idx, start_idx + len(polygon.vertices)))
            
            polygons.append({
                'texture_index': polygon.texture_index,
                'indices': poly_indices,
                'normal': polygon.normal.to_list(),
                'plane_distance': polygon.plane_distance
            })
        
        if node.front_child:
            traverse_node(node.front_child)
        if node.back_child:
            traverse_node(node.back_child)
    
    traverse_node(bsp_tree)
    
    return vertices, normals, uvs, polygons