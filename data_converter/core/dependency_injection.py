#!/usr/bin/env python3
"""
Dependency Injection Container - SOLID Refactoring

Simple dependency injection container to decouple components and
follow Dependency Inversion Principle (DIP).

Author: Dev (GDScript Developer)
Date: June 15, 2025
Story: DM-009 - SOLID Principle Refactoring
Epic: EPIC-003 - Data Migration & Conversion Tools
"""

from pathlib import Path
from typing import Any, Callable, Dict, Optional, Type


class DIContainer:
    """
    Simple dependency injection container.

    Provides basic dependency injection capabilities to decouple
    components and enable better testability.
    """

    def __init__(self):
        """Initialize the DI container."""
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._singletons: Dict[str, Any] = {}

    def register_service(self, name: str, service: Any) -> None:
        """Register a service instance."""
        self._services[name] = service

    def register_factory(self, name: str, factory: Callable) -> None:
        """Register a service factory."""
        self._factories[name] = factory

    def register_singleton(self, name: str, singleton: Any) -> None:
        """Register a singleton instance."""
        self._singletons[name] = singleton

    def get_service(self, name: str) -> Any:
        """Get a service by name."""
        if name in self._services:
            return self._services[name]
        elif name in self._factories:
            return self._factories[name]()
        elif name in self._singletons:
            return self._singletons[name]
        else:
            raise KeyError(f"Service '{name}' not found in container")

    def has_service(self, name: str) -> bool:
        """Check if a service exists in the container."""
        return (
            name in self._services
            or name in self._factories
            or name in self._singletons
        )


# Global container instance for simplicity
_container = DIContainer()


def get_container() -> DIContainer:
    """Get the global DI container instance."""
    return _container


def register_converter_services(wcs_source_dir: Path, godot_target_dir: Path) -> None:
    """
    Register all converter services in the DI container.

    This function sets up the dependency injection for all converters,
    enabling loose coupling and better testability.
    """
    container = get_container()

    # Register core services
    from .conversion.job_manager import JobManager
    from .conversion.progress_tracker import ProgressTracker
    from .catalog.asset_catalog import AssetCatalog

    container.register_singleton("job_manager", JobManager())
    container.register_singleton("progress_tracker", ProgressTracker())
    container.register_factory(
        "asset_catalog", lambda: AssetCatalog(godot_target_dir / "asset_catalog.db")
    )

    # Register converter factories
    from ..table_converters.refactored_ship_converter import RefactoredShipConverter
    from ..table_converters.weapon_converter import WeaponTableConverter
    from ..table_converters.armor_converter import ArmorTableConverter

    # Use factories to create converters with proper dependencies
    container.register_factory(
        "ship_converter",
        lambda: RefactoredShipConverter(wcs_source_dir, godot_target_dir),
    )
    container.register_factory(
        "weapon_converter",
        lambda: WeaponTableConverter(wcs_source_dir, godot_target_dir),
    )
    container.register_factory(
        "armor_converter", lambda: ArmorTableConverter(wcs_source_dir, godot_target_dir)
    )

    # Register strategy factories
    from ..table_converters.strategies.ship_strategy import ShipTableStrategy
    from ..table_converters.strategies.base_strategy import BaseTableStrategy

    container.register_factory(
        "ship_strategy", lambda: ShipTableStrategy(wcs_source_dir, godot_target_dir)
    )


def inject_dependencies(obj: Any) -> None:
    """
    Inject dependencies into an object based on type annotations.

    This is a simple dependency injection mechanism that looks for
    type annotations and injects appropriate services.
    """
    container = get_container()

    # Get all attributes with type annotations
    annotations = getattr(obj, "__annotations__", {})

    for attr_name, attr_type in annotations.items():
        # Simple heuristic: if the type name suggests it's a service
        type_name = attr_type.__name__.lower()

        if "converter" in type_name or "manager" in type_name or "tracker" in type_name:
            service_name = type_name
            if container.has_service(service_name):
                setattr(obj, attr_name, container.get_service(service_name))
