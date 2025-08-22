"""
Task Queue Manager

This module manages the persistent task queue for the migration process.
"""

import yaml
import json
import time
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
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
    ESCALATED = "escalated"


class TaskQueueManager:
    """Manager for the persistent task queue."""
    
    def __init__(self, queue_file: str = "task_queue.yaml"):
        """
        Initialize the task queue manager.
        
        Args:
            queue_file: Path to the task queue file
        """
        self.queue_file = Path(queue_file)
        self.tasks = {}
        self._load_queue()
        
        logger.info(f"Task Queue Manager initialized with {len(self.tasks)} tasks")
    
    def _load_queue(self) -> None:
        """Load the task queue from file."""
        if self.queue_file.exists():
            try:
                with open(self.queue_file, 'r') as f:
                    self.tasks = yaml.safe_load(f) or {}
                logger.info(f"Loaded {len(self.tasks)} tasks from {self.queue_file}")
            except Exception as e:
                logger.error(f"Failed to load task queue: {str(e)}")
                self.tasks = {}
        else:
            logger.info("Task queue file not found, starting with empty queue")
            self.tasks = {}
    
    def _save_queue(self) -> None:
        """Save the task queue to file."""
        try:
            # Create directory if it doesn't exist
            self.queue_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.queue_file, 'w') as f:
                yaml.dump(self.tasks, f, default_flow_style=False)
            logger.debug(f"Saved task queue to {self.queue_file}")
        except Exception as e:
            logger.error(f"Failed to save task queue: {str(e)}")
    
    def add_task(self, task_id: str, task_data: Dict[str, Any]) -> None:
        """
        Add a new task to the queue.
        
        Args:
            task_id: Unique identifier for the task
            task_data: Data for the task
        """
        if task_id in self.tasks:
            logger.warning(f"Task {task_id} already exists, updating...")
        
        # Ensure required fields are present
        task_entry = {
            "task_id": task_id,
            "description": task_data.get("description", ""),
            "source_files": task_data.get("source_files", []),
            "dependencies": task_data.get("dependencies", []),
            "status": task_data.get("status", TaskStatus.PENDING.value),
            "retry_count": task_data.get("retry_count", 0),
            "failure_logs": task_data.get("failure_logs", []),
            "created_at": task_data.get("created_at", time.time()),
            "updated_at": time.time()
        }
        
        self.tasks[task_id] = task_entry
        self._save_queue()
        
        logger.info(f"Added task {task_id} to queue")
    
    def update_task_status(self, task_id: str, status: TaskStatus, 
                          additional_data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Update the status of a task.
        
        Args:
            task_id: Unique identifier for the task
            status: New status for the task
            additional_data: Additional data to update
            
        Returns:
            True if update was successful, False otherwise
        """
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found in queue")
            return False
        
        self.tasks[task_id]["status"] = status.value
        self.tasks[task_id]["updated_at"] = time.time()
        
        if additional_data:
            # Update any additional fields
            for key, value in additional_data.items():
                if key in self.tasks[task_id]:
                    self.tasks[task_id][key] = value
                else:
                    # Add new field
                    self.tasks[task_id][key] = value
        
        self._save_queue()
        logger.info(f"Updated task {task_id} status to {status.value}")
        return True
    
    def get_next_pending_task(self) -> Optional[Dict[str, Any]]:
        """
        Get the next pending task that has all dependencies met.
        
        Returns:
            Task data for the next pending task, or None if no task is available
        """
        # Get all completed task IDs
        completed_tasks = {
            task_id for task_id, task in self.tasks.items()
            if task["status"] == TaskStatus.COMPLETED.value
        }
        
        # Find next pending task with all dependencies met
        for task_id, task in self.tasks.items():
            if task["status"] == TaskStatus.PENDING.value:
                # Check if all dependencies are completed
                dependencies_met = all(
                    dep_id in completed_tasks for dep_id in task.get("dependencies", [])
                )
                
                if dependencies_met:
                    return task
        
        return None
    
    def get_task_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a task by its ID.
        
        Args:
            task_id: Unique identifier for the task
            
        Returns:
            Task data, or None if not found
        """
        return self.tasks.get(task_id)
    
    def add_failure_log(self, task_id: str, error_message: str, 
                       error_details: Optional[Dict[str, Any]] = None) -> bool:
        """
        Add a failure log to a task.
        
        Args:
            task_id: Unique identifier for the task
            error_message: Error message
            error_details: Additional error details
            
        Returns:
            True if log was added, False otherwise
        """
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found in queue")
            return False
        
        failure_log = {
            "timestamp": time.time(),
            "error_message": error_message,
            "error_details": error_details or {}
        }
        
        self.tasks[task_id]["failure_logs"].append(failure_log)
        self.tasks[task_id]["updated_at"] = time.time()
        self._save_queue()
        
        logger.info(f"Added failure log to task {task_id}")
        return True
    
    def get_queue_summary(self) -> Dict[str, int]:
        """
        Get a summary of the task queue.
        
        Returns:
            Dictionary with counts of tasks by status
        """
        summary = {
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "failed": 0,
            "escalated": 0,
            "total": len(self.tasks)
        }
        
        for task in self.tasks.values():
            status = task.get("status", "unknown")
            if status in summary:
                summary[status] += 1
            else:
                summary["total"] += 1
        
        return summary


def main():
    """Main function for testing the TaskQueueManager."""
    # Create task queue manager
    queue_manager = TaskQueueManager("test_task_queue.yaml")
    
    # Add some test tasks
    queue_manager.add_task("SHIP-GTC_FENRIS", {
        "description": "Migrate the GTC Fenris cruiser",
        "source_files": ["source/tables/ships.tbl", "source/models/fenris.pof"],
        "dependencies": []
    })
    
    queue_manager.add_task("SHIP-GTF_MYRMIDON", {
        "description": "Migrate the GTF Myrmidon fighter",
        "source_files": ["source/tables/ships.tbl", "source/models/myrmidon.pof"],
        "dependencies": ["SHIP-GTC_FENRIS"]
    })
    
    # Print queue summary
    print("Queue summary:", queue_manager.get_queue_summary())
    
    # Get next pending task
    next_task = queue_manager.get_next_pending_task()
    print("Next task:", next_task)
    
    # Update task status
    if next_task:
        queue_manager.update_task_status(next_task["task_id"], TaskStatus.IN_PROGRESS)
        print("Updated queue summary:", queue_manager.get_queue_summary())


if __name__ == "__main__":
    main()