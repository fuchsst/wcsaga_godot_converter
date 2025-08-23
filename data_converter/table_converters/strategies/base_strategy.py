#!/usr/bin/env python3
"""
Base Table Strategy - Strategy Pattern Implementation

Abstract base class for all table conversion strategies following
Strategy Pattern to eliminate code duplication.

Author: Dev (GDScript Developer)
Date: June 15, 2025
Story: DM-009 - SOLID Principle Refactoring
Epic: EPIC-003 - Data Migration & Conversion Tools
"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ....core.interfaces import IFileConverter


class BaseTableStrategy(ABC, IFileConverter):
    """
    Abstract base strategy for table conversion operations.
    
    Implements the Strategy Pattern to extract common functionality
    from the 22 table converter classes.
    """
    
    def __init__(self, source_dir: Path, target_dir: Path):
        """
        Initialize table conversion strategy.
        
        Args:
            source_dir: Source directory containing table files
            target_dir: Target directory for converted output
        """
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.conversion_stats: Dict[str, Any] = {
            'files_processed': 0,
            'files_converted': 0,
            'files_failed': 0,
            'errors': [],
            'warnings': []
        }
    
    @abstractmethod
    def can_convert(self, file_path: Path) -> bool:
        """Check if this strategy can handle the given file."""
        pass
    
    @abstractmethod
    def convert_file(self, file_path: Path, target_path: Optional[Path] = None) -> bool:
        """Convert a single file using this strategy."""
        pass
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of file extensions this strategy supports."""
        return ['.tbl', '.tbm']
    
    def get_table_type_patterns(self) -> List[str]:
        """Get filename patterns that indicate this table type."""
        return []
    
    def get_content_patterns(self) -> List[str]:
        """Get content patterns that indicate this table type."""
        return []
    
    # ========== COMMON UTILITY METHODS ==========
    
    def _extract_string_value(self, line: str) -> str:
        """Extract string value from table line."""
        from ....core.common_utils import ConversionUtils
        return ConversionUtils.extract_string_value(line)
    
    def _extract_int_value(self, line: str) -> int:
        """Extract integer value from table line."""
        from ....core.common_utils import ConversionUtils
        return ConversionUtils.extract_int_value(line)
    
    def _extract_float_value(self, line: str) -> float:
        """Extract float value from table line."""
        from ....core.common_utils import ConversionUtils
        return ConversionUtils.extract_float_value(line)
    
    def _extract_bool_value(self, line: str) -> bool:
        """Extract boolean value from table line."""
        from ....core.common_utils import ConversionUtils
        return ConversionUtils.extract_bool_value(line)
    
    def _extract_vector3(self, line: str) -> Tuple[float, float, float]:
        """Extract Vector3 values from table line."""
        from ....core.common_utils import ConversionUtils
        return ConversionUtils.extract_vector3(line)
    
    def _extract_string_list(self, line: str) -> List[str]:
        """Extract list of strings from table line."""
        from ....core.common_utils import ConversionUtils
        return ConversionUtils.extract_string_list(line)
    
    def _extract_int_list(self, line: str) -> List[int]:
        """Extract list of integers from table line."""
        from ....core.common_utils import ConversionUtils
        return ConversionUtils.extract_int_list(line)
    
    def _preprocess_lines(self, raw_lines: List[str]) -> List[str]:
        """Preprocess table lines (comments, continuations, etc.)."""
        from ....core.common_utils import ConversionUtils
        return ConversionUtils.preprocess_lines(raw_lines)
    
    def _load_table_file(self, table_file: Path) -> Optional[List[str]]:
        """Load and preprocess table file content."""
        from ....core.common_utils import ConversionUtils
        return ConversionUtils.load_table_file(table_file)
    
    def _determine_table_type(self, table_file: Path, content: Optional[List[str]] = None) -> bool:
        """
        Determine if the given file matches this strategy's table type using centralized detection.
        
        Args:
            table_file: Path to the table file
            content: Optional pre-loaded content for efficiency
            
        Returns:
            True if file matches this strategy's table type
        """
        from ....core.common_utils import TableTypeDetector
        
        # Use centralized detection for the main logic
        detected_type = TableTypeDetector.determine_table_type(table_file)
        
        # Check if the detected type matches this strategy's patterns
        filename_patterns = self.get_table_type_patterns()
        
        # Convert strategy patterns to expected type string
        expected_type = None
        if filename_patterns:
            # Extract expected type from first pattern (e.g., ['ship'] -> 'ships')
            first_pattern = filename_patterns[0]
            if 'ship' in first_pattern:
                expected_type = 'ships'
            elif 'weapon' in first_pattern:
                expected_type = 'weapons'
            elif 'armor' in first_pattern:
                expected_type = 'armor'
            elif 'species' in first_pattern:
                expected_type = 'species_defs'
            elif 'iff' in first_pattern:
                expected_type = 'iff_defs'
        
        return detected_type == expected_type if expected_type else False
    
    def _update_stats(self, processed: int = 0, converted: int = 0, 
                     failed: int = 0, error: Optional[str] = None, 
                     warning: Optional[str] = None) -> None:
        """Update conversion statistics."""
        self.conversion_stats['files_processed'] += processed
        self.conversion_stats['files_converted'] += converted
        self.conversion_stats['files_failed'] += failed
        
        if error:
            self.conversion_stats['errors'].append(error)
        if warning:
            self.conversion_stats['warnings'].append(warning)