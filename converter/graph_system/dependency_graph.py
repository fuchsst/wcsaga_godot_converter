"""
Dependency Graph Implementation

This module implements a dependency graph system for tracking codebase relationships
in the Wing Commander Saga to Godot migration.
"""

import json
import time
import logging
from typing import Dict, Any, List, Optional, Set
from pathlib import Path
import networkx as nx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DependencyGraph:
    """Dependency graph for tracking codebase relationships."""
    
    def __init__(self, graph_file: Optional[str] = None):
        """
        Initialize the dependency graph.
        
        Args:
            graph_file: Optional path to load/save the graph
        """
        self.graph = nx.DiGraph()
        self.graph_file = graph_file
        self.last_updated = time.time()
        
        # Load graph from file if provided
        if self.graph_file and Path(self.graph_file).exists():
            self.load_graph()
        
        logger.info("Dependency Graph initialized")
    
    def add_entity(self, entity_id: str, entity_type: str, 
                   properties: Optional[Dict[str, Any]] = None) -> None:
        """
        Add an entity to the graph.
        
        Args:
            entity_id: Unique identifier for the entity
            entity_type: Type of the entity (e.g., 'ship', 'weapon', 'module')
            properties: Optional properties of the entity
        """
        if properties is None:
            properties = {}
            
        properties.update({
            "type": entity_type,
            "created_at": time.time(),
            "last_modified": time.time()
        })
        
        self.graph.add_node(entity_id, **properties)
        self._mark_updated()
        
        logger.debug(f"Added entity {entity_id} of type {entity_type}")
    
    def add_dependency(self, from_entity: str, to_entity: str, 
                      dependency_type: str = "depends_on") -> None:
        """
        Add a dependency relationship between two entities.
        
        Args:
            from_entity: ID of the dependent entity
            to_entity: ID of the dependency
            dependency_type: Type of dependency (e.g., 'depends_on', 'inherits_from')
        """
        # Ensure both entities exist
        if not self.graph.has_node(from_entity):
            self.add_entity(from_entity, "unknown")
        
        if not self.graph.has_node(to_entity):
            self.add_entity(to_entity, "unknown")
        
        # Add the dependency edge
        self.graph.add_edge(from_entity, to_entity, type=dependency_type)
        self._mark_updated()
        
        logger.debug(f"Added dependency: {from_entity} -> {to_entity} ({dependency_type})")
    
    def get_dependencies(self, entity_id: str) -> List[Dict[str, Any]]:
        """
        Get all dependencies of an entity.
        
        Args:
            entity_id: ID of the entity
            
        Returns:
            List of dependencies
        """
        if not self.graph.has_node(entity_id):
            return []
        
        dependencies = []
        for successor in self.graph.successors(entity_id):
            edge_data = self.graph.get_edge_data(entity_id, successor)
            dependencies.append({
                "dependent": entity_id,
                "dependency": successor,
                "type": edge_data.get("type", "depends_on")
            })
        
        return dependencies
    
    def get_dependents(self, entity_id: str) -> List[Dict[str, Any]]:
        """
        Get all entities that depend on this entity.
        
        Args:
            entity_id: ID of the entity
            
        Returns:
            List of dependents
        """
        if not self.graph.has_node(entity_id):
            return []
        
        dependents = []
        for predecessor in self.graph.predecessors(entity_id):
            edge_data = self.graph.get_edge_data(predecessor, entity_id)
            dependents.append({
                "dependent": predecessor,
                "dependency": entity_id,
                "type": edge_data.get("type", "depends_on")
            })
        
        return dependents
    
    def get_entity_properties(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """
        Get properties of an entity.
        
        Args:
            entity_id: ID of the entity
            
        Returns:
            Entity properties, or None if entity not found
        """
        if not self.graph.has_node(entity_id):
            return None
        
        return dict(self.graph.nodes[entity_id])
    
    def update_entity_properties(self, entity_id: str, 
                                properties: Dict[str, Any]) -> bool:
        """
        Update properties of an entity.
        
        Args:
            entity_id: ID of the entity
            properties: Properties to update
            
        Returns:
            True if successful, False otherwise
        """
        if not self.graph.has_node(entity_id):
            return False
        
        # Update the properties
        for key, value in properties.items():
            self.graph.nodes[entity_id][key] = value
        
        self.graph.nodes[entity_id]["last_modified"] = time.time()
        self._mark_updated()
        
        logger.debug(f"Updated properties for entity {entity_id}")
        return True
    
    def get_topological_order(self) -> List[str]:
        """
        Get entities in topological order (suitable for migration sequence).
        
        Returns:
            List of entity IDs in topological order
        """
        try:
            # Get topological sort
            topo_order = list(nx.topological_sort(self.graph))
            return topo_order
        except nx.NetworkXError as e:
            logger.warning(f"Graph has cycles, cannot perform topological sort: {str(e)}")
            # Return nodes in a simple order as fallback
            return list(self.graph.nodes())
    
    def find_cycles(self) -> List[List[str]]:
        """
        Find cycles in the dependency graph.
        
        Returns:
            List of cycles (each cycle is a list of entity IDs)
        """
        try:
            cycles = list(nx.simple_cycles(self.graph))
            return cycles
        except Exception as e:
            logger.error(f"Error finding cycles: {str(e)}")
            return []
    
    def get_subgraph(self, entity_ids: List[str]) -> 'DependencyGraph':
        """
        Get a subgraph containing only the specified entities and their relationships.
        
        Args:
            entity_ids: List of entity IDs to include
            
        Returns:
            New DependencyGraph instance with the subgraph
        """
        subgraph = self.graph.subgraph(entity_ids).copy()
        new_graph = DependencyGraph()
        new_graph.graph = subgraph
        return new_graph
    
    def save_graph(self, file_path: Optional[str] = None) -> bool:
        """
        Save the graph to a file.
        
        Args:
            file_path: Path to save the graph (uses self.graph_file if None)
            
        Returns:
            True if successful, False otherwise
        """
        if file_path is None:
            file_path = self.graph_file
        
        if file_path is None:
            logger.warning("No file path specified for saving graph")
            return False
        
        try:
            # Convert graph to JSON-serializable format
            graph_data = {
                "nodes": [],
                "edges": [],
                "metadata": {
                    "last_updated": self.last_updated,
                    "node_count": self.graph.number_of_nodes(),
                    "edge_count": self.graph.number_of_edges()
                }
            }
            
            # Add nodes
            for node_id, node_data in self.graph.nodes(data=True):
                graph_data["nodes"].append({
                    "id": node_id,
                    "properties": node_data
                })
            
            # Add edges
            for from_node, to_node, edge_data in self.graph.edges(data=True):
                graph_data["edges"].append({
                    "from": from_node,
                    "to": to_node,
                    "properties": edge_data
                })
            
            # Save to file
            with open(file_path, 'w') as f:
                json.dump(graph_data, f, indent=2)
            
            logger.info(f"Graph saved to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save graph: {str(e)}")
            return False
    
    def load_graph(self, file_path: Optional[str] = None) -> bool:
        """
        Load the graph from a file.
        
        Args:
            file_path: Path to load the graph from (uses self.graph_file if None)
            
        Returns:
            True if successful, False otherwise
        """
        if file_path is None:
            file_path = self.graph_file
        
        if file_path is None or not Path(file_path).exists():
            logger.warning("No graph file to load")
            return False
        
        try:
            # Load from file
            with open(file_path, 'r') as f:
                graph_data = json.load(f)
            
            # Clear current graph
            self.graph.clear()
            
            # Add nodes
            for node_info in graph_data.get("nodes", []):
                node_id = node_info["id"]
                properties = node_info.get("properties", {})
                self.graph.add_node(node_id, **properties)
            
            # Add edges
            for edge_info in graph_data.get("edges", []):
                from_node = edge_info["from"]
                to_node = edge_info["to"]
                properties = edge_info.get("properties", {})
                self.graph.add_edge(from_node, to_node, **properties)
            
            # Update metadata
            self.last_updated = graph_data.get("metadata", {}).get("last_updated", time.time())
            
            logger.info(f"Graph loaded from {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load graph: {str(e)}")
            return False
    
    def _mark_updated(self) -> None:
        """Mark the graph as updated."""
        self.last_updated = time.time()
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the graph.
        
        Returns:
            Dictionary with graph statistics
        """
        return {
            "node_count": self.graph.number_of_nodes(),
            "edge_count": self.graph.number_of_edges(),
            "isolated_nodes": len(list(nx.isolates(self.graph))),
            "strongly_connected_components": nx.number_strongly_connected_components(self.graph),
            "last_updated": self.last_updated
        }


def main():
    """Main function for testing the DependencyGraph."""
    # Create dependency graph
    graph = DependencyGraph("test_dependency_graph.json")
    
    # Add some test entities
    graph.add_entity("SHIP-GTC_FENRIS", "ship", {
        "name": "GTC Fenris",
        "type": "cruiser",
        "file_path": "source/tables/ships.tbl"
    })
    
    graph.add_entity("SHIP-GTF_MYRMIDON", "ship", {
        "name": "GTF Myrmidon",
        "type": "fighter",
        "file_path": "source/tables/ships.tbl"
    })
    
    graph.add_entity("MODULE-ENGINE", "module", {
        "name": "Engine Module",
        "type": "propulsion"
    })
    
    # Add dependencies
    graph.add_dependency("SHIP-GTC_FENRIS", "MODULE-ENGINE", "uses")
    graph.add_dependency("SHIP-GTF_MYRMIDON", "MODULE-ENGINE", "uses")
    
    # Print graph statistics
    print("Graph statistics:", graph.get_statistics())
    
    # Get dependencies
    print("Dependencies of SHIP-GTC_FENRIS:", graph.get_dependencies("SHIP-GTC_FENRIS"))
    print("Dependents of MODULE-ENGINE:", graph.get_dependents("MODULE-ENGINE"))
    
    # Get topological order
    print("Topological order:", graph.get_topological_order())
    
    # Save graph
    graph.save_graph()


if __name__ == "__main__":
    main()