#!/usr/bin/env python3
"""
POF Validation System - Comprehensive data validation.

Based on Rust reference validation patterns with enhanced error reporting
and recovery strategies for robust parsing.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple

from .pof_enhanced_types import (
    BSPNode,
    BSPNodeType,
    POFModelDataEnhanced,
    POFVersion,
    SubObject,
    Vector3D,
)
from .pof_error_handler import POFErrorHandler, ErrorSeverity, ErrorCategory

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Comprehensive validation result with detailed findings."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    data_loss_expected: bool


class POFValidator:
    """Comprehensive POF data validator based on Rust patterns."""

    def __init__(self, error_handler: Optional[POFErrorHandler] = None):
        """Initialize validator with optional error handler."""
        self.error_handler = error_handler or POFErrorHandler()

    def validate_model_data(self, model_data: POFModelDataEnhanced) -> ValidationResult:
        """
        Validate complete POF model data with Rust-like thoroughness.
        
        Based on Rust validation patterns with comprehensive checks for:
        - Data consistency and integrity
        - Version compatibility
        - Structural validity
        - Gameplay element sanity
        """
        errors = []
        warnings = []
        suggestions = []
        
        try:
            # Version compatibility validation
            self._validate_version(model_data.version, errors, warnings)
            
            # Header validation
            self._validate_header(model_data.header, errors, warnings)
            
            # Subobject hierarchy validation
            self._validate_subobjects(model_data.subobjects, errors, warnings)
            
            # Texture reference validation
            self._validate_texture_references(model_data, errors, warnings)
            
            # BSP tree validation
            self._validate_bsp_trees(model_data.subobjects, errors, warnings)
            
            # Gameplay element validation
            self._validate_gameplay_elements(model_data, errors, warnings)
            
            # Spatial consistency validation
            self._validate_spatial_consistency(model_data, errors, warnings)
            
        except Exception as e:
            errors.append(f"Validation process failed: {e}")
            self.error_handler.add_error(
                f"Validation system error: {e}",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.VALIDATION,
                recovery_action="Continue with partial validation"
            )
        
        # Determine overall validity
        is_valid = len(errors) == 0
        data_loss_expected = len(warnings) > 0 or not is_valid
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            data_loss_expected=data_loss_expected
        )

    def _validate_version(self, version: POFVersion, errors: List[str], warnings: List[str]) -> None:
        """Validate POF version compatibility."""
        if version < POFVersion.MIN_COMPATIBLE:
            errors.append(f"Version {version} is below minimum compatible version {POFVersion.MIN_COMPATIBLE}")
            self.error_handler.add_error(
                f"Incompatible POF version: {version}",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.COMPATIBILITY,
                recovery_action="Requires version conversion"
            )
        elif version > POFVersion.MAX_COMPATIBLE:
            warnings.append(f"Version {version} may have unsupported features")
            self.error_handler.add_compatibility_warning(
                f"Newer POF version: {version}",
                recovery_action="Proceed with caution and validate results"
            )

    def _validate_header(self, header: Any, errors: List[str], warnings: List[str]) -> None:
        """Validate POF header data."""
        # Validate numerical values
        if header.max_radius <= 0:
            errors.append(f"Invalid max radius: {header.max_radius}")
            self.error_handler.add_validation_error(
                f"Invalid max radius: {header.max_radius}",
                recovery_action="Use calculated bounding sphere"
            )
        
        if header.num_subobjects < 0:
            errors.append(f"Invalid number of subobjects: {header.num_subobjects}")
            self.error_handler.add_validation_error(
                f"Negative subobject count: {header.num_subobjects}",
                recovery_action="Treat as zero subobjects"
            )
        
        if header.mass < 0:
            warnings.append(f"Negative mass value: {header.mass}")
            self.error_handler.add_data_integrity_warning(
                f"Negative mass: {header.mass}",
                recovery_action="Use absolute value"
            )
        
        # Validate bounding box
        if (header.bounding_box.min.x > header.bounding_box.max.x or
            header.bounding_box.min.y > header.bounding_box.max.y or
            header.bounding_box.min.z > header.bounding_box.max.z):
            errors.append("Invalid bounding box (min > max)")
            self.error_handler.add_validation_error(
                "Bounding box min greater than max",
                recovery_action="Recalculate bounding box from geometry"
            )

    def _validate_subobjects(self, subobjects: List[SubObject], errors: List[str], warnings: List[str]) -> None:
        """Validate subobject hierarchy and properties."""
        subobj_ids = set()
        
        for i, subobj in enumerate(subobjects):
            # Check for duplicate subobject numbers
            if subobj.number in subobj_ids:
                errors.append(f"Duplicate subobject number: {subobj.number}")
                self.error_handler.add_validation_error(
                    f"Duplicate subobject {subobj.number}",
                    recovery_action="Renumber duplicate subobjects"
                )
            subobj_ids.add(subobj.number)
            
            # Validate subobject properties
            if subobj.radius < 0:
                warnings.append(f"Subobject {subobj.number} has negative radius: {subobj.radius}")
                self.error_handler.add_data_integrity_warning(
                    f"Negative radius in subobject {subobj.number}",
                    recovery_action="Use absolute value"
                )
            
            if subobj.parent >= len(subobjects) and subobj.parent != -1:
                errors.append(f"Subobject {subobj.number} has invalid parent: {subobj.parent}")
                self.error_handler.add_validation_error(
                    f"Invalid parent index {subobj.parent} for subobject {subobj.number}",
                    recovery_action="Attach to root"
                )
            
            # Validate BSP data references
            if subobj.has_bsp_data() and subobj.bsp_data_size <= 0:
                warnings.append(f"Subobject {subobj.number} has invalid BSP data size: {subobj.bsp_data_size}")
                self.error_handler.add_data_integrity_warning(
                    f"Invalid BSP data size in subobject {subobj.number}",
                    recovery_action="Ignore BSP data"
                )

    def _validate_texture_references(self, model_data: POFModelDataEnhanced, 
                                   errors: List[str], warnings: List[str]) -> None:
        """Validate texture references throughout the model."""
        max_texture_index = len(model_data.textures) - 1
        
        # Check all polygons for valid texture indices
        texture_refs = set()
        
        for subobj in model_data.subobjects:
            if subobj.bsp_tree:
                self._collect_texture_indices(subobj.bsp_tree, texture_refs)
        
        for tex_idx in texture_refs:
            if tex_idx > max_texture_index:
                errors.append(f"Invalid texture index referenced: {tex_idx} (max: {max_texture_index})")
                self.error_handler.add_validation_error(
                    f"Invalid texture index {tex_idx}",
                    recovery_action="Use default texture"
                )
            elif tex_idx < 0:
                warnings.append(f"Negative texture index: {tex_idx}")
                self.error_handler.add_data_integrity_warning(
                    f"Negative texture index {tex_idx}",
                    recovery_action="Use absolute value"
                )

    def _collect_texture_indices(self, node: BSPNode, indices: Set[int]) -> None:
        """Recursively collect texture indices from BSP tree."""
        # Handle both BSPNode types (basic and enhanced)
        if hasattr(node, 'polygons'):
            # Enhanced BSPNode with polygons list
            for polygon in node.polygons:
                indices.add(polygon.texture_index)
        elif hasattr(node, 'polygon') and node.polygon:
            # Basic BSPNode with single polygon
            indices.add(node.polygon.texture_index)
        
        if node.front_child:
            self._collect_texture_indices(node.front_child, indices)
        if node.back_child:
            self._collect_texture_indices(node.back_child, indices)

    def _validate_bsp_trees(self, subobjects: List[SubObject], 
                          errors: List[str], warnings: List[str]) -> None:
        """Validate BSP tree structures."""
        for subobj in subobjects:
            if subobj.bsp_tree:
                self._validate_bsp_node(subobj.bsp_tree, f"subobject {subobj.number}", errors, warnings)

    def _validate_bsp_node(self, node: BSPNode, context: str, 
                         errors: List[str], warnings: List[str]) -> None:
        """Validate a single BSP node."""
        # Validate node type
        if not isinstance(node.node_type, BSPNodeType):
            errors.append(f"Invalid BSP node type in {context}: {node.node_type}")
            return
        
        # Validate normal for splitting nodes
        if node.node_type == BSPNodeType.NODE:
            normal_length = node.normal.length()
            if abs(normal_length - 1.0) > 1e-3:
                warnings.append(f"Non-unit normal in {context}: length {normal_length}")
                self.error_handler.add_data_integrity_warning(
                    f"Non-unit normal in {context}",
                    recovery_action="Normalize splitting plane"
                )
        
        # Validate polygons in leaf nodes
        if node.node_type == BSPNodeType.LEAF:
            # Handle both BSPNode types (basic and enhanced)
            polygons_to_validate = []
            if hasattr(node, 'polygons'):
                # Enhanced BSPNode with polygons list
                polygons_to_validate = node.polygons
            elif hasattr(node, 'polygon') and node.polygon:
                # Basic BSPNode with single polygon
                polygons_to_validate = [node.polygon]
            
            for i, polygon in enumerate(polygons_to_validate):
                if len(polygon.vertices) < 3:
                    errors.append(f"Invalid polygon in {context}: only {len(polygon.vertices)} vertices")
                    self.error_handler.add_validation_error(
                        f"Degenerate polygon in {context}",
                        recovery_action="Skip invalid polygon"
                    )
        
        # Recursively validate children
        if node.front_child:
            self._validate_bsp_node(node.front_child, context, errors, warnings)
        if node.back_child:
            self._validate_bsp_node(node.back_child, context, errors, warnings)

    def _validate_gameplay_elements(self, model_data: POFModelDataEnhanced, 
                                  errors: List[str], warnings: List[str]) -> None:
        """Validate gameplay-related elements."""
        # Validate weapon points
        for i, wp in enumerate(model_data.gun_points + model_data.missile_points):
            if not (-1.0 <= wp.normal.x <= 1.0 and 
                   -1.0 <= wp.normal.y <= 1.0 and 
                   -1.0 <= wp.normal.z <= 1.0):
                warnings.append(f"Weapon point {i} has non-normalized normal")
                self.error_handler.add_data_integrity_warning(
                    f"Non-normalized weapon point normal",
                    recovery_action="Normalize direction vector"
                )
        
        # Validate docking points
        for i, dock in enumerate(model_data.docking_points):
            if not dock.name.strip():
                warnings.append(f"Docking point {i} has empty name")
                self.error_handler.add_data_integrity_warning(
                    f"Unnamed docking point",
                    recovery_action="Generate default name"
                )

    def _validate_spatial_consistency(self, model_data: POFModelDataEnhanced, 
                                    errors: List[str], warnings: List[str]) -> None:
        """Validate spatial relationships and consistency."""
        # Check if subobject bounds are within main bounds
        main_min = model_data.header.bounding_box.min
        main_max = model_data.header.bounding_box.max
        
        for subobj in model_data.subobjects:
            sub_min = subobj.bounding_box.min
            sub_max = subobj.bounding_box.max
            
            if (sub_min.x < main_min.x or sub_min.y < main_min.y or sub_min.z < main_min.z or
                sub_max.x > main_max.x or sub_max.y > main_max.y or sub_max.z > main_max.z):
                warnings.append(f"Subobject {subobj.number} extends outside main bounds")
                self.error_handler.add_data_integrity_warning(
                    f"Subobject {subobj.number} outside main bounds",
                    recovery_action="Recalculate main bounding box"
                )


def validate_pof_model(model_data: POFModelDataEnhanced, 
                      error_handler: Optional[POFErrorHandler] = None) -> ValidationResult:
    """
    Convenience function for validating POF model data.
    
    Args:
        model_data: The POF model data to validate
        error_handler: Optional error handler for tracking issues
    
    Returns:
        ValidationResult with detailed findings
    """
    validator = POFValidator(error_handler)
    return validator.validate_model_data(model_data)