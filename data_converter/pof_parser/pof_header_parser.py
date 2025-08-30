#!/usr/bin/env python3
"""
POF Header Parser - Consolidated OHDR/HDR2 chunk parsing.

This module provides unified parsing for the Object Header chunk across
all POF versions, using the enhanced binary reader for robust error handling.
"""

import logging
from typing import Any, BinaryIO, Dict

from .pof_chunks import (
    MAX_DEBRIS_OBJECTS,
    MAX_MODEL_DETAIL_LEVELS,
)
from .pof_binary_reader import create_reader
from .pof_error_handler import get_global_error_handler, ErrorSeverity, ErrorCategory

logger = logging.getLogger(__name__)


def read_ohdr_chunk(f: BinaryIO, length: int) -> Dict[str, Any]:
    """
    Parses the Object Header (OHDR/HDR2) chunk with enhanced error handling.

    This is the main header parsing function that handles all POF versions
    through adaptive parsing based on available data length.
    """
    reader = create_reader(f)
    error_handler = get_global_error_handler()

    start_pos = f.tell()
    header_data = {}

    try:
        # Basic header information (present in all versions)
        header_data["max_radius"] = reader.read_float32()
        header_data["obj_flags"] = reader.read_uint32()
        header_data["num_subobjects"] = reader.read_int32()

        # Bounding box (present in all versions)
        min_bounding = reader.read_vector3d()
        max_bounding = reader.read_vector3d()
        header_data["min_bounding"] = min_bounding.to_list()
        header_data["max_bounding"] = max_bounding.to_list()

        # Detail levels and debris pieces (present in all versions)
        header_data["detail_levels"] = [
            reader.read_int32() for _ in range(MAX_MODEL_DETAIL_LEVELS)
        ]
        header_data["debris_pieces"] = [
            reader.read_int32() for _ in range(MAX_DEBRIS_OBJECTS)
        ]

        # Calculate bytes read so far
        bytes_read = f.tell() - start_pos

        # Enhanced properties (added in later POF versions)
        # Check remaining length to determine what additional fields exist

        # Mass properties (added in FS2/WCS)
        if bytes_read + 4 <= length:
            header_data["mass"] = reader.read_float32()
            bytes_read += 4
        else:
            header_data["mass"] = 0.0

        # Center of mass (added in FS2/WCS)
        if bytes_read + 12 <= length:
            mass_center = reader.read_vector3d()
            bytes_read += 12
            header_data["mass_center"] = mass_center.to_list()
        else:
            header_data["mass_center"] = [0.0, 0.0, 0.0]

        # Moment of inertia (3x3 matrix stored as 3 vectors) (added in FS2/WCS)
        if bytes_read + 36 <= length:  # 3 vectors × 12 bytes each
            rvec = reader.read_vector3d()
            uvec = reader.read_vector3d()
            fvec = reader.read_vector3d()
            bytes_read += 36
            # Store as list of lists (rows)
            header_data["moment_inertia"] = [
                rvec.to_list(),
                uvec.to_list(),
                fvec.to_list(),
            ]
        else:
            header_data["moment_inertia"] = [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1],
            ]  # Identity matrix

        # Cross Sections (Added in WCS)
        header_data["cross_sections"] = []
        if bytes_read + 4 <= length:
            num_cross_sections = reader.read_int32()
            bytes_read += 4

            # Validate number of cross sections
            if num_cross_sections > 1000:  # Arbitrary reasonable limit
                error_handler.add_error(
                    f"Unreasonable number of cross sections: {num_cross_sections}",
                    severity=ErrorSeverity.WARNING,
                    category=ErrorCategory.VALIDATION,
                    recovery_action="Limiting to 1000 cross sections",
                )
                num_cross_sections = min(num_cross_sections, 1000)

            for _ in range(num_cross_sections):
                if bytes_read + 8 <= length:  # 2 floats × 4 bytes each
                    depth = reader.read_float32()
                    radius = reader.read_float32()
                    bytes_read += 8
                    header_data["cross_sections"].append((depth, radius))
                else:
                    error_handler.add_error(
                        "Insufficient data for cross section",
                        severity=ErrorSeverity.WARNING,
                        category=ErrorCategory.PARSING,
                        recovery_action="Skipping remaining cross sections",
                    )
                    break

        # Lights (Added in WCS)
        header_data["lights"] = []
        if bytes_read + 4 <= length:
            num_lights = reader.read_int32()
            bytes_read += 4

            # Validate number of lights
            if num_lights > 1000:  # Arbitrary reasonable limit
                error_handler.add_error(
                    f"Unreasonable number of lights: {num_lights}",
                    severity=ErrorSeverity.WARNING,
                    category=ErrorCategory.VALIDATION,
                    recovery_action="Limiting to 1000 lights",
                )
                num_lights = min(num_lights, 1000)

            for _ in range(num_lights):
                if bytes_read + 16 <= length:  # Vector3D (12) + int (4)
                    pos = reader.read_vector3d()
                    light_type = reader.read_int32()
                    bytes_read += 16
                    header_data["lights"].append(
                        {"position": pos.to_list(), "type": light_type}
                    )
                else:
                    error_handler.add_error(
                        "Insufficient data for light",
                        severity=ErrorSeverity.WARNING,
                        category=ErrorCategory.PARSING,
                        recovery_action="Skipping remaining lights",
                    )
                    break

        # Skip any remaining unknown data in the chunk
        remaining = length - bytes_read
        if remaining > 0:
            logger.warning(f"Skipping {remaining} unknown bytes in OHDR chunk.")
            f.seek(remaining, 1)
        elif remaining < 0:
            error_handler.add_error(
                f"Read past end of OHDR chunk by {-remaining} bytes!",
                severity=ErrorSeverity.ERROR,
                category=ErrorCategory.PARSING,
                recovery_action="Continue with parsed data",
            )

        return header_data

    except Exception as e:
        error_handler.add_error(
            f"Failed to parse OHDR chunk: {e}",
            severity=ErrorSeverity.ERROR,
            category=ErrorCategory.PARSING,
            recovery_action="Return partial header data",
        )
        # Return whatever data we managed to parse
        return header_data


