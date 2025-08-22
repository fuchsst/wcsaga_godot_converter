"""
LangGraph Orchestrator Implementation

This module implements the main orchestrator using LangGraph for deterministic state management
and replaces the CrewAI-based orchestrator with a more robust, stateful approach.
"""

import asyncio
import logging
import json
from typing import Dict, Any, List, Optional, TypedDict
from pathlib import Path
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from ..utils import setup_logging, generate_timestamp
from ..graph_system.graph_manager import GraphManager
from ..validation.test_quality_gate import TestQualityGate
from ..hitl.hitl_integration import HITLIntegration
from ..analyst.codebase_analyst import CodebaseAnalyst
from ..refactoring.refactoring_specialist import RefactoringSpecialist
from ..test_generator.test_generator import TestGenerator
from ..validation.validation_engineer import ValidationEngineer

# Configure logging
logger = setup_logging(__name__)


class MigrationState(TypedDict, total=False):
    """State class for LangGraph migration workflow with proper type definitions."""
    task_id: str
    entity_name: str
    source_files: List[str]
    target_files: List[str]
    analysis_result: Optional[Dict[str, Any]]
    refactored_code: Optional[str]
    test_results: Optional[Dict[str, Any]]
    validation_results: Optional[Dict[str, Any]]
    error_logs: List[Dict[str, Any]]
    retry_count: int
    max_retries: int
    status: str
    current_step: str
    quality_gate_passed: bool
    requires_human_review: bool
    human_review_result: Optional[Dict[str, Any]]


