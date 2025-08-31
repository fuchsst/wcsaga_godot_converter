#!/usr/bin/env python3
"""
IFF Resource Generator

Generates .tres IFFResource files from iff_defs.tbl data following the
data-based organization structure: /assets/data/iff/{iff_name}.tres
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .base_resource_generator import ResourceGenerator
from ..core.catalog.asset_catalog import AssetCatalog
from ..core.relationship_builder import RelationshipBuilder

logger = logging.getLogger(__name__)


class IFFResourceGenerator(ResourceGenerator):
    """Generates IFFResource .tres resource files from parsed IFF table data following data-based organization"""

    def __init__(
        self,
        asset_catalog: AssetCatalog,
        relationship_builder: RelationshipBuilder,
        output_dir: Union[str, Path],
    ):
        """
        Initialize the IFF resource generator.

        Args:
            asset_catalog: Enhanced asset catalog instance
            relationship_builder: Relationship builder instance
            output_dir: Output directory for generated resources
        """
        super().__init__(asset_catalog, relationship_builder, output_dir)

        # Create the data directory for IFF definitions
        self.data_dir = self.output_dir / "assets" / "data" / "iff"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def generate_resource(self, asset_id: str) -> Optional[str]:
        """
        Generate a Godot resource for the specified IFF asset.

        Args:
            asset_id: ID of the IFF asset to generate resource for

        Returns:
            Path to generated resource file, or None if generation failed
        """
        # Look up IFF in asset catalog
        asset_entry = self.asset_catalog.get_asset(asset_id)
        if not asset_entry:
            logger.warning(f"IFF asset not found: {asset_id}")
            return None

        # Generate data-based IFF resource
        data_resource_file = self._generate_data_iff_resource(asset_entry.metadata)
        if not data_resource_file:
            return None

        return data_resource_file

    def validate_resource(self, resource_path: Union[str, Path]) -> bool:
        """
        Validate a generated IFF resource file.

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

    def generate_iff_resources(
        self, iff_entries: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Generate .tres resource files for all IFF entries following data-based organization.

        Args:
            iff_entries: List of parsed IFF entry dictionaries

        Returns:
            Dictionary mapping IFF names to generated resource paths
        """
        results = {}

        for iff in iff_entries:
            try:
                # Generate data-based IFF resource
                data_resource_file = self._generate_data_iff_resource(iff)
                if data_resource_file:
                    iff_name = iff.get("name", "unknown_iff")
                    results[iff_name] = data_resource_file

            except Exception as e:
                iff_name = iff.get("name", "unknown")
                logger.error(
                    f"Error generating resources for IFF {iff_name}: {e}"
                )
                continue

        # Generate IFF registry
        registry_file = self._generate_iff_registry(iff_entries)
        if registry_file:
            results["registry"] = registry_file

        return results

    def _generate_data_iff_resource(self, iff: Dict[str, Any]) -> Optional[str]:
        """
        Generate an IFF resource in the data directory structure.

        Args:
            iff: IFF data dictionary

        Returns:
            Path to generated resource file, or None if generation failed
        """
        try:
            iff_name = iff.get("name", "unknown_iff")
            safe_name = self._sanitize_filename(iff_name)

            # Create .tres resource content
            resource_content = self._create_iff_resource_content(iff)

            # Write resource file in data directory
            output_path = self.data_dir / f"{safe_name}.tres"

            if self._write_resource_file(resource_content, output_path):
                logger.info(f"Generated data IFF resource: {output_path}")
                self.generated_resources.append(str(output_path))
                return str(output_path)
            else:
                self.failed_resources.append(iff_name)
                return None

        except Exception as e:
            iff_name = iff.get("name", "unknown")
            logger.error(
                f"Error generating data IFF resource for {iff_name}: {e}"
            )
            self.failed_resources.append(iff_name)
            return None

    def _create_iff_resource_content(self, iff: Dict[str, Any]) -> str:
        """
        Create .tres resource content for IFFResource with complete property mapping.

        Args:
            iff: IFF data dictionary

        Returns:
            Formatted .tres resource content string
        """
        # Extract all IFF properties with proper defaults
        iff_name = iff.get("name", "Unknown IFF")
        
        # Color handling - convert RGB values to Color format
        color = iff.get("color", [255, 255, 255])
        if isinstance(color, list) and len(color) >= 3:
            # Convert 0-255 RGB values to 0-1 range for Godot Color
            r = color[0] / 255.0
            g = color[1] / 255.0
            b = color[2] / 255.0
            display_color = f"Color({r}, {g}, {b}, 1)"
        else:
            display_color = "Color(1, 1, 1, 1)"  # Default white

        # Attacks list
        attacks = iff.get("attacks", [])
        
        # Flags
        flags = iff.get("flags", [])
        
        # Default ship flags
        default_ship_flags = iff.get("default_ship_flags", [])
        default_ship_flags2 = iff.get("default_ship_flags2", [])
        
        # Perceptions dictionary
        perceptions = iff.get("sees_as", {})
        formatted_perceptions = {}
        for target_iff, color_values in perceptions.items():
            if isinstance(color_values, list) and len(color_values) >= 3:
                # Convert 0-255 RGB values to 0-1 range for Godot Color
                r = color_values[0] / 255.0
                g = color_values[1] / 255.0
                b = color_values[2] / 255.0
                formatted_perceptions[target_iff] = f"Color({r}, {g}, {b}, 1)"

        # Create resource content with all properties
        resource_content = self._create_tres_header("Resource", "IFFResource")

        # Add script reference
        resource_content += (
            self._create_ext_resource_entry(
                "Script", "res://scripts/resources/iff_resource.gd", "1"
            )
            + "\n\n"
        )

        # Add resource properties
        properties = {
            "script": 'ExtResource("1")',
            "name": iff_name,
            "display_color": display_color,
            "attacks": attacks,
            "flags": flags,
            "default_ship_flags": default_ship_flags,
            "default_ship_flags2": default_ship_flags2,
        }
        
        # Add perceptions if they exist
        if formatted_perceptions:
            properties["perceptions"] = formatted_perceptions

        resource_content += self._create_resource_section(properties)

        return resource_content

    def _generate_iff_registry(
        self, iff_entries: List[Dict[str, Any]]
    ) -> Optional[str]:
        """
        Generate IFF registry resource file.

        Args:
            iff_entries: List of IFF entry dictionaries

        Returns:
            Path to generated registry file, or None if generation failed
        """
        try:
            registry_content = self._create_tres_header(
                "Resource", "IFFRegistryData"
            )

            # Add script reference
            registry_content += (
                self._create_ext_resource_entry(
                    "Script", "res://scripts/systems/iff_registry_data.gd", "1"
                )
                + "\n\n"
            )

            # Create IFFs dictionary
            iffs_dict = {}
            for iff in iff_entries:
                iff_name = iff.get("name", "unknown")
                safe_name = self._sanitize_filename(iff_name)
                # Reference to data-based resource
                resource_path = f"res://assets/data/iff/{safe_name}.tres"
                iffs_dict[iff_name] = resource_path

            # Add resource section with IFFs registry
            registry_content += self._create_resource_section({"iffs": iffs_dict})

            # Write registry file in data directory
            registry_path = self.data_dir / "iff_registry.tres"

            if self._write_resource_file(registry_content, registry_path):
                logger.info(f"Generated IFF registry: {registry_path}")
                self.generated_resources.append(str(registry_path))
                return str(registry_path)
            else:
                self.failed_resources.append("iff_registry")
                return None

        except Exception as e:
            logger.error(f"Error generating IFF registry: {e}")
            self.failed_resources.append("iff_registry")
            return None

    def _sanitize_filename(self, name: str) -> str:
        """
        Convert IFF name to valid filename following Godot conventions.

        Args:
            name: IFF name to sanitize

        Returns:
            Sanitized filename
        """
        # Remove invalid characters and spaces
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
        safe_name = safe_name.lower().strip("_")
        return safe_name or "unnamed_iff"