#!/usr/bin/env python3
"""
Ship Physics Data Models

Data classes and models for representing ship physics properties parsed from ships.tbl files.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class VelocityVector:
    """Represents velocity components in different directions"""
    forward: float = 0.0
    reverse: float = 0.0
    side: float = 0.0
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'VelocityVector':
        """Create VelocityVector from dictionary"""
        return cls(
            forward=data.get('forward', 0.0),
            reverse=data.get('reverse', 0.0),
            side=data.get('side', 0.0)
        )


@dataclass
class AccelerationRates:
    """Represents acceleration rates for different movement types"""
    forward: float = 0.0
    reverse: float = 0.0
    side: float = 0.0
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'AccelerationRates':
        """Create AccelerationRates from dictionary"""
        return cls(
            forward=data.get('forward', 0.0),
            reverse=data.get('reverse', 0.0),
            side=data.get('side', 0.0)
        )


@dataclass
class RotationalPhysics:
    """Represents rotational physics properties"""
    pitch: float = 0.0
    bank: float = 0.0
    heading: float = 0.0
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'RotationalPhysics':
        """Create RotationalPhysics from dictionary"""
        return cls(
            pitch=data.get('pitch', 0.0),
            bank=data.get('bank', 0.0),
            heading=data.get('heading', 0.0)
        )


@dataclass
class AfterburnerStats:
    """Represents afterburner-related statistics"""
    fuel_capacity: float = 0.0
    max_velocity: float = 0.0
    acceleration_mult: float = 1.0  # Multiplier for normal acceleration when afterburning
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'AfterburnerStats':
        """Create AfterburnerStats from dictionary"""
        return cls(
            fuel_capacity=data.get('fuel_capacity', 0.0),
            max_velocity=data.get('max_velocity', 0.0),
            acceleration_mult=data.get('acceleration_mult', 1.0)
        )


@dataclass
class ShipPhysics:
    """Comprehensive ship physics properties"""
    # Basic physical properties
    mass: float = 0.0
    density: float = 0.0
    
    # Velocity properties
    max_velocity: Optional[VelocityVector] = None
    afterburner_velocity: Optional[VelocityVector] = None
    
    # Acceleration properties
    acceleration: Optional[AccelerationRates] = None
    
    # Rotational properties
    rotation: Optional[RotationalPhysics] = None
    
    # Afterburner properties
    afterburner: Optional[AfterburnerStats] = None
    
    # Other physics properties
    hitpoints: float = 0.0
    power_output: float = 0.0
    max_weapon_energy: float = 0.0
    
    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'ShipPhysics':
        """Create ShipPhysics from dictionary of parsed properties"""
        physics = cls()
        
        # Basic properties
        physics.mass = data.get('mass', 0.0)
        physics.density = data.get('density', 0.0)
        physics.hitpoints = data.get('hitpoints', 0.0)
        physics.power_output = data.get('power_output', 0.0)
        physics.max_weapon_energy = data.get('max_weapon_energy', 0.0)
        
        # Velocity vectors
        if 'max_velocity' in data:
            if isinstance(data['max_velocity'], dict):
                physics.max_velocity = VelocityVector.from_dict(data['max_velocity'])
            else:
                # Handle single value case
                val = float(data['max_velocity']) if data['max_velocity'] else 0.0
                physics.max_velocity = VelocityVector(forward=val, reverse=val, side=val)
                
        if 'afterburner_velocity' in data:
            # Convert to VelocityVector format
            val = float(data['afterburner_velocity']) if data['afterburner_velocity'] else 0.0
            physics.afterburner_velocity = VelocityVector(forward=val, reverse=val, side=val)
        
        # Afterburner stats
        afterburner_data = {}
        if 'afterburner_fuel' in data:
            afterburner_data['fuel_capacity'] = float(data['afterburner_fuel'])
        if 'afterburner_velocity' in data:
            # Use the forward velocity as the max afterburner velocity
            if physics.afterburner_velocity:
                afterburner_data['max_velocity'] = physics.afterburner_velocity.forward
        physics.afterburner = AfterburnerStats.from_dict(afterburner_data)
        
        return physics