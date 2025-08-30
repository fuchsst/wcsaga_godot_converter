#!/usr/bin/env python3
"""
Asset Reference Data Models

Data classes and models for representing asset references parsed from ships.tbl files.
These models organize assets by category for proper Godot integration.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ModelAsset:
    """Represents a 3D model asset reference"""
    file_path: str
    asset_type: str = "model"  # pof, obj, gltf, glb
    is_cockpit: bool = False
    is_target: bool = False
    
    def __post_init__(self):
        """Determine asset type from file extension"""
        if self.file_path.lower().endswith('.pof'):
            self.asset_type = "pof"
        elif self.file_path.lower().endswith('.obj'):
            self.asset_type = "obj"
        elif self.file_path.lower().endswith('.gltf'):
            self.asset_type = "gltf"
        elif self.file_path.lower().endswith('.glb'):
            self.asset_type = "glb"


@dataclass
class AudioAsset:
    """Represents an audio asset reference"""
    file_path: str
    asset_type: str = "audio"  # wav, ogg, mp3
    sound_category: str = "general"  # warp, engine, weapon, ui, etc.
    
    def __post_init__(self):
        """Determine asset type from file extension"""
        if self.file_path.lower().endswith('.wav'):
            self.asset_type = "wav"
        elif self.file_path.lower().endswith('.ogg'):
            self.asset_type = "ogg"
        elif self.file_path.lower().endswith('.mp3'):
            self.asset_type = "mp3"


@dataclass
class VisualEffectAsset:
    """Represents a visual effect asset reference"""
    file_path: str
    effect_type: str  # explosion, thruster, warp, shockwave, selection
    asset_type: str = "effect"


@dataclass
class TextureAsset:
    """Represents a texture/UI asset reference"""
    file_path: str
    asset_type: str = "texture"  # dds, png, jpg, tga
    texture_type: str = "general"  # icon, ui, tech, overhead
    
    def __post_init__(self):
        """Determine asset type from file extension"""
        if self.file_path.lower().endswith('.dds'):
            self.asset_type = "dds"
        elif self.file_path.lower().endswith('.png'):
            self.asset_type = "png"
        elif self.file_path.lower().endswith('.jpg') or self.file_path.lower().endswith('.jpeg'):
            self.asset_type = "jpg"
        elif self.file_path.lower().endswith('.tga'):
            self.asset_type = "tga"


@dataclass
class AssetReference:
    """Generic asset reference with metadata"""
    property_name: str
    file_path: str
    asset_category: str  # model, audio, effect, texture
    asset_type: str  # specific file type
    metadata: Optional[Dict[str, any]] = None


@dataclass
class ShipAssetCollection:
    """Complete asset collection for a ship"""
    # 3D Models
    main_model: Optional[ModelAsset] = None
    cockpit_model: Optional[ModelAsset] = None
    target_model: Optional[ModelAsset] = None
    additional_models: List[ModelAsset] = None
    
    # Audio assets
    engine_sounds: List[AudioAsset] = None
    warp_sounds: List[AudioAsset] = None
    weapon_sounds: List[AudioAsset] = None
    ui_sounds: List[AudioAsset] = None
    other_sounds: List[AudioAsset] = None
    
    # Visual effects
    explosion_effects: List[VisualEffectAsset] = None
    thruster_effects: List[VisualEffectAsset] = None
    warp_effects: List[VisualEffectAsset] = None
    shockwave_effects: List[VisualEffectAsset] = None
    selection_effects: List[VisualEffectAsset] = None
    other_effects: List[VisualEffectAsset] = None
    
    # UI/Texture assets
    ship_icons: List[TextureAsset] = None
    overhead_views: List[TextureAsset] = None
    tech_database_assets: List[TextureAsset] = None
    other_textures: List[TextureAsset] = None
    
    def __post_init__(self):
        """Initialize list fields"""
        if self.additional_models is None:
            self.additional_models = []
        if self.engine_sounds is None:
            self.engine_sounds = []
        if self.warp_sounds is None:
            self.warp_sounds = []
        if self.weapon_sounds is None:
            self.weapon_sounds = []
        if self.ui_sounds is None:
            self.ui_sounds = []
        if self.other_sounds is None:
            self.other_sounds = []
        if self.explosion_effects is None:
            self.explosion_effects = []
        if self.thruster_effects is None:
            self.thruster_effects = []
        if self.warp_effects is None:
            self.warp_effects = []
        if self.shockwave_effects is None:
            self.shockwave_effects = []
        if self.selection_effects is None:
            self.selection_effects = []
        if self.other_effects is None:
            self.other_effects = []
        if self.ship_icons is None:
            self.ship_icons = []
        if self.overhead_views is None:
            self.overhead_views = []
        if self.tech_database_assets is None:
            self.tech_database_assets = []
        if self.other_textures is None:
            self.other_textures = []
    
    @classmethod
    def from_asset_registry(cls, asset_registry: List[Dict]) -> 'ShipAssetCollection':
        """Create ShipAssetCollection from asset registry data"""
        collection = cls()
        
        for asset_ref in asset_registry:
            property_name = asset_ref.get("property", "")
            file_path = asset_ref.get("asset_path", "")
            asset_type = asset_ref.get("asset_type", "unknown")
            
            # Model assets
            if asset_type == "model":
                model_asset = ModelAsset(file_path=file_path)
                if "cockpit" in property_name.lower():
                    model_asset.is_cockpit = True
                    collection.cockpit_model = model_asset
                elif "target" in property_name.lower():
                    model_asset.is_target = True
                    collection.target_model = model_asset
                elif property_name in ["pof_file", "model_file"]:
                    collection.main_model = model_asset
                else:
                    collection.additional_models.append(model_asset)
            
            # Audio assets
            elif asset_type == "audio":
                audio_asset = AudioAsset(file_path=file_path)
                if "warp" in property_name.lower():
                    audio_asset.sound_category = "warp"
                    collection.warp_sounds.append(audio_asset)
                elif "engine" in property_name.lower() or "engsnd" in property_name.lower():
                    audio_asset.sound_category = "engine"
                    collection.engine_sounds.append(audio_asset)
                elif "alive" in property_name.lower() or "dead" in property_name.lower():
                    audio_asset.sound_category = "state"
                    collection.other_sounds.append(audio_asset)
                elif "rotation" in property_name.lower():
                    audio_asset.sound_category = "rotation"
                    collection.other_sounds.append(audio_asset)
                elif "turret" in property_name.lower():
                    audio_asset.sound_category = "turret"
                    collection.weapon_sounds.append(audio_asset)
                elif "thruster" in property_name.lower():
                    audio_asset.sound_category = "thruster"
                    collection.other_sounds.append(audio_asset)
                else:
                    collection.other_sounds.append(audio_asset)
            
            # Animation/Effect assets
            elif asset_type == "animation":
                effect_asset = VisualEffectAsset(
                    file_path=file_path,
                    effect_type="general"
                )
                if "explosion" in property_name.lower():
                    effect_asset.effect_type = "explosion"
                    collection.explosion_effects.append(effect_asset)
                elif "thruster" in property_name.lower():
                    effect_asset.effect_type = "thruster"
                    collection.thruster_effects.append(effect_asset)
                elif "warp" in property_name.lower():
                    effect_asset.effect_type = "warp"
                    collection.warp_effects.append(effect_asset)
                elif "shockwave" in property_name.lower():
                    effect_asset.effect_type = "shockwave"
                    collection.shockwave_effects.append(effect_asset)
                elif "selection" in property_name.lower():
                    effect_asset.effect_type = "selection"
                    collection.selection_effects.append(effect_asset)
                else:
                    collection.other_effects.append(effect_asset)
            
            # Texture/UI assets
            elif asset_type == "texture":
                texture_asset = TextureAsset(file_path=file_path)
                if "icon" in property_name.lower():
                    texture_asset.texture_type = "icon"
                    collection.ship_icons.append(texture_asset)
                elif "overhead" in property_name.lower():
                    texture_asset.texture_type = "overhead"
                    collection.overhead_views.append(texture_asset)
                elif "tech" in property_name.lower():
                    texture_asset.texture_type = "tech"
                    collection.tech_database_assets.append(texture_asset)
                else:
                    collection.other_textures.append(texture_asset)
        
        return collection