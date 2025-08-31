#!/usr/bin/env python3
"""
Unified Base Table Converter

Provides common functionality for all WCS table converters with a clean,
SOLID-compliant architecture. Uses composition over inheritance where possible.

SOLID Principles Applied:
- Single Responsibility: Separates file handling, parsing, and conversion
- Open/Closed: Open for extension via strategy pattern, closed for modification
- Liskov Substitution: All table converters can be used interchangeably
- Interface Segregation: Focused interfaces for different responsibilities
- Dependency Inversion: Depends on abstractions, not concrete implementations
"""

import logging
import re
from abc import abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, Tuple

from ..core.common_utils import ConversionUtils
from ..core.interfaces import IFileConverter, IValidatableConverter
from ..core.table_data_structures import TableType

logger = logging.getLogger(__name__)


class ParseError(Exception):
    """Custom exception for table parsing errors"""

    def __init__(self, message: str, line_number: int = -1, filename: str = ""):
        self.message = message
        self.line_number = line_number
        self.filename = filename
        super().__init__(
            f"{filename}:{line_number}: {message}" if line_number > 0 else message
        )


@dataclass
class ParseState:
    """Maintains state during table parsing"""

    lines: List[str] = field(default_factory=list)
    current_line: int = 0
    filename: str = ""
    in_multiline_comment: bool = False
    current_section: str = ""

    def has_more_lines(self) -> bool:
        return self.current_line < len(self.lines)

    def peek_line(self) -> Optional[str]:
        if self.has_more_lines():
            return self.lines[self.current_line]
        return None

    def next_line(self) -> Optional[str]:
        if self.has_more_lines():
            line = self.lines[self.current_line]
            self.current_line += 1
            return line
        return None

    def skip_line(self) -> None:
        if self.has_more_lines():
            self.current_line += 1


