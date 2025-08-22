"""
HITL (Human-in-the-Loop) Integration Implementation

This module implements proactive HITL patterns for critical decision points in the migration process.
"""

import time
import logging
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HITLPattern(Enum):
    """Enumeration of HITL patterns."""
    INTERRUPT_AND_RESUME = "interrupt_and_resume"
    HUMAN_AS_A_TOOL = "human_as_a_tool"
    POLICY_BASED_APPROVAL = "policy_based_approval"
    FALLBACK_ESCALATION = "fallback_escalation"


class HITLRequestType(Enum):
    """Enumeration of HITL request types."""
    APPROVAL = "approval"
    EXPERTISE = "expertise"
    CLARIFICATION = "clarification"
    VERIFICATION = "verification"


@dataclass
class HITLRequest:
    """Representation of a HITL request."""
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


class HITLIntegration:
    """Integration point for Human-in-the-Loop collaboration."""
    
    def __init__(self, notification_callback: Optional[Callable[[HITLRequest], None]] = None):
        """
        Initialize the HITL integration.
        
        Args:
            notification_callback: Optional callback for notifying humans of requests
        """
        self.notification_callback = notification_callback
        self.pending_requests = {}
        self.resolved_requests = {}
        
        logger.info("HITL Integration initialized")
    
    def request_interrupt_and_resume(self, entity_id: str, description: str,
                                    context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request human approval before continuing a critical operation.
        
        Args:
            entity_id: ID of the entity being processed
            description: Description of what needs approval
            context: Context information for the human reviewer
            
        Returns:
            Dictionary with approval result
        """
        request = HITLRequest(
            request_id=f"iar_{entity_id}_{int(time.time())}",
            request_type=HITLRequestType.APPROVAL,
            pattern=HITLPattern.INTERRUPT_AND_RESUME,
            entity_id=entity_id,
            description=description,
            context=context,
            priority=10  # High priority
        )
        
        return self._submit_request(request)
    
    def request_human_expertise(self, entity_id: str, description: str,
                               context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request human expertise to resolve ambiguity.
        
        Args:
            entity_id: ID of the entity being processed
            description: Description of what expertise is needed
            context: Context information for the human expert
            
        Returns:
            Dictionary with expert response
        """
        request = HITLRequest(
            request_id=f"hex_{entity_id}_{int(time.time())}",
            request_type=HITLRequestType.EXPERTISE,
            pattern=HITLPattern.HUMAN_AS_A_TOOL,
            entity_id=entity_id,
            description=description,
            context=context,
            priority=5  # Medium priority
        )
        
        return self._submit_request(request)
    
    def request_clarification(self, entity_id: str, description: str,
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request human clarification for ambiguous situations.
        
        Args:
            entity_id: ID of the entity being processed
            description: Description of what needs clarification
            context: Context information for the human reviewer
            
        Returns:
            Dictionary with clarification response
        """
        request = HITLRequest(
            request_id=f"clr_{entity_id}_{int(time.time())}",
            request_type=HITLRequestType.CLARIFICATION,
            pattern=HITLPattern.HUMAN_AS_A_TOOL,
            entity_id=entity_id,
            description=description,
            context=context,
            priority=3  # Lower priority
        )
        
        return self._submit_request(request)
    
    def request_verification(self, entity_id: str, description: str,
                           context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Request human verification of critical results.
        
        Args:
            entity_id: ID of the entity being processed
            description: Description of what needs verification
            context: Context information for the human reviewer
            
        Returns:
            Dictionary with verification result
        """
        request = HITLRequest(
            request_id=f"ver_{entity_id}_{int(time.time())}",
            request_type=HITLRequestType.VERIFICATION,
            pattern=HITLPattern.INTERRUPT_AND_RESUME,
            entity_id=entity_id,
            description=description,
            context=context,
            priority=8  # High priority
        )
        
        return self._submit_request(request)
    
    def _submit_request(self, request: HITLRequest) -> Dict[str, Any]:
        """
        Submit a HITL request.
        
        Args:
            request: HITL request to submit
            
        Returns:
            Dictionary with submission result
        """
        # Store the request
        self.pending_requests[request.request_id] = request
        
        # Notify human (if callback is provided)
        if self.notification_callback:
            try:
                self.notification_callback(request)
            except Exception as e:
                logger.error(f"Error notifying human of HITL request: {str(e)}")
        
        # Log the request
        logger.info(f"HITL request submitted: {request.request_id} ({request.pattern.value})")
        
        # In a real implementation, this would wait for human response
        # For now, we'll simulate a response
        return self._simulate_response(request)
    
    def _simulate_response(self, request: HITLRequest) -> Dict[str, Any]:
        """
        Simulate a human response to a HITL request.
        
        Args:
            request: HITL request
            
        Returns:
            Dictionary with simulated response
        """
        # In a real implementation, this would wait for actual human response
        # For now, we'll simulate an approval/positive response
        
        response = {
            "approved": True,
            "timestamp": time.time(),
            "comments": "Simulated human response - approved for demonstration purposes"
        }
        
        # Update the request with response
        request.response = response
        request.responded_at = response["timestamp"]
        
        # Move from pending to resolved
        self.resolved_requests[request.request_id] = self.pending_requests.pop(request.request_id)
        
        logger.info(f"HITL request resolved: {request.request_id}")
        
        return response
    
    def provide_response(self, request_id: str, response: Dict[str, Any]) -> bool:
        """
        Provide a response to a HITL request.
        
        Args:
            request_id: ID of the request
            response: Response from human
            
        Returns:
            True if response was accepted, False otherwise
        """
        if request_id not in self.pending_requests:
            logger.warning(f"HITL request {request_id} not found or already resolved")
            return False
        
        # Update the request with response
        request = self.pending_requests[request_id]
        request.response = response
        request.responded_at = time.time()
        
        # Move from pending to resolved
        self.resolved_requests[request_id] = self.pending_requests.pop(request_id)
        
        logger.info(f"HITL request resolved by human: {request_id}")
        return True
    
    def get_pending_requests(self) -> List[Dict[str, Any]]:
        """
        Get all pending HITL requests.
        
        Returns:
            List of pending requests
        """
        return [
            {
                "request_id": req.request_id,
                "request_type": req.request_type.value,
                "pattern": req.pattern.value,
                "entity_id": req.entity_id,
                "description": req.description,
                "priority": req.priority,
                "created_at": req.created_at
            }
            for req in self.pending_requests.values()
        ]
    
    def get_resolved_requests(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get recently resolved HITL requests.
        
        Args:
            limit: Maximum number of requests to return
            
        Returns:
            List of resolved requests
        """
        # Get requests sorted by responded time (newest first)
        sorted_requests = sorted(
            self.resolved_requests.values(),
            key=lambda r: r.responded_at or 0,
            reverse=True
        )
        
        return [
            {
                "request_id": req.request_id,
                "request_type": req.request_type.value,
                "pattern": req.pattern.value,
                "entity_id": req.entity_id,
                "description": req.description,
                "response": req.response,
                "responded_at": req.responded_at
            }
            for req in sorted_requests[:limit]
        ]


def main():
    """Main function for testing the HITLIntegration."""
    # Create notification callback
    def notify_human(request: HITLRequest):
        print(f"Notification: {request.request_type.value} request for {request.entity_id}")
        print(f"Description: {request.description}")
        print("---")
    
    # Create HITL integration
    hitl = HITLIntegration(notification_callback=notify_human)
    
    # Test interrupt and resume
    result = hitl.request_interrupt_and_resume(
        entity_id="SHIP-GTC_FENRIS",
        description="Migration of critical core dependency",
        context={
            "files": ["source/tables/ships.tbl", "source/models/fenris.pof"],
            "risk_level": "high"
        }
    )
    print("Interrupt and resume result:", result)
    
    # Test human expertise
    result = hitl.request_human_expertise(
        entity_id="WEAPON-BEAM_TURRET",
        description="Ambiguous SEXP command in mission script",
        context={
            "command": "(ai-evade-beam-turret #self)",
            "file": "source/missions/main.fs2"
        }
    )
    print("Human expertise result:", result)
    
    # Print pending requests
    print("Pending requests:", hitl.get_pending_requests())


if __name__ == "__main__":
    main()