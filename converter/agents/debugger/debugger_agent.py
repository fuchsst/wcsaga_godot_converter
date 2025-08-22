"""
Debugger Agent for the Centurion migration system.
"""

from converter.agents.base_agent import SpecialistAgent
from converter.graph_system.graph_state import CenturionGraphState


class DebuggerAgent(SpecialistAgent):
    """Specialist agent responsible for debugging failed code."""

    def __init__(self):
        """Initialize the DebuggerAgent."""
        super().__init__("DebuggerAgent")

    async def execute(self, state: CenturionGraphState) -> CenturionGraphState:
        """
        Execute the debugging task.

        Args:
            state: Current graph state

        Returns:
            Updated graph state with debugged code
        """
        self._log_execution_start(
            state.get("active_task", {}).get("task_id", "unknown")
        )

        try:
            # Get the active task and validation results
            active_task = state.get("active_task", {})
            entity_name = active_task.get("entity_name", "unknown")
            generated_gdscript = state.get("generated_gdscript", "")
            validation_result = state.get("validation_result", {})
            test_results = state.get("test_results", {})

            # In a real implementation, this would analyze the error and generate fixed code
            # For now, we'll just log the error and increment the retry count
            print(f"[{self.name}] Debugging failed code for {entity_name}")
            print(f"[{self.name}] Validation result: {validation_result}")
            print(f"[{self.name}] Test results: {test_results}")

            # Update the state
            state["current_step"] = "debugging"
            state["retry_count"] = state.get("retry_count", 0) + 1

        except Exception as e:
            print(f"[{self.name}] Debugging failed: {str(e)}")
            if "error_logs" not in state:
                state["error_logs"] = []
            state["error_logs"].append(
                {
                    "step": "debugging",
                    "error": str(e),
                    "entity": state.get("active_task", {}).get(
                        "entity_name", "unknown"
                    ),
                }
            )

        self._log_execution_end(state.get("active_task", {}).get("task_id", "unknown"))
        return state
