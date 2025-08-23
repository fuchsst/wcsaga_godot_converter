#!/usr/bin/env python3
"""
WCS Table Data Converter

Converts WCS table files (.tbl) to Godot-compatible resource formats.
Handles ship classes, weapon definitions, armor specifications, and faction data
with complete fidelity to the original C++ parsing implementation.

Author: Dev (GDScript Developer)
Date: January 29, 2025
Story: DM-008 - Asset Table Processing
Epic: EPIC-003 - Data Migration & Conversion Tools
Architecture: Mo's EPIC-003 Architecture Document v2.0

Original C++ Analysis:
- Based on parselo.cpp/h parsing framework from WCS source
- Maintains compatibility with ship.cpp, weapons.cpp, species_defs.cpp, iff_defs.cpp
- Supports modular table system (.tbl base + .tbm modular overrides)
- Preserves all data fields and parsing behaviors from original implementation
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

# Import our new modular components
from .table_converters.converter_factory import ConverterFactory

logger = logging.getLogger(__name__)
class TableDataConverter:
    """
    Main table data converter following EPIC-003 architecture.
    
    Converts WCS table files (.tbl) to Godot BaseAssetData resource format
    with complete data fidelity and relationship mapping.
    
    This class now delegates to modular converter implementations.
    """
    
    def __init__(self, source_dir: Path, target_dir: Path):
        """
        Initialize table data converter.
        
        Args:
            source_dir: WCS source directory containing table files
            target_dir: Target Godot project directory for output
        """
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.assets_dir = self.target_dir / "assets" / "tables"
        self.conversion_stats = {
            "ships_processed": 0,
            "weapons_processed": 0,
            "armor_types_processed": 0,
            "species_processed": 0,
            "iff_factions_processed": 0,
            "relationships_mapped": 0,
            "errors": []
        }
        
        # Asset relationship mapping
        self.ship_weapon_compatibility: Dict[str, List[str]] = {}
        self.damage_type_registry: Dict[str, int] = {}
        self.armor_type_registry: Dict[str, str] = {}
        self.species_registry: Dict[str, int] = {}
        
        # Ensure output directory exists
        self.assets_dir.mkdir(parents=True, exist_ok=True)
    
    def convert_table_file(self, table_file: Path) -> bool:
        """
        Convert a single table file to Godot resources.
        
        Args:
            table_file: Path to the table file to convert
            
        Returns:
            True if conversion successful, False otherwise
        """
        try:
            logger.info(f"Converting table file: {table_file}")
            
            # Try to get a converter for this file type
            converter = ConverterFactory.get_converter_for_file(table_file, self.source_dir, self.target_dir)
            
            if converter is None:
                logger.warning(f"Unknown table type for file: {table_file}")
                return False
            
            # Use the modular converter to process the file
            success = converter.convert_table_file(table_file)
            
            if success:
                logger.info(f"Successfully converted: {table_file}")
                # Aggregate stats from the modular converter
                self._aggregate_stats(converter)
            else:
                logger.error(f"Failed to convert: {table_file}")
                
            return success
            
        except Exception as e:
            error_msg = f"Error converting {table_file}: {str(e)}"
            logger.error(error_msg)
            self.conversion_stats["errors"].append(error_msg)
            return False
    
    def _aggregate_stats(self, converter) -> None:
        """
        Aggregate statistics from a modular converter using proper interface methods.
        
        Args:
            converter: The modular converter instance
        """
        # Get statistics using interface method
        converter_stats = converter.get_stats()
        
        # Aggregate entries processed
        if "entries_processed" in converter_stats:
            self.conversion_stats["ships_processed"] += converter_stats["entries_processed"]
            
        # Aggregate errors
        if "errors" in converter_stats:
            self.conversion_stats["errors"].extend(converter_stats["errors"])
            
        # Get registries using interface method
        registries = converter.get_registries()
        
        # Update relationship mappings
        if "relationship_mappings" in registries:
            self.conversion_stats["relationships_mapped"] += len(registries["relationship_mappings"])
            # Update specific registries
            for mapping_type, mapping_data in registries["relationship_mappings"].items():
                if mapping_type == "ship_weapon_compatibility":
                    self.ship_weapon_compatibility.update(mapping_data)
                elif mapping_type == "armor_type_registry":
                    self.armor_type_registry.update(mapping_data)
                elif mapping_type == "damage_type_registry":
                    self.damage_type_registry.update(mapping_data)
                elif mapping_type == "species_registry":
                    self.species_registry.update(mapping_data)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def generate_conversion_summary(self) -> Dict[str, Any]:
        """Generate comprehensive conversion summary report"""
        return {
            "conversion_statistics": self.conversion_stats,
            "asset_relationships": {
                "ship_weapon_compatibility": self.ship_weapon_compatibility,
                "damage_type_registry": self.damage_type_registry,
                "armor_type_registry": self.armor_type_registry,
                "species_registry": self.species_registry
            },
            "output_directories": {
                "ships": str(self.assets_dir / "ships"),
                "weapons": str(self.assets_dir / "weapons"),
                "armor": str(self.assets_dir / "armor"),
                "species": str(self.assets_dir / "species"),
                "factions": str(self.assets_dir / "factions")
            },
            "validation_summary": {
                "total_assets_converted": (
                    self.conversion_stats["ships_processed"] +
                    self.conversion_stats["weapons_processed"] +
                    self.conversion_stats["armor_types_processed"] +
                    self.conversion_stats["species_processed"] +
                    self.conversion_stats["iff_factions_processed"]
                ),
                "relationship_mappings": self.conversion_stats["relationships_mapped"],
                "error_count": len(self.conversion_stats["errors"])
            }
        }

