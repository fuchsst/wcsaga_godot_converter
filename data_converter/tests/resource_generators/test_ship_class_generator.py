#!/usr/bin/env python3
"""
Unit tests for ShipClassGenerator
"""

import tempfile
import os
import pytest

from data_converter.resource_generators.ship_class_generator import ShipClassGenerator


def test_ship_class_generator_initialization():
    """Test ShipClassGenerator initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        generator = ShipClassGenerator(temp_dir)

        # Check that the generator is properly initialized
        assert generator.output_dir == temp_dir
        assert generator.ships_dir is None


def test_determine_faction():
    """Test faction determination"""
    with tempfile.TemporaryDirectory() as temp_dir:
        generator = ShipClassGenerator(temp_dir)

        # Test Terran faction
        assert generator._determine_faction("GTB Nova") == "terran"
        assert generator._determine_faction("GTF Rapier") == "terran"
        assert generator._determine_faction("GTCv Deimos") == "terran"

        # Test Vasudan faction
        assert generator._determine_faction("PVF Hawk") == "vasudan"
        assert generator._determine_faction("PVB Demon") == "vasudan"

        # Test Shivan faction
        assert generator._determine_faction("SF Dragon") == "shivan"
        assert generator._determine_faction("SB Banshee") == "shivan"

        # Test other faction
        assert generator._determine_faction("Unknown Ship") == "other"


def test_determine_ship_category():
    """Test ship category determination"""
    with tempfile.TemporaryDirectory() as temp_dir:
        generator = ShipClassGenerator(temp_dir)

        # Test bomber category (GTB should be bomber)
        assert generator._determine_ship_category("GTB Nova") == "bomber"
        assert generator._determine_ship_category("GTF Rapier") == "fighter"
        assert generator._determine_ship_category("Stealth Fighter") == "fighter"

        # Test bomber category
        assert generator._determine_ship_category("GTB Hades") == "bomber"
        assert generator._determine_ship_category("Assault Ship") == "bomber"

        # Test corvette category
        assert generator._determine_ship_category("Corvette") == "corvette"
        assert generator._determine_ship_category("Gunboat") == "corvette"

        # Test cruiser category (GTC should be cruiser)
        assert generator._determine_ship_category("GTCv Deimos") == "cruiser"
        assert generator._determine_ship_category("Destroyer") == "cruiser"

        # Test capital category
        assert generator._determine_ship_category("GTD Hekate") == "capital"
        assert generator._determine_ship_category("Dreadnought") == "capital"
        assert generator._determine_ship_category("Carrier") == "capital"

        # Test transport category
        assert generator._determine_ship_category("Transport") == "transport"
        assert generator._determine_ship_category("Cargo Ship") == "transport"
        assert generator._determine_ship_category("Freighter") == "transport"


def test_sanitize_filename():
    """Test filename sanitization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        generator = ShipClassGenerator(temp_dir)

        # Test normal names
        assert generator._sanitize_filename("GTB Nova") == "gtb_nova"
        assert generator._sanitize_filename("GTF Rapier") == "gtf_rapier"

        # Test names with special characters
        assert generator._sanitize_filename("GTB Nova!") == "gtb_nova"
        assert generator._sanitize_filename("GTF.Rapier") == "gtf_rapier"

        # Test empty name
        assert generator._sanitize_filename("") == "unnamed_ship"


def test_format_weapon_banks():
    """Test weapon bank formatting"""
    with tempfile.TemporaryDirectory() as temp_dir:
        generator = ShipClassGenerator(temp_dir)

        # Test empty list
        assert generator._format_weapon_banks([]) == "[]"

        # Test single bank with single weapon
        assert generator._format_weapon_banks([["Laser"]]) == '[["Laser"]]'

        # Test multiple banks with multiple weapons
        result = generator._format_weapon_banks([["Laser", "Ion"], ["Missile"]])
        assert result == '[["Laser", "Ion"], ["Missile"]]'


def test_format_integer_list():
    """Test integer list formatting"""
    with tempfile.TemporaryDirectory() as temp_dir:
        generator = ShipClassGenerator(temp_dir)

        # Test empty list
        assert generator._format_integer_list([]) == "[]"

        # Test single integer
        assert generator._format_integer_list([20]) == "[20]"

        # Test multiple integers
        assert generator._format_integer_list([20, 15, 10]) == "[20, 15, 10]"


