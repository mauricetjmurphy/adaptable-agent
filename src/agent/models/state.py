"""Agent state models."""

from typing import Any, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """
    Represents the state of an agent at a point in time.
    
    Used for state persistence and debugging.
    """
    
    agent_name: str = Field(description="Name of the agent")
    session_id: str = Field(description="Unique session identifier")
    iteration: int = Field(default=0, description="Current iteration number")
    
    # Execution state
    input_data: Dict[str, Any] = Field(description="Original input")
    current_prompt: Optional[str] = Field(default=None, description="Current prompt")
    last_response: Optional[str] = Field(default=None, description="Last model response")
    
    # Memory and tools
    memory_context: list[Dict[str, Any]] = Field(
        default_factory=list,
        description="Current memory context"
    )
    tool_calls: list[Dict[str, Any]] = Field(
        default_factory=list,
        description="History of tool calls"
    )
    
    # Metadata
    started_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def update(self) -> None:
        """Update the timestamp."""
        self.updated_at = datetime.now()
