#!/usr/bin/env python3
import logging
from typing import Any, BinaryIO, Dict, List

# Import unified binary reader
from .pof_binary_reader import create_reader

# Import Vector3D if needed for type hinting or direct use
# from .pof_types import Vector3D

logger = logging.getLogger(__name__)


def read_shld_chunk(f: BinaryIO, length: int) -> Dict[str, Any]:
    """Parses the Shield Mesh (SHLD) chunk."""
    reader = create_reader(f)
    logger.debug("Reading SHLD chunk...")
    shield_data = {"vertices": [], "faces": []}
    num_verts = reader.read_int32()
    # Read vertices first, store them in a temporary list
    temp_verts = [reader.read_vector3d() for _ in range(num_verts)]
    shield_data["vertices"] = [v.to_list() for v in temp_verts]  # Store as lists

    num_tris = reader.read_int32()
    for _ in range(num_tris):
        norm = reader.read_vector3d().to_list()
        vert_indices = [reader.read_int32() for _ in range(3)]
        neighbor_indices = [reader.read_int32() for _ in range(3)]
        # Validate indices
        valid_indices = True
        for idx in vert_indices:
            if idx < 0 or idx >= num_verts:
                logger.error(
                    f"Invalid vertex index {idx} in SHLD chunk (max: {num_verts-1}). Skipping face."
                )
                valid_indices = False
                break
        if not valid_indices:
            continue  # Skip this face

        valid_neighbors = True
        for idx in neighbor_indices:
            # Neighbor index can be -1 if there's no neighbor
            if idx < -1 or idx >= num_tris:
                logger.error(
                    f"Invalid neighbor index {idx} in SHLD chunk (max: {num_tris-1}). Skipping face."
                )
                valid_neighbors = False
                break
        if not valid_neighbors:
            continue  # Skip this face

        shield_data["faces"].append(
            {
                "normal": norm,
                "vertex_indices": vert_indices,
                "neighbor_indices": neighbor_indices,
            }
        )
    return shield_data


def read_sldc_chunk(f: BinaryIO, length: int) -> bytes:
    """Reads the Shield Collision Tree (SLDC) chunk as raw bytes."""
    logger.debug("Reading SLDC chunk (raw bytes)...")
    return f.read(length)
