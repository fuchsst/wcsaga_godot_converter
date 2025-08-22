"""
LangGraph Orchestrator Implementation

This module implements the main orchestrator using LangGraph for deterministic state management
with a robust, stateful approach.
"""

import asyncio
import time
from pathlib import Path
from typing import Any, Dict, List, Union

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph
from langgraph.types import Command, RetryPolicy, interrupt

from converter.agents.asset_conversion.asset_conversion_agent import \
    AssetConversionAgent
from converter.agents.code_reimplementation.code_reimplementation_agent import \
    CodeReimplementationAgent
from converter.agents.debugger.debugger_agent import DebuggerAgent
from converter.agents.test_generation.test_generation_agent import \
    TestGenerationAgent
from converter.agents.validation.validation_agent import ValidationAgent
from converter.analyst.codebase_analyst import CodebaseAnalyst
from converter.graph_system.graph_manager import GraphManager
from converter.graph_system.graph_state import CenturionGraphState, Task
from converter.hitl.langgraph_hitl import LangGraphHITLIntegration
from converter.refactoring.refactoring_specialist import RefactoringSpecialist
from converter.test_generator.test_generator import TestGenerator
from converter.utils import generate_timestamp, setup_logging
from converter.validation.test_quality_gate import TestQualityGate
from converter.validation.validation_engineer import ValidationEngineer

# Configure logging
logger = setup_logging(__name__)


# Backward compatibility alias
MigrationState = CenturionGraphState


