"""Audit logging for agent actions."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel


class AuditEvent(BaseModel):
    """An audit log event."""
    timestamp: datetime
    agent_name: str
    event_type: str
    user_id: Optional[str] = None
    details: Dict[str, Any]
    success: bool


class AuditLogger:
    """
    Centralized audit logging for agent system.
    
    Logs all significant actions:
    - Agent executions
    - Tool calls
    - Permission checks
    - Approval decisions
    - Errors and failures
    """
    
    def __init__(self, log_file: Optional[str] = None):
        self.log_file = log_file
        self._events: List[AuditEvent] = []
    
    def log_event(
        self,
        agent_name: str,
        event_type: str,
        details: Dict[str, Any],
        success: bool = True,
        user_id: Optional[str] = None
    ) -> None:
        """Log an audit event."""
        event = AuditEvent(
            timestamp=datetime.now(),
            agent_name=agent_name,
            event_type=event_type,
            user_id=user_id,
            details=details,
            success=success
        )
        
        self._events.append(event)
        
        # Write to file if configured
        if self.log_file:
            self._write_to_file(event)
    
    def log_agent_run(
        self,
        agent_name: str,
        input_data: Dict[str, Any],
        output: Dict[str, Any],
        success: bool
    ) -> None:
        """Log an agent execution."""
        self.log_event(
            agent_name=agent_name,
            event_type="agent_execution",
            details={
                "input": input_data,
                "output": output
            },
            success=success
        )
    
    def log_tool_call(
        self,
        agent_name: str,
        tool_name: str,
        arguments: Dict[str, Any],
        result: Any,
        success: bool
    ) -> None:
        """Log a tool execution."""
        self.log_event(
            agent_name=agent_name,
            event_type="tool_execution",
            details={
                "tool": tool_name,
                "arguments": arguments,
                "result": result
            },
            success=success
        )
    
    def log_approval(
        self,
        agent_name: str,
        tool_name: str,
        approved: bool,
        approver: str
    ) -> None:
        """Log an approval decision."""
        self.log_event(
            agent_name=agent_name,
            event_type="approval_decision",
            details={
                "tool": tool_name,
                "approved": approved,
                "approver": approver
            },
            success=True
        )
    
    def get_events(
        self,
        agent_name: Optional[str] = None,
        event_type: Optional[str] = None
    ) -> List[AuditEvent]:
        """Get audit events, optionally filtered."""
        events = self._events
        
        if agent_name:
            events = [e for e in events if e.agent_name == agent_name]
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        return events
    
    def _write_to_file(self, event: AuditEvent) -> None:
        """Write event to log file."""
        # TODO: Implement file writing
        pass


# Global audit logger
_global_audit_logger = AuditLogger()


def get_global_audit_logger() -> AuditLogger:
    """Get the global audit logger."""
    return _global_audit_logger
