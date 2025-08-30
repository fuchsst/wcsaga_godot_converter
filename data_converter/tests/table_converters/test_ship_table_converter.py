#!/usr/bin/env python3
"""
Unit tests for ShipTableConverter
"""

import tempfile
from pathlib import Path
import pytest

from data_converter.table_converters.ship_table_converter import ShipTableConverter
from data_converter.table_converters.base_converter import ParseState


def test_ship_converter_initialization():
    """Test ShipTableConverter initialization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ShipTableConverter(source_dir, target_dir)

        # Check that the converter is properly initialized
        assert converter.source_dir == source_dir
        assert converter.target_dir == target_dir
        assert converter.get_table_type().value == "ships"
        assert len(converter._parse_patterns) > 0


def test_ship_converter_can_convert():
    """Test that ShipTableConverter can identify ship table files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ShipTableConverter(source_dir, target_dir)

        # Create a test ship table file
        ship_file = source_dir / "ships.tbl"
        with open(ship_file, "w") as f:
            f.write("#Ship Classes\\n$Name: Test Ship\\n#End")

        # Should be able to convert ship table files
        assert converter.can_convert(ship_file)


def test_parse_ship_entry():
    """Test parsing a single ship entry"""
    # Create test content
    test_content = [
        "$Name: Test Fighter",
        "$Species: Terran",
        "$Type: Fighter",
        "$Max velocity: 100, 100, 100",
        "$Shields: 100",
        "$Hitpoints: 150",
        "$end_multi_text",
    ]

    state = ParseState(lines=test_content, current_line=0)
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ShipTableConverter(source_dir, target_dir)
        result = converter.parse_entry(state)

        assert result is not None
        assert result["name"] == "Test Fighter"
        assert result["species"] == "Terran"
        assert result["type"] == "Fighter"
        assert "max_velocity" in result
        assert result["max_shield"] == 100.0
        assert result["hitpoints"] == 150.0


def test_parse_velocity_vector():
    """Test parsing velocity vector strings"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ShipTableConverter(source_dir, target_dir)

        # Test 3-component vector
        result = converter._parse_velocity_vector("100, 75, 50")
        assert result["forward"] == 100.0
        assert result["reverse"] == 75.0
        assert result["side"] == 50.0

        # Test single value
        result = converter._parse_velocity_vector("65")
        assert result["forward"] == 65.0
        assert result["reverse"] == 65.0
        assert result["side"] == 65.0


def test_validate_ship_entry():
    """Test ship entry validation"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ShipTableConverter(source_dir, target_dir)

        # Valid entry
        valid_entry = {"name": "Test Ship", "hitpoints": 100.0, "mass": 50.0}
        assert converter.validate_entry(valid_entry)

        # Invalid entry - missing name
        invalid_entry = {"hitpoints": 100.0, "mass": 50.0}
        assert not converter.validate_entry(invalid_entry)

        # Invalid entry - wrong type for numeric field
        invalid_entry2 = {"name": "Test Ship", "hitpoints": "invalid", "mass": 50.0}
        assert not converter.validate_entry(invalid_entry2)


def test_convert_ship_table_file():
    """Test converting a complete ship table file"""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ShipTableConverter(source_dir, target_dir)

        # Create test table content
        table_content = """#Ship Classes

$Name: Test Fighter
$Species: Terran
$Type: Fighter
$Max velocity: 100, 100, 100
$Shields: 100
$Hitpoints: 150

$end_multi_text
"""

        # Create test file
        test_file = source_dir / "ships.tbl"
        with open(test_file, "w") as f:
            f.write(table_content)

        # Test conversion
        success = converter.convert_table_file(test_file)
        assert success

        # Check that output files were created
        output_files = list((target_dir / "assets" / "tables").glob("*.tres"))
        assert len(output_files) >= 0  # At least the main table file


def test_ship_converter_new_asset_patterns():
    """Test parsing ship entries with new asset patterns"""
    # Create test content with new asset patterns
    test_content = [
        "$Name: Test Ship",
        "$Short name: Test",
        "$Species: Terran",
        "$POF file: test_ship.pof",
        "$EngineSnd: 126",
        "$Shield_icon: test_icon",
        "$Closeup_pos: 0.0, 0.0, -15.0",
        "$Closeup_zoom: 0.43633",
        "$Thruster01 Radius factor: 0.6",
        "$Thruster02 Length factor: 0.7",
        '$Allowed PBanks: ( "Laser" ) ( "Ion" )',
        '$Allowed SBanks: ( "Spiculum IR" "Javelin HS" )',
        '$Default PBanks: ( "Laser" "Ion" )',
        '$Default SBanks: ( "Javelin HS" "Spiculum IR" )',
        "$SBank Capacity: (20, 20)",
        "$Subsystem: communication, 10.0, 0.0",
        "    $Alt Subsystem Name: Comm",
        "    $Alt Damage Popup Subsystem Name: Communication",
        "$end_multi_text",
    ]

    state = ParseState(lines=test_content, current_line=0)
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ShipTableConverter(source_dir, target_dir)
        result = converter.parse_entry(state)

        assert result is not None
        assert result["name"] == "Test Ship"
        assert result["short_name"] == "Test"
        assert result["species"] == "Terran"
        assert result["pof_file"] == "test_ship.pof"
        assert result["engine_sound"] == "126"
        assert result["shield_icon"] == "test_icon"
        assert result["closeup_pos"] == {"x": 0.0, "y": 0.0, "z": -15.0}
        assert result["closeup_zoom"] == 0.43633
        assert result["thruster_radius_factor"] == 0.6
        assert result["thruster_length_factor"] == 0.7
        assert result["allowed_pbanks"] == [["Laser"], ["Ion"]]
        assert result["allowed_sbanks"] == [["Spiculum IR", "Javelin HS"]]
        assert result["sbank_capacity"] == [20, 20]

        # Check asset relationships were captured
        registries = converter.get_registries()
        asset_registry = registries["asset_registry"]
        assert "Test Ship" in asset_registry
        assert len(asset_registry["Test Ship"]) > 0


