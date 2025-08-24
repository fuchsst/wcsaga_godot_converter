#!/usr/bin/env python3
import logging
from typing import Any, BinaryIO, Dict, List

# Import unified binary reader
from .pof_binary_reader import create_reader

# Import Vector3D if needed for type hinting or direct use
# from .pof_types import Vector3D

logger = logging.getLogger(__name__)


def read_eye_chunk(f: BinaryIO, length: int) -> List[Dict[str, Any]]:
    """Parses the Eye Points (EYE) chunk."""
    reader = create_reader(f)
    logger.debug("Reading EYE chunk...")
    num_eyes = reader.read_int32()
    eyes = []
    for _ in range(num_eyes):
        parent = reader.read_int32()
        pos = reader.read_vector3d()
        norm = reader.read_vector3d()
        eyes.append(
            {"parent": parent, "position": pos.to_list(), "normal": norm.to_list()}
        )
    return eyes
