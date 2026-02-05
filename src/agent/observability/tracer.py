"""Execution tracing for debugging and analysis."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel


class TraceEvent(BaseModel):
    """A single trace event."""
    timestamp: datetime
    event_type: str
    agent_name: str
    details: Dict[str, Any]
    iteration: int


class ExecutionTracer:
    """
    Traces agent execution for debugging and analysis.
    
    Captures:
    - Prompts sent to LLM
    - LLM responses
    - Tool calls and results
    - Memory operations
    - Decision points
    """
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self._traces: List[TraceEvent] = []
    
    def trace(
        self,
        event_type: str,
        agent_name: str,
        details: Dict[str, Any],
        iteration: int = 0
    ) -> None:
        """Record a trace event."""
        if not self.enabled:
            return
        
        event = TraceEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            agent_name=agent_name,
            details=details,
            iteration=iteration
        )
        self._traces.append(event)
    
    def get_traces(
        self,
        agent_name: Optional[str] = None,
        event_type: Optional[str] = None
    ) -> List[TraceEvent]:
        """Get recorded traces, optionally filtered."""
        traces = self._traces
        
        if agent_name:
            traces = [t for t in traces if t.agent_name == agent_name]
        
        if event_type:
            traces = [t for t in traces if t.event_type == event_type]
        
        return traces
    
    def clear(self) -> None:
        """Clear all traces."""
        self._traces.clear()
    
    def export(self) -> List[Dict[str, Any]]:
        """Export traces as JSON-serializable list."""
        return [trace.model_dump() for trace in self._traces]


# Global tracer
_global_tracer = ExecutionTracer()


def get_global_tracer() -> ExecutionTracer:
    """Get the global execution tracer."""
    return _global_tracer
