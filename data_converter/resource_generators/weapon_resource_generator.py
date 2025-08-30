#!/usr/bin/env python3
"""
Weapon Resource Generator

Generates .tres WeaponData resource files from weapons.tbl data following the
feature-based organization structure: /features/weapons/{weapon_name}/
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .base_resource_generator import ResourceGenerator
from ..core.catalog.asset_catalog import AssetCatalog
from ..core.relationship_builder import RelationshipBuilder

logger = logging.getLogger(__name__)


class WeaponResourceGenerator(ResourceGenerator):
    """Generates WeaponData .tres resource files from parsed weapon table data following feature-based organization"""

    def __init__(
        self,
        asset_catalog: AssetCatalog,
        relationship_builder: RelationshipBuilder,
        output_dir: Union[str, Path],
    ):
        """
        Initialize the weapon resource generator.

        Args:
            asset_catalog: Enhanced asset catalog instance
            relationship_builder: Relationship builder instance
            output_dir: Output directory for generated resources
        """
        super().__init__(asset_catalog, relationship_builder, output_dir)

        # Create the features/weapons directory structure
        self.features_dir = self.output_dir / "features" / "weapons"
        self.features_dir.mkdir(parents=True, exist_ok=True)

        # Also create the data directory for weapon definitions
        self.data_dir = self.output_dir / "assets" / "data" / "weapons"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def generate_resource(self, asset_id: str) -> Optional[str]:
        """
        Generate a Godot resource for the specified weapon asset.

        Args:
            asset_id: ID of the weapon asset to generate resource for

        Returns:
            Path to generated resource file, or None if generation failed
        """
        # Look up weapon in asset catalog
        asset_entry = self.asset_catalog.get_asset(asset_id)
        if not asset_entry:
            logger.warning(f"Weapon asset not found: {asset_id}")
            return None

        # Generate feature-based weapon resource
        feature_resource_file = self._generate_feature_weapon_resource(
            asset_entry.metadata
        )
        if not feature_resource_file:
            return None

        # Generate data-based weapon resource
        data_resource_file = self._generate_data_weapon_resource(asset_entry.metadata)
        if not data_resource_file:
            return None

        return feature_resource_file

    def validate_resource(self, resource_path: Union[str, Path]) -> bool:
        """
        Validate a generated weapon resource file.

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

            # Check if it's a valid .tres file
            with open(resource_path, "r") as f:
                content = f.read()

            # Basic validation - check for required sections
            if "[gd_resource" not in content:
                logger.error(f"Invalid .tres file format: {resource_path}")
                return False

            if "[resource]" not in content:
                logger.error(f"Missing resource section: {resource_path}")
                return False

            logger.debug(f"Resource validation passed: {resource_path}")
            return True

        except Exception as e:
            logger.error(f"Error validating resource {resource_path}: {e}")
            return False

    def generate_weapon_resources(
        self, weapon_entries: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Generate .tres resource files for all weapon entries following feature-based organization.

        Args:
            weapon_entries: List of parsed weapon entry dictionaries

        Returns:
            Dictionary mapping weapon names to generated resource paths
        """
        results = {}

        for weapon in weapon_entries:
            try:
                # Generate feature-based weapon resource
                feature_resource_file = self._generate_feature_weapon_resource(weapon)
                if feature_resource_file:
                    weapon_name = weapon.get("name", "unknown_weapon")
                    results[weapon_name] = feature_resource_file

                # Generate data-based weapon resource
                data_resource_file = self._generate_data_weapon_resource(weapon)
                if data_resource_file:
                    # We'll track this in our internal statistics
                    pass

            except Exception as e:
                weapon_name = weapon.get("name", "unknown")
                logger.error(
                    f"Error generating resources for weapon {weapon_name}: {e}"
                )
                continue

        # Generate weapon registry
        registry_file = self._generate_weapon_registry(weapon_entries)
        if registry_file:
            results["registry"] = registry_file

        return results

    def _generate_feature_weapon_resource(
        self, weapon: Dict[str, Any]
    ) -> Optional[str]:
        """
        Generate a weapon resource in the feature-based structure.

        Args:
            weapon: Weapon data dictionary

        Returns:
            Path to generated resource file, or None if generation failed
        """
        try:
            weapon_name = weapon.get("name", "unknown_weapon")
            safe_name = self._sanitize_filename(weapon_name)

            # Create feature directory for this weapon
            weapon_dir = self.features_dir / safe_name
            weapon_dir.mkdir(exist_ok=True)

            # Create .tres resource content
            resource_content = self._create_weapon_resource_content(weapon)

            # Write resource file in feature directory
            output_path = weapon_dir / f"{safe_name}.tres"

            if self._write_resource_file(resource_content, output_path):
                logger.info(f"Generated feature weapon resource: {output_path}")
                self.generated_resources.append(str(output_path))
                return str(output_path)
            else:
                self.failed_resources.append(weapon_name)
                return None

        except Exception as e:
            weapon_name = weapon.get("name", "unknown")
            logger.error(
                f"Error generating feature weapon resource for {weapon_name}: {e}"
            )
            self.failed_resources.append(weapon_name)
            return None

    def _generate_data_weapon_resource(self, weapon: Dict[str, Any]) -> Optional[str]:
        """
        Generate a weapon resource in the data directory structure.

        Args:
            weapon: Weapon data dictionary

        Returns:
            Path to generated resource file, or None if generation failed
        """
        try:
            weapon_name = weapon.get("name", "unknown_weapon")
            safe_name = self._sanitize_filename(weapon_name)

            # Create .tres resource content
            resource_content = self._create_weapon_resource_content(weapon)

            # Write resource file in data directory
            output_path = self.data_dir / f"{safe_name}.tres"

            if self._write_resource_file(resource_content, output_path):
                logger.info(f"Generated data weapon resource: {output_path}")
                self.generated_resources.append(str(output_path))
                return str(output_path)
            else:
                self.failed_resources.append(weapon_name)
                return None

        except Exception as e:
            weapon_name = weapon.get("name", "unknown")
            logger.error(
                f"Error generating data weapon resource for {weapon_name}: {e}"
            )
            self.failed_resources.append(weapon_name)
            return None

    def _create_weapon_resource_content(self, weapon: Dict[str, Any]) -> str:
        """
        Create .tres resource content for WeaponData with complete property mapping.

        Args:
            weapon: Weapon data dictionary

        Returns:
            Formatted .tres resource content string
        """
        # Extract all weapon properties with proper defaults
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

        # Damage factors
        armor_factor = weapon.get("armor_factor", 1.0)
        shield_factor = weapon.get("shield_factor", 1.0)
        subsystem_factor = weapon.get("subsystem_factor", 1.0)

        # Model files
        model_file = weapon.get("model_file", "")
        pof_file = weapon.get("pof_file", "")
        external_model_file = weapon.get("external_model_file", "")
        submodel = weapon.get("submodel", "")

        # Laser properties
        laser_bitmap = weapon.get("laser_bitmap", "")
        laser_glow = weapon.get("laser_glow", "")
        laser_length = weapon.get("laser_length", 100.0)
        laser_head_radius = weapon.get("laser_head_radius", 1.0)
        laser_tail_radius = weapon.get("laser_tail_radius", 1.0)
        laser_color = weapon.get("laser_color", "255, 255, 255")
        laser_color2 = weapon.get("laser_color2", "0, 0, 0")

        # Visual effects
        muzzleflash = weapon.get("muzzleflash", "")
        impact_effect = weapon.get("impact_effect", "")
        particle_spew = weapon.get("particle_spew", "")
        trails = weapon.get("trails", "")
        shockwave_anim = weapon.get("shockwave_anim", "")
        icon = weapon.get("icon", "")
        anim = weapon.get("anim", "")
        impact_explosion = weapon.get("impact_explosion", "")
        impact_explosion_radius = weapon.get("impact_explosion_radius", 0.0)

        # Tech database assets
        tech_model = weapon.get("tech_model", "")
        tech_anim = weapon.get("tech_anim", "")
        tech_image = weapon.get("tech_image", "")

        # Audio assets
        launch_sound = weapon.get("launch_sound", "")
        impact_sound = weapon.get("impact_sound", "")
        disarmed_sound = weapon.get("disarmed_sound", "")
        armed_sound = weapon.get("armed_sound", "")
        flyby_sound = weapon.get("flyby_sound", "")

        # Homing properties
        homing_type = weapon.get("homing_type", "NO")
        turn_time = weapon.get("turn_time", 0.0)
        free_flight_time = weapon.get("free_flight_time", 0.0)
        fov = weapon.get("fov", 0.0)
        seeker_strength = weapon.get("seeker_strength", 0.0)

        # Special properties
        swarm_count = weapon.get("swarm_count", 0)
        swarm_wait = weapon.get("swarm_wait", 0)

        # Characteristics
        weapon_class = weapon.get("weapon_class", "PRIMARY_WEAPON")

        # Create resource content with all properties
        resource_content = self._create_tres_header("Resource", "WeaponData")

        # Add script reference
        resource_content += (
            self._create_ext_resource_entry(
                "Script", "res://scripts/weapon/weapon_data.gd", "1"
            )
            + "\n\n"
        )

        # Add resource properties
        properties = {
            # General Information
            "weapon_name": weapon_name,
            "alt_name": alt_name,
            "title": title,
            "description": description,
            "tech_title": tech_title,
            "tech_description": tech_description,
            # Physics Properties
            "damage": damage,
            "mass": mass,
            "velocity": velocity,
            "fire_wait": fire_wait,
            "weapon_range": weapon_range,
            "lifetime": lifetime,
            "energy_consumed": energy_consumed,
            "cargo_size": cargo_size,
            # Damage Factors
            "armor_factor": armor_factor,
            "shield_factor": shield_factor,
            "subsystem_factor": subsystem_factor,
            # Model Files
            "model_file": model_file,
            "pof_file": pof_file,
            "external_model_file": external_model_file,
            "submodel": submodel,
            # Laser Properties
            "laser_bitmap": laser_bitmap,
            "laser_glow": laser_glow,
            "laser_length": laser_length,
            "laser_head_radius": laser_head_radius,
            "laser_tail_radius": laser_tail_radius,
            "laser_color": laser_color,
            "laser_color2": laser_color2,
            # Visual Effects
            "muzzleflash": muzzleflash,
            "impact_effect": impact_effect,
            "particle_spew": particle_spew,
            "trails": trails,
            "shockwave_anim": shockwave_anim,
            "icon": icon,
            "anim": anim,
            "impact_explosion": impact_explosion,
            "impact_explosion_radius": impact_explosion_radius,
            # Tech Database Assets
            "tech_model": tech_model,
            "tech_anim": tech_anim,
            "tech_image": tech_image,
            # Audio Assets
            "launch_sound": launch_sound,
            "impact_sound": impact_sound,
            "disarmed_sound": disarmed_sound,
            "armed_sound": armed_sound,
            "flyby_sound": flyby_sound,
            # Homing Properties
            "homing_type": homing_type,
            "turn_time": turn_time,
            "free_flight_time": free_flight_time,
            "fov": fov,
            "seeker_strength": seeker_strength,
            # Special Properties
            "swarm_count": swarm_count,
            "swarm_wait": swarm_wait,
            # Characteristics
            "weapon_class": weapon_class,
        }

        resource_content += self._create_resource_section(properties)

        return resource_content

    def _generate_weapon_registry(
        self, weapon_entries: List[Dict[str, Any]]
    ) -> Optional[str]:
        """
        Generate weapon registry resource file.

        Args:
            weapon_entries: List of weapon entry dictionaries

        Returns:
            Path to generated registry file, or None if generation failed
        """
        try:
            registry_content = self._create_tres_header(
                "Resource", "WeaponRegistryData"
            )

            # Add script reference
            registry_content += (
                self._create_ext_resource_entry(
                    "Script", "res://scripts/weapon/weapon_registry_data.gd", "1"
                )
                + "\n\n"
            )

            # Create weapons dictionary
            weapons_dict = {}
            for weapon in weapon_entries:
                weapon_name = weapon.get("name", "unknown")
                safe_name = self._sanitize_filename(weapon_name)
                # Reference to feature-based resource
                resource_path = f"res://features/weapons/{safe_name}/{safe_name}.tres"
                weapons_dict[weapon_name] = resource_path

            # Add resource section with weapons registry
            registry_content += self._create_resource_section({"weapons": weapons_dict})

            # Write registry file in data directory
            registry_path = self.data_dir / "weapon_registry.tres"

            if self._write_resource_file(registry_content, registry_path):
                logger.info(f"Generated weapon registry: {registry_path}")
                self.generated_resources.append(str(registry_path))
                return str(registry_path)
            else:
                self.failed_resources.append("weapon_registry")
                return None

        except Exception as e:
            logger.error(f"Error generating weapon registry: {e}")
            self.failed_resources.append("weapon_registry")
            return None

    def _sanitize_filename(self, name: str) -> str:
        """
        Convert weapon name to valid filename following Godot conventions.

        Args:
            name: Weapon name to sanitize

        Returns:
            Sanitized filename
        """
        # Handle special case for weapon names that start with @
        if name.startswith("@"):
            name = name[1:]  # Remove @ prefix

        # Remove invalid characters and spaces
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
        safe_name = safe_name.lower().strip("_")
        return safe_name or "unnamed_weapon"
