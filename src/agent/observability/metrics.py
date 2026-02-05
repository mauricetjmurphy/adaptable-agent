"""Metrics collection for agent execution."""

from typing import Any, Dict
from collections import defaultdict
from datetime import datetime


class MetricsCollector:
    """
    Collects and tracks metrics for agent execution.
    
    Tracks:
    - Execution times
    - Tool call counts
    - Token usage
    - Success/failure rates
    """
    
    def __init__(self):
        self._metrics: Dict[str, Any] = defaultdict(list)
        self._counters: Dict[str, int] = defaultdict(int)
    
    def record_execution_time(self, agent_name: str, duration: float) -> None:
        """Record agent execution time."""
        self._metrics[f"{agent_name}.execution_time"].append(duration)
    
    def record_tool_call(self, tool_name: str, success: bool) -> None:
        """Record tool call."""
        self._counters[f"tool.{tool_name}.calls"] += 1
        if success:
            self._counters[f"tool.{tool_name}.success"] += 1
        else:
            self._counters[f"tool.{tool_name}.failure"] += 1
    
    def record_token_usage(self, tokens: int) -> None:
        """Record token usage."""
        self._counters["tokens.total"] += tokens
    
    def record_agent_run(self, agent_name: str, success: bool, iterations: int) -> None:
        """Record agent run."""
        self._counters[f"agent.{agent_name}.runs"] += 1
        if success:
            self._counters[f"agent.{agent_name}.success"] += 1
        else:
            self._counters[f"agent.{agent_name}.failure"] += 1
        self._metrics[f"agent.{agent_name}.iterations"].append(iterations)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all collected metrics."""
        return {
            "metrics": dict(self._metrics),
            "counters": dict(self._counters),
            "timestamp": datetime.now().isoformat()
        }
    
    def reset(self) -> None:
        """Reset all metrics."""
        self._metrics.clear()
        self._counters.clear()


# Global metrics collector
_global_collector = MetricsCollector()


def get_global_metrics() -> MetricsCollector:
    """Get the global metrics collector."""
    return _global_collector