# --- Version-Specific Parsers (Maintained for backward compatibility) ---


def read_ohdr_chunk_v1800(f: BinaryIO, length: int) -> Dict[str, Any]:
    """Parses OHDR chunk for FS1 format (version 1800)."""
    reader = create_reader(f)

    header_data = {}
    header_data["max_radius"] = reader.read_float32()
    header_data["obj_flags"] = reader.read_uint32()
    header_data["num_subobjects"] = reader.read_int32()

    min_bounding = reader.read_vector3d()
    max_bounding = reader.read_vector3d()
    header_data["min_bounding"] = min_bounding.to_list()
    header_data["max_bounding"] = max_bounding.to_list()

    header_data["detail_levels"] = [
        reader.read_int32() for _ in range(MAX_MODEL_DETAIL_LEVELS)
    ]
    header_data["debris_pieces"] = [
        reader.read_int32() for _ in range(MAX_DEBRIS_OBJECTS)
    ]

    # FS1 format doesn't have mass properties, cross sections, or lights
    header_data["mass"] = 0.0
    header_data["mass_center"] = [0.0, 0.0, 0.0]
    header_data["moment_inertia"] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    header_data["cross_sections"] = []
    header_data["lights"] = []

    return header_data


def read_ohdr_chunk_v2100(f: BinaryIO, length: int) -> Dict[str, Any]:
    """Parses OHDR chunk for FS2 base format (version 2100)."""
    reader = create_reader(f)

    header_data = {}
    header_data["max_radius"] = reader.read_float32()
    header_data["obj_flags"] = reader.read_uint32()
    header_data["num_subobjects"] = reader.read_int32()

    min_bounding = reader.read_vector3d()
    max_bounding = reader.read_vector3d()
    header_data["min_bounding"] = min_bounding.to_list()
    header_data["max_bounding"] = max_bounding.to_list()

    header_data["detail_levels"] = [
        reader.read_int32() for _ in range(MAX_MODEL_DETAIL_LEVELS)
    ]
    header_data["debris_pieces"] = [
        reader.read_int32() for _ in range(MAX_DEBRIS_OBJECTS)
    ]

    # FS2 base format has mass properties but not cross sections or lights
    header_data["mass"] = reader.read_float32()
    mass_center = reader.read_vector3d()
    header_data["mass_center"] = mass_center.to_list()

    # Moment of inertia (3x3 matrix stored as 3 vectors)
    rvec = reader.read_vector3d()
    uvec = reader.read_vector3d()
    fvec = reader.read_vector3d()
    header_data["moment_inertia"] = [rvec.to_list(), uvec.to_list(), fvec.to_list()]

    header_data["cross_sections"] = []
    header_data["lights"] = []

    return header_data


