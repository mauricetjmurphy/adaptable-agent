"""Unit tests for chat model adapters."""

import pytest
from agent.adapters.factory import AdapterFactory


def test_adapter_factory_openai():
    """Test creating OpenAI adapter via factory."""
    adapter = AdapterFactory.create(
        provider="openai",
        model_name="gpt-4",
        temperature=0.7
    )
    
    assert adapter is not None
    assert adapter.model_name == "gpt-4"


def test_adapter_factory_anthropic():
    """Test creating Anthropic adapter via factory."""
    adapter = AdapterFactory.create(
        provider="anthropic",
        model_name="claude-3-sonnet-20240229",
        temperature=0.5
    )
    
    assert adapter is not None
    assert adapter.model_name == "claude-3-sonnet-20240229"


def test_adapter_factory_invalid_provider():
    """Test that invalid provider raises error."""
    with pytest.raises(ValueError):
        AdapterFactory.create(
            provider="invalid",
            model_name="test"
        )
