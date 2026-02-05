"""Base agent configuration utilities."""

from typing import List, Type
from pydantic import BaseModel
from agent.core.config import AgentConfig
from agent.core.contracts import ChatModelAdapter, MemoryProvider, Tool


def create_agent_config(
    name: str,
    description: str,
    input_schema: Type[BaseModel],
    chat_model: ChatModelAdapter,
    memory: MemoryProvider,
    tools: List[Tool],
    **kwargs
) -> AgentConfig:
    """
    Create an agent configuration.
    
    Helper function to simplify agent creation.
    
    Args:
        name: Agent name
        description: Agent description
        input_schema: Pydantic input model
        chat_model: Chat model adapter
        memory: Memory provider
        tools: List of tools
        **kwargs: Additional configuration options
        
    Returns:
        AgentConfig instance
    """
    return AgentConfig(
        name=name,
        description=description,
        input_schema=input_schema,
        chat_model=chat_model,
        memory=memory,
        tools=tools,
        **kwargs
    )
