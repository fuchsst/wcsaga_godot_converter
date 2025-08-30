#!/usr/bin/env python3
"""
Data Converter Models Package
"""

from .asset_references import (
    ModelAsset,
    AudioAsset,
    VisualEffectAsset,
    TextureAsset,
    AssetReference,
    ShipAssetCollection,
)
from .ship_physics import (
    VelocityVector,
    AccelerationRates,
    RotationalPhysics,
    AfterburnerStats,
    ShipPhysics,
)
from .weapon_banks import (
    WeaponBank,
    PrimaryWeaponBank,
    SecondaryWeaponBank,
    WeaponBankConfiguration,
    WeaponSystem,
)

__all__ = [
    # Asset references
    "ModelAsset",
    "AudioAsset",
    "VisualEffectAsset",
    "TextureAsset",
    "AssetReference",
    "ShipAssetCollection",
    # Ship physics
    "VelocityVector",
    "AccelerationRates",
    "RotationalPhysics",
    "AfterburnerStats",
    "ShipPhysics",
    # Weapon banks
    "WeaponBank",
    "PrimaryWeaponBank",
    "SecondaryWeaponBank",
    "WeaponBankConfiguration",
    "WeaponSystem",
]
