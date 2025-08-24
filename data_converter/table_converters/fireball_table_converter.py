#!/usr/bin/env python3
"""
Fireball Table Converter

Single Responsibility: Fireball/explosion effects definitions parsing and conversion only.
Handles fireball.tbl files for visual effects configuration.
"""

import re
from typing import Any, Dict, List, Optional

from .base_converter import BaseTableConverter, ParseState, TableType


class FireballTableConverter(BaseTableConverter):
    """Converts WCS fireball.tbl files to Godot explosion effect resources"""

    # Metadata for auto-registration
    TABLE_TYPE = TableType.FIREBALL
    FILENAME_PATTERNS = ["fireball.tbl"]
    CONTENT_PATTERNS = ["fireball.tbl"]

    def _init_parse_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for fireball table parsing"""
        return {
            "fireball_entry": re.compile(r"^\$Name:[\s\t]*(\w+)[\s\t]*.*$", re.IGNORECASE),
            "lod_entry": re.compile(r"^\$LOD:[\s\t]*(\d+)[\s\t]*$", re.IGNORECASE),
            "section_start": re.compile(r"^#Start$", re.IGNORECASE),
            "section_end": re.compile(r"^#End$", re.IGNORECASE),
        }

    def get_table_type(self) -> TableType:
        return TableType.FIREBALL

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire fireball.tbl file"""
        entries = []
        current_fireball = None
        in_section = False

        while state.has_more_lines():
            line = state.next_line()
            if not line or self._should_skip_line(line, state):
                continue

            line = line.strip()

            # Check for section boundaries
            if self._parse_patterns["section_start"].match(line):
                in_section = True
                continue
            if self._parse_patterns["section_end"].match(line):
                in_section = False
                if current_fireball:
                    entries.append(current_fireball)
                    current_fireball = None
                continue

            if not in_section:
                continue

            # Parse fireball entries
            match = self._parse_patterns["fireball_entry"].match(line)
            if match:
                if current_fireball:
                    entries.append(current_fireball)
                current_fireball = {"name": match.group(1).strip()}
                continue

            # Parse LOD entries
            match = self._parse_patterns["lod_entry"].match(line)
            if match and current_fireball:
                current_fireball["lod"] = int(match.group(1))
                continue

        # Add the last fireball if exists
        if current_fireball:
            entries.append(current_fireball)

        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Not used when parse_table is overridden."""
        return None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed fireball entry"""
        required_fields = ["name", "lod"]

        for field in required_fields:
            if field not in entry:
                self.logger.warning(f"Fireball entry missing required field: {field}")
                return False

        # Validate LOD value
        if entry["lod"] not in [0, 1]:
            self.logger.warning(f"Fireball {entry['name']}: Invalid LOD value: {entry['lod']}")
            return False

        return True

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed fireball entries to Godot resource format"""
        return {
            "resource_type": "WCSFireballDatabase",
            "fireballs": {
                entry["name"]: self._convert_fireball_entry(entry) for entry in entries
            },
            "fireball_count": len(entries),
        }

    def _convert_fireball_entry(self, fireball: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single fireball entry to Godot format"""
        return {
            "name": fireball.get("name", ""),
            "lod": fireball.get("lod", 1),
            "animation_path": f"res://animations/effects/explosions/{fireball['name']}.tres",
            "texture_path": f"res://textures/effects/explosions/{fireball['name']}.webp",
        }
