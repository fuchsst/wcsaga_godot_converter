#!/usr/bin/env python3
"""
Converter Registry - Registry Pattern Implementation

Replaces the factory pattern with a registry pattern for automatic
converter discovery and registration, following Open/Closed Principle.

Author: Dev (GDScript Developer)
Date: June 15, 2025
Story: DM-009 - SOLID Principle Refactoring
Epic: EPIC-003 - Data Migration & Conversion Tools
"""

import inspect
from pathlib import Path
from typing import Dict, List, Optional, Type, Callable

from .table_types import TableType
from .base_converter import BaseTableConverter


class ConverterRegistry:
    """
    Registry for table converters using automatic discovery.

    Replaces the factory pattern with a more flexible registry pattern
    that supports automatic converter registration and discovery.
    """

    _registry: Dict[TableType, Callable[[Path, Path], BaseTableConverter]] = {}
    _type_patterns: Dict[TableType, List[str]] = {}
    _content_patterns: Dict[TableType, List[str]] = {}

    @classmethod
    def register(
        cls,
        table_type: TableType,
        converter_factory: Callable[[Path, Path], BaseTableConverter],
        filename_patterns: Optional[List[str]] = None,
        content_patterns: Optional[List[str]] = None,
    ) -> None:
        """
        Register a converter factory for a table type.

        Args:
            table_type: The table type this converter handles
            converter_factory: Factory function that creates converter instances
            filename_patterns: Optional filename patterns for auto-detection
            content_patterns: Optional content patterns for auto-detection
        """
        cls._registry[table_type] = converter_factory

        if filename_patterns:
            cls._type_patterns[table_type] = filename_patterns
        if content_patterns:
            cls._content_patterns[table_type] = content_patterns

    @classmethod
    def create_converter(
        cls, table_type: TableType, source_dir: Path, target_dir: Path
    ) -> BaseTableConverter:
        """
        Create a converter for the specified table type.

        Args:
            table_type: Type of table to convert
            source_dir: WCS source directory containing table files
            target_dir: Target Godot project directory for output

        Returns:
            Appropriate converter instance for the table type

        Raises:
            ValueError: If table_type is not registered
        """
        if table_type not in cls._registry:
            raise ValueError(f"No converter registered for table type: {table_type}")

        return cls._registry[table_type](source_dir, target_dir)

    @classmethod
    def get_converter_for_file(
        cls, table_file: Path, source_dir: Path, target_dir: Path
    ) -> Optional[BaseTableConverter]:
        """
        Create a converter for the specified table file.

        Args:
            table_file: Path to the table file
            source_dir: WCS source directory containing table files
            target_dir: Target Godot project directory for output

        Returns:
            Appropriate converter instance for the table file, or None if file type is unknown
        """
        table_type = cls._determine_table_type(table_file)
        if table_type == TableType.UNKNOWN:
            return None

        return cls.create_converter(table_type, source_dir, target_dir)

    @classmethod
    def _determine_table_type(cls, table_file: Path) -> TableType:
        """Determine the type of table file using centralized detection."""
        from ..core.common_utils import TableTypeDetector

        return TableTypeDetector.get_table_type_enum(table_file)

    @classmethod
    def get_registered_types(cls) -> List[TableType]:
        """Get list of all registered table types."""
        return list(cls._registry.keys())

    @classmethod
    def is_type_registered(cls, table_type: TableType) -> bool:
        """Check if a table type has a registered converter."""
        return table_type in cls._registry


def auto_register_converters() -> None:
    """
    Automatically register all converters in the table_converters module.

    This function uses introspection to find all converter classes
    and register them with the appropriate table types.
    """
    import sys
    import os

    # Get the table_converters module
    current_dir = os.path.dirname(__file__)
    converter_files = [
        f
        for f in os.listdir(current_dir)
        if f.endswith("_converter.py") and f != "base_converter.py"
    ]

    for converter_file in converter_files:
        module_name = converter_file[:-3]  # Remove .py

        try:
            # Import the converter module
            module = __import__(
                f"data_converter.table_converters.{module_name}", fromlist=["*"]
            )

            # Find converter classes in the module
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if name.endswith("Converter") and name != "BaseTableConverter":
                    # Check if the class has table type information
                    if hasattr(obj, "TABLE_TYPE") and hasattr(obj, "FILENAME_PATTERNS"):
                        ConverterRegistry.register(
                            table_type=obj.TABLE_TYPE,
                            converter_factory=obj,
                            filename_patterns=obj.FILENAME_PATTERNS,
                            content_patterns=getattr(obj, "CONTENT_PATTERNS", None),
                        )

        except ImportError as e:
            print(f"Warning: Could not import {module_name}: {e}")
        except Exception as e:
            print(f"Warning: Error processing {module_name}: {e}")


# Initialize the registry with auto-registration
auto_register_converters()
