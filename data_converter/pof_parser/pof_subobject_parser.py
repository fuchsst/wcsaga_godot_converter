#!/usr/bin/env python3
"""
POF Subobject Parser - Consolidated SOBJ/OBJ2 chunk parsing.

This module provides unified parsing for the Subobject chunk using the
enhanced binary reader with improved error handling and validation.
"""

import logging
from typing import Any, BinaryIO, Dict, Optional

# Import necessary helper functions and constants from pof_chunks
from .pof_chunks import (
    MAX_NAME_LEN,
    MAX_PROP_LEN,
)
from .pof_binary_reader import create_reader
from .pof_error_handler import get_global_error_handler, ErrorSeverity, ErrorCategory

# Import dataclass types
from .pof_types import SubObject, Vector3D, BoundingBox
from .pof_types import MovementType, MovementAxis

logger = logging.getLogger(__name__)


def read_sobj_chunk(f: BinaryIO, length: int) -> Optional[SubObject]:
    """
    Parses a Subobject (SOBJ/OBJ2) chunk and returns SubObject dataclass.
    
    This function uses the enhanced binary reader for robust error handling
    and validation, replacing the scattered reading functions.
    """
    reader = create_reader(f)
    error_handler = get_global_error_handler()
    
    start_pos = f.tell()
    bytes_read = 0
    
    try:
        # Read basic subobject data with validation
        number = reader.read_int32()
        bytes_read += 4
        
        radius = reader.read_float32()
        bytes_read += 4
        # Validate radius is non-negative
        if radius < 0:
            error_handler.add_data_integrity_warning(
                f"Subobject {number} has negative radius: {radius}",
                recovery_action="Using absolute value"
            )
            radius = abs(radius)

        parent = reader.read_int32()
        bytes_read += 4
        
        offset = reader.read_vector3d()
        bytes_read += 12
        
        geometric_center = reader.read_vector3d()
        bytes_read += 12
        
        min_bb = reader.read_vector3d()
        bytes_read += 12
        
        max_bb = reader.read_vector3d()
        bytes_read += 12
        
        # Create bounding box with validation
        bounding_box = BoundingBox(min=min_bb, max=max_bb)
        
        # Validate bounding box
        if (bounding_box.min.x > bounding_box.max.x or
            bounding_box.min.y > bounding_box.max.y or
            bounding_box.min.z > bounding_box.max.z):
            error_handler.add_validation_error(
                f"Invalid bounding box for subobject {number} (min > max)",
                recovery_action="Recalculating from geometry"
            )

        # Read name and properties
        name_start_pos = f.tell()
        name = reader.read_string(MAX_NAME_LEN)
        bytes_read += f.tell() - name_start_pos

        props_start_pos = f.tell()
        properties = reader.read_string(MAX_PROP_LEN)
        bytes_read += f.tell() - props_start_pos

        # Read movement data
        movement_type_val = reader.read_int32()
        bytes_read += 4
        movement_axis_val = reader.read_int32()
        bytes_read += 4
        
        # Validate and convert to enum types
        try:
            movement_type = MovementType(movement_type_val)
        except ValueError:
            error_handler.add_validation_error(
                f"Invalid movement type {movement_type_val} for subobject {number}",
                recovery_action="Using static movement type"
            )
            movement_type = MovementType.STATIC

        try:
            movement_axis = MovementAxis(movement_axis_val)
        except ValueError:
            error_handler.add_validation_error(
                f"Invalid movement axis {movement_axis_val} for subobject {number}",
                recovery_action="Using no axis"
            )
            movement_axis = MovementAxis.NONE

        # Read BSP data size
        bsp_data_size = reader.read_int32()
        bytes_read += 4
        
        # Validate BSP data size
        if bsp_data_size < 0:
            error_handler.add_validation_error(
                f"Negative BSP data size {bsp_data_size} for subobject {number}",
                recovery_action="Setting to zero"
            )
            bsp_data_size = 0
        
        if bsp_data_size > 0:
            bsp_data_offset = f.tell()
            f.seek(bsp_data_size, 1)
            bytes_read += bsp_data_size
        else:
            bsp_data_offset = -1

        # Check if we read exactly the chunk length
        if bytes_read != length:
            error_message = (
                f"SOBJ chunk length mismatch for subobject {number} ('{name}'). "
                f"Expected {length}, read {bytes_read}."
            )
            
            if bytes_read < length:
                error_message += " There might be extra reserved data."
            else:
                error_message += " Read past expected end of chunk!"
            
            error_handler.add_error(
                error_message,
                severity=ErrorSeverity.WARNING if bytes_read < length else ErrorSeverity.ERROR,
                category=ErrorCategory.PARSING,
                recovery_action="Attempting to recover chunk position"
            )
            
            # Attempt to seek to the expected end of the chunk if we read less
            if bytes_read < length:
                f.seek(start_pos + 8 + length)  # Seek from start of chunk + header size

        # Create and return SubObject dataclass
        return SubObject(
            number=number,
            radius=radius,
            parent=parent,
            offset=offset,
            geometric_center=geometric_center,
            bounding_box=bounding_box,
            name=name,
            properties=properties,
            movement_type=movement_type,
            movement_axis=movement_axis,
            bsp_data_size=bsp_data_size,
            bsp_data_offset=bsp_data_offset,
            bsp_tree=None  # Will be populated later during BSP parsing
        )
        
    except Exception as e:
        error_handler.add_error(
            f"Failed to parse SOBJ chunk: {e}",
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.PARSING,
            recovery_action="Skipping subobject and continuing"
        )
        # Try to recover position
        if bytes_read < length:
            try:
                f.seek(start_pos + 8 + length)
            except Exception as seek_error:
                logger.error(f"Failed to recover position after SOBJ parsing error: {seek_error}")
        return None
