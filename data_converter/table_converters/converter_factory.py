#!/usr/bin/env python3
"""
Converter Factory

Factory pattern implementation for creating table converters.

Author: Qwen AI Assistant
Date: Today
"""

from pathlib import Path
from typing import Optional

from .table_types import TableType


class ConverterFactory:
    """
    Factory for creating table converters.

    Uses the factory pattern to instantiate the appropriate converter
    based on the table type.
    """

    @staticmethod
    def create_converter(table_type: TableType, source_dir: Path, target_dir: Path):
        """
        Create a converter for the specified table type.

        Args:
            table_type: Type of table to convert
            source_dir: WCS source directory containing table files
            target_dir: Target Godot project directory for output

        Returns:
            Appropriate converter instance for the table type

        Raises:
            ValueError: If table_type is not supported
        """
        if table_type == TableType.SHIPS:
            from .ship_table_converter import ShipTableConverter

            return ShipTableConverter(source_dir, target_dir)
        elif table_type == TableType.WEAPONS:
            from .weapon_table_converter import WeaponTableConverter

            return WeaponTableConverter(source_dir, target_dir)
        elif table_type == TableType.ARMOR:
            from .armor_table_converter import ArmorTableConverter

            return ArmorTableConverter(source_dir, target_dir)
        elif table_type == TableType.SPECIES:
            from .species_defs_table_converter import SpeciesDefsTableConverter

            return SpeciesDefsTableConverter(source_dir, target_dir)
        elif table_type == TableType.IFF:
            from .iff_table_converter import IFFTableConverter

            return IFFTableConverter(source_dir, target_dir)
        elif table_type == TableType.CREDITS:
            from .credits_table_converter import CreditsTableConverter

            return CreditsTableConverter(source_dir, target_dir)
        elif table_type == TableType.HELP:
            from .help_table_converter import HelpTableConverter

            return HelpTableConverter(source_dir, target_dir)
        elif table_type == TableType.TIPS:
            from .tips_table_converter import TipsTableConverter

            return TipsTableConverter(source_dir, target_dir)
        else:
            raise ValueError(f"Unsupported table type: {table_type}")

    @staticmethod
    def get_converter_for_file(table_file: Path, source_dir: Path, target_dir: Path):
        """
        Create a converter for the specified table file.

        Args:
            table_file: Path to the table file
            source_dir: WCS source directory containing table files
            target_dir: Target Godot project directory for output

        Returns:
            Appropriate converter instance for the table file, or None if file type is unknown
        """
        table_type = ConverterFactory._determine_table_type(table_file)
        if table_type == TableType.UNKNOWN:
            return None

        return ConverterFactory.create_converter(table_type, source_dir, target_dir)

    @staticmethod
    def _determine_table_type(table_file: Path) -> TableType:
        """Determine the type of table file using centralized detection."""
        from ..core.common_utils import TableTypeDetector

        return TableTypeDetector.get_table_type_enum(table_file)
