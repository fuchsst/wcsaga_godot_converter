"""
Task Decomposition Agent for the Centurion migration system.

This agent is responsible for analyzing the dependency graph and creating
a proper task execution order based on dependencies.
"""

import json
import logging
import networkx as nx
from pathlib import Path
from typing import Any, Dict, List, Optional

from converter.agents.base_agent import SpecialistAgent
from converter.graph_system.dependency_graph import DependencyGraph
from converter.graph_system.graph_state import CenturionGraphState, Task

logger = logging.getLogger(__name__)


class TaskDecompositionAgent(SpecialistAgent):
    """Specialist agent responsible for decomposing the migration into atomic tasks."""

    def __init__(self, graph_file: str = "dependency_graph.json"):
        """Initialize the TaskDecompositionAgent."""
        super().__init__("TaskDecompositionAgent")
        self.dependency_graph = DependencyGraph(graph_file)

    async def execute(self, state: CenturionGraphState) -> CenturionGraphState:
        """
        Execute the task decomposition based on dependency graph analysis.

        Args:
            state: Current graph state

        Returns:
            Updated graph state with decomposed tasks
        """
        self._log_execution_start("task_decomposition")
        state.current_step = "task_decomposition"

        try:
            # Analyze the dependency graph to create task execution order
            task_queue = self._create_task_queue_from_dependencies()
            
            # Update the state with the properly ordered task queue
            state.task_queue = task_queue
            state.dependency_analysis = self._analyze_dependencies()

            logger.info(f"Created task queue with {len(task_queue)} tasks in dependency order")

        except Exception as e:
            logger.error(f"Task decomposition failed: {str(e)}")
            if not state.error_logs:
                state.error_logs = []
            state.error_logs.append({
                "step": "task_decomposition",
                "error": str(e),
                "entity": "dependency_graph"
            })

        self._log_execution_end("task_decomposition")
        return state

    def _create_task_queue_from_dependencies(self) -> List[Task]:
        """
        Create a task queue based on dependency graph topological order.

        Returns:
            List of tasks in proper execution order
        """
        # Get topological order from dependency graph
        try:
            execution_order = self.dependency_graph.get_topological_order()
        except Exception as e:
            logger.warning(f"Failed to get topological order: {str(e)}")
            # Fallback to node order if topological sort fails
            execution_order = list(self.dependency_graph.graph.nodes())

        task_queue = []
        
        for entity_id in execution_order:
            # Get entity properties from dependency graph
            entity_props = self.dependency_graph.get_entity_properties(entity_id)
            if not entity_props:
                continue

            # Create task based on entity type and properties
            task = self._create_task_from_entity(entity_id, entity_props)
            task_queue.append(task)

        return task_queue

    def _create_task_from_entity(self, entity_id: str, entity_props: Dict[str, Any]) -> Task:
        """
        Create a task from an entity in the dependency graph.

        Args:
            entity_id: ID of the entity
            entity_props: Properties of the entity

        Returns:
            Task object for the entity
        """
        entity_type = entity_props.get("type", "unknown")
        entity_name = entity_props.get("name", entity_id)
        
        # Determine source files based on entity type
        source_files = self._determine_source_files(entity_id, entity_props)
        
        # Determine if human approval is needed based on complexity
        requires_human_approval = self._requires_human_approval(entity_props)
        
        # Determine max retries based on complexity
        max_retries = self._determine_max_retries(entity_props)
        
        # Get dependencies for this entity
        dependencies = self._get_entity_dependencies(entity_id)

        return Task(
            task_id=entity_id,
            entity_name=entity_name,
            entity_type=entity_type,
            source_files=source_files,
            status="pending",
            requires_human_approval=requires_human_approval,
            max_retries=max_retries,
            dependencies=dependencies,
            properties=entity_props
        )

    def _determine_source_files(self, entity_id: str, entity_props: Dict[str, Any]) -> List[str]:
        """Determine source files for an entity based on its type and properties."""
        entity_type = entity_props.get("type", "")
        source_files = []

        # Map entity types to likely source file locations
        type_to_files = {
            "ship": ["source/tables/ships.tbl", "source/models/*.pof"],
            "weapon": ["source/tables/weapons.tbl", "source/models/*.pof"],
            "module": ["source/tables/modules.tbl"],
            "mission": ["source/missions/*.fs2", "source/scripts/*.lua"],
            "ai": ["source/ai/*.cpp", "source/ai/*.h"],
            "ui": ["source/ui/*.cpp", "source/ui/*.h"],
            "physics": ["source/physics/*.cpp", "source/physics/*.h"],
        }

        # Add type-specific files
        if entity_type in type_to_files:
            source_files.extend(type_to_files[entity_type])

        # Add any explicitly specified files
        if "file_path" in entity_props:
            source_files.append(entity_props["file_path"])
        if "source_files" in entity_props:
            if isinstance(entity_props["source_files"], list):
                source_files.extend(entity_props["source_files"])
            else:
                source_files.append(entity_props["source_files"])

        # Add common C++ source files for code entities
        if entity_type in ["ai", "ui", "physics", "module"]:
            source_files.extend([
                f"source/code/{entity_id.lower()}.cpp",
                f"source/code/{entity_id.lower()}.h"
            ])

        return list(set(source_files))  # Remove duplicates

    def _requires_human_approval(self, entity_props: Dict[str, Any]) -> bool:
        """Determine if this entity requires human approval based on complexity."""
        complexity = entity_props.get("complexity", 0)
        criticality = entity_props.get("criticality", 0)
        
        # Require approval for complex or critical entities
        return complexity >= 8 or criticality >= 9 or entity_props.get("type") == "core"

    def _determine_max_retries(self, entity_props: Dict[str, Any]) -> int:
        """Determine maximum retries based on entity complexity."""
        complexity = entity_props.get("complexity", 5)
        
        # More complex entities get fewer retries (they're harder to debug)
        if complexity >= 9:
            return 2
        elif complexity >= 7:
            return 3
        else:
            return 5

    def _get_entity_dependencies(self, entity_id: str) -> List[str]:
        """Get all dependencies for an entity as task IDs."""
        dependencies = []
        for dep in self.dependency_graph.get_dependencies(entity_id):
            dependencies.append(dep["dependency"])
        return dependencies

    def _analyze_dependencies(self) -> Dict[str, Any]:
        """Perform comprehensive dependency analysis."""
        stats = self.dependency_graph.get_statistics()
        
        # Find cycles (circular dependencies)
        cycles = self.dependency_graph.find_cycles()
        
        # Analyze dependency depth
        dependency_depth = self._calculate_dependency_depth()
        
        # Identify critical paths
        critical_paths = self._identify_critical_paths()

        return {
            "statistics": stats,
            "cycles": cycles,
            "dependency_depth": dependency_depth,
            "critical_paths": critical_paths,
            "has_circular_dependencies": len(cycles) > 0
        }

    def _calculate_dependency_depth(self) -> Dict[str, Any]:
        """Calculate maximum dependency depth for the graph."""
        try:
            # Find the longest path in the DAG
            if self.dependency_graph.graph.number_of_nodes() == 0:
                return {"max_depth": 0, "average_depth": 0.0}

            # Calculate depth for each node
            depths = {}
            for node in self.dependency_graph.graph.nodes():
                if self.dependency_graph.graph.in_degree(node) == 0:
                    # Root node
                    depths[node] = 0
                else:
                    # Maximum depth of predecessors + 1
                    pred_depths = [depths[pred] for pred in self.dependency_graph.graph.predecessors(node) 
                                  if pred in depths]
                    depths[node] = max(pred_depths) + 1 if pred_depths else 0

            max_depth = max(depths.values()) if depths else 0
            avg_depth = sum(depths.values()) / len(depths) if depths else 0

            return {
                "max_depth": max_depth,
                "average_depth": round(avg_depth, 2),
                "node_depths": depths
            }

        except Exception as e:
            logger.warning(f"Failed to calculate dependency depth: {str(e)}")
            return {"max_depth": 0, "average_depth": 0.0, "error": str(e)}

    def _identify_critical_paths(self) -> List[List[str]]:
        """Identify critical paths in the dependency graph."""
        try:
            # Find all paths from root nodes to leaf nodes
            root_nodes = [node for node in self.dependency_graph.graph.nodes() 
                         if self.dependency_graph.graph.in_degree(node) == 0]
            leaf_nodes = [node for node in self.dependency_graph.graph.nodes() 
                         if self.dependency_graph.graph.out_degree(node) == 0]

            critical_paths = []
            for root in root_nodes:
                for leaf in leaf_nodes:
                    if nx.has_path(self.dependency_graph.graph, root, leaf):
                        paths = list(nx.all_simple_paths(self.dependency_graph.graph, root, leaf))
                        # Take the longest path as critical
                        if paths:
                            critical_path = max(paths, key=len)
                            critical_paths.append(critical_path)

            return critical_paths

        except Exception as e:
            logger.warning(f"Failed to identify critical paths: {str(e)}")
            return []

    def validate_task_order(self, task_queue: List[Task]) -> Dict[str, Any]:
        """
        Validate that the task execution order respects dependencies.

        Args:
            task_queue: List of tasks to validate

        Returns:
            Validation results
        """
        validation_results = {
            "valid": True,
            "violations": [],
            "suggestions": []
        }

        # Create mapping of task_id to execution index
        task_indices = {task.task_id: idx for idx, task in enumerate(task_queue)}

        # Check each task's dependencies
        for task in task_queue:
            for dep_id in task.dependencies:
                if dep_id in task_indices:
                    if task_indices[dep_id] > task_indices[task.task_id]:
                        validation_results["valid"] = False
                        validation_results["violations"].append({
                            "task": task.task_id,
                            "dependency": dep_id,
                            "task_index": task_indices[task.task_id],
                            "dep_index": task_indices[dep_id],
                            "message": f"Task {task.task_id} executes before its dependency {dep_id}"
                        })

        # Suggest improvements if violations found
        if not validation_results["valid"]:
            validation_results["suggestions"].append(
                "Re-order tasks using topological sort from dependency graph"
            )

        return validation_results


def main():
    """Main function for testing the TaskDecompositionAgent."""
    # Create agent and test with sample dependency graph
    agent = TaskDecompositionAgent("test_dependency_graph.json")
    
    # Create a mock state for testing
    class MockState:
        def __init__(self):
            self.current_step = ""
            self.task_queue = []
            self.error_logs = []
            self.dependency_analysis = {}

    state = MockState()
    
    # Test task decomposition
    result_state = agent.execute(state)
    
    print("Task decomposition completed:")
    print(f"Tasks in queue: {len(result_state.task_queue)}")
    print(f"Dependency analysis: {json.dumps(result_state.dependency_analysis, indent=2)}")
    
    # Validate task order
    validation = agent.validate_task_order(result_state.task_queue)
    print(f"Task order validation: {validation['valid']}")
    if not validation['valid']:
        print("Violations:", json.dumps(validation['violations'], indent=2))


if __name__ == "__main__":
    main()