class LangGraphOrchestrator:
    """Main orchestrator using LangGraph for deterministic state management."""
    
    def __init__(self, source_path: str, target_path: str, 
                 graph_file: str = "dependency_graph.json"):
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
        self.hitl_integration = HITLIntegration()
        
        # Build the LangGraph workflow
        self.workflow = self._build_workflow()
        
        logger.info("LangGraph Orchestrator initialized")
    
    def _build_workflow(self):
        """Build the LangGraph workflow for migration."""
        builder = StateGraph(MigrationState)
        
        # Define nodes
        builder.add_node("initialize_bolt", self._initialize_bolt)
        builder.add_node("analyze_code", self._analyze_code)
        builder.add_node("refactor_code", self._refactor_code)
        builder.add_node("generate_tests", self._generate_tests)
        builder.add_node("validate_tests", self._validate_tests)
        builder.add_node("check_quality_gate", self._check_quality_gate)
        builder.add_node("complete_bolt", self._complete_bolt)
        builder.add_node("handle_failure", self._handle_failure)
        builder.add_node("escalate_to_human", self._escalate_to_human)
        
        # Define edges
        builder.set_entry_point("initialize_bolt")
        
        builder.add_edge("initialize_bolt", "analyze_code")
        builder.add_conditional_edges(
            "analyze_code",
            self._should_continue_after_analysis,
            {"continue": "refactor_code", "fail": "handle_failure"}
        )
        builder.add_conditional_edges(
            "refactor_code",
            self._should_continue_after_refactoring,
            {"continue": "generate_tests", "fail": "handle_failure"}
        )
        builder.add_conditional_edges(
            "generate_tests",
            self._should_continue_after_test_generation,
            {"continue": "validate_tests", "fail": "handle_failure"}
        )
        builder.add_conditional_edges(
            "validate_tests",
            self._should_continue_after_validation,
            {"continue": "check_quality_gate", "fail": "handle_failure"}
        )
        builder.add_conditional_edges(
            "check_quality_gate",
            self._should_complete_bolt,
            {"complete": "complete_bolt", "fail": "handle_failure"}
        )
        builder.add_conditional_edges(
            "handle_failure",
            self._should_retry_or_escalate,
            {"retry": "analyze_code", "escalate": "escalate_to_human"}
        )
        builder.add_edge("complete_bolt", END)
        builder.add_edge("escalate_to_human", END)
        
        return builder.compile()
    
    async def _initialize_bolt(self, state: MigrationState) -> MigrationState:
        """Initialize a new bolt execution."""
        logger.info(f"Initializing bolt for task {state.task_id}")
        state.status = "in_progress"
        state.current_step = "initialization"
        return state
    
    async def _analyze_code(self, state: MigrationState) -> MigrationState:
        """Analyze the source code using CodebaseAnalyst."""
        logger.info(f"Analyzing code for {state.entity_name}")
        state.current_step = "analysis"
        
        try:
            # Initialize Codebase Analyst
            analyst = CodebaseAnalyst()
            
            # Perform actual analysis
            analysis_result = analyst.analyze_entity(
                state.entity_name, 
                state.source_files
            )
            
            state.analysis_result = analysis_result
            
            # Determine target files based on analysis
            state.target_files = self._determine_target_files(
                state.entity_name, 
                analysis_result
            )
            
        except Exception as e:
            logger.error(f"Analysis failed for {state.entity_name}: {str(e)}")
            state.error_logs.append({
                "step": "analysis",
                "error": str(e),
                "entity": state.entity_name
            })
        
        return state
    
    def _determine_target_files(self, entity_name: str, analysis_result: Dict[str, Any]) -> List[str]:
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
    
    async def _refactor_code(self, state: MigrationState) -> MigrationState:
        """Refactor the code to GDScript using RefactoringSpecialist."""
        logger.info(f"Refactoring code for {state.entity_name}")
        state.current_step = "refactoring"
        
        try:
            # Initialize Refactoring Specialist
            refactoring_specialist = RefactoringSpecialist()
            
            # Perform actual refactoring
            # Note: This would need to be implemented based on the RefactoringSpecialist class
            # For now, we'll simulate the refactoring process
            refactored_code = refactoring_specialist.refactor_entity(
                state.entity_name,
                state.source_files,
                state.analysis_result
            )
            
            state.refactored_code = refactored_code
            
        except Exception as e:
            logger.error(f"Refactoring failed for {state.entity_name}: {str(e)}")
            state.error_logs.append({
                "step": "refactoring",
                "error": str(e),
                "entity": state.entity_name
            })
        
        return state
    
    async def _generate_tests(self, state: MigrationState) -> MigrationState:
        """Generate tests for the refactored code using TestGenerator."""
        logger.info(f"Generating tests for {state.entity_name}")
        state.current_step = "test_generation"
        
        try:
            # Initialize Test Generator
            test_generator = TestGenerator()
            
            # Generate tests based on the refactored code and analysis
            test_results = test_generator.generate_tests(
                state.entity_name,
                state.refactored_code,
                state.analysis_result
            )
            
            state.test_results = test_results
            
        except Exception as e:
            logger.error(f"Test generation failed for {state.entity_name}: {str(e)}")
            state.error_logs.append({
                "step": "test_generation",
                "error": str(e),
                "entity": state.entity_name
            })
        
        return state
    
    async def _validate_tests(self, state: MigrationState) -> MigrationState:
        """Validate the generated tests using ValidationEngineer."""
        logger.info(f"Validating tests for {state.entity_name}")
        state.current_step = "validation"
        
        try:
            # Initialize Validation Engineer
            validation_engineer = ValidationEngineer()
            
            # Validate the generated tests
            validation_results = validation_engineer.validate_tests(
                state.entity_name,
                state.refactored_code,
                state.test_results
            )
            
            state.validation_results = validation_results
            
            # Check if validation passed
            if validation_results.get("syntax_valid", False) and validation_results.get("style_compliant", False):
                state.quality_gate_passed = True
            else:
                state.quality_gate_passed = False
                state.error_logs.append({
                    "step": "validation",
                    "error": "Tests failed validation",
                    "details": validation_results
                })
            
        except Exception as e:
            logger.error(f"Validation failed for {state.entity_name}: {str(e)}")
            state.error_logs.append({
                "step": "validation",
                "error": str(e),
                "entity": state.entity_name
            })
        
        return state
    
    async def _check_quality_gate(self, state: MigrationState) -> MigrationState:
        """Check if tests pass the quality gate."""
        logger.info(f"Checking quality gate for {state.entity_name}")
        state.current_step = "quality_check"
        
        # Use the test quality gate
        quality_result = self.quality_gate.validate_test_quality(state.test_results)
        
        if not quality_result["passed"]:
            state.error_logs.append({
                "step": "quality_gate",
                "error": "Tests failed quality gate",
                "details": quality_result
            })
        
        return state
    
    async def _complete_bolt(self, state: MigrationState) -> MigrationState:
        """Complete the bolt execution."""
        logger.info(f"Completing bolt for {state.entity_name}")
        state.status = "completed"
        state.current_step = "completed"
        
        # Update dependency graph
        self.graph_manager.add_entity(state.task_id, "migrated_entity", {
            "name": state.entity_name,
            "status": "completed",
            "target_files": state.target_files
        })
        
        return state
    
    async def _handle_failure(self, state: MigrationState) -> MigrationState:
        """Handle bolt execution failure."""
        logger.warning(f"Handling failure for {state.entity_name}")
        state.status = "failed"
        state.retry_count += 1
        
        return state
    
    async def _escalate_to_human(self, state: MigrationState) -> MigrationState:
        """Escalate to human review."""
        logger.error(f"Escalating {state.entity_name} to human review")
        state.status = "escalated"
        
        # Request human review
        self.hitl_integration.request_verification(
            state.task_id,
            f"Migration escalation for {state.entity_name}",
            {
                "error_logs": state.error_logs,
                "retry_count": state.retry_count
            }
        )
        
        return state
    
    def _should_continue_after_analysis(self, state: MigrationState) -> str:
        """Determine if we should continue after analysis."""
        if state.analysis_result and state.target_files:
            return "continue"
        return "fail"
    
    def _should_continue_after_refactoring(self, state: MigrationState) -> str:
        """Determine if we should continue after refactoring."""
        if state.refactored_code:
            return "continue"
        return "fail"
    
    def _should_continue_after_test_generation(self, state: MigrationState) -> str:
        """Determine if we should continue after test generation."""
        if state.test_results and state.test_results.get("total", 0) > 0:
            return "continue"
        return "fail"
    
    def _should_continue_after_validation(self, state: MigrationState) -> str:
        """Determine if we should continue after validation."""
        if state.validation_results and state.validation_results.get("syntax_valid", False):
            return "continue"
        return "fail"
    
    def _should_complete_bolt(self, state: MigrationState) -> str:
        """Determine if we should complete the bolt."""
        # Check if quality gate passed
        quality_result = self.quality_gate.validate_test_quality(state.test_results)
        if quality_result["passed"]:
            return "complete"
        
        # Add quality failure to error logs
        state.error_logs.append({
            "step": "quality_gate",
            "error": "Tests failed quality gate",
            "details": quality_result
        })
        return "fail"
    
    def _should_retry_or_escalate(self, state: MigrationState) -> str:
        """Determine if we should retry or escalate."""
        if state.retry_count < state.max_retries:
            return "retry"
        return "escalate"
    
    async def execute_bolt(self, task_id: str, entity_name: str, source_files: List[str]) -> Dict[str, Any]:
        """Execute a complete bolt cycle."""
        logger.info(f"Executing bolt for task {task_id}: {entity_name}")
        
        # Initialize state
        initial_state = MigrationState()
        initial_state.task_id = task_id
        initial_state.entity_name = entity_name
        initial_state.source_files = source_files
        
        try:
            # Execute the workflow
            final_state = await self.workflow.ainvoke(initial_state)
            
            return {
                "success": final_state.status == "completed",
                "task_id": task_id,
                "entity_name": entity_name,
                "status": final_state.status,
                "retry_count": final_state.retry_count,
                "error_count": len(final_state.error_logs),
                "analysis_result": final_state.analysis_result,
                "refactored_code": final_state.refactored_code,
                "test_results": final_state.test_results,
                "validation_results": final_state.validation_results
            }
            
        except Exception as e:
            logger.error(f"Error executing bolt for task {task_id}: {str(e)}")
            return {
                "success": False,
                "task_id": task_id,
                "entity_name": entity_name,
                "error": str(e),
                "status": "failed"
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the orchestrator."""
        return {
            "source_path": str(self.source_path),
            "target_path": str(self.target_path),
            "graph_entities": self.graph_manager.get_statistics().get("node_count", 0),
            "graph_dependencies": self.graph_manager.get_statistics().get("edge_count", 0),
            "last_updated": generate_timestamp()
        }


def main():
    """Main function for testing the LangGraphOrchestrator."""
    # Create orchestrator
    orchestrator = LangGraphOrchestrator(
        source_path="../source",
        target_path="../target",
        graph_file="test_dependency_graph.json"
    )
    
    # Print initial status
    print("Initial status:", orchestrator.get_status())
    
    # Execute a bolt
    result = asyncio.run(orchestrator.execute_bolt(
        task_id="SHIP-GTC_FENRIS",
        entity_name="GTC Fenris",
        source_files=["source/tables/ships.tbl", "source/models/fenris.pof"]
    ))
    
    # Print final status
    print("Final status:", orchestrator.get_status())
    print("Bolt result:", result)


if __name__ == "__main__":
    main()
