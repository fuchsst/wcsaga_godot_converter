#!/usr/bin/env python3
"""
POF Stability Tests - Comprehensive pytest test suite for POF parser stability.

Tests BSP parsing, version compatibility, error handling, and type system.
"""

import pytest
import struct
import tempfile
from pathlib import Path
from typing import Dict, List, Any

from .pof_types import (
    POFVersion, Vector3D, BoundingBox, BSPNode, BSPNodeType, BSPPolygon,
    POFHeader, SubObject, POFModelData
)
from .pof_bsp_parser import BSPParser, parse_bsp_data
from .pof_version_handler import POFVersionHandler, validate_pof_version


class TestPOFTypes:
    """Test POF type system and data structures."""
    
    def test_vector3d_validation(self):
        """Test Vector3D validation and operations."""
        # Valid vector
        v = Vector3D(1.0, 2.0, 3.0)
        assert v.x == 1.0
        assert v.y == 2.0
        assert v.z == 3.0
        
        # Invalid vector should raise error
        with pytest.raises(ValueError):
            Vector3D("invalid", 2.0, 3.0)
        
        # Test operations
        v1 = Vector3D(1.0, 2.0, 3.0)
        v2 = Vector3D(4.0, 5.0, 6.0)
        
        assert (v1 + v2) == Vector3D(5.0, 7.0, 9.0)
        assert (v2 - v1) == Vector3D(3.0, 3.0, 3.0)
        assert (v1 * 2) == Vector3D(2.0, 4.0, 6.0)
        
    def test_bounding_box_validation(self):
        """Test BoundingBox validation."""
        min_vec = Vector3D(0.0, 0.0, 0.0)
        max_vec = Vector3D(1.0, 1.0, 1.0)
        
        # Valid bounding box
        bbox = BoundingBox(min_vec, max_vec)
        assert bbox.center() == Vector3D(0.5, 0.5, 0.5)
        assert bbox.size() == Vector3D(1.0, 1.0, 1.0)
        
        # Invalid bounding box (min > max)
        with pytest.raises(ValueError):
            BoundingBox(max_vec, min_vec)
    
    def test_bsp_polygon_validation(self):
        """Test BSPPolygon validation."""
        vertices = [Vector3D(0, 0, 0), Vector3D(1, 0, 0), Vector3D(0, 1, 0)]
        normal = Vector3D(0, 0, 1)
        
        # Valid polygon
        poly = BSPPolygon(vertices, normal, 0.0, 0)
        assert len(poly.vertices) == 3
        
        # Invalid polygon (too few vertices)
        with pytest.raises(ValueError):
            BSPPolygon([Vector3D(0, 0, 0)], normal, 0.0, 0)
    
    def test_pof_header_validation(self):
        """Test POFHeader validation."""
        bbox = BoundingBox(Vector3D(-1, -1, -1), Vector3D(1, 1, 1))
        mass_center = Vector3D(0, 0, 0)
        moment_inertia = [Vector3D(1, 0, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1)]
        
        # Valid header
        header = POFHeader(
            version=POFVersion.VERSION_2117,
            max_radius=10.0,
            object_flags=0,
            num_subobjects=1,
            bounding_box=bbox,
            detail_levels=[0, -1, -1, -1, -1, -1, -1, -1],
            debris_pieces=[-1] * 32,
            mass=100.0,
            mass_center=mass_center,
            moment_of_inertia=moment_inertia,
            cross_sections=[],
            lights=[]
        )
        
        assert header.version == POFVersion.VERSION_2117
        assert header.max_radius == 10.0
        
        # Invalid header (negative values)
        with pytest.raises(ValueError):
            POFHeader(
                version=POFVersion.VERSION_2117,
                max_radius=-1.0,  # Invalid
                object_flags=0,
                num_subobjects=1,
                bounding_box=bbox,
                detail_levels=[],
                debris_pieces=[],
                mass=100.0,
                mass_center=mass_center,
                moment_of_inertia=moment_inertia,
                cross_sections=[],
                lights=[]
            )