def read_ohdr_chunk_v2112(f: BinaryIO, length: int) -> Dict[str, Any]:
    """Parses OHDR chunk for FS2 enhanced format (version 2112)."""
    reader = create_reader(f)

    header_data = {}
    header_data["max_radius"] = reader.read_float32()
    header_data["obj_flags"] = reader.read_uint32()
    header_data["num_subobjects"] = reader.read_int32()

    min_bounding = reader.read_vector3d()
    max_bounding = reader.read_vector3d()
    header_data["min_bounding"] = min_bounding.to_list()
    header_data["max_bounding"] = max_bounding.to_list()

    header_data["detail_levels"] = [
        reader.read_int32() for _ in range(MAX_MODEL_DETAIL_LEVELS)
    ]
    header_data["debris_pieces"] = [
        reader.read_int32() for _ in range(MAX_DEBRIS_OBJECTS)
    ]

    # FS2 enhanced format has mass properties and cross sections
    header_data["mass"] = reader.read_float32()
    mass_center = reader.read_vector3d()
    header_data["mass_center"] = mass_center.to_list()

    # Moment of inertia (3x3 matrix stored as 3 vectors)
    rvec = reader.read_vector3d()
    uvec = reader.read_vector3d()
    fvec = reader.read_vector3d()
    header_data["moment_inertia"] = [rvec.to_list(), uvec.to_list(), fvec.to_list()]

    # Cross sections
    num_cross_sections = reader.read_int32()
    header_data["cross_sections"] = []
    for _ in range(num_cross_sections):
        depth = reader.read_float32()
        radius = reader.read_float32()
        header_data["cross_sections"].append((depth, radius))

    header_data["lights"] = []

    return header_data


def read_ohdr_chunk_v2117(f: BinaryIO, length: int) -> Dict[str, Any]:
    """Parses OHDR chunk for WCS current format (version 2117)."""
    reader = create_reader(f)

    header_data = {}
    header_data["max_radius"] = reader.read_float32()
    header_data["obj_flags"] = reader.read_uint32()
    header_data["num_subobjects"] = reader.read_int32()

    min_bounding = reader.read_vector3d()
    max_bounding = reader.read_vector3d()
    header_data["min_bounding"] = min_bounding.to_list()
    header_data["max_bounding"] = max_bounding.to_list()

    header_data["detail_levels"] = [
        reader.read_int32() for _ in range(MAX_MODEL_DETAIL_LEVELS)
    ]
    header_data["debris_pieces"] = [
        reader.read_int32() for _ in range(MAX_DEBRIS_OBJECTS)
    ]

    # WCS current format has all features
    header_data["mass"] = reader.read_float32()
    mass_center = reader.read_vector3d()
    header_data["mass_center"] = mass_center.to_list()

    # Moment of inertia (3x3 matrix stored as 3 vectors)
    rvec = reader.read_vector3d()
    uvec = reader.read_vector3d()
    fvec = reader.read_vector3d()
    header_data["moment_inertia"] = [rvec.to_list(), uvec.to_list(), fvec.to_list()]

    # Cross sections
    num_cross_sections = reader.read_int32()
    header_data["cross_sections"] = []
    for _ in range(num_cross_sections):
        depth = reader.read_float32()
        radius = reader.read_float32()
        header_data["cross_sections"].append((depth, radius))

    # Lights
    num_lights = reader.read_int32()
    header_data["lights"] = []
    for _ in range(num_lights):
        pos = reader.read_vector3d()
        light_type = reader.read_int32()
        header_data["lights"].append({"position": pos.to_list(), "type": light_type})

    return header_data