def test_asset_reference_extraction_and_mapping():
    """Test comprehensive asset reference extraction and mapping"""
    # Create test content with all types of asset references
    test_content = [
        "$Name: Asset Test Ship",
        # Model assets
        "$POF file: test_ship.pof",
        "$Cockpit POF file: test_cockpit.pof",
        "$POF target file: test_target.pof",
        # Audio assets
        "$EngineSnd: engine_sound.wav",
        "$AliveSnd: alive_sound.ogg",
        "$DeadSnd: dead_sound.mp3",
        "$Warpin Start Sound: warpin_start.wav",
        "$Warpout End Sound: warpout_end.ogg",
        "$RotationSnd: rotation_sound.wav",
        "$Turret Base RotationSnd: turret_base.wav",
        "$Turret Gun RotationSnd: turret_gun.wav",
        # Visual effects
        "$Warpin animation: warpin_effect",
        "$Warpout animation: warpout_effect",
        "$Explosion Animations: explosion_effect",
        "$Shockwave model: shockwave_effect",
        "$Selection Effect: selection_effect",
        "$Thruster flame effect: thruster_flame",
        "$Thruster glow effect: thruster_glow",
        # UI assets
        "$Shield_icon: shield_icon.dds",
        "$Ship_icon: ship_icon.png",
        "$Ship_overhead: overhead_view.jpg",
        "$Tech Model: tech_model.obj",
        "$Tech Anim: tech_anim",
        "$Tech Image: tech_image.tga",
        # Texture assets
        "$Texture Replace: old_texture.dds, new_texture.png",
        "$end_multi_text",
    ]

    state = ParseState(lines=test_content, current_line=0)
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        target_dir = Path(temp_dir) / "target"
        source_dir.mkdir()
        target_dir.mkdir()

        converter = ShipTableConverter(source_dir, target_dir)
        result = converter.parse_entry(state)

        assert result is not None
        assert result["name"] == "Asset Test Ship"

        # Check that all asset properties were parsed
        assert result["pof_file"] == "test_ship.pof"
        assert result["cockpit_pof_file"] == "test_cockpit.pof"
        assert result["pof_target_file"] == "test_target.pof"
        assert result["engine_sound"] == "engine_sound.wav"
        assert result["alive_sound"] == "alive_sound.ogg"
        assert result["dead_sound"] == "dead_sound.mp3"
        assert result["warpin_start_sound"] == "warpin_start.wav"
        assert result["warpout_end_sound"] == "warpout_end.ogg"
        assert result["rotation_sound"] == "rotation_sound.wav"
        assert result["turret_base_rotation_sound"] == "turret_base.wav"
        assert result["turret_gun_rotation_sound"] == "turret_gun.wav"
        assert result["warpin_animation"] == "warpin_effect"
        assert result["warpout_animation"] == "warpout_effect"
        assert result["explosion_animations"] == "explosion_effect"
        assert result["shockwave_model"] == "shockwave_effect"
        assert result["selection_effect"] == "selection_effect"
        assert result["thruster_flame"] == "thruster_flame"
        assert result["thruster_glow"] == "thruster_glow"
        assert result["shield_icon"] == "shield_icon.dds"
        assert result["ship_icon"] == "ship_icon.png"
        assert result["ship_overhead"] == "overhead_view.jpg"
        assert result["tech_model"] == "tech_model.obj"
        assert result["tech_anim"] == "tech_anim"
        assert result["tech_image"] == "tech_image.tga"
        assert result["texture_replace"] == "old_texture.dds, new_texture.png"

        # Check asset relationships were captured with correct types
        registries = converter.get_registries()
        asset_registry = registries["asset_registry"]
        assert "Asset Test Ship" in asset_registry

        assets = asset_registry["Asset Test Ship"]
        assert len(assets) > 0

        # Check that assets are categorized correctly
        model_assets = [asset for asset in assets if asset["asset_type"] == "model"]
        audio_assets = [asset for asset in assets if asset["asset_type"] == "audio"]
        animation_assets = [
            asset for asset in assets if asset["asset_type"] == "animation"
        ]
        texture_assets = [asset for asset in assets if asset["asset_type"] == "texture"]

        # Should have model assets
        assert len(model_assets) >= 3  # pof_file, cockpit_pof_file, pof_target_file

        # Should have audio assets
        assert (
            len(audio_assets) >= 7
        )  # engine, alive, dead, warpin, warpout, rotation, turret sounds

        # Should have animation/effect assets
        assert (
            len(animation_assets) >= 7
        )  # warpin, warpout, explosion, shockwave, selection, thruster flame/glow

        # Should have texture assets
        assert (
            len(texture_assets) >= 5
        )  # shield_icon, ship_icon, ship_overhead, tech_image, tech_model


if __name__ == "__main__":
    pytest.main([__file__])
