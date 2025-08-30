#!/usr/bin/env python3
"""
Weapon Explosion Table Converter

Single Responsibility: Weapon explosion effects definitions parsing and conversion only.
Handles weapon_expl.tbl files for weapon impact effect configuration.
"""

import re
from typing import Any, Dict, List, Optional

from .base_converter import BaseTableConverter, ParseState, TableType


class WeaponExplTableConverter(BaseTableConverter):
    """Converts WCS weapon_expl.tbl files to Godot weapon explosion effect resources"""

    # Metadata for auto-registration
    TABLE_TYPE = TableType.WEAPON_EXPL
    FILENAME_PATTERNS = ["weapon_expl.tbl"]
    CONTENT_PATTERNS = ["weapon_expl.tbl"]

    def _init_parse_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for weapon explosion table parsing"""
        return {
            "explosion_entry": re.compile(
                r"^\$Name:[\s\t]*(\w+)[\s\t]*.*$", re.IGNORECASE
            ),
            "lod_entry": re.compile(r"^\$LOD:[\s\t]*(\d+)[\s\t]*$", re.IGNORECASE),
            "section_start": re.compile(r"^#Start$", re.IGNORECASE),
            "section_end": re.compile(r"^#End$", re.IGNORECASE),
        }

    def get_table_type(self) -> TableType:
        return TableType.WEAPON_EXPL

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire weapon_expl.tbl file"""
        entries = []
        current_explosion = None
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
                if current_explosion:
                    entries.append(current_explosion)
                    current_explosion = None
                continue

            if not in_section:
                continue

            # Parse explosion entries
            match = self._parse_patterns["explosion_entry"].match(line)
            if match:
                if current_explosion:
                    entries.append(current_explosion)
                current_explosion = {"name": match.group(1).strip()}
                continue

            # Parse LOD entries
            match = self._parse_patterns["lod_entry"].match(line)
            if match and current_explosion:
                current_explosion["lod"] = int(match.group(1))
                continue

        # Add the last explosion if exists
        if current_explosion:
            entries.append(current_explosion)

        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Not used when parse_table is overridden."""
        return None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed weapon explosion entry"""
        required_fields = ["name", "lod"]

        for field in required_fields:
            if field not in entry:
                self.logger.warning(
                    f"Weapon explosion entry missing required field: {field}"
                )
                return False

        # Validate LOD value
        if entry["lod"] not in [0, 1]:
            self.logger.warning(
                f"Weapon explosion {entry['name']}: Invalid LOD value: {entry['lod']}"
            )
            return False

        return True

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed weapon explosion entries to Godot resource format"""
        return {
            "resource_type": "WCSWeaponExplosionDatabase",
            "explosions": {
                entry["name"]: self._convert_explosion_entry(entry) for entry in entries
            },
            "explosion_count": len(entries),
        }

    def _convert_explosion_entry(self, explosion: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single explosion entry to Godot format"""
        return {
            "name": explosion.get("name", ""),
            "lod": explosion.get("lod", 1),
            "animation_path": f"res://animations/effects/weapons/impacts/{explosion['name']}.tres",
            "texture_path": f"res://textures/effects/weapons/impacts/{explosion['name']}.webp",
        }
