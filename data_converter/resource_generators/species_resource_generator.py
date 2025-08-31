#!/usr/bin/env python3
"""
Species Resource Generator

Generates .tres SpeciesResource files from Species_defs.tbl data following the
data-based organization structure: /assets/data/species/{species_name}.tres
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .base_resource_generator import ResourceGenerator
from ..core.catalog.asset_catalog import AssetCatalog
from ..core.relationship_builder import RelationshipBuilder

logger = logging.getLogger(__name__)


class SpeciesResourceGenerator(ResourceGenerator):
    """Generates SpeciesResource .tres resource files from parsed species table data following data-based organization"""

    def __init__(
        self,
        asset_catalog: AssetCatalog,
        relationship_builder: RelationshipBuilder,
        output_dir: Union[str, Path],
    ):
        """
        Initialize the species resource generator.

        Args:
            asset_catalog: Enhanced asset catalog instance
            relationship_builder: Relationship builder instance
            output_dir: Output directory for generated resources
        """
        super().__init__(asset_catalog, relationship_builder, output_dir)

        # Create the data directory for species definitions
        self.data_dir = self.output_dir / "assets" / "data" / "species"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def generate_resource(self, asset_id: str) -> Optional[str]:
        """
        Generate a Godot resource for the specified species asset.

        Args:
            asset_id: ID of the species asset to generate resource for

        Returns:
            Path to generated resource file, or None if generation failed
        """
        # Look up species in asset catalog
        asset_entry = self.asset_catalog.get_asset(asset_id)
        if not asset_entry:
            logger.warning(f"Species asset not found: {asset_id}")
            return None

        # Generate data-based species resource
        data_resource_file = self._generate_data_species_resource(asset_entry.metadata)
        if not data_resource_file:
            return None

        return data_resource_file

    def validate_resource(self, resource_path: Union[str, Path]) -> bool:
        """
        Validate a generated species resource file.

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

    def generate_species_resources(
        self, species_entries: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Generate .tres resource files for all species entries following data-based organization.

        Args:
            species_entries: List of parsed species entry dictionaries

        Returns:
            Dictionary mapping species names to generated resource paths
        """
        results = {}

        for species in species_entries:
            try:
                # Generate data-based species resource
                data_resource_file = self._generate_data_species_resource(species)
                if data_resource_file:
                    species_name = species.get("name", "unknown_species")
                    results[species_name] = data_resource_file

            except Exception as e:
                species_name = species.get("name", "unknown")
                logger.error(
                    f"Error generating resources for species {species_name}: {e}"
                )
                continue

        # Generate species registry
        registry_file = self._generate_species_registry(species_entries)
        if registry_file:
            results["registry"] = registry_file

        return results

    def _generate_data_species_resource(self, species: Dict[str, Any]) -> Optional[str]:
        """
        Generate a species resource in the data directory structure.

        Args:
            species: Species data dictionary

        Returns:
            Path to generated resource file, or None if generation failed
        """
        try:
            species_name = species.get("name", "unknown_species")
            safe_name = self._sanitize_filename(species_name)

            # Create .tres resource content
            resource_content = self._create_species_resource_content(species)

            # Write resource file in data directory
            output_path = self.data_dir / f"{safe_name}.tres"

            if self._write_resource_file(resource_content, output_path):
                logger.info(f"Generated data species resource: {output_path}")
                self.generated_resources.append(str(output_path))
                return str(output_path)
            else:
                self.failed_resources.append(species_name)
                return None

        except Exception as e:
            species_name = species.get("name", "unknown")
            logger.error(
                f"Error generating data species resource for {species_name}: {e}"
            )
            self.failed_resources.append(species_name)
            return None

    def _create_species_resource_content(self, species: Dict[str, Any]) -> str:
        """
        Create .tres resource content for SpeciesResource with complete property mapping.

        Args:
            species: Species data dictionary

        Returns:
            Formatted .tres resource content string
        """
        # Extract all species properties with proper defaults
        species_name = species.get("name", "Unknown Species")
        default_iff = species.get("default_iff", "")
        default_armor = species.get("default_armor", "")
        color = species.get("color", "")
        
        # Create resource content with all properties
        resource_content = self._create_tres_header("Resource", "SpeciesResource")

        # Add script reference
        resource_content += (
            self._create_ext_resource_entry(
                "Script", "res://scripts/resources/species_resource.gd", "1"
            )
            + "\n\n"
        )

        # Add resource properties
        properties = {
            "script": 'ExtResource("1")',
            "name": species_name,
            "default_iff": default_iff,
            "default_armor": default_armor,
            "color": color,
        }
        
        # Add AI behavior properties
        ai_props = ["ai_aggression", "ai_caution", "ai_accuracy"]
        for prop in ai_props:
            if prop in species:
                properties[prop] = species[prop]

        # Add other properties
        other_props = [
            "debris_texture", "shield_hit_ani", "thrust_anims", "thrust_glows", "awacs_multiplier"
        ]
        for prop in other_props:
            if prop in species:
                properties[prop] = species[prop]

        resource_content += self._create_resource_section(properties)

        return resource_content

    def _generate_species_registry(
        self, species_entries: List[Dict[str, Any]]
    ) -> Optional[str]:
        """
        Generate species registry resource file.

        Args:
            species_entries: List of species entry dictionaries

        Returns:
            Path to generated registry file, or None if generation failed
        """
        try:
            registry_content = self._create_tres_header(
                "Resource", "SpeciesRegistryData"
            )

            # Add script reference
            registry_content += (
                self._create_ext_resource_entry(
                    "Script", "res://scripts/systems/species_registry_data.gd", "1"
                )
                + "\n\n"
            )

            # Create species dictionary
            species_dict = {}
            for species in species_entries:
                species_name = species.get("name", "unknown")
                safe_name = self._sanitize_filename(species_name)
                # Reference to data-based resource
                resource_path = f"res://assets/data/species/{safe_name}.tres"
                species_dict[species_name] = resource_path

            # Add resource section with species registry
            registry_content += self._create_resource_section({"species": species_dict})

            # Write registry file in data directory
            registry_path = self.data_dir.parent / "species_registry.tres"

            if self._write_resource_file(registry_content, registry_path):
                logger.info(f"Generated species registry: {registry_path}")
                self.generated_resources.append(str(registry_path))
                return str(registry_path)
            else:
                self.failed_resources.append("species_registry")
                return None

        except Exception as e:
            logger.error(f"Error generating species registry: {e}")
            self.failed_resources.append("species_registry")
            return None