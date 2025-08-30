#!/usr/bin/env python3
"""
Nebula Table Converter

Single Responsibility: Nebula background and cloud definitions parsing and conversion only.
Handles nebula.tbl files for environment configuration.
"""

import re
from typing import Any, Dict, List, Optional

from .base_converter import BaseTableConverter, ParseState, TableType


class NebulaTableConverter(BaseTableConverter):
    """Converts WCS nebula.tbl files to Godot environment resources"""

    # Metadata for auto-registration
    TABLE_TYPE = TableType.NEBULA
    FILENAME_PATTERNS = ["nebula.tbl"]
    CONTENT_PATTERNS = ["nebula.tbl"]

    def _init_parse_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for nebula.tbl parsing"""
        return {
            "nebula": re.compile(r"^\+Nebula:\s*(.+)$", re.IGNORECASE),
            "poof": re.compile(r"^\+Poof:\s*(.+)$", re.IGNORECASE),
            "section_end": re.compile(r"^#end$", re.IGNORECASE),
        }

    def get_table_type(self) -> TableType:
        return TableType.NEBULA

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire nebula.tbl file."""
        entries = []

        while state.has_more_lines():
            line = state.next_line()
            if not line or self._should_skip_line(line, state):
                continue

            line = line.strip()
            if not line:
                continue

            if self._parse_patterns["section_end"].match(line):
                continue

            # Nebula background bitmaps
            match = self._parse_patterns["nebula"].match(line)
            if match:
                entries.append(
                    {
                        "name": match.group(1).strip(),
                        "type": "nebula_background",
                    }
                )
                continue

            # Poof cloud bitmaps
            match = self._parse_patterns["poof"].match(line)
            if match:
                entries.append(
                    {
                        "name": match.group(1).strip(),
                        "type": "poof_cloud",
                    }
                )
                continue

        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Not used when parse_table is overridden."""
        return None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed nebula entry."""
        return "name" in entry and "type" in entry

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed nebula entries to a Godot resource dictionary."""
        nebula_backgrounds = [
            e for e in entries if e.get("type") == "nebula_background"
        ]
        poof_clouds = [e for e in entries if e.get("type") == "poof_cloud"]

        return {
            "resource_type": "WCSNebulaDatabase",
            "nebula_backgrounds": {
                nb["name"]: {
                    "type": "Texture",
                    "path": f"res://textures/environment/nebula/backgrounds/{nb['name']}.webp",
                }
                for nb in nebula_backgrounds
            },
            "poof_clouds": {
                pc["name"]: {
                    "type": "Texture",
                    "path": f"res://textures/environment/nebula/clouds/{pc['name']}.webp",
                }
                for pc in poof_clouds
            },
        }
