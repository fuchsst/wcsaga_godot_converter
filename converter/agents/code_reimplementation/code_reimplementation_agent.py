"""
Code Reimplementation Agent for the Centurion migration system.
"""

from typing import Dict

from converter.agents.base_agent import SpecialistAgent
from converter.graph_system.graph_state import CenturionGraphState
from converter.refactoring.refactoring_specialist import RefactoringSpecialist


class CodeReimplementationAgent(SpecialistAgent):
    """Specialist agent responsible for generating Godot code from C++ specifications."""

    def __init__(self):
        """Initialize the CodeReimplementationAgent."""
        super().__init__("CodeReimplementationAgent")
        self.refactoring_specialist = RefactoringSpecialist()

    async def execute(self, state: CenturionGraphState) -> CenturionGraphState:
        """
        Execute the code reimplementation task.

        Args:
            state: Current graph state

        Returns:
            Updated graph state with generated GDScript code
        """
        self._log_execution_start(
            state.get("active_task", {}).get("task_id", "unknown")
        )

        try:
            # Get the active task
            active_task = state.get("active_task", {})
            entity_name = active_task.get("entity_name", "unknown")
            source_files = active_task.get("source_files", [])
            analysis_report = state.get("analysis_report", {})

            # Perform actual refactoring using the analysis report
            refactored_code = self.refactoring_specialist.refactor_entity(
                entity_name, source_files, analysis_report
            )

            # Update the state with the generated code
            state["generated_gdscript"] = refactored_code
            state["current_step"] = "code_generation"

        except Exception as e:
            print(f"[{self.name}] Code generation failed: {str(e)}")
            if "error_logs" not in state:
                state["error_logs"] = []
            state["error_logs"].append(
                {
                    "step": "code_generation",
                    "error": str(e),
                    "entity": state.get("active_task", {}).get(
                        "entity_name", "unknown"
                    ),
                }
            )

        self._log_execution_end(state.get("active_task", {}).get("task_id", "unknown"))
        return state
