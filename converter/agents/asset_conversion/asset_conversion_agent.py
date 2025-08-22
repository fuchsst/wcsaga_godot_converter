"""
Asset Conversion Agent for the Centurion migration system.
"""

from converter.agents.base_agent import SpecialistAgent
from converter.graph_system.graph_state import CenturionGraphState


class AssetConversionAgent(SpecialistAgent):
    """Specialist agent responsible for converting game assets."""

    def __init__(self):
        """Initialize the AssetConversionAgent."""
        super().__init__("AssetConversionAgent")

    async def execute(self, state: CenturionGraphState) -> CenturionGraphState:
        """
        Execute the asset conversion task.

        Args:
            state: Current graph state

        Returns:
            Updated graph state with converted assets
        """
        self._log_execution_start(
            state.get("active_task", {}).get("task_id", "unknown")
        )

        try:
            # Get the active task
            active_task = state.get("active_task", {})
            source_files = active_task.get("source_files", [])

            # In a real implementation, this would convert assets using external tools
            # For now, we'll just log the files that would be converted
            print(f"[{self.name}] Converting assets: {source_files}")

            # Update the state
            state["current_step"] = "asset_conversion"
            state["converted_assets"] = source_files  # Placeholder

        except Exception as e:
            print(f"[{self.name}] Asset conversion failed: {str(e)}")
            if "error_logs" not in state:
                state["error_logs"] = []
            state["error_logs"].append(
                {
                    "step": "asset_conversion",
                    "error": str(e),
                    "entity": state.get("active_task", {}).get(
                        "entity_name", "unknown"
                    ),
                }
            )

        self._log_execution_end(state.get("active_task", {}).get("task_id", "unknown"))
        return state
