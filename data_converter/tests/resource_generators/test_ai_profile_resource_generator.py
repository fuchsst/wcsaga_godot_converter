#!/usr/bin/env python3
"""
Unit tests for AIProfileResourceGenerator
"""

import tempfile
import os
from pathlib import Path
import pytest

from data_converter.resource_generators.ai_profile_resource_generator import AIProfileResourceGenerator


def test_ai_profile_resource_generator_initialization():
    """Test AIProfileResourceGenerator initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = AIProfileResourceGenerator(
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

        generator = AIProfileResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Test normal names
        assert generator._sanitize_filename("SAGA RETAIL") == "saga_retail"
        assert generator._sanitize_filename("Test Profile") == "test_profile"

        # Test names with special characters
        assert generator._sanitize_filename("Non Combatant") == "non_combatant"
        assert generator._sanitize_filename("AI-Type!") == "ai-type"

        # Test empty name
        assert generator._sanitize_filename("") == "unnamed_resource"


def test_generate_single_ai_profile_resource():
    """Test generating a single AI profile resource"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = AIProfileResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Create test AI profile data
        ai_profile_data = {
            "name": "SAGA RETAIL",
            "default_profile": "SAGA RETAIL",
            "primary_weapon_delay": [0.5, 0.4, 0.3, 0.2, 0.1],
            "secondary_weapon_delay": [1.0, 0.8, 0.6, 0.4, 0.2],
            "use_countermeasures": [True, True, True, True, True],
            "evade_missiles": [True, True, True, True, True],
        }

        result_path = generator._generate_data_ai_profile_resource(ai_profile_data)

        # Check that the file was created
        assert result_path is not None
        assert result_path != ""
        assert os.path.exists(result_path)

        # Check that the path follows the data-based structure
        assert "assets/data/ai/profiles/saga_retail.tres" in result_path

        # Check the content
        with open(result_path, "r") as f:
            content = f.read()

        # Check for key elements in the content
        assert "SAGA RETAIL" in content
        assert "default_profile = \"SAGA RETAIL\"" in content
        assert "primary_weapon_delay = [0.5, 0.4, 0.3, 0.2, 0.1]" in content
        assert "secondary_weapon_delay = [1.0, 0.8, 0.6, 0.4, 0.2]" in content
        assert "use_countermeasures = [true, true, true, true, true]" in content
        assert "evade_missiles = [true, true, true, true, true]" in content


def test_generate_ai_profile_resources():
    """Test generating multiple AI profile resources"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = AIProfileResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Create test AI profile data
        ai_profile_entries = [
            {
                "name": "SAGA RETAIL",
                "default_profile": "SAGA RETAIL",
                "primary_weapon_delay": [0.5, 0.4, 0.3, 0.2, 0.1],
                "secondary_weapon_delay": [1.0, 0.8, 0.6, 0.4, 0.2],
                "use_countermeasures": [True, True, True, True, True],
                "evade_missiles": [True, True, True, True, True],
            },
            {
                "name": "TEST PROFILE",
                "default_profile": "SAGA RETAIL",
                "primary_weapon_delay": [0.6, 0.5, 0.4, 0.3, 0.2],
                "secondary_weapon_delay": [1.2, 1.0, 0.8, 0.6, 0.4],
                "use_countermeasures": [False, False, False, False, False],
                "evade_missiles": [False, False, False, False, False],
            },
        ]

        result_files = generator.generate_ai_profile_resources(ai_profile_entries)

        # Should generate 3 files (2 AI profile resources + 1 registry)
        assert len(result_files) == 3

        # Check that all files exist
        for file_path in result_files.values():
            assert os.path.exists(file_path)

        # Check that registry file is generated
        assert "registry" in result_files


def test_generate_ai_profile_registry():
    """Test generating AI profile registry"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = AIProfileResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Create test AI profile data
        ai_profile_entries = [
            {
                "name": "SAGA RETAIL",
                "default_profile": "SAGA RETAIL",
                "primary_weapon_delay": [0.5, 0.4, 0.3, 0.2, 0.1],
            },
            {
                "name": "TEST PROFILE",
                "default_profile": "SAGA RETAIL",
                "primary_weapon_delay": [0.6, 0.5, 0.4, 0.3, 0.2],
            },
        ]

        registry_path = generator._generate_ai_profile_registry(ai_profile_entries)

        # Check that the registry file was created
        assert registry_path is not None
        assert registry_path != ""
        assert os.path.exists(registry_path)

        # Check the content
        with open(registry_path, "r") as f:
            content = f.read()

        # Check for key elements in the content
        assert "AIProfileRegistryData" in content
        # Check that both AI profiles are in the registry
        assert "saga_retail" in content
        assert "test_profile" in content


if __name__ == "__main__":
    pytest.main([__file__])