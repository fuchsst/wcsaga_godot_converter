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
    
    def _init_parse_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for IFF table parsing"""
        return {
            'iff_start': re.compile(r'^\$Name:\s*(.+)$', re.IGNORECASE),
            'iff_color': re.compile(r'^\$Color:\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$', re.IGNORECASE),
            'iff_string': re.compile(r'^\$String:\s*(.+)$', re.IGNORECASE),
            'iff_attackable': re.compile(r'^\$Attackable:\s*(YES|NO)$', re.IGNORECASE),
            'iff_visible': re.compile(r'^\$Visible:\s*(YES|NO)$', re.IGNORECASE),
            'section_end': re.compile(r'^#End$', re.IGNORECASE)
        }
    
    def get_table_type(self) -> TableType:
        return TableType.IFF
    
    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single IFF entry from the table"""
        iff_data = {}
        
        while state.has_more_lines():
            line = state.next_line()
            if not line:
                continue
                
            line = line.strip()
            if not line or self._should_skip_line(line, state):
                continue
            
            # Check for IFF start
            match = self._parse_patterns['iff_start'].match(line)
            if match:
                iff_data['name'] = match.group(1).strip()
                continue
            
            # Parse IFF properties
            if 'name' in iff_data:
                if self._parse_iff_property(line, iff_data):
                    continue
                
                # Check for section end or next entry
                if (self._parse_patterns['iff_start'].match(line) or 
                    self._parse_patterns['section_end'].match(line)):
                    state.current_line -= 1  # Put line back for next iteration
                    return iff_data if iff_data else None
        
        return iff_data if iff_data else None
    
    def _parse_iff_property(self, line: str, iff_data: Dict[str, Any]) -> bool:
        """Parse a single IFF property line"""
        for property_name, pattern in self._parse_patterns.items():
            if property_name in ['iff_start', 'section_end']:
                continue
                
            match = pattern.match(line)
            if match:
                value = match.group(1).strip()
                
                # Handle different property types
                if property_name == 'iff_color':
                    # Convert RGB values to list of integers
                    iff_data['color'] = [int(match.group(1)), int(match.group(2)), int(match.group(3))]
                elif property_name in ['iff_attackable', 'iff_visible']:
                    iff_data[property_name] = value.upper() == 'YES'
                else:
                    iff_data[property_name] = value
                
                return True
        
        return False
    
    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed IFF entry"""
        required_fields = ['name']
        
        for field in required_fields:
            if field not in entry:
                self.logger.warning(f"IFF entry missing required field: {field}")
                return False
        
        # Validate color format if present
        if 'color' in entry:
            color = entry['color']
            if not isinstance(color, list) or len(color) != 3:
                self.logger.warning(f"IFF {entry['name']}: Invalid color format")
                return False
            for component in color:
                if not isinstance(component, int) or not (0 <= component <= 255):
                    self.logger.warning(f"IFF {entry['name']}: Invalid color component {component}")
                    return False
        
        return True
    
    def convert_to_godot_resource(self, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Convert parsed IFF entries to Godot resource format"""
        return {
            'resource_type': 'WCSIFFDatabase',
            'iffs': {entry['name']: self._convert_iff_entry(entry) for entry in entries},
            'iff_count': len(entries)
        }
    
    def _convert_iff_entry(self, iff: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single IFF entry to Godot format"""
        return {
            'display_name': iff.get('name', ''),
            'color': iff.get('color', [255, 255, 255]),
            'string': iff.get('string', ''),
            'attackable': iff.get('attackable', True),
            'visible': iff.get('visible', True)
        }
