#!/usr/bin/env python3
"""
AI Behavior Resource Generator

Generates .tres AIBehaviorResource files from ai.tbl data following the
data-based organization structure: /assets/data/ai/{behavior_name}.tres
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .base_resource_generator import ResourceGenerator
from ..core.catalog.asset_catalog import AssetCatalog
from ..core.relationship_builder import RelationshipBuilder

logger = logging.getLogger(__name__)


class AIBehaviorResourceGenerator(ResourceGenerator):
    """Generates AIBehaviorResource .tres resource files from parsed AI behavior table data following data-based organization"""

    def __init__(
        self,
        asset_catalog: AssetCatalog,
        relationship_builder: RelationshipBuilder,
        output_dir: Union[str, Path],
    ):
        """
        Initialize the AI behavior resource generator.

        Args:
            asset_catalog: Enhanced asset catalog instance
            relationship_builder: Relationship builder instance
            output_dir: Output directory for generated resources
        """
        super().__init__(asset_catalog, relationship_builder, output_dir)

        # Create the data directory for AI behavior definitions
        self.data_dir = self.output_dir / "assets" / "data" / "ai"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def generate_resource(self, asset_id: str) -> Optional[str]:
        """
        Generate a Godot resource for the specified AI behavior asset.

        Args:
            asset_id: ID of the AI behavior asset to generate resource for

        Returns:
            Path to generated resource file, or None if generation failed
        """
        # Look up AI behavior in asset catalog
        asset_entry = self.asset_catalog.get_asset(asset_id)
        if not asset_entry:
            logger.warning(f"AI behavior asset not found: {asset_id}")
            return None

        # Generate data-based AI behavior resource
        data_resource_file = self._generate_data_ai_behavior_resource(asset_entry.metadata)
        if not data_resource_file:
            return None

        return data_resource_file

    def validate_resource(self, resource_path: Union[str, Path]) -> bool:
        """
        Validate a generated AI behavior resource file.

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

    def generate_ai_behavior_resources(
        self, ai_behavior_entries: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Generate .tres resource files for all AI behavior entries following data-based organization.

        Args:
            ai_behavior_entries: List of parsed AI behavior entry dictionaries

        Returns:
            Dictionary mapping AI behavior names to generated resource paths
        """
        results = {}

        for ai_behavior in ai_behavior_entries:
            try:
                # Generate data-based AI behavior resource
                data_resource_file = self._generate_data_ai_behavior_resource(ai_behavior)
                if data_resource_file:
                    behavior_name = ai_behavior.get("name", "unknown_ai_behavior")
                    results[behavior_name] = data_resource_file

            except Exception as e:
                behavior_name = ai_behavior.get("name", "unknown")
                logger.error(
                    f"Error generating resources for AI behavior {behavior_name}: {e}"
                )
                continue

        # Generate AI behavior registry
        registry_file = self._generate_ai_behavior_registry(ai_behavior_entries)
        if registry_file:
            results["registry"] = registry_file

        return results

    def _generate_data_ai_behavior_resource(self, ai_behavior: Dict[str, Any]) -> Optional[str]:
        """
        Generate an AI behavior resource in the data directory structure.

        Args:
            ai_behavior: AI behavior data dictionary

        Returns:
            Path to generated resource file, or None if generation failed
        """
        try:
            behavior_name = ai_behavior.get("name", "unknown_ai_behavior")
            safe_name = self._sanitize_filename(behavior_name)

            # Create .tres resource content
            resource_content = self._create_ai_behavior_resource_content(ai_behavior)

            # Write resource file in data directory (avoid naming conflict with profiles directory)
            output_path = self.data_dir / f"{safe_name}_behavior.tres"

            if self._write_resource_file(resource_content, output_path):
                logger.info(f"Generated data AI behavior resource: {output_path}")
                self.generated_resources.append(str(output_path))
                return str(output_path)
            else:
                self.failed_resources.append(behavior_name)
                return None

        except Exception as e:
            behavior_name = ai_behavior.get("name", "unknown")
            logger.error(
                f"Error generating data AI behavior resource for {behavior_name}: {e}"
            )
            self.failed_resources.append(behavior_name)
            return None

    def _create_ai_behavior_resource_content(self, ai_behavior: Dict[str, Any]) -> str:
        """
        Create .tres resource content for AIBehaviorResource with complete property mapping.

        Args:
            ai_behavior: AI behavior data dictionary

        Returns:
            Formatted .tres resource content string
        """
        # Extract all AI behavior properties with proper defaults
        behavior_name = ai_behavior.get("name", "Unknown AI Behavior")
        
        # Create resource content with all properties
        resource_content = self._create_tres_header("Resource", "AIBehaviorResource")

        # Add script reference
        resource_content += (
            self._create_ext_resource_entry(
                "Script", "res://scripts/resources/ai_behavior_resource.gd", "1"
            )
            + "\n\n"
        )

        # Add resource properties
        properties = {
            "script": 'ExtResource("1")',
            "name": behavior_name,
        }
        
        # Add behavior properties
        behavior_props = [
            "accuracy", "evasion", "courage", "patience", "afterburner_use_factor",
            "shockwave_evade_chances", "get_away_chance", "secondary_range_multiplier",
            "bomb_range_multiplier", "autoscale_by_ai_class", "ai_countermeasure_firing_chance"
        ]
        
        for prop in behavior_props:
            if prop in ai_behavior:
                properties[prop] = ai_behavior[prop]

        resource_content += self._create_resource_section(properties)

        return resource_content

    def _generate_ai_behavior_registry(
        self, ai_behavior_entries: List[Dict[str, Any]]
    ) -> Optional[str]:
        """
        Generate AI behavior registry resource file.

        Args:
            ai_behavior_entries: List of AI behavior entry dictionaries

        Returns:
            Path to generated registry file, or None if generation failed
        """
        try:
            registry_content = self._create_tres_header(
                "Resource", "AIBehaviorRegistryData"
            )

            # Add script reference
            registry_content += (
                self._create_ext_resource_entry(
                    "Script", "res://scripts/systems/ai_behavior_registry_data.gd", "1"
                )
                + "\n\n"
            )

            # Create AI behaviors dictionary
            behaviors_dict = {}
            for ai_behavior in ai_behavior_entries:
                behavior_name = ai_behavior.get("name", "unknown")
                safe_name = self._sanitize_filename(behavior_name)
                # Reference to data-based resource
                resource_path = f"res://assets/data/ai/{safe_name}_behavior.tres"
                behaviors_dict[behavior_name] = resource_path

            # Add resource section with AI behaviors registry
            registry_content += self._create_resource_section({"behaviors": behaviors_dict})

            # Write registry file in data directory
            registry_path = self.data_dir / "ai_behavior_registry.tres"

            if self._write_resource_file(registry_content, registry_path):
                logger.info(f"Generated AI behavior registry: {registry_path}")
                self.generated_resources.append(str(registry_path))
                return str(registry_path)
            else:
                self.failed_resources.append("ai_behavior_registry")
                return None

        except Exception as e:
            logger.error(f"Error generating AI behavior registry: {e}")
            self.failed_resources.append("ai_behavior_registry")
            return None