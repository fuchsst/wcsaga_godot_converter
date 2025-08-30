#!/usr/bin/env python3
"""
Weapon Banks Data Models

Data classes and models for representing weapon bank configurations parsed from ships.tbl files.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WeaponBank:
    """Represents a single weapon bank configuration"""

    bank_id: int
    weapons: List[str]
    capacity: Optional[int] = None

    def __post_init__(self):
        """Initialize the bank with default capacity if not provided"""
        if self.capacity is None and self.weapons:
            self.capacity = len(self.weapons) * 10  # Default capacity estimation


@dataclass
class PrimaryWeaponBank(WeaponBank):
    """Represents a primary weapon bank"""

    pass


@dataclass
class SecondaryWeaponBank(WeaponBank):
    """Represents a secondary weapon bank"""

    pass


@dataclass
class WeaponBankConfiguration:
    """Comprehensive weapon bank configuration for a ship"""

    # Allowed weapon banks
    allowed_primary_banks: List[List[str]]
    allowed_secondary_banks: List[List[str]]

    # Default weapon banks
    default_primary_banks: List[str]
    default_secondary_banks: List[str]

    # Dogfight mode banks
    allowed_dogfight_primary_banks: Optional[List[List[str]]] = None
    allowed_dogfight_secondary_banks: Optional[List[List[str]]] = None

    # Bank capacities
    secondary_bank_capacities: List[int] = field(default_factory=list)

    # Weapon energy properties
    weapon_regeneration_rate: Optional[float] = None
    max_weapon_energy: Optional[float] = None

    def __post_init__(self):
        """Initialize with default values if needed"""
        if self.secondary_bank_capacities is None:
            self.secondary_bank_capacities = []
        if self.allowed_dogfight_primary_banks is None:
            self.allowed_dogfight_primary_banks = []
        if self.allowed_dogfight_secondary_banks is None:
            self.allowed_dogfight_secondary_banks = []


@dataclass
class WeaponSystem:
    """Represents the complete weapon system of a ship"""

    configuration: WeaponBankConfiguration
    primary_banks: List[PrimaryWeaponBank]
    secondary_banks: List[SecondaryWeaponBank]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WeaponSystem":
        """Create WeaponSystem from parsed ship data"""
        # Create weapon bank configuration
        config = WeaponBankConfiguration(
            allowed_primary_banks=data.get("allowed_pbanks", []),
            allowed_secondary_banks=data.get("allowed_sbanks", []),
            default_primary_banks=data.get("default_pbanks", []),
            default_secondary_banks=data.get("default_sbanks", []),
            secondary_bank_capacities=data.get("sbank_capacity", []),
            weapon_regeneration_rate=data.get("weapon_regeneration_rate"),
            max_weapon_energy=data.get("max_weapon_energy"),
        )

        # Add dogfight banks if available
        if "allowed_dogfight_pbanks" in data:
            config.allowed_dogfight_primary_banks = data["allowed_dogfight_pbanks"]
        if "allowed_dogfight_sbanks" in data:
            config.allowed_dogfight_secondary_banks = data["allowed_dogfight_sbanks"]

        # Create primary weapon banks
        primary_banks = []
        for i, weapons in enumerate(config.allowed_primary_banks):
            primary_banks.append(PrimaryWeaponBank(bank_id=i, weapons=weapons))

        # Create secondary weapon banks
        secondary_banks = []
        for i, weapons in enumerate(config.allowed_secondary_banks):
            capacity = None
            if i < len(config.secondary_bank_capacities):
                capacity = config.secondary_bank_capacities[i]
            secondary_banks.append(
                SecondaryWeaponBank(bank_id=i, weapons=weapons, capacity=capacity)
            )

        return cls(
            configuration=config,
            primary_banks=primary_banks,
            secondary_banks=secondary_banks,
        )
