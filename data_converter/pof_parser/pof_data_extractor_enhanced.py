#!/usr/bin/env python3
"""
Enhanced POF Data Extractor - Works with POFModelDataEnhanced structure.

This module extracts structured data from POF files for conversion to Godot-compatible formats.
Focuses on geometry, materials, textures, and gameplay-relevant metadata.

Based on WCS C++ analysis from source/code/model/modelread.cpp
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .pof_parser import POFParser
from .pof_enhanced_types import POFModelDataEnhanced, Vector3D

logger = logging.getLogger(__name__)


@dataclass
class GeometryData:
    """Extracted geometry data from POF subobjects."""

    vertices: List[Tuple[float, float, float]] = field(default_factory=list)
    normals: List[Tuple[float, float, float]] = field(default_factory=list)
    texture_coordinates: List[Tuple[float, float]] = field(default_factory=list)
    faces: List[List[int]] = field(default_factory=list)  # Vertex indices per face
    materials: List[int] = field(default_factory=list)  # Material indices per face


@dataclass
class MaterialData:
    """Material information for POF models."""

    name: str
    texture_path: str
    diffuse_color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    specular_color: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    ambient_color: Tuple[float, float, float] = (0.2, 0.2, 0.2)
    shininess: float = 0.0


@dataclass
class SubsystemData:
    """Subsystem information for gameplay features."""

    name: str
    subobject_number: int
    position: Tuple[float, float, float]
    radius: float
    health: float = 100.0
    armor: float = 0.0


@dataclass
class WeaponPointData:
    """Weapon hardpoint data."""

    name: str
    position: Tuple[float, float, float]
    normal: Tuple[float, float, float]
    weapon_type: str  # "gun", "missile", "turret"
    bank_number: int
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DockingPointData:
    """Docking point data."""

    name: str
    position: Tuple[float, float, float]
    normal: Tuple[float, float, float]
    dock_type: str  # "fighter", "transport", "cargo"
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThrusterData:
    """Thruster/engine data."""

    position: Tuple[float, float, float]
    normal: Tuple[float, float, float]
    radius: float
    thrust: float = 1000.0
    afterburner: bool = False


class POFDataExtractorEnhanced:
    """Enhanced POF data extractor for Godot conversion."""

    def __init__(self):
        """Initialize enhanced POF data extractor."""
        self.parser = POFParser()

    def extract_model_data(self, file_path: Path) -> Optional[POFModelDataEnhanced]:
        """
        Extract comprehensive model data from POF file.

        Args:
            file_path: Path to POF file

        Returns:
            POFModelDataEnhanced object with extracted data, or None if parsing failed
        """
        logger.info(f"Extracting model data from: {file_path}")

        # Parse POF file
        parsed_data = self.parser.parse(file_path)
        if not parsed_data:
            logger.error(f"Failed to parse POF file: {file_path}")
            return None

        try:
            logger.info(
                f"Successfully extracted model data: {len(parsed_data.subobjects)} subobjects, "
                f"{len(parsed_data.textures)} textures, {len(parsed_data.gun_points)} gun points"
            )

            return parsed_data

        except Exception as e:
            logger.error(
                f"Error extracting model data from {file_path}: {e}", exc_info=True
            )
            return None

    def extract_for_godot_conversion(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Extract POF data specifically formatted for Godot conversion.

        Args:
            file_path: Path to POF file

        Returns:
            Dictionary with Godot-optimized data structure
        """
        model_data = self.extract_model_data(file_path)
        if not model_data:
            return None

        # Convert to Godot-friendly format
        godot_data = {
            "metadata": {
                "source_file": model_data.filename,
                "pof_version": model_data.version.value,
                "max_radius": model_data.header.max_radius,
                "mass": model_data.header.mass,
                "center_of_mass": model_data.header.mass_center.to_list(),
            },
            "scene_tree": self._create_godot_scene_tree(model_data),
            "materials": self._create_godot_materials(model_data),
            "collision_shapes": self._create_collision_data(model_data),
            "gameplay_nodes": self._create_gameplay_nodes(model_data),
        }

        return godot_data

    def _create_godot_scene_tree(self, model_data: POFModelDataEnhanced) -> Dict[str, Any]:
        """Create Godot scene tree structure from subobjects."""
        scene_tree = {
            "root": {
                "name": Path(model_data.filename).stem,
                "type": "Node3D",
                "children": [],
            }
        }

        # Process subobjects in hierarchy order
        root_objects = [
            subobj for subobj in model_data.subobjects if subobj.parent == -1
        ]

        for root_obj in root_objects:
            child_node = self._create_subobject_node(root_obj, model_data.subobjects)
            scene_tree["root"]["children"].append(child_node)

        return scene_tree

    def _create_subobject_node(self, subobj, all_subobjects: List) -> Dict[str, Any]:
        """Create Godot node for a subobject."""
        node = {
            "name": subobj.name or f"subobject_{subobj.number}",
            "type": "Node3D",
            "transform": {
                "translation": subobj.offset.to_list(),
                "rotation": [0, 0, 0, 1],  # Default quaternion
                "scale": [1, 1, 1],
            },
            "children": [],
        }

        # Add child subobjects
        child_objects = [
            child for child in all_subobjects if child.parent == subobj.number
        ]

        for child_obj in child_objects:
            child_node = self._create_subobject_node(child_obj, all_subobjects)
            node["children"].append(child_node)

        return node

    def _create_godot_materials(self, model_data: POFModelDataEnhanced) -> List[Dict[str, Any]]:
        """Create Godot material definitions."""
        godot_materials = []

        for i, texture_path in enumerate(model_data.textures):
            godot_material = {
                "name": f"material_{i}",
                "texture": texture_path,
                "shader": "standard_3d",
                "parameters": {
                    "albedo_color": [1.0, 1.0, 1.0],
                    "metallic": 0.0,
                    "roughness": 0.8,
                    "emission": [0.0, 0.0, 0.0],
                },
            }
            godot_materials.append(godot_material)

        return godot_materials

    def _create_collision_data(self, model_data: POFModelDataEnhanced) -> Dict[str, Any]:
        """Create collision shape data for Godot."""
        return {
            "hull_shape": {
                "type": "ConvexPolygonShape3D",
                "vertices": [
                    model_data.header.bounding_box.min.to_list(),
                    model_data.header.bounding_box.max.to_list(),
                ],
            },
            "detail_shapes": [],  # Per-subobject collision shapes
        }

    def _create_gameplay_nodes(self, model_data: POFModelDataEnhanced) -> Dict[str, Any]:
        """Create gameplay-specific node data."""
        return {
            "weapon_hardpoints": [
                {
                    "name": f"gun_point_{i}",
                    "position": point.position.to_list(),
                    "normal": point.normal.to_list(),
                    "type": "gun",
                    "bank": 0,
                }
                for i, point in enumerate(model_data.gun_points)
            ],
            "docking_bays": [
                {
                    "name": f"dock_point_{i}",
                    "position": point.position.to_list(),
                    "normal": point.normal.to_list(),
                    "type": "generic",
                }
                for i, point in enumerate(model_data.docking_points)
            ],
            "engine_points": [
                {
                    "position": thruster.position.to_list(),
                    "normal": thruster.normal.to_list(),
                    "radius": thruster.radius,
                }
                for thruster in model_data.thrusters
            ],
        }


def main():
    """Test the enhanced data extractor."""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python pof_data_extractor_enhanced.py <pof_file>")
        sys.exit(1)
    
    extractor = POFDataExtractorEnhanced()
    model_data = extractor.extract_model_data(Path(sys.argv[1]))
    
    if model_data:
        print(f"Successfully extracted: {model_data.filename}")
        print(f"Version: {model_data.version.value}")
        print(f"Subobjects: {len(model_data.subobjects)}")
        print(f"Textures: {len(model_data.textures)}")
    else:
        print("Failed to extract model data")


if __name__ == "__main__":
    main()