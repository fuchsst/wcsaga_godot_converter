#!/usr/bin/env python3
"""
Unit tests for IFFResourceGenerator
"""

import tempfile
import os
from pathlib import Path
import pytest

from data_converter.resource_generators.iff_resource_generator import IFFResourceGenerator


def test_iff_resource_generator_initialization():
    """Test IFFResourceGenerator initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = IFFResourceGenerator(
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

        generator = IFFResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Test normal names
        assert generator._sanitize_filename("Friendly") == "friendly"
        assert generator._sanitize_filename("Hostile") == "hostile"

        # Test names with special characters
        assert generator._sanitize_filename("Non Combatant") == "non_combatant"
        assert generator._sanitize_filename("IFF-Type!") == "iff-type"

        # Test empty name
        assert generator._sanitize_filename("") == "unnamed_iff"


def test_generate_single_iff_resource():
    """Test generating a single IFF resource"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = IFFResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Create test IFF data
        iff_data = {
            "name": "Friendly",
            "color": [24, 72, 232],
            "attacks": ["Hostile", "Neutral", "Traitor"],
            "flags": ["orders hidden"],
            "default_ship_flags": ["cargo-known"],
            "default_ship_flags2": ["no-subspace-drive"],
        }

        result_path = generator._generate_data_iff_resource(iff_data)

        # Check that the file was created
        assert result_path is not None
        assert result_path != ""
        assert os.path.exists(result_path)

        # Check that the path follows the data-based structure
        assert "assets/data/iff/friendly.tres" in result_path

        # Check the content
        with open(result_path, "r") as f:
            content = f.read()

        # Check for key elements in the content
        assert "Friendly" in content
        assert "Color(0.09411764705882353, 0.2823529411764706, 0.9098039215686274, 1)" in content
        assert 'attacks = ["Hostile", "Neutral", "Traitor"]' in content
        assert 'flags = ["orders hidden"]' in content
        assert 'default_ship_flags = ["cargo-known"]' in content
        assert 'default_ship_flags2 = ["no-subspace-drive"]' in content


def test_generate_iff_resources():
    """Test generating multiple IFF resources"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = IFFResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Create test IFF data
        iff_entries = [
            {
                "name": "Friendly",
                "color": [24, 72, 232],
                "attacks": ["Hostile", "Neutral", "Traitor"],
                "flags": ["orders hidden"],
                "default_ship_flags": ["cargo-known"],
                "default_ship_flags2": ["no-subspace-drive"],
            },
            {
                "name": "Hostile",
                "color": [236, 56, 24],
                "attacks": ["Friendly", "Neutral", "Traitor"],
                "flags": ["orders hidden", "wing name hidden"],
                "default_ship_flags2": ["no-subspace-drive"],
            },
        ]

        result_files = generator.generate_iff_resources(iff_entries)

        # Should generate 3 files (2 IFF resources + 1 registry)
        assert len(result_files) == 3

        # Check that all files exist
        for file_path in result_files.values():
            assert os.path.exists(file_path)

        # Check that registry file is generated
        assert "registry" in result_files


def test_generate_iff_registry():
    """Test generating IFF registry"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = IFFResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Create test IFF data
        iff_entries = [
            {
                "name": "Friendly",
                "color": [24, 72, 232],
                "attacks": ["Hostile", "Neutral", "Traitor"],
            },
            {
                "name": "Hostile",
                "color": [236, 56, 24],
                "attacks": ["Friendly", "Neutral", "Traitor"],
            },
        ]

        registry_path = generator._generate_iff_registry(iff_entries)

        # Check that the registry file was created
        assert registry_path is not None
        assert registry_path != ""
        assert os.path.exists(registry_path)

        # Check the content
        with open(registry_path, "r") as f:
            content = f.read()

        # Check for key elements in the content
        assert "IFFRegistryData" in content
        # Check that both IFFs are in the registry
        assert "friendly" in content
        assert "hostile" in content


if __name__ == "__main__":
    pytest.main([__file__])