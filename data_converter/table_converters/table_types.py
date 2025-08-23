#!/usr/bin/env python3
"""
Table Types Enum

Enumeration of supported table types for the converter system.

Author: Qwen AI Assistant
Date: Today
"""

from enum import Enum


class TableType(Enum):
    """Table file types supported by the converter system."""
    SHIPS = "ships"
    WEAPONS = "weapons"
    ARMOR = "armor"
    SPECIES = "species_defs"
    IFF = "iff_defs"
    UNKNOWN = "unknown"