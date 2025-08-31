"""
Core data structures for table parsing and conversion.

This module contains the fundamental data classes used throughout the table conversion
system, including parsing state, ship classes, weapons, armor types, species, and IFF data.
These classes are designed to be independent and not depend on any other modules.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class ParseError(Exception):
    """Custom exception for table parsing errors"""

    def __init__(self, message: str, line_number: int = -1, filename: str = ""):
        self.message = message
        self.line_number = line_number
        self.filename = filename
        super().__init__(f"{filename}:{line_number}: {message}")


class TableType(Enum):
    """Table file types supported by the converter"""

    AI = "ai"
    AI_PROFILES = "ai_profiles"
    ARMOR = "armor"
    ASTEROID = "asteroid"
    CUTSCENES = "cutscenes"
    FIREBALL = "fireball"
    HUD_GAUGES = "hud_gauges"
    IFF = "iff_defs"
    LIGHTNING = "lightning"
    NEBULA = "nebula"
    MEDALS = "medals"
    MFLASH = "mflash"
    MUSIC = "music"
    RANK = "rank"
    SCRIPTING = "scripting"
    SHIPS = "ships"
    SOUNDS = "sounds"
    SPECIES = "species_defs"
    SPECIES_ENTRIES = "species"
    STARS = "stars"
    STRINGS = "strings"
    UNKNOWN = "unknown"
    WEAPONS = "weapons"
    WEAPON_EXPL = "weapon_expl"


@dataclass
class ShipClassData:
    """Complete ship class data structure."""

    name: str = ""
    alt_name: str = ""
    short_name: str = ""
    species: str = ""
    class_type: str = ""
    manufacturer: str = ""

    # Model and visual
    pof_file: str = ""
    cockpit_pof_file: str = ""

    # Physics and performance
    density: float = 0.0
    damp: float = 0.0
    rotdamp: float = 0.0
    banking_constant: float = 0.0
    max_velocity: float = 0.0
    rear_velocity: float = 0.0
    forward_accel: float = 0.0
    forward_decel: float = 0.0
    slide_accel: float = 0.0
    slide_decel: float = 0.0
    can_glide: bool = False
    dynamic_glide_cap: bool = False
    max_glide_speed: float = 0.0
    glide_accel_mult: float = 0.0
    use_newtonian_dampening: bool = False
    autoaim_fov: float = 0.0

    # Combat capabilities
    primary_weapon_count: int = 0
    secondary_weapon_count: int = 0

    # Defense and durability
    shields: float = 0.0
    hull: float = 0.0
    hull_repair_rate: float = 0.0
    subsystem_repair_rate: float = 0.0
    armor_type: str = ""
    shield_armor_type: str = ""

    # Power and systems
    power_output: float = 0.0
    max_oclk_speed: float = 0.0
    max_weapon_reserve: float = 0.0
    max_shield_regen: float = 0.0
    max_weapon_regen: float = 0.0
    has_afterburner: bool = False
    afterburner_fuel_capacity: float = 0.0
    afterburner_burn_rate: float = 0.0
    afterburner_rec_rate: float = 0.0
    afterburner_forward_accel: float = 0.0

    # Countermeasures and sensors
    countermeasures: int = 0
    engine_sound: str = ""

    # UI and interface
    closeup_zoom: float = 0.0
    shield_icon: str = ""
    ship_icon: str = ""
    ship_anim: str = ""
    ship_overhead: str = ""
    score: int = 0
    scan_time: int = 0

    # AI and behavior
    ai_class: int = 0

    # Explosion properties
    explosion_damage_type: str = ""
    explosion_inner_damage: float = 0.0
    explosion_outer_damage: float = 0.0
    explosion_inner_radius: float = 0.0
    explosion_outer_radius: float = 0.0
    explosion_shockwave_speed: float = 0.0

    # Impact effects
    impact_spew_max_particles: int = 0

    # Damage effects
    damage_spew_max_particles: int = 0

    # Debris properties
    debris_min_lifetime: float = 0.0
    debris_max_lifetime: float = 0.0
    debris_min_speed: float = 0.0
    debris_max_speed: float = 0.0
    debris_min_rotation_speed: float = 0.0
    debris_max_rotation_speed: float = 0.0
    debris_damage_type: str = ""
    debris_min_hitpoints: float = 0.0
    debris_max_hitpoints: float = 0.0
    debris_damage_multiplier: float = 0.0
    debris_lightning_arc_percent: float = 0.0

    # Subsystems
    subsystems: List[Dict[str, Any]] = field(default_factory=list)

    # Texture replacements
    texture_replacements: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class WeaponData:
    """Weapon definition data structure."""

    name: str = ""
    display_name: str = ""
    description: str = ""
    tech_description: str = ""
    model_file: str = ""
    model_scale: float = 1.0

    # Ballistic properties
    velocity: float = 0.0
    lifetime: float = 0.0
    damage: float = 0.0
    damage_type: str = ""
    armor_piercing: bool = False

    # Energy properties
    energy_consumption: float = 0.0
    heat_production: float = 0.0

    # Firing properties
    fire_rate: float = 0.0
    burst_count: int = 0
    burst_delay: float = 0.0

    # Visual effects
    muzzle_flash: str = ""
    impact_effect: str = ""
    trail_effect: str = ""

    # Audio
    fire_sound: str = ""
    impact_sound: str = ""

    # Compatibility
    compatible_ships: List[str] = field(default_factory=list)


@dataclass
class ArmorTypeData:
    """Armor type definition data structure."""

    name: str = ""
    damage_type_modifiers: Dict[str, float] = field(default_factory=dict)


@dataclass
class SpeciesData:
    """Species definition data structure."""

    name: str = ""
    display_name: str = ""
    default_iff: str = ""
    default_armor: str = ""
    color: str = ""

    # AI behavior
    ai_aggression: float = 0.0
    ai_caution: float = 0.0
    ai_accuracy: float = 0.0


@dataclass
class IFFData:
    """IFF (Identification Friend or Foe) definition data structure."""

    name: str = ""
    display_name: str = ""
    color: str = ""

    # Relationships
    hostile_to: List[str] = field(default_factory=list)
    friendly_to: List[str] = field(default_factory=list)


@dataclass
class AIProfileData:
    """AI profile definition data structure with difficulty scaling parameters."""

    name: str = ""
    default_profile: str = ""
    
    # Difficulty scaling parameters (5 values for Very Easy, Easy, Medium, Hard, Insane)
    primary_weapon_delay: List[float] = field(default_factory=lambda: [0.0] * 5)
    secondary_weapon_delay: List[float] = field(default_factory=lambda: [0.0] * 5)
    shield_manage_delay: List[float] = field(default_factory=lambda: [0.0] * 5)
    predict_position_delay: List[float] = field(default_factory=lambda: [0.0] * 5)
    in_range_time: List[float] = field(default_factory=lambda: [0.0] * 5)
    accuracy_scale: List[float] = field(default_factory=lambda: [0.0] * 5)
    evasion_scale: List[float] = field(default_factory=lambda: [0.0] * 5)
    courage_scale: List[float] = field(default_factory=lambda: [0.0] * 5)
    
    # Boolean flags
    use_countermeasures: List[bool] = field(default_factory=lambda: [False] * 5)
    evade_missiles: List[bool] = field(default_factory=lambda: [False] * 5)
    allow_player_targeting: List[bool] = field(default_factory=lambda: [False] * 5)
    ai_aims_at_friendly: List[bool] = field(default_factory=lambda: [False] * 5)
    respect_player_orders: List[bool] = field(default_factory=lambda: [True] * 5)


@dataclass
class AIBehaviorData:
    """AI behavior definition data structure with combat parameters."""

    name: str = ""
    
    # Combat behavior parameters (5 values for Trainee, Rookie, Hotshot, Ace, Insane)
    accuracy: List[float] = field(default_factory=lambda: [0.0] * 5)  # 0.0 .. 1.0
    evasion: List[float] = field(default_factory=lambda: [0.0] * 5)   # 0.0 .. 100.0
    courage: List[float] = field(default_factory=lambda: [0.0] * 5)   # 0.0 .. 100.0
    patience: List[float] = field(default_factory=lambda: [0.0] * 5)  # 0.0 .. 100.0
    
    # Additional behavior parameters
    afterburner_use_factor: List[float] = field(default_factory=lambda: [0.0] * 5)
    shockwave_evade_chances: List[float] = field(default_factory=lambda: [0.0] * 5)
    get_away_chance: List[float] = field(default_factory=lambda: [0.0] * 5)
    secondary_range_multiplier: List[float] = field(default_factory=lambda: [0.0] * 5)
    bomb_range_multiplier: List[float] = field(default_factory=lambda: [0.0] * 5)
    
    # Boolean flags
    autoscale_by_ai_class: bool = False
    ai_countermeasure_firing_chance: List[float] = field(default_factory=lambda: [0.0] * 5)
