"""
State Machine Orchestrator Implementation

This module implements a custom state machine-based orchestrator for deterministic bolt cycles
in the Wing Commander Saga to Godot migration.
"""

import json
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
from converter.utils import setup_logging, generate_timestamp, calculate_duration

# Configure logging
logger = setup_logging(__name__)


class BoltState(Enum):
    """Enumeration of bolt states."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    ANALYSIS_COMPLETE = "analysis_complete"
    REFACTORING_COMPLETE = "refactoring_complete"
    TESTING_COMPLETE = "testing_complete"
    VALIDATION_COMPLETE = "validation_complete"
    COMPLETED = "completed"
    FAILED = "failed"
    ESCALATED = "escalated"


class BoltAction(Enum):
    """Enumeration of bolt actions."""
    START_ANALYSIS = "start_analysis"
    COMPLETE_ANALYSIS = "complete_analysis"
    START_REFACTORING = "start_refactoring"
    COMPLETE_REFACTORING = "complete_refactoring"
    START_TESTING = "start_testing"
    COMPLETE_TESTING = "complete_testing"
    START_VALIDATION = "start_validation"
    COMPLETE_VALIDATION = "complete_validation"
    COMPLETE_BOLT = "complete_bolt"
    FAIL_BOLT = "fail_bolt"
    ESCALATE_BOLT = "escalate_bolt"


@dataclass
class BoltContext:
    """Context data for a bolt execution."""
    task_id: str
    entity_name: str
    source_files: List[str]
    target_files: List[str] = field(default_factory=list)
    analysis_result: Optional[Dict[str, Any]] = None
    refactored_code: Optional[str] = None
    test_results: Optional[Dict[str, Any]] = None
    validation_results: Optional[Dict[str, Any]] = None
    error_logs: List[Dict[str, Any]] = field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3


class StateMachineOrchestrator:
    """Custom state machine orchestrator for deterministic bolt cycles."""
    
    def __init__(self, max_retries: int = 3):
        """
        Initialize the state machine orchestrator.
        
        Args:
            max_retries: Maximum number of retries for a bolt before escalation
        """
        self.max_retries = max_retries
        self.current_state = BoltState.PENDING
        self.context = None
        self.start_time = None
        self.end_time = None
        
        # Define state transitions
        self.transitions = {
            (BoltState.PENDING, BoltAction.START_ANALYSIS): BoltState.IN_PROGRESS,
            (BoltState.IN_PROGRESS, BoltAction.COMPLETE_ANALYSIS): BoltState.ANALYSIS_COMPLETE,
            (BoltState.ANALYSIS_COMPLETE, BoltAction.START_REFACTORING): BoltState.IN_PROGRESS,
            (BoltState.IN_PROGRESS, BoltAction.COMPLETE_REFACTORING): BoltState.REFACTORING_COMPLETE,
            (BoltState.REFACTORING_COMPLETE, BoltAction.START_TESTING): BoltState.IN_PROGRESS,
            (BoltState.IN_PROGRESS, BoltAction.COMPLETE_TESTING): BoltState.TESTING_COMPLETE,
            (BoltState.TESTING_COMPLETE, BoltAction.START_VALIDATION): BoltState.IN_PROGRESS,
            (BoltState.IN_PROGRESS, BoltAction.COMPLETE_VALIDATION): BoltState.VALIDATION_COMPLETE,
            (BoltState.VALIDATION_COMPLETE, BoltAction.COMPLETE_BOLT): BoltState.COMPLETED,
            (BoltState.IN_PROGRESS, BoltAction.FAIL_BOLT): BoltState.FAILED,
            (BoltState.ANALYSIS_COMPLETE, BoltAction.FAIL_BOLT): BoltState.FAILED,
            (BoltState.REFACTORING_COMPLETE, BoltAction.FAIL_BOLT): BoltState.FAILED,
            (BoltState.TESTING_COMPLETE, BoltAction.FAIL_BOLT): BoltState.FAILED,
            (BoltState.VALIDATION_COMPLETE, BoltAction.FAIL_BOLT): BoltState.FAILED,
            (BoltState.FAILED, BoltAction.ESCALATE_BOLT): BoltState.ESCALATED,
        }
        
        logger.info("State Machine Orchestrator initialized")
    
    def initialize_bolt(self, task_id: str, entity_name: str, source_files: List[str]) -> None:
        """
        Initialize a new bolt execution.
        
        Args:
            task_id: Unique identifier for the task
            entity_name: Name of the entity being migrated
            source_files: List of source files to process
        """
        self.context = BoltContext(
            task_id=task_id,
            entity_name=entity_name,
            source_files=source_files,
            max_retries=self.max_retries
        )
        self.current_state = BoltState.PENDING
        self.start_time = generate_timestamp()
        self.end_time = None
        
        logger.info(f"Initialized bolt execution for task {task_id}: {entity_name}")
    
    def transition(self, action: BoltAction, data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Transition to a new state based on an action.
        
        Args:
            action: The action to perform
            data: Optional data associated with the action
            
        Returns:
            True if transition was successful, False otherwise
        """
        if self.context is None:
            logger.error("Cannot transition: bolt not initialized")
            return False
            
        # Check if transition is valid
        if (self.current_state, action) not in self.transitions:
            logger.warning(f"Invalid transition: {self.current_state} -> {action}")
            return False
        
        # Perform the transition
        previous_state = self.current_state
        self.current_state = self.transitions[(self.current_state, action)]
        
        # Update context with data if provided
        if data:
            self._update_context(action, data)
        
        # Log the transition
        logger.info(f"State transition: {previous_state} -> {action} -> {self.current_state}")
        
        # Handle special transitions
        if self.current_state == BoltState.COMPLETED:
            self.end_time = generate_timestamp()
            duration = calculate_duration(self.start_time, self.end_time)
            logger.info(f"Bolt execution completed in {duration:.2f} seconds")
        elif self.current_state == BoltState.FAILED:
            self.context.retry_count += 1
            logger.warning(f"Bolt execution failed (attempt {self.context.retry_count})")
            
            # Check if we should escalate
            if self.context.retry_count >= self.context.max_retries:
                self.transition(BoltAction.ESCALATE_BOLT)
        elif self.current_state == BoltState.ESCALATED:
            self.end_time = generate_timestamp()
            duration = calculate_duration(self.start_time, self.end_time)
            logger.error(f"Bolt execution escalated after {self.context.retry_count} attempts in {duration:.2f} seconds")
        
        return True
    
    def _update_context(self, action: BoltAction, data: Dict[str, Any]) -> None:
        """
        Update the context based on the action and data.
        
        Args:
            action: The action that was performed
            data: Data associated with the action
        """
        if action == BoltAction.COMPLETE_ANALYSIS:
            self.context.analysis_result = data.get("analysis_result")
            self.context.target_files = data.get("target_files", [])
        elif action == BoltAction.COMPLETE_REFACTORING:
            self.context.refactored_code = data.get("refactored_code")
        elif action == BoltAction.COMPLETE_TESTING:
            self.context.test_results = data.get("test_results")
        elif action == BoltAction.COMPLETE_VALIDATION:
            self.context.validation_results = data.get("validation_results")
        elif action == BoltAction.FAIL_BOLT:
            error_log = {
                "action": action.value,
                "timestamp": generate_timestamp(),
                "error": data.get("error", "Unknown error"),
                "details": data.get("details", {})
            }
            self.context.error_logs.append(error_log)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the bolt execution.
        
        Returns:
            Dictionary with current status information
        """
        if self.context is None:
            return {"status": "not_initialized"}
        
        duration = None
        if self.start_time:
            if self.end_time:
                duration = calculate_duration(self.start_time, self.end_time)
            else:
                duration = calculate_duration(self.start_time)
        
        return {
            "task_id": self.context.task_id,
            "entity_name": self.context.entity_name,
            "state": self.current_state.value,
            "retry_count": self.context.retry_count,
            "max_retries": self.context.max_retries,
            "duration": duration,
            "error_count": len(self.context.error_logs)
        }
    
    def is_complete(self) -> bool:
        """
        Check if the bolt execution is complete.
        
        Returns:
            True if complete (success or failure), False otherwise
        """
        return self.current_state in [BoltState.COMPLETED, BoltState.FAILED, BoltState.ESCALATED]
    
    def should_retry(self) -> bool:
        """
        Check if the bolt should be retried.
        
        Returns:
            True if should retry, False otherwise
        """
        return self.current_state == BoltState.FAILED and self.context.retry_count < self.context.max_retries
    
    def should_escalate(self) -> bool:
        """
        Check if the bolt should be escalated.
        
        Returns:
            True if should escalate, False otherwise
        """
        return self.current_state == BoltState.FAILED and self.context.retry_count >= self.context.max_retries


def main():
    """Main function for testing the StateMachineOrchestrator."""
    # Create orchestrator
    orchestrator = StateMachineOrchestrator(max_retries=2)
    
    # Initialize a bolt
    orchestrator.initialize_bolt(
        task_id="SHIP-GTC_FENRIS",
        entity_name="GTC Fenris",
        source_files=["source/tables/ships.tbl", "source/models/fenris.pof"]
    )
    
    # Print initial status
    print("Initial status:", orchestrator.get_status())
    
    # Start analysis
    orchestrator.transition(BoltAction.START_ANALYSIS)
    orchestrator.transition(BoltAction.COMPLETE_ANALYSIS, {
        "analysis_result": {"components": ["hull", "shields", "weapons"]},
        "target_files": ["target/scenes/fenris.tscn", "target/scripts/fenris.gd"]
    })
    
    # Start refactoring
    orchestrator.transition(BoltAction.START_REFACTORING)
    orchestrator.transition(BoltAction.COMPLETE_REFACTORING, {
        "refactored_code": "class_name Fenris extends Node3D"
# Refactored code here"
    })
    
    # Start testing
    orchestrator.transition(BoltAction.START_TESTING)
    orchestrator.transition(BoltAction.COMPLETE_TESTING, {
        "test_results": {"passed": 5, "failed": 0, "total": 5}
    })
    
    # Start validation
    orchestrator.transition(BoltAction.START_VALIDATION)
    orchestrator.transition(BoltAction.COMPLETE_VALIDATION, {
        "validation_results": {"syntax_valid": True, "style_compliant": True}
    })
    
    # Complete bolt
    orchestrator.transition(BoltAction.COMPLETE_BOLT)
    
    # Print final status
    print("Final status:", orchestrator.get_status())


if __name__ == "__main__":
    main()