#!/usr/bin/env python3
"""
IFF Table Converter

Single Responsibility: IFF (Identification Friend or Foe) definitions parsing only.
"""

import re
from typing import Any, Dict, List, Optional

from .base_converter import BaseTableConverter, ParseState, TableType


class IFFTableConverter(BaseTableConverter):
    """Converts WCS iff_defs.tbl files to Godot IFF resources"""

    TABLE_TYPE = TableType.IFF
    FILENAME_PATTERNS = ["iff_defs.tbl", "IFF_defs.tbl"]
    CONTENT_PATTERNS = ["$IFF Name:", "$Traitor IFF:"]

    def _init_parse_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for IFF table parsing"""
        return {
            "iff_start": re.compile(r"^\$IFF Name:\s*(.+)$", re.IGNORECASE),
            "iff_color": re.compile(
                r"^\$Color:\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$", re.IGNORECASE
            ),
            "iff_attacks": re.compile(r"^\$Attacks:\s*\(([^)]+)\)$", re.IGNORECASE),
            "iff_sees_as": re.compile(
                r"^\+Sees (\w+) As:\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$",
                re.IGNORECASE,
            ),
            "iff_flags": re.compile(r"^\$Flags:\s*\(([^)]+)\)$", re.IGNORECASE),
            "iff_default_flags": re.compile(
                r"^\$Default Ship Flags:\s*\(([^)]+)\)$", re.IGNORECASE
            ),
            "iff_default_flags2": re.compile(
                r"^\$Default Ship Flags2:\s*\(([^)]+)\)$", re.IGNORECASE
            ),
            "traitor_iff": re.compile(r"^\$Traitor IFF:\s*(.+)$", re.IGNORECASE),
            "section_end": re.compile(r"^#End$", re.IGNORECASE),
        }

    def get_table_type(self) -> TableType:
        return TableType.IFF

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single IFF entry from the table"""
        iff_data = {
            "attacks": [],
            "flags": [],
            "default_ship_flags": [],
            "default_ship_flags2": [],
            "sees_as": {},
        }

        while state.has_more_lines():
            line = state.next_line()
            if not line:
                continue

            line = line.strip()
            if not line or self._should_skip_line(line, state):
                continue

            # Check for section end
            if self._parse_patterns["section_end"].match(line):
                break

            # Check for IFF start
            match = self._parse_patterns["iff_start"].match(line)
            if match:
                if "name" in iff_data:
                    # We've hit the next entry, so we're done with the current one
                    state.current_line -= 1
                    break
                iff_data["name"] = match.group(1).strip()
                continue

            # Parse IFF properties only if we have a name
            if "name" in iff_data:
                if self._parse_iff_property(line, iff_data):
                    continue

        return iff_data if iff_data and "name" in iff_data else None

    def _parse_iff_property(self, line: str, iff_data: Dict[str, Any]) -> bool:
        """Parse a single IFF property line"""
        for property_name, pattern in self._parse_patterns.items():
            if property_name in ["iff_start", "section_end"]:
                continue

            match = pattern.match(line)
            if match:
                # Handle different property types
                if property_name == "iff_color":
                    # Convert RGB values to list of integers
                    iff_data["color"] = [
                        int(match.group(1)),
                        int(match.group(2)),
                        int(match.group(3)),
                    ]
                elif property_name == "iff_attacks":
                    # Parse list of IFFs that this IFF attacks
                    attacks = [
                        a.strip().strip('"')
                        for a in match.group(1).split()
                        if a.strip()
                    ]
                    iff_data["attacks"] = attacks
                elif property_name == "iff_sees_as":
                    # Parse how this IFF sees other IFFs
                    target_iff = match.group(1).strip()
                    color = [
                        int(match.group(2)),
                        int(match.group(3)),
                        int(match.group(4)),
                    ]
                    iff_data["sees_as"][target_iff] = color
                elif property_name == "iff_flags":
                    # Parse IFF flags
                    flags = [
                        f.strip().strip('"')
                        for f in match.group(1).split()
                        if f.strip()
                    ]
                    iff_data["flags"] = flags
                elif property_name == "iff_default_flags":
                    # Parse default ship flags
                    flags = [
                        f.strip().strip('"')
                        for f in match.group(1).split()
                        if f.strip()
                    ]
                    iff_data["default_ship_flags"] = flags
                elif property_name == "iff_default_flags2":
                    # Parse default ship flags 2
                    flags = [
                        f.strip().strip('"')
                        for f in match.group(1).split()
                        if f.strip()
                    ]
                    iff_data["default_ship_flags2"] = flags
                elif property_name == "traitor_iff":
                    # Parse traitor IFF reference
                    iff_data["traitor_iff"] = match.group(1).strip()
                else:
                    # Handle simple string properties
                    iff_data[property_name] = match.group(1).strip()

                return True

        return False

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed IFF entry"""
        required_fields = ["name"]

        for field in required_fields:
            if field not in entry:
                self.logger.warning(f"IFF entry missing required field: {field}")
                return False

        # Validate color format if present
        if "color" in entry:
            color = entry["color"]
            if not isinstance(color, list) or len(color) != 3:
                self.logger.warning(f"IFF {entry['name']}: Invalid color format")
                return False
            for component in color:
                if not isinstance(component, int) or not (0 <= component <= 255):
                    self.logger.warning(
                        f"IFF {entry['name']}: Invalid color component {component}"
                    )
                    return False

        # Validate sees_as colors
        for target_iff, color in entry.get("sees_as", {}).items():
            if not isinstance(color, list) or len(color) != 3:
                self.logger.warning(
                    f"IFF {entry['name']}: Invalid sees_as color for {target_iff}"
                )
                return False
            for component in color:
                if not isinstance(component, int) or not (0 <= component <= 255):
                    self.logger.warning(
                        f"IFF {entry['name']}: Invalid sees_as color component {component} for {target_iff}"
                    )
                    return False

        return True

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed IFF entries to Godot resource format"""
        return {
            "resource_type": "WCSIFFDatabase",
            "iffs": {
                entry["name"]: self._convert_iff_entry(entry) for entry in entries
            },
            "iff_count": len(entries),
        }

    def _convert_iff_entry(self, iff: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single IFF entry to Godot format"""
        return {
            "display_name": iff.get("name", ""),
            "color": iff.get("color", [255, 255, 255]),
            "attacks": iff.get("attacks", []),
            "flags": iff.get("flags", []),
            "default_ship_flags": iff.get("default_ship_flags", []),
            "default_ship_flags2": iff.get("default_ship_flags2", []),
            "sees_as": iff.get("sees_as", {}),
            "traitor_iff": iff.get("traitor_iff", ""),
        }
