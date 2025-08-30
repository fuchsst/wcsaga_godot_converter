#!/usr/bin/env python3
"""
Sounds Table Converter

Single Responsibility: Sound definitions parsing and conversion only.
Handles sounds.tbl files for audio system configuration, including
parsing different sections and formats, inspired by the robust parsing
logic of other converters.
"""

import re
from typing import Any, Dict, List, Optional


from .base_converter import BaseTableConverter, ParseState, TableType


class SoundsTableConverter(BaseTableConverter):
    """Converts WCS sounds.tbl files to Godot audio resources"""

    # Metadata for auto-registration
    TABLE_TYPE = TableType.SOUNDS
    FILENAME_PATTERNS = ["sounds.tbl"]
    CONTENT_PATTERNS = ["sounds.tbl"]

    def _init_parse_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for sounds table parsing"""
        return {
            "section_start": re.compile(r"^#\s*(\w+)\s+Sounds\s+Start", re.IGNORECASE),
            "section_end": re.compile(r"^#\s*(\w+)\s+Sounds\s+End", re.IGNORECASE),
            "sound_entry": re.compile(
                r"^\$Name:\s*(\d+)\s+([^,]+),\s*(\d+),\s*([\d\.]+),\s*(\d+)(?:,\s*([\d\.]+),\s*([\d\.]+))?\s*;\s*(.*)",
                re.IGNORECASE,
            ),
            "flyby_entry": re.compile(
                r"^\$(\w+):\s*(\d+)\s+([^,]+),\s*(\d+),\s*([\d\.]+),\s*(\d+)(?:,\s*([\d\.]+),\s*([\d\.]+))?\s*;\s*\*\s*(.*)",
                re.IGNORECASE,
            ),
        }

    def get_table_type(self) -> TableType:
        return TableType.SOUNDS

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """
        Parse the entire sounds.tbl file, handling different sections and formats.
        """
        entries = []
        current_section = "unknown"

        while state.has_more_lines():
            line = state.next_line()
            if not line or self._should_skip_line(line, state):
                continue

            # Update current section
            start_match = self._parse_patterns["section_start"].match(line)
            if start_match:
                current_section = start_match.group(1).lower()
                self.logger.info(f"Parsing sound section: '{current_section}'")
                continue

            end_match = self._parse_patterns["section_end"].match(line)
            if end_match:
                self.logger.info(f"Finished parsing sound section: '{current_section}'")
                current_section = "unknown"
                continue

            # Parse entry based on current section
            entry = None
            if current_section == "flyby":
                entry = self._parse_flyby_sound(line, current_section)
            elif current_section in ["game", "interface"]:
                entry = self._parse_standard_sound(line, current_section)

            if entry and self.validate_entry(entry):
                entries.append(entry)
                self.logger.debug(f"Parsed sound entry: {entry['name']}")
            elif (
                line.strip()
                and not line.strip().startswith(";")
                and current_section != "unknown"
            ):
                self.logger.debug(
                    f"Skipped line in section '{current_section}': {line.strip()}"
                )

        return entries

    def _parse_standard_sound(
        self, line: str, section: str
    ) -> Optional[Dict[str, Any]]:
        """Parse a standard game or interface sound line."""
        match = self._parse_patterns["sound_entry"].match(line)
        if not match:
            return None

        sound_id, filename, preload, volume, sound_type, min_dist, max_dist, comment = (
            match.groups()
        )
        unique_name = f"{section}_{sound_id}"

        return {
            "name": unique_name,
            "filename": filename.strip(),
            "preload": int(preload) > 0,
            "default_volume": float(volume),
            "is_3d": int(sound_type) > 0,
            "min_distance": float(min_dist) if min_dist else 100.0,
            "max_distance": float(max_dist) if max_dist else 1000.0,
            "comment": comment.strip() if comment else "",
        }

    def _parse_flyby_sound(self, line: str, section: str) -> Optional[Dict[str, Any]]:
        """Parse a flyby sound line with faction information."""
        match = self._parse_patterns["flyby_entry"].match(line)
        if not match:
            return None

        (
            faction,
            sound_id,
            filename,
            preload,
            volume,
            sound_type,
            min_dist,
            max_dist,
            comment,
        ) = match.groups()
        unique_name = f"{section}_{faction.lower()}_{sound_id}"

        return {
            "name": unique_name,
            "filename": filename.strip(),
            "preload": int(preload) > 0,
            "default_volume": float(volume),
            "is_3d": int(sound_type) > 0,
            "min_distance": float(min_dist) if min_dist else 100.0,
            "max_distance": float(max_dist) if max_dist else 1000.0,
            "comment": comment.strip() if comment else "",
        }

    def _convert_sound_entry(self, sound: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single sound entry to the target Godot format."""
        # Map to proper audio paths based on sound type and documentation
        filename = sound.get("filename", "")
        if filename.lower() == "none.wav":
            return None

        # Determine audio type and target path based on documentation
        audio_type = self._determine_audio_type(sound)
        target_path = self._generate_target_path(filename, audio_type)

        return {
            "display_name": sound.get("name", "Unknown Sound"),
            "filename": filename,
            "target_path": target_path,
            "description": sound.get("comment", ""),
            "default_volume": sound.get("default_volume", 0.8),
            "preload": sound.get("preload", False),
            "is_3d": sound.get("is_3d", False),
            "min_distance": sound.get("min_distance", 100.0),
            "max_distance": sound.get("max_distance", 1000.0),
            "audio_type": audio_type,
        }

    def _determine_audio_type(self, sound: Dict[str, Any]) -> str:
        """Determine the audio type based on sound properties and documentation."""
        name = sound.get("name", "").lower()
        sound.get("comment", "").lower()

        if "weapon" in name or "laser" in name or "missile" in name or "fire" in name:
            return "weapon"
        elif "explosion" in name or "explode" in name or "blast" in name:
            return "explosion"
        elif "engine" in name or "thrust" in name or "aburn" in name:
            return "engine"
        elif "ui" in name or "interface" in name or "menu" in name or "click" in name:
            return "ui"
        elif "voice" in name or "briefing" in name or "communication" in name:
            return "voice"
        elif "ambient" in name or "environment" in name or "space" in name:
            return "ambient"
        elif "flyby" in name:
            return "flyby"
        else:
            return "sfx"

    def _generate_target_path(self, filename: str, audio_type: str) -> str:
        """Generate target path based on audio type and documentation."""
        base_name = filename.replace(".wav", ".ogg")

        if audio_type == "weapon":
            return f"res://audio/sfx/weapons/{base_name}"
        elif audio_type == "explosion":
            return f"res://audio/sfx/explosions/{base_name}"
        elif audio_type == "engine":
            return f"res://audio/sfx/environment/engines/{base_name}"
        elif audio_type == "ui":
            return f"res://audio/sfx/ui/{base_name}"
        elif audio_type == "voice":
            return f"res://audio/voice/{base_name}"
        elif audio_type == "ambient":
            return f"res://audio/ambient/{base_name}"
        elif audio_type == "flyby":
            return f"res://audio/sfx/flyby/{base_name}"
        else:
            return f"res://audio/sfx/{base_name}"

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed sound entry."""
        if not entry.get("name") or not entry.get("filename"):
            return False

        if "default_volume" in entry and not (0.0 <= entry["default_volume"] <= 1.0):
            self.logger.warning(
                f"Sound '{entry['name']}' has invalid volume: {entry['default_volume']}"
            )
            return False

        return True

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed sound entries to a Godot resource dictionary."""
        return {
            "resource_type": "WCSSoundDatabase",
            "sounds": {
                entry["name"]: self._convert_sound_entry(entry) for entry in entries
            },
            "sound_count": len(entries),
        }

    def _convert_sound_entry(self, sound: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single sound entry to the target Godot format."""
        return {
            "display_name": sound.get("name", "Unknown Sound"),
            "filename": sound.get("filename"),
            "description": sound.get("comment", ""),
            "default_volume": sound.get("default_volume", 0.8),
            "preload": sound.get("preload", False),
            "is_3d": sound.get("is_3d", False),
            "min_distance": sound.get("min_distance", 100.0),
            "max_distance": sound.get("max_distance", 1000.0),
        }

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Not used when parse_table is overridden."""
        return None
