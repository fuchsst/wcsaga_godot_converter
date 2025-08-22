"""
Bolt Executor

This module executes individual bolt cycles using the state machine orchestrator.
"""

import time
import logging
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path

# Import our modules
from .core import StateMachineOrchestrator, BoltAction, BoltState
from .task_queue import TaskQueueManager, TaskStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BoltExecutor:
    """Executor for individual bolt cycles."""
    
    def __init__(self, queue_file: str = "task_queue.yaml", max_retries: int = 3):
        """
        Initialize the bolt executor.
        
        Args:
            queue_file: Path to the task queue file
            max_retries: Maximum number of retries for a bolt before escalation
        """
        self.queue_manager = TaskQueueManager(queue_file)
        self.max_retries = max_retries
        self.orchestrator = None
        
        logger.info("Bolt Executor initialized")
    
    def execute_bolt_cycle(self, task_id: str) -> Dict[str, Any]:
        """
        Execute a complete bolt cycle for a task.
        
        Args:
            task_id: Unique identifier for the task
            
        Returns:
            Dictionary with execution results
        """
        # Get task from queue
        task = self.queue_manager.get_task_by_id(task_id)
        if not task:
            return {
                "success": False,
                "error": f"Task {task_id} not found in queue"
            }
        
        # Initialize orchestrator
        self.orchestrator = StateMachineOrchestrator(max_retries=self.max_retries)
        self.orchestrator.initialize_bolt(
            task_id=task_id,
            entity_name=task.get("description", "Unknown Entity"),
            source_files=task.get("source_files", [])
        )
        
        # Update task status to in progress
        self.queue_manager.update_task_status(task_id, TaskStatus.IN_PROGRESS)
        
        try:
            # Execute the bolt cycle
            result = self._execute_bolt_steps(task)
            
            # Update task status based on result
            if result["success"]:
                self.queue_manager.update_task_status(task_id, TaskStatus.COMPLETED)
            else:
                self.queue_manager.update_task_status(
                    task_id, 
                    TaskStatus.FAILED,
                    {"retry_count": self.orchestrator.context.retry_count}
                )
                self.queue_manager.add_failure_log(
                    task_id, 
                    result.get("error", "Unknown error"),
                    result.get("details", {})
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Exception during bolt execution for task {task_id}: {str(e)}")
            self.queue_manager.update_task_status(task_id, TaskStatus.FAILED)
            self.queue_manager.add_failure_log(task_id, str(e))
            
            return {
                "success": False,
                "error": str(e)
            }
    
    def _execute_bolt_steps(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the individual steps of a bolt cycle.
        
        Args:
            task: Task data
            
        Returns:
            Dictionary with execution results
        """
        task_id = task["task_id"]
        
        # Analysis step
        if not self._execute_analysis_step(task):
            return {
                "success": False,
                "error": "Analysis step failed",
                "details": self.orchestrator.context.error_logs[-1] if self.orchestrator.context.error_logs else {}
            }
        
        # Refactoring step
        if not self._execute_refactoring_step(task):
            return {
                "success": False,
                "error": "Refactoring step failed",
                "details": self.orchestrator.context.error_logs[-1] if self.orchestrator.context.error_logs else {}
            }
        
        # Testing step
        if not self._execute_testing_step(task):
            return {
                "success": False,
                "error": "Testing step failed",
                "details": self.orchestrator.context.error_logs[-1] if self.orchestrator.context.error_logs else {}
            }
        
        # Validation step
        if not self._execute_validation_step(task):
            return {
                "success": False,
                "error": "Validation step failed",
                "details": self.orchestrator.context.error_logs[-1] if self.orchestrator.context.error_logs else {}
            }
        
        # Mark bolt as complete
        self.orchestrator.transition(BoltAction.COMPLETE_BOLT)
        
        return {
            "success": True,
            "task_id": task_id,
            "entity_name": self.orchestrator.context.entity_name,
            "duration": self.orchestrator.get_status().get("duration"),
            "analysis_result": self.orchestrator.context.analysis_result,
            "refactored_code": self.orchestrator.context.refactored_code,
            "test_results": self.orchestrator.context.test_results,
            "validation_results": self.orchestrator.context.validation_results
        }
    
    def _execute_analysis_step(self, task: Dict[str, Any]) -> bool:
        """
        Execute the analysis step of a bolt cycle.
        
        Args:
            task: Task data
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Executing analysis step for task {task['task_id']}")
        
        # Transition to analysis state
        self.orchestrator.transition(BoltAction.START_ANALYSIS)
        
        # Simulate analysis work
        time.sleep(0.1)  # Simulate work
        
        # For now, we'll simulate a successful analysis
        # In a real implementation, this would call the CodebaseAnalyst agent
        analysis_result = {
            "components": ["hull", "shields", "weapons"],
            "dependencies": [],
            "file_types": [".tbl", ".pof"]
        }
        
        target_files = [
            f"target/scenes/{task['task_id'].split('-')[1].lower()}.tscn",
            f"target/scripts/{task['task_id'].split('-')[1].lower()}.gd"
        ]
        
        # Complete analysis
        success = self.orchestrator.transition(BoltAction.COMPLETE_ANALYSIS, {
            "analysis_result": analysis_result,
            "target_files": target_files
        })
        
        logger.info(f"Analysis step completed for task {task['task_id']}: {success}")
        return success
    
    def _execute_refactoring_step(self, task: Dict[str, Any]) -> bool:
        """
        Execute the refactoring step of a bolt cycle.
        
        Args:
            task: Task data
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Executing refactoring step for task {task['task_id']}")
        
        # Transition to refactoring state
        self.orchestrator.transition(BoltAction.START_REFACTORING)
        
        # Simulate refactoring work
        time.sleep(0.1)  # Simulate work
        
        # For now, we'll simulate a successful refactoring
        # In a real implementation, this would call the RefactoringSpecialist agent
        refactored_code = f"class_name {task['task_id'].split('-')[1]}\nextends Node3D\n\n# Refactored code here"
        
        # Complete refactoring
        success = self.orchestrator.transition(BoltAction.COMPLETE_REFACTORING, {
            "refactored_code": refactored_code
        })
        
        logger.info(f"Refactoring step completed for task {task['task_id']}: {success}")
        return success
    
    def _execute_testing_step(self, task: Dict[str, Any]) -> bool:
        """
        Execute the testing step of a bolt cycle.
        
        Args:
            task: Task data
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Executing testing step for task {task['task_id']}")
        
        # Transition to testing state
        self.orchestrator.transition(BoltAction.START_TESTING)
        
        # Simulate testing work
        time.sleep(0.1)  # Simulate work
        
        # For now, we'll simulate successful tests
        # In a real implementation, this would call the TestGenerator and ValidationEngineer agents
        test_results = {
            "passed": 5,
            "failed": 0,
            "total": 5,
            "coverage": 95.0
        }
        
        # Complete testing
        success = self.orchestrator.transition(BoltAction.COMPLETE_TESTING, {
            "test_results": test_results
        })
        
        logger.info(f"Testing step completed for task {task['task_id']}: {success}")
        return success
    
    def _execute_validation_step(self, task: Dict[str, Any]) -> bool:
        """
        Execute the validation step of a bolt cycle.
        
        Args:
            task: Task data
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Executing validation step for task {task['task_id']}")
        
        # Transition to validation state
        self.orchestrator.transition(BoltAction.START_VALIDATION)
        
        # Simulate validation work
        time.sleep(0.1)  # Simulate work
        
        # For now, we'll simulate successful validation
        # In a real implementation, this would call the ValidationEngineer agent
        validation_results = {
            "syntax_valid": True,
            "style_compliant": True,
            "security_issues": [],
            "performance_metrics": {"memory": "normal", "cpu": "normal"}
        }
        
        # Complete validation
        success = self.orchestrator.transition(BoltAction.COMPLETE_VALIDATION, {
            "validation_results": validation_results
        })
        
        logger.info(f"Validation step completed for task {task['task_id']}: {success}")
        return success
    
    def process_next_task(self) -> Optional[Dict[str, Any]]:
        """
        Process the next available task from the queue.
        
        Returns:
            Execution results, or None if no task is available
        """
        # Get next pending task
        task = self.queue_manager.get_next_pending_task()
        if not task:
            logger.info("No pending tasks available")
            return None
        
        task_id = task["task_id"]
        logger.info(f"Processing task {task_id}")
        
        # Execute the bolt cycle
        result = self.execute_bolt_cycle(task_id)
        return result


def main():
    """Main function for testing the BoltExecutor."""
    # Create bolt executor
    executor = BoltExecutor("test_task_queue.yaml", max_retries=2)
    
    # Add some test tasks
    executor.queue_manager.add_task("SHIP-GTC_FENRIS", {
        "description": "Migrate the GTC Fenris cruiser",
        "source_files": ["source/tables/ships.tbl", "source/models/fenris.pof"],
        "dependencies": []
    })
    
    # Process the next task
    result = executor.process_next_task()
    print("Execution result:", result)
    
    # Print queue summary
    print("Queue summary:", executor.queue_manager.get_queue_summary())


if __name__ == "__main__":
    main()