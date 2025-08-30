#!/usr/bin/env python3
"""
TBM Merger Utility

Handles the inheritance and override system for TBM (Table Behavior Modification) files.
Merges base TBL files with TBM modifications following proper precedence rules.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ..core.common_utils import ConversionUtils
from ..table_converters.base_converter import ParseState

logger = logging.getLogger(__name__)


class TBMMerger:
    """
    TBM Merger Utility for handling inheritance and override system.
    
    This class handles the merging of base TBL files with TBM modifications,
    ensuring proper precedence and conflict resolution.
    """

    def __init__(self):
        """Initialize the TBM merger."""
        self.merged_entries = {}
        self.conflicts = []

    def discover_tbm_files(self, source_dir: Path, base_filename: str) -> List[Path]:
        """
        Discover all TBM files associated with a base TBL file.
        
        Args:
            source_dir: Source directory to search in
            base_filename: Base filename without extension (e.g., 'ships')
            
        Returns:
            List of TBM file paths in order of application
        """
        tbm_files = []
        
        # Look for TBM files with the same base name
        # TBM files are typically named as base_name-*.tbm or base_name_*.tbm
        patterns = [
            f"{base_filename}*.tbm",
            f"{base_filename.upper()}*.tbm",
            f"{base_filename.lower()}*.tbm"
        ]
        
        for pattern in patterns:
            tbm_files.extend(source_dir.rglob(pattern))
        
        # Sort by modification time to ensure proper application order
        tbm_files.sort(key=lambda x: x.stat().st_mtime)
        
        logger.info(f"Discovered {len(tbm_files)} TBM files for {base_filename}")
        return tbm_files

    def merge_tbl_with_tbm(self, tbl_path: Path, source_dir: Path) -> List[Dict[str, Any]]:
        """
        Merge a base TBL file with all associated TBM files.
        
        Args:
            tbl_path: Path to the base TBL file
            source_dir: Source directory containing TBM files
            
        Returns:
            List of merged entries with TBM modifications applied
        """
        # Load base TBL file
        tbl_entries = self._load_table_entries(tbl_path)
        
        # Discover associated TBM files
        base_name = tbl_path.stem
        tbm_files = self.discover_tbm_files(source_dir, base_name)
        
        # Apply TBM modifications in order
        merged_entries = tbl_entries.copy()
        for tbm_file in tbm_files:
            logger.info(f"Merging TBM file: {tbm_file}")
            merged_entries = self._apply_tbm_modifications(merged_entries, tbm_file)
        
        return merged_entries

    def _load_table_entries(self, table_file: Path) -> List[Dict[str, Any]]:
        """
        Load entries from a table file.
        
        Args:
            table_file: Path to the table file
            
        Returns:
            List of parsed entries
        """
        try:
            lines = ConversionUtils.load_table_file(table_file)
            if lines is None:
                return []
            
            # Create a temporary parse state
            state = ParseState(lines=lines, filename=str(table_file))
            
            # For now, we'll return the raw lines as we don't have access to specific converters
            # In practice, this would use the appropriate converter for the table type
            return [{"raw_lines": lines, "source_file": str(table_file)}]
        except Exception as e:
            logger.error(f"Failed to load table file {table_file}: {e}")
            return []

    def _apply_tbm_modifications(self, base_entries: List[Dict[str, Any]], tbm_file: Path) -> List[Dict[str, Any]]:
        """
        Apply TBM modifications to base entries.
        
        Args:
            base_entries: List of base entries
            tbm_file: Path to the TBM file
            
        Returns:
            List of entries with TBM modifications applied
        """
        try:
            # Load TBM file
            tbm_lines = ConversionUtils.load_table_file(tbm_file)
            if tbm_lines is None:
                return base_entries
            
            # Parse TBM modifications
            tbm_modifications = self._parse_tbm_modifications(tbm_lines)
            
            # Apply modifications to base entries
            merged_entries = self._merge_entries_with_modifications(base_entries, tbm_modifications, tbm_file.name)
            
            return merged_entries
        except Exception as e:
            logger.error(f"Failed to apply TBM modifications from {tbm_file}: {e}")
            return base_entries

    def _parse_tbm_modifications(self, tbm_lines: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Parse TBM modifications from lines.
        
        Args:
            tbm_lines: List of lines from TBM file
            
        Returns:
            Dictionary of modifications keyed by entry name
        """
        modifications = {}
        current_entry = None
        current_entry_name = None
        
        for line in tbm_lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for entry start (e.g., $Name:)
            if line.startswith("$Name:"):
                # Extract entry name
                entry_name = line.split(":", 1)[1].strip()
                if entry_name.startswith('"') and entry_name.endswith('"'):
                    entry_name = entry_name[1:-1]
                
                current_entry_name = entry_name
                if current_entry_name not in modifications:
                    modifications[current_entry_name] = {}
                current_entry = modifications[current_entry_name]
                continue
                
            # If we're in an entry, collect property modifications
            if current_entry is not None:
                # Handle property lines
                if line.startswith("$"):
                    # Extract property name and value
                    if ":" in line:
                        prop_name, prop_value = line.split(":", 1)
                        prop_name = prop_name.strip().lower()
                        prop_value = prop_value.strip()
                        
                        # Store the modification
                        current_entry[prop_name] = prop_value
                        
        return modifications

    def _merge_entries_with_modifications(
        self, 
        base_entries: List[Dict[str, Any]], 
        tbm_modifications: Dict[str, Dict[str, Any]], 
        tbm_filename: str
    ) -> List[Dict[str, Any]]:
        """
        Merge base entries with TBM modifications.
        
        Args:
            base_entries: List of base entries
            tbm_modifications: Dictionary of TBM modifications
            tbm_filename: Name of the TBM file (for conflict tracking)
            
        Returns:
            List of merged entries
        """
        merged_entries = []
        
        # For each base entry, check if there are TBM modifications
        for entry in base_entries:
            # For this implementation, we'll assume entries have a 'name' field
            # In practice, this would depend on the specific table type
            entry_name = entry.get("name", "")
            
            if entry_name in tbm_modifications:
                # Apply modifications
                modifications = tbm_modifications[entry_name]
                merged_entry = self._apply_modifications_to_entry(entry, modifications, tbm_filename)
                merged_entries.append(merged_entry)
                
                # Remove this entry from modifications as it's been applied
                del tbm_modifications[entry_name]
            else:
                # No modifications, keep original entry
                merged_entries.append(entry.copy())
        
        # Handle any new entries that are only in TBM files
        for entry_name, modifications in tbm_modifications.items():
            new_entry = {"name": entry_name}
            # Apply all modifications as this is a new entry
            merged_entry = self._apply_modifications_to_entry(new_entry, modifications, tbm_filename)
            merged_entries.append(merged_entry)
        
        return merged_entries

    def _apply_modifications_to_entry(
        self, 
        entry: Dict[str, Any], 
        modifications: Dict[str, Any], 
        tbm_filename: str
    ) -> Dict[str, Any]:
        """
        Apply modifications to a single entry.
        
        Args:
            entry: Base entry
            modifications: Dictionary of modifications to apply
            tbm_filename: Name of the TBM file (for conflict tracking)
            
        Returns:
            Entry with modifications applied
        """
        merged_entry = entry.copy()
        
        for prop_name, prop_value in modifications.items():
            # Check for conflicts
            if prop_name in entry and entry[prop_name] != prop_value:
                conflict = {
                    "entry_name": entry.get("name", "unknown"),
                    "property": prop_name,
                    "original_value": entry[prop_name],
                    "modified_value": prop_value,
                    "source_tbm": tbm_filename
                }
                self.conflicts.append(conflict)
                logger.warning(f"Property conflict in {entry.get('name', 'unknown')}.{prop_name}: "
                              f"{entry[prop_name]} -> {prop_value} (from {tbm_filename})")
            
            # Apply the modification (override)
            merged_entry[prop_name] = prop_value
            
        return merged_entry

    def get_conflicts(self) -> List[Dict[str, Any]]:
        """
        Get list of conflicts encountered during merging.
        
        Returns:
            List of conflict dictionaries
        """
        return self.conflicts.copy()

    def resolve_conflicts(self, resolution_strategy: str = "tbm_wins") -> None:
        """
        Resolve conflicts based on the specified strategy.
        
        Args:
            resolution_strategy: Strategy for conflict resolution
                - "tbm_wins": TBM modifications override base values (default)
                - "base_wins": Base values override TBM modifications
                - "warn_only": Only warn about conflicts, don't resolve
        """
        # For now, our implementation already uses "tbm_wins" as that's how TBM files work
        # This method is provided for future expansion
        if resolution_strategy == "warn_only":
            # Just log conflicts without changing behavior
            for conflict in self.conflicts:
                logger.info(f"Conflict noted: {conflict}")
        # Other strategies could be implemented here