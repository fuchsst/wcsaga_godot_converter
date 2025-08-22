"""
Test Generation Agent for the Centurion migration system.
"""

from converter.agents.base_agent import SpecialistAgent
from converter.graph_system.graph_state import CenturionGraphState
from converter.test_generator.test_generator import TestGenerator


class TestGenerationAgent(SpecialistAgent):
    """Specialist agent responsible for generating tests for the re-implemented code."""

    def __init__(self):
        """Initialize the TestGenerationAgent."""
        super().__init__("TestGenerationAgent")
        self.test_generator = TestGenerator()

    async def execute(self, state: CenturionGraphState) -> CenturionGraphState:
        """
        Execute the test generation task.

        Args:
            state: Current graph state

        Returns:
            Updated graph state with generated tests
        """
        self._log_execution_start(
            state.get("active_task", {}).get("task_id", "unknown")
        )

        try:
            # Get the active task
            active_task = state.get("active_task", {})
            entity_name = active_task.get("entity_name", "unknown")
            generated_gdscript = state.get("generated_gdscript", "")
            analysis_report = state.get("analysis_report", {})

            # Generate tests
            test_results = self.test_generator.generate_tests(
                entity_name, generated_gdscript, analysis_report
            )

            # Update the state with the generated tests
            state["test_results"] = test_results
            state["current_step"] = "test_generation"

        except Exception as e:
            print(f"[{self.name}] Test generation failed: {str(e)}")
            if "error_logs" not in state:
                state["error_logs"] = []
            state["error_logs"].append(
                {
                    "step": "test_generation",
                    "error": str(e),
                    "entity": state.get("active_task", {}).get(
                        "entity_name", "unknown"
                    ),
                }
            )

        self._log_execution_end(state.get("active_task", {}).get("task_id", "unknown"))
        return state
