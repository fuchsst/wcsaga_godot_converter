"""
Integration Orchestrator - Coordinates all conversion components

This module orchestrates the complete conversion pipeline, integrating:
1. Asset cataloging and relationship building
2. Resource generation for Godot assets
3. File structure creation following target concepts
4. Validation and quality assurance

Author: Qwen Code Assistant
"""

import logging
from pathlib import Path
from typing import Dict

from .core.catalog.asset_catalog import AssetCatalog
from .core.relationship_builder import RelationshipBuilder
from .core.catalog.asset_catalog import AssetMapping
from .resource_generators.base_resource_generator import ResourceGenerator
from .file_structure_creator.file_structure_creator import FileStructureCreator

logger = logging.getLogger(__name__)


class IntegrationOrchestrator:
    """
    Orchestrates the complete conversion pipeline from asset cataloging
    through resource generation to file structure creation.
    """

    def __init__(
        self, source_dir: str, output_dir: str, project_name: str = "wcs_godot"
    ):
        """
        Initialize the integration orchestrator.

        Args:
            source_dir: WCS source directory
            output_dir: Output directory for Godot project
            project_name: Name of the Godot project
        """
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.project_name = project_name

        # Initialize core components
        self.asset_catalog = AssetCatalog(
            catalog_path=str(self.output_dir / "asset_catalog.json"),
            db_path=str(self.output_dir / "asset_catalog.db"),
        )

        self.relationship_builder = RelationshipBuilder(
            source_dir=self.source_dir,
            target_structure={},  # Will be populated during processing
        )

        self.file_structure_creator = FileStructureCreator(
            asset_catalog=self.asset_catalog,
            relationship_builder=self.relationship_builder,
            output_root=self.output_dir / self.project_name,
        )

        # Resource generators (will be populated as needed)
        self.resource_generators: Dict[str, ResourceGenerator] = {}

        # Asset mappings from relationship builder
        self.asset_mappings: Dict[str, AssetMapping] = {}

        logger.info("Initialized IntegrationOrchestrator")

    def run_complete_pipeline(self) -> bool:
        """
        Run the complete conversion pipeline.

        Returns:
            True if pipeline completed successfully
        """
        try:
            logger.info("Starting complete conversion pipeline")

            # Step 1: Catalog assets
            if not self._catalog_assets():
                return False

            # Step 2: Build relationships
            if not self._build_relationships():
                return False

            # Step 3: Create file structure
            if not self._create_file_structure():
                return False

            # Step 4: Generate resources
            if not self._generate_resources():
                return False

            # Step 5: Validate output
            if not self._validate_output():
                return False

            logger.info("Complete conversion pipeline finished successfully")
            return True

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            return False

    def _catalog_assets(self) -> bool:
        """
        Catalog all assets from source directory.

        Returns:
            True if assets were cataloged successfully
        """
        try:
            logger.info("Cataloging assets...")

            # Discover and catalog table files
            table_files = list(self.source_dir.rglob("*.tbl"))
            logger.info(f"Found {len(table_files)} table files")

            # For now, we'll simulate cataloging by adding some sample assets
            # In a real implementation, this would parse the table files
            sample_assets = [
                {
                    "asset_id": "rapier_fighter",
                    "name": "Rapier Fighter",
                    "asset_type": "ship",
                    "category": "fighters",
                    "subcategory": "confed",
                    "file_path": "hermes_models/rapier.pof",
                    "file_size": 1024000,
                    "file_hash": "abc123",
                    "creation_date": "2025-01-01T00:00:00",
                    "modification_date": "2025-01-01T00:00:00",
                    "wcs_source_file": "ships.tbl",
                    "wcs_format": "POF",
                    "polygon_count": 5000,
                    "properties": {
                        "ship_class": "Fighter",
                        "manufacturer": "Confederation",
                        "max_velocity": 300.0,
                    },
                },
                {
                    "asset_id": "mkii_laser",
                    "name": "Mk.II Laser Cannon",
                    "asset_type": "weapon",
                    "category": "lasers",
                    "subcategory": "primary",
                    "file_path": "hermes_models/mk2laser.pof",
                    "file_size": 51200,
                    "file_hash": "def456",
                    "creation_date": "2025-01-01T00:00:00",
                    "modification_date": "2025-01-01T00:00:00",
                    "wcs_source_file": "weapons.tbl",
                    "wcs_format": "POF",
                    "polygon_count": 500,
                    "properties": {
                        "weapon_type": "Laser",
                        "damage": 25.0,
                        "fire_rate": 4.0,
                    },
                },
            ]

            # Register sample assets
            for asset_data in sample_assets:
                self.asset_catalog.register_asset(asset_data)

            logger.info(f"Cataloged {len(sample_assets)} sample assets")
            return True

        except Exception as e:
            logger.error(f"Asset cataloging failed: {e}")
            return False

    def _build_relationships(self) -> bool:
        """
        Build relationships between assets.

        Returns:
            True if relationships were built successfully
        """
        try:
            logger.info("Building asset relationships...")

            # In a real implementation, this would process the actual table files
            # For now, we'll simulate with sample relationships

            # Example: Rapier fighter mounts Mk.II laser
            self.relationship_builder.add_relationship(
                source_id="rapier_fighter",
                target_id="mkii_laser",
                relationship_type="weapon_mount",
                strength=1.0,
                metadata={"mount_point": "wing_hardpoint_01"},
            )

            # Example: Mk.II laser is used by Rapier fighter
            self.relationship_builder.add_relationship(
                source_id="mkii_laser",
                target_id="rapier_fighter",
                relationship_type="mounted_on",
                strength=1.0,
                metadata={"mount_point": "wing_hardpoint_01"},
            )

            # Get asset mappings (simulated)
            self.asset_mappings = {
                "rapier_fighter": AssetMapping(
                    entity_name="Rapier Fighter",
                    entity_type="ship",
                    primary_asset=None,  # Would be populated in real implementation
                    related_assets=[],  # Would be populated in real implementation
                    metadata={"faction": "confed", "class": "fighter"},
                ),
                "mkii_laser": AssetMapping(
                    entity_name="Mk.II Laser Cannon",
                    entity_type="weapon",
                    primary_asset=None,  # Would be populated in real implementation
                    related_assets=[],  # Would be populated in real implementation
                    metadata={"type": "primary", "category": "laser"},
                ),
            }

            logger.info("Built sample asset relationships")
            return True

        except Exception as e:
            logger.error(f"Relationship building failed: {e}")
            return False

    def _create_file_structure(self) -> bool:
        """
        Create the Godot project file structure.

        Returns:
            True if structure was created successfully
        """
        try:
            logger.info("Creating Godot project structure...")

            # Create main project structure
            if not self.file_structure_creator.create_project_structure():
                return False

            # Create asset directories
            if not self.file_structure_creator.create_asset_directories(
                self.asset_mappings
            ):
                return False

            # Create campaign directories
            if not self.file_structure_creator.create_campaign_directories():
                return False

            # Create media directories
            if not self.file_structure_creator.create_media_directories():
                return False

            logger.info("Created Godot project structure")
            return True

        except Exception as e:
            logger.error(f"File structure creation failed: {e}")
            return False

    def _generate_resources(self) -> bool:
        """
        Generate Godot resource files.

        Returns:
            True if resources were generated successfully
        """
        try:
            logger.info("Generating Godot resources...")

            # In a real implementation, this would:
            # 1. Initialize specific resource generators (ship, weapon, etc.)
            # 2. Generate .tres files for each asset
            # 3. Generate .tscn files for complex entities
            # 4. Create resource relationships and references

            # For now, we'll simulate by creating some sample files
            project_root = self.output_dir / self.project_name

            # Create a sample ship resource
            ship_resource_path = project_root / "data" / "ships" / "rapier_fighter.tres"
            ship_resource_path.parent.mkdir(parents=True, exist_ok=True)

            ship_resource_content = """[gd_resource type="Resource" load_steps=2 format=3]

[ext_resource type="Script" path="res://addons/wcs_asset_core/resources/ship/ship_class.gd" id="1"]

[resource]
script = ExtResource("1")
class_name = "Rapier Fighter"
display_name = "Raptor-Class Fighter"
ship_type = "Fighter"
manufacturer = "Confederation"
mass = 10.0
max_velocity = 300.0
shields = 100.0
hull = 50.0
primary_weapon_count = 2
secondary_weapon_count = 2
"""

            with open(ship_resource_path, "w") as f:
                f.write(ship_resource_content)

            # Create a sample weapon resource
            weapon_resource_path = project_root / "data" / "weapons" / "mkii_laser.tres"
            weapon_resource_path.parent.mkdir(parents=True, exist_ok=True)

            weapon_resource_content = """[gd_resource type="Resource" load_steps=2 format=3]

[ext_resource type="Script" path="res://addons/wcs_asset_core/resources/weapon/weapon_class.gd" id="1"]

[resource]
script = ExtResource("1")
weapon_name = "Mk.II Laser Cannon"
weapon_type = "Laser"
damage = 25.0
fire_rate = 4.0
velocity = 500.0
range = 1000.0
"""

            with open(weapon_resource_path, "w") as f:
                f.write(weapon_resource_content)

            # Create a sample ship scene
            ship_scene_path = (
                project_root
                / "entities"
                / "fighters"
                / "confed"
                / "fighters"
                / "rapier"
                / "rapier.tscn"
            )
            ship_scene_path.parent.mkdir(parents=True, exist_ok=True)

            ship_scene_content = """[gd_scene load_steps=3 format=3]

[ext_resource type="Script" path="res://entities/fighters/confed/fighter/rapier/rapier.gd" id="1"]
[ext_resource type="PackedScene" path="res://entities/fighters/confed/fighter/rapier/rapier_model.tscn" id="2"]

[node name="RapierFighter" type="Node3D"]
script = ExtResource("1")

[node name="Model" type="Node3D" parent="."]
instance = ExtResource("2")

[node name="Weapons" type="Node" parent="."]
"""

            with open(ship_scene_path, "w") as f:
                f.write(ship_scene_content)

            logger.info("Generated sample Godot resources")
            return True

        except Exception as e:
            logger.error(f"Resource generation failed: {e}")
            return False

    def _validate_output(self) -> bool:
        """
        Validate the generated output.

        Returns:
            True if output is valid
        """
        try:
            logger.info("Validating output...")

            # In a real implementation, this would:
            # 1. Validate all generated .tres files
            # 2. Validate all generated .tscn files
            # 3. Check resource references and relationships
            # 4. Verify file structure integrity
            # 5. Run quality assurance checks

            project_root = self.output_dir / self.project_name

            # Check that required files exist
            required_files = [
                "project.godot",
                "data/ships/rapier_fighter.tres",
                "data/weapons/mkii_laser.tres",
                "entities/fighters/confed/fighters/rapier/rapier.tscn",
            ]

            missing_files = []
            for required_file in required_files:
                if not (project_root / required_file).exists():
                    missing_files.append(required_file)

            if missing_files:
                logger.error(f"Missing required files: {missing_files}")
                return False

            logger.info("Output validation passed")
            return True

        except Exception as e:
            logger.error(f"Output validation failed: {e}")
            return False


def main():
    """Main entry point for the integration orchestrator."""
    import argparse

    parser = argparse.ArgumentParser(description="WCS to Godot Conversion Pipeline")
    parser.add_argument("--source", required=True, help="WCS source directory")
    parser.add_argument(
        "--output", required=True, help="Output directory for Godot project"
    )
    parser.add_argument(
        "--project-name", default="wcs_godot", help="Name of Godot project"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Initialize orchestrator
    orchestrator = IntegrationOrchestrator(
        source_dir=args.source, output_dir=args.output, project_name=args.project_name
    )

    # Run pipeline
    success = orchestrator.run_complete_pipeline()

    if success:
        print("Conversion pipeline completed successfully!")
        print(f"Godot project created at: {args.output}/{args.project_name}")
        return 0
    else:
        print("Conversion pipeline failed!")
        return 1


if __name__ == "__main__":
    exit(main())
