#!/usr/bin/env python3
import logging
from typing import Any, BinaryIO, Dict, List

# Import necessary helper functions and constants from pof_chunks
from .pof_chunks import MAX_NAME_LEN

# Import unified binary reader
from .pof_binary_reader import create_reader

# Import Vector3D if needed for type hinting or direct use
# from .pof_types import Vector3D

logger = logging.getLogger(__name__)


def read_path_chunk(f: BinaryIO, length: int) -> List[Dict[str, Any]]:
    """Parses the Paths (PATH) chunk."""
    reader = create_reader(f)
    logger.debug("Reading PATH chunk...")
    num_paths = reader.read_int32()
    paths = []
    for _ in range(num_paths):
        path_data = {"verts": []}
        path_data["name"] = reader.read_length_prefixed_string(MAX_NAME_LEN)
        path_data["parent_name"] = reader.read_length_prefixed_string(
            MAX_NAME_LEN
        )  # POF v2002+
        num_verts = reader.read_int32()
        path_data["nverts"] = num_verts
        for _ in range(num_verts):
            pos = reader.read_vector3d()
            radius = reader.read_float32()
            num_turrets = reader.read_int32()
            turret_ids = [reader.read_int32() for _ in range(num_turrets)]
            path_data["verts"].append(
                {"position": pos.to_list(), "radius": radius, "turret_ids": turret_ids}
            )
        paths.append(path_data)
    return paths