def test_generate_single_ship_resource_fighter():
    """Test generating a single fighter ship resource"""
    with tempfile.TemporaryDirectory() as temp_dir:
        generator = ShipClassGenerator(temp_dir)

        # Create test ship data
        ship_data = {
            "name": "GTB Nova",
            "hitpoints": 150.0,
            "max_shield": 100.0,
            "mass": 50.0,
            "max_velocity": 75.0,
            "pof_file": "nova.pof",
            "ship_icon": "nova_icon.png",
            "allowed_pbanks": [["Laser"], ["Ion"]],
            "allowed_sbanks": [["Missile"]],
            "sbank_capacity": [20, 20],
        }

        result_path = generator._generate_single_ship_resource(ship_data)

        # Check that the file was created
        assert result_path is not None
        assert result_path != ""
        assert os.path.exists(result_path)

        # Check that the path follows the feature-based structure
        assert "features/fighters/terran/gtb_nova/gtb_nova.tres" in result_path

        # Check the content
        with open(result_path, "r") as f:
            content = f.read()

        # Check for key elements in the content
        assert "GTB Nova" in content
        assert "max_velocity = 75.0" in content
        assert "max_hull_strength = 150.0" in content
        assert 'allowed_primary_banks = [["Laser"], ["Ion"]]' in content
        assert 'allowed_secondary_banks = [["Missile"]]' in content
        assert "secondary_bank_capacities = [20, 20]" in content


def test_generate_single_ship_resource_capital():
    """Test generating a single capital ship resource"""
    with tempfile.TemporaryDirectory() as temp_dir:
        generator = ShipClassGenerator(temp_dir)

        # Create test ship data (use a proper capital ship name)
        ship_data = {
            "name": "GTD Hekate",
            "hitpoints": 1000.0,
            "max_shield": 500.0,
            "mass": 10000.0,
            "max_velocity": 30.0,
            "pof_file": "hekate.pof",
            "ship_icon": "hekate_icon.png",
        }

        result_path = generator._generate_single_ship_resource(ship_data)

        # Check that the file was created
        assert result_path is not None
        assert result_path != ""
        assert os.path.exists(result_path)

        # Check that the path follows the feature-based structure
        assert "features/capital_ships/terran/gtd_hekate/gtd_hekate.tres" in result_path


def test_generate_ship_resources():
    """Test generating multiple ship resources"""
    with tempfile.TemporaryDirectory() as temp_dir:
        generator = ShipClassGenerator(temp_dir)

        # Create test ship data
        ship_entries = [
            {
                "name": "GTB Nova",
                "hitpoints": 150.0,
                "max_shield": 100.0,
                "mass": 50.0,
                "max_velocity": 75.0,
                "pof_file": "nova.pof",
                "ship_icon": "nova_icon.png",
            },
            {
                "name": "GTD Hekate",
                "hitpoints": 1000.0,
                "max_shield": 500.0,
                "mass": 10000.0,
                "max_velocity": 30.0,
                "pof_file": "hekate.pof",
                "ship_icon": "hekate_icon.png",
            },
        ]

        result_files = generator.generate_ship_resources(ship_entries)

        # Should generate 3 files (2 ship resources + 1 registry)
        assert len(result_files) == 3

        # Check that all files exist
        for file_path in result_files:
            assert os.path.exists(file_path)

        # Check that registry file is generated
        registry_files = [f for f in result_files if "ship_registry.tres" in f]
        assert len(registry_files) == 1


def test_generate_ship_registry():
    """Test generating ship registry"""
    with tempfile.TemporaryDirectory() as temp_dir:
        generator = ShipClassGenerator(temp_dir)

        # Create test ship data
        ship_entries = [
            {
                "name": "GTB Nova",
                "hitpoints": 150.0,
                "max_shield": 100.0,
                "mass": 50.0,
                "max_velocity": 75.0,
            },
            {
                "name": "GTD Hekate",
                "hitpoints": 1000.0,
                "max_shield": 500.0,
                "mass": 10000.0,
                "max_velocity": 30.0,
            },
        ]

        registry_path = generator._generate_ship_registry(ship_entries)

        # Check that the registry file was created
        assert registry_path is not None
        assert registry_path != ""
        assert os.path.exists(registry_path)

        # Check the content
        with open(registry_path, "r") as f:
            content = f.read()

        # Check for key elements in the content
        assert "ShipRegistryData" in content
        # Check that both ships are in the registry
        assert "gtb_nova" in content
        assert "gtd_hekate" in content
        assert "terran" in content
        assert "bomber" in content
        assert "capital" in content


if __name__ == "__main__":
    pytest.main([__file__])
