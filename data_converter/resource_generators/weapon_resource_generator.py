#!/usr/bin/env python3
"""
Weapon Resource Generator

Generates .tres WeaponData resource files from weapons.tbl data.
Uses existing weapon system architecture - no custom logic.
"""

import os
from pathlib import Path
from typing import Any, Dict, List


class WeaponResourceGenerator:
    """Generates WeaponData .tres resource files from parsed weapon table data"""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.weapons_dir = os.path.join(output_dir, "weapons")
        os.makedirs(self.weapons_dir, exist_ok=True)

    def generate_weapon_resources(
        self, weapon_entries: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate .tres resource files for all weapon entries"""
        generated_files = []

        # Organize weapons by type
        weapons_by_type = self._organize_weapons_by_type(weapon_entries)

        for weapon_type, weapons in weapons_by_type.items():
            type_dir = os.path.join(self.weapons_dir, weapon_type)
            os.makedirs(type_dir, exist_ok=True)

            for weapon in weapons:
                resource_file = self._generate_single_weapon_resource(
                    weapon, weapon_type
                )
                if resource_file:
                    generated_files.append(resource_file)

        # Generate weapon registry
        registry_file = self._generate_weapon_registry(weapon_entries)
        if registry_file:
            generated_files.append(registry_file)

        return generated_files

    def _organize_weapons_by_type(
        self, weapon_entries: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Organize weapons by type (primary, secondary, beam, etc.)"""
        weapons_by_type = {"primary": [], "secondary": [], "beam": [], "special": []}

        for weapon in weapon_entries:
            weapon_type = self._determine_weapon_type(weapon.get("name", ""))
            weapons_by_type[weapon_type].append(weapon)

        return weapons_by_type

    def _determine_weapon_type(self, weapon_name: str) -> str:
        """Determine weapon type from name"""
        name_lower = weapon_name.lower()

        if any(word in name_lower for word in ["beam", "laser"]):
            return "beam"
        elif any(
            word in name_lower for word in ["missile", "torpedo", "bomb", "rocket"]
        ):
            return "secondary"
        elif any(word in name_lower for word in ["emp", "flak", "swarm"]):
            return "special"
        else:
            return "primary"  # Default for guns, cannons, etc.

    def _generate_single_weapon_resource(
        self, weapon: Dict[str, Any], weapon_type: str
    ) -> str:
        """Generate a single WeaponData .tres resource file"""
        weapon_name = weapon.get("name", "unknown_weapon")
        safe_name = self._sanitize_filename(weapon_name)

        # Create .tres resource content
        resource_content = self._create_weapon_resource_content(weapon, weapon_type)

        # Write resource file
        output_path = os.path.join(self.weapons_dir, weapon_type, f"{safe_name}.tres")

        try:
            with open(output_path, "w") as f:
                f.write(resource_content)
            print(f"Generated weapon resource: {output_path}")
            return output_path
        except Exception as e:
            print(f"Error writing weapon resource {output_path}: {e}")
            return ""

    def _create_weapon_resource_content(
        self, weapon: Dict[str, Any], weapon_type: str
    ) -> str:
        """Create .tres resource content for WeaponData"""
        # Use the comprehensive weapon resource method
        return self._create_comprehensive_weapon_resource(weapon, weapon_type)

    def _is_homing_weapon(self, weapon_name: str) -> bool:
        """Determine if weapon has homing capability"""
        name_lower = weapon_name.lower()
        return any(
            word in name_lower for word in ["homing", "missile", "torpedo", "aspect"]
        )

    def _pierces_shields(self, weapon_name: str) -> bool:
        """Determine if weapon pierces shields"""
        piercing_weapons = [
            "flak",
            "emp",
            "jammer",
            "disruptor",
            "plasma",
            "neutron",
            "meson",
        ]
        return any(weapon.lower() in weapon_name.lower() for weapon in piercing_weapons)

    def _get_weapon_class(self, weapon_type: str) -> str:
        """Get weapon class from type"""
        class_map = {
            "primary": "PRIMARY_WEAPON",
            "secondary": "SECONDARY_WEAPON", 
            "beam": "BEAM_WEAPON",
            "special": "SPECIAL_WEAPON"
        }
        return class_map.get(weapon_type, "PRIMARY_WEAPON")

    def _create_comprehensive_weapon_resource(self, weapon: Dict[str, Any], weapon_type: str) -> str:
        """Create comprehensive weapon resource content"""
        # Extract weapon properties
        weapon_name = weapon.get("name", "Unknown Weapon")
        alt_name = weapon.get("alt_name", "")
        title = weapon.get("title", "")
        description = weapon.get("description", "")
        tech_title = weapon.get("tech_title", "")
        tech_description = weapon.get("tech_description", "")
        
        # Physics properties
        damage = weapon.get("damage", 0.0)
        mass = weapon.get("mass", 1.0)
        velocity = weapon.get("velocity", 100.0)
        fire_wait = weapon.get("fire_wait", 1.0)
        weapon_range = weapon.get("weapon_range", 1000.0)
        lifetime = weapon.get("lifetime", 5.0)
        energy_consumed = weapon.get("energy_consumed", 1.0)
        cargo_size = weapon.get("cargo_size", 1.0)
        
        # Model files
        model_file = weapon.get("model_file", "")
        pof_file = weapon.get("pof_file", "")
        external_model_file = weapon.get("external_model_file", "")
        
        # Laser properties
        laser_bitmap = weapon.get("laser_bitmap", "")
        laser_length = weapon.get("laser_length", 100.0)
        laser_head_radius = weapon.get("laser_head_radius", 1.0)
        laser_tail_radius = weapon.get("laser_tail_radius", 1.0)
        
        # Characteristics
        weapon_submodel = weapon.get("weapon_submodel", "")
        weapon_class = self._get_weapon_class(weapon_type)
        
        # Create resource content
        return f"""[gd_resource type="WeaponData" load_steps=2 format=3]

[ext_resource type="Script" path="res://addons/wcs_asset_core/structures/weapon_data.gd" id="1"]

[resource]
script = ExtResource("1")

# General Information
weapon_name = "{weapon_name}"
alt_name = "{alt_name}"
title = "{title}"
description = "{description}"
tech_title = "{tech_title}"
tech_description = "{tech_description}"

# Physics Properties
damage = {damage}
mass = {mass}
velocity = {velocity}
fire_wait = {fire_wait}
weapon_range = {weapon_range}
lifetime = {lifetime}
energy_consumed = {energy_consumed}
cargo_size = {cargo_size}

# Model Files
model_file = "{model_file}"
pof_file = "{pof_file}"
external_model_file = "{external_model_file}"

# Laser Properties
laser_bitmap = "{laser_bitmap}"
laser_length = {laser_length}
laser_head_radius = {laser_head_radius}
laser_tail_radius = {laser_tail_radius}

# Characteristics
weapon_submodel = "{weapon_submodel}"
weapon_class = "{weapon_class}"
"""

    def _get_weapon_subtype(self, weapon_type: str) -> int:
        """Get weapon subtype from type"""
        subtype_map = {
            "primary": 0,
            "secondary": 1,
            "beam": 2,
            "special": 3
        }
        return subtype_map.get(weapon_type, 0)

    def _get_render_type(self, weapon: Dict[str, Any], weapon_type: str) -> int:
        """Determine render type from weapon data"""
        # Check for POF model
        if weapon.get("model_file") or weapon.get("pof_file"):
            return 1  # WRT_POF
        # Check for laser properties
        elif weapon.get("laser_bitmap") or weapon_type == "beam":
            return 2  # WRT_LASER
        else:
            return 1  # Default to POF

    def _get_effect_path(
        self, effect_name: str, effect_type: str, weapon_type: str
    ) -> str:
        """Get effect path from extracted data or fallback"""
        if effect_name:
            return f"res://effects/weapons/{effect_name}.tscn"
        else:
            return f"res://effects/weapons/{effect_type}_{weapon_type}.tscn"

    def _sanitize_filename(self, name: str) -> str:
        """Convert weapon name to valid filename"""
        # Remove invalid characters and spaces
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
        safe_name = safe_name.lower().strip("_")
        return safe_name or "unnamed_weapon"

    def _generate_weapon_registry(self, weapon_entries: List[Dict[str, Any]]) -> str:
        """Generate weapon registry resource file"""
        registry_content = """[gd_resource type="Resource" script_class="WeaponRegistryData" load_steps=2 format=3]

[ext_resource type="Script" path="res://resources/weapons/weapon_registry_data.gd" id="1"]

[resource]
script = ExtResource("1")
weapons_by_type = {
"""

        # Organize weapons by type
        weapons_by_type = self._organize_weapons_by_type(weapon_entries)

        for weapon_type, weapons in weapons_by_type.items():
            if weapons:  # Only include types that have weapons
                registry_content += f'    "{weapon_type}": [\n'
                for weapon in weapons:
                    weapon_name = weapon.get("name", "unknown")
                    safe_name = self._sanitize_filename(weapon_name)
                    resource_path = (
                        f"res://resources/weapons/{weapon_type}/{safe_name}.tres"
                    )
                    registry_content += f'        "{resource_path}",\n'
                registry_content += "    ],\n"

        registry_content += f"""}}
total_weapons = {len(weapon_entries)}
"""

        # Write registry file
        registry_path = os.path.join(self.output_dir, "weapon_registry.tres")
        try:
            with open(registry_path, "w") as f:
                f.write(registry_content)
            print(f"Generated weapon registry: {registry_path}")
            return registry_path
        except Exception as e:
            print(f"Error writing weapon registry: {e}")
            return ""
