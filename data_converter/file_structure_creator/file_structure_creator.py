"""
File Structure Creator - Creates Godot project directory structure

This module creates the complete file structure for the converted Godot project,
following the target structure concepts and feature-based organization principles.

Author: Qwen Code Assistant
"""

import logging
from pathlib import Path
from typing import Dict, Union

from ..core.catalog.enhanced_asset_catalog import EnhancedAssetCatalog
from ..core.relationship_builder import RelationshipBuilder
from ..core.catalog.asset_catalog import AssetMapping

logger = logging.getLogger(__name__)


class FileStructureCreator:
    """
    Creates the complete file structure for the Godot project following
    feature-based organization principles.
    """

    def __init__(
        self,
        asset_catalog: EnhancedAssetCatalog,
        relationship_builder: RelationshipBuilder,
        output_root: Union[str, Path],
    ):
        """
        Initialize the file structure creator.

        Args:
            asset_catalog: Enhanced asset catalog with all assets
            relationship_builder: Relationship builder with asset relationships
            output_root: Root directory for the Godot project
        """
        self.asset_catalog = asset_catalog
        self.relationship_builder = relationship_builder
        self.output_root = Path(output_root)

        # Godot project structure following target structure concepts
        self.project_structure = {
            "addons": {},
            "core": {},
            "data": {
                "ships": {},
                "weapons": {},
                "ai": {},
                "missions": {},
                "campaigns": {},
                "effects": {},
                "config": {},
            },
            "entities": {
                "fighters": {},
                "capital_ships": {},
                "projectiles": {},
                "weapons": {},
                "effects": {},
                "environment": {},
            },
            "systems": {
                "ai": {},
                "mission_control": {},
                "weapon_control": {},
                "physics": {},
                "audio": {},
                "graphics": {},
                "networking": {},
            },
            "ui": {
                "main_menu": {},
                "hud": {},
                "briefing": {},
                "debriefing": {},
                "options": {},
                "tech_database": {},
                "components": {},
                "themes": {},
            },
            "missions": {},
            "campaigns": {},
            "docs": {},
        }

    def create_project_structure(self) -> bool:
        """
        Create the complete Godot project directory structure.

        Returns:
            True if structure was created successfully
        """
        try:
            logger.info(f"Creating Godot project structure at: {self.output_root}")

            # Create root directory
            self.output_root.mkdir(parents=True, exist_ok=True)

            # Create project structure
            self._create_directories(self.project_structure, self.output_root)

            # Create project file
            self._create_project_file()

            # Create README
            self._create_readme()

            logger.info("Godot project structure created successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to create project structure: {e}")
            return False

    def _create_directories(self, structure: Dict, parent_path: Path) -> None:
        """
        Recursively create directory structure.

        Args:
            structure: Directory structure dictionary
            parent_path: Parent directory path
        """
        for name, substructure in structure.items():
            dir_path = parent_path / name
            dir_path.mkdir(exist_ok=True)
            logger.debug(f"Created directory: {dir_path}")

            if substructure:
                self._create_directories(substructure, dir_path)

    def _create_project_file(self) -> None:
        """Create the Godot project file."""
        project_file = self.output_root / "project.godot"

        # Basic Godot project configuration
        project_content = """[application]
config/name="Wing Commander Saga"
config/icon="res://icon.png"

[editor_plugins]
enabled=["wcs_asset_core"]

[rendering]
environment/default_environment/bg_mode=2
"""

        with open(project_file, "w") as f:
            f.write(project_content)

        logger.debug(f"Created project file: {project_file}")

    def _create_readme(self) -> None:
        """Create project README file."""
        readme_file = self.output_root / "README.md"

        readme_content = """# Wing Commander Saga - Godot Conversion

This is the Godot conversion of Wing Commander Saga, following feature-based
organization principles as recommended by Godot community best practices.

## Directory Structure

- `addons/` - Third-party plugins and extensions
- `core/` - Engine-agnostic core logic
- `data/` - Data-driven Resource files (.tres)
- `entities/` - Physical game objects
- `systems/` - Game logic systems
- `ui/` - User interface elements
- `missions/` - Mission scenes and data
- `campaigns/` - Campaign data and progression
- `docs/` - Documentation

## Feature-Based Organization

All files related to a single conceptual unit are grouped together in a 
self-contained directory. For example:

```
/entities/fighters/confed_rapier/
├── rapier.tscn    # Scene file
├── rapier.gd      # Script file
├── rapier.tres    # Ship data resource
├── rapier.glb     # 3D model
├── rapier.png     # Texture
└── rapier_engine.ogg # Engine sound
```

This structure enables better maintainability and modularity.
"""

        with open(readme_file, "w") as f:
            f.write(readme_content)

        logger.debug(f"Created README: {readme_file}")

    def create_asset_directories(self, asset_mappings: Dict[str, AssetMapping]) -> bool:
        """
        Create directories for all assets based on their mappings.

        Args:
            asset_mappings: Dictionary of asset mappings from relationship builder

        Returns:
            True if directories were created successfully
        """
        try:
            logger.info(f"Creating asset directories for {len(asset_mappings)} assets")

            for entity_name, asset_mapping in asset_mappings.items():
                try:
                    # Create entity directory based on type
                    entity_type = asset_mapping.entity_type.lower()

                    if entity_type == "ship":
                        # Determine faction and category
                        faction = self._get_asset_faction(entity_name)
                        category = self._get_ship_category(entity_name)

                        entity_dir = (
                            self.output_root
                            / "entities"
                            / "fighters"
                            / faction
                            / category
                            / self._sanitize_name(entity_name)
                        )

                    elif entity_type == "weapon":
                        entity_dir = (
                            self.output_root
                            / "entities"
                            / "weapons"
                            / self._sanitize_name(entity_name)
                        )

                    elif entity_type == "effect":
                        entity_dir = (
                            self.output_root
                            / "entities"
                            / "effects"
                            / self._sanitize_name(entity_name)
                        )

                    else:
                        # Default to general entities directory
                        entity_dir = (
                            self.output_root
                            / "entities"
                            / "environment"
                            / self._sanitize_name(entity_name)
                        )

                    # Create entity directory
                    entity_dir.mkdir(parents=True, exist_ok=True)
                    logger.debug(f"Created entity directory: {entity_dir}")

                    # Create data directory for this entity
                    data_dir = (
                        self.output_root
                        / "data"
                        / f"{entity_type}s"
                        / self._sanitize_name(entity_name)
                    )
                    data_dir.mkdir(parents=True, exist_ok=True)
                    logger.debug(f"Created data directory: {data_dir}")

                except Exception as e:
                    logger.warning(
                        f"Failed to create directories for {entity_name}: {e}"
                    )
                    continue

            logger.info("Asset directories created successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to create asset directories: {e}")
            return False

    def create_campaign_directories(self) -> bool:
        """
        Create directory structure for campaigns.

        Returns:
            True if directories were created successfully
        """
        try:
            # Create main campaign directories
            campaigns = ["hermes", "brimstone", "training"]

            for campaign in campaigns:
                # Campaign data directory
                campaign_data_dir = self.output_root / "data" / "campaigns" / campaign
                campaign_data_dir.mkdir(parents=True, exist_ok=True)

                # Campaign missions directory
                campaign_missions_dir = self.output_root / "missions" / campaign
                campaign_missions_dir.mkdir(parents=True, exist_ok=True)

                # Campaign directory
                campaign_dir = self.output_root / "campaigns" / campaign
                campaign_dir.mkdir(parents=True, exist_ok=True)

                logger.debug(f"Created campaign directories for: {campaign}")

            return True

        except Exception as e:
            logger.error(f"Failed to create campaign directories: {e}")
            return False

    def create_media_directories(self) -> bool:
        """
        Create directory structure for media files.

        Returns:
            True if directories were created successfully
        """
        try:
            # Audio directories
            audio_dirs = [
                "audio/sfx/weapons",
                "audio/sfx/explosions",
                "audio/sfx/environment",
                "audio/sfx/ui",
                "audio/music",
                "audio/voice",
            ]

            for audio_dir in audio_dirs:
                (self.output_root / audio_dir).mkdir(parents=True, exist_ok=True)

            # Texture directories
            texture_dirs = [
                "textures/ships",
                "textures/weapons",
                "textures/effects",
                "textures/ui",
                "textures/environment",
            ]

            for texture_dir in texture_dirs:
                (self.output_root / texture_dir).mkdir(parents=True, exist_ok=True)

            # Animation directories
            anim_dirs = ["animations/effects", "animations/ui", "animations/weapons"]

            for anim_dir in anim_dirs:
                (self.output_root / anim_dir).mkdir(parents=True, exist_ok=True)

            logger.debug("Created media directories")
            return True

        except Exception as e:
            logger.error(f"Failed to create media directories: {e}")
            return False

    def _get_asset_faction(self, asset_name: str) -> str:
        """
        Determine faction from asset name.

        Args:
            asset_name: Name of the asset

        Returns:
            Faction name
        """
        name_lower = asset_name.lower()

        # Terran patterns
        if any(
            pattern in name_lower
            for pattern in [
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
                "rapier",
                "arrow",
            ]
        ):
            return "confed"

        # Kilrathi patterns
        elif any(
            pattern in name_lower
            for pattern in [
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
        ):
            return "kilrathi"

        # Pirate patterns
        elif any(
            pattern in name_lower
            for pattern in ["pirate", "bandit", "corsair", "privateer"]
        ):
            return "pirate"

        # Default to confed
        return "confed"

    def _get_ship_category(self, ship_name: str) -> str:
        """
        Determine ship category from name.

        Args:
            ship_name: Name of the ship

        Returns:
            Ship category
        """
        name_lower = ship_name.lower()

        if any(
            pattern in name_lower for pattern in ["fighter", "interceptor", "stealth"]
        ):
            return "fighters"

        elif any(pattern in name_lower for pattern in ["bomber", "assault"]):
            return "bombers"

        elif any(pattern in name_lower for pattern in ["corvette", "gunboat"]):
            return "corvettes"

        elif any(pattern in name_lower for pattern in ["cruiser", "destroyer"]):
            return "cruisers"

        elif any(
            pattern in name_lower for pattern in ["capital", "dreadnought", "carrier"]
        ):
            return "capital_ships"

        # Default to fighters
        return "fighters"

    def _sanitize_name(self, name: str) -> str:
        """
        Sanitize name for use as directory name.

        Args:
            name: Name to sanitize

        Returns:
            Sanitized name
        """
        # Replace spaces and special characters
        sanitized = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)

        # Remove multiple underscores
        while "__" in sanitized:
            sanitized = sanitized.replace("__", "_")

        # Remove leading/trailing underscores
        sanitized = sanitized.strip("_")

        # Ensure not empty
        if not sanitized:
            sanitized = "unnamed"

        return sanitized.lower()
