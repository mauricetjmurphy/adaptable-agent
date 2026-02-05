"""Base chat model adapter implementation."""

from typing import Any, Dict, List, Optional
from agent.core.contracts import ChatModelAdapter, ChatMessage, Tool


class BaseChatAdapter(ChatModelAdapter):
    """
    Base implementation of ChatModelAdapter.
    
    Provides common functionality for all adapters.
    """
    
    def __init__(
        self,
        model_name: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.extra_params = kwargs
    
    async def generate(self, prompt: str, **kwargs: Any) -> ChatMessage:
        """Generate a response from the chat model."""
        raise NotImplementedError("Subclasses must implement generate()")
    
    async def generate_with_tools(
        self,
        prompt: str,
        tools: List[Tool],
        **kwargs: Any
    ) -> ChatMessage:
        """Generate a response with tool calling capability."""
        raise NotImplementedError("Subclasses must implement generate_with_tools()")
    
    def _format_tools_for_model(self, tools: List[Tool]) -> List[Dict[str, Any]]:
        """Format tools into the model-specific format."""
        return [tool.get_schema() for tool in tools]
