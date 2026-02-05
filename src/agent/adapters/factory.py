"""Factory for creating chat model adapters."""

from typing import Optional
from agent.core.contracts import ChatModelAdapter
from agent.adapters.openai import OpenAIAdapter
from agent.adapters.anthropic import AnthropicAdapter


class AdapterFactory:
    """Factory for creating chat model adapter instances."""
    
    @staticmethod
    def create(
        provider: str,
        model_name: str,
        api_key: Optional[str] = None,
        **kwargs
    ) -> ChatModelAdapter:
        """
        Create a chat model adapter.
        
        Args:
            provider: Provider name (openai, anthropic, etc.)
            model_name: Model name
            api_key: Optional API key
            **kwargs: Additional model parameters
            
        Returns:
            ChatModelAdapter instance
        """
        provider = provider.lower()
        
        if provider == "openai":
            return OpenAIAdapter(
                model_name=model_name,
                api_key=api_key,
                **kwargs
            )
        elif provider in ["anthropic", "claude"]:
            return AnthropicAdapter(
                model_name=model_name,
                api_key=api_key,
                **kwargs
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    @staticmethod
    def from_config(config: dict) -> ChatModelAdapter:
        """Create adapter from configuration dictionary."""
        provider = config.get("provider")
        model_name = config.get("model_name")
        api_key = config.get("api_key")
        
        # Remove known keys, pass rest as kwargs
        extra = {k: v for k, v in config.items() 
                if k not in ["provider", "model_name", "api_key"]}
        
        return AdapterFactory.create(provider, model_name, api_key, **extra)
