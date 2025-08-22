"""
LangGraph Orchestrator Implementation

This module implements the main orchestrator using LangGraph for deterministic state management
with a robust, stateful approach.
"""

import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict, Union

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from langgraph.pregel import RetryPolicy
from langgraph.types import Command, interrupt

from converter.analyst.codebase_analyst import CodebaseAnalyst
from converter.graph_system.graph_manager import GraphManager
from converter.hitl.langgraph_hitl import LangGraphHITLIntegration
from converter.refactoring.refactoring_specialist import RefactoringSpecialist
from converter.test_generator.test_generator import TestGenerator
from converter.utils import generate_timestamp, setup_logging
from converter.validation.test_quality_gate import TestQualityGate
from converter.validation.validation_engineer import ValidationEngineer

# Configure logging
logger = setup_logging(__name__)


class CenturionGraphState(TypedDict, total=False):
    """
    Master state schema for the LangGraph-based Centurion migration system.
    This state serves as the "single source of truth" for the entire workflow.
    """

    # Task queue management
    task_queue: List[
        Dict[str, Any]
    ]  # The full list of tasks, loaded from task_queue.yaml
    active_task: Optional[
        Dict[str, Any]
    ]  # The task dictionary currently being processed

    # Code analysis and content
    source_code_content: Dict[str, str]  # Mapping of file paths to their string content
    analysis_report: Optional[
        Dict[str, Any]
    ]  # Structured JSON output from Codebase Analyst

    # Code generation
    generated_gdscript: Optional[
        str
    ]  # GDScript code produced by Refactoring Specialist

    # Validation and testing
    validation_result: Optional[
        Dict[str, Any]
    ]  # Structured output from Validation toolchain
    test_results: Optional[Dict[str, Any]]  # Test execution results

    # Communication and messaging
    messages: List[Dict[str, Any]]  # Conversational history for LLM-powered nodes

    # Error handling and retry logic
    retry_count: int  # Number of attempts for the active task
    last_error: Optional[
        str
    ]  # Formatted error message from the last failed validation step

    # Human-in-the-loop integration
    human_intervention_request: Optional[
        Dict[str, Any]
    ]  # Data surfaced to a human for interrupt patterns

    # Workflow tracking
    target_files: List[str]  # Paths to target files for the current task
    status: str  # Current status of the workflow
    current_step: str  # Current step in the bolt cycle


# Backward compatibility alias
MigrationState = CenturionGraphState