class TestBSPParser:
    """Test BSP tree parsing functionality."""
    
    def test_bsp_parser_initialization(self):
        """Test BSP parser initialization."""
        parser = BSPParser()
        assert parser._error_count == 0
        assert parser._current_pos == 0
    
    def test_parse_empty_bsp_data(self):
        """Test parsing empty BSP data."""
        parser = BSPParser()
        result = parser.parse_bsp_tree(b"", 2117)
        assert result is None
    
    def test_parse_simple_bsp_tree(self):
        """Test parsing a simple BSP tree."""
        # Create minimal BSP data for testing
        bsp_data = b""
        
        # Tree header: 1 node, 1 polygon
        bsp_data += struct.pack('<ii', 1, 1)
        
        # Node: type=0 (NODE), normal=(0,1,0), distance=0.0
        bsp_data += struct.pack('<i', 0)  # node_type
        bsp_data += struct.pack('<fff', 0.0, 1.0, 0.0)  # normal
        bsp_data += struct.pack('<f', 0.0)  # plane_distance
        
        # Polygon: 3 vertices, normal=(0,1,0), distance=0.0, texture=0
        bsp_data += struct.pack('<i', 3)  # num_vertices
        bsp_data += struct.pack('<fff', 0.0, 0.0, 0.0)  # vertex 1
        bsp_data += struct.pack('<fff', 1.0, 0.0, 0.0)  # vertex 2
        bsp_data += struct.pack('<fff', 0.0, 0.0, 1.0)  # vertex 3
        bsp_data += struct.pack('<fff', 0.0, 1.0, 0.0)  # normal
        bsp_data += struct.pack('<f', 0.0)  # plane_distance
        bsp_data += struct.pack('<i', 0)  # texture_index
        
        # Polygon-node assignment: polygon 0 -> node 0
        bsp_data += struct.pack('<i', 0)
        
        # Node children: front=-1, back=-1
        bsp_data += struct.pack('<ii', -1, -1)
        
        parser = BSPParser()
        result = parser.parse_bsp_tree(bsp_data, 2117)
        
        assert result is not None
        assert result.node_type == BSPNodeType.NODE
        assert len(result.polygons) == 1
        assert result.polygons[0].texture_index == 0
    
    def test_parse_legacy_bsp_format(self):
        """Test parsing legacy BSP format."""
        # Legacy format: just polygons without tree structure
        bsp_data = b""
        bsp_data += struct.pack('<i', 1)  # 1 polygon
        
        # Polygon: 3 vertices
        bsp_data += struct.pack('<i', 3)  # num_vertices
        bsp_data += struct.pack('<fff', 0.0, 0.0, 0.0)  # vertex 1
        bsp_data += struct.pack('<fff', 1.0, 0.0, 0.0)  # vertex 2
        bsp_data += struct.pack('<fff', 0.0, 0.0, 1.0)  # vertex 3
        
        parser = BSPParser()
        result = parser.parse_bsp_tree(bsp_data, 2100)  # Legacy version
        
        assert result is not None
        assert len(result.polygons) == 1
    
    def test_bsp_parsing_error_handling(self):
        """Test BSP parsing error handling."""
        # Invalid BSP data (truncated)
        bsp_data = struct.pack('<ii', 1, 1)  # Header only
        
        parser = BSPParser()
        result = parser.parse_bsp_tree(bsp_data, 2117)
        
        # Should handle error gracefully
        assert result is None
        assert parser._error_count > 0


class TestVersionHandler:
    """Test version compatibility handling."""
    
    def test_version_validation(self):
        """Test POF version validation."""
        handler = POFVersionHandler()
        
        # Valid versions
        result = handler.validate_version(2117)
        assert result['valid']
        assert result['compatible']
        assert result['version'] == POFVersion.VERSION_2117
        
        result = handler.validate_version(2100)
        assert result['valid']
        assert result['version'] == POFVersion.VERSION_2100
        
        # Invalid version
        result = handler.validate_version(9999)
        assert not result['valid']
        assert not result['compatible']
    
    def test_chunk_compatibility(self):
        """Test chunk compatibility checking."""
        handler = POFVersionHandler()
        
        # OHDR chunk should be compatible with all versions
        result = handler.check_chunk_compatibility(2117, 0x4F484452)  # OHDR
        assert result['compatible']
        assert result['required']
        assert result['chunk_name'] == 'OHDR'
        
        # SLDC chunk should only be compatible with newer versions
        result = handler.check_chunk_compatibility(2117, 0x534C4443)  # SLDC
        assert result['compatible']
        assert not result['required']
        
        # SLDC chunk with old version should be incompatible
        result = handler.check_chunk_compatibility(2100, 0x534C4443)  # SLDC
        assert not result['compatible']
    
    def test_version_specific_fixes(self):
        """Test version-specific data fixes."""
        handler = POFVersionHandler()
        
        # Test data without mass properties (old version)
        test_data = {
            'header': {},
            'textures': ['texture1.dds']
        }
        
        # Apply fixes for old version
        fixed_data = handler.apply_version_specific_fixes(test_data, 1800)
        
        # Should add default mass properties
        assert 'mass' in fixed_data['header']
        assert 'mass_center' in fixed_data['header']
        assert 'moment_inertia' in fixed_data['header']
        
        # Test texture normalization
        assert fixed_data['textures'][0] == 'texture1.dds'
    
    def test_compatibility_report(self):
        """Test compatibility report generation."""
        handler = POFVersionHandler()
        
        report = handler.generate_compatibility_report(
            2117, 
            ['OHDR', 'SOBJ', 'TXTR', 'SLDC']
        )
        
        assert 'version_info' in report
        assert 'issues' in report
        assert 'warnings' in report
        assert 'recommendations' in report
        
        # Should not have issues for valid version
        assert len(report['issues']) == 0


