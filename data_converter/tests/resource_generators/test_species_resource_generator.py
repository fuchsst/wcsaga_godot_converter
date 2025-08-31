#!/usr/bin/env python3
"""
Unit tests for SpeciesResourceGenerator
"""

import tempfile
import os
from pathlib import Path
import pytest

from data_converter.resource_generators.species_resource_generator import SpeciesResourceGenerator


def test_species_resource_generator_initialization():
    """Test SpeciesResourceGenerator initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = SpeciesResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Check that the generator is properly initialized
        assert generator.output_dir == Path(temp_dir)
        assert generator.data_dir.exists()


def test_sanitize_filename():
    """Test filename sanitization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = SpeciesResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Test normal names
        assert generator._sanitize_filename("Terran") == "terran"
        assert generator._sanitize_filename("Kilrathi") == "kilrathi"

        # Test names with special characters
        assert generator._sanitize_filename("Non Combatant") == "non_combatant"
        assert generator._sanitize_filename("Species-Type!") == "species-type"

        # Test empty name
        assert generator._sanitize_filename("") == "unnamed_resource"


def test_generate_single_species_resource():
    """Test generating a single species resource"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = SpeciesResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Create test species data
        species_data = {
            "name": "Terran",
            "default_iff": "Friendly",
            "default_armor": "Terran",
            "color": "(0, 0, 192)",
            "ai_aggression": 0.5,
            "ai_caution": 0.7,
            "ai_accuracy": 0.8,
            "debris_texture": "debris01a",
            "shield_hit_ani": "shieldhit01a",
        }

        result_path = generator._generate_data_species_resource(species_data)

        # Check that the file was created
        assert result_path is not None
        assert result_path != ""
        assert os.path.exists(result_path)

        # Check that the path follows the data-based structure
        assert "assets/data/species/terran.tres" in result_path

        # Check the content
        with open(result_path, "r") as f:
            content = f.read()

        # Check for key elements in the content
        assert "Terran" in content
        assert "default_iff = \"Friendly\"" in content
        assert "default_armor = \"Terran\"" in content
        assert "color = \"(0, 0, 192)\"" in content
        assert "ai_aggression = 0.5" in content
        assert "ai_caution = 0.7" in content
        assert "ai_accuracy = 0.8" in content
        assert "debris_texture = \"debris01a\"" in content
        assert "shield_hit_ani = \"shieldhit01a\"" in content


def test_generate_species_resources():
    """Test generating multiple species resources"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = SpeciesResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Create test species data
        species_entries = [
            {
                "name": "Terran",
                "default_iff": "Friendly",
                "default_armor": "Terran",
                "color": "(0, 0, 192)",
                "ai_aggression": 0.5,
                "ai_caution": 0.7,
                "ai_accuracy": 0.8,
            },
            {
                "name": "Kilrathi",
                "default_iff": "Hostile",
                "default_armor": "Kilrathi",
                "color": "(192, 0, 0)",
                "ai_aggression": 0.9,
                "ai_caution": 0.3,
                "ai_accuracy": 0.7,
            },
        ]

        result_files = generator.generate_species_resources(species_entries)

        # Should generate 3 files (2 species resources + 1 registry)
        assert len(result_files) == 3

        # Check that all files exist
        for file_path in result_files.values():
            assert os.path.exists(file_path)

        # Check that registry file is generated
        assert "registry" in result_files


def test_generate_species_registry():
    """Test generating species registry"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = SpeciesResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Create test species data
        species_entries = [
            {
                "name": "Terran",
                "default_iff": "Friendly",
            },
            {
                "name": "Kilrathi",
                "default_iff": "Hostile",
            },
        ]

        registry_path = generator._generate_species_registry(species_entries)

        # Check that the registry file was created
        assert registry_path is not None
        assert registry_path != ""
        assert os.path.exists(registry_path)

        # Check the content
        with open(registry_path, "r") as f:
            content = f.read()

        # Check for key elements in the content
        assert "SpeciesRegistryData" in content
        # Check that both species are in the registry
        assert "terran" in content
        assert "kilrathi" in content


if __name__ == "__main__":
    pytest.main([__file__])