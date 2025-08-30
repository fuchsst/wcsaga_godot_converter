#!/usr/bin/env python3
"""
Base Resource Generator

This module provides the base ResourceGenerator class that all specific
resource generators inherit from. It implements common functionality for
generating Godot-compatible resource files.

Author: Qwen Code Assistant
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ..core.catalog.asset_catalog import AssetCatalog
from ..core.relationship_builder import RelationshipBuilder

logger = logging.getLogger(__name__)


class ResourceGenerator(ABC):
    """
    Abstract base class for all resource generators.

    This class provides common functionality for generating Godot-compatible
    resource files (.tres) from asset metadata, using an AssetCatalog
    for asset lookup and a RelationshipBuilder for relationship resolution.
    """

    def __init__(
        self,
        asset_catalog: AssetCatalog,
        relationship_builder: RelationshipBuilder,
        output_dir: Union[str, Path],
    ):
        """
        Initialize the resource generator.

        Args:
            asset_catalog: Enhanced asset catalog instance
            relationship_builder: Relationship builder instance
            output_dir: Output directory for generated resources
        """
        self.asset_catalog = asset_catalog
        self.relationship_builder = relationship_builder
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Resource tracking
        self.generated_resources: List[str] = []
        self.failed_resources: List[str] = []

        logger.info(f"Initialized {self.__class__.__name__}")

    @abstractmethod
    def generate_resource(self, asset_id: str) -> Optional[str]:
        """
        Generate a Godot resource for the specified asset.

        This method must be implemented by subclasses.

        Args:
            asset_id: ID of the asset to generate resource for

        Returns:
            Path to generated resource file, or None if generation failed
        """
        pass

    @abstractmethod
    def validate_resource(self, resource_path: Union[str, Path]) -> bool:
        """
        Validate a generated resource file.

        This method must be implemented by subclasses.

        Args:
            resource_path: Path to the resource file to validate

        Returns:
            True if resource is valid, False otherwise
        """
        pass

    def generate_resources(self, asset_ids: List[str]) -> Dict[str, str]:
        """
        Generate resources for multiple assets.

        Args:
            asset_ids: List of asset IDs to generate resources for

        Returns:
            Dictionary mapping asset IDs to generated resource paths
        """
        results = {}

        for asset_id in asset_ids:
            try:
                resource_path = self.generate_resource(asset_id)
                if resource_path:
                    results[asset_id] = resource_path
                    self.generated_resources.append(resource_path)
                    logger.debug(f"Generated resource for {asset_id}: {resource_path}")
                else:
                    self.failed_resources.append(asset_id)
                    logger.warning(f"Failed to generate resource for {asset_id}")

            except Exception as e:
                self.failed_resources.append(asset_id)
                logger.error(f"Error generating resource for {asset_id}: {e}")
                continue

        return results

    def validate_resources(
        self, resource_paths: List[Union[str, Path]]
    ) -> Dict[str, bool]:
        """
        Validate multiple resource files.

        Args:
            resource_paths: List of resource file paths to validate

        Returns:
            Dictionary mapping resource paths to validation results
        """
        results = {}

        for resource_path in resource_paths:
            try:
                is_valid = self.validate_resource(resource_path)
                results[str(resource_path)] = is_valid
                logger.debug(
                    f"Resource validation {'passed' if is_valid else 'failed'}: {resource_path}"
                )

            except Exception as e:
                results[str(resource_path)] = False
                logger.error(f"Error validating resource {resource_path}: {e}")
                continue

        return results

    def get_generation_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about resource generation.

        Returns:
            Dictionary with generation statistics
        """
        total_generated = len(self.generated_resources)
        total_failed = len(self.failed_resources)
        total_attempted = total_generated + total_failed

        success_rate = total_generated / total_attempted if total_attempted > 0 else 0.0

        return {
            "total_generated": total_generated,
            "total_failed": total_failed,
            "total_attempted": total_attempted,
            "success_rate": success_rate,
            "generated_resources": self.generated_resources.copy(),
            "failed_resources": self.failed_resources.copy(),
        }

    def _create_tres_header(
        self,
        resource_type: str,
        script_class: Optional[str] = None,
        load_steps: int = 2,
        format_version: int = 3,
    ) -> str:
        """
        Create a standard Godot .tres file header.

        Args:
            resource_type: Type of resource (e.g., "Resource", "ShipClass")
            script_class: Optional script class name
            load_steps: Number of load steps
            format_version: Format version

        Returns:
            TRES file header string
        """
        header_lines = [f'[gd_resource type="{resource_type}"']

        if script_class:
            header_lines[0] += f' script_class="{script_class}"'

        header_lines[0] += f" load_steps={load_steps} format={format_version}]"
        header_lines.append("")  # Empty line after header

        return "\n".join(header_lines)

    def _create_ext_resource_entry(
        self, resource_type: str, path: str, resource_id: str
    ) -> str:
        """
        Create an external resource entry.

        Args:
            resource_type: Type of external resource
            path: Path to the external resource
            resource_id: ID for the resource reference

        Returns:
            External resource entry string
        """
        return f'[ext_resource type="{resource_type}" path="{path}" id="{resource_id}"]'

    def _create_resource_section(self, properties: Dict[str, Any]) -> str:
        """
        Create the resource section with properties.

        Args:
            properties: Dictionary of resource properties

        Returns:
            Resource section string
        """
        lines = ["[resource]"]

        for key, value in properties.items():
            formatted_value = self._format_value(value)
            lines.append(f"{key} = {formatted_value}")

        return "\n".join(lines)

    def _format_value(self, value: Any) -> str:
        """
        Format a value for inclusion in a .tres file.

        Args:
            value: Value to format

        Returns:
            Formatted string representation
        """
        if isinstance(value, str):
            # Escape quotes and backslashes
            escaped = value.replace("\\", "\\\\").replace('"', '\\"')
            return f'"{escaped}"'
        elif isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, list):
            formatted_items = [self._format_value(item) for item in value]
            return "[" + ", ".join(formatted_items) + "]"
        elif isinstance(value, dict):
            formatted_items = [
                f'"{k}": {self._format_value(v)}' for k, v in value.items()
            ]
            return "{" + ", ".join(formatted_items) + "}"
        elif hasattr(value, "__dict__"):
            # Handle dataclass objects
            return self._format_value(asdict(value))
        else:
            return str(value)

    def _write_resource_file(
        self, content: str, file_path: Union[str, Path], create_dirs: bool = True
    ) -> bool:
        """
        Write resource content to a file.

        Args:
            content: Content to write
            file_path: Path to write to
            create_dirs: Whether to create parent directories

        Returns:
            True if write was successful, False otherwise
        """
        try:
            file_path = Path(file_path)

            if create_dirs:
                file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            logger.debug(f"Wrote resource file: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to write resource file {file_path}: {e}")
            return False

    def _sanitize_filename(self, name: str) -> str:
        """
        Sanitize a name for use as a filename.

        Args:
            name: Name to sanitize

        Returns:
            Sanitized filename
        """
        # Replace invalid characters with underscores
        sanitized = "".join(c if c.isalnum() or c in "-_." else "_" for c in name)

        # Remove multiple consecutive underscores
        while "__" in sanitized:
            sanitized = sanitized.replace("__", "_")

        # Remove leading/trailing underscores and dots
        sanitized = sanitized.strip("_.")

        # Ensure it's not empty
        if not sanitized:
            sanitized = "unnamed_resource"

        return sanitized.lower()

    def _get_asset_faction(self, asset_name: str) -> str:
        """
        Determine faction from asset name using WCS naming conventions.

        Args:
            asset_name: Name of the asset

        Returns:
            Faction name
        """
        name_lower = asset_name.lower()

        # Terran Confederation patterns
        terran_patterns = [
            "gtf_",
            "gtb_",
            "gtc_",
            "gtd_",
            "gtt_",
            "gta_",
            "confed",
            "terran",
            "tc_",
            "hermes",
        ]
        if any(pattern in name_lower for pattern in terran_patterns):
            return "terran"

        # Kilrathi patterns
        kilrathi_patterns = [
            "kaf_",
            "kab_",
            "kac_",
            "kad_",
            "kat_",
            "k_",
            "kilrathi",
            "dralthi",
            "salthi",
            "gratha",
            "jalthi",
        ]
        if any(pattern in name_lower for pattern in kilrathi_patterns):
            return "kilrathi"

        # Vasudan patterns
        vasudan_patterns = ["pvf_", "pvb_", "pvc_", "pvd_", "pva_", "vasudan"]
        if any(pattern in name_lower for pattern in vasudan_patterns):
            return "vasudan"

        # Shivan patterns
        shivan_patterns = ["sf_", "sb_", "sc_", "sd_", "sj_", "shivan"]
        if any(pattern in name_lower for pattern in shivan_patterns):
            return "shivan"

        # Pirate/Bandit patterns
        pirate_patterns = ["pirate", "bandit", "corsair", "privateer"]
        if any(pattern in name_lower for pattern in pirate_patterns):
            return "pirate"

        # Default to terran for unknown
        return "terran"

    def _get_asset_category(self, asset_name: str, asset_type: str) -> str:
        """
        Determine category from asset name and type.

        Args:
            asset_name: Name of the asset
            asset_type: Type of the asset

        Returns:
            Category name
        """
        name_lower = asset_name.lower()

        # Ship categories
        if asset_type == "ship":
            if any(
                pattern in name_lower
                for pattern in ["fighter", "interceptor", "stealth"]
            ):
                return "fighters"
            elif any(pattern in name_lower for pattern in ["bomber", "assault"]):
                return "bombers"
            elif any(pattern in name_lower for pattern in ["corvette", "gunboat"]):
                return "corvettes"
            elif any(pattern in name_lower for pattern in ["cruiser", "destroyer"]):
                return "cruisers"
            elif any(
                pattern in name_lower
                for pattern in ["capital", "dreadnought", "carrier"]
            ):
                return "capital_ships"
            elif any(
                pattern in name_lower for pattern in ["transport", "cargo", "freighter"]
            ):
                return "transports"
            else:
                return "fighters"  # Default

        # Weapon categories
        elif asset_type == "weapon":
            if any(pattern in name_lower for pattern in ["laser", "beam"]):
                return "beams"
            elif any(
                pattern in name_lower for pattern in ["missile", "torpedo", "rocket"]
            ):
                return "missiles"
            elif any(pattern in name_lower for pattern in ["flak", "aa", "anti-air"]):
                return "aa_weapons"
            else:
                return "primary_weapons"  # Default

        # Effect categories
        elif asset_type == "effect":
            if "explosion" in name_lower:
                return "explosions"
            elif "engine" in name_lower or "thruster" in name_lower:
                return "engines"
            elif "shield" in name_lower:
                return "shields"
            else:
                return "general"

        # Default category
        return "misc"