class TestIntegration:
    """Integration tests for complete POF parsing."""
    
    def test_bsp_data_extraction(self):
        """Test complete BSP data extraction."""
        # Create test BSP data
        bsp_data = b""
        bsp_data += struct.pack('<ii', 1, 1)  # 1 node, 1 polygon
        
        # Node
        bsp_data += struct.pack('<i', 0)  # node_type
        bsp_data += struct.pack('<fff', 0.0, 1.0, 0.0)  # normal
        bsp_data += struct.pack('<f', 0.0)  # plane_distance
        
        # Polygon
        bsp_data += struct.pack('<i', 3)  # num_vertices
        bsp_data += struct.pack('<fff', 0.0, 0.0, 0.0)  # vertex 1
        bsp_data += struct.pack('<fff', 1.0, 0.0, 0.0)  # vertex 2
        bsp_data += struct.pack('<fff', 0.0, 0.0, 1.0)  # vertex 3
        bsp_data += struct.pack('<fff', 0.0, 1.0, 0.0)  # normal
        bsp_data += struct.pack('<f', 0.0)  # plane_distance
        bsp_data += struct.pack('<i', 0)  # texture_index
        
        # Assignment and children
        bsp_data += struct.pack('<i', 0)  # polygon -> node 0
        bsp_data += struct.pack('<ii', -1, -1)  # no children
        
        # Test complete parsing
        result = parse_bsp_data(bsp_data, 2117)
        
        assert result is not None
        assert 'bsp_tree' in result
        assert 'vertices' in result
        assert 'normals' in result
        assert 'polygons' in result
        assert 'parsing_stats' in result
        
        # Should have extracted geometry
        assert len(result['vertices']) == 3
        assert len(result['normals']) == 3
        assert len(result['polygons']) == 1
    
    def test_error_handling_integration(self):
        """Test error handling throughout the parsing pipeline."""
        # Test with invalid BSP data
        result = parse_bsp_data(b"invalid", 2117)
        assert result is None
        
        # Test with partially valid data
        partial_data = struct.pack('<ii', 1, 1)  # Header only
        result = parse_bsp_data(partial_data, 2117)
        assert result is None


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_complete_stability_scenario(temp_dir):
    """Complete stability test scenario."""
    # Test type system
    vector = Vector3D(1.0, 2.0, 3.0)
    assert vector.to_list() == [1.0, 2.0, 3.0]
    
    # Test version handling
    version_info = validate_pof_version(2117)
    assert version_info['valid']
    assert version_info['compatible']
    
    # Test BSP parsing - create valid minimal BSP data
    bsp_data = struct.pack('<ii', 1, 1)  # 1 node, 1 polygon
    # Node data
    bsp_data += struct.pack('<i', 0)  # node_type
    bsp_data += struct.pack('<fff', 0.0, 1.0, 0.0)  # normal
    bsp_data += struct.pack('<f', 0.0)  # plane_distance
    # Polygon data
    bsp_data += struct.pack('<i', 3)  # num_vertices
    bsp_data += struct.pack('<fff', 0.0, 0.0, 0.0)  # vertex 1
    bsp_data += struct.pack('<fff', 1.0, 0.0, 0.0)  # vertex 2
    bsp_data += struct.pack('<fff', 0.0, 0.0, 1.0)  # vertex 3
    bsp_data += struct.pack('<fff', 0.0, 1.0, 0.0)  # normal
    bsp_data += struct.pack('<f', 0.0)  # plane_distance
    bsp_data += struct.pack('<i', 0)  # texture_index
    # Assignment and children
    bsp_data += struct.pack('<i', 0)  # polygon -> node 0
    bsp_data += struct.pack('<ii', -1, -1)  # no children
    
    result = parse_bsp_data(bsp_data, 2117)
    assert result is not None
    
    # Test error handling
    with pytest.raises(ValueError):
        Vector3D("invalid", 0, 0)


if __name__ == "__main__":
    # Run tests with detailed output
    pytest.main([
        __file__,
        "-v",
        "--tb=short"
    ])