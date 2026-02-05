"""Core interfaces and protocols for the agent system."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Represents a chat message."""
    role: str
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None


class ChatModelAdapter(ABC):
    """
    Abstract interface for chat model adapters.
    
    All LLM interactions go through this adapter layer.
    LangChain is used internally but not exposed at system boundaries.
    """
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> ChatMessage:
        """
        Generate a response from the chat model.
        
        Args:
            prompt: Input prompt
            **kwargs: Additional model-specific parameters
            
        Returns:
            ChatMessage with response
        """
        pass
    
    @abstractmethod
    async def generate_with_tools(
        self,
        prompt: str,
        tools: List["Tool"],
        **kwargs
    ) -> ChatMessage:
        """
        Generate a response with tool calling capability.
        
        Args:
            prompt: Input prompt
            tools: Available tools
            **kwargs: Additional model-specific parameters
            
        Returns:
            ChatMessage with potential tool calls
        """
        pass


class MemoryProvider(ABC):
    """
    Abstract interface for memory providers.
    
    Agent-scoped memory controlling what context is available.
    Memory is isolated per agent unless explicitly shared.
    """
    
    @abstractmethod
    async def load(self) -> List[Dict[str, Any]]:
        """Load memory context."""
        pass
    
    @abstractmethod
    async def persist(self, data: List[Dict[str, Any]]) -> None:
        """Persist data to memory."""
        pass
    
    @abstractmethod
    async def clear(self) -> None:
        """Clear all memory."""
        pass


class Tool(ABC):
    """
    Abstract base class for agent tools.
    
    Tools represent capabilities, not raw API calls.
    Characteristics:
    - Narrow and well-defined
    - Schema-validated with Pydantic
    - Explicitly declared per agent
    """
    
    name: str
    description: str
    input_schema: type[BaseModel]
    
    @abstractmethod
    async def execute(self, arguments: Dict[str, Any]) -> Any:
        """
        Execute the tool with given arguments.
        
        Args:
            arguments: Tool input arguments
            
        Returns:
            Tool execution result
        """
        pass
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the JSON schema for this tool."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema.model_json_schema()
        }
