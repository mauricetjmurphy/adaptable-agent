"""Integration test for email agent."""

import pytest
from agent.agents.email_agent import create_email_agent
from agent.adapters.factory import AdapterFactory
from agent.models.input import ChatInput


@pytest.mark.asyncio
@pytest.mark.integration
async def test_email_agent_creation():
    """Test email agent creation."""
    # Create adapter
    adapter = AdapterFactory.create(
        provider="openai",
        model_name="gpt-4"
    )
    
    # Create agent config
    config = create_email_agent(adapter)
    
    assert config.name == "email_agent"
    assert len(config.tools) == 2  # ReadInbox and SendEmail


# Add more integration tests as needed
