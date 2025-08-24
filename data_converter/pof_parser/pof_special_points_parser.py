#!/usr/bin/env python3
import logging
from typing import Any, BinaryIO, Dict, List

# Import necessary helper functions and constants from pof_chunks
from .pof_chunks import (
    MAX_NAME_LEN,
    MAX_PROP_LEN,
)

# Import unified binary reader
from .pof_binary_reader import create_reader

# Import Vector3D if needed for type hinting or direct use
# from .pof_types import Vector3D

logger = logging.getLogger(__name__)


def read_spcl_chunk(f: BinaryIO, length: int) -> List[Dict[str, Any]]:
    """Parses the Special Points (SPCL) chunk."""
    reader = create_reader(f)
    logger.debug("Reading SPCL chunk...")
    num_specials = reader.read_int32()
    specials = []
    for _ in range(num_specials):
        name = reader.read_length_prefixed_string(MAX_NAME_LEN)
        props = reader.read_length_prefixed_string(MAX_PROP_LEN)
        pos = reader.read_vector3d()
        radius = reader.read_float32()
        specials.append(
            {
                "name": name,
                "properties": props,
                "position": pos.to_list(),
                "radius": radius,
            }
        )
    return specials
