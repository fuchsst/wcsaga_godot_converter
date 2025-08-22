"""
Graph Manager Implementation

This module implements a graph manager that handles dynamic updates and concurrency control
for the dependency graph system.
"""

import logging
import time
from threading import Lock, RLock
from typing import Any, Dict, List, Optional

# Import our modules
from .dependency_graph import DependencyGraph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphManager:
    """Manager for the dependency graph with concurrency control."""

    def __init__(self, graph_file: Optional[str] = None, auto_save: bool = True):
        """
        Initialize the graph manager.

        Args:
            graph_file: Optional path to load/save the graph
            auto_save: Whether to automatically save changes
        """
        self.graph = DependencyGraph(graph_file)
        self.auto_save = auto_save
        self.graph_file = graph_file
        self.lock = RLock()  # Reentrant lock for thread safety
        self.transaction_lock = Lock()  # Lock for transactions
        self.transaction_active = False
        self.transaction_changes = []

        logger.info("Graph Manager initialized")

    def add_entity(
        self,
        entity_id: str,
        entity_type: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Add an entity to the graph (thread-safe).

        Args:
            entity_id: Unique identifier for the entity
            entity_type: Type of the entity
            properties: Optional properties of the entity
        """
        with self.lock:
            self.graph.add_entity(entity_id, entity_type, properties)
            if self.auto_save:
                self.graph.save_graph()

    def add_dependency(
        self, from_entity: str, to_entity: str, dependency_type: str = "depends_on"
    ) -> None:
        """
        Add a dependency relationship between two entities (thread-safe).

        Args:
            from_entity: ID of the dependent entity
            to_entity: ID of the dependency
            dependency_type: Type of dependency
        """
        with self.lock:
            self.graph.add_dependency(from_entity, to_entity, dependency_type)
            if self.auto_save:
                self.graph.save_graph()

    def update_entity_properties(
        self, entity_id: str, properties: Dict[str, Any]
    ) -> bool:
        """
        Update properties of an entity (thread-safe).

        Args:
            entity_id: ID of the entity
            properties: Properties to update

        Returns:
            True if successful, False otherwise
        """
        with self.lock:
            result = self.graph.update_entity_properties(entity_id, properties)
            if result and self.auto_save:
                self.graph.save_graph()
            return result

    def get_entity_properties(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """
        Get properties of an entity (thread-safe).

        Args:
            entity_id: ID of the entity

        Returns:
            Entity properties, or None if entity not found
        """
        with self.lock:
            return self.graph.get_entity_properties(entity_id)

    def get_dependencies(self, entity_id: str) -> List[Dict[str, Any]]:
        """
        Get all dependencies of an entity (thread-safe).

        Args:
            entity_id: ID of the entity

        Returns:
            List of dependencies
        """
        with self.lock:
            return self.graph.get_dependencies(entity_id)

    def get_dependents(self, entity_id: str) -> List[Dict[str, Any]]:
        """
        Get all entities that depend on this entity (thread-safe).

        Args:
            entity_id: ID of the entity

        Returns:
            List of dependents
        """
        with self.lock:
            return self.graph.get_dependents(entity_id)

    def get_topological_order(self) -> List[str]:
        """
        Get entities in topological order (thread-safe).

        Returns:
            List of entity IDs in topological order
        """
        with self.lock:
            return self.graph.get_topological_order()

    def begin_transaction(self) -> bool:
        """
        Begin a transaction for atomic updates.

        Returns:
            True if transaction started, False if already in transaction
        """
        if self.transaction_lock.acquire(blocking=False):
            with self.lock:
                if not self.transaction_active:
                    self.transaction_active = True
                    self.transaction_changes = []
                    logger.debug("Transaction started")
                    return True
                else:
                    self.transaction_lock.release()
                    logger.warning("Transaction already active")
                    return False
        else:
            logger.warning("Could not acquire transaction lock")
            return False

    def commit_transaction(self) -> bool:
        """
        Commit the current transaction.

        Returns:
            True if committed, False if no transaction active
        """
        with self.lock:
            if self.transaction_active:
                self.transaction_active = False
                self.transaction_changes = []
                if self.auto_save:
                    self.graph.save_graph()
                self.transaction_lock.release()
                logger.debug("Transaction committed")
                return True
            else:
                logger.warning("No transaction active to commit")
                return False

    def rollback_transaction(self) -> bool:
        """
        Rollback the current transaction.

        Returns:
            True if rolled back, False if no transaction active
        """
        with self.lock:
            if self.transaction_active:
                # Undo changes (simplified implementation)
                # In a real implementation, we would need to track and undo changes
                self.transaction_active = False
                self.transaction_changes = []
                self.transaction_lock.release()
                logger.debug("Transaction rolled back")
                return True
            else:
                logger.warning("No transaction active to rollback")
                return False

    def add_entity_in_transaction(
        self,
        entity_id: str,
        entity_type: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Add an entity to the graph within a transaction.

        Args:
            entity_id: Unique identifier for the entity
            entity_type: Type of the entity
            properties: Optional properties of the entity
        """
        if not self.transaction_active:
            raise RuntimeError("No transaction active")

        with self.lock:
            self.graph.add_entity(entity_id, entity_type, properties)
            self.transaction_changes.append(("add_entity", entity_id))

    def add_dependency_in_transaction(
        self, from_entity: str, to_entity: str, dependency_type: str = "depends_on"
    ) -> None:
        """
        Add a dependency relationship within a transaction.

        Args:
            from_entity: ID of the dependent entity
            to_entity: ID of the dependency
            dependency_type: Type of dependency
        """
        if not self.transaction_active:
            raise RuntimeError("No transaction active")

        with self.lock:
            self.graph.add_dependency(from_entity, to_entity, dependency_type)
            self.transaction_changes.append(("add_dependency", from_entity, to_entity))

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the graph (thread-safe).

        Returns:
            Dictionary with graph statistics
        """
        with self.lock:
            return self.graph.get_statistics()

    def save_graph(self, file_path: Optional[str] = None) -> bool:
        """
        Save the graph to a file (thread-safe).

        Args:
            file_path: Path to save the graph

        Returns:
            True if successful, False otherwise
        """
        with self.lock:
            return self.graph.save_graph(file_path)

    def load_graph(self, file_path: Optional[str] = None) -> bool:
        """
        Load the graph from a file (thread-safe).

        Args:
            file_path: Path to load the graph from

        Returns:
            True if successful, False otherwise
        """
        with self.lock:
            return self.graph.load_graph(file_path)


def main():
    """Main function for testing the GraphManager."""
    # Create graph manager
    manager = GraphManager("test_graph_manager.json", auto_save=True)

    # Add some test entities
    manager.add_entity(
        "SHIP-GTC_FENRIS", "ship", {"name": "GTC Fenris", "type": "cruiser"}
    )

    manager.add_entity(
        "SHIP-GTF_MYRMIDON", "ship", {"name": "GTF Myrmidon", "type": "fighter"}
    )

    # Add dependency
    manager.add_dependency("SHIP-GTF_MYRMIDON", "SHIP-GTC_FENRIS", "escort")

    # Print statistics
    print("Graph statistics:", manager.get_statistics())

    # Test transaction
    if manager.begin_transaction():
        manager.add_entity_in_transaction(
            "MODULE-SHIELD", "module", {"name": "Shield Module", "type": "defense"}
        )
        manager.add_dependency_in_transaction(
            "SHIP-GTC_FENRIS", "MODULE-SHIELD", "uses"
        )
        manager.commit_transaction()

    # Print updated statistics
    print("Updated graph statistics:", manager.get_statistics())


if __name__ == "__main__":
    main()
