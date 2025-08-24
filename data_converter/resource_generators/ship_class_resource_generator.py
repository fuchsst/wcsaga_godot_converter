#!/usr/bin/env python3
"""
Ship Class Resource Generator

This module generates Godot .tres resource files for ship classes,
including subsystems, weapons, physics properties, and visual effects.

Author: Qwen Code Assistant
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .base_resource_generator import ResourceGenerator
from ..core.catalog.enhanced_asset_catalog import EnhancedAssetCatalog
from ..core.relationship_builder import RelationshipBuilder
from ..core.table_data_structures import ShipClassData

logger = logging.getLogger(__name__)


class ShipClassResourceGenerator(ResourceGenerator):
    """
    Generates Godot .tres resource files for ship classes.
    """

    def __init__(
        self,
        asset_catalog: EnhancedAssetCatalog,
        relationship_builder: RelationshipBuilder,
        output_dir: Union[str, Path]
    ):
        """
        Initialize the ship class resource generator.
        
        Args:
            asset_catalog: Enhanced asset catalog instance
            relationship_builder: Relationship builder instance
            output_dir: Output directory for generated resources
        """
        super().__init__(asset_catalog, relationship_builder, output_dir)
        logger.info("Initialized ShipClassResourceGenerator")

    def generate_resource(self, asset_id: str) -> Optional[str]:
        """
        Generate a Godot resource for a ship class.
        
        Args:
            asset_id: ID of the ship class asset
            
        Returns:
            Path to generated resource file, or None if generation failed
        """
        try:
            # Get asset metadata
            if asset_id not in self.asset_catalog.assets:
                logger.error(f"Asset {asset_id} not found in catalog")
                return None
                
            asset = self.asset_catalog.assets[asset_id]
            
            # Get ship class data from properties
            ship_data_dict = asset.properties.get("ship_data", {})
            if not ship_data_dict:
                logger.warning(f"No ship data found for asset {asset_id}")
                return None
                
            # Create ShipClassData from dictionary
            ship_data = ShipClassData(**ship_data_dict)
            
            # Generate resource content
            resource_content = self._create_ship_class_resource_content(asset_id, ship_data)
            
            # Determine output path
            faction = self._get_asset_faction(asset.name)
            category = self._get_asset_category(asset.name, "ship")
            safe_name = self._sanitize_filename(asset.name)
            
            resource_path = (
                self.output_dir / "ships" / faction / category / f"{safe_name}.tres"
            )
            
            # Write resource file
            if self._write_resource_file(resource_content, resource_path):
                logger.info(f"Generated ship class resource: {resource_path}")
                return str(resource_path)
            else:
                logger.error(f"Failed to write ship class resource: {resource_path}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating ship class resource for {asset_id}: {e}")
            return None

    def validate_resource(self, resource_path: Union[str, Path]) -> bool:
        """
        Validate a generated ship class resource file.
        
        Args:
            resource_path: Path to the resource file to validate
            
        Returns:
            True if resource is valid, False otherwise
        """
        try:
            resource_path = Path(resource_path)
            
            if not resource_path.exists():
                logger.error(f"Resource file does not exist: {resource_path}")
                return False
                
            # Basic validation - check if it's a valid TRES file
            with open(resource_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Check for required sections
            required_sections = ["[gd_resource", "[ext_resource", "[resource"]
            for section in required_sections:
                if section not in content:
                    logger.error(f"Missing required section {section} in {resource_path}")
                    return False
                    
            # Check for required ship class properties
            required_properties = [
                "class_name",
                "display_name", 
                "ship_type",
                "mass",
                "max_velocity"
            ]
            
            for prop in required_properties:
                if f"{prop} =" not in content:
                    logger.error(f"Missing required property {prop} in {resource_path}")
                    return False
                    
            logger.debug(f"Ship class resource validation passed: {resource_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error validating ship class resource {resource_path}: {e}")
            return False

    def _create_ship_class_resource_content(
        self, 
        asset_id: str, 
        ship_data: ShipClassData
    ) -> str:
        """
        Create the content for a ship class .tres file.
        
        Args:
            asset_id: ID of the asset
            ship_data: Ship class data
            
        Returns:
            Resource file content as string
        """
        # Create resource header
        content = self._create_tres_header("Resource", "ShipClass")
        
        # Add external resources
        content += self._create_ext_resource_entry(
            "Script", 
            "res://addons/wcs_asset_core/resources/ship/ship_class.gd", 
            "1"
        ) + "\n\n"
        
        # Create ship properties
        properties = self._extract_ship_properties(ship_data)
        
        # Add resource section
        content += self._create_resource_section(properties)
        
        return content

    def _extract_ship_properties(self, ship_data: ShipClassData) -> Dict[str, Any]:
        """
        Extract ship properties for the resource file.
        
        Args:
            ship_data: Ship class data
            
        Returns:
            Dictionary of properties
        """
        properties = {
            # Basic identification
            "script": "ExtResource(\"1\")",
            "class_name": ship_data.name,
            "display_name": getattr(ship_data, "alt_name", ship_data.name),
            "short_name": getattr(ship_data, "short_name", ""),
            
            # Classification
            "species": getattr(ship_data, "species", "Terran"),
            "class_type": getattr(ship_data, "class_type", "Fighter"),
            "manufacturer": getattr(ship_data, "manufacturer", ""),
            
            # Model and visual
            "pof_file": getattr(ship_data, "pof_file", ""),
            "cockpit_pof_file": getattr(ship_data, "cockpit_pof_file", ""),
            
            # Physics and performance
            "density": getattr(ship_data, "density", 1.0),
            "damp": getattr(ship_data, "damp", 0.1),
            "rotdamp": getattr(ship_data, "rotdamp", 0.1),
            "banking_constant": getattr(ship_data, "banking_constant", 0.5),
            "max_velocity": getattr(ship_data, "max_velocity", 100.0),
            "rear_velocity": getattr(ship_data, "rear_velocity", 50.0),
            "forward_accel": getattr(ship_data, "forward_accel", 5.0),
            "forward_decel": getattr(ship_data, "forward_decel", 5.0),
            "slide_accel": getattr(ship_data, "slide_accel", 5.0),
            "slide_decel": getattr(ship_data, "slide_decel", 5.0),
            "can_glide": getattr(ship_data, "can_glide", False),
            "dynamic_glide_cap": getattr(ship_data, "dynamic_glide_cap", False),
            "max_glide_speed": getattr(ship_data, "max_glide_speed", 0.0),
            "glide_accel_mult": getattr(ship_data, "glide_accel_mult", 0.0),
            "use_newtonian_dampening": getattr(ship_data, "use_newtonian_dampening", False),
            "autoaim_fov": getattr(ship_data, "autoaim_fov", 0.0),
            
            # Combat capabilities
            "primary_weapon_count": getattr(ship_data, "primary_weapon_count", 0),
            "secondary_weapon_count": getattr(ship_data, "secondary_weapon_count", 0),
            
            # Defense and durability
            "shields": getattr(ship_data, "shields", 100.0),
            "hull": getattr(ship_data, "hull", 100.0),
            "hull_repair_rate": getattr(ship_data, "hull_repair_rate", 0.0),
            "subsystem_repair_rate": getattr(ship_data, "subsystem_repair_rate", 0.0),
            "armor_type": getattr(ship_data, "armor_type", ""),
            "shield_armor_type": getattr(ship_data, "shield_armor_type", ""),
            
            # Power and systems
            "power_output": getattr(ship_data, "power_output", 0.0),
            "max_oclk_speed": getattr(ship_data, "max_oclk_speed", 0.0),
            "max_weapon_reserve": getattr(ship_data, "max_weapon_reserve", 0.0),
            "max_shield_regen": getattr(ship_data, "max_shield_regen", 0.0),
            "max_weapon_regen": getattr(ship_data, "max_weapon_regen", 0.0),
            "has_afterburner": getattr(ship_data, "has_afterburner", False),
            "afterburner_fuel_capacity": getattr(ship_data, "afterburner_fuel_capacity", 0.0),
            "afterburner_burn_rate": getattr(ship_data, "afterburner_burn_rate", 0.0),
            "afterburner_rec_rate": getattr(ship_data, "afterburner_rec_rate", 0.0),
            "afterburner_forward_accel": getattr(ship_data, "afterburner_forward_accel", 0.0),
            
            # Countermeasures and sensors
            "countermeasures": getattr(ship_data, "countermeasures", 0),
            "engine_sound": getattr(ship_data, "engine_sound", ""),
            
            # UI and interface
            "closeup_zoom": getattr(ship_data, "closeup_zoom", 1.0),
            "shield_icon": getattr(ship_data, "shield_icon", ""),
            "ship_icon": getattr(ship_data, "ship_icon", ""),
            "ship_anim": getattr(ship_data, "ship_anim", ""),
            "ship_overhead": getattr(ship_data, "ship_overhead", ""),
            "score": getattr(ship_data, "score", 0),
            "scan_time": getattr(ship_data, "scan_time", 0),
            
            # AI and behavior
            "ai_class": getattr(ship_data, "ai_class", 0),
            
            # Explosion properties
            "explosion_damage_type": getattr(ship_data, "explosion_damage_type", ""),
            "explosion_inner_damage": getattr(ship_data, "explosion_inner_damage", 0.0),
            "explosion_outer_damage": getattr(ship_data, "explosion_outer_damage", 0.0),
            "explosion_inner_radius": getattr(ship_data, "explosion_inner_radius", 0.0),
            "explosion_outer_radius": getattr(ship_data, "explosion_outer_radius", 0.0),
            "explosion_shockwave_speed": getattr(ship_data, "explosion_shockwave_speed", 0.0),
            
            # Impact effects
            "impact_spew_max_particles": getattr(ship_data, "impact_spew_max_particles", 0),
            
            # Damage effects
            "damage_spew_max_particles": getattr(ship_data, "damage_spew_max_particles", 0),
            
            # Debris properties
            "debris_min_lifetime": getattr(ship_data, "debris_min_lifetime", 0.0),
            "debris_max_lifetime": getattr(ship_data, "debris_max_lifetime", 0.0),
            "debris_min_speed": getattr(ship_data, "debris_min_speed", 0.0),
            "debris_max_speed": getattr(ship_data, "debris_max_speed", 0.0),
            "debris_min_rotation_speed": getattr(ship_data, "debris_min_rotation_speed", 0.0),
            "debris_max_rotation_speed": getattr(ship_data, "debris_max_rotation_speed", 0.0),
            "debris_damage_type": getattr(ship_data, "debris_damage_type", ""),
            "debris_min_hitpoints": getattr(ship_data, "debris_min_hitpoints", 0.0),
            "debris_max_hitpoints": getattr(ship_data, "debris_max_hitpoints", 0.0),
            "debris_damage_multiplier": getattr(ship_data, "debris_damage_multiplier", 0.0),
            "debris_lightning_arc_percent": getattr(ship_data, "debris_lightning_arc_percent", 0.0),
        }
        
        # Add subsystems if present
        if hasattr(ship_data, "subsystems") and ship_data.subsystems:
            properties["subsystems"] = ship_data.subsystems
            
        # Add texture replacements if present
        if hasattr(ship_data, "texture_replacements") and ship_data.texture_replacements:
            properties["texture_replacements"] = ship_data.texture_replacements
            
        return properties

    def generate_ship_subsystems(self, asset_id: str) -> List[str]:
        """
        Generate subsystem resources for a ship class.
        
        Args:
            asset_id: ID of the ship class asset
            
        Returns:
            List of paths to generated subsystem resources
        """
        subsystem_paths = []
        
        try:
            if asset_id not in self.asset_catalog.assets:
                logger.warning(f"Asset {asset_id} not found for subsystem generation")
                return subsystem_paths
                
            asset = self.asset_catalog.assets[asset_id]
            ship_data_dict = asset.properties.get("ship_data", {})
            
            if not ship_data_dict:
                logger.warning(f"No ship data found for subsystem generation: {asset_id}")
                return subsystem_paths
                
            ship_data = ShipClassData(**ship_data_dict)
            
            if not hasattr(ship_data, "subsystems") or not ship_data.subsystems:
                logger.debug(f"No subsystems found for ship class: {asset_id}")
                return subsystem_paths
                
            faction = self._get_asset_faction(asset.name)
            category = self._get_asset_category(asset.name, "ship")
            safe_name = self._sanitize_filename(asset.name)
            
            for i, subsystem in enumerate(ship_data.subsystems):
                try:
                    subsystem_name = subsystem.get("name", f"subsystem_{i}")
                    subsystem_safe_name = self._sanitize_filename(subsystem_name)
                    
                    # Create subsystem resource content
                    subsystem_content = self._create_subsystem_resource_content(subsystem)
                    
                    # Determine output path
                    subsystem_path = (
                        self.output_dir / "ships" / faction / category / safe_name / 
                        "subsystems" / f"{subsystem_safe_name}.tres"
                    )
                    
                    # Write subsystem resource
                    if self._write_resource_file(subsystem_content, subsystem_path):
                        subsystem_paths.append(str(subsystem_path))
                        logger.debug(f"Generated subsystem resource: {subsystem_path}")
                    else:
                        logger.error(f"Failed to write subsystem resource: {subsystem_path}")
                        
                except Exception as e:
                    logger.error(f"Error generating subsystem {i} for {asset_id}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in generate_ship_subsystems for {asset_id}: {e}")
            
        return subsystem_paths

    def _create_subsystem_resource_content(self, subsystem_data: Dict[str, Any]) -> str:
        """
        Create the content for a subsystem .tres file.
        
        Args:
            subsystem_data: Subsystem data dictionary
            
        Returns:
            Resource file content as string
        """
        # Create resource header
        content = self._create_tres_header("Resource", "ShipSubsystem")
        
        # Add external resources
        content += self._create_ext_resource_entry(
            "Script", 
            "res://addons/wcs_asset_core/resources/ship/ship_subsystem.gd", 
            "1"
        ) + "\n\n"
        
        # Create subsystem properties
        properties = {
            "script": "ExtResource(\"1\")",
            "subsystem_name": subsystem_data.get("name", "Unknown Subsystem"),
            "subsystem_type": subsystem_data.get("type", "Generic"),
            "hitpoints": subsystem_data.get("hitpoints", 100.0),
            "repair_rate": subsystem_data.get("repair_rate", 0.0),
            "armor_type": subsystem_data.get("armor_type", ""),
            "flags": subsystem_data.get("flags", 0),
            "activation_level": subsystem_data.get("activation_level", 0.0),
            "transfer_rate": subsystem_data.get("transfer_rate", 0.0),
            "max_instances": subsystem_data.get("max_instances", 1),
            "cooldown_time": subsystem_data.get("cooldown_time", 0.0),
            "goal_priority": subsystem_data.get("goal_priority", 0),
        }
        
        # Add resource section
        content += self._create_resource_section(properties)
        
        return content

    def generate_ship_hardpoints(self, asset_id: str) -> Optional[str]:
        """
        Generate weapon hardpoint resources for a ship class.
        
        Args:
            asset_id: ID of the ship class asset
            
        Returns:
            Path to generated hardpoint resource, or None if generation failed
        """
        try:
            if asset_id not in self.asset_catalog.assets:
                logger.warning(f"Asset {asset_id} not found for hardpoint generation")
                return None
                
            asset = self.asset_catalog.assets[asset_id]
            
            # For now, we'll create a generic hardpoint configuration
            # In a full implementation, this would extract actual hardpoint data
            hardpoint_content = self._create_hardpoint_resource_content(asset.name)
            
            faction = self._get_asset_faction(asset.name)
            category = self._get_asset_category(asset.name, "ship")
            safe_name = self._sanitize_filename(asset.name)
            
            hardpoint_path = (
                self.output_dir / "ships" / faction / category / safe_name / 
                f"{safe_name}_hardpoints.tres"
            )
            
            if self._write_resource_file(hardpoint_content, hardpoint_path):
                logger.info(f"Generated hardpoint resource: {hardpoint_path}")
                return str(hardpoint_path)
            else:
                logger.error(f"Failed to write hardpoint resource: {hardpoint_path}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating hardpoint resource for {asset_id}: {e}")
            return None

    def _create_hardpoint_resource_content(self, ship_name: str) -> str:
        """
        Create the content for a hardpoint .tres file.
        
        Args:
            ship_name: Name of the ship
            
        Returns:
            Resource file content as string
        """
        # Create resource header
        content = self._create_tres_header("Resource", "WeaponHardpoints")
        
        # Add external resources
        content += self._create_ext_resource_entry(
            "Script", 
            "res://addons/wcs_asset_core/resources/ship/weapon_hardpoints.gd", 
            "1"
        ) + "\n\n"
        
        # Create default hardpoint configuration based on ship type
        hardpoint_config = self._generate_default_hardpoint_configuration(ship_name)
        
        # Create properties
        properties = {
            "script": "ExtResource(\"1\")",
            "ship_name": ship_name,
            "hardpoint_configuration": hardpoint_config
        }
        
        # Add resource section
        content += self._create_resource_section(properties)
        
        return content

    def _generate_default_hardpoint_configuration(self, ship_name: str) -> Dict[str, Any]:
        """
        Generate a default hardpoint configuration based on ship name.
        
        Args:
            ship_name: Name of the ship
            
        Returns:
            Hardpoint configuration dictionary
        """
        name_lower = ship_name.lower()
        
        # Default hardpoints
        hardpoints = {}
        
        # Fighter-type ships
        if any(pattern in name_lower for pattern in ["fighter", "interceptor", "stealth"]):
            hardpoints = {
                "primary_gun_01": {"position": [1.2, 0.1, 2.1], "type": "primary"},
                "primary_gun_02": {"position": [-1.2, 0.1, 2.1], "type": "primary"},
                "missile_launcher_01": {"position": [2.0, -0.5, 1.0], "type": "secondary"},
                "missile_launcher_02": {"position": [-2.0, -0.5, 1.0], "type": "secondary"},
            }
            
        # Bomber-type ships
        elif any(pattern in name_lower for pattern in ["bomber", "assault"]):
            hardpoints = {
                "primary_gun_01": {"position": [1.5, 0.2, 2.5], "type": "primary"},
                "primary_gun_02": {"position": [-1.5, 0.2, 2.5], "type": "primary"},
                "missile_launcher_01": {"position": [3.0, -0.8, 0.5], "type": "secondary"},
                "missile_launcher_02": {"position": [-3.0, -0.8, 0.5], "type": "secondary"},
                "torpedo_launcher": {"position": [0.0, -1.0, 1.5], "type": "secondary"},
            }
            
        # Capital ships
        elif any(pattern in name_lower for pattern in ["capital", "cruiser", "destroyer", "carrier"]):
            hardpoints = {
                "primary_turret_01": {"position": [10.0, 2.0, 0.0], "type": "primary"},
                "primary_turret_02": {"position": [-10.0, 2.0, 0.0], "type": "primary"},
                "secondary_turret_01": {"position": [8.0, -1.0, 5.0], "type": "secondary"},
                "secondary_turret_02": {"position": [-8.0, -1.0, 5.0], "type": "secondary"},
                "anti_fighter_bay_01": {"position": [0.0, 0.0, -15.0], "type": "secondary"},
                "anti_fighter_bay_02": {"position": [0.0, 0.0, 15.0], "type": "secondary"},
            }
            
        # Default (generic)
        else:
            hardpoints = {
                "primary_gun_01": {"position": [1.0, 0.0, 1.0], "type": "primary"},
                "primary_gun_02": {"position": [-1.0, 0.0, 1.0], "type": "primary"},
            }
            
        return hardpoints