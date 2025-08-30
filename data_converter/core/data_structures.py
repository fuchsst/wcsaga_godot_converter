"""
Data structures for conversion operations.

This module contains data classes used throughout the conversion system
for reporting, configuration, and data transfer.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class ConversionReport:
    """Comprehensive conversion validation report."""

    source_file: str
    output_file: str
    conversion_time: float
    success: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # Source analysis
    source_version: int = 0
    source_chunks: int = 0
    source_subobjects: int = 0
    source_textures: int = 0

    # Intermediate data
    intermediate_vertices: int = 0
    intermediate_faces: int = 0
    intermediate_materials: int = 0
    intermediate_groups: int = 0

    # Final output data
    output_file_size: int = 0
    output_exists: bool = False
    import_file_exists: bool = False

    # Validation results
    geometry_preserved: bool = False
    materials_preserved: bool = False
    hierarchy_preserved: bool = False
    textures_mapped: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary for JSON serialization."""
        return {
            "source_file": self.source_file,
            "output_file": self.output_file,
            "conversion_time": self.conversion_time,
            "success": self.success,
            "errors": self.errors,
            "warnings": self.warnings,
            "source_analysis": {
                "source_version": self.source_version,
                "source_chunks": self.source_chunks,
                "source_subobjects": self.source_subobjects,
                "source_textures": self.source_textures,
            },
            "intermediate_data": {
                "intermediate_vertices": self.intermediate_vertices,
                "intermediate_faces": self.intermediate_faces,
                "intermediate_materials": self.intermediate_materials,
                "intermediate_groups": self.intermediate_groups,
            },
            "output_data": {
                "output_file_size": self.output_file_size,
                "output_exists": self.output_exists,
                "import_file_exists": self.import_file_exists,
            },
            "validation_results": {
                "geometry_preserved": self.geometry_preserved,
                "materials_preserved": self.materials_preserved,
                "hierarchy_preserved": self.hierarchy_preserved,
                "textures_mapped": self.textures_mapped,
            },
        }


@dataclass
class ConversionSettings:
    """Configuration settings for conversion operations."""

    preserve_hierarchy: bool = True
    generate_collision: bool = True
    optimize_meshes: bool = True
    generate_lods: bool = False
    texture_quality: int = 85
    max_texture_size: int = 2048

    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary."""
        return {
            "preserve_hierarchy": self.preserve_hierarchy,
            "generate_collision": self.generate_collision,
            "optimize_meshes": self.optimize_meshes,
            "generate_lods": self.generate_lods,
            "texture_quality": self.texture_quality,
            "max_texture_size": self.max_texture_size,
        }


@dataclass
class ConversionContext:
    """Context for conversion operations."""

    source_path: Path
    target_path: Path
    settings: ConversionSettings = field(default_factory=ConversionSettings)
    stats: Dict[str, Any] = field(default_factory=dict)

    def update_stats(self, key: str, value: Any) -> None:
        """Update conversion statistics."""
        self.stats[key] = value
