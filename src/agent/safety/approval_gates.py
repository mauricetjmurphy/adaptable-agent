"""Human approval gates for sensitive operations."""

from typing import Any, Callable, Dict, Optional
from datetime import datetime


class ApprovalRequest:
    """Represents a request for human approval."""
    
    def __init__(
        self,
        request_id: str,
        agent_name: str,
        tool_name: str,
        arguments: Dict[str, Any],
        reason: str
    ):
        self.request_id = request_id
        self.agent_name = agent_name
        self.tool_name = tool_name
        self.arguments = arguments
        self.reason = reason
        self.timestamp = datetime.now()
        self.approved: Optional[bool] = None
        self.approver: Optional[str] = None


class ApprovalGate:
    """
    Manages human approval for sensitive operations.
    
    Provides a mechanism to pause agent execution and
    request human approval before proceeding.
    """
    
    def __init__(self):
        self._pending_approvals: Dict[str, ApprovalRequest] = {}
        self._approval_callback: Optional[Callable] = None
    
    def request_approval(
        self,
        agent_name: str,
        tool_name: str,
        arguments: Dict[str, Any],
        reason: str = "Sensitive operation"
    ) -> ApprovalRequest:
        """Request approval for an operation."""
        request_id = f"{agent_name}_{tool_name}_{datetime.now().timestamp()}"
        
        request = ApprovalRequest(
            request_id=request_id,
            agent_name=agent_name,
            tool_name=tool_name,
            arguments=arguments,
            reason=reason
        )
        
        self._pending_approvals[request_id] = request
        
        # Trigger callback if set
        if self._approval_callback:
            self._approval_callback(request)
        
        return request
    
    def approve(self, request_id: str, approver: str) -> bool:
        """Approve a pending request."""
        if request_id in self._pending_approvals:
            request = self._pending_approvals[request_id]
            request.approved = True
            request.approver = approver
            return True
        return False
    
    def deny(self, request_id: str, approver: str) -> bool:
        """Deny a pending request."""
        if request_id in self._pending_approvals:
            request = self._pending_approvals[request_id]
            request.approved = False
            request.approver = approver
            return True
        return False
    
    def is_approved(self, request_id: str) -> Optional[bool]:
        """Check if a request is approved."""
        if request_id in self._pending_approvals:
            return self._pending_approvals[request_id].approved
        return None
    
    def set_approval_callback(self, callback: Callable) -> None:
        """Set a callback function to be called when approval is requested."""
        self._approval_callback = callback
