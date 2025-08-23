#!/usr/bin/env python3
"""
Armor Table Converter

Focused converter for WCS armor.tbl files.
Single Responsibility: Armor table parsing and conversion only.
"""

import re
from typing import Any, Dict, List, Optional

from .base_converter import BaseTableConverter, ParseState, TableType


class ArmorTableConverter(BaseTableConverter):
    """Converts WCS armor.tbl files to Godot armor resources"""
    
    def _init_parse_patterns(self) -> Dict[str, re.Pattern]:
        return {
            'armor_start': re.compile(r'^\$Name:\s*(.+)$', re.IGNORECASE),
            'damage_type': re.compile(r'^\$Damage Type:\s*(.+)$', re.IGNORECASE),
            'reduction': re.compile(r'^\$Reduction:\s*([\d\.]+)$', re.IGNORECASE)
        }
    
    def get_table_type(self) -> TableType:
        return TableType.ARMOR
    
    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single armor entry from the table"""
        armor_data = {}
        
        while state.has_more_lines():
            line = state.next_line()
            if not line:
                continue
                
            line = line.strip()
            if not line or self._should_skip_line(line, state):
                continue
            
            # Check for armor start
            match = self._parse_patterns['armor_start'].match(line)
            if match:
                armor_data['name'] = match.group(1).strip()
                continue
            
            # Parse armor properties
            if 'name' in armor_data:
                if self._parse_armor_property(line, armor_data):
                    continue
                
                # Check for section end or next entry
                if line.startswith('$Name:') or line.startswith('#End'):
                    state.current_line -= 1  # Put line back for next iteration
                    return armor_data if armor_data else None
        
        return armor_data if armor_data else None
    
    def _parse_armor_property(self, line: str, armor_data: Dict[str, Any]) -> bool:
        """Parse a single armor property line"""
        for property_name, pattern in self._parse_patterns.items():
            if property_name == 'armor_start':
                continue
                
            match = pattern.match(line)
            if match:
                value = match.group(1).strip()
                
                if property_name == 'reduction':
                    armor_data[property_name] = self.parse_value(value, float)
                else:
                    armor_data[property_name] = value
                
                return True
        
        return False
    
    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed armor entry"""
        required_fields = ['name']
        
        for field in required_fields:
            if field not in entry:
                self.logger.warning(f"Armor entry missing required field: {field}")
                return False
        
        # Validate numeric properties
        if 'reduction' in entry and not isinstance(entry['reduction'], (int, float)):
            self.logger.warning(f"Armor {entry['name']}: Invalid reduction value")
            return False
        
        return True
    
    def convert_to_godot_resource(self, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Convert parsed armor entries to Godot resource format"""
        return {
            'resource_type': 'WCSArmorDatabase',
            'armor_types': {entry['name']: self._convert_armor_entry(entry) for entry in entries},
            'armor_count': len(entries)
        }
    
    def _convert_armor_entry(self, armor: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a single armor entry to Godot format"""
        return {
            'display_name': armor.get('name', ''),
            'damage_type': armor.get('damage_type', ''),
            'reduction': armor.get('reduction', 0.0)
        }
