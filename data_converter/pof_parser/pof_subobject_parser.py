#!/usr/bin/env python3
import logging
from typing import Any, BinaryIO, Dict, Optional

# Import necessary helper functions and constants from pof_chunks
from .pof_chunks import (
    MAX_NAME_LEN,
    MAX_PROP_LEN,
    read_float,
    read_int,
    read_string_len,
    read_vector,
)

# Import dataclass types
from .pof_enhanced_types import SubObject, Vector3D, BoundingBox
from .pof_enhanced_types import MovementType, MovementAxis

logger = logging.getLogger(__name__)


def read_sobj_chunk(f: BinaryIO, length: int) -> Optional[SubObject]:
    """Parses a Subobject (SOBJ/OBJ2) chunk and returns SubObject dataclass."""
    start_pos = f.tell()
    bytes_read = 0
    
    try:
        # Read basic subobject data
        number = read_int(f)
        bytes_read += 4
        radius = read_float(f)
        bytes_read += 4
        parent = read_int(f)
        bytes_read += 4
        offset = read_vector(f)
        bytes_read += 12
        geometric_center = read_vector(f)
        bytes_read += 12
        min_bb = read_vector(f)
        bytes_read += 12
        max_bb = read_vector(f)
        bytes_read += 12
        
        # Create bounding box
        bounding_box = BoundingBox(min=min_bb, max=max_bb)

        # Read name and properties
        name_start_pos = f.tell()
        name = read_string_len(f, MAX_NAME_LEN)
        bytes_read += f.tell() - name_start_pos

        props_start_pos = f.tell()
        properties = read_string_len(f, MAX_PROP_LEN)
        bytes_read += f.tell() - props_start_pos

        # Read movement data
        movement_type_val = read_int(f)
        bytes_read += 4
        movement_axis_val = read_int(f)
        bytes_read += 4
        
        # Convert to enum types
        movement_type = MovementType(movement_type_val)
        movement_axis = MovementAxis(movement_axis_val)

        # Read BSP data size
        bsp_data_size = read_int(f)
        bytes_read += 4
        
        if bsp_data_size > 0:
            bsp_data_offset = f.tell()
            f.seek(bsp_data_size, 1)
            bytes_read += bsp_data_size
        else:
            bsp_data_offset = -1

        # Check if we read exactly the chunk length
        if bytes_read != length:
            logger.warning(
                f"SOBJ chunk length mismatch for subobject {number} ('{name}'). Expected {length}, read {bytes_read}. There might be extra reserved data."
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
        logger.error(f"Failed to parse SOBJ chunk: {e}")
        # Try to recover position
        if bytes_read < length:
            f.seek(start_pos + 8 + length)
        return None
