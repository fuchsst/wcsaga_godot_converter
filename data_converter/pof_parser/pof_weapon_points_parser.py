#!/usr/bin/env python3
import logging
from typing import Any, BinaryIO, Dict, List

# Import unified binary reader
from .pof_binary_reader import create_reader

# Import Vector3D if needed for type hinting or direct use
# from .pof_types import Vector3D

logger = logging.getLogger(__name__)


def read_gpnt_chunk(f: BinaryIO, length: int) -> List[Dict[str, Any]]:
    """Parses the Gun Points (GPNT) chunk."""
    reader = create_reader(f)
    logger.debug("Reading GPNT chunk...")
    num_banks = reader.read_int32()
    gun_banks = []
    for _ in range(num_banks):
        bank = {"points": []}
        num_slots = reader.read_int32()
        bank["num_slots"] = num_slots
        for _ in range(num_slots):
            pos = reader.read_vector3d()
            norm = reader.read_vector3d()
            bank["points"].append({"position": pos.to_list(), "normal": norm.to_list()})
        gun_banks.append(bank)
    return gun_banks


def read_mpnt_chunk(f: BinaryIO, length: int) -> List[Dict[str, Any]]:
    """Parses the Missile Points (MPNT) chunk."""
    reader = create_reader(f)
    logger.debug("Reading MPNT chunk...")
    num_banks = reader.read_int32()
    missile_banks = []
    for _ in range(num_banks):
        bank = {"points": []}
        num_slots = reader.read_int32()
        bank["num_slots"] = num_slots
        for _ in range(num_slots):
            pos = reader.read_vector3d()
            norm = reader.read_vector3d()
            bank["points"].append({"position": pos.to_list(), "normal": norm.to_list()})
        missile_banks.append(bank)
    return missile_banks
