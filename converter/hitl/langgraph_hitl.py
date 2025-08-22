"""
LangGraph-based Human-in-the-Loop Integration

This module implements proactive HITL patterns using LangGraph's native interrupt capabilities,
specifically the "Interrupt & Resume" and "Human-as-a-Tool" patterns following official
LangGraph documentation patterns.
"""

import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union

from langgraph.types import Command, interrupt

# Configure logging
logger = logging.getLogger(__name__)


class HITLPattern(Enum):
    """Enumeration of HITL patterns."""

    INTERRUPT_AND_RESUME = "interrupt_and_resume"
    HUMAN_AS_A_TOOL = "human_as_a_tool"


class HITLRequestType(Enum):
    """Enumeration of HITLPattern request types."""

    APPROVAL = "approval"
    EXPERTISE = "expertise"
    CLARIFICATION = "clarification"
    VERIFICATION = "verification"


@dataclass
class HITLRequest:
    """Representation of a HITL request compatible with LangGraph."""

    request_id: str
    request_type: HITLRequestType
    pattern: HITLPattern
    entity_id: str
    description: str
    context: Dict[str, Any] = field(default_factory=dict)
    priority: int = 1
    created_at: float = field(default_factory=time.time)
    response: Optional[Dict[str, Any]] = None
    responded_at: Optional[float] = None


