#!/usr/bin/env python3
"""
Help Table Converter

Single Responsibility: Help overlay definitions parsing and conversion only.
Handles help.tbl files for in-game help system.
"""

import re
from typing import Any, Dict, List, Optional

from .base_converter import BaseTableConverter, ParseState, TableType


class HelpTableConverter(BaseTableConverter):
    """Converts WCS help.tbl files to Godot help overlay resources"""

    FILENAME_PATTERNS = ["help.tbl"]
    CONTENT_PATTERNS = ["$ship", "$weapon", "$briefing"]

    def _init_parse_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for help.tbl parsing"""
        return {
            "overlay_start": re.compile(r"^\$(\w+)$", re.IGNORECASE),
            "overlay_end": re.compile(r"^\$end$", re.IGNORECASE),
            "comment": re.compile(r"^;|^//"),
            "text": re.compile(
                r'^\+text\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+XSTR\("(.+)",\s*-1\)',
                re.IGNORECASE,
            ),
            "line": re.compile(r"^\+pline\s+(\d+)\s+(.+)", re.IGNORECASE),
            "right_bracket": re.compile(
                r"^\+right_bracket\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", re.IGNORECASE
            ),
            "left_bracket": re.compile(
                r"^\+left_bracket\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", re.IGNORECASE
            ),
        }

    def get_table_type(self) -> TableType:
        return TableType.HELP

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire help.tbl file."""
        entries = []

        while state.has_more_lines():
            line = state.peek_line()
            if not line:
                state.skip_line()
                continue

            line = line.strip()

            # Skip comments
            if self._should_skip_line(line, state):
                state.skip_line()
                continue

            # Look for overlay start markers
            match = self._parse_patterns["overlay_start"].match(line)
            if match:
                entry = self.parse_entry(state)
                if entry:
                    entries.append(entry)
            else:
                state.skip_line()

        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single help overlay entry."""
        entry_data = {
            "texts": [],
            "lines": [],
            "right_brackets": [],
            "left_brackets": [],
        }

        # Get the overlay name from the first line
        first_line = state.next_line()
        if first_line:
            match = self._parse_patterns["overlay_start"].match(first_line.strip())
            if match:
                entry_data["name"] = match.group(1).strip().lower()

        # Parse overlay elements
        while state.has_more_lines():
            line = state.next_line()
            if not line:
                continue

            line = line.strip()

            # Skip comments
            if self._parse_patterns["comment"].match(line):
                continue

            # Check for overlay end
            if self._parse_patterns["overlay_end"].match(line):
                break

            # Check for next overlay start
            if self._parse_patterns["overlay_start"].match(line):
                # Put line back for next entry
                state.current_line -= 1
                break

            # Parse text elements
            match = self._parse_patterns["text"].match(line)
            if match:
                entry_data["texts"].append(
                    {
                        "x": int(match.group(1)),
                        "y": int(match.group(2)),
                        "x1024": int(match.group(3)),
                        "y1024": int(match.group(4)),
                        "string": match.group(5).strip(),
                    }
                )
                continue

            # Parse line elements
            match = self._parse_patterns["line"].match(line)
            if match:
                point_count = int(match.group(1))
                points_str = match.group(2).strip()
                # Parse points: pairs of numbers separated by spaces
                points = []
                coords = points_str.split()
                for i in range(0, len(coords), 2):
                    if i + 1 < len(coords):
                        try:
                            points.append((int(coords[i]), int(coords[i + 1])))
                        except ValueError:
                            continue
                entry_data["lines"].append(
                    {"point_count": point_count, "points": points}
                )
                continue

            # Parse right brackets
            match = self._parse_patterns["right_bracket"].match(line)
            if match:
                entry_data["right_brackets"].append(
                    {
                        "x1": int(match.group(1)),
                        "y1": int(match.group(2)),
                        "x2": int(match.group(3)),
                        "y2": int(match.group(4)),
                    }
                )
                continue

            # Parse left brackets
            match = self._parse_patterns["left_bracket"].match(line)
            if match:
                entry_data["left_brackets"].append(
                    {
                        "x1": int(match.group(1)),
                        "y1": int(match.group(2)),
                        "x2": int(match.group(3)),
                        "y2": int(match.group(4)),
                    }
                )
                continue

        return self.validate_entry(entry_data) and entry_data or None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed help overlay entry."""
        return "name" in entry

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed help overlay entries to a Godot resource dictionary."""
        return {
            "resource_type": "WCSHelpOverlayDatabase",
            "overlays": {
                entry["name"]: self._convert_help_overlay_entry(entry)
                for entry in entries
            },
            "overlay_count": len(entries),
        }

    def _convert_help_overlay_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single help overlay entry to the target Godot format."""
        return {
            "name": entry.get("name"),
            "texts": entry.get("texts", []),
            "lines": entry.get("lines", []),
            "right_brackets": entry.get("right_brackets", []),
            "left_brackets": entry.get("left_brackets", []),
            "line": re.compile(r"^\+pline\s+(\d+)\s+(.+)", re.IGNORECASE),
        }
