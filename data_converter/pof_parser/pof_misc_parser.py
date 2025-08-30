#!/usr/bin/env python3
import logging
import struct
from typing import Any, BinaryIO, Dict, List

# Import necessary helper functions and constants from pof_chunks
from .pof_chunks import (
    MAX_PROP_LEN,
)

# Import unified binary reader
from .pof_binary_reader import create_reader

# Import Vector3D if needed for type hinting or direct use

logger = logging.getLogger(__name__)


def read_acen_chunk(f: BinaryIO, length: int) -> List[float]:
    """Parses the Autocentering (ACEN) chunk."""
    reader = create_reader(f)
    logger.debug("Reading ACEN chunk...")
    vec = reader.read_vector3d()
    return vec.to_list()


def read_glow_chunk(f: BinaryIO, length: int) -> List[Dict[str, Any]]:
    """Parses the Glow Points (GLOW) chunk."""
    reader = create_reader(f)
    logger.debug("Reading GLOW chunk...")
    num_banks = reader.read_int32()
    glow_banks = []
    for _ in range(num_banks):
        bank_data = {"points": []}
        bank_data["disp_time"] = reader.read_int32()
        bank_data["on_time"] = reader.read_int32()
        bank_data["off_time"] = reader.read_int32()
        bank_data["parent"] = reader.read_int32()
        bank_data["lod"] = reader.read_int32()
        bank_data["type"] = reader.read_int32()
        num_points = reader.read_int32()
        bank_data["properties"] = reader.read_length_prefixed_string(MAX_PROP_LEN)
        for _ in range(num_points):
            pos = reader.read_vector3d()
            norm = reader.read_vector3d()
            radius = reader.read_float32()
            bank_data["points"].append(
                {"position": pos.to_list(), "normal": norm.to_list(), "radius": radius}
            )
        glow_banks.append(bank_data)
    return glow_banks


def read_unknown_chunk(f: BinaryIO, length: int, chunk_id: int) -> None:
    """Skips an unknown chunk."""
    try:
        # Attempt to decode the chunk ID as ASCII for logging
        chunk_id_str = struct.pack("<I", chunk_id).decode("ascii", errors="replace")
    except:
        chunk_id_str = "Invalid ID"
    logger.warning(
        f"Skipping unknown chunk '{chunk_id_str}' (ID: {chunk_id:08X}) of length {length}"
    )
    f.seek(length, 1)
