#!/usr/bin/env python3
"""
Credits Table Converter

Single Responsibility: Credits definitions parsing and conversion only.
Handles credits.tbl files for game credits display.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from .base_converter import BaseTableConverter, ParseState, TableType


class CreditsTableConverter(BaseTableConverter):
    """Converts WCS credits.tbl files to Godot credits resources"""

    FILENAME_PATTERNS = ["credits.tbl"]
    CONTENT_PATTERNS = ["XSTR(", "#end"]

    def _init_parse_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for credits.tbl parsing"""
        return {
            "xstr": re.compile(r'^XSTR\("(.+)",\s*-1\)', re.IGNORECASE)
        }

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire credits.tbl file."""
        entries = []
        
        # Parse all XSTR entries as credit lines
        credit_lines = []
        
        while state.has_more_lines():
            line = state.next_line()
            if not line:
                continue
                
            line = line.strip()
            
            # Skip empty lines and comments
            if self._should_skip_line(line, state):
                continue
                
            # Stop at #end marker
            if self._parse_patterns["section_end"].match(line):
                break
            
            # Extract XSTR entries
            match = self._parse_patterns["xstr"].match(line)
            if match:
                credit_lines.append(match.group(1).strip())
                
        if credit_lines:
            entries.append({
                "credit_lines": credit_lines
            })
            
        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single credits entry."""
        # For credits, we treat the entire file as one entry
        return None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed credits entry."""
        return "credit_lines" in entry and len(entry["credit_lines"]) > 0

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed credits entries to a Godot resource dictionary."""
        # For credits, we expect only one entry with all the credit lines
        if not entries:
            return {
                "resource_type": "WCSCreditsDatabase",
                "credit_lines": [],
                "line_count": 0,
            }
            
        credit_entry = entries[0]
        return {
            "resource_type": "WCSCreditsDatabase",
            "credit_lines": credit_entry.get("credit_lines", []),
            "line_count": len(credit_entry.get("credit_lines", [])),
            "section_end": re.compile(r"^#end$", re.IGNORECASE),
            "empty_line": re.compile(r"^\s*$"),
        }

    def get_table_type(self) -> TableType:
        return TableType.CREDITS

    def get_table_type(self) -> TableType:
        return TableType.CREDITS

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire credits.tbl file."""
        entries = []
        
        # Parse all XSTR entries as credit lines
        credit_lines = []
        
        while state.has_more_lines():
            line = state.next_line()
            if not line:
                continue
                
            line = line.strip()
            
            # Skip empty lines and comments
            if self._should_skip_line(line, state):
                continue
                
            # Stop at #end marker
            if self._parse_patterns["section_end"].match(line):
                break
            
            # Extract XSTR entries
            match = self._parse_patterns["xstr"].match(line)
            if match:
                credit_lines.append(match.group(1).strip())
                
        if credit_lines:
            entries.append({
                "credit_lines": credit_lines
            })
            
        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single credits entry."""
        # For credits, we treat the entire file as one entry
        return None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed credits entry."""
        return "credit_lines" in entry and len(entry["credit_lines"]) > 0

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed credits entries to a Godot resource dictionary."""
        # For credits, we expect only one entry with all the credit lines
        if not entries:
            return {
                "resource_type": "WCSCreditsDatabase",
                "credit_lines": [],
                "line_count": 0,
            }
            
        credit_entry = entries[0]
        return {
            "resource_type": "WCSCreditsDatabase",
            "credit_lines": credit_entry.get("credit_lines", []),
            "line_count": len(credit_entry.get("credit_lines", [])),
            "section_end": re.compile(r"^#end$", re.IGNORECASE),
            "empty_line": re.compile(r"^\s*$"),
        }

    def get_table_type(self) -> TableType:
        return TableType.CREDITS

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire credits.tbl file."""
        entries = []
        
        # Parse all XSTR entries as credit lines
        credit_lines = []
        
        while state.has_more_lines():
            line = state.next_line()
            if not line:
                continue
                
            line = line.strip()
            
            # Skip empty lines and comments
            if self._should_skip_line(line, state):
                continue
                
            # Stop at #end marker
            if self._parse_patterns["section_end"].match(line):
                break
            
            # Extract XSTR entries
            match = self._parse_patterns["xstr"].match(line)
            if match:
                credit_lines.append(match.group(1).strip())
                
        if credit_lines:
            entries.append({
                "credit_lines": credit_lines
            })
            
        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single credits entry."""
        # For credits, we treat the entire file as one entry
        return None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed credits entry."""
        return "credit_lines" in entry and len(entry["credit_lines"]) > 0

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed credits entries to a Godot resource dictionary."""
        # For credits, we expect only one entry with all the credit lines
        if not entries:
            return {
                "resource_type": "WCSCreditsDatabase",
                "credit_lines": [],
                "line_count": 0,
            }
            
        credit_entry = entries[0]
        return {
            "resource_type": "WCSCreditsDatabase",
            "credit_lines": credit_entry.get("credit_lines", []),
            "line_count": len(credit_entry.get("credit_lines", [])),
            "section_end": re.compile(r"^#end$", re.IGNORECASE),
            "empty_line": re.compile(r"^\s*$"),
        }

    def get_table_type(self) -> TableType:
        return TableType.CREDITS

    def get_table_type(self) -> TableType:
        return TableType.CREDITS

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire credits.tbl file."""
        entries = []
        
        # Parse all XSTR entries as credit lines
        credit_lines = []
        
        while state.has_more_lines():
            line = state.next_line()
            if not line:
                continue
                
            line = line.strip()
            
            # Skip empty lines and comments
            if self._should_skip_line(line, state):
                continue
                
            # Stop at #end marker
            if self._parse_patterns["section_end"].match(line):
                break
            
            # Extract XSTR entries
            match = self._parse_patterns["xstr"].match(line)
            if match:
                credit_lines.append(match.group(1).strip())
                
        if credit_lines:
            entries.append({
                "credit_lines": credit_lines
            })
            
        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single credits entry."""
        # For credits, we treat the entire file as one entry
        return None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed credits entry."""
        return "credit_lines" in entry and len(entry["credit_lines"]) > 0

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed credits entries to a Godot resource dictionary."""
        # For credits, we expect only one entry with all the credit lines
        if not entries:
            return {
                "resource_type": "WCSCreditsDatabase",
                "credit_lines": [],
                "line_count": 0,
            }
            
        credit_entry = entries[0]
        return {
            "resource_type": "WCSCreditsDatabase",
            "credit_lines": credit_entry.get("credit_lines", []),
            "line_count": len(credit_entry.get("credit_lines", [])),
            "section_end": re.compile(r"^#end$", re.IGNORECASE),
            "empty_line": re.compile(r"^\s*$"),
        }

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire credits.tbl file."""
        entries = []
        
        # Parse all XSTR entries as credit lines
        credit_lines = []
        
        while state.has_more_lines():
            line = state.next_line()
            if not line:
                continue
                
            line = line.strip()
            
            # Skip empty lines and comments
            if self._should_skip_line(line, state):
                continue
                
            # Stop at #end marker
            if self._parse_patterns["section_end"].match(line):
                break
            
            # Extract XSTR entries
            match = self._parse_patterns["xstr"].match(line)
            if match:
                credit_lines.append(match.group(1).strip())
                
        if credit_lines:
            entries.append({
                "credit_lines": credit_lines
            })
            
        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single credits entry."""
        # For credits, we treat the entire file as one entry
        return None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed credits entry."""
        return "credit_lines" in entry and len(entry["credit_lines"]) > 0

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed credits entries to a Godot resource dictionary."""
        # For credits, we expect only one entry with all the credit lines
        if not entries:
            return {
                "resource_type": "WCSCreditsDatabase",
                "credit_lines": [],
                "line_count": 0,
            }
            
        credit_entry = entries[0]
        return {
            "resource_type": "WCSCreditsDatabase",
            "credit_lines": credit_entry.get("credit_lines", []),
            "line_count": len(credit_entry.get("credit_lines", [])),
            "section_end": re.compile(r"^#end$", re.IGNORECASE),
            "empty_line": re.compile(r"^\s*$"),
        }

    def get_table_type(self) -> TableType:
        return TableType.CREDITS

    def get_table_type(self) -> TableType:
        return TableType.CREDITS

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire credits.tbl file."""
        entries = []
        
        # Parse all XSTR entries as credit lines
        credit_lines = []
        
        while state.has_more_lines():
            line = state.next_line()
            if not line:
                continue
                
            line = line.strip()
            
            # Skip empty lines and comments
            if self._should_skip_line(line, state):
                continue
                
            # Stop at #end marker
            if self._parse_patterns["section_end"].match(line):
                break
            
            # Extract XSTR entries
            match = self._parse_patterns["xstr"].match(line)
            if match:
                credit_lines.append(match.group(1).strip())
                
        if credit_lines:
            entries.append({
                "credit_lines": credit_lines
            })
            
        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single credits entry."""
        # For credits, we treat the entire file as one entry
        return None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed credits entry."""
        return "credit_lines" in entry and len(entry["credit_lines"]) > 0

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed credits entries to a Godot resource dictionary."""
        # For credits, we expect only one entry with all the credit lines
        if not entries:
            return {
                "resource_type": "WCSCreditsDatabase",
                "credit_lines": [],
                "line_count": 0,
            }
            
        credit_entry = entries[0]
        return {
            "resource_type": "WCSCreditsDatabase",
            "credit_lines": credit_entry.get("credit_lines", []),
            "line_count": len(credit_entry.get("credit_lines", [])),
            "section_end": re.compile(r"^#end$", re.IGNORECASE),
            "empty_line": re.compile(r"^\s*$"),
        }

    def get_table_type(self) -> TableType:
        return TableType.CREDITS

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire credits.tbl file."""
        entries = []
        
        # Parse all XSTR entries as credit lines
        credit_lines = []
        
        while state.has_more_lines():
            line = state.next_line()
            if not line:
                continue
                
            line = line.strip()
            
            # Skip empty lines and comments
            if self._should_skip_line(line, state):
                continue
                
            # Stop at #end marker
            if self._parse_patterns["section_end"].match(line):
                break
            
            # Extract XSTR entries
            match = self._parse_patterns["xstr"].match(line)
            if match:
                credit_lines.append(match.group(1).strip())
                
        if credit_lines:
            entries.append({
                "credit_lines": credit_lines
            })
            
        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single credits entry."""
        # For credits, we treat the entire file as one entry
        return None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed credits entry."""
        return "credit_lines" in entry and len(entry["credit_lines"]) > 0

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed credits entries to a Godot resource dictionary."""
        # For credits, we expect only one entry with all the credit lines
        if not entries:
            return {
                "resource_type": "WCSCreditsDatabase",
                "credit_lines": [],
                "line_count": 0,
            }
            
        credit_entry = entries[0]
        return {
            "resource_type": "WCSCreditsDatabase",
            "credit_lines": credit_entry.get("credit_lines", []),
            "line_count": len(credit_entry.get("credit_lines", [])),
            "section_end": re.compile(r"^#end$", re.IGNORECASE),
            "empty_line": re.compile(r"^\s*$"),
        }

    def get_table_type(self) -> TableType:
        return TableType.CREDITS

    def get_table_type(self) -> TableType:
        return TableType.CREDITS

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire credits.tbl file."""
        entries = []
        
        # Parse all XSTR entries as credit lines
        credit_lines = []
        
        while state.has_more_lines():
            line = state.next_line()
            if not line:
                continue
                
            line = line.strip()
            
            # Skip empty lines and comments
            if self._should_skip_line(line, state):
                continue
                
            # Stop at #end marker
            if self._parse_patterns["section_end"].match(line):
                break
            
            # Extract XSTR entries
            match = self._parse_patterns["xstr"].match(line)
            if match:
                credit_lines.append(match.group(1).strip())
                
        if credit_lines:
            entries.append({
                "credit_lines": credit_lines
            })
            
        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single credits entry."""
        # For credits, we treat the entire file as one entry
        return None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed credits entry."""
        return "credit_lines" in entry and len(entry["credit_lines"]) > 0

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed credits entries to a Godot resource dictionary."""
        # For credits, we expect only one entry with all the credit lines
        if not entries:
            return {
                "resource_type": "WCSCreditsDatabase",
                "credit_lines": [],
                "line_count": 0,
            }
            
        credit_entry = entries[0]
        return {
            "resource_type": "WCSCreditsDatabase",
            "credit_lines": credit_entry.get("credit_lines", []),
            "line_count": len(credit_entry.get("credit_lines", [])),
        }