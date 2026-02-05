"""Agent configuration models."""

from typing import Any, List, Type
from pydantic import BaseModel, Field

from agent.core.contracts import ChatModelAdapter, MemoryProvider, Tool


class AgentConfig(BaseModel):
    """
    Configuration for an agent instance.
    
    Agents are created via configuration, not inheritance.
    All agents share the same engine but differ in configuration.
    """
    
    name: str = Field(description="Unique name for this agent")
    description: str = Field(description="Human-readable description of agent purpose")
    
    # Required components (The Agent Contract)
    input_schema: Type[BaseModel] = Field(description="Pydantic model for input validation")
    chat_model: ChatModelAdapter = Field(description="Chat model adapter instance")
    memory: MemoryProvider = Field(description="Memory provider instance")
    tools: List[Tool] = Field(default_factory=list, description="Available tools for this agent")
    
    # Execution control
    max_iterations: int = Field(default=10, description="Maximum execution loop iterations")
    stop_conditions: List[str] = Field(
        default_factory=list,
        description="Conditions that trigger agent stop"
    )
    
    # Metadata
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional agent-specific metadata"
    )
    
    class Config:
        arbitrary_types_allowed = True
