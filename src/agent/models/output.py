"""Base output schemas for agents."""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class BaseOutput(BaseModel):
    """
    Base class for all agent outputs.
    
    Provides a consistent output format across all agents.
    """
    
    content: str = Field(description="Main output content")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional output metadata"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Output generation timestamp"
    )
    success: bool = Field(default=True, description="Whether execution was successful")
    error: Optional[str] = Field(default=None, description="Error message if failed")


class ChatOutput(BaseOutput):
    """Output for chat-based agents."""
    
    message: str = Field(description="Agent response message")
    conversation_id: Optional[str] = Field(
        default=None,
        description="Conversation identifier"
    )


class TaskOutput(BaseOutput):
    """Output for task-based agents."""
    
    result: Dict[str, Any] = Field(description="Task execution result")
    status: str = Field(default="completed", description="Task status")


class QueryOutput(BaseOutput):
    """Output for query-based agents."""
    
    results: list[Dict[str, Any]] = Field(
        default_factory=list,
        description="Query results"
    )
    count: int = Field(description="Number of results returned")
