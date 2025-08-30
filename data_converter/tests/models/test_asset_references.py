#!/usr/bin/env python3
"""
Unit tests for asset reference models
"""

import tempfile
from pathlib import Path
import pytest

from data_converter.models.asset_references import (
    ModelAsset, AudioAsset, VisualEffectAsset, TextureAsset, ShipAssetCollection
)
from data_converter.table_converters.ship_table_converter import ShipTableConverter
from data_converter.table_converters.base_converter import ParseState


def test_model_asset_creation():
    """Test ModelAsset creation and type detection"""
    # Test POF model
    pof_asset = ModelAsset(file_path="test_ship.pof")
    assert pof_asset.file_path == "test_ship.pof"
    assert pof_asset.asset_type == "pof"
    assert pof_asset.is_cockpit == False
    assert pof_asset.is_target == False
    
    # Test GLTF model
    gltf_asset = ModelAsset(file_path="test_ship.gltf")
    assert gltf_asset.file_path == "test_ship.gltf"
    assert gltf_asset.asset_type == "gltf"


def test_audio_asset_creation():
    """Test AudioAsset creation and type detection"""
    # Test WAV audio
    wav_asset = AudioAsset(file_path="engine_sound.wav")
    assert wav_asset.file_path == "engine_sound.wav"
    assert wav_asset.asset_type == "wav"
    assert wav_asset.sound_category == "general"
    
    # Test with specific category
    warp_asset = AudioAsset(file_path="warpin_sound.ogg", sound_category="warp")
    assert warp_asset.file_path == "warpin_sound.ogg"
    assert warp_asset.asset_type == "ogg"
    assert warp_asset.sound_category == "warp"


def test_visual_effect_asset_creation():
    """Test VisualEffectAsset creation"""
    effect_asset = VisualEffectAsset(file_path="explosion_effect", effect_type="explosion")
    assert effect_asset.file_path == "explosion_effect"
    assert effect_asset.effect_type == "explosion"
    assert effect_asset.asset_type == "effect"


def test_texture_asset_creation():
    """Test TextureAsset creation and type detection"""
    # Test DDS texture
    dds_asset = TextureAsset(file_path="ship_icon.dds")
    assert dds_asset.file_path == "ship_icon.dds"
    assert dds_asset.asset_type == "dds"
    assert dds_asset.texture_type == "general"
    
    # Test with specific type
    icon_asset = TextureAsset(file_path="shield_icon.png", texture_type="icon")
    assert icon_asset.file_path == "shield_icon.png"
    assert icon_asset.asset_type == "png"
    assert icon_asset.texture_type == "icon"


def test_ship_asset_collection_creation():
    """Test ShipAssetCollection creation and initialization"""
    collection = ShipAssetCollection()
    
    # Check that all list fields are initialized
    assert collection.additional_models == []
    assert collection.engine_sounds == []
    assert collection.warp_sounds == []
    assert collection.weapon_sounds == []
    assert collection.ui_sounds == []
    assert collection.other_sounds == []
    assert collection.explosion_effects == []
    assert collection.thruster_effects == []
    assert collection.warp_effects == []
    assert collection.shockwave_effects == []
    assert collection.selection_effects == []
    assert collection.other_effects == []
    assert collection.ship_icons == []
    assert collection.overhead_views == []
    assert collection.tech_database_assets == []
    assert collection.other_textures == []


def test_ship_asset_collection_from_registry():
    """Test creating ShipAssetCollection from asset registry data"""
    # Create test asset registry data
    asset_registry = [
        {
            "property": "pof_file",
            "asset_path": "test_ship.pof",
            "asset_type": "model"
        },
        {
            "property": "cockpit_pof_file",
            "asset_path": "test_cockpit.pof",
            "asset_type": "model"
        },
        {
            "property": "engine_sound",
            "asset_path": "engine.wav",
            "asset_type": "audio"
        },
        {
            "property": "warpin_start_sound",
            "asset_path": "warpin.ogg",
            "asset_type": "audio"
        },
        {
            "property": "explosion_animations",
            "asset_path": "explosion_effect",
            "asset_type": "animation"
        },
        {
            "property": "ship_icon",
            "asset_path": "ship_icon.dds",
            "asset_type": "texture"
        }
    ]
    
    # Create collection from registry
    collection = ShipAssetCollection.from_asset_registry(asset_registry)
    
    # Check that assets are properly categorized
    assert collection.main_model is not None
    assert collection.main_model.file_path == "test_ship.pof"
    assert collection.cockpit_model is not None
    assert collection.cockpit_model.file_path == "test_cockpit.pof"
    assert len(collection.engine_sounds) == 1
    assert collection.engine_sounds[0].file_path == "engine.wav"
    assert len(collection.warp_sounds) == 1
    assert collection.warp_sounds[0].file_path == "warpin.ogg"
    assert len(collection.explosion_effects) == 1
    assert collection.explosion_effects[0].file_path == "explosion_effect"
    assert len(collection.ship_icons) == 1
    assert collection.ship_icons[0].file_path == "ship_icon.dds"


if __name__ == "__main__":
    pytest.main([__file__])