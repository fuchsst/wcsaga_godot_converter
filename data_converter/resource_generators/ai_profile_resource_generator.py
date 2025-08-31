#!/usr/bin/env python3
"""
AI Profile Resource Generator

Generates .tres AIProfileResource files from ai_profiles.tbl data following the
data-based organization structure: /assets/data/ai/profiles/{profile_name}.tres
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .base_resource_generator import ResourceGenerator
from ..core.catalog.asset_catalog import AssetCatalog
from ..core.relationship_builder import RelationshipBuilder

logger = logging.getLogger(__name__)


class AIProfileResourceGenerator(ResourceGenerator):
    """Generates AIProfileResource .tres resource files from parsed AI profile table data following data-based organization"""

    def __init__(
        self,
        asset_catalog: AssetCatalog,
        relationship_builder: RelationshipBuilder,
        output_dir: Union[str, Path],
    ):
        """
        Initialize the AI profile resource generator.

        Args:
            asset_catalog: Enhanced asset catalog instance
            relationship_builder: Relationship builder instance
            output_dir: Output directory for generated resources
        """
        super().__init__(asset_catalog, relationship_builder, output_dir)

        # Create the data directory for AI profile definitions
        self.data_dir = self.output_dir / "assets" / "data" / "ai" / "profiles"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def generate_resource(self, asset_id: str) -> Optional[str]:
        """
        Generate a Godot resource for the specified AI profile asset.

        Args:
            asset_id: ID of the AI profile asset to generate resource for

        Returns:
            Path to generated resource file, or None if generation failed
        """
        # Look up AI profile in asset catalog
        asset_entry = self.asset_catalog.get_asset(asset_id)
        if not asset_entry:
            logger.warning(f"AI profile asset not found: {asset_id}")
            return None

        # Generate data-based AI profile resource
        data_resource_file = self._generate_data_ai_profile_resource(asset_entry.metadata)
        if not data_resource_file:
            return None

        return data_resource_file

    def validate_resource(self, resource_path: Union[str, Path]) -> bool:
        """
        Validate a generated AI profile resource file.

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

    def generate_ai_profile_resources(
        self, ai_profile_entries: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Generate .tres resource files for all AI profile entries following data-based organization.

        Args:
            ai_profile_entries: List of parsed AI profile entry dictionaries

        Returns:
            Dictionary mapping AI profile names to generated resource paths
        """
        results = {}

        for ai_profile in ai_profile_entries:
            try:
                # Generate data-based AI profile resource
                data_resource_file = self._generate_data_ai_profile_resource(ai_profile)
                if data_resource_file:
                    profile_name = ai_profile.get("name", "unknown_ai_profile")
                    results[profile_name] = data_resource_file

            except Exception as e:
                profile_name = ai_profile.get("name", "unknown")
                logger.error(
                    f"Error generating resources for AI profile {profile_name}: {e}"
                )
                continue

        # Generate AI profile registry
        registry_file = self._generate_ai_profile_registry(ai_profile_entries)
        if registry_file:
            results["registry"] = registry_file

        return results

    def _generate_data_ai_profile_resource(self, ai_profile: Dict[str, Any]) -> Optional[str]:
        """
        Generate an AI profile resource in the data directory structure.

        Args:
            ai_profile: AI profile data dictionary

        Returns:
            Path to generated resource file, or None if generation failed
        """
        try:
            profile_name = ai_profile.get("name", "unknown_ai_profile")
            safe_name = self._sanitize_filename(profile_name)

            # Create .tres resource content
            resource_content = self._create_ai_profile_resource_content(ai_profile)

            # Write resource file in data directory
            output_path = self.data_dir / f"{safe_name}.tres"

            if self._write_resource_file(resource_content, output_path):
                logger.info(f"Generated data AI profile resource: {output_path}")
                self.generated_resources.append(str(output_path))
                return str(output_path)
            else:
                self.failed_resources.append(profile_name)
                return None

        except Exception as e:
            profile_name = ai_profile.get("name", "unknown")
            logger.error(
                f"Error generating data AI profile resource for {profile_name}: {e}"
            )
            self.failed_resources.append(profile_name)
            return None

    def _create_ai_profile_resource_content(self, ai_profile: Dict[str, Any]) -> str:
        """
        Create .tres resource content for AIProfileResource with complete property mapping.

        Args:
            ai_profile: AI profile data dictionary

        Returns:
            Formatted .tres resource content string
        """
        # Extract all AI profile properties with proper defaults
        profile_name = ai_profile.get("name", "Unknown AI Profile")
        default_profile = ai_profile.get("default_profile", "")
        
        # Create resource content with all properties
        resource_content = self._create_tres_header("Resource", "AIProfileResource")

        # Add script reference
        resource_content += (
            self._create_ext_resource_entry(
                "Script", "res://scripts/resources/ai_profile_resource.gd", "1"
            )
            + "\n\n"
        )

        # Add resource properties
        properties = {
            "script": 'ExtResource("1")',
            "name": profile_name,
            "default_profile": default_profile,
        }
        
        # Add difficulty scaling properties
        difficulty_props = [
            "primary_weapon_delay", "secondary_weapon_delay", "shield_manage_delay",
            "predict_position_delay", "in_range_time", "accuracy_scale", "evasion_scale",
            "courage_scale", "use_countermeasures", "evade_missiles", "allow_player_targeting",
            "ai_aims_at_friendly", "respect_player_orders"
        ]
        
        for prop in difficulty_props:
            if prop in ai_profile:
                properties[prop] = ai_profile[prop]

        resource_content += self._create_resource_section(properties)

        return resource_content

    def _generate_ai_profile_registry(
        self, ai_profile_entries: List[Dict[str, Any]]
    ) -> Optional[str]:
        """
        Generate AI profile registry resource file.

        Args:
            ai_profile_entries: List of AI profile entry dictionaries

        Returns:
            Path to generated registry file, or None if generation failed
        """
        try:
            registry_content = self._create_tres_header(
                "Resource", "AIProfileRegistryData"
            )

            # Add script reference
            registry_content += (
                self._create_ext_resource_entry(
                    "Script", "res://scripts/systems/ai_profile_registry_data.gd", "1"
                )
                + "\n\n"
            )

            # Create AI profiles dictionary
            profiles_dict = {}
            for ai_profile in ai_profile_entries:
                profile_name = ai_profile.get("name", "unknown")
                safe_name = self._sanitize_filename(profile_name)
                # Reference to data-based resource
                resource_path = f"res://assets/data/ai/profiles/{safe_name}.tres"
                profiles_dict[profile_name] = resource_path

            # Add resource section with AI profiles registry
            registry_content += self._create_resource_section({"profiles": profiles_dict})

            # Write registry file in data directory
            registry_path = self.data_dir.parent / "ai_profile_registry.tres"

            if self._write_resource_file(registry_content, registry_path):
                logger.info(f"Generated AI profile registry: {registry_path}")
                self.generated_resources.append(str(registry_path))
                return str(registry_path)
            else:
                self.failed_resources.append("ai_profile_registry")
                return None

        except Exception as e:
            logger.error(f"Error generating AI profile registry: {e}")
            self.failed_resources.append("ai_profile_registry")
            return None