class LangGraphHITLIntegration:
    """
    LangGraph-based HITL integration implementing proactive patterns.

    This class implements the "Interrupt & Resume" and "Human-as-a-Tool" patterns
    using LangGraph's native interrupt capabilities as recommended in the architectural document.
    """

    def __init__(self):
        """Initialize the LangGraph-based HITL integration."""
        self.requests: Dict[str, HITLRequest] = {}
        logger.info("LangGraph HITL Integration initialized")

    def interrupt_and_resume(
        self,
        entity_id: str,
        description: str,
        context: Dict[str, Any],
        requires_approval: bool = True,
    ) -> Union[Command, Dict[str, Any]]:
        """
        Implement the "Interrupt & Resume" pattern for critical path validation.

        This method is designed to be called from within a LangGraph node. It will:
        1. Create a HITL request for human approval
        2. Call interrupt() to pause graph execution
        3. Wait for human response
        4. Return Command(resume=True/False) to resume execution

        Args:
            entity_id: ID of the entity being processed
            description: Description of what needs approval
            context: Context information for the human reviewer
            requires_approval: Whether approval is required (True) or just notification (False)

        Returns:
            Either a Command to resume execution or context data for human review
        """
        request_id = f"iar_{entity_id}_{int(time.time())}"

        # Create the HITL request
        request = HITLRequest(
            request_id=request_id,
            request_type=HITLRequestType.APPROVAL,
            pattern=HITLPattern.INTERRUPT_AND_RESUME,
            entity_id=entity_id,
            description=description,
            context=context,
            priority=10,  # High priority
        )

        # Store the request
        self.requests[request_id] = request

        # Log the request
        logger.info(f"Interrupt & Resume request created: {request_id} for {entity_id}")

        # If approval is not required, just log and continue
        if not requires_approval:
            logger.info(
                f"Notification-only request for {entity_id}, continuing without interrupt"
            )
            return {"status": "notified", "request_id": request_id}

        # Call interrupt() to pause execution and wait for human input
        interrupt_payload = {
            "request_id": request_id,
            "entity_id": entity_id,
            "description": description,
            "context": context,
            "request_type": "approval",
            "pattern": "interrupt_and_resume",
        }

        # Use LangGraph's native interrupt function
        human_response = interrupt(interrupt_payload)

        # Process the human response and return appropriate Command
        if human_response.get("approved", False):
            return Command(resume=True, update={"human_approval": "approved"})
        else:
            return Command(resume=False, update={"human_approval": "rejected"})

    def human_as_tool(
        self,
        entity_id: str,
        description: str,
        context: Dict[str, Any],
        confidence_threshold: float = 0.8,
    ) -> Union[Command, Dict[str, Any]]:
        """
        Implement the "Human-as-a-Tool" pattern for ambiguity resolution.

        This method is designed to be called from within a LangGraph node. It will:
        1. Assess confidence in automated processing
        2. If confidence is low, create a HITL request for human expertise
        3. Call interrupt() to pause graph execution
        4. Wait for human response with expert knowledge
        5. Return Command(resume={'resolved_logic': '...'}) to resume with expert data

        Args:
            entity_id: ID of the entity being processed
            description: Description of what expertise is needed
            context: Context information including confidence score and ambiguous data
            confidence_threshold: Threshold below which human expertise is requested

        Returns:
            Either a Command with expert data or context data for human review
        """
        request_id = f"hat_{entity_id}_{int(time.time())}"

        # Extract confidence from context
        confidence = context.get("confidence_score", 1.0)

        # If confidence is high enough, continue without human intervention
        if confidence >= confidence_threshold:
            logger.info(
                f"Confidence {confidence:.2f} above threshold {confidence_threshold}, proceeding automatically"
            )
            return {"status": "proceed", "confidence": confidence}

        # Create the HITL request
        request = HITLRequest(
            request_id=request_id,
            request_type=HITLRequestType.EXPERTISE,
            pattern=HITLPattern.HUMAN_AS_A_TOOL,
            entity_id=entity_id,
            description=description,
            context=context,
            priority=7,  # Medium-high priority
        )

        # Store the request
        self.requests[request_id] = request

        # Log the request
        logger.info(
            f"Human-as-a-Tool request created: {request_id} for {entity_id} (confidence: {confidence:.2f})"
        )

        # Call interrupt() to pause execution and request human expertise
        interrupt_payload = {
            "request_id": request_id,
            "entity_id": entity_id,
            "description": description,
            "context": context,
            "confidence_score": confidence,
            "request_type": "expertise",
            "pattern": "human_as_a_tool",
        }

        # Use LangGraph's native interrupt function
        expert_response = interrupt(interrupt_payload)

        # Return Command with expert-provided data to resume execution
        return Command(
            resume=True,
            update={
                "expert_resolution": expert_response.get("resolution", {}),
                "confidence_boosted": True,
                "human_expertise_applied": True,
            },
        )

    def handle_human_response(
        self, request_id: str, response_data: Dict[str, Any]
    ) -> bool:
        """
        Handle a response from a human reviewer.

        Args:
            request_id: ID of the request being responded to
            response_data: Data provided by the human reviewer

        Returns:
            True if response was accepted, False otherwise
        """
        if request_id not in self.requests:
            logger.warning(f"HITL request {request_id} not found")
            return False

        # Update the request with response
        request = self.requests[request_id]
        request.response = response_data
        request.responded_at = time.time()

        logger.info(f"HITL request {request_id} resolved by human")
        return True

    def get_request_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a specific HITL request.

        Args:
            request_id: ID of the request to check

        Returns:
            Dictionary with request status or None if not found
        """
        if request_id not in self.requests:
            return None

        request = self.requests[request_id]
        return {
            "request_id": request.request_id,
            "entity_id": request.entity_id,
            "request_type": request.request_type.value,
            "pattern": request.pattern.value,
            "description": request.description,
            "status": "resolved" if request.response else "pending",
            "created_at": request.created_at,
            "responded_at": request.responded_at,
            "response": request.response,
        }

    def get_pending_requests(self) -> List[Dict[str, Any]]:
        """
        Get all pending HITL requests.

        Returns:
            List of pending requests
        """
        return [
            {
                "request_id": req.request_id,
                "entity_id": req.entity_id,
                "request_type": req.request_type.value,
                "pattern": req.pattern.value,
                "description": req.description,
                "priority": req.priority,
                "created_at": req.created_at,
            }
            for req in self.requests.values()
            if not req.response
        ]


def main():
    """Main function for testing the LangGraphHITLIntegration."""
    # Create HITL integration
    hitl = LangGraphHITLIntegration()

    # Test Interrupt & Resume pattern
    print("Testing Interrupt & Resume pattern:")
    result = hitl.interrupt_and_resume(
        entity_id="SHIP-GTC_FENRIS",
        description="Migration of critical core dependency",
        context={
            "files": ["source/tables/ships.tbl", "source/models/fenris.pof"],
            "risk_level": "high",
            "generated_code": "class_name GTCFenris\nextends Node3D\n# ... code here",
        },
    )
    print("Interrupt & Resume result type:", type(result).__name__)
    if hasattr(result, "resume"):
        print("Command resume:", result.resume)
        print("Command update:", getattr(result, "update", {}))

    # Test Human-as-a-Tool pattern with high confidence
    print("\nTesting Human-as-a-Tool pattern (high confidence):")
    result = hitl.human_as_tool(
        entity_id="WEAPON-BEAM_TURRET",
        description="Ambiguous SEXP command in mission script",
        context={
            "command": "(ai-evade-beam-turret #self)",
            "file": "source/missions/main.fs2",
            "confidence_score": 0.9,
        },
    )
    print("Human-as-a-Tool result (high confidence):", result)

    # Test Human-as-a-Tool pattern with low confidence
    print("\nTesting Human-as-a-Tool pattern (low confidence):")
    result = hitl.human_as_tool(
        entity_id="WEAPON-BEAM_TURRET",
        description="Ambiguous SEXP command in mission script",
        context={
            "command": "(ai-evade-beam-turret #self)",
            "file": "source/missions/main.fs2",
            "confidence_score": 0.3,
        },
    )
    print("Human-as-a-Tool result type (low confidence):", type(result).__name__)
    if hasattr(result, "resume"):
        print("Command resume:", result.resume)
        print("Command update:", getattr(result, "update", {}))

    # Test getting pending requests
    print("\nPending requests:", hitl.get_pending_requests())


if __name__ == "__main__":
    main()
