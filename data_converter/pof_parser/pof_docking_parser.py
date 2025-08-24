#!/usr/bin/env python3
import logging
from typing import Any, BinaryIO, Dict, List

# Import necessary helper functions and constants from pof_chunks
from .pof_chunks import (
    MAX_DOCK_SLOTS,
    MAX_PROP_LEN,
)

# Import unified binary reader
from .pof_binary_reader import create_reader

# Import Vector3D if needed for type hinting or direct use
# from .pof_types import Vector3D

logger = logging.getLogger(__name__)


def read_dock_chunk(f: BinaryIO, length: int) -> List[Dict[str, Any]]:
    """Parses the Docking Points (DOCK) chunk."""
    reader = create_reader(f)
    logger.debug("Reading DOCK chunk...")
    num_docks = reader.read_int32()
    docking_points = []
    for _ in range(num_docks):
        dock_data = {"points": []}
        dock_data["properties"] = reader.read_length_prefixed_string(MAX_PROP_LEN)
        num_spline_paths = reader.read_int32()
        dock_data["spline_paths"] = [reader.read_int32() for _ in range(num_spline_paths)]
        num_slots = reader.read_int32()
        dock_data["num_slots"] = num_slots
        # Ensure we read exactly MAX_DOCK_SLOTS (2) points, even if num_slots differs
        for slot_idx in range(MAX_DOCK_SLOTS):
            pos = reader.read_vector3d()
            norm = reader.read_vector3d()
            if slot_idx < num_slots:  # Only store valid slots read
                dock_data["points"].append(
                    {"position": pos.to_list(), "normal": norm.to_list()}
                )
            else:
                logger.warning(
                    f"Dock point expected {num_slots} slots but reading fixed {MAX_DOCK_SLOTS}. Discarding extra read for slot {slot_idx+1}."
                )
        # If num_slots was less than MAX_DOCK_SLOTS, fill remaining with defaults? Or log error?
        if num_slots < MAX_DOCK_SLOTS:
            logger.warning(
                f"Dock point only defined {num_slots} slots, expected {MAX_DOCK_SLOTS}."
            )
            # Optionally fill remaining slots with default values if required downstream
            # for _ in range(MAX_DOCK_SLOTS - num_slots):
            #     dock_data['points'].append({'position': [0,0,0], 'normal': [0,0,1]})

        docking_points.append(dock_data)
    return docking_points
