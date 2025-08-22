"""
Graph State definitions for the Centurion migration system with Pydantic models for type safety.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Task(BaseModel):
    """Represents a migration task with proper typing."""
    task_id: str
    entity_name: str
    source_files: List[str]
    status: str = "pending"  # pending, in_progress, completed, escalated
    requires_human_approval: bool = False
    max_retries: int = 3
    dependencies: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    escalated_at: Optional[datetime] = None


class AnalysisReport(BaseModel):
    """Structured analysis report from Codebase Analyst."""
    entity_name: str
    source_files: List[str]
    dependencies: List[str]
    components: Dict[str, Any]
    complexity_score: float
    migration_priority: int


class ValidationResult(BaseModel):
    """Structured validation results with quality metrics."""
    syntax_valid: bool
    style_compliant: bool
    test_coverage: float
    test_count: int
    passed_tests: int
    failed_tests: int
    quality_score: float
    security_issues: List[str] = Field(default_factory=list)
    performance_concerns: List[str] = Field(default_factory=list)


class HumanInterventionRequest(BaseModel):
    """Structured data for human-in-the-loop requests."""
    task_id: str
    entity_name: str
    request_type: str  # approval, escalation, review
    reason: str
    generated_code: Optional[str] = None
    test_results: Optional[Dict[str, Any]] = None
    validation_result: Optional[Dict[str, Any]] = None
    requested_at: datetime = Field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    resolution: Optional[str] = None  # approved, rejected, modified


class CircuitBreakerState(BaseModel):
    """Circuit breaker state for failure management."""
    state: str  # closed, open, half-open
    failure_count: int
    last_failure_time: Optional[datetime] = None
    max_failures: int = 5
    reset_timeout: int = 600  # seconds


class CenturionGraphState(BaseModel):
    """
    Master state schema for the LangGraph-based Centurion migration system.
    This state serves as the "single source of truth" for the entire workflow.
    Uses Pydantic for type safety and validation.
    """

    # Task queue management
    task_queue: List[Task] = Field(default_factory=list)
    active_task: Optional[Task] = None

    # Code analysis and content
    source_code_content: Dict[str, str] = Field(default_factory=dict)
    analysis_report: Optional[AnalysisReport] = None

    # Code generation
    generated_gdscript: Optional[str] = None

    # Validation and testing
    validation_result: Optional[ValidationResult] = None
    test_results: Optional[Dict[str, Any]] = None

    # Error handling and retry logic
    retry_count: int = 0
    last_error: Optional[str] = None
    error_logs: List[Dict[str, Any]] = Field(default_factory=list)

    # Human-in-the-loop integration
    human_intervention_request: Optional[HumanInterventionRequest] = None
    human_review_status: str = "pending"  # pending, approved, rejected, needs_review

    # Workflow tracking
    target_files: List[str] = Field(default_factory=list)
    status: str = "idle"  # idle, in_progress, completed, failed, escalated
    current_step: str = "initialized"

    # Quality metrics and validation
    test_coverage: float = 0.0
    quality_score: float = 0.0
    security_scan_results: Dict[str, Any] = Field(default_factory=dict)

    # Circuit breaker and failure management
    circuit_breaker_state: CircuitBreakerState = Field(
        default_factory=lambda: CircuitBreakerState(
            state="closed", failure_count=0, max_failures=5, reset_timeout=600
        )
    )

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True


# Backward compatibility alias
MigrationState = CenturionGraphState
