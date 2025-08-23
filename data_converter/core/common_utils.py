#!/usr/bin/env python3
"""
Common Utilities - Code Duplication Elimination

Extracts common utility functions that were duplicated across multiple
converter classes to eliminate code duplication.

Author: Dev (GDScript Developer)
Date: June 15, 2025
Story: DM-009 - SOLID Principle Refactoring
Epic: EPIC-003 - Data Migration & Conversion Tools
"""

import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class ConversionUtils:
    """
    Common utility functions for data conversion operations.

    Extracts functionality that was duplicated across multiple converter classes.
    """

    @staticmethod
    def extract_string_value(line: str) -> str:
        """Extract string value from table line."""
        if ":" not in line:
            return ""
        value = line.split(":", 1)[1].strip()
        # Remove quotes if present
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        return value

    @staticmethod
    def extract_int_value(line: str) -> int:
        """Extract integer value from table line."""
        try:
            value_str = ConversionUtils.extract_string_value(line)
            return int(float(value_str))  # Handle float strings like "1.0"
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def extract_float_value(line: str) -> float:
        """Extract float value from table line."""
        try:
            value_str = ConversionUtils.extract_string_value(line)
            return float(value_str)
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def extract_bool_value(line: str) -> bool:
        """Extract boolean value from table line."""
        value_str = ConversionUtils.extract_string_value(line).lower()
        return value_str in ("true", "yes", "1", "on")

    @staticmethod
    def extract_vector3(line: str) -> Tuple[float, float, float]:
        """Extract Vector3 values from table line."""
        try:
            value_str = ConversionUtils.extract_string_value(line)
            # Remove parentheses and split by comma
            value_str = value_str.strip("()[]")
            parts = [p.strip() for p in value_str.split(",")]
            if len(parts) >= 3:
                return (float(parts[0]), float(parts[1]), float(parts[2]))
            else:
                return (0.0, 0.0, 0.0)
        except (ValueError, TypeError, IndexError):
            return (0.0, 0.0, 0.0)

    @staticmethod
    def extract_string_list(line: str) -> List[str]:
        """Extract list of strings from table line."""
        try:
            value_str = ConversionUtils.extract_string_value(line)
            # Remove parentheses and split by comma
            value_str = value_str.strip("()[]")
            if not value_str:
                return []
            parts = [p.strip().strip('"') for p in value_str.split(",")]
            return [p for p in parts if p]  # Filter empty strings
        except (ValueError, TypeError):
            return []

    @staticmethod
    def extract_int_list(line: str) -> List[int]:
        """Extract list of integers from table line."""
        try:
            value_str = ConversionUtils.extract_string_value(line)
            # Remove parentheses and split by comma
            value_str = value_str.strip("()[]")
            if not value_str:
                return []
            parts = [p.strip() for p in value_str.split(",")]
            return [int(float(p)) for p in parts if p]  # Handle float strings
        except (ValueError, TypeError):
            return []

    @staticmethod
    def preprocess_lines(raw_lines: List[str]) -> List[str]:
        """Preprocess table lines (comments, continuations, etc.)."""
        processed_lines = []
        in_block_comment = False

        for line in raw_lines:
            line = line.rstrip("\n\r")

            # Handle block comments
            if "/*" in line and "*/" in line:
                # Single line block comment
                start = line.find("/*")
                end = line.find("*/") + 2
                line = line[:start] + line[end:]
            elif "/*" in line:
                # Start of block comment
                in_block_comment = True
                line = line[: line.find("/*")]
            elif "*/" in line and in_block_comment:
                # End of block comment
                in_block_comment = False
                line = line[line.find("*/") + 2 :]
            elif in_block_comment:
                # Skip lines inside block comment
                continue

            # Handle line comments
            if ";" in line and not in_block_comment:
                line = line[: line.find(";")]

            # Skip empty lines and comment-only lines
            line = line.strip()
            if not line:
                continue

            processed_lines.append(line)

        return processed_lines

    @staticmethod
    def load_table_file(table_file: Path) -> Optional[List[str]]:
        """Load and preprocess table file content."""
        try:
            with open(table_file, "r", encoding="utf-8", errors="replace") as f:
                raw_lines = f.readlines()

            return ConversionUtils.preprocess_lines(raw_lines)

        except Exception as e:
            logging.getLogger(__name__).error(
                f"Failed to load table file {table_file}: {e}"
            )
            return None

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for cross-platform compatibility."""
        # Replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        sanitized = filename

        for char in invalid_chars:
            sanitized = sanitized.replace(char, "_")

        # Remove leading/trailing dots and spaces
        sanitized = sanitized.strip(". ")

        # Ensure it's not empty
        if not sanitized:
            sanitized = "unnamed"

        return sanitized

    @staticmethod
    def ensure_directory_exists(directory: Path) -> bool:
        """Ensure directory exists, creating it if necessary."""
        try:
            directory.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logging.getLogger(__name__).error(
                f"Failed to create directory {directory}: {e}"
            )
            return False

    @staticmethod
    def create_resource_file(content: str, target_path: Path) -> bool:
        """Create a resource file with the given content."""
        try:
            ConversionUtils.ensure_directory_exists(target_path.parent)

            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)

            return True

        except Exception as e:
            logging.getLogger(__name__).error(
                f"Failed to create resource file {target_path}: {e}"
            )
            return False


class ValidationFramework:
    """
    Common validation framework for conversion operations.

    Provides standardized validation methods that were duplicated
    across multiple converter classes.
    """

    @staticmethod
    def validate_file_exists(file_path: Path) -> bool:
        """Validate that a file exists and is readable."""
        if not file_path.exists():
            logging.getLogger(__name__).error(f"File does not exist: {file_path}")
            return False

        if file_path.is_file() and not file_path.is_readable():
            logging.getLogger(__name__).error(f"File is not readable: {file_path}")
            return False

        return True

    @staticmethod
    def validate_conversion_output(target_path: Path, min_size: int = 1) -> bool:
        """Validate conversion output file."""
        if not target_path.exists():
            logging.getLogger(__name__).error(
                f"Output file does not exist: {target_path}"
            )
            return False

        if target_path.stat().st_size < min_size:
            logging.getLogger(__name__).warning(
                f"Output file is empty or too small: {target_path}"
            )
            return False

        return True

    @staticmethod
    def validate_resource_content(
        content: str, required_fields: List[str] = None
    ) -> bool:
        """Validate Godot resource file content."""
        if not content.startswith("[gd_resource"):
            logging.getLogger(__name__).error(
                "Invalid resource format: missing [gd_resource] header"
            )
            return False

        if required_fields:
            for field in required_fields:
                if field not in content:
                    logging.getLogger(__name__).warning(
                        f"Resource missing required field: {field}"
                    )
                    return False

        return True


class TableTypeDetector:
    """
    Centralized table type detection to eliminate code duplication.

    Replaces duplicate _determine_table_type methods found in:
    - converter_factory.py:76
    - converter_registry.py:96
    - base_converter.py:59
    - ship_converter.py:91
    - base_strategy.py:118
    """

    # Table type patterns for filename and content detection
    TABLE_PATTERNS = {
        "ships": {
            "filename": ["ship"],
            "content": ["#ship classes", "$name:", "$pof file:"],
        },
        "weapons": {
            "filename": ["weapon"],
            "content": ["#primary weapons", "#secondary weapons", "$damage:"],
        },
        "armor": {"filename": ["armor"], "content": ["#armor type", "$reduction:"]},
        "species_defs": {
            "filename": ["species_defs", "species"],
            "content": ["#species defs", "$iff:"],
        },
        "iff_defs": {"filename": ["iff"], "content": ["#iffs", "$iff name:"]},
        "ai_profiles": {"filename": ["ai_profiles"], "content": ["#ai profiles"]},
        "asteroid": {"filename": ["asteroid"], "content": ["#asteroid types"]},
        "cutscenes": {"filename": ["cutscenes"], "content": ["#cutscenes"]},
        "fireball": {"filename": ["fireball"], "content": ["#fireball types"]},
        "hud_gauges": {"filename": ["hud_gauges"], "content": ["#hud gauges"]},
        "lightning": {"filename": ["lightning"], "content": ["#lightning types"]},
        "medals": {"filename": ["medals"], "content": ["#medals"]},
        "music": {"filename": ["music"], "content": ["#music entries"]},
        "rank": {"filename": ["rank"], "content": ["#rank names"]},
        "scripting": {"filename": ["scripting"], "content": ["#scripting hooks"]},
        "sounds": {"filename": ["sounds"], "content": ["#sound entries"]},
        "stars": {"filename": ["stars"], "content": ["#star types"]},
        "strings": {"filename": ["strings"], "content": ["#string entries"]},
    }

    @staticmethod
    def determine_table_type(table_file: Path) -> str:
        """
        Determine the type of table file using centralized logic.

        Args:
            table_file: Path to the table file

        Returns:
            Table type as string (e.g., 'ships', 'weapons', 'armor')
            Returns 'unknown' if type cannot be determined
        """
        filename = table_file.name.lower()

        # Check filename patterns first
        for table_type, patterns in TableTypeDetector.TABLE_PATTERNS.items():
            for pattern in patterns["filename"]:
                if pattern in filename:
                    return table_type

        # Check content patterns if filename didn't match
        try:
            with open(table_file, "r", encoding="utf-8", errors="replace") as f:
                first_lines = f.read(1000).lower()

            for table_type, patterns in TableTypeDetector.TABLE_PATTERNS.items():
                for pattern in patterns["content"]:
                    if pattern in first_lines:
                        return table_type

        except Exception:
            pass

        return "unknown"

    @staticmethod
    def get_table_type_enum(table_file: Path) -> "TableType":
        """
        Determine table type and return as TableType enum.

        Args:
            table_file: Path to the table file

        Returns:
            TableType enum value
        """
        table_type_str = TableTypeDetector.determine_table_type(table_file)

        # Map string to TableType enum
        try:
            # Try different import paths to handle different execution contexts
            try:
                from ..table_converters.table_types import TableType
            except ImportError:
                from table_converters.table_types import TableType
            return TableType[table_type_str.upper()]
        except (ImportError, KeyError):
            try:
                from ..table_converters.table_types import TableType
            except ImportError:
                from table_converters.table_types import TableType
            return TableType.UNKNOWN
