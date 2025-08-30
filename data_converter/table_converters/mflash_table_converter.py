#!/usr/bin/env python3
"""
Muzzle Flash Table Converter

Single Responsibility: Muzzle flash effects definitions parsing and conversion only.
Handles mflash.tbl files for weapon muzzle flash configuration.
"""

import re
from typing import Any, Dict, List, Optional

from .base_converter import BaseTableConverter, ParseState, TableType


class MflashTableConverter(BaseTableConverter):
    """Converts WCS mflash.tbl files to Godot muzzle flash effect resources"""

    # Metadata for auto-registration
    TABLE_TYPE = TableType.MFLASH
    FILENAME_PATTERNS = ["mflash.tbl"]
    CONTENT_PATTERNS = ["#Muzzle flash types"]

    def _init_parse_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for mflash table parsing"""
        return {
            "mflash_start": re.compile(r"^\$Mflash:\s*$", re.IGNORECASE),
            "name": re.compile(r"^\+name:\s*(.+)$", re.IGNORECASE),
            "blob_name": re.compile(r"^\+blob_name:\s*(.+)$", re.IGNORECASE),
            "blob_offset": re.compile(r"^\+blob_offset:\s*([\d\.]+)$", re.IGNORECASE),
            "blob_radius": re.compile(r"^\+blob_radius:\s*([\d\.]+)$", re.IGNORECASE),
            "section_end": re.compile(r"^#end$", re.IGNORECASE),
        }

    def get_table_type(self) -> TableType:
        return TableType.MFLASH

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire mflash.tbl file"""
        entries = []
        current_mflash = None
        current_blobs = []

        while state.has_more_lines():
            line = state.next_line()
            if not line or self._should_skip_line(line, state):
                continue

            line = line.strip()

            # Check for section boundaries
            if self._parse_patterns["section_end"].match(line):
                if current_mflash and current_blobs:
                    current_mflash["blobs"] = current_blobs
                    entries.append(current_mflash)
                    current_mflash = None
                    current_blobs = []
                continue

            # Parse mflash start
            match = self._parse_patterns["mflash_start"].match(line)
            if match:
                if current_mflash and current_blobs:
                    current_mflash["blobs"] = current_blobs
                    entries.append(current_mflash)
                current_mflash = {}
                current_blobs = []
                continue

            # Parse mflash properties
            if current_mflash is not None:
                match = self._parse_patterns["name"].match(line)
                if match:
                    current_mflash["name"] = match.group(1).strip()
                    continue

                # Parse blob properties
                match = self._parse_patterns["blob_name"].match(line)
                if match:
                    blob_data = {"name": match.group(1).strip()}
                    current_blobs.append(blob_data)
                    continue

                if current_blobs:
                    current_blob = current_blobs[-1]
                    match = self._parse_patterns["blob_offset"].match(line)
                    if match:
                        current_blob["offset"] = float(match.group(1))
                        continue

                    match = self._parse_patterns["blob_radius"].match(line)
                    if match:
                        current_blob["radius"] = float(match.group(1))
                        continue

        # Add the last mflash if exists
        if current_mflash and current_blobs:
            current_mflash["blobs"] = current_blobs
            entries.append(current_mflash)

        return entries

    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Not used when parse_table is overridden."""
        return None

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed mflash entry"""
        required_fields = ["name", "blobs"]

        for field in required_fields:
            if field not in entry:
                self.logger.warning(f"Mflash entry missing required field: {field}")
                return False

        # Validate blob properties
        for i, blob in enumerate(entry["blobs"]):
            blob_required = ["name", "offset", "radius"]
            for field in blob_required:
                if field not in blob:
                    self.logger.warning(
                        f"Mflash {entry['name']} blob {i}: missing field: {field}"
                    )
                    return False

            if blob["offset"] < 0:
                self.logger.warning(
                    f"Mflash {entry['name']} blob {i}: invalid offset: {blob['offset']}"
                )
                return False

            if blob["radius"] <= 0:
                self.logger.warning(
                    f"Mflash {entry['name']} blob {i}: invalid radius: {blob['radius']}"
                )
                return False

        return True

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Convert parsed mflash entries to Godot resource format"""
        return {
            "resource_type": "WCSMuzzleFlashDatabase",
            "muzzle_flashes": {
                entry["name"]: self._convert_mflash_entry(entry) for entry in entries
            },
            "muzzle_flash_count": len(entries),
        }

    def _convert_mflash_entry(self, mflash: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single mflash entry to Godot format"""
        converted_blobs = []
        for blob in mflash.get("blobs", []):
            converted_blobs.append(
                {
                    "name": blob.get("name", ""),
                    "offset": blob.get("offset", 0.0),
                    "radius": blob.get("radius", 1.0),
                    "texture_path": f"res://textures/effects/weapons/muzzle_flashes/{blob.get('name', '')}.webp",
                }
            )

        return {
            "name": mflash.get("name", ""),
            "blobs": converted_blobs,
        }
