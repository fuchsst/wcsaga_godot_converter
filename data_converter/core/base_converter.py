#!/usr/bin/env python3
"""
Base Data Converter - EPIC-003 DM-008 Implementation

Abstract base class for all data converters in the WCS-Godot conversion pipeline.
Provides common functionality and structure for consistent converter behavior.

Following Interface Segregation Principle (ISP) with specialized interfaces.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional

from .data_structures import ConversionReport, ConversionSettings
from .interfaces import (
    IFileConverter,
    IDirectoryConverter,
)


class ConversionType(Enum):
    """Supported conversion types."""

    TABLE = "table"
    POF = "pof"
    VP = "vp"
    MISSION = "mission"
    UNKNOWN = "unknown"


@dataclass
class ConversionContext:
    """Context information for conversion operations."""

    source_path: Path
    target_path: Path
    conversion_type: ConversionType
    settings: ConversionSettings = field(default_factory=ConversionSettings)
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseDataConverter(ABC, IFileConverter, IDirectoryConverter):
    """
    Abstract base class for all data converters.

    Provides common functionality and structure for consistent converter behavior
    following the Template Method pattern. Subclasses implement specific conversion
    logic while inheriting common infrastructure.

    Implements IFileConverter and IDirectoryConverter interfaces by default.
    Subclasses can implement additional interfaces as needed.
    """

    def __init__(self, source_dir: Path, target_dir: Path):
        """
        Initialize base data converter.

        Args:
            source_dir: Source directory containing files to convert
            target_dir: Target directory for converted output
        """
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.conversion_stats: Dict[str, Any] = {
            "files_processed": 0,
            "files_converted": 0,
            "files_failed": 0,
            "errors": [],
            "warnings": [],
        }

    @abstractmethod
    def can_convert(self, file_path: Path) -> bool:
        """
        Check if this converter can handle the given file.

        Args:
            file_path: Path to file to check

        Returns:
            True if converter can handle file, False otherwise
        """
        pass

    @abstractmethod
    def convert_file(self, file_path: Path, target_path: Optional[Path] = None) -> bool:
        """
        Convert a single file.

        Args:
            file_path: Path to source file to convert
            target_path: Optional target path for output

        Returns:
            True if conversion successful, False otherwise
        """
        pass

    def convert_directory(
        self, source_dir: Path, target_dir: Path, pattern: str = "*"
    ) -> ConversionReport:
        """
        Convert all matching files in directory.

        Args:
            source_dir: Directory containing files to convert
            target_dir: Target directory for converted output
            pattern: File pattern to match (glob syntax)

        Returns:
            ConversionReport with detailed results
        """
        self.logger.warning("Default directory conversion not implemented")
        return ConversionReport(
            source_file=str(source_dir),
            target_file=str(target_dir),
            conversion_type="directory",
            files_processed=0,
            files_converted=0,
            files_failed=0,
            errors=["Directory conversion not implemented"],
            warnings=[],
            metadata={},
        )

    def _validate_paths(self, source_path: Path, target_path: Path) -> bool:
        """
        Validate source and target paths.

        Args:
            source_path: Source file or directory path
            target_path: Target file or directory path

        Returns:
            True if paths are valid, False otherwise
        """
        if not source_path.exists():
            self.logger.error(f"Source path does not exist: {source_path}")
            return False

        if source_path.is_file() and not source_path.is_readable():
            self.logger.error(f"Source file is not readable: {source_path}")
            return False

        # Ensure target directory exists
        target_path.parent.mkdir(parents=True, exist_ok=True)

        return True

    def _create_conversion_report(self, context: ConversionContext) -> ConversionReport:
        """
        Create conversion report from context and stats.

        Args:
            context: Conversion context information

        Returns:
            ConversionReport with current state
        """
        return ConversionReport(
            source_file=str(context.source_path),
            target_file=str(context.target_path),
            conversion_type=context.conversion_type.value,
            files_processed=self.conversion_stats["files_processed"],
            files_converted=self.conversion_stats["files_converted"],
            files_failed=self.conversion_stats["files_failed"],
            errors=self.conversion_stats["errors"],
            warnings=self.conversion_stats["warnings"],
            metadata=context.metadata,
        )

    def _update_stats(
        self,
        processed: int = 0,
        converted: int = 0,
        failed: int = 0,
        error: Optional[str] = None,
        warning: Optional[str] = None,
    ) -> None:
        """
        Update conversion statistics.

        Args:
            processed: Number of files processed
            converted: Number of files successfully converted
            failed: Number of files that failed conversion
            error: Error message to record
            warning: Warning message to record
        """
        self.conversion_stats["files_processed"] += processed
        self.conversion_stats["files_converted"] += converted
        self.conversion_stats["files_failed"] += failed

        if error:
            self.conversion_stats["errors"].append(error)
        if warning:
            self.conversion_stats["warnings"].append(warning)

    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename for cross-platform compatibility.

        Args:
            filename: Original filename

        Returns:
            Sanitized filename
        """
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

    def _get_file_extension(self, file_path: Path) -> str:
        """
        Get file extension in lowercase.

        Args:
            file_path: Path to file

        Returns:
            File extension in lowercase (without dot)
        """
        return file_path.suffix.lower().lstrip(".")

    def _ensure_directory_exists(self, directory: Path) -> bool:
        """
        Ensure directory exists, creating it if necessary.

        Args:
            directory: Directory path to ensure

        Returns:
            True if directory exists or was created, False on error
        """
        try:
            directory.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Failed to create directory {directory}: {e}")
            return False

    # Default implementations for optional interfaces
    def convert_batch(
        self, file_paths: list[Path], target_dir: Path
    ) -> ConversionReport:
        """
        Convert multiple files in a batch operation.
        Default implementation processes files sequentially.
        """
        self.logger.info(f"Processing batch of {len(file_paths)} files")

        report = ConversionReport(
            source_file="batch_operation",
            target_file=str(target_dir),
            conversion_type="batch",
            files_processed=0,
            files_converted=0,
            files_failed=0,
            errors=[],
            warnings=[],
            metadata={"file_count": len(file_paths)},
        )

        for file_path in file_paths:
            try:
                success = self.convert_file(file_path, target_dir / file_path.name)
                if success:
                    report.files_converted += 1
                else:
                    report.files_failed += 1
                report.files_processed += 1
            except Exception as e:
                report.errors.append(f"Failed to convert {file_path}: {e}")
                report.files_failed += 1
                report.files_processed += 1

        return report

    def validate_conversion(self, source_path: Path, target_path: Path) -> bool:
        """
        Validate conversion results.
        Default implementation checks file existence and basic integrity.
        """
        if not target_path.exists():
            self.logger.error(
                f"Validation failed: target file does not exist: {target_path}"
            )
            return False

        if target_path.stat().st_size == 0:
            self.logger.warning(
                f"Validation warning: target file is empty: {target_path}"
            )
            return False

        return True

    def configure(self, config: dict) -> None:
        """
        Configure converter with settings.
        Default implementation stores configuration.
        """
        self._config = config
        self.logger.info(f"Converter configured with {len(config)} settings")

    def get_configuration(self) -> dict:
        """
        Get current converter configuration.
        """
        return getattr(self, "_config", {})

    def set_progress_callback(self, callback) -> None:
        """
        Set progress reporting callback.
        """
        self._progress_callback = callback

    def get_progress(self) -> float:
        """
        Get current conversion progress (0.0 to 1.0).
        """
        return getattr(self, "_progress", 0.0)
