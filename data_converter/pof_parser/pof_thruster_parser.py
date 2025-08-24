#!/usr/bin/env python3
import logging
from typing import Any, BinaryIO, Dict, List

# Import necessary helper functions and constants from pof_chunks
from .pof_chunks import MAX_PROP_LEN

# Import unified binary reader
from .pof_binary_reader import create_reader

# Import Vector3D if needed for type hinting or direct use
# from .pof_types import Vector3D

logger = logging.getLogger(__name__)


def read_fuel_chunk(f: BinaryIO, length: int) -> List[Dict[str, Any]]:
    """Parses the Thrusters (FUEL) chunk."""
    reader = create_reader(f)
    logger.debug("Reading FUEL chunk...")
    num_thrusters = reader.read_int32()
    thrusters = []
    for _ in range(num_thrusters):
        thruster_data = {"points": []}
        num_points = reader.read_int32()
        thruster_data["num_points"] = num_points
        thruster_data["properties"] = reader.read_length_prefixed_string(
            MAX_PROP_LEN
        )  # Properties string
        for _ in range(num_points):
            pos = reader.read_vector3d()
            norm = reader.read_vector3d()
            radius = reader.read_float32()
            thruster_data["points"].append(
                {"position": pos.to_list(), "normal": norm.to_list(), "radius": radius}
            )
        thrusters.append(thruster_data)
    return thrusters
