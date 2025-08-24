#!/usr/bin/env python3
"""
Refined Asset Organization and Cataloging System

This module provides a consolidated and refined asset cataloging system
for the WCS-Godot conversion pipeline, following the target structure concepts
and feature-based organization principles.

Author: Qwen Code Assistant
"""

import hashlib
import json
import logging
import re
import sqlite3
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

logger = logging.getLogger(__name__)


@dataclass
class AssetMetadata:
    """Comprehensive asset metadata structure following feature-based organization"""

    # Core identification
    asset_id: str
    name: str
    file_path: str
    asset_type: str
    category: str
    subcategory: str

    # File properties
    file_size: int
    file_hash: str
    creation_date: str
    modification_date: str

    # WCS-specific properties
    wcs_source_file: Optional[str] = None
    wcs_format: Optional[str] = None
    wcs_version: Optional[str] = None

    # Asset-specific metadata
    dimensions: Optional[Tuple[int, int]] = None  # For textures/images
    duration: Optional[float] = None  # For audio/video
    polygon_count: Optional[int] = None  # For 3D models
    texture_format: Optional[str] = None  # For textures

    # Relationships
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)
    related_assets: List[str] = field(default_factory=list)

    # Tags and properties
    tags: List[str] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)

    # Feature-based organization
    feature_group: Optional[str] = None  # e.g., "fighters/confed_rapier"
    target_path: Optional[str] = None  # Final path in Godot project


