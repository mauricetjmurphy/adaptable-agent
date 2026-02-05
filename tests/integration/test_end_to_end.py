"""End-to-end integration tests."""

import pytest
from agent.core.engine import AgentEngine
from agent.agents.email_agent import create_email_agent
from agent.adapters.factory import AdapterFactory
from agent.models.input import ChatInput


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.e2e
async def test_full_agent_execution():
    """Test complete agent execution flow."""
    # TODO: Implement full e2e test with mock LLM
    pass
