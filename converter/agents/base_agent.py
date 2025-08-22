"""
Base Specialist Agent for the Centurion migration system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

from converter.graph_system.graph_state import CenturionGraphState


class SpecialistAgent(ABC):
    """Abstract base class for all specialist agents in the Centurion system."""

    def __init__(self, name: str):
        """
        Initialize the specialist agent.

        Args:
            name: Name of the specialist agent
        """
        self.name = name

    @abstractmethod
    async def execute(self, state: CenturionGraphState) -> CenturionGraphState:
        """
        Execute the specialist agent's task.

        Args:
            state: Current graph state

        Returns:
            Updated graph state
        """
        pass

    def _log_execution_start(self, task_id: str):
        """Log the start of execution."""
        print(f"[{self.name}] Starting execution for task {task_id}")

    def _log_execution_end(self, task_id: str):
        """Log the end of execution."""
        print(f"[{self.name}] Completed execution for task {task_id}")
