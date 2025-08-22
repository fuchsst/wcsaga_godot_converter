"""
Validation Agent for the Centurion migration system.
"""

from converter.agents.base_agent import SpecialistAgent
from converter.graph_system.graph_state import CenturionGraphState
from converter.validation.validation_engineer import ValidationEngineer


class ValidationAgent(SpecialistAgent):
    """Specialist agent responsible for validating the generated code and tests."""

    def __init__(self):
        """Initialize the ValidationAgent."""
        super().__init__("ValidationAgent")
        self.validation_engineer = ValidationEngineer()

    async def execute(self, state: CenturionGraphState) -> CenturionGraphState:
        """
        Execute the validation task.

        Args:
            state: Current graph state

        Returns:
            Updated graph state with validation results
        """
        self._log_execution_start(
            state.get("active_task", {}).get("task_id", "unknown")
        )

        try:
            # Get the active task
            active_task = state.get("active_task", {})
            entity_name = active_task.get("entity_name", "unknown")
            generated_gdscript = state.get("generated_gdscript", "")
            test_results = state.get("test_results", {})

            # Validate the generated code and tests
            validation_results = self.validation_engineer.validate_tests(
                entity_name, generated_gdscript, test_results
            )

            # Update the state with the validation results
            state["validation_result"] = validation_results
            state["current_step"] = "code_validation"

        except Exception as e:
            print(f"[{self.name}] Code validation failed: {str(e)}")
            if "error_logs" not in state:
                state["error_logs"] = []
            state["error_logs"].append(
                {
                    "step": "code_validation",
                    "error": str(e),
                    "entity": state.get("active_task", {}).get(
                        "entity_name", "unknown"
                    ),
                }
            )

        self._log_execution_end(state.get("active_task", {}).get("task_id", "unknown"))
        return state
