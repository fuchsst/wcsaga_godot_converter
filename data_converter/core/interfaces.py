#!/usr/bin/env python3
"""
Converter Interfaces - EPIC-003 SOLID Refactoring

Specialized interfaces following Interface Segregation Principle (ISP)
to replace the monolithic BaseDataConverter interface.

Author: Dev (GDScript Developer)
Date: June 15, 2025
Story: DM-009 - SOLID Principle Refactoring
Epic: EPIC-003 - Data Migration & Conversion Tools
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from .data_structures import ConversionReport


class IFileConverter(ABC):
    """Interface for converters that operate on single files."""

    @abstractmethod
    def can_convert(self, file_path: Path) -> bool:
        """Check if this converter can handle the given file."""
        pass

    @abstractmethod
    def convert_file(self, file_path: Path, target_path: Optional[Path] = None) -> bool:
        """Convert a single file."""
        pass


class IDirectoryConverter(ABC):
    """Interface for converters that operate on directories."""

    @abstractmethod
    def convert_directory(
        self, source_dir: Path, target_dir: Path, pattern: str = "*"
    ) -> ConversionReport:
        """Convert all matching files in directory."""
        pass


class IBatchConverter(ABC):
    """Interface for converters that support batch operations."""

    @abstractmethod
    def convert_batch(
        self, file_paths: list[Path], target_dir: Path
    ) -> ConversionReport:
        """Convert multiple files in a batch operation."""
        pass


class IValidatableConverter(ABC):
    """Interface for converters that support validation."""

    @abstractmethod
    def validate_conversion(self, source_path: Path, target_path: Path) -> bool:
        """Validate conversion results."""
        pass


class IConfigurableConverter(ABC):
    """Interface for converters that support configuration."""

    @abstractmethod
    def configure(self, config: dict) -> None:
        """Configure converter with settings."""
        pass

    @abstractmethod
    def get_configuration(self) -> dict:
        """Get current converter configuration."""
        pass


class IProgressReporter(ABC):
    """Interface for converters that report progress."""

    @abstractmethod
    def set_progress_callback(self, callback) -> None:
        """Set progress reporting callback."""
        pass

    @abstractmethod
    def get_progress(self) -> float:
        """Get current conversion progress (0.0 to 1.0)."""
        pass