class TableParser(Protocol):
    """Protocol defining the interface for table parsers"""

    def parse_line(self, line: str, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single line and return data if complete entry found"""
        ...

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed table entry"""
        ...


class ResourceConverter(Protocol):
    """Protocol defining the interface for resource converters"""

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed entries to Godot resource format"""
        ...


class BaseTableConverter(IFileConverter, IValidatableConverter):
    """
    Unified base class for all table converters.

    Implements Template Method pattern for consistent parsing workflow.
    Uses composition for parsing and conversion strategies.
    """

    # Metadata for auto-registration (must be defined by subclasses)
    TABLE_TYPE: TableType = TableType.UNKNOWN
    FILENAME_PATTERNS: List[str] = []
    CONTENT_PATTERNS: List[str] = []

    def __init__(self, source_dir: Path, target_dir: Path):
        """
        Initialize the base converter.

        Args:
            source_dir: WCS source directory containing table files
            target_dir: Target Godot project directory for output
        """
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.assets_dir = self.target_dir / "assets" / "tables"
        self.logger = logging.getLogger(self.__class__.__name__)

        # Ensure output directory exists
        self.assets_dir.mkdir(parents=True, exist_ok=True)

        # Initialize parsing patterns
        self._parse_patterns = self._init_parse_patterns()

    @abstractmethod
    def _init_parse_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for parsing this table type"""
        pass

    def get_table_type(self) -> TableType:
        """Return the table type this converter handles"""
        return self.TABLE_TYPE

    @abstractmethod
    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single table entry from the current position"""
        pass

    @abstractmethod
    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed table entry"""
        pass

    @abstractmethod
    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed entries to Godot resource format"""
        pass

    def convert_table_file(
        self, table_path: Path, output_path: Optional[Path] = None
    ) -> bool:
        """
        Main conversion method (Template Method pattern).
        Defines the algorithm for converting any table file.
        """
        try:
            # Use default output path if not specified
            if output_path is None:
                output_path = self.assets_dir / f"{table_path.stem}.tres"

            # Step 1: Load and prepare file
            content = self._load_file(table_path)
            state = self._prepare_parse_state(content, str(table_path))

            # Step 2: Parse all entries
            entries = self._parse_all_entries(state)

            # Step 3: Validate entries
            valid_entries = self._validate_all_entries(entries)

            # Step 4: Convert to Godot format
            godot_resource = self.convert_to_godot_resource(valid_entries)

            # Step 5: Save result
            return self._save_resource(godot_resource, output_path)

        except Exception as e:
            self.logger.error(f"Failed to convert {table_path}: {e}")
            return False

    def _load_file(self, table_path: Path) -> str:
        """Load table file content using common utilities"""
        lines = ConversionUtils.load_table_file(table_path)
        if lines is None:
            return ""
        return "\n".join(lines)

    def _prepare_parse_state(self, content: str, filename: str) -> ParseState:
        """Prepare parsing state from file content"""
        lines = content.split("\n")
        return ParseState(lines=lines, filename=filename)

    def _parse_all_entries(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse all entries from the table"""
        entries = []
        while state.has_more_lines():
            # Check for section headers
            line = state.peek_line()
            if line:
                line = line.strip()
                # Check for section header patterns
                if line.startswith("#") and not line.startswith(("#", "$", "+", ";")):
                    # This is a section header, store it
                    state.current_section = line.strip("#").strip()
                    state.skip_line()  # Skip the section header line
                    continue

            entry = self.parse_entry(state)
            if entry:
                entries.append(entry)
        return entries

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire table and return all entries"""
        return self._parse_all_entries(state)

    def _validate_all_entries(
        self, entries: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Validate all parsed entries"""
        valid_entries = []

        for entry in entries:
            if self.validate_entry(entry):
                valid_entries.append(entry)
            else:
                self.logger.warning(
                    f"Invalid entry skipped: {entry.get('name', 'Unknown')}"
                )

        return valid_entries

    def _save_resource(self, resource: Dict[str, Any], output_path: Path) -> bool:
        """Save Godot resource to file using common utilities"""
        # Convert resource to string content
        content = self._convert_resource_to_string(resource)
        return ConversionUtils.create_resource_file(content, output_path)

    def _convert_resource_to_string(self, resource: Dict[str, Any]) -> str:
        """Convert resource dictionary to string content"""
        lines = ['[gd_resource type="Resource"]', "", "[resource]"]
        for key, value in resource.items():
            lines.append(f"{key} = {self._format_value(value)}")
        return "\n".join(lines)

    def _format_value(self, value: Any) -> str:
        """Format a value for Godot TRES format"""
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, list):
            formatted_items = [self._format_value(item) for item in value]
            return f"[{', '.join(formatted_items)}]"
        elif isinstance(value, dict):
            formatted_items = [
                f"{k}: {self._format_value(v)}" for k, v in value.items()
            ]
            return f"{{{', '.join(formatted_items)}}}"
        else:
            return f'"{str(value)}"'

    def _should_skip_line(self, line: str, state: ParseState) -> bool:
        """Check if line should be skipped (comments, empty lines)"""
        line = line.strip()

        # Empty line
        if not line:
            return True

        # Handle multi-line comments
        if "/*" in line:
            state.in_multiline_comment = True
            return False  # Don't skip the line that starts the comment
        if "*/" in line:
            state.in_multiline_comment = False
            return True
        if state.in_multiline_comment:
            return True

        # Single-line comments
        if line.startswith("//") or line.startswith(";"):
            return True

        return False

    def parse_value(self, value_str: str, expected_type: type = str) -> Any:
        """Parse a value string to the expected type"""
        try:
            if expected_type == str:
                # Strip surrounding quotes if they exist
                if value_str.startswith('"') and value_str.endswith('"'):
                    return value_str[1:-1]
                elif value_str.startswith("'") and value_str.endswith("'"):
                    return value_str[1:-1]
                return value_str
            elif expected_type == int:
                return int(value_str)
            elif expected_type == float:
                return float(value_str)
            elif expected_type == bool:
                return value_str.lower() in ("true", "yes", "1", "on")
            else:
                return value_str
        except (ValueError, TypeError):
            # Return default values for failed conversions
            if expected_type == int:
                return 0
            elif expected_type == float:
                return 0.0
            elif expected_type == bool:
                return False
            else:
                return ""

    # Common utility methods that use the shared ConversionUtils
    def _extract_string_value(self, line: str) -> str:
        """Extract string value from table line"""
        return ConversionUtils.extract_string_value(line)

    def _extract_int_value(self, line: str) -> int:
        """Extract integer value from table line"""
        return ConversionUtils.extract_int_value(line)

    def _extract_float_value(self, line: str) -> float:
        """Extract float value from table line"""
        return ConversionUtils.extract_float_value(line)

    def _extract_bool_value(self, line: str) -> bool:
        """Extract boolean value from table line"""
        return ConversionUtils.extract_bool_value(line)

    def _extract_vector3(self, line: str) -> Tuple[float, float, float]:
        """Extract Vector3 values from table line"""
        return ConversionUtils.extract_vector3(line)

    def _extract_string_list(self, line: str) -> List[str]:
        """Extract list of strings from table line"""
        return ConversionUtils.extract_string_list(line)

    def _extract_int_list(self, line: str) -> List[int]:
        """Extract list of integers from table line"""
        return ConversionUtils.extract_int_list(line)

    def _preprocess_lines(self, raw_lines: List[str]) -> List[str]:
        """Preprocess table lines (comments, continuations, etc.)"""
        return ConversionUtils.preprocess_lines(raw_lines)

    def _load_table_file_lines(self, table_file: Path) -> Optional[List[str]]:
        """Load and preprocess table file content"""
        return ConversionUtils.load_table_file_lines(table_file)

    # IFileConverter interface implementation
    def can_convert(self, file_path: Path) -> bool:
        """Check if this converter can handle the given file."""
        from ..core.common_utils import TableTypeDetector

        detected_type = TableTypeDetector.determine_table_type(file_path)

        # Convert TableType enum to string for comparison
        expected_type = (
            self.TABLE_TYPE.value if self.TABLE_TYPE != TableType.UNKNOWN else None
        )
        return detected_type == expected_type

    def convert_file(self, file_path: Path, target_path: Optional[Path] = None) -> bool:
        """Convert a single file (IFileConverter interface)."""
        return self.convert_table_file(file_path, target_path)

    # IValidatableConverter interface implementation
    def validate_conversion(self, source_path: Path, target_path: Path) -> bool:
        """Validate conversion results."""
        from ..core.common_utils import ValidationFramework

        # Check if target file exists and has content
        if not ValidationFramework.validate_conversion_output(target_path):
            return False

        # Additional validation can be added by subclasses
        return True

    def get_stats(self) -> Dict[str, Any]:
        """Get conversion statistics for this converter instance."""
        return {
            "entries_processed": getattr(self, "_entries_processed", 0),
            "errors": getattr(self, "_conversion_errors", []),
            "warnings": getattr(self, "_conversion_warnings", []),
        }

    def get_registries(self) -> Dict[str, Any]:
        """Get asset registries for relationship mapping."""
        return {
            "asset_registry": getattr(self, "_asset_registry", {}),
            "relationship_mappings": getattr(self, "_relationship_mappings", {}),
        }
