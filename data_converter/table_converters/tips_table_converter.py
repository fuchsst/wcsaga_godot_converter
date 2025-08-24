#!/usr/bin/env python3
"""
Tips Table Converter

Single Responsibility: Tips definitions parsing and conversion only.
Handles tips.tbl files for in-game tips display.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base_converter import BaseTableConverter, ParseState, TableType


class TipsTableConverter(BaseTableConverter):
    """Converts WCS tips.tbl files to Godot tips resources"""

    FILENAME_PATTERNS = ["tips.tbl"]
    CONTENT_PATTERNS = ["+Tip:", "XSTR("]

    def _init_parse_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for tips.tbl parsing"""
        return {
            "tip_start": re.compile(r"^\+Tip:\s*XSTR\(\"(.+)\",\s*-1\)$", re.IGNORECASE),
            "tip_continuation": re.compile(r'^\s*XSTR\("(.+)",\s*-1\)\s*', re.IGNORECASE)
        }

    def get_table_type(self) -> TableType:
        return TableType.TIPS

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire tips.tbl file."""
        entries = []
        
        while state.has_more_lines():
            line = state.peek_line()
            if not line:
                state.skip_line()
                continue
                
            line = line.strip()
            
            # Skip comments
            if self._parse_patterns["comment"].match(line):
                state.skip_line()
                continue
                
            # Look for tip start markers
            if line.startswith("+Tip:"):
                entry = self.parse_entry(state)
                if entry:
                    entries.append(entry)
            else:
                state.skip_line()
                
        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single tip entry."""
        entry_data = {
            "tip_text": ""
        }
        
        # Get the first line with the tip
        first_line = state.next_line()
        if not first_line:
            return None
            
        first_line = first_line.strip()
        
        # Extract tip text from XSTR
        match = self._parse_patterns["tip_start"].match(first_line)
        if match:
            entry_data["tip_text"] = match.group(1).strip()
        else:
            return None
            
        # Continue parsing if there are continuation lines
        while state.has_more_lines():
            line = state.peek_line()
            if not line:
                break
                
            line = line.strip()
            
            # Stop if we hit another tip, section end, or comment
            if (line.startswith("+Tip:") or 
                self._parse_patterns["section_end"].match(line) or
                self._parse_patterns["comment"].match(line)):
                break
                
            # Check for continuation XSTR lines
            match = self._parse_patterns["tip_continuation"].match(line)
            if match:
                # Consume the line
                state.skip_line()
                entry_data["tip_text"] += " " + match.group(1).strip()
            else:
                # Not a continuation line, so we're done with this tip
                break
                
        return self.validate_entry(entry_data) and entry_data or None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed tip entry."""
        return "tip_text" in entry and len(entry["tip_text"]) > 0

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed tip entries to a Godot resource dictionary."""
        return {
            "resource_type": "WCSTipsDatabase",
            "tips": [self._convert_tip_entry(entry) for entry in entries],
            "tip_count": len(entries),
        }

    def _convert_tip_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single tip entry to the target Godot format."""
        return {
            "tip_text": entry.get("tip_text", ""),
            "section_end": re.compile(r"^#end$", re.IGNORECASE),
            "comment": re.compile(r"^;"),
        }

    def get_table_type(self) -> TableType:
        return TableType.TIPS

    def get_table_type(self) -> TableType:
        return TableType.TIPS

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire tips.tbl file."""
        entries = []
        
        while state.has_more_lines():
            line = state.peek_line()
            if not line:
                state.skip_line()
                continue
                
            line = line.strip()
            
            # Skip comments
            if self._parse_patterns["comment"].match(line):
                state.skip_line()
                continue
                
            # Look for tip start markers
            if line.startswith("+Tip:"):
                entry = self.parse_entry(state)
                if entry:
                    entries.append(entry)
            else:
                state.skip_line()
                
        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single tip entry."""
        entry_data = {
            "tip_text": ""
        }
        
        # Get the first line with the tip
        first_line = state.next_line()
        if not first_line:
            return None
            
        first_line = first_line.strip()
        
        # Extract tip text from XSTR
        match = self._parse_patterns["tip_start"].match(first_line)
        if match:
            entry_data["tip_text"] = match.group(1).strip()
        else:
            return None
            
        # Continue parsing if there are continuation lines
        while state.has_more_lines():
            line = state.peek_line()
            if not line:
                break
                
            line = line.strip()
            
            # Stop if we hit another tip, section end, or comment
            if (line.startswith("+Tip:") or 
                self._parse_patterns["section_end"].match(line) or
                self._parse_patterns["comment"].match(line)):
                break
                
            # Check for continuation XSTR lines
            match = self._parse_patterns["tip_continuation"].match(line)
            if match:
                # Consume the line
                state.skip_line()
                entry_data["tip_text"] += " " + match.group(1).strip()
            else:
                # Not a continuation line, so we're done with this tip
                break
                
        return self.validate_entry(entry_data) and entry_data or None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed tip entry."""
        return "tip_text" in entry and len(entry["tip_text"]) > 0

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed tip entries to a Godot resource dictionary."""
        return {
            "resource_type": "WCSTipsDatabase",
            "tips": [self._convert_tip_entry(entry) for entry in entries],
            "tip_count": len(entries),
        }

    def _convert_tip_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single tip entry to the target Godot format."""
        return {
            "tip_text": entry.get("tip_text", ""),
        }