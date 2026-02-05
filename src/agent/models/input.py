"""Base input schemas for agents."""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class BaseInput(BaseModel):
    """
    Base class for all agent inputs.
    
    Agents define their own input schemas by inheriting from this class.
    Structured, validated input using Pydantic.
    """
    
    request_id: Optional[str] = Field(
        default=None,
        description="Unique identifier for this request"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata for the request"
    )


class ChatInput(BaseInput):
    """Input for chat-based agents."""
    
    message: str = Field(description="User message")
    conversation_id: Optional[str] = Field(
        default=None,
        description="Conversation identifier for multi-turn chats"
    )


class TaskInput(BaseInput):
    """Input for task-based agents."""
    
    task: str = Field(description="Task description")
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Task-specific parameters"
    )


class QueryInput(BaseInput):
    """Input for query-based agents (e.g., financial data)."""
    
    query: str = Field(description="Query string")
    filters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Query filters"
    )
    limit: Optional[int] = Field(
        default=10,
        description="Maximum number of results"
    )
