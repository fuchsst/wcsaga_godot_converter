"""
Validation Framework - Validates converted assets and file structure

This module provides comprehensive validation for the converted Godot project,
ensuring all assets are correctly converted and organized according to the
target structure concepts.

Author: Qwen Code Assistant
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

from ..core.catalog.enhanced_asset_catalog import EnhancedAssetCatalog
from ..core.relationship_builder import RelationshipBuilder

logger = logging.getLogger(__name__)


class ValidationFramework:
    """
    Validates converted assets and file structure for correctness and completeness.
    """

    def __init__(
        self,
        asset_catalog: EnhancedAssetCatalog,
        relationship_builder: RelationshipBuilder,
        project_root: Path,
    ):
        """
        Initialize the validation framework.

        Args:
            asset_catalog: Enhanced asset catalog with all assets
            relationship_builder: Relationship builder with asset relationships
            project_root: Root directory of the Godot project
        """
        self.asset_catalog = asset_catalog
        self.relationship_builder = relationship_builder
        self.project_root = project_root

        # Validation results
        self.validation_results: Dict[str, List[str]] = {
            "errors": [],
            "warnings": [],
            "info": [],
        }

        # Required directories and files
        self.required_structure = {
            "directories": [
                "addons",
                "core",
                "data",
                "data/ships",
                "data/weapons",
                "data/ai",
                "data/missions",
                "data/campaigns",
                "data/effects",
                "data/config",
                "entities",
                "entities/fighters",
                "entities/capital_ships",
                "entities/projectiles",
                "entities/weapons",
                "entities/effects",
                "entities/environment",
                "systems",
                "systems/ai",
                "systems/mission_control",
                "systems/weapon_control",
                "systems/physics",
                "systems/audio",
                "systems/graphics",
                "systems/networking",
                "ui",
                "ui/main_menu",
                "ui/hud",
                "ui/briefing",
                "ui/debriefing",
                "ui/options",
                "ui/tech_database",
                "ui/components",
                "ui/themes",
                "missions",
                "campaigns",
                "docs",
            ],
            "files": ["project.godot", "README.md"],
        }

    def validate_all(self) -> Dict[str, List[str]]:
        """
        Run all validation checks.

        Returns:
            Dictionary with validation results
        """
        logger.info("Starting comprehensive validation...")

        # Clear previous results
        self.validation_results = {"errors": [], "warnings": [], "info": []}

        # Run individual validations
        self._validate_project_structure()
        self._validate_asset_catalog()
        self._validate_asset_relationships()
        self._validate_resource_files()
        self._validate_scene_files()
        self._validate_media_files()
        self._validate_cross_references()

        # Log summary
        error_count = len(self.validation_results["errors"])
        warning_count = len(self.validation_results["warnings"])
        info_count = len(self.validation_results["info"])

        logger.info(
            f"Validation complete - Errors: {error_count}, Warnings: {warning_count}, Info: {info_count}"
        )

        return self.validation_results

    def _validate_project_structure(self) -> None:
        """Validate the basic project directory structure."""
        logger.debug("Validating project structure...")

        # Check required directories exist
        for required_dir in self.required_structure["directories"]:
            dir_path = self.project_root / required_dir
            if not dir_path.exists():
                self.validation_results["errors"].append(
                    f"Required directory missing: {required_dir}"
                )
            elif not dir_path.is_dir():
                self.validation_results["errors"].append(
                    f"Required path is not a directory: {required_dir}"
                )
            else:
                self.validation_results["info"].append(
                    f"Found required directory: {required_dir}"
                )

        # Check required files exist
        for required_file in self.required_structure["files"]:
            file_path = self.project_root / required_file
            if not file_path.exists():
                self.validation_results["errors"].append(
                    f"Required file missing: {required_file}"
                )
            elif not file_path.is_file():
                self.validation_results["errors"].append(
                    f"Required path is not a file: {required_file}"
                )
            else:
                self.validation_results["info"].append(
                    f"Found required file: {required_file}"
                )

    def _validate_asset_catalog(self) -> None:
        """Validate the asset catalog completeness."""
        logger.debug("Validating asset catalog...")

        if not self.asset_catalog.assets:
            self.validation_results["warnings"].append(
                "Asset catalog is empty - no assets registered"
            )
            return

        # Check for assets without proper metadata
        assets_without_type = []
        assets_without_category = []
        assets_without_file = []

        for asset_id, asset in self.asset_catalog.assets.items():
            if not asset.asset_type:
                assets_without_type.append(asset_id)

            if not asset.category:
                assets_without_category.append(asset_id)

            if not asset.file_path or not Path(asset.file_path).exists():
                assets_without_file.append(asset_id)

        if assets_without_type:
            self.validation_results["warnings"].append(
                f"Assets without type: {len(assets_without_type)}"
            )

        if assets_without_category:
            self.validation_results["warnings"].append(
                f"Assets without category: {len(assets_without_category)}"
            )

        if assets_without_file:
            self.validation_results["errors"].append(
                f"Assets with missing files: {len(assets_without_file)}"
            )

    def _validate_asset_relationships(self) -> None:
        """Validate asset relationships for consistency."""
        logger.debug("Validating asset relationships...")

        # Check for circular dependencies
        circular_deps = self.asset_catalog.validate_dependency_graph()
        if circular_deps:
            for chain in circular_deps:
                self.validation_results["errors"].append(
                    f"Circular dependency detected: {chain}"
                )

        # Check for missing dependencies
        missing_deps = []
        for asset_id in self.asset_catalog.assets:
            dependencies = self.asset_catalog.get_assets_by_dependency(asset_id)
            for dep in dependencies:
                if dep.asset_id not in self.asset_catalog.assets:
                    missing_deps.append((asset_id, dep.asset_id))

        if missing_deps:
            for source, target in missing_deps:
                self.validation_results["errors"].append(
                    f"Missing dependency: {source} -> {target}"
                )

    def _validate_resource_files(self) -> None:
        """Validate Godot resource files (.tres)."""
        logger.debug("Validating resource files...")

        # Find all .tres files
        tres_files = list(self.project_root.rglob("*.tres"))
        logger.debug(f"Found {len(tres_files)} .tres files")

        # Validate each .tres file
        for tres_file in tres_files:
            try:
                self._validate_tres_file(tres_file)
            except Exception as e:
                self.validation_results["errors"].append(
                    f"Failed to validate .tres file {tres_file}: {e}"
                )

    def _validate_tres_file(self, tres_file: Path) -> None:
        """
        Validate a single .tres file.

        Args:
            tres_file: Path to the .tres file
        """
        # Check file can be parsed
        try:
            with open(tres_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Basic checks for Godot .tres format
            if not content.startswith("[gd_resource"):
                self.validation_results["errors"].append(
                    f"Invalid .tres file format: {tres_file}"
                )
                return

            # Check for required sections
            if "[resource]" not in content:
                self.validation_results["warnings"].append(
                    f".tres file missing [resource] section: {tres_file}"
                )

            self.validation_results["info"].append(
                f"Validated .tres file: {tres_file.name}"
            )

        except Exception as e:
            self.validation_results["errors"].append(
                f"Error reading .tres file {tres_file}: {e}"
            )

    def _validate_scene_files(self) -> None:
        """Validate Godot scene files (.tscn)."""
        logger.debug("Validating scene files...")

        # Find all .tscn files
        tscn_files = list(self.project_root.rglob("*.tscn"))
        logger.debug(f"Found {len(tscn_files)} .tscn files")

        # Validate each .tscn file
        for tscn_file in tscn_files:
            try:
                self._validate_tscn_file(tscn_file)
            except Exception as e:
                self.validation_results["errors"].append(
                    f"Failed to validate .tscn file {tscn_file}: {e}"
                )

    def _validate_tscn_file(self, tscn_file: Path) -> None:
        """
        Validate a single .tscn file.

        Args:
            tscn_file: Path to the .tscn file
        """
        # Check file can be parsed
        try:
            with open(tscn_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Basic checks for Godot .tscn format
            if not content.startswith("[gd_scene"):
                self.validation_results["errors"].append(
                    f"Invalid .tscn file format: {tscn_file}"
                )
                return

            self.validation_results["info"].append(
                f"Validated .tscn file: {tscn_file.name}"
            )

        except Exception as e:
            self.validation_results["errors"].append(
                f"Error reading .tscn file {tscn_file}: {e}"
            )

    def _validate_media_files(self) -> None:
        """Validate media files (textures, audio, etc.)."""
        logger.debug("Validating media files...")

        # Check for common media file types
        media_extensions = {
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
            ".ogg",
            ".wav",
            ".glb",
            ".gltf",
        }
        media_files = [
            f
            for f in self.project_root.rglob("*")
            if f.is_file() and f.suffix.lower() in media_extensions
        ]

        logger.debug(f"Found {len(media_files)} media files")

        # Basic validation - just check they exist and are readable
        for media_file in media_files:
            try:
                # Just check if file is readable
                with open(media_file, "rb") as f:
                    f.read(1)  # Read first byte to check readability

                self.validation_results["info"].append(
                    f"Validated media file: {media_file.name}"
                )

            except Exception as e:
                self.validation_results["errors"].append(
                    f"Error reading media file {media_file}: {e}"
                )

    def _validate_cross_references(self) -> None:
        """Validate cross-references between assets."""
        logger.debug("Validating cross-references...")

        # Check that referenced assets exist
        for asset_id, asset in self.asset_catalog.assets.items():
            # Check dependencies
            for dep_id in asset.dependencies:
                if dep_id not in self.asset_catalog.assets:
                    self.validation_results["errors"].append(
                        f"Asset {asset_id} references missing dependency: {dep_id}"
                    )

            # Check dependents
            for dep_id in asset.dependents:
                if dep_id not in self.asset_catalog.assets:
                    self.validation_results["errors"].append(
                        f"Asset {asset_id} has missing dependent: {dep_id}"
                    )

    def generate_validation_report(self, output_file: Optional[Path] = None) -> str:
        """
        Generate a comprehensive validation report.

        Args:
            output_file: Optional path to save report to file

        Returns:
            Validation report as string
        """
        # Generate report
        report_lines = [
            "Wing Commander Saga to Godot Conversion - Validation Report",
            "=" * 60,
            "",
            f"Project Root: {self.project_root}",
            f"Report Generated: {self._get_timestamp()}",
            "",
            "Summary:",
            f"  Errors: {len(self.validation_results['errors'])}",
            f"  Warnings: {len(self.validation_results['warnings'])}",
            f"  Info: {len(self.validation_results['info'])}",
            "",
        ]

        # Add detailed results
        if self.validation_results["errors"]:
            report_lines.append("Errors:")
            report_lines.append("-" * 10)
            for error in self.validation_results["errors"]:
                report_lines.append(f"  - {error}")
            report_lines.append("")

        if self.validation_results["warnings"]:
            report_lines.append("Warnings:")
            report_lines.append("-" * 10)
            for warning in self.validation_results["warnings"]:
                report_lines.append(f"  - {warning}")
            report_lines.append("")

        if self.validation_results["info"]:
            report_lines.append("Information:")
            report_lines.append("-" * 12)
            # Limit info messages to avoid overly long reports
            info_count = len(self.validation_results["info"])
            display_count = min(info_count, 50)  # Show first 50 info messages
            for i in range(display_count):
                report_lines.append(f"  - {self.validation_results['info'][i]}")
            if info_count > display_count:
                report_lines.append(
                    f"  ... and {info_count - display_count} more info messages"
                )
            report_lines.append("")

        # Add statistics
        report_lines.extend(
            [
                "Statistics:",
                "-" * 10,
                f"  Total Assets Cataloged: {len(self.asset_catalog.assets)}",
                f"  Total Relationships: {sum(len(rels) for rels in self.asset_catalog.enhanced_relationships.values())}",
                f"  Total Resource Files (.tres): {len(list(self.project_root.rglob('*.tres')))}",
                f"  Total Scene Files (.tscn): {len(list(self.project_root.rglob('*.tscn')))}",
                f"  Total Media Files: {len(list(self.project_root.rglob('*')))}",
            ]
        )

        report_content = "\n".join(report_lines)

        # Save to file if requested
        if output_file:
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(report_content)
                logger.info(f"Validation report saved to: {output_file}")
            except Exception as e:
                logger.error(f"Failed to save validation report: {e}")

        return report_content

    def _get_timestamp(self) -> str:
        """Get current timestamp as string."""
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
