"""Execution flow and loop control logic."""

from typing import Any, Callable, Optional
from enum import Enum

from pydantic import BaseModel


class ExecutionStatus(Enum):
    """Status of agent execution."""
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    MAX_ITERATIONS = "max_iterations"
    STOPPED = "stopped"


class ExecutionContext(BaseModel):
    """Context for a single agent execution."""
    iteration: int = 0
    status: ExecutionStatus = ExecutionStatus.RUNNING
    messages: list[dict[str, Any]] = []
    tool_calls: list[dict[str, Any]] = []
    metadata: dict[str, Any] = {}
    
    class Config:
        arbitrary_types_allowed = True


class StopCondition:
    """Defines a condition that should stop agent execution."""
    
    def __init__(self, name: str, condition: Callable[[ExecutionContext], bool]):
        self.name = name
        self.condition = condition
    
    def should_stop(self, context: ExecutionContext) -> bool:
        """Check if the stop condition is met."""
        return self.condition(context)


class ExecutionController:
    """Controls the execution flow and loop management."""
    
    def __init__(self, max_iterations: int = 10):
        self.max_iterations = max_iterations
        self.stop_conditions: list[StopCondition] = []
    
    def add_stop_condition(self, condition: StopCondition) -> None:
        """Add a stop condition to the controller."""
        self.stop_conditions.append(condition)
    
    def should_continue(self, context: ExecutionContext) -> bool:
        """Determine if execution should continue."""
        # Check max iterations
        if context.iteration >= self.max_iterations:
            context.status = ExecutionStatus.MAX_ITERATIONS
            return False
        
        # Check custom stop conditions
        for condition in self.stop_conditions:
            if condition.should_stop(context):
                context.status = ExecutionStatus.STOPPED
                context.metadata["stop_reason"] = condition.name
                return False
        
        # Check if already completed or failed
        if context.status in [ExecutionStatus.COMPLETED, ExecutionStatus.FAILED]:
            return False
        
        return True
