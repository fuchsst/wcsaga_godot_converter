#!/usr/bin/env python3
"""
AI Table Converter

Single Responsibility: AI behavior definitions parsing and conversion only.
Handles ai.tbl files for AI ship behavior configuration with 5-skill-level scaling.
"""

import re
from typing import Any, Dict, List, Optional

from .base_converter import BaseTableConverter, ParseState, TableType


class AITableConverter(BaseTableConverter):
    """Converts WCS ai.tbl files to Godot AI behavior resources"""

    TABLE_TYPE = TableType.AI
    FILENAME_PATTERNS = ["ai.tbl"]

    def _init_parse_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for AI table parsing"""
        return {
            "ai_class_start": re.compile(r"^\$Name:\s*(.+)$", re.IGNORECASE),
            "ai_class_end": re.compile(r"^\$end$", re.IGNORECASE),
            "ai_property": re.compile(
                r"^\$(\w[\w\s#]*):\s*([\d\-\.\s,]+)$", re.IGNORECASE
            ),
            "boolean_flag": re.compile(r"^\$(\w[\w\s]*):\s*(YES|NO)$", re.IGNORECASE),
            "section_end": re.compile(r"^#End$", re.IGNORECASE),
        }

    def get_table_type(self) -> TableType:
        return self.TABLE_TYPE

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire ai.tbl file."""
        entries = []
        # Skip to the start of AI class definitions
        while state.has_more_lines():
            line = state.peek_line()
            if line and "#AI Classes" in line:
                state.skip_line()
                break
            state.skip_line()

        while state.has_more_lines():
            line = state.peek_line()
            if not line or self._should_skip_line(line, state):
                state.skip_line()
                continue

            if self._parse_patterns["ai_class_start"].match(line.strip()):
                entry = self.parse_entry(state)
                if entry:
                    entries.append(entry)
            elif self._parse_patterns["section_end"].match(line.strip()):
                break
            else:
                state.skip_line()
        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single AI class entry from the table"""
        ai_class_data: Dict[str, Any] = {"properties": {}, "flags": {}}

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
                self._parse_patterns["ai_class_start"].match(line)
                and "name" in ai_class_data
            ):
                state.current_line -= 1
                break

            if self._parse_patterns["section_end"].match(line):
                state.current_line -= 1
                break

            match = self._parse_patterns["ai_class_start"].match(line)
            if match:
                ai_class_data["name"] = match.group(1).strip()
                continue

            match = self._parse_patterns["ai_property"].match(line)
            if match:
                key, values = match.groups()
                key = key.strip().lower().replace(" ", "_")
                # Parse comma-separated values for 5 skill levels
                ai_class_data["properties"][key] = [
                    self.parse_value(v.strip(), float) for v in values.split(",")
                ]
                continue

            match = self._parse_patterns["boolean_flag"].match(line)
            if match:
                key, value = match.groups()
                key = key.strip().lower().replace(" ", "_")
                ai_class_data["flags"][key] = value.upper() == "YES"
                continue

            if self._parse_patterns["ai_class_end"].match(line):
                break

        return self.validate_entry(ai_class_data) and ai_class_data or None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed AI class entry"""
        if "name" not in entry:
            self.logger.warning("AI class entry missing required field: name")
            return False

        # Validate that all property arrays have exactly 5 values (5 skill levels)
        for prop_name, values in entry.get("properties", {}).items():
            if not isinstance(values, list) or len(values) != 5:
                self.logger.warning(
                    f"AI class {entry['name']}: Property {prop_name} must have exactly 5 values, got {len(values)}"
                )
                return False

        return True

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed AI class entries to Godot resource format"""
        return {
            "resource_type": "WCSAIDatabase",
            "ai_classes": {
                entry["name"]: self._convert_ai_class_entry(entry) for entry in entries
            },
            "ai_class_count": len(entries),
        }

    def _convert_ai_class_entry(self, ai_class: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single AI class entry to Godot format"""
        skill_levels = ["trainee", "rookie", "hotshot", "ace", "insane"]
        converted = {
            "display_name": ai_class.get("name", ""),
            "skill_levels": skill_levels,
            "flags": ai_class.get("flags", {}),
        }

        # Convert properties to skill-level based structure
        properties = ai_class.get("properties", {})
        for prop_name, values in properties.items():
            for i, level in enumerate(skill_levels):
                level_key = f"{prop_name}_{level}"
                converted[level_key] = values[i] if i < len(values) else 0.0

        return converted