@dataclass
class AssetRelationship:
    """Asset relationship mapping with metadata"""
    
    source_asset: str
    target_asset: str
    relationship_type: str  # dependency, texture_map, weapon_mount, etc.
    strength: float = 1.0  # Relationship strength (0.0 to 1.0)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AssetGroup:
    """Logical grouping of related assets"""
    
    name: str
    description: str = ""
    asset_ids: Set[str] = field(default_factory=set)
    tags: List[str] = field(default_factory=list)
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ValidationIssue:
    """Asset validation issue"""
    
    asset_id: str
    issue_type: str  # missing_dependency, broken_reference, format_error, etc.
    severity: str  # error, warning, info
    message: str
    recommendation: Optional[str] = None
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AssetMapping:
    """Asset mapping for an entity with its related assets"""
    
    entity_name: str
    entity_type: str
    primary_asset: Optional[AssetRelationship] = None
    related_assets: List[AssetRelationship] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class AssetCatalog:
    """
    Comprehensive asset catalog following feature-based organization principles.
    
    This catalog manages all converted assets with their relationships, groups,
    and validation status, organized according to Godot's recommended structure.
    """

    # Asset type mappings following Godot conventions
    ASSET_TYPE_MAP = {
        ".png": "texture",
        ".jpg": "texture", 
        ".jpeg": "texture",
        ".webp": "texture",
        ".json": "metadata",
        ".tres": "resource",
        ".tscn": "scene",
        ".gltf": "model",
        ".glb": "model",
        ".wav": "audio",
        ".ogg": "audio",
        ".fs2": "mission",
        ".tbl": "table",
        ".tbm": "table_mod",
        ".pof": "model_source",
        ".pcx": "texture_source",
        ".ani": "animation",
    }

    # Category mappings based on feature-based organization
    CATEGORY_MAP = {
        "ships": {
            "fighters": "Ships/Fighters",
            "capital_ships": "Ships/Capital",
            "support": "Ships/Support",
        },
        "weapons": {
            "primary": "Weapons/Primary",
            "secondary": "Weapons/Secondary", 
            "beam": "Weapons/Beam",
        },
        "entities": {
            "effects": "Entities/Effects",
            "projectiles": "Entities/Projectiles",
            "environment": "Entities/Environment",
        },
        "data": {
            "ships": "Data/Ships",
            "weapons": "Data/Weapons",
            "ai": "Data/AI",
            "missions": "Data/Missions",
        },
        "audio": {
            "sfx": "Audio/SFX",
            "music": "Audio/Music",
            "voice": "Audio/Voice",
        },
        "textures": {
            "ui": "Textures/UI",
            "ships": "Textures/Ships",
            "effects": "Textures/Effects",
        },
        "animations": {
            "effects": "Animations/Effects",
            "ui": "Animations/UI",
        },
        "missions": {
            "hermes": "Missions/Hermes",
            "brimstone": "Missions/Brimstone",
        }
    }

    def __init__(
        self,
        catalog_path: str = "asset_catalog.json",
        db_path: str = "asset_catalog.db",
    ):
        """
        Initialize the asset catalog.
        
        Args:
            catalog_path: Path to JSON catalog file
            db_path: Path to SQLite database file
        """
        self.catalog_path = Path(catalog_path)
        self.db_path = Path(db_path)
        self.assets: Dict[str, AssetMetadata] = {}
        self.relationships: List[AssetRelationship] = []
        self.groups: Dict[str, AssetGroup] = {}
        self.validation_issues: List[ValidationIssue] = []

        self._init_database()

    def _init_database(self) -> None:
        """Initialize SQLite database with all required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Assets table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS assets (
                        asset_id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        file_path TEXT NOT NULL,
                        asset_type TEXT NOT NULL,
                        category TEXT NOT NULL,
                        subcategory TEXT,
                        feature_group TEXT,
                        target_path TEXT,
                        file_size INTEGER,
                        file_hash TEXT,
                        creation_date TEXT,
                        modification_date TEXT,
                        wcs_source_file TEXT,
                        wcs_format TEXT,
                        metadata_json TEXT
                    )
                """)

                # Relationships table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS relationships (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        source_asset TEXT NOT NULL,
                        target_asset TEXT NOT NULL,
                        relationship_type TEXT NOT NULL,
                        strength REAL DEFAULT 1.0,
                        metadata_json TEXT,
                        created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (source_asset) REFERENCES assets (asset_id),
                        FOREIGN KEY (target_asset) REFERENCES assets (asset_id)
                    )
                """)

                # Asset groups table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS asset_groups (
                        name TEXT PRIMARY KEY,
                        description TEXT,
                        tags_json TEXT,
                        created_date TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Group memberships table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS group_memberships (
                        group_name TEXT NOT NULL,
                        asset_id TEXT NOT NULL,
                        PRIMARY KEY (group_name, asset_id),
                        FOREIGN KEY (group_name) REFERENCES asset_groups (name),
                        FOREIGN KEY (asset_id) REFERENCES assets (asset_id)
                    )
                """)

                # Tags table (many-to-many)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS asset_tags (
                        asset_id TEXT NOT NULL,
                        tag TEXT NOT NULL,
                        PRIMARY KEY (asset_id, tag),
                        FOREIGN KEY (asset_id) REFERENCES assets (asset_id)
                    )
                """)

                # Validation issues table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS validation_issues (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        asset_id TEXT NOT NULL,
                        issue_type TEXT NOT NULL,
                        severity TEXT NOT NULL,
                        message TEXT NOT NULL,
                        recommendation TEXT,
                        created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (asset_id) REFERENCES assets (asset_id)
                    )
                """)

                # Create indexes for performance
                indexes = [
                    "CREATE INDEX IF NOT EXISTS idx_assets_type ON assets (asset_type)",
                    "CREATE INDEX IF NOT EXISTS idx_assets_category ON assets (category)",
                    "CREATE INDEX IF NOT EXISTS idx_assets_feature ON assets (feature_group)",
                    "CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships (source_asset)",
                    "CREATE INDEX IF NOT EXISTS idx_relationships_target ON relationships (target_asset)",
                    "CREATE INDEX IF NOT EXISTS idx_relationships_type ON relationships (relationship_type)",
                    "CREATE INDEX IF NOT EXISTS idx_tags_asset ON asset_tags (asset_id)",
                    "CREATE INDEX IF NOT EXISTS idx_tags_tag ON asset_tags (tag)",
                    "CREATE INDEX IF NOT EXISTS idx_groups_name ON asset_groups (name)",
                    "CREATE INDEX IF NOT EXISTS idx_group_memberships_group ON group_memberships (group_name)",
                    "CREATE INDEX IF NOT EXISTS idx_group_memberships_asset ON group_memberships (asset_id)"
                ]

                for index_sql in indexes:
                    cursor.execute(index_sql)

                conn.commit()
                logger.info(f"Initialized asset catalog database: {self.db_path}")

        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.warning(f"Failed to calculate hash for {file_path}: {e}")
            return ""

    def register_asset(self, asset_data: Dict[str, Any]) -> bool:
        """
        Register a new asset in the catalog.
        
        Args:
            asset_data: Dictionary containing asset metadata
            
        Returns:
            True if asset was registered successfully
        """
        try:
            # Create AssetMetadata from dictionary
            metadata = AssetMetadata(**asset_data)
            
            # Add to in-memory catalog
            self.assets[metadata.asset_id] = metadata
            
            # Save to database
            self._save_asset_to_db(metadata)
            
            logger.debug(f"Registered asset: {metadata.name} ({metadata.asset_id})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register asset: {e}")
            return False

    def _save_asset_to_db(self, metadata: AssetMetadata) -> None:
        """Save asset metadata to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Insert or replace asset
                cursor.execute("""
                    INSERT OR REPLACE INTO assets (
                        asset_id, name, file_path, asset_type, category, subcategory,
                        feature_group, target_path, file_size, file_hash, creation_date,
                        modification_date, wcs_source_file, wcs_format, metadata_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    metadata.asset_id,
                    metadata.name,
                    metadata.file_path,
                    metadata.asset_type,
                    metadata.category,
                    metadata.subcategory,
                    metadata.feature_group,
                    metadata.target_path,
                    metadata.file_size,
                    metadata.file_hash,
                    metadata.creation_date,
                    metadata.modification_date,
                    metadata.wcs_source_file,
                    metadata.wcs_format,
                    json.dumps(metadata.properties)
                ))
                
                # Insert tags
                cursor.executemany("""
                    INSERT OR REPLACE INTO asset_tags (asset_id, tag) VALUES (?, ?)
                """, [(metadata.asset_id, tag) for tag in metadata.tags])
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Failed to save asset to database: {e}")

    def add_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
        strength: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Add relationship between two assets.
        
        Args:
            source_id: ID of source asset
            target_id: ID of target asset
            relationship_type: Type of relationship
            strength: Strength of relationship (0.0-1.0)
            metadata: Additional metadata
            
        Returns:
            True if relationship was added successfully
        """
        try:
            # Validate assets exist
            if source_id not in self.assets or target_id not in self.assets:
                logger.warning(f"One or both assets not found: {source_id}, {target_id}")
                return False
                
            # Create relationship
            relationship = AssetRelationship(
                source_asset=source_id,
                target_asset=target_id,
                relationship_type=relationship_type,
                strength=strength,
                metadata=metadata or {}
            )
            
            # Add to in-memory catalog
            self.relationships.append(relationship)
            
            # Update asset dependencies
            if source_id in self.assets:
                if target_id not in self.assets[source_id].dependencies:
                    self.assets[source_id].dependencies.append(target_id)
            if target_id in self.assets:
                if source_id not in self.assets[target_id].dependents:
                    self.assets[target_id].dependents.append(source_id)
            
            # Save to database
            self._save_relationship_to_db(relationship)
            
            logger.debug(f"Added relationship: {source_id} -> {target_id} ({relationship_type})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add relationship: {e}")
            return False

    def _save_relationship_to_db(self, relationship: AssetRelationship) -> None:
        """Save relationship to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO relationships 
                    (source_asset, target_asset, relationship_type, strength, metadata_json)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    relationship.source_asset,
                    relationship.target_asset,
                    relationship.relationship_type,
                    relationship.strength,
                    json.dumps(relationship.metadata)
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to save relationship to database: {e}")

    def create_group(
        self,
        name: str,
        description: str = "",
        tags: List[str] = None
    ) -> bool:
        """
        Create a new asset group.
        
        Args:
            name: Name of the group
            description: Description of the group
            tags: Tags for the group
            
        Returns:
            True if group was created successfully
        """
        try:
            if name in self.groups:
                logger.warning(f"Group {name} already exists")
                return False
                
            # Create group
            group = AssetGroup(
                name=name,
                description=description,
                tags=tags or []
            )
            
            # Add to in-memory catalog
            self.groups[name] = group
            
            # Save to database
            self._save_group_to_db(group)
            
            logger.info(f"Created asset group: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create group: {e}")
            return False

    def _save_group_to_db(self, group: AssetGroup) -> None:
        """Save group to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO asset_groups (name, description, tags_json)
                    VALUES (?, ?, ?)
                """, (
                    group.name,
                    group.description,
                    json.dumps(group.tags)
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to save group to database: {e}")

    def add_to_group(self, group_name: str, asset_id: str) -> bool:
        """
        Add an asset to a group.
        
        Args:
            group_name: Name of the group
            asset_id: ID of the asset to add
            
        Returns:
            True if asset was added successfully
        """
        try:
            if group_name not in self.groups:
                logger.warning(f"Group {group_name} does not exist")
                return False
                
            if asset_id not in self.assets:
                logger.warning(f"Asset {asset_id} does not exist")
                return False
                
            # Add to in-memory group
            self.groups[group_name].asset_ids.add(asset_id)
            
            # Save to database
            self._save_group_membership_to_db(group_name, asset_id)
            
            logger.debug(f"Added asset {asset_id} to group {group_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add asset to group: {e}")
            return False

    def _save_group_membership_to_db(self, group_name: str, asset_id: str) -> None:
        """Save group membership to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO group_memberships (group_name, asset_id)
                    VALUES (?, ?)
                """, (group_name, asset_id))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to save group membership to database: {e}")

    def search_assets(
        self,
        query: str = "",
        asset_type: str = "",
        category: str = "",
        feature_group: str = "",
        tags: List[str] = None,
        limit: int = 100,
    ) -> List[AssetMetadata]:
        """
        Search assets with various filters following feature-based organization.
        
        Args:
            query: Text search in name or properties
            asset_type: Filter by asset type
            category: Filter by category
            feature_group: Filter by feature group
            tags: Filter by tags
            limit: Maximum results to return
            
        Returns:
            List of matching assets
        """
        results = []
        
        for asset in self.assets.values():
            # Text search
            if query:
                search_fields = [
                    asset.name.lower(),
                    asset.asset_type.lower() if asset.asset_type else "",
                    asset.category.lower() if asset.category else "",
                    asset.subcategory.lower() if asset.subcategory else "",
                    asset.feature_group.lower() if asset.feature_group else "",
                    str(asset.properties).lower() if asset.properties else ""
                ]
                
                if not any(query.lower() in field for field in search_fields if field):
                    continue
            
            # Type filter
            if asset_type and asset.asset_type != asset_type:
                continue
                
            # Category filter
            if category and not (
                (asset.category and category.lower() in asset.category.lower()) or
                (asset.subcategory and category.lower() in asset.subcategory.lower())
            ):
                continue
                
            # Feature group filter
            if feature_group and asset.feature_group != feature_group:
                continue
                
            # Tags filter
            if tags:
                if not any(tag in asset.tags for tag in tags):
                    continue
                    
            results.append(asset)
            
            if len(results) >= limit:
                break
                
        return results

    def get_assets_by_feature_group(self, feature_group: str) -> List[AssetMetadata]:
        """
        Get all assets belonging to a specific feature group.
        
        Args:
            feature_group: Feature group name (e.g., "fighters/confed_rapier")
            
        Returns:
            List of assets in the feature group
        """
        return [asset for asset in self.assets.values() 
                if asset.feature_group == feature_group]

    def get_feature_groups(self) -> List[str]:
        """
        Get all feature groups in the catalog.
        
        Returns:
            List of feature group names
        """
        groups = set()
        for asset in self.assets.values():
            if asset.feature_group:
                groups.add(asset.feature_group)
        return sorted(list(groups))

    def validate_assets(self) -> List[ValidationIssue]:
        """
        Validate all assets and return issues.
        
        Returns:
            List of validation issues found
        """
        self.validation_issues = []
        logger.info(f"Validating {len(self.assets)} assets...")

        for asset_id, asset in self.assets.items():
            # Check file existence
            if not Path(asset.file_path).exists():
                self.validation_issues.append(ValidationIssue(
                    asset_id=asset_id,
                    issue_type="missing_file",
                    severity="error",
                    message=f"Asset file does not exist: {asset.file_path}",
                    recommendation="Re-extract or convert the asset"
                ))

            # Check dependencies
            for dep_id in asset.dependencies:
                if dep_id not in self.assets:
                    self.validation_issues.append(ValidationIssue(
                        asset_id=asset_id,
                        issue_type="missing_dependency",
                        severity="warning",
                        message=f"Dependency not found: {dep_id}",
                        recommendation="Check if dependency was converted or update reference"
                    ))

            # Format-specific validation
            if asset.asset_type == "texture" and asset.dimensions:
                width, height = asset.dimensions
                if width > 4096 or height > 4096:
                    self.validation_issues.append(ValidationIssue(
                        asset_id=asset_id,
                        issue_type="oversized_texture",
                        severity="warning",
                        message=f"Large texture dimensions: {width}x{height}",
                        recommendation="Consider texture compression or optimization"
                    ))

        logger.info(f"Found {len(self.validation_issues)} validation issues")
        return self.validation_issues

    def get_asset_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about assets in catalog.
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            "total_assets": len(self.assets),
            "total_relationships": len(self.relationships),
            "total_groups": len(self.groups),
            "assets_by_type": {},
            "assets_by_category": {},
            "assets_by_feature_group": {},
            "total_file_size": sum(asset.file_size for asset in self.assets.values()),
            "validation_issues": len(self.validation_issues)
        }
        
        # Count by type
        for asset in self.assets.values():
            asset_type = asset.asset_type or "unknown"
            stats["assets_by_type"][asset_type] = stats["assets_by_type"].get(asset_type, 0) + 1
            
            category = asset.category or "uncategorized"
            stats["assets_by_category"][category] = stats["assets_by_category"].get(category, 0) + 1
            
            feature_group = asset.feature_group or "ungrouped"
            stats["assets_by_feature_group"][feature_group] = stats["assets_by_feature_group"].get(feature_group, 0) + 1
            
        return stats

    def save_catalog(self) -> None:
        """Save catalog to JSON and database"""
        try:
            # Save to database (already done incrementally)
            
            # Generate and save manifest
            manifest = self.generate_manifest()
            manifest_path = self.catalog_path.with_suffix('.manifest.json')
            
            with open(manifest_path, "w") as f:
                json.dump(manifest, f, indent=2)
                
            logger.info(f"Saved catalog manifest to {manifest_path}")

        except Exception as e:
            logger.error(f"Failed to save catalog: {e}")
            raise

    def generate_manifest(self) -> Dict[str, Any]:
        """Generate comprehensive conversion manifest"""
        return {
            "catalog_info": {
                "generated_date": datetime.now().isoformat(),
                "total_assets": len(self.assets),
                "total_relationships": len(self.relationships),
                "total_groups": len(self.groups),
                "validation_issues": len(self.validation_issues),
            },
            "asset_summary": self.get_asset_statistics(),
            "feature_groups": self.get_feature_groups(),
        }

    def load_catalog(self) -> bool:
        """Load catalog from database"""
        try:
            if not self.db_path.exists():
                logger.warning(f"Database file not found: {self.db_path}")
                return False

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Load assets
                cursor.execute("SELECT * FROM assets")
                for row in cursor.fetchall():
                    asset_dict = {
                        "asset_id": row[0],
                        "name": row[1],
                        "file_path": row[2],
                        "asset_type": row[3],
                        "category": row[4],
                        "subcategory": row[5],
                        "feature_group": row[6],
                        "target_path": row[7],
                        "file_size": row[8],
                        "file_hash": row[9],
                        "creation_date": row[10],
                        "modification_date": row[11],
                        "wcs_source_file": row[12],
                        "wcs_format": row[13],
                        "properties": json.loads(row[14]) if row[14] else {},
                        "dependencies": [],
                        "dependents": [],
                        "related_assets": [],
                        "tags": []
                    }
                    
                    # Load tags
                    tag_cursor = conn.cursor()
                    tag_cursor.execute("SELECT tag FROM asset_tags WHERE asset_id = ?", (row[0],))
                    asset_dict["tags"] = [tag_row[0] for tag_row in tag_cursor.fetchall()]
                    
                    self.assets[row[0]] = AssetMetadata(**asset_dict)

                # Load relationships
                cursor.execute("SELECT * FROM relationships")
                for row in cursor.fetchall():
                    relationship = AssetRelationship(
                        source_asset=row[1],
                        target_asset=row[2],
                        relationship_type=row[3],
                        strength=row[4],
                        metadata=json.loads(row[5]) if row[5] else {},
                        created_date=row[6]
                    )
                    self.relationships.append(relationship)
                    
                    # Update asset dependencies
                    if relationship.source_asset in self.assets:
                        if relationship.target_asset not in self.assets[relationship.source_asset].dependencies:
                            self.assets[relationship.source_asset].dependencies.append(relationship.target_asset)
                    if relationship.target_asset in self.assets:
                        if relationship.source_asset not in self.assets[relationship.target_asset].dependents:
                            self.assets[relationship.target_asset].dependents.append(relationship.source_asset)

                # Load groups
                cursor.execute("SELECT * FROM asset_groups")
                for row in cursor.fetchall():
                    group = AssetGroup(
                        name=row[0],
                        description=row[1],
                        tags=json.loads(row[2]) if row[2] else [],
                        created_date=row[3]
                    )
                    self.groups[row[0]] = group

                # Load group memberships
                cursor.execute("SELECT group_name, asset_id FROM group_memberships")
                for row in cursor.fetchall():
                    group_name, asset_id = row
                    if group_name in self.groups and asset_id in self.assets:
                        self.groups[group_name].asset_ids.add(asset_id)

                # Load validation issues
                cursor.execute("SELECT * FROM validation_issues")
                for row in cursor.fetchall():
                    issue = ValidationIssue(
                        asset_id=row[1],
                        issue_type=row[2],
                        severity=row[3],
                        message=row[4],
                        recommendation=row[5],
                        created_date=row[6]
                    )
                    self.validation_issues.append(issue)

            logger.info(f"Loaded catalog with {len(self.assets)} assets")
            return True

        except Exception as e:
            logger.error(f"Failed to load catalog: {e}")
            return False
