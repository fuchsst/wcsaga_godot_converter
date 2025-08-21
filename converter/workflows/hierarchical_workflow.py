"""
Hierarchical Workflow Implementation

This module implements the hierarchical workflow process for complex tasks
in the Wing Commander Saga to Godot migration.
"""

import json
import time
import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

# Import sequential workflow
from .sequential_workflow import SequentialWorkflow, Task, TaskStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkflowType(Enum):
    """Enumeration of workflow types."""
    SEQUENTIAL = "sequential"
    HIERARCHICAL = "hierarchical"


@dataclass
class SubWorkflow:
    """Represents a sub-workflow in a hierarchical workflow."""
    id: str
    name: str
    workflow: SequentialWorkflow
    status: TaskStatus = TaskStatus.PENDING
    manager_agent: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    
    def duration(self) -> Optional[float]:
        """Calculate sub-workflow duration in seconds."""
        return self.workflow.duration()


class HierarchicalWorkflow:
    """Hierarchical workflow processor for complex tasks."""
    
    def __init__(self, name: str = "Hierarchical Workflow", manager_agent: str = "MigrationArchitect"):
        """
        Initialize the hierarchical workflow.
        
        Args:
            name: Name of the workflow
            manager_agent: Agent responsible for managing this workflow
        """
        self.name = name
        self.manager_agent = manager_agent
        self.sub_workflows: List[SubWorkflow] = []
        self.status = TaskStatus.PENDING
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.results: List[Dict[str, Any]] = []
        
    def add_sub_workflow(self, sub_workflow: SubWorkflow) -> None:
        """
        Add a sub-workflow to the hierarchical workflow.
        
        Args:
            sub_workflow: Sub-workflow to add
        """
        self.sub_workflows.append(sub_workflow)
        logger.info(f"Added sub-workflow '{sub_workflow.name}' to hierarchical workflow '{self.name}'")
    
    def add_sub_workflows(self, sub_workflows: List[SubWorkflow]) -> None:
        """
        Add multiple sub-workflows to the hierarchical workflow.
        
        Args:
            sub_workflows: List of sub-workflows to add
        """
        for sub_workflow in sub_workflows:
            self.add_sub_workflow(sub_workflow)
    
    def can_execute_sub_workflow(self, sub_workflow: SubWorkflow) -> bool:
        """
        Check if a sub-workflow can be executed (all dependencies completed).
        
        Args:
            sub_workflow: Sub-workflow to check
            
        Returns:
            True if sub-workflow can be executed, False otherwise
        """
        # If no dependencies, sub-workflow can be executed
        if not sub_workflow.dependencies:
            return True
        
        # Check if all dependencies are completed
        completed_sub_workflow_ids = {
            sw.id for sw in self.sub_workflows 
            if sw.status == TaskStatus.COMPLETED
        }
        
        return all(dep_id in completed_sub_workflow_ids for dep_id in sub_workflow.dependencies)
    
    def execute_sub_workflow(self, sub_workflow: SubWorkflow, 
                           task_executor: Callable[[Task], Dict[str, Any]]) -> bool:
        """
        Execute a single sub-workflow.
        
        Args:
            sub_workflow: Sub-workflow to execute
            task_executor: Function that executes tasks and returns results
            
        Returns:
            True if sub-workflow completed successfully, False otherwise
        """
        # Check if sub-workflow can be executed
        if not self.can_execute_sub_workflow(sub_workflow):
            logger.warning(f"Cannot execute sub-workflow '{sub_workflow.name}' due to unmet dependencies")
            return False
        
        # Update sub-workflow status
        sub_workflow.status = TaskStatus.IN_PROGRESS
        logger.info(f"Executing sub-workflow '{sub_workflow.name}' (ID: {sub_workflow.id})")
        
        try:
            # Execute the sub-workflow
            result = sub_workflow.workflow.execute_all(task_executor)
            
            # Update sub-workflow with results
            sub_workflow.status = TaskStatus.COMPLETED
            
            # Store result
            self.results.append({
                "sub_workflow_id": sub_workflow.id,
                "sub_workflow_name": sub_workflow.name,
                "result": result,
                "duration": sub_workflow.duration()
            })
            
            logger.info(f"Sub-workflow '{sub_workflow.name}' completed successfully in {sub_workflow.duration():.2f} seconds")
            return True
            
        except Exception as e:
            # Handle sub-workflow failure
            sub_workflow.status = TaskStatus.FAILED
            
            logger.error(f"Sub-workflow '{sub_workflow.name}' failed: {str(e)}")
            return False
    
    def execute_next_sub_workflow(self, task_executor: Callable[[Task], Dict[str, Any]]) -> Optional[SubWorkflow]:
        """
        Execute the next pending sub-workflow in the workflow.
        
        Args:
            task_executor: Function that executes tasks and returns results
            
        Returns:
            The executed sub-workflow, or None if no sub-workflow could be executed
        """
        # Find the next pending sub-workflow that can be executed
        for sub_workflow in self.sub_workflows:
            if sub_workflow.status == TaskStatus.PENDING and self.can_execute_sub_workflow(sub_workflow):
                success = self.execute_sub_workflow(sub_workflow, task_executor)
                return sub_workflow if success else None
        
        # No sub-workflows could be executed
        return None
    
    def execute_all(self, task_executor: Callable[[Task], Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute all sub-workflows in the hierarchical workflow.
        
        Args:
            task_executor: Function that executes tasks and returns results
            
        Returns:
            Dictionary with workflow execution results
        """
        logger.info(f"Starting execution of hierarchical workflow '{self.name}' with {len(self.sub_workflows)} sub-workflows")
        
        # Update workflow status
        self.status = TaskStatus.IN_PROGRESS
        self.start_time = time.time()
        
        # Execute sub-workflows until completion or failure
        completed_sub_workflows = 0
        failed_sub_workflows = 0
        
        while completed_sub_workflows + failed_sub_workflows < len(self.sub_workflows):
            sub_workflow = self.execute_next_sub_workflow(task_executor)
            
            if sub_workflow is None:
                # No sub-workflow could be executed, check for stuck sub-workflows
                pending_sub_workflows = [sw for sw in self.sub_workflows if sw.status == TaskStatus.PENDING]
                if pending_sub_workflows:
                    logger.error(f"Hierarchical workflow stuck: {len(pending_sub_workflows)} sub-workflows cannot be executed due to unmet dependencies")
                    break
                else:
                    break
            
            if sub_workflow.status == TaskStatus.COMPLETED:
                completed_sub_workflows += 1
            elif sub_workflow.status == TaskStatus.FAILED:
                failed_sub_workflows += 1
        
        # Update workflow status
        self.end_time = time.time()
        if failed_sub_workflows == 0:
            self.status = TaskStatus.COMPLETED
            logger.info(f"Hierarchical workflow '{self.name}' completed successfully in {self.duration():.2f} seconds")
        else:
            self.status = TaskStatus.FAILED
            logger.error(f"Hierarchical workflow '{self.name}' failed with {failed_sub_workflows} failed sub-workflows")
        
        return {
            "workflow_name": self.name,
            "manager_agent": self.manager_agent,
            "status": self.status.value,
            "total_sub_workflows": len(self.sub_workflows),
            "completed_sub_workflows": completed_sub_workflows,
            "failed_sub_workflows": failed_sub_workflows,
            "skipped_sub_workflows": len(self.sub_workflows) - completed_sub_workflows - failed_sub_workflows,
            "duration": self.duration(),
            "results": self.results
        }
    
    def duration(self) -> Optional[float]:
        """Calculate workflow duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None
    
    def get_sub_workflow_by_id(self, sub_workflow_id: str) -> Optional[SubWorkflow]:
        """
        Get a sub-workflow by its ID.
        
        Args:
            sub_workflow_id: ID of the sub-workflow to retrieve
            
        Returns:
            SubWorkflow with the specified ID, or None if not found
        """
        for sub_workflow in self.sub_workflows:
            if sub_workflow.id == sub_workflow_id:
                return sub_workflow
        return None
    
    def get_pending_sub_workflows(self) -> List[SubWorkflow]:
        """Get all pending sub-workflows."""
        return [sw for sw in self.sub_workflows if sw.status == TaskStatus.PENDING]
    
    def get_completed_sub_workflows(self) -> List[SubWorkflow]:
        """Get all completed sub-workflows."""
        return [sw for sw in self.sub_workflows if sw.status == TaskStatus.COMPLETED]
    
    def get_failed_sub_workflows(self) -> List[SubWorkflow]:
        """Get all failed sub-workflows."""
        return [sw for sw in self.sub_workflows if sw.status == TaskStatus.FAILED]
    
    def reset(self) -> None:
        """Reset the workflow to its initial state."""
        self.status = TaskStatus.PENDING
        self.start_time = None
        self.end_time = None
        self.results = []
        
        for sub_workflow in self.sub_workflows:
            sub_workflow.status = TaskStatus.PENDING
            sub_workflow.workflow.reset()
        
        logger.info(f"Hierarchical workflow '{self.name}' has been reset")


def create_migration_phase_workflow(phase_name: str, phase_tasks: List[Task], 
                                  manager_agent: str = "MigrationArchitect") -> SubWorkflow:
    """
    Create a sub-workflow for a migration phase.
    
    Args:
        phase_name: Name of the migration phase
        phase_tasks: List of tasks for this phase
        manager_agent: Agent managing this phase
        
    Returns:
        SubWorkflow for the migration phase
    """
    # Create sequential workflow for the phase
    phase_workflow = SequentialWorkflow(f"Migration Phase: {phase_name}")
    phase_workflow.add_tasks(phase_tasks)
    
    # Create sub-workflow
    sub_workflow = SubWorkflow(
        id=f"phase_{phase_name.lower().replace(' ', '_')}",
        name=phase_name,
        workflow=phase_workflow,
        manager_agent=manager_agent
    )
    
    return sub_workflow


def main():
    """Main function for testing the HierarchicalWorkflow."""
    # Create a hierarchical workflow
    workflow = HierarchicalWorkflow("Wing Commander Saga Migration", "MigrationArchitect")
    
    # Create some test tasks for different phases
    analysis_tasks = [
        Task(
            id="analyze_codebase",
            name="Analyze Source Codebase",
            description="Analyze the complete C++ codebase structure",
            agent="CodebaseAnalyst",
            expected_output="Complete codebase analysis report"
        ),
        Task(
            id="identify_dependencies",
            name="Identify Dependencies",
            description="Map all dependencies between modules",
            agent="CodebaseAnalyst",
            expected_output="Dependency graph",
            dependencies=["analyze_codebase"]
        )
    ]
    
    planning_tasks = [
        Task(
            id="create_migration_plan",
            name="Create Migration Plan",
            description="Create detailed migration plan based on analysis",
            agent="MigrationArchitect",
            expected_output="Migration plan document"
        ),
        Task(
            id="prioritize_modules",
            name="Prioritize Modules",
            description="Prioritize modules for migration based on dependencies",
            agent="MigrationArchitect",
            expected_output="Module priority list",
            dependencies=["create_migration_plan"]
        )
    ]
    
    # Create sub-workflows for each phase
    analysis_sub_workflow = create_migration_phase_workflow(
        "Codebase Analysis", analysis_tasks, "CodebaseAnalyst"
    )
    
    planning_sub_workflow = create_migration_phase_workflow(
        "Migration Planning", planning_tasks, "MigrationArchitect"
    )
    planning_sub_workflow.dependencies = [analysis_sub_workflow.id]
    
    # Add sub-workflows to the hierarchical workflow
    workflow.add_sub_workflows([analysis_sub_workflow, planning_sub_workflow])
    
    # Execute the workflow (using example task executor)
    from .sequential_workflow import example_task_executor
    results = workflow.execute_all(example_task_executor)
    
    # Print results
    print("Hierarchical Workflow Execution Results:")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
