"""
Sequential Workflow Implementation

This module implements the sequential workflow process for atomic tasks
in the Wing Commander Saga to Godot migration.
"""

import json
import time
import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Enumeration of task statuses."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Task:
    """Represents a single task in the workflow."""
    id: str
    name: str
    description: str
    agent: str
    expected_output: str
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    dependencies: List[str] = field(default_factory=list)
    
    def duration(self) -> Optional[float]:
        """Calculate task duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


class SequentialWorkflow:
    """Sequential workflow processor for atomic tasks."""
    
    def __init__(self, name: str = "Sequential Workflow"):
        """
        Initialize the sequential workflow.
        
        Args:
            name: Name of the workflow
        """
        self.name = name
        self.tasks: List[Task] = []
        self.current_task_index = 0
        self.status = TaskStatus.PENDING
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.results: List[Dict[str, Any]] = []
        
    def add_task(self, task: Task) -> None:
        """
        Add a task to the workflow.
        
        Args:
            task: Task to add
        """
        self.tasks.append(task)
        logger.info(f"Added task '{task.name}' to workflow '{self.name}'")
    
    def add_tasks(self, tasks: List[Task]) -> None:
        """
        Add multiple tasks to the workflow.
        
        Args:
            tasks: List of tasks to add
        """
        for task in tasks:
            self.add_task(task)
    
    def can_execute_task(self, task: Task) -> bool:
        """
        Check if a task can be executed (all dependencies completed).
        
        Args:
            task: Task to check
            
        Returns:
            True if task can be executed, False otherwise
        """
        # If no dependencies, task can be executed
        if not task.dependencies:
            return True
        
        # Check if all dependencies are completed
        completed_task_ids = {
            t.id for t in self.tasks 
            if t.status == TaskStatus.COMPLETED
        }
        
        return all(dep_id in completed_task_ids for dep_id in task.dependencies)
    
    def execute_task(self, task: Task, task_executor: Callable[[Task], Dict[str, Any]]) -> bool:
        """
        Execute a single task.
        
        Args:
            task: Task to execute
            task_executor: Function that executes the task and returns results
            
        Returns:
            True if task completed successfully, False otherwise
        """
        # Check if task can be executed
        if not self.can_execute_task(task):
            logger.warning(f"Cannot execute task '{task.name}' due to unmet dependencies")
            return False
        
        # Update task status
        task.status = TaskStatus.IN_PROGRESS
        task.start_time = time.time()
        logger.info(f"Executing task '{task.name}' (ID: {task.id})")
        
        try:
            # Execute the task
            result = task_executor(task)
            
            # Update task with results
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.end_time = time.time()
            
            # Store result
            self.results.append({
                "task_id": task.id,
                "task_name": task.name,
                "result": result,
                "duration": task.duration()
            })
            
            logger.info(f"Task '{task.name}' completed successfully in {task.duration():.2f} seconds")
            return True
            
        except Exception as e:
            # Handle task failure
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.end_time = time.time()
            
            logger.error(f"Task '{task.name}' failed: {str(e)}")
            return False
    
    def execute_next_task(self, task_executor: Callable[[Task], Dict[str, Any]]) -> Optional[Task]:
        """
        Execute the next pending task in the workflow.
        
        Args:
            task_executor: Function that executes the task and returns results
            
        Returns:
            The executed task, or None if no task could be executed
        """
        # Find the next pending task that can be executed
        for task in self.tasks:
            if task.status == TaskStatus.PENDING and self.can_execute_task(task):
                success = self.execute_task(task, task_executor)
                return task if success else None
        
        # No tasks could be executed
        return None
    
    def execute_all(self, task_executor: Callable[[Task], Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute all tasks in the workflow sequentially.
        
        Args:
            task_executor: Function that executes tasks and returns results
            
        Returns:
            Dictionary with workflow execution results
        """
        logger.info(f"Starting execution of workflow '{self.name}' with {len(self.tasks)} tasks")
        
        # Update workflow status
        self.status = TaskStatus.IN_PROGRESS
        self.start_time = time.time()
        
        # Execute tasks until completion or failure
        completed_tasks = 0
        failed_tasks = 0
        
        while completed_tasks + failed_tasks < len(self.tasks):
            task = self.execute_next_task(task_executor)
            
            if task is None:
                # No task could be executed, check for stuck tasks
                pending_tasks = [t for t in self.tasks if t.status == TaskStatus.PENDING]
                if pending_tasks:
                    logger.error(f"Workflow stuck: {len(pending_tasks)} tasks cannot be executed due to unmet dependencies")
                    break
                else:
                    break
            
            if task.status == TaskStatus.COMPLETED:
                completed_tasks += 1
            elif task.status == TaskStatus.FAILED:
                failed_tasks += 1
        
        # Update workflow status
        self.end_time = time.time()
        if failed_tasks == 0:
            self.status = TaskStatus.COMPLETED
            logger.info(f"Workflow '{self.name}' completed successfully in {self.duration():.2f} seconds")
        else:
            self.status = TaskStatus.FAILED
            logger.error(f"Workflow '{self.name}' failed with {failed_tasks} failed tasks")
        
        return {
            "workflow_name": self.name,
            "status": self.status.value,
            "total_tasks": len(self.tasks),
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "skipped_tasks": len(self.tasks) - completed_tasks - failed_tasks,
            "duration": self.duration(),
            "results": self.results
        }
    
    def duration(self) -> Optional[float]:
        """Calculate workflow duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Get a task by its ID.
        
        Args:
            task_id: ID of the task to retrieve
            
        Returns:
            Task with the specified ID, or None if not found
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks."""
        return [task for task in self.tasks if task.status == TaskStatus.PENDING]
    
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks."""
        return [task for task in self.tasks if task.status == TaskStatus.COMPLETED]
    
    def get_failed_tasks(self) -> List[Task]:
        """Get all failed tasks."""
        return [task for task in self.tasks if task.status == TaskStatus.FAILED]
    
    def reset(self) -> None:
        """Reset the workflow to its initial state."""
        self.current_task_index = 0
        self.status = TaskStatus.PENDING
        self.start_time = None
        self.end_time = None
        self.results = []
        
        for task in self.tasks:
            task.status = TaskStatus.PENDING
            task.result = None
            task.error = None
            task.start_time = None
            task.end_time = None
        
        logger.info(f"Workflow '{self.name}' has been reset")


def example_task_executor(task: Task) -> Dict[str, Any]:
    """
    Example task executor function for testing.
    
    Args:
        task: Task to execute
        
    Returns:
        Dictionary with task execution results
    """
    # Simulate task execution time
    import time
    import random
    time.sleep(random.uniform(0.1, 0.5))
    
    # Simulate random failures for testing
    if random.random() < 0.1:  # 10% failure rate
        raise Exception(f"Simulated failure for task '{task.name}'")
    
    return {
        "status": "success",
        "message": f"Task '{task.name}' executed successfully",
        "task_id": task.id
    }


def main():
    """Main function for testing the SequentialWorkflow."""
    # Create a workflow
    workflow = SequentialWorkflow("Test Sequential Workflow")
    
    # Create some test tasks
    tasks = [
        Task(
            id="task_1",
            name="Analyze Source Code",
            description="Analyze the C++ source code structure",
            agent="CodebaseAnalyst",
            expected_output="Codebase analysis report"
        ),
        Task(
            id="task_2",
            name="Generate Migration Plan",
            description="Create a detailed migration plan",
            agent="MigrationArchitect",
            expected_output="Migration plan document",
            dependencies=["task_1"]
        ),
        Task(
            id="task_3",
            name="Refactor Player Class",
            description="Refactor the player class from C++ to GDScript",
            agent="RefactoringSpecialist",
            expected_output="Refactored GDScript player class",
            dependencies=["task_2"]
        )
    ]
    
    # Add tasks to workflow
    workflow.add_tasks(tasks)
    
    # Execute the workflow
    results = workflow.execute_all(example_task_executor)
    
    # Print results
    print("Workflow Execution Results:")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
