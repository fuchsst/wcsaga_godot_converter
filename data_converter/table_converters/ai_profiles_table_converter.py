#!/usr/bin/env python3
"""
AI Profiles Table Converter

Single Responsibility: AI profile definitions parsing and conversion only.
Handles ai_profiles.tbl files for global AI difficulty settings and behavior flags.
"""

import re
from typing import Any, Dict, List, Optional

from .base_converter import BaseTableConverter, ParseState, TableType


class AIProfilesTableConverter(BaseTableConverter):
    """Converts WCS ai_profiles.tbl files to Godot AI profile resources"""

    TABLE_TYPE = TableType.AI_PROFILES
    FILENAME_PATTERNS = ["ai_profiles.tbl"]

    def _init_parse_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for ai_profiles.tbl parsing"""
        return {
            "profile_name": re.compile(r"^\$Profile Name:\s*(.+)$", re.IGNORECASE),
            "default_profile": re.compile(r"^\$Default Profile:\s*(.+)$", re.IGNORECASE),
            "difficulty_scale": re.compile(r"^\$(.+):\s*([\d\-\.\s,]+)$", re.IGNORECASE),
            "boolean_flag": re.compile(r"^\$(.+):\s*(YES|NO)$", re.IGNORECASE),
            "section_end": re.compile(r"^#End$", re.IGNORECASE),
        }

    def get_table_type(self) -> TableType:
        return self.TABLE_TYPE

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire ai_profiles.tbl file."""
        entries = []
        # Skip to the start of AI profile definitions
        while state.has_more_lines():
            line = state.peek_line()
            if line and "#AI Profiles" in line:
                state.skip_line()
                break
            state.skip_line()

        while state.has_more_lines():
            line = state.peek_line()
            if not line or self._should_skip_line(line, state):
                state.skip_line()
                continue

            if self._parse_patterns["profile_name"].match(line.strip()):
                entry = self.parse_entry(state)
                if entry:
                    entries.append(entry)
            elif self._parse_patterns["section_end"].match(line.strip()):
                break
            else:
                state.skip_line()
        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single AI profile entry."""
        entry_data: Dict[str, Any] = {"difficulty_scales": {}, "flags": {}}

        while state.has_more_lines():
            line = state.next_line()
            if line is None:
                break

            line = line.strip()
            if not line:
                continue
            
            # Strip inline comments (semicolons)
            if ";" in line:
                line = line.split(";", 1)[0].strip()

            if (
                self._parse_patterns["profile_name"].match(line)
                and "name" in entry_data
            ):
                state.current_line -= 1
                break

            if self._parse_patterns["section_end"].match(line):
                state.current_line -= 1
                break

            match = self._parse_patterns["profile_name"].match(line)
            if match:
                entry_data["name"] = match.group(1).strip()
                continue

            match = self._parse_patterns["default_profile"].match(line)
            if match:
                entry_data["default_profile"] = match.group(1).strip()
                continue

            match = self._parse_patterns["boolean_flag"].match(line)
            if match:
                key, value = match.groups()
                key = key.strip().lower().replace(" ", "_")
                entry_data["flags"][key] = value.upper() == "YES"
                continue

            match = self._parse_patterns["difficulty_scale"].match(line)
            if match:
                key, values = match.groups()
                key = key.strip().lower().replace(" ", "_")
                # Parse comma-separated values for 5 difficulty levels
                entry_data["difficulty_scales"][key] = [
                    self.parse_value(v.strip(), float) for v in values.split(",")
                ]
                continue

        return self.validate_entry(entry_data) and entry_data or None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed AI profile entry."""
        if "name" not in entry:
            self.logger.warning("AI profile entry missing required field: name")
            return False

        # Validate that all difficulty scale arrays have exactly 5 values
        for scale_name, values in entry.get("difficulty_scales", {}).items():
            if not isinstance(values, list) or len(values) != 5:
                self.logger.warning(
                    f"AI profile {entry['name']}: Difficulty scale {scale_name} must have exactly 5 values, got {len(values)}"
                )
                return False

        return True

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed AI profile entries to a Godot resource dictionary."""
        return {
            "resource_type": "WCSAIProfileDatabase",
            "profiles": {
                entry["name"]: self._convert_profile_entry(entry) for entry in entries
            },
            "profile_count": len(entries),
            "default_profile": entries[0].get("default_profile", "SAGA RETAIL") if entries else "SAGA RETAIL",
        }

    def _convert_profile_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single AI profile entry to the target Godot format."""
        difficulty_levels = ["very_easy", "easy", "medium", "hard", "insane"]
        converted = {
            "name": entry.get("name"),
            "default_profile": entry.get("default_profile", ""),
            "difficulty_levels": difficulty_levels,
            "flags": entry.get("flags", {}),
        }

        # Convert difficulty scales to level-based structure
        scales = entry.get("difficulty_scales", {})
        for scale_name, values in scales.items():
            for i, level in enumerate(difficulty_levels):
                level_key = f"{scale_name}_{level}"
                converted[level_key] = values[i] if i < len(values) else 0.0

        return converted
