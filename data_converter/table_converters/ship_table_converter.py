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
    """Converts WCS ships.tbl files to Godot ship resources following SOLID principles"""

    # Metadata for auto-registration
    TABLE_TYPE = TableType.SHIPS
    FILENAME_PATTERNS = ["ships.tbl", "Ships.tbl"]
    CONTENT_PATTERNS = ["$Name:", "$Species:", "$POF file:"]

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
        """Initialize regex patterns for ship table parsing, organized by category"""
        # Basic ship identification
        basic_patterns = {
            "ship_start": re.compile(r"^\$Name:\s*(.+)$", re.IGNORECASE),
            "short_name": re.compile(r"^\$Short name:\s*(.+)$", re.IGNORECASE),
            "species": re.compile(r"^\$Species:\s*(.+)$", re.IGNORECASE),
            "type": re.compile(r"^\$Type:\s*(.+)$", re.IGNORECASE),
        }
        
        # Engine wash properties
        engine_wash_patterns = {
            "engine_wash_start": re.compile(r"^\$Name:\s*(.+)$", re.IGNORECASE),
            "angle": re.compile(r"^\$Angle:\s*([\d\.]+)$", re.IGNORECASE),
            "radius_mult": re.compile(r"^\$Radius Mult:\s*([\d\.]+)$", re.IGNORECASE),
            "length": re.compile(r"^\$Length:\s*([\d\.]+)$", re.IGNORECASE),
            "intensity": re.compile(r"^\$Intensity:\s*([\d\.]+)$", re.IGNORECASE),
        }
        
        # Physics and performance
        physics_patterns = {
            "max_velocity": re.compile(
                r"^\$Max velocity:\s*([\d\.\-\s,]+)$", re.IGNORECASE
            ),
            "afterburner_velocity": re.compile(
                r"^\$Max afterburner velocity:\s*([\d\.]+)$", re.IGNORECASE
            ),
            "hitpoints": re.compile(r"^\$Hitpoints:\s*([\d\.]+)$", re.IGNORECASE),
            "mass": re.compile(r"^\$Mass:\s*([\d\.]+)$", re.IGNORECASE),
            "density": re.compile(r"^\$Density:\s*([\d\.]+)$", re.IGNORECASE),
            "max_shield": re.compile(r"^\$Shields?:\s*([\d\.]+)$", re.IGNORECASE),
            "power_output": re.compile(r"^\$Power Output:\s*([\d\.]+)$", re.IGNORECASE),
            "max_weapon_energy": re.compile(
                r"^\$Max Weapon Energy:\s*([\d\.]+)$", re.IGNORECASE
            ),
            "afterburner_fuel": re.compile(
                r"^\$Afterburner Fuel Capacity:\s*([\d\.]+)$", re.IGNORECASE
            ),
            # Acceleration properties
            "forward_accel": re.compile(
                r"^\$Forward accel:\s*([\d\.]+)$", re.IGNORECASE
            ),
            "forward_decel": re.compile(
                r"^\$Forward decel:\s*([\d\.]+)$", re.IGNORECASE
            ),
            "slide_accel": re.compile(
                r"^\$Slide accel:\s*([\d\.]+)$", re.IGNORECASE
            ),
            "slide_decel": re.compile(
                r"^\$Slide decel:\s*([\d\.]+)$", re.IGNORECASE
            ),
            # Rotational physics properties
            "rotation_time": re.compile(
                r"^\$Rotation time:\s*([\d\.\-\s,]+)$", re.IGNORECASE
            ),
            "rotation_accel": re.compile(
                r"^\$Rotation accel:\s*([\d\.\-\s,]+)$", re.IGNORECASE
            ),
            "rotation_decel": re.compile(
                r"^\$Rotation decel:\s*([\d\.\-\s,]+)$", re.IGNORECASE
            ),
        }
        
        # 3D Models and geometry
        model_patterns = {
            "model_file": re.compile(r"^\$Model file:\s*(.+)$", re.IGNORECASE),
            "pof_file": re.compile(r"^\$POF file:\s*(.+)$", re.IGNORECASE),
            "pof_target_file": re.compile(
                r"^\$POF target file:\s*(.+)$", re.IGNORECASE
            ),
            "cockpit_pof_file": re.compile(
                r"^\$Cockpit POF file:\s*(.+)$", re.IGNORECASE
            ),
            "detail_distance": re.compile(
                r"^\$Detail distance:\s*([\d\.]+)$", re.IGNORECASE
            ),
        }
        
        # Audio assets
        audio_patterns = {
            "warpin_start_sound": re.compile(
                r"^\$Warpin Start Sound:\s*(.+)$", re.IGNORECASE
            ),
            "warpin_end_sound": re.compile(
                r"^\$Warpin End Sound:\s*(.+)$", re.IGNORECASE
            ),
            "warpout_start_sound": re.compile(
                r"^\$Warpout Start Sound:\s*(.+)$", re.IGNORECASE
            ),
            "warpout_end_sound": re.compile(
                r"^\$Warpout End Sound:\s*(.+)$", re.IGNORECASE
            ),
            "engine_sound": re.compile(r"^\$EngineSnd:\s*(.+)$", re.IGNORECASE),
            "alive_sound": re.compile(r"^\$AliveSnd:\s*(.+)$", re.IGNORECASE),
            "dead_sound": re.compile(r"^\$DeadSnd:\s*(.+)$", re.IGNORECASE),
            "rotation_sound": re.compile(r"^\$RotationSnd:\s*(.+)$", re.IGNORECASE),
            "turret_base_rotation_sound": re.compile(
                r"^\$Turret Base RotationSnd:\s*(.+)$", re.IGNORECASE
            ),
            "turret_gun_rotation_sound": re.compile(
                r"^\$Turret Gun RotationSnd:\s*(.+)$", re.IGNORECASE
            ),
        }
        
        # Animation and effects
        animation_patterns = {
            "warpin_animation": re.compile(
                r"^\$Warpin animation:\s*(.+)$", re.IGNORECASE
            ),
            "warpout_animation": re.compile(
                r"^\$Warpout animation:\s*(.+)$", re.IGNORECASE
            ),
            "explosion_animations": re.compile(
                r"^\$Explosion Animations:\s*(.+)$", re.IGNORECASE
            ),
            "shockwave_model": re.compile(
                r"^\$Shockwave model:\s*(.+)$", re.IGNORECASE
            ),
            "selection_effect": re.compile(
                r"^\$Selection Effect:\s*(.+)$", re.IGNORECASE
            ),
        }
        
        # Thruster configuration and effects
        thruster_patterns = {
            "thruster_flame": re.compile(
                r"^\$Thruster flame effect:\s*(.+)$", re.IGNORECASE
            ),
            "thruster_glow": re.compile(
                r"^\$Thruster glow effect:\s*(.+)$", re.IGNORECASE
            ),
            "thruster_start_sound": re.compile(r"^\+StartSnd:\s*(.+)$", re.IGNORECASE),
            "thruster_loop_sound": re.compile(r"^\+LoopSnd:\s*(.+)$", re.IGNORECASE),
            "thruster_stop_sound": re.compile(r"^\+StopSnd:\s*(.+)$", re.IGNORECASE),
        }
        
        # UI and HUD assets
        ui_patterns = {
            "shield_icon": re.compile(r"^\$Shield_icon:\s*(.+)$", re.IGNORECASE),
            "ship_icon": re.compile(r"^\$Ship_icon:\s*(.+)$", re.IGNORECASE),
            "ship_anim": re.compile(r"^\$Ship_anim:\s*(.+)$", re.IGNORECASE),
            "ship_overhead": re.compile(r"^\$Ship_overhead:\s*(.+)$", re.IGNORECASE),
        }
        
        # Camera and viewport
        camera_patterns = {
            "closeup_pos": re.compile(r"^\$Closeup_pos:\s*(.+)$", re.IGNORECASE),
            "closeup_zoom": re.compile(r"^\$Closeup_zoom:\s*(.+)$", re.IGNORECASE),
        }
        
        # Thruster configuration factors
        thruster_config_patterns = {
            "thruster_radius_factor": re.compile(r"^\$Thruster.*Radius factor:\s*(.+)$", re.IGNORECASE),
            "thruster_length_factor": re.compile(r"^\$Thruster.*Length factor:\s*(.+)$", re.IGNORECASE),
        }
        
        # Subsystem definitions
        subsystem_patterns = {
            "subsystem": re.compile(r"^\$Subsystem:\s*(.+)$", re.IGNORECASE),
            "alt_subsystem_name": re.compile(r"^\s*\$Alt Subsystem Name:\s*(.+)$", re.IGNORECASE),
            "alt_damage_popup_name": re.compile(r"^\s*\$Alt Damage Popup Subsystem Name:\s*(.+)$", re.IGNORECASE),
        }
        
        # Weapon bank allocations
        weapon_patterns = {
            "allowed_pbanks": re.compile(r"^\$Allowed PBanks:\s*(.+)$", re.IGNORECASE),
            "allowed_sbanks": re.compile(r"^\$Allowed SBanks:\s*(.+)$", re.IGNORECASE),
            "default_pbanks": re.compile(r"^\$Default PBanks:\s*(.+)$", re.IGNORECASE),
            "default_sbanks": re.compile(r"^\$Default SBanks:\s*(.+)$", re.IGNORECASE),
            "sbank_capacity": re.compile(r"^\$SBank Capacity:\s*(.+)$", re.IGNORECASE),
            # Dogfight mode weapon banks
            "allowed_dogfight_pbanks": re.compile(r"^\$Allowed Dogfight PBanks:\s*(.+)$", re.IGNORECASE),
            "allowed_dogfight_sbanks": re.compile(r"^\$Allowed Dogfight SBanks:\s*(.+)$", re.IGNORECASE),
            # Weapon energy properties
            "weapon_regeneration_rate": re.compile(r"^\$Weapon Regeneration Rate:\s*([\d\.]+)$", re.IGNORECASE),
            "max_weapon_energy": re.compile(r"^\$Max Weapon Eng:\s*([\d\.]+)$", re.IGNORECASE),
        }
        
        # Tech database assets
        tech_patterns = {
            "tech_model": re.compile(r"^\$Tech Model:\s*(.+)$", re.IGNORECASE),
            "tech_anim": re.compile(r"^\$Tech Anim:\s*(.+)$", re.IGNORECASE),
            "tech_image": re.compile(r"^\$Tech Image:\s*(.+)$", re.IGNORECASE),
        }
        
        # Texture modifications
        texture_patterns = {
            "texture_replace": re.compile(
                r"^\$Texture Replace:\s*(.+)$", re.IGNORECASE
            ),
        }
        
        # Section termination
        section_patterns = {
            "section_end": re.compile(r"^#End\s*$", re.IGNORECASE),
        }
        
        # Combine all patterns
        all_patterns = {}
        all_patterns.update(basic_patterns)
        all_patterns.update(engine_wash_patterns)
        all_patterns.update(physics_patterns)
        all_patterns.update(model_patterns)
        all_patterns.update(audio_patterns)
        all_patterns.update(animation_patterns)
        all_patterns.update(thruster_patterns)
        all_patterns.update(ui_patterns)
        all_patterns.update(camera_patterns)
        all_patterns.update(thruster_config_patterns)
        all_patterns.update(subsystem_patterns)
        all_patterns.update(weapon_patterns)
        all_patterns.update(tech_patterns)
        all_patterns.update(texture_patterns)
        all_patterns.update(section_patterns)
        
        return all_patterns

    def get_table_type(self) -> TableType:
        return TableType.SHIPS

    def parse_table(self, state: ParseState) -> List[Dict[str, Any]]:
        """Parse the entire ships.tbl file, handling all sections"""
        entries = []
        
        # First, skip to the #Ship Classes section
        while state.has_more_lines():
            line = state.peek_line()
            if not line or self._should_skip_line(line, state):
                state.skip_line()
                continue
                
            # Look for the Ship Classes section
            if "#Ship Classes" in line:
                state.skip_line()  # Skip the section header
                break
            else:
                state.skip_line()
        
        # Now parse all ship class entries
        while state.has_more_lines():
            line = state.peek_line()
            if not line or self._should_skip_line(line, state):
                state.skip_line()
                continue

            # Check for ship start
            if self._parse_patterns["ship_start"].match(line.strip()):
                entry = self.parse_entry(state)
                if entry:
                    entry["entry_type"] = "ship"
                    entries.append(entry)
            # Check for section end - this indicates the end of Ship Classes
            elif self._parse_patterns["section_end"].match(line.strip()):
                state.skip_line()
                break
            else:
                state.skip_line()
        
        return entries

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
            match = self._parse_patterns["ship_start"].match(line)
            if match:
                if "name" in ship_data:
                    # We already have a ship entry, this is the start of the next one
                    state.current_line -= 1  # Rewind so next parse can catch this
                    return ship_data
                ship_data["name"] = match.group(1).strip()
                continue

            # Parse ship properties
            if "name" in ship_data:  # Only parse if we're in a ship section
                if self._parse_ship_property(line, ship_data):
                    # Capture asset relationships for asset mapping
                    self._capture_asset_relationships(line, ship_data)
                    continue

                # Check for section end
                if self._parse_patterns["section_end"].match(line):
                    # Finalize asset mapping for this ship
                    self._finalize_ship_asset_mapping(ship_data)
                    return ship_data if ship_data else None

                # Check for start of next ship entry (dash comment line pattern)
                if line.startswith(';---') and state.has_more_lines():
                    # This is a separator line between ships, return current entry
                    return ship_data if ship_data else None

        return ship_data if ship_data else None

    def _parse_engine_wash_entry(self, state: ParseState) -> Optional[Dict[str, Any]]:
        """Parse a single engine wash entry from the table"""
        wash_data = {}

        while state.has_more_lines():
            line = state.next_line()
            if not line:
                continue

            line = line.strip()
            if not line or self._should_skip_line(line, state):
                continue

            # Check for engine wash start
            match = self._parse_patterns["engine_wash_start"].match(line)
            if match:
                if "name" in wash_data:
                    # We already have an entry, this is the start of the next one
                    state.current_line -= 1  # Rewind so next parse can catch this
                    return wash_data
                wash_data["name"] = match.group(1).strip()
                continue

            # Parse engine wash properties
            if "name" in wash_data:  # Only parse if we're in an engine wash section
                if self._parse_engine_wash_property(line, wash_data):
                    continue

                # Check for section end
                if self._parse_patterns["section_end"].match(line):
                    return wash_data if wash_data else None

                # If we reach here, it's an unexpected line - assume end of entry
                state.current_line -= 1  # Rewind so this line can be processed again
                return wash_data

        return wash_data if wash_data else None

    def _parse_engine_wash_property(self, line: str, wash_data: Dict[str, Any]) -> bool:
        """Parse a single engine wash property line"""
        engine_wash_properties = ["angle", "radius_mult", "length", "intensity"]

        for property_name in engine_wash_properties:
            pattern = self._parse_patterns.get(property_name)
            if pattern:
                match = pattern.match(line)
                if match:
                    value = match.group(1).strip()
                    
                    # Strip inline comments (semicolons)
                    if ";" in value:
                        value = value.split(";", 1)[0].strip()
                    
                    # Parse numeric values
                    wash_data[property_name] = self.parse_value(value, float)
                    return True

        return False

    def _parse_ship_property(self, line: str, ship_data: Dict[str, Any]) -> bool:
        """Parse a single ship property line, organized by property categories"""
        for property_name, pattern in self._parse_patterns.items():
            if property_name in ["ship_start", "section_end"]:
                continue

            match = pattern.match(line)
            if match:
                value = match.group(1).strip()
                
                # Strip inline comments (semicolons)
                if ";" in value:
                    value = value.split(";", 1)[0].strip()

                # Handle special parsing for specific properties by category
                if property_name == "max_velocity":
                    ship_data["max_velocity"] = self._parse_velocity_vector(value)
                elif property_name in [
                    "hitpoints",
                    "mass",
                    "density",
                    "max_shield",
                    "power_output",
                    "afterburner_fuel",
                    "detail_distance",
                    "closeup_zoom",
                    "thruster_radius_factor",
                    "thruster_length_factor",
                    "weapon_regeneration_rate",
                    "max_weapon_energy",
                ]:
                    # All numeric float properties
                    ship_data[property_name] = self.parse_value(value, float)
                elif property_name == "afterburner_velocity":
                    # Parse afterburner velocity as a single float value
                    ship_data[property_name] = self.parse_value(value, float)
                elif property_name == "closeup_pos":
                    ship_data["closeup_pos"] = self._parse_position_vector(value)
                elif property_name in [
                    "forward_accel",
                    "forward_decel",
                    "slide_accel",
                    "slide_decel",
                ]:
                    # Parse acceleration properties
                    ship_data[property_name] = self.parse_value(value, float)
                elif property_name in [
                    "rotation_time",
                    "rotation_accel",
                    "rotation_decel",
                ]:
                    # Parse rotation properties as vectors
                    ship_data[property_name] = self._parse_rotation_vector(value)
                elif property_name in ["allowed_pbanks", "allowed_sbanks", "default_pbanks", "default_sbanks", "allowed_dogfight_pbanks", "allowed_dogfight_sbanks"]:
                    # Handle weapon bank lists - parse as string lists
                    ship_data[property_name] = self._parse_weapon_banks(value)
                elif property_name == "sbank_capacity":
                    # Handle secondary bank capacity as integer list
                    ship_data["sbank_capacity"] = self._parse_integer_list(value)
                else:
                    # Default string properties
                    ship_data[property_name] = value

                return True

        return False

    def _parse_velocity_vector(self, velocity_str: str) -> Dict[str, float]:
        """Parse velocity vector string like '65.0, 75.0, 65.0'"""
        try:
            components = [float(x.strip()) for x in velocity_str.split(",")]
            if len(components) == 3:
                return {
                    "forward": components[0],
                    "reverse": components[1],
                    "side": components[2],
                }
            else:
                # Single value for all directions
                value = components[0] if components else 0.0
                return {"forward": value, "reverse": value, "side": value}
        except (ValueError, IndexError):
            self.logger.warning(f"Failed to parse velocity: {velocity_str}")
            return {"forward": 0.0, "reverse": 0.0, "side": 0.0}

    def _parse_position_vector(self, position_str: str) -> Dict[str, float]:
        """Parse position vector string like '0.0, 0.0, -14.94688'"""
        try:
            # Strip inline comments (semicolons)
            if ";" in position_str:
                position_str = position_str.split(";", 1)[0].strip()
            
            components = [float(x.strip()) for x in position_str.split(",")]
            if len(components) == 3:
                return {
                    "x": components[0],
                    "y": components[1],
                    "z": components[2],
                }
            else:
                self.logger.warning(f"Invalid position format: {position_str}")
                return {"x": 0.0, "y": 0.0, "z": 0.0}
        except (ValueError, IndexError):
            self.logger.warning(f"Failed to parse position: {position_str}")
            return {"x": 0.0, "y": 0.0, "z": 0.0}

    def _parse_acceleration_vector(self, accel_str: str) -> Dict[str, float]:
        """Parse acceleration vector string like '5.0, 5.0, 5.0'"""
        try:
            components = [float(x.strip()) for x in accel_str.split(",")]
            if len(components) == 3:
                return {
                    "forward": components[0],
                    "reverse": components[1],
                    "side": components[2],
                }
            else:
                # Single value for all directions
                value = components[0] if components else 0.0
                return {"forward": value, "reverse": value, "side": value}
        except (ValueError, IndexError):
            self.logger.warning(f"Failed to parse acceleration: {accel_str}")
            return {"forward": 0.0, "reverse": 0.0, "side": 0.0}

    def _parse_rotation_vector(self, rotation_str: str) -> Dict[str, float]:
        """Parse rotation vector string like '3.0, 3.0, 3.0' for pitch, bank, heading"""
        try:
            # Strip inline comments (semicolons)
            if ";" in rotation_str:
                rotation_str = rotation_str.split(";", 1)[0].strip()
            
            components = [float(x.strip()) for x in rotation_str.split(",")]
            if len(components) == 3:
                return {
                    "pitch": components[0],
                    "bank": components[1],
                    "heading": components[2],
                }
            elif len(components) == 1:
                # Single value for all directions
                value = components[0]
                return {"pitch": value, "bank": value, "heading": value}
            else:
                self.logger.warning(f"Invalid rotation format: {rotation_str}")
                return {"pitch": 0.0, "bank": 0.0, "heading": 0.0}
        except (ValueError, IndexError):
            self.logger.warning(f"Failed to parse rotation: {rotation_str}")
            return {"pitch": 0.0, "bank": 0.0, "heading": 0.0}

    def _parse_weapon_banks(self, bank_str: str) -> List[List[str]]:
        """Parse weapon bank lists like '(\"Laser\") (\"Ion\")' or '(\"Pilum FF\" \"Spiculum IR\")'"""
        try:
            # Remove outer parentheses and split by individual bank groups
            bank_str = bank_str.strip()
            if not bank_str.startswith("(") or not bank_str.endswith(")"):
                return []
            
            # Extract individual bank groups
            banks = []
            current_bank = []
            in_quotes = False
            current_token = ""
            
            for char in bank_str[1:-1]:  # Skip outer parentheses
                if char == '"':
                    in_quotes = not in_quotes
                    if not in_quotes and current_token:
                        current_bank.append(current_token)
                        current_token = ""
                elif char == ')' and not in_quotes:
                    if current_bank:
                        banks.append(current_bank)
                        current_bank = []
                elif char not in ' ()' or in_quotes:
                    current_token += char
            
            # Add the last bank if any
            if current_bank:
                banks.append(current_bank)
            
            return banks
            
        except Exception as e:
            self.logger.warning(f"Failed to parse weapon banks: {bank_str}, error: {e}")
            return []

    def _parse_integer_list(self, list_str: str) -> List[int]:
        """Parse integer list like '(20, 20, 20, 20)'"""
        try:
            # Remove parentheses and split by commas
            list_str = list_str.strip().strip("()")
            if not list_str:
                return []
            
            return [int(x.strip()) for x in list_str.split(",") if x.strip()]
        except (ValueError, IndexError):
            self.logger.warning(f"Failed to parse integer list: {list_str}")
            return []

    def validate_entry(self, entry: Dict[str, Any]) -> bool:
        """Validate a parsed ship entry with organized validation categories"""
        # Validate required fields
        required_fields = ["name"]
        for field in required_fields:
            if field not in entry:
                self.logger.warning(f"Ship entry missing required field: {field}")
                return False

        # Validate numeric fields by category
        physics_numeric_fields = [
            "hitpoints",
            "mass",
            "density",
            "max_shield",
            "power_output",
            "afterburner_fuel",
        ]
        
        weapon_numeric_fields = [
            "weapon_regeneration_rate",
            "max_weapon_energy",
        ]
        
        acceleration_numeric_fields = [
            "forward_accel",
            "forward_decel",
            "slide_accel",
            "slide_decel",
        ]
        
        configuration_numeric_fields = [
            "detail_distance",
            "closeup_zoom",
            "thruster_radius_factor",
            "thruster_length_factor",
        ]
        
        all_numeric_fields = physics_numeric_fields + weapon_numeric_fields + acceleration_numeric_fields + configuration_numeric_fields
        
        for field in all_numeric_fields:
            if field in entry and not isinstance(entry[field], (int, float)):
                self.logger.warning(f"Ship {entry['name']}: Invalid {field} value")
                return False

        return True

    def convert_to_godot_resources(
        self, entries: List[Dict[str, Any]], output_dir: str
    ) -> Dict[str, Any]:
        """Convert parsed ship entries to Godot .tres resource files"""
        from ..resource_generators.ship_class_generator import ShipClassGenerator

        # Create resource generator
        generator = ShipClassGenerator(output_dir)

        # Generate ship resources
        resource_files = generator.generate_ship_resources(entries)

        return {
            "conversion_type": "ship_resources",
            "resource_files": resource_files,
            "ship_count": len(entries),
            "output_directory": output_dir,
        }

    def convert_to_godot_resource(
        self, entries: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Legacy method - now redirects to resource generation"""
        # For compatibility - generate resources in default location
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            return self.convert_to_godot_resources(entries, temp_dir)

    # ========== ASSET MAPPING INTEGRATION ==========

    def _capture_asset_relationships(
        self, line: str, ship_data: Dict[str, Any]
    ) -> None:
        """Capture asset relationships from parsed ship properties, organized by asset categories"""
        # Asset property patterns that should be captured for mapping, organized by category
        model_assets = [
            "model_file",
            "pof_file",
            "pof_target_file",
            "cockpit_pof_file",
        ]
        
        audio_assets = [
            "warpin_start_sound",
            "warpin_end_sound",
            "warpout_start_sound",
            "warpout_end_sound",
            "engine_sound",
            "alive_sound",
            "dead_sound",
            "rotation_sound",
            "turret_base_rotation_sound",
            "turret_gun_rotation_sound",
            "thruster_start_sound",
            "thruster_loop_sound",
            "thruster_stop_sound",
        ]
        
        animation_assets = [
            "warpin_animation",
            "warpout_animation",
            "explosion_animations",
            "shockwave_model",
            "selection_effect",
            "thruster_flame",
            "thruster_glow",
        ]
        
        ui_assets = [
            "shield_icon",
            "ship_icon",
            "ship_anim",
            "ship_overhead",
        ]
        
        tech_assets = [
            "tech_model",
            "tech_anim",
            "tech_image",
        ]
        
        texture_assets = [
            "texture_replace",
        ]
        
        # Configuration assets (not traditional assets but still tracked)
        configuration_assets = [
            "closeup_pos",
            "closeup_zoom",
            "thruster_radius_factor",
            "thruster_length_factor",
        ]
        
        # Weapon configuration assets
        weapon_assets = [
            "allowed_pbanks",
            "allowed_sbanks",
            "default_pbanks",
            "default_sbanks",
            "sbank_capacity",
            "allowed_dogfight_pbanks",
            "allowed_dogfight_sbanks",
            "weapon_regeneration_rate",
            "max_weapon_energy",
        ]
        
        # Combine all asset properties
        all_asset_properties = (
            model_assets + audio_assets + animation_assets + ui_assets + 
            tech_assets + texture_assets + configuration_assets + weapon_assets
        )

        for prop_name in all_asset_properties:
            pattern = self._parse_patterns.get(prop_name)
            if pattern:
                match = pattern.match(line)
                if match:
                    asset_path = match.group(1).strip()
                    if asset_path:
                        # Store in asset registry
                        ship_name = ship_data.get("name", "unknown")
                        if ship_name not in self._asset_registry:
                            self._asset_registry[ship_name] = []
                        self._asset_registry[ship_name].append(
                            {
                                "property": prop_name,
                                "asset_path": asset_path,
                                "asset_type": self._get_asset_type(
                                    prop_name, asset_path
                                ),
                            }
                        )

    def _finalize_ship_asset_mapping(self, ship_data: Dict[str, Any]) -> None:
        """Finalize asset mapping for a completed ship entry"""
        ship_name = ship_data.get("name")
        if not ship_name or ship_name not in self._asset_registry:
            return

        # Create relationship mapping for this ship
        self._relationship_mappings[ship_name] = {
            "entity_type": "ship",
            "assets": self._asset_registry[ship_name],
            "primary_asset": self._get_primary_asset(ship_data),
            "related_assets": self._asset_registry[ship_name],
        }

        # Update statistics
        self._entries_processed += 1

    def _get_asset_type(self, property_name: str, asset_path: str) -> str:
        """Determine asset type based on property name and path"""
        # More specific categorization based on property name
        if any(prop in property_name.lower() for prop in ["sound", "snd"]):
            return "audio"
        elif any(prop in property_name.lower() for prop in ["model", "pof"]):
            return "model"
        elif any(prop in property_name.lower() for prop in ["animation", "anim", "effect", "flame", "glow"]):
            return "animation"
        elif any(prop in property_name.lower() for prop in ["icon", "image", "overhead", "tech"]):
            return "texture"
        else:
            # Infer from file extension
            if asset_path.lower().endswith((".wav", ".ogg", ".mp3")):
                return "audio"
            elif asset_path.lower().endswith((".pof", ".obj", ".gltf", ".glb")):
                return "model"
            elif asset_path.lower().endswith((".dds", ".png", ".jpg", ".jpeg", ".tga")):
                return "texture"
            else:
                return "unknown"

    def _get_primary_asset(self, ship_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get the primary asset (main model) for the ship"""
        primary_asset_props = ["pof_file", "model_file"]

        for prop in primary_asset_props:
            asset_path = ship_data.get(prop)
            if asset_path:
                return {
                    "property": prop,
                    "asset_path": asset_path,
                    "asset_type": "model",
                }
        return None