class LangGraphOrchestrator:
    """Main orchestrator using LangGraph for deterministic state management."""

    def __init__(
        self,
        source_path: str,
        target_path: str,
        graph_file: str = "dependency_graph.json",
    ):
        """
        Initialize the LangGraph orchestrator.

        Args:
            source_path: Path to the source C++ codebase
            target_path: Path to the target Godot project
            graph_file: Path to the dependency graph file
        """
        self.source_path = Path(source_path)
        self.target_path = Path(target_path)

        # Initialize enhanced components
        self.graph_manager = GraphManager(graph_file, auto_save=True)
        self.quality_gate = TestQualityGate(min_coverage=85.0, min_test_count=5)
        self.hitl_integration = LangGraphHITLIntegration()

        # Configure checkpointer for state persistence
        self.checkpointer = MemorySaver()

        # Configure retry policy for error handling
        self.retry_policy = RetryPolicy(
            max_attempts=3, retry_on=(ValueError, RuntimeError, ConnectionError)
        )

        # Build the LangGraph workflow
        self.workflow = self._build_workflow()

        logger.info("LangGraph Orchestrator initialized")

    def _build_workflow(self):
        """Build the LangGraph workflow for migration following the Centurion blueprint."""
        builder = StateGraph(CenturionGraphState)

        # Define nodes as per the architectural recommendation
        builder.add_node(
            "select_next_task", self._select_next_task
        )  # Orchestrator role
        builder.add_node(
            "analyze_codebase", self._analyze_codebase
        )  # Codebase Analyst role
        builder.add_node(
            "generate_code", self._generate_code
        )  # Refactoring Specialist via Prompt Engineer
        builder.add_node(
            "validate_code", self._validate_code
        )  # Quality Assurance Agent
        builder.add_node(
            "handle_failure", self._handle_failure
        )  # Implicit Orchestrator
        builder.add_node("complete_task", self._complete_task)  # Implicit Orchestrator
        builder.add_node(
            "human_approval_gate", self._human_approval_gate
        )  # HITL integration
        builder.add_node(
            "escalate_to_human", self._escalate_to_human
        )  # Escalation node

        # Define edges
        builder.set_entry_point("select_next_task")

        builder.add_edge("select_next_task", "analyze_codebase")
        builder.add_edge("analyze_codebase", "generate_code")
        builder.add_edge("generate_code", "validate_code")

        # Conditional edges for validation results
        builder.add_conditional_edges(
            "validate_code",
            self._check_validation_results,
            {"success": "check_human_approval", "failure": "handle_failure"},
        )

        # Add the missing check_human_approval node
        builder.add_node("check_human_approval", self._check_human_approval)

        # Conditional edges for human approval
        builder.add_conditional_edges(
            "check_human_approval",
            self._check_human_approval_needed,
            {"needs_approval": "human_approval_gate", "no_approval": "complete_task"},
        )

        # Human approval gate
        builder.add_conditional_edges(
            "human_approval_gate",
            self._check_human_approval_result,
            {"approved": "complete_task", "rejected": "escalate_to_human"},
        )

        # Failure handling with retry logic
        builder.add_conditional_edges(
            "handle_failure",
            self._should_retry_or_escalate,
            {"retry": "generate_code", "escalate": "escalate_to_human"},
        )

        builder.add_edge("complete_task", END)
        builder.add_edge("escalate_to_human", END)

        return builder.compile(checkpointer=self.checkpointer)

    async def _select_next_task(self, state: dict) -> dict:
        """Select the next pending task from the task queue (Orchestrator role)."""
        logger.info("Selecting next task from task queue")
        state["current_step"] = "task_selection"

        # For now, we'll use a simple approach to select the next task
        # In a real implementation, this would load from task_queue.yaml
        if not state.get("task_queue"):
            state["task_queue"] = [
                {
                    "task_id": "SHIP-GTC_FENRIS",
                    "entity_name": "GTC Fenris",
                    "source_files": [
                        "source/tables/ships.tbl",
                        "source/models/fenris.pof",
                    ],
                    "status": "pending",
                    "requires_human_approval": False,
                }
            ]

        # Find the next pending task
        for task in state["task_queue"]:
            if task.get("status") == "pending":
                state["active_task"] = task
                task["status"] = "in_progress"

                # Load source code content
                source_code_content = {}
                for file_path in task.get("source_files", []):
                    try:
                        if Path(file_path).exists():
                            with open(file_path, "r", encoding="utf-8") as f:
                                source_code_content[file_path] = f.read()
                        else:
                            source_code_content[file_path] = (
                                f"# File not found: {file_path}"
                            )
                    except Exception as e:
                        source_code_content[file_path] = (
                            f"# Error reading file: {str(e)}"
                        )

                state["source_code_content"] = source_code_content
                break

        state["status"] = "in_progress"
        return state

    async def _analyze_codebase(
        self, state: CenturionGraphState
    ) -> CenturionGraphState:
        """Parse source code and legacy files using tools (Codebase Analyst role)."""
        logger.info(
            f"Analyzing codebase for {state.get('active_task', {}).get('entity_name', 'unknown')}"
        )
        state["current_step"] = "codebase_analysis"

        try:
            # Initialize Codebase Analyst
            analyst = CodebaseAnalyst()

            # Perform actual analysis
            analysis_result = analyst.analyze_entity(
                state.get("active_task", {}).get("entity_name", "unknown"),
                state.get("active_task", {}).get("source_files", []),
            )

            state["analysis_report"] = analysis_result

            # Determine target files based on analysis
            target_files = []
            entity_name = (
                state.get("active_task", {}).get("entity_name", "unknown").lower()
            )
            target_files.append(f"target/scenes/{entity_name}.tscn")
            target_files.append(f"target/scripts/{entity_name}.gd")
            state["target_files"] = target_files

        except Exception as e:
            logger.error(f"Codebase analysis failed: {str(e)}")
            if "error_logs" not in state:
                state["error_logs"] = []
            state["error_logs"].append(
                {
                    "step": "codebase_analysis",
                    "error": str(e),
                    "entity": state.get("active_task", {}).get(
                        "entity_name", "unknown"
                    ),
                }
            )

        return state

    def _determine_target_files(
        self, entity_name: str, analysis_result: Dict[str, Any]
    ) -> List[str]:
        """Determine target file paths based on analysis results."""
        target_files = []
        entity_name_lower = entity_name.lower()

        # Add scene file
        target_files.append(f"target/scenes/{entity_name_lower}.tscn")

        # Add script file
        target_files.append(f"target/scripts/{entity_name_lower}.gd")

        # Add any additional files based on analysis
        if analysis_result.get("components"):
            # For example, if there are specific components, we might need additional files
            pass

        return target_files

    async def _generate_code(self, state: CenturionGraphState) -> CenturionGraphState:
        """Craft prompt and call qwen-code tool (Refactoring Specialist via Prompt Engineer)."""
        logger.info(
            f"Generating code for {state.active_task.get('entity_name', 'unknown')}"
        )
        state.current_step = "code_generation"

        try:
            # Initialize Refactoring Specialist
            refactoring_specialist = RefactoringSpecialist()

            # Perform actual refactoring using the analysis report
            refactored_code = refactoring_specialist.refactor_entity(
                state.active_task.get("entity_name", "unknown"),
                state.active_task.get("source_files", []),
                state.analysis_report,
            )

            state.generated_gdscript = refactored_code

        except Exception as e:
            logger.error(f"Code generation failed: {str(e)}")
            if "error_logs" not in state:
                state.error_logs = []
            state.error_logs.append(
                {
                    "step": "code_generation",
                    "error": str(e),
                    "entity": state.active_task.get("entity_name", "unknown"),
                }
            )

        return state

    async def _validate_code(self, state: CenturionGraphState) -> CenturionGraphState:
        """Run compilation and unit tests via tools (Quality Assurance Agent)."""
        logger.info(
            f"Validating code for {state.active_task.get('entity_name', 'unknown')}"
        )
        state.current_step = "code_validation"

        try:
            # Initialize Validation Engineer
            validation_engineer = ValidationEngineer()

            # Generate tests first
            test_generator = TestGenerator()
            test_results = test_generator.generate_tests(
                state.active_task.get("entity_name", "unknown"),
                state.generated_gdscript,
                state.analysis_report,
            )
            state.test_results = test_results

            # Validate the generated code and tests
            validation_results = validation_engineer.validate_tests(
                state.active_task.get("entity_name", "unknown"),
                state.generated_gdscript,
                test_results,
            )

            state.validation_result = validation_results

        except Exception as e:
            logger.error(f"Code validation failed: {str(e)}")
            if "error_logs" not in state:
                state.error_logs = []
            state.error_logs.append(
                {
                    "step": "code_validation",
                    "error": str(e),
                    "entity": state.active_task.get("entity_name", "unknown"),
                }
            )

        return state

    async def _complete_task(self, state: CenturionGraphState) -> CenturionGraphState:
        """Update task status to completed in task_queue (Implicit Orchestrator)."""
        logger.info(f"Completing task {state.active_task.get('task_id', 'unknown')}")
        state.current_step = "task_completion"
        state.status = "completed"

        # Update the active task status
        if state.active_task:
            state.active_task["status"] = "completed"
            state.active_task["completed_at"] = generate_timestamp()

            # Update dependency graph
            self.graph_manager.add_entity(
                state.active_task.get("task_id", "unknown"),
                "migrated_entity",
                {
                    "name": state.active_task.get("entity_name", "unknown"),
                    "status": "completed",
                    "target_files": state.target_files,
                    "completed_at": state.active_task["completed_at"],
                },
            )

        return state

    async def _human_approval_gate(
        self, state: CenturionGraphState
    ) -> Union[CenturionGraphState, Command]:
        """Request human approval for critical tasks (HITL integration)."""
        logger.info(
            f"Requesting human approval for {state.get('active_task', {}).get('task_id', 'unknown')}"
        )
        state["current_step"] = "human_approval"

        # Create human intervention request
        human_request = {
            "task_id": state.get("active_task", {}).get("task_id", "unknown"),
            "entity_name": state.get("active_task", {}).get("entity_name", "unknown"),
            "generated_code": state.get("generated_gdscript"),
            "test_results": state.get("test_results"),
            "validation_result": state.get("validation_result"),
            "request_type": "approval",
            "requested_at": generate_timestamp(),
        }

        state["human_intervention_request"] = human_request

        # Use LangGraph's interrupt function to pause execution for human input
        human_response = interrupt(human_request)

        # Process human response
        if human_response.get("approved", False):
            state["human_review_result"] = {
                "approved": True,
                "timestamp": generate_timestamp(),
                "comments": human_response.get("comments", ""),
            }
            return state
        else:
            # If rejected, return Command to route to escalation
            return Command(
                goto="escalate_to_human",
                update={
                    "human_review_result": {
                        "approved": False,
                        "timestamp": generate_timestamp(),
                        "comments": human_response.get(
                            "comments", "Task rejected by human reviewer"
                        ),
                    }
                },
            )

    async def _check_human_approval(
        self, state: CenturionGraphState
    ) -> CenturionGraphState:
        """Check if human approval is needed (implicit node)."""
        logger.info(
            f"Checking if human approval is needed for {state.active_task.get('task_id', 'unknown')}"
        )
        state.current_step = "check_human_approval"
        return state

    async def _handle_failure(self, state: CenturionGraphState) -> CenturionGraphState:
        """Increment retry count and log errors (Implicit Orchestrator)."""
        logger.warning(
            f"Handling failure for {state.get('active_task', {}).get('entity_name', 'unknown')}"
        )
        state["current_step"] = "failure_handling"
        state["retry_count"] = state.get("retry_count", 0) + 1

        return state

    async def _escalate_to_human(
        self, state: CenturionGraphState
    ) -> CenturionGraphState:
        """Escalate to human review (Implicit Orchestrator)."""
        logger.error(
            f"Escalating task {state.get('active_task', {}).get('task_id', 'unknown')} to human review"
        )
        state["current_step"] = "human_escalation"
        state["status"] = "escalated"

        # Update the active task status
        if state.get("active_task"):
            state["active_task"]["status"] = "escalated"
            state["active_task"]["escalated_at"] = generate_timestamp()

        # Request human review through HITL integration
        self.hitl_integration.request_verification(
            state.get("active_task", {}).get("task_id", "unknown"),
            f"Migration escalation for {state.get('active_task', {}).get('entity_name', 'unknown')}",
            {
                "error_logs": state.get("error_logs", []),
                "retry_count": state.get("retry_count", 0),
                "generated_code": state.get("generated_gdscript"),
                "test_results": state.get("test_results"),
                "validation_result": state.get("validation_result"),
            },
        )

        return state

    def _check_validation_results(self, state: CenturionGraphState) -> str:
        """Check validation results and route accordingly."""
        # Check if validation passed
        if state.get("validation_result") and state["validation_result"].get(
            "syntax_valid", False
        ):
            return "success"
        return "failure"

    def _check_human_approval_needed(self, state: CenturionGraphState) -> str:
        """Check if human approval is needed for this task."""
        if state.get("active_task") and state["active_task"].get(
            "requires_human_approval", False
        ):
            return "needs_approval"
        return "no_approval"

    def _check_human_approval_result(self, state: CenturionGraphState) -> str:
        """Check the result of human approval."""
        if state.get("human_review_result") and state["human_review_result"].get(
            "approved", False
        ):
            return "approved"
        return "rejected"

    def _should_retry_or_escalate(self, state: CenturionGraphState) -> str:
        """Determine if we should retry or escalate based on retry count."""
        retry_count = state.get("retry_count", 0)
        max_retries = (
            state.get("active_task", {}).get("max_retries", 3)
            if state.get("active_task")
            else 3
        )

        if retry_count < max_retries:
            return "retry"
        return "escalate"

    async def execute_bolt(
        self, task_id: str, entity_name: str, source_files: List[str]
    ) -> Dict[str, Any]:
        """Execute a complete bolt cycle."""
        logger.info(f"Executing bolt for task {task_id}: {entity_name}")

        # Initialize state with proper task queue structure
        initial_state = {
            "task_queue": [
                {
                    "task_id": task_id,
                    "entity_name": entity_name,
                    "source_files": source_files,
                    "status": "pending",
                    "requires_human_approval": False,
                }
            ]
        }

        try:
            # Execute the workflow
            final_state = await self.workflow.ainvoke(initial_state)

            return {
                "success": final_state.get("status") == "completed",
                "task_id": task_id,
                "entity_name": entity_name,
                "status": final_state.get("status", "unknown"),
                "retry_count": final_state.get("retry_count", 0),
                "error_count": len(final_state.get("error_logs", [])),
                "analysis_report": final_state.get("analysis_report"),
                "generated_gdscript": final_state.get("generated_gdscript"),
                "test_results": final_state.get("test_results"),
                "validation_result": final_state.get("validation_result"),
            }

        except Exception as e:
            logger.error(f"Error executing bolt for task {task_id}: {str(e)}")
            return {
                "success": False,
                "task_id": task_id,
                "entity_name": entity_name,
                "error": str(e),
                "status": "failed",
            }

    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the orchestrator."""
        return {
            "source_path": str(self.source_path),
            "target_path": str(self.target_path),
            "graph_entities": self.graph_manager.get_statistics().get("node_count", 0),
            "graph_dependencies": self.graph_manager.get_statistics().get(
                "edge_count", 0
            ),
            "last_updated": generate_timestamp(),
        }


def main():
    """Main function for testing the LangGraphOrchestrator."""
    # Create orchestrator
    orchestrator = LangGraphOrchestrator(
        source_path="../source",
        target_path="../target",
        graph_file="test_dependency_graph.json",
    )

    # Print initial status
    print("Initial status:", orchestrator.get_status())

    # Execute a bolt
    result = asyncio.run(
        orchestrator.execute_bolt(
            task_id="SHIP-GTC_FENRIS",
            entity_name="GTC Fenris",
            source_files=["source/tables/ships.tbl", "source/models/fenris.pof"],
        )
    )

    # Print final status
    print("Final status:", orchestrator.get_status())
    print("Bolt result:", result)


if __name__ == "__main__":
    main()
