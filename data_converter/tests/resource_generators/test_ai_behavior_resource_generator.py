#!/usr/bin/env python3
"""
Unit tests for AIBehaviorResourceGenerator
"""

import tempfile
import os
from pathlib import Path
import pytest

from data_converter.resource_generators.ai_behavior_resource_generator import AIBehaviorResourceGenerator


def test_ai_behavior_resource_generator_initialization():
    """Test AIBehaviorResourceGenerator initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = AIBehaviorResourceGenerator(
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

        generator = AIBehaviorResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Test normal names
        assert generator._sanitize_filename("Coward") == "coward"
        assert generator._sanitize_filename("Test Behavior") == "test_behavior"

        # Test names with special characters
        assert generator._sanitize_filename("Aggressive AI") == "aggressive_ai"
        assert generator._sanitize_filename("Behavior-Type!") == "behavior-type"

        # Test empty name
        assert generator._sanitize_filename("") == "unnamed_resource"


def test_generate_single_ai_behavior_resource():
    """Test generating a single AI behavior resource"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = AIBehaviorResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Create test AI behavior data
        ai_behavior_data = {
            "name": "Coward",
            "accuracy": [0.8, 0.85, 0.9, 0.95, 1.0],
            "evasion": [40.0, 50.0, 60.0, 80.0, 100.0],
            "courage": [50.0, 50.0, 50.0, 50.0, 50.0],
            "patience": [40.0, 50.0, 60.0, 80.0, 100.0],
            "autoscale_by_ai_class": False,
        }

        result_path = generator._generate_data_ai_behavior_resource(ai_behavior_data)

        # Check that the file was created
        assert result_path is not None
        assert result_path != ""
        assert os.path.exists(result_path)

        # Check that the path follows the data-based structure
        assert "assets/data/ai/coward_behavior.tres" in result_path

        # Check the content
        with open(result_path, "r") as f:
            content = f.read()

        # Check for key elements in the content
        assert "Coward" in content
        assert "accuracy = [0.8, 0.85, 0.9, 0.95, 1.0]" in content
        assert "evasion = [40.0, 50.0, 60.0, 80.0, 100.0]" in content
        assert "courage = [50.0, 50.0, 50.0, 50.0, 50.0]" in content
        assert "patience = [40.0, 50.0, 60.0, 80.0, 100.0]" in content
        assert "autoscale_by_ai_class = false" in content


def test_generate_ai_behavior_resources():
    """Test generating multiple AI behavior resources"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = AIBehaviorResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Create test AI behavior data
        ai_behavior_entries = [
            {
                "name": "Coward",
                "accuracy": [0.8, 0.85, 0.9, 0.95, 1.0],
                "evasion": [40.0, 50.0, 60.0, 80.0, 100.0],
                "courage": [50.0, 50.0, 50.0, 50.0, 50.0],
                "patience": [40.0, 50.0, 60.0, 80.0, 100.0],
            },
            {
                "name": "Aggressive",
                "accuracy": [0.9, 0.92, 0.94, 0.96, 0.98],
                "evasion": [20.0, 30.0, 40.0, 60.0, 80.0],
                "courage": [80.0, 85.0, 90.0, 95.0, 100.0],
                "patience": [10.0, 15.0, 20.0, 25.0, 30.0],
            },
        ]

        result_files = generator.generate_ai_behavior_resources(ai_behavior_entries)

        # Should generate 3 files (2 AI behavior resources + 1 registry)
        assert len(result_files) == 3

        # Check that all files exist
        for file_path in result_files.values():
            assert os.path.exists(file_path)

        # Check that registry file is generated
        assert "registry" in result_files


def test_generate_ai_behavior_registry():
    """Test generating AI behavior registry"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock objects for the required parameters
        class MockAssetCatalog:
            def get_asset(self, asset_id):
                return None

        class MockRelationshipBuilder:
            pass

        generator = AIBehaviorResourceGenerator(
            MockAssetCatalog(), MockRelationshipBuilder(), temp_dir
        )

        # Create test AI behavior data
        ai_behavior_entries = [
            {
                "name": "Coward",
                "accuracy": [0.8, 0.85, 0.9, 0.95, 1.0],
            },
            {
                "name": "Aggressive",
                "accuracy": [0.9, 0.92, 0.94, 0.96, 0.98],
            },
        ]

        registry_path = generator._generate_ai_behavior_registry(ai_behavior_entries)

        # Check that the registry file was created
        assert registry_path is not None
        assert registry_path != ""
        assert os.path.exists(registry_path)

        # Check the content
        with open(registry_path, "r") as f:
            content = f.read()

        # Check for key elements in the content
        assert "AIBehaviorRegistryData" in content
        # Check that both AI behaviors are in the registry
        assert "coward_behavior" in content
        assert "aggressive_behavior" in content


if __name__ == "__main__":
    pytest.main([__file__])