#!/usr/bin/env python3
"""
Ship Table Converter

Focused converter for WCS ships.tbl files.
Handles ship class definitions, specifications, and capabilities.

Single Responsibility: Ship table parsing and conversion only.
"""

import re
from typing import Any, Dict, List, Optional

from .base_converter import BaseTableConverter, ParseState, TableType


class ShipTableConverter(BaseTableConverter):
    """Converts WCS ships.tbl files to Godot ship resources"""
    
    def __init__(self, source_dir, target_dir):
        """Initialize ship table converter with statistics tracking."""
        super().__init__(source_dir, target_dir)
        
        # Ship-specific statistics
        self._entries_processed = 0
        self._conversion_errors = []
        self._conversion_warnings = []
        self._asset_registry = {}
        self._relationship_mappings = {}
    
    def _init_parse_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for ship table parsing"""
        return {
            # Basic ship identification
            'ship_start': re.compile(r'^\$Name:\s*(.+)$', re.IGNORECASE),
            'short_name': re.compile(r'^\$Short name:\s*(.+)$', re.IGNORECASE),
            'species': re.compile(r'^\$Species:\s*(.+)$', re.IGNORECASE),
            'type': re.compile(r'^\$Type:\s*(.+)$', re.IGNORECASE),
            
            # Physics and performance
            'max_velocity': re.compile(r'^\$Max velocity:\s*([\d\.\-\s,]+)$', re.IGNORECASE),
            'afterburner_velocity': re.compile(r'^\$Max afterburner velocity:\s*([\d\.]+)$', re.IGNORECASE),
            'hitpoints': re.compile(r'^\$Hitpoints:\s*([\d\.]+)$', re.IGNORECASE),
            'mass': re.compile(r'^\$Mass:\s*([\d\.]+)$', re.IGNORECASE),
            'density': re.compile(r'^\$Density:\s*([\d\.]+)$', re.IGNORECASE),
            'max_shield': re.compile(r'^\$Shield:\s*([\d\.]+)$', re.IGNORECASE),
            'power_output': re.compile(r'^\$Power Output:\s*([\d\.]+)$', re.IGNORECASE),
            'max_weapon_energy': re.compile(r'^\$Max Weapon Energy:\s*([\d\.]+)$', re.IGNORECASE),
            'afterburner_fuel': re.compile(r'^\$Afterburner Fuel Capacity:\s*([\d\.]+)$', re.IGNORECASE),
            
            # 3D Models and geometry
            'model_file': re.compile(r'^\$Model file:\s*(.+)$', re.IGNORECASE),
            'pof_file': re.compile(r'^\$POF file:\s*(.+)$', re.IGNORECASE),
            'pof_target_file': re.compile(r'^\$POF target file:\s*(.+)$', re.IGNORECASE),
            'cockpit_pof_file': re.compile(r'^\$Cockpit POF file:\s*(.+)$', re.IGNORECASE),
            'detail_distance': re.compile(r'^\$Detail distance:\s*([\d\.]+)$', re.IGNORECASE),
            
            # Audio assets
            'warpin_start_sound': re.compile(r'^\$Warpin Start Sound:\s*(.+)$', re.IGNORECASE),
            'warpin_end_sound': re.compile(r'^\$Warpin End Sound:\s*(.+)$', re.IGNORECASE),
            'warpout_start_sound': re.compile(r'^\$Warpout Start Sound:\s*(.+)$', re.IGNORECASE),
            'warpout_end_sound': re.compile(r'^\$Warpout End Sound:\s*(.+)$', re.IGNORECASE),
            'engine_sound': re.compile(r'^\$EngineSnd:\s*(.+)$', re.IGNORECASE),
            'alive_sound': re.compile(r'^\$AliveSnd:\s*(.+)$', re.IGNORECASE),
            'dead_sound': re.compile(r'^\$DeadSnd:\s*(.+)$', re.IGNORECASE),
            'rotation_sound': re.compile(r'^\$RotationSnd:\s*(.+)$', re.IGNORECASE),
            'turret_base_rotation_sound': re.compile(r'^\$Turret Base RotationSnd:\s*(.+)$', re.IGNORECASE),
            'turret_gun_rotation_sound': re.compile(r'^\$Turret Gun RotationSnd:\s*(.+)$', re.IGNORECASE),
            
            # Animation and effects
            'warpin_animation': re.compile(r'^\$Warpin animation:\s*(.+)$', re.IGNORECASE),
            'warpout_animation': re.compile(r'^\$Warpout animation:\s*(.+)$', re.IGNORECASE),
            'explosion_animations': re.compile(r'^\$Explosion Animations:\s*(.+)$', re.IGNORECASE),
            'shockwave_model': re.compile(r'^\$Shockwave model:\s*(.+)$', re.IGNORECASE),
            'selection_effect': re.compile(r'^\$Selection Effect:\s*(.+)$', re.IGNORECASE),
            
            # Thruster configuration and effects
            'thruster_flame': re.compile(r'^\$Thruster flame effect:\s*(.+)$', re.IGNORECASE),
            'thruster_glow': re.compile(r'^\$Thruster glow effect:\s*(.+)$', re.IGNORECASE),
            'thruster_start_sound': re.compile(r'^\+StartSnd:\s*(.+)$', re.IGNORECASE),
            'thruster_loop_sound': re.compile(r'^\+LoopSnd:\s*(.+)$', re.IGNORECASE),
            'thruster_stop_sound': re.compile(r'^\+StopSnd:\s*(.+)$', re.IGNORECASE),
            
            # UI and HUD assets
            'shield_icon': re.compile(r'^\$Shield Icon:\s*(.+)$', re.IGNORECASE),
            'ship_icon': re.compile(r'^\$Ship_icon:\s*(.+)$', re.IGNORECASE),
            'ship_anim': re.compile(r'^\$Ship_anim:\s*(.+)$', re.IGNORECASE),
            'ship_overhead': re.compile(r'^\$Ship_overhead:\s*(.+)$', re.IGNORECASE),
            
            # Tech database assets
            'tech_model': re.compile(r'^\$Tech Model:\s*(.+)$', re.IGNORECASE),
            'tech_anim': re.compile(r'^\$Tech Anim:\s*(.+)$', re.IGNORECASE),
            'tech_image': re.compile(r'^\$Tech Image:\s*(.+)$', re.IGNORECASE),
            
            # Texture modifications
            'texture_replace': re.compile(r'^\$Texture Replace:\s*(.+)$', re.IGNORECASE),
            
            # Section termination
            'section_end': re.compile(r'^\$end_multi_text\s*$', re.IGNORECASE),
        }
    
    def get_table_type(self) -> TableType:
        return TableType.SHIPS
    
    def parse_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single ship entry from the table and capture asset relationships"""
        ship_data = {}
        
        while state.has_more_lines():
            line = state.next_line()
            if not line:
                continue
                
            line = line.strip()
            if not line or self._should_skip_line(line, state):
                continue
            
            # Check for ship start
            match = self._parse_patterns['ship_start'].match(line)
            if match:
                ship_data['name'] = match.group(1).strip()
                continue
            
            # Parse ship properties
            if 'name' in ship_data:  # Only parse if we're in a ship section
                if self._parse_ship_property(line, ship_data):
                    # Capture asset relationships for asset mapping
                    self._capture_asset_relationships(line, ship_data)
                    continue
                
                # Check for section end
                if self._parse_patterns['section_end'].match(line):
                    # Finalize asset mapping for this ship
                    self._finalize_ship_asset_mapping(ship_data)
                    return ship_data if ship_data else None
        
        return ship_data if ship_data else None
    
    def _parse_ship_property(self, line: str, ship_data: Dict[str, Any]) -> bool:
        """Parse a single ship property line"""
        for property_name, pattern in self._parse_patterns.items():
            if property_name in ['ship_start', 'section_end']:
                continue
                
            match = pattern.match(line)
            if match:
                value = match.group(1).strip()
                
                # Handle special parsing for specific properties
                if property_name == 'max_velocity':
                    ship_data['max_velocity'] = self._parse_velocity_vector(value)
                elif property_name in ['afterburner_velocity', 'hitpoints', 'mass', 'density', 'max_shield', 
                                     'power_output', 'max_weapon_energy', 'afterburner_fuel', 'detail_distance']:
                    ship_data[property_name] = self.parse_value(value, float)
                else:
                    ship_data[property_name] = value
                
                return True
        
        return False
    
    def _parse_velocity_vector(self, velocity_str: str) -> Dict[str, float]:
        """Parse velocity vector string like '65.0, 75.0, 65.0'"""
        try:
            components = [float(x.strip()) for x in velocity_str.split(',')]
            if len(components) == 3:
                return {
                    'forward': components[0],
                    'reverse': components[1], 
                    'side': components[2]
                }
            else:
                # Single value for all directions
                value = components[0] if components else 0.0
                return {
                    'forward': value,
                    'reverse': value,
                    'side': value
                }
        except (ValueError, IndexError):
            self.logger.warning(f"Failed to parse velocity: {velocity_str}")
            return {'forward': 0.0, 'reverse': 0.0, 'side': 0.0}
    
    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed ship entry"""
        required_fields = ['name']
        
        for field in required_fields:
            if field not in entry:
                self.logger.warning(f"Ship entry missing required field: {field}")
                return False
        
        # Validate numeric fields
        numeric_fields = ['hitpoints', 'mass', 'density', 'max_shield', 'power_output', 
                         'max_weapon_energy', 'afterburner_fuel', 'detail_distance']
        for field in numeric_fields:
            if field in entry and not isinstance(entry[field], (int, float)):
                self.logger.warning(f"Ship {entry['name']}: Invalid {field} value")
                return False
        
        return True
    
    def convert_to_godot_resources(self, entries: List[Dict[str, Any]], output_dir: str) -> Dict[str, Any]:
        """Convert parsed ship entries to Godot .tres resource files"""
        from ..resource_generators.ship_class_generator import \
            ShipClassGenerator

        # Create resource generator
        generator = ShipClassGenerator(output_dir)
        
        # Generate ship resources
        resource_files = generator.generate_ship_resources(entries)
        
        return {
            'conversion_type': 'ship_resources',
            'resource_files': resource_files,
            'ship_count': len(entries),
            'output_directory': output_dir
        }
    
    def convert_to_godot_resource(self, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Legacy method - now redirects to resource generation"""
        # For compatibility - generate resources in default location
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            return self.convert_to_godot_resources(entries, temp_dir)
    
    # ========== ASSET MAPPING INTEGRATION ==========
    
    def _capture_asset_relationships(self, line: str, ship_data: Dict[str, Any]) -> None:
        """Capture asset relationships from parsed ship properties"""
        # Asset property patterns that should be captured for mapping
        asset_properties = [
            'model_file', 'pof_file', 'pof_target_file', 'cockpit_pof_file',
            'warpin_start_sound', 'warpin_end_sound', 'warpout_start_sound', 'warpout_end_sound',
            'engine_sound', 'alive_sound', 'dead_sound', 'rotation_sound',
            'turret_base_rotation_sound', 'turret_gun_rotation_sound',
            'warpin_animation', 'warpout_animation', 'explosion_animations', 'shockwave_model',
            'selection_effect', 'thruster_flame', 'thruster_glow',
            'thruster_start_sound', 'thruster_loop_sound', 'thruster_stop_sound',
            'shield_icon', 'ship_icon', 'ship_anim', 'ship_overhead',
            'tech_model', 'tech_anim', 'tech_image', 'texture_replace'
        ]
        
        for prop_name in asset_properties:
            pattern = self._parse_patterns.get(prop_name)
            if pattern:
                match = pattern.match(line)
                if match:
                    asset_path = match.group(1).strip()
                    if asset_path:
                        # Store in asset registry
                        ship_name = ship_data.get('name', 'unknown')
                        if ship_name not in self._asset_registry:
                            self._asset_registry[ship_name] = []
                        self._asset_registry[ship_name].append({
                            'property': prop_name,
                            'asset_path': asset_path,
                            'asset_type': self._get_asset_type(prop_name, asset_path)
                        })
    
    def _finalize_ship_asset_mapping(self, ship_data: Dict[str, Any]) -> None:
        """Finalize asset mapping for a completed ship entry"""
        ship_name = ship_data.get('name')
        if not ship_name or ship_name not in self._asset_registry:
            return
        
        # Create relationship mapping for this ship
        self._relationship_mappings[ship_name] = {
            'entity_type': 'ship',
            'assets': self._asset_registry[ship_name],
            'primary_asset': self._get_primary_asset(ship_data),
            'related_assets': self._asset_registry[ship_name]
        }
        
        # Update statistics
        self._entries_processed += 1
    
    def _get_asset_type(self, property_name: str, asset_path: str) -> str:
        """Determine asset type based on property name and path"""
        if any(prop in property_name for prop in ['sound', 'snd']):
            return 'audio'
        elif any(prop in property_name for prop in ['model', 'pof']):
            return 'model'
        elif any(prop in property_name for prop in ['animation', 'anim', 'effect']):
            return 'animation'
        elif any(prop in property_name for prop in ['icon', 'image']):
            return 'texture'
        else:
            # Infer from file extension
            if asset_path.lower().endswith(('.wav', '.ogg', '.mp3')):
                return 'audio'
            elif asset_path.lower().endswith(('.pof', '.obj', '.gltf', '.glb')):
                return 'model'
            elif asset_path.lower().endswith(('.dds', '.png', '.jpg', '.jpeg', '.tga')):
                return 'texture'
            else:
                return 'unknown'
    
    def _get_primary_asset(self, ship_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get the primary asset (main model) for the ship"""
        primary_asset_props = ['pof_file', 'model_file']
        
        for prop in primary_asset_props:
            asset_path = ship_data.get(prop)
            if asset_path:
                return {
                    'property': prop,
                    'asset_path': asset_path,
                    'asset_type': 'model'
                }
        return None