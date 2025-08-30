#!/usr/bin/env python3
"""
Unit tests for WeaponTableConverter asset reference extraction
"""

import tempfile
from pathlib import Path
import pytest

from data_converter.table_converters.weapon_table_converter import WeaponTableConverter
from data_converter.table_converters.base_converter import ParseState


def test_parse_weapon_asset_references():
    """Test parsing weapon asset references including new patterns"""
    # Create test content with asset references
    test_content = [
        "$Name: Test Weapon",
        "$Damage: 25",
        "$Icon: IconTest",
        "$Anim: LoadoutTest",
        "$LaunchSnd: 80",
        "$ImpactSnd: 85",
        "$FlyBySnd: 90",
        "$Muzzleflash: TestMuzzle",
        "$Impact Effect: TestImpact",
        "$Impact Explosion Radius: 2.5",
        "$end_multi_text",
    ]

    state = ParseState(lines=test_content, current_line=0)
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = WeaponTableConverter(source_dir, target_dir)
        result = converter.parse_entry(state)

        assert result is not None
        assert result["name"] == "Test Weapon"
        assert result["damage"] == 25.0
        assert result["icon"] == "IconTest"
        assert result["anim"] == "LoadoutTest"
        assert result["launch_sound"] == "80"
        assert result["impact_sound"] == "85"
        assert result["flyby_sound"] == "90"
        assert result["muzzleflash"] == "TestMuzzle"
        assert result["impact_effect"] == "TestImpact"
        assert result["impact_explosion_radius"] == 2.5


def test_parse_weapon_with_model_file():
    """Test parsing weapon with model file reference"""
    # Create test content with model file
    test_content = [
        "$Name: Test Missile",
        "$Model File: test_missile.pof",
        "$Damage: 100",
        "$Velocity: 300",
        "$end_multi_text",
    ]

    state = ParseState(lines=test_content, current_line=0)
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = WeaponTableConverter(source_dir, target_dir)
        result = converter.parse_entry(state)

        assert result is not None
        assert result["name"] == "Test Missile"
        assert result["model_file"] == "test_missile.pof"
        assert result["damage"] == 100.0
        assert result["velocity"] == 300.0


if __name__ == "__main__":
    pytest.main([__file__])
