#!/usr/bin/env python3
"""
POF Chunks - Consolidated chunk constants and utilities.

This module provides constants and utility functions for POF file chunks.
All binary reading functionality has been moved to pof_binary_reader.py.
"""

import logging
import struct
from typing import BinaryIO

logger = logging.getLogger(__name__)

# --- POF Chunk IDs (from modelsinc.h) ---

# POF Header ID and Version constants
POF_HEADER_ID = 0x4F505350  # 'OPSP'
PM_COMPATIBLE_VERSION = 1900
PM_OBJFILE_MAJOR_VERSION = 30

# Main POF Chunk IDs
ID_OHDR = 0x32524448  # HDR2 - Object Header
ID_SOBJ = 0x324A424F  # OBJ2 - Subobject
ID_TXTR = 0x52545854  # TXTR - Textures
ID_INFO = 0x464E4950  # PINF - Info (Deprecated?)
ID_GRID = 0x44495247  # GRID - Grid (Unused?)
ID_SPCL = 0x4C435053  # SPCL - Special Points
ID_PATH = 0x48544150  # PATH - Animation Paths
ID_GPNT = 0x544E5047  # GPNT - Gun Points
ID_MPNT = 0x544E504D  # MPNT - Missile Points
ID_DOCK = 0x4B434F44  # DOCK - Docking Points
ID_TGUN = 0x4E554754  # TGUN - Turret Gun (Deprecated)
ID_TMIS = 0x53494D54  # TMIS - Turret Missile (Deprecated)
ID_FUEL = 0x4C455546  # FUEL - Thrusters/Fuel
ID_SHLD = 0x444C4853  # SHLD - Shield Mesh
ID_EYE = 0x20455945  # EYE  - Eye Points
ID_INSG = 0x47534E49  # INSG - Insignia
ID_ACEN = 0x4E454341  # ACEN - Auto-center
ID_GLOW = 0x574F4C47  # GLOW - Glow Points
ID_GLOX = 0x584f4c47  # GLOX - Glow Points Extended (Unused)
ID_SLDC = 0x43444C53  # SLDC - Shield Collision Tree

# BSP Chunk IDs (from modelinterp.cpp and modelsinc.h)
OP_EOF = 0
OP_DEFPOINTS = 1
OP_FLATPOLY = 2
OP_TMAPPOLY = 3
OP_SORTNORM = 4
OP_BOUNDBOX = 5

# --- Constants ---

# String length constants
MAX_NAME_LEN = 32
MAX_PROP_LEN = 256

# Model structure constants
MAX_DEBRIS_OBJECTS = 32
MAX_MODEL_DETAIL_LEVELS = 8
MAX_MODEL_TEXTURES = 35  # From model.h
MAX_SLOTS = 25  # Max gun/missile slots per bank
MAX_DOCK_SLOTS = 2
MAX_TFP = 10  # Max turret firing points
MAX_EYES = 10
MAX_SPLIT_PLANE = 5
MAX_REPLACEMENT_TEXTURES = MAX_MODEL_TEXTURES * 5  # From model.h TM_NUM_TYPES


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
    
    try:
        f.seek(length, 1)
    except Exception as e:
        logger.error(f"Error seeking past unknown chunk {chunk_id_str}: {e}")
        raise EOFError(f"Could not seek past unknown chunk {chunk_id_str}")


# --- Utility Functions ---

def get_chunk_name(chunk_id: int) -> str:
    """Get human-readable name for chunk ID."""
    chunk_names = {
        ID_OHDR: "HDR2",
        ID_SOBJ: "OBJ2", 
        ID_TXTR: "TXTR",
        ID_INFO: "PINF",
        ID_GRID: "GRID",
        ID_SPCL: "SPCL",
        ID_PATH: "PATH",
        ID_GPNT: "GPNT",
        ID_MPNT: "MPNT",
        ID_DOCK: "DOCK",
        ID_TGUN: "TGUN",
        ID_TMIS: "TMIS",
        ID_FUEL: "FUEL",
        ID_SHLD: "SHLD",
        ID_EYE: "EYE",
        ID_INSG: "INSG",
        ID_ACEN: "ACEN",
        ID_GLOW: "GLOW",
        ID_GLOX: "GLOX",
        ID_SLDC: "SLDC",
        OP_EOF: "EOF",
        OP_DEFPOINTS: "DEFPOINTS",
        OP_FLATPOLY: "FLATPOLY",
        OP_TMAPPOLY: "TMAPPOLY",
        OP_SORTNORM: "SORTNORM",
        OP_BOUNDBOX: "BOUNDBOX",
    }
    
    if chunk_id in chunk_names:
        return chunk_names[chunk_id]
    
    # Try to decode as ASCII
    try:
        chunk_str = struct.pack("<I", chunk_id).decode("ascii", errors="replace")
        # Remove non-printable characters
        chunk_str = "".join(c if c.isprintable() else "?" for c in chunk_str)
        return chunk_str
    except:
        return f"UNK_{chunk_id:08X}"


def is_valid_chunk_length(length: int) -> bool:
    """Validate chunk length is reasonable."""
    # Negative lengths are invalid
    if length < 0:
        return False
    
    # Extremely large chunks are suspicious
    if length > 100 * 1024 * 1024:  # 100MB limit
        return False
    
    return True