class CircuitBreaker:
    """Circuit breaker pattern for handling persistent failures."""

    def __init__(self, max_failures: int = 3, reset_timeout: int = 300):
        """
        Initialize the circuit breaker.

        Args:
            max_failures: Maximum number of failures before breaking
            reset_timeout: Time in seconds before attempting to reset the circuit
        """
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open

    def should_break(self) -> bool:
        """Determine if the circuit should break."""
        if self.state == "open":
            # Check if enough time has passed to try resetting
            if (
                self.last_failure_time
                and time.time() - self.last_failure_time > self.reset_timeout
            ):
                self.state = "half-open"
                return False
            return True

        return self.failure_count >= self.max_failures

    def record_failure(self):
        """Record a failure and update circuit state."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.max_failures:
            self.state = "open"

    def record_success(self):
        """Record a success and reset the circuit."""
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"

    def get_state(self) -> Dict[str, Any]:
        """Get the current circuit breaker state."""
        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "last_failure_time": self.last_failure_time,
            "max_failures": self.max_failures,
            "reset_timeout": self.reset_timeout,
        }


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

        # Validate paths
        if not self.source_path.exists():
            raise ValueError(f"Source path does not exist: {self.source_path}")

        # Create target directory if it doesn't exist
        self.target_path.mkdir(parents=True, exist_ok=True)

        # Initialize enhanced components
        self.graph_manager = GraphManager(graph_file, auto_save=True)
        self.quality_gate = TestQualityGate(min_coverage=85.0, min_test_count=5)
        self.hitl_integration = LangGraphHITLIntegration()

        # Configure checkpointer for state persistence
        # Use SQLite for production-grade persistence instead of in-memory
        self.checkpointer = SqliteSaver.from_conn_string("sqlite:///checkpoints.db")

        # Configure retry policy for error handling
        self.retry_policy = RetryPolicy(
            max_attempts=3, retry_on=(ValueError, RuntimeError, ConnectionError)
        )

        # Initialize circuit breaker for persistent failure handling
        self.circuit_breaker = CircuitBreaker(max_failures=5, reset_timeout=600)

        # Build the LangGraph workflow
        self.workflow = self._build_workflow()

        logger.info("LangGraph Orchestrator initialized")

    def _build_workflow(self):
        """Build the LangGraph workflow for migration following the Centurion blueprint."""
        builder = StateGraph(CenturionGraphState)

        # Initialize specialist agents
        self.code_reimplementation_agent = CodeReimplementationAgent()
        self.test_generation_agent = TestGenerationAgent()
        self.validation_agent = ValidationAgent()
        self.debugger_agent = DebuggerAgent()
        self.asset_conversion_agent = AssetConversionAgent()

        # Define nodes as per the architectural recommendation
        builder.add_node(
            "select_next_task", self._select_next_task
        )  # Orchestrator role
        builder.add_node(
            "analyze_codebase", self._analyze_codebase
        )  # Codebase Analyst role
        builder.add_node(
            "generate_code", self.code_reimplementation_agent.execute
        )  # CodeReimplementationAgent
        builder.add_node(
            "generate_tests", self.test_generation_agent.execute
        )  # TestGenerationAgent
        builder.add_node(
            "validate_code", self.validation_agent.execute
        )  # ValidationAgent
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
        builder.add_node(
            "convert_assets", self.asset_conversion_agent.execute
        )  # AssetConversionAgent
        builder.add_node("debug_code", self.debugger_agent.execute)  # DebuggerAgent

        # Define edges
        builder.set_entry_point("select_next_task")

        builder.add_edge("select_next_task", "analyze_codebase")
        builder.add_edge("analyze_codebase", "generate_code")
        builder.add_edge("generate_code", "generate_tests")
        builder.add_edge("generate_tests", "validate_code")

        # Conditional edges for validation results
        builder.add_conditional_edges(
            "validate_code",
            self._check_validation_results,
            {"success": "check_human_approval", "failure": "debug_code"},
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
            "debug_code",
            self._should_retry_or_escalate,
            {"retry": "generate_code", "escalate": "escalate_to_human"},
        )

        builder.add_edge("complete_task", END)
        builder.add_edge("escalate_to_human", END)

        return builder.compile(checkpointer=self.checkpointer)

    async def _select_next_task(self, state: CenturionGraphState) -> CenturionGraphState:
        """Select the next pending task from the task queue (Orchestrator role)."""
        logger.info("Selecting next task from task queue")
        state.current_step = "task_selection"

        # For now, we'll use a simple approach to select the next task
        # In a real implementation, this would load from task_queue.yaml
        if not state.task_queue:
            state.task_queue = [
                Task(
                    task_id="SHIP-GTC_FENRIS",
                    entity_name="GTC Fenris",
                    source_files=[
                        "source/tables/ships.tbl",
                        "source/models/fenris.pof",
                    ],
                    status="pending",
                    requires_human_approval=False,
                )
            ]

        # Find the next pending task
        for task in state.task_queue:
            if task.status == "pending":
                state.active_task = task
                task.status = "in_progress"
                task.started_at = datetime.now()

                # Load source code content
                source_code_content = {}
                for file_path in task.source_files:
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

                state.source_code_content = source_code_content
                break

        state.status = "in_progress"
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

        # Reset circuit breaker on successful completion
        self.circuit_breaker.record_success()
        state["circuit_breaker_state"] = self.circuit_breaker.get_state()

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
        """Increment retry count, log errors, and update circuit breaker (Implicit Orchestrator)."""
        entity_name = state.get("active_task", {}).get("entity_name", "unknown")
        logger.warning(f"Handling failure for {entity_name}")

        state["current_step"] = "failure_handling"
        state["retry_count"] = state.get("retry_count", 0) + 1

        # Record failure in circuit breaker
        self.circuit_breaker.record_failure()

        # Update state with circuit breaker information
        state["circuit_breaker_state"] = self.circuit_breaker.get_state()

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
        """Determine if we should retry or escalate based on retry count and circuit breaker."""
        retry_count = state.get("retry_count", 0)
        max_retries = (
            state.get("active_task", {}).get("max_retries", 3)
            if state.get("active_task")
            else 3
        )

        # Check circuit breaker first
        if self.circuit_breaker.should_break():
            logger.warning("Circuit breaker tripped - escalating to human")
            return "escalate"

        if retry_count < max_retries:
            return "retry"

        # Record failure in circuit breaker when max retries reached
        self.circuit_breaker.record_failure()
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
