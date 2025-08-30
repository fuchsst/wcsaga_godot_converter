#!/usr/bin/env python3
"""
Ship Class Resource Generator

Generates .tres ShipClass resource files from ships.tbl data.
Uses existing BaseShip and ShipClass architecture - no custom logic.
"""

import os
from typing import Any, Dict, List


class ShipClassGenerator:
    """Generates ShipClass .tres resource files from parsed ship table data"""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        # Remove the old ships_dir - we'll use feature-based organization
        self.ships_dir = None

    def generate_ship_resources(self, ship_entries: List[Dict[str, Any]]) -> List[str]:
        """Generate .tres resource files for all ship entries"""
        generated_files = []

        for ship in ship_entries:
            resource_file = self._generate_single_ship_resource(ship)
            if resource_file:
                generated_files.append(resource_file)

        # Generate ship registry file
        registry_file = self._generate_ship_registry(ship_entries)
        if registry_file:
            generated_files.append(registry_file)

        return generated_files

    def _generate_single_ship_resource(self, ship: Dict[str, Any]) -> str:
        """Generate a single ShipClass .tres resource file using feature-based organization"""
        ship_name = ship.get("name", "unknown_ship")
        safe_name = self._sanitize_filename(ship_name)

        # Determine faction and ship type for directory structure
        faction = self._determine_faction(ship_name)
        ship_category = self._determine_ship_category(ship_name)
        
        # Create feature-based directory structure
        # /features/fighters/{faction}/{ship_name}/{ship_name}.tres for fighters and bombers
        # /features/capital_ships/{faction}/{ship_name}/{ship_name}.tres for capital ships
        if ship_category in ["fighter", "bomber", "interceptor", "stealth", "corvette"]:
            feature_dir = os.path.join(self.output_dir, "features", "fighters", faction, safe_name)
        else:
            feature_dir = os.path.join(self.output_dir, "features", "capital_ships", faction, safe_name)
        
        os.makedirs(feature_dir, exist_ok=True)

        # Create .tres resource content
        resource_content = self._create_ship_resource_content(ship)

        # Write resource file
        output_path = os.path.join(feature_dir, f"{safe_name}.tres")

        try:
            with open(output_path, "w") as f:
                f.write(resource_content)
            print(f"Generated ship resource: {output_path}")
            return output_path
        except Exception as e:
            print(f"Error writing ship resource {output_path}: {e}")
            return ""

    def _create_ship_resource_content(self, ship: Dict[str, Any]) -> str:
        """Create .tres resource content for ShipClass with complete ship data"""
        
        # Extract ship properties with defaults
        ship_name = ship.get("name", "Unknown Ship")
        
        # Handle max_velocity which can be a dictionary or single value
        max_velocity_data = ship.get("max_velocity", 75.0)
        if isinstance(max_velocity_data, dict):
            # Use forward velocity from dictionary
            max_velocity = max_velocity_data.get("forward", 75.0)
        else:
            # Use single value directly
            max_velocity = max_velocity_data
            
        max_hull_strength = ship.get("hitpoints", 100.0)  # hitpoints in source data
        max_shield_strength = ship.get("max_shield", 50.0)
        mass = ship.get("mass", 1000.0)
        
        # Physics properties
        density = ship.get("density", 1.0)
        power_output = ship.get("power_output", 100.0)
        afterburner_fuel = ship.get("afterburner_fuel", 500.0)
        max_weapon_energy = ship.get("max_weapon_energy", 100.0)
        weapon_regeneration_rate = ship.get("weapon_regeneration_rate", 0.1)
        
        # Acceleration properties
        forward_accel = ship.get("forward_accel", 5.0)
        forward_decel = ship.get("forward_decel", 4.0)
        slide_accel = ship.get("slide_accel", 3.0)
        slide_decel = ship.get("slide_decel", 2.0)
        
        # Rotation properties
        rotation_time = ship.get("rotation_time", {"pitch": 3.0, "bank": 3.0, "heading": 3.0})
        if isinstance(rotation_time, dict):
            pitch_time = rotation_time.get("pitch", 3.0)
            bank_time = rotation_time.get("bank", 3.0)
            heading_time = rotation_time.get("heading", 3.0)
        else:
            pitch_time = bank_time = heading_time = rotation_time
            
        # Determine ship type
        ship_type = self._determine_ship_type(ship_name)

        # Extract actual asset paths from ship data
        pof_file = ship.get("pof_file", ship.get("model_file", ""))
        pof_target_file = ship.get("pof_target_file", "")
        cockpit_pof_file = ship.get("cockpit_pof_file", "")
        ship_icon = ship.get("ship_icon", "")
        ship_anim = ship.get("ship_anim", "")
        ship_overhead = ship.get("ship_overhead", "")
        tech_model = ship.get("tech_model", "")
        tech_anim = ship.get("tech_anim", "")
        tech_image = ship.get("tech_image", "")
        thruster_flame = ship.get("thruster_flame", "")
        thruster_glow = ship.get("thruster_glow", "")
        
        # Audio assets
        engine_sound = ship.get("engine_sound", "")
        alive_sound = ship.get("alive_sound", "")
        dead_sound = ship.get("dead_sound", "")
        warpin_start_sound = ship.get("warpin_start_sound", "")
        warpin_end_sound = ship.get("warpin_end_sound", "")
        warpout_start_sound = ship.get("warpout_start_sound", "")
        warpout_end_sound = ship.get("warpout_end_sound", "")
        rotation_sound = ship.get("rotation_sound", "")
        turret_base_rotation_sound = ship.get("turret_base_rotation_sound", "")
        turret_gun_rotation_sound = ship.get("turret_gun_rotation_sound", "")
        
        # Weapon bank configurations
        allowed_pbanks = ship.get("allowed_pbanks", [])
        allowed_sbanks = ship.get("allowed_sbanks", [])
        default_pbanks = ship.get("default_pbanks", [])
        default_sbanks = ship.get("default_sbanks", [])
        sbank_capacity = ship.get("sbank_capacity", [])
        allowed_dogfight_pbanks = ship.get("allowed_dogfight_pbanks", [])
        allowed_dogfight_sbanks = ship.get("allowed_dogfight_sbanks", [])
        
        # Convert weapon banks to Godot format
        allowed_pbanks_str = self._format_weapon_banks(allowed_pbanks)
        allowed_sbanks_str = self._format_weapon_banks(allowed_sbanks)
        default_pbanks_str = self._format_weapon_banks(default_pbanks)
        default_sbanks_str = self._format_weapon_banks(default_sbanks)
        sbank_capacity_str = self._format_integer_list(sbank_capacity)
        dogfight_pbanks_str = self._format_weapon_banks(allowed_dogfight_pbanks)
        dogfight_sbanks_str = self._format_weapon_banks(allowed_dogfight_sbanks)

        # Convert to Godot resource paths with fallbacks
        safe_name = self._sanitize_filename(ship_name)
        faction = self._determine_faction(ship_name)

        # Use actual POF file path when available
        if pof_file:
            model_path = f"res://assets/models/ships/{pof_file}"
        else:
            model_path = f"res://assets/models/ships/{faction}/{safe_name}.glb"

        # Use ship icon when available
        if ship_icon:
            icon_path = f"res://assets/ui/ships/{ship_icon}"
        else:
            icon_path = f"res://assets/ui/ships/{safe_name}_icon.png"

        # Generate texture path (fallback only)
        texture_path = f"res://assets/textures/ships/{faction}/{safe_name}_diffuse.png"

        # Create .tres content
        resource_content = f"""[gd_resource type="ShipClass" script_class="ShipClass" load_steps=2 format=3]

[ext_resource type="Script" path="res://addons/wcs_asset_core/resources/ship/ship_class.gd" id="1"]

[resource]
script = ExtResource("1")
class_name = "{ship_name}"
display_name = "{ship_name}"
ship_type = {ship_type}
mass = {mass}
density = {density}
power_output = {power_output}
max_velocity = {max_velocity}
max_afterburner_velocity = {max_velocity * 1.5}
max_hull_strength = {max_hull_strength}
max_shield_strength = {max_shield_strength}
max_weapon_energy = {max_weapon_energy}
weapon_regeneration_rate = {weapon_regeneration_rate}
afterburner_fuel_capacity = {afterburner_fuel}
forward_acceleration = {forward_accel}
forward_deceleration = {forward_decel}
slide_acceleration = {slide_accel}
slide_deceleration = {slide_decel}
pitch_rotation_time = {pitch_time}
bank_rotation_time = {bank_time}
heading_rotation_time = {heading_time}
model_path = "{model_path}"
texture_path = "{texture_path}"
ship_scene_path = "res://scenes/ships/{faction}/{safe_name}.tscn"
hardpoint_configuration = {self._format_hardpoints(ship)}
subsystem_definitions = {self._format_subsystems(ship)}

# Weapon Bank Configuration
allowed_primary_banks = {allowed_pbanks_str}
allowed_secondary_banks = {allowed_sbanks_str}
default_primary_banks = {default_pbanks_str}
default_secondary_banks = {default_sbanks_str}
secondary_bank_capacities = {sbank_capacity_str}
dogfight_allowed_primary_banks = {dogfight_pbanks_str}
dogfight_allowed_secondary_banks = {dogfight_sbanks_str}

# Asset paths from extracted table data
icon_path = "{icon_path}"
pof_target_file_path = "{f'res://assets/models/ships/{pof_target_file}' if pof_target_file else ''}"
cockpit_pof_file_path = "{f'res://assets/models/ships/{cockpit_pof_file}' if cockpit_pof_file else ''}"
ship_anim_path = "{f'res://assets/animations/ships/{ship_anim}' if ship_anim else ''}"
ship_overhead_path = "{f'res://assets/ui/ships/{ship_overhead}' if ship_overhead else ''}"
tech_model_path = "{f'res://assets/models/tech/{tech_model}' if tech_model else ''}"
tech_anim_path = "{f'res://assets/animations/tech/{tech_anim}' if tech_anim else ''}"
tech_image_path = "{f'res://assets/images/tech/{tech_image}' if tech_image else ''}"
thruster_flame_effect_path = "{f'res://effects/ships/{thruster_flame}' if thruster_flame else ''}"
thruster_glow_effect_path = "{f'res://effects/ships/{thruster_glow}' if thruster_glow else ''}"

# Audio asset paths
engine_sound_path = "{f'res://assets/audio/ships/{engine_sound}' if engine_sound else ''}"
alive_sound_path = "{f'res://assets/audio/ships/{alive_sound}' if alive_sound else ''}"
dead_sound_path = "{f'res://assets/audio/ships/{dead_sound}' if dead_sound else ''}"
warpin_start_sound_path = "{f'res://assets/audio/ships/{warpin_start_sound}' if warpin_start_sound else ''}"
warpin_end_sound_path = "{f'res://assets/audio/ships/{warpin_end_sound}' if warpin_end_sound else ''}"
warpout_start_sound_path = "{f'res://assets/audio/ships/{warpout_start_sound}' if warpout_start_sound else ''}"
warpout_end_sound_path = "{f'res://assets/audio/ships/{warpout_end_sound}' if warpout_end_sound else ''}"
rotation_sound_path = "{f'res://assets/audio/ships/{rotation_sound}' if rotation_sound else ''}"
turret_base_rotation_sound_path = "{f'res://assets/audio/ships/{turret_base_rotation_sound}' if turret_base_rotation_sound else ''}"
turret_gun_rotation_sound_path = "{f'res://assets/audio/ships/{turret_gun_rotation_sound}' if turret_gun_rotation_sound else ''}"
"""
        return resource_content

    def _determine_ship_type(self, ship_name: str) -> str:
        """Determine ship type constant from name"""
        name_lower = ship_name.lower()

        if any(word in name_lower for word in ["fighter", "interceptor", "stealth"]):
            return "ShipTypes.Type.FIGHTER"
        elif any(word in name_lower for word in ["bomber", "assault"]):
            return "ShipTypes.Type.BOMBER"
        elif any(word in name_lower for word in ["corvette", "gunboat"]):
            return "ShipTypes.Type.CORVETTE"
        elif any(word in name_lower for word in ["cruiser", "destroyer"]):
            return "ShipTypes.Type.CRUISER"
        elif any(word in name_lower for word in ["capital", "dreadnought", "carrier"]):
            return "ShipTypes.Type.CAPITAL"
        elif any(word in name_lower for word in ["transport", "cargo", "freighter"]):
            return "ShipTypes.Type.TRANSPORT"
        else:
            return "ShipTypes.Type.FIGHTER"  # Default

    def _determine_faction(self, ship_name: str) -> str:
        """Determine faction folder from ship name"""
        name_lower = ship_name.lower()

        # Terran prefixes
        if any(
            prefix in name_lower
            for prefix in ["gtf", "gtb", "gtc", "gtd", "gtt", "gta"]
        ):
            return "terran"
        # Vasudan prefixes
        elif any(
            prefix in name_lower for prefix in ["pva", "pvf", "pvb", "pvc", "pvd"]
        ):
            return "vasudan"
        # Shivan prefixes
        elif any(prefix in name_lower for prefix in ["sf", "sb", "sc", "sd", "sj"]):
            return "shivan"
        # Generic/Other
        else:
            return "other"

    def _determine_ship_category(self, ship_name: str) -> str:
        """Determine ship category for directory structure"""
        name_lower = ship_name.lower()

        # Check for specific ship name patterns first
        if "gtb" in name_lower or "pvb" in name_lower or "sb" in name_lower:
            return "bomber"
        elif "gtd" in name_lower or "pvd" in name_lower or "sd" in name_lower:
            return "capital"
        elif "gtc" in name_lower or "pvc" in name_lower or "sc" in name_lower:
            return "cruiser"
        elif any(word in name_lower for word in ["fighter", "interceptor", "stealth"]):
            return "fighter"
        elif any(word in name_lower for word in ["bomber", "assault"]):
            return "bomber"
        elif any(word in name_lower for word in ["corvette", "gunboat"]):
            return "corvette"
        elif any(word in name_lower for word in ["cruiser", "destroyer"]):
            return "cruiser"
        elif any(word in name_lower for word in ["capital", "dreadnought", "carrier"]):
            return "capital"
        elif any(word in name_lower for word in ["transport", "cargo", "freighter"]):
            return "transport"
        else:
            # Default to fighter for unknown ship types
            return "fighter"

    def _format_hardpoints(self, ship: Dict[str, Any]) -> str:
        """Format hardpoint configuration dictionary"""
        # Default hardpoints based on ship type
        hardpoints = {}

        ship_name = ship.get("name", "").lower()
        if "fighter" in ship_name or "interceptor" in ship_name:
            hardpoints = {
                "primary_gun_01": "Vector3(1.2, 0.1, 2.1)",
                "primary_gun_02": "Vector3(-1.2, 0.1, 2.1)",
                "missile_launcher_01": "Vector3(2.0, -0.5, 1.0)",
                "missile_launcher_02": "Vector3(-2.0, -0.5, 1.0)",
            }
        elif "bomber" in ship_name:
            hardpoints = {
                "primary_gun_01": "Vector3(1.5, 0.2, 2.5)",
                "primary_gun_02": "Vector3(-1.5, 0.2, 2.5)",
                "missile_launcher_01": "Vector3(3.0, -0.8, 0.5)",
                "missile_launcher_02": "Vector3(-3.0, -0.8, 0.5)",
                "torpedo_launcher": "Vector3(0.0, -1.0, 1.5)",
            }

        # Format as Godot dictionary
        formatted_items = [f'"{k}": {v}' for k, v in hardpoints.items()]
        return "{" + ", ".join(formatted_items) + "}"

    def _format_subsystems(self, ship: Dict[str, Any]) -> str:
        """Format subsystem definition paths array"""
        # Default subsystems based on ship type
        ship_name = ship.get("name", "").lower()

        subsystems = [
            '"res://resources/subsystems/engine_standard.tres"',
            '"res://resources/subsystems/weapons_standard.tres"',
            '"res://resources/subsystems/shields_standard.tres"',
        ]

        if "fighter" in ship_name:
            subsystems.append('"res://resources/subsystems/navigation_fighter.tres"')
        elif "bomber" in ship_name:
            subsystems.extend(
                [
                    '"res://resources/subsystems/navigation_bomber.tres"',
                    '"res://resources/subsystems/sensors_enhanced.tres"',
                ]
            )
        elif any(word in ship_name for word in ["capital", "cruiser", "destroyer"]):
            subsystems.extend(
                [
                    '"res://resources/subsystems/navigation_capital.tres"',
                    '"res://resources/subsystems/sensors_capital.tres"',
                    '"res://resources/subsystems/communications.tres"',
                ]
            )

        return "[" + ", ".join(subsystems) + "]"

    def _format_weapon_banks(self, weapon_banks: List[List[str]]) -> str:
        """Format weapon bank configuration as Godot array of arrays"""
        if not weapon_banks:
            return "[]"
        
        formatted_banks = []
        for bank in weapon_banks:
            if isinstance(bank, list):
                formatted_weapons = [f'"{weapon}"' for weapon in bank]
                formatted_banks.append("[" + ", ".join(formatted_weapons) + "]")
            else:
                # Handle single weapon strings
                formatted_banks.append(f'["{bank}"]')
        
        return "[" + ", ".join(formatted_banks) + "]"

    def _format_integer_list(self, int_list: List[int]) -> str:
        """Format integer list as Godot array"""
        if not int_list:
            return "[]"
        
        formatted_items = [str(item) for item in int_list]
        return "[" + ", ".join(formatted_items) + "]"

    def _sanitize_filename(self, name: str) -> str:
        """Convert ship name to valid filename"""
        # Remove invalid characters and spaces
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
        safe_name = safe_name.lower().strip("_")
        # Remove multiple consecutive underscores
        while "__" in safe_name:
            safe_name = safe_name.replace("__", "_")
        return safe_name or "unnamed_ship"

    def _generate_ship_registry(self, ship_entries: List[Dict[str, Any]]) -> str:
        """Generate ship registry resource file using feature-based organization"""
        registry_content = """[gd_resource type="Resource" script_class="ShipRegistryData" load_steps=2 format=3]

[ext_resource type="Script" path="res://resources/ships/ship_registry_data.gd" id="1"]

[resource]
script = ExtResource("1")
ship_classes = {
"""

        # Add all ship entries organized by faction and category
        ships_by_faction = {}
        for ship in ship_entries:
            ship_name = ship.get("name", "unknown")
            faction = self._determine_faction(ship_name)
            category = self._determine_ship_category(ship_name)
            
            if faction not in ships_by_faction:
                ships_by_faction[faction] = {}
            if category not in ships_by_faction[faction]:
                ships_by_faction[faction][category] = []
            ships_by_faction[faction][category].append(ship)

        for faction, categories in ships_by_faction.items():
            registry_content += f'    "{faction}": {{\n'
            for category, ships in categories.items():
                registry_content += f'        "{category}": [\n'
                for ship in ships:
                    ship_name = ship.get("name", "unknown")
                    safe_name = self._sanitize_filename(ship_name)
                    # Use the new feature-based path structure
                    if category in ["fighter", "bomber", "interceptor", "stealth", "corvette"]:
                        resource_path = f"res://features/fighters/{faction}/{safe_name}/{safe_name}.tres"
                    else:
                        resource_path = f"res://features/capital_ships/{faction}/{safe_name}/{safe_name}.tres"
                    registry_content += f'            "{resource_path}",\n'
                registry_content += "        ],\n"
            registry_content += "    },\n"

        registry_content += f"""}}
ship_count = {len(ship_entries)}
"""

        # Write registry file
        registry_path = os.path.join(self.output_dir, "ship_registry.tres")
        try:
            with open(registry_path, "w") as f:
                f.write(registry_content)
            print(f"Generated ship registry: {registry_path}")
            return registry_path
        except Exception as e:
            print(f"Error writing ship registry: {e}")
            return ""
