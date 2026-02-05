"""Integration test for financial agent."""

import pytest
from agent.agents.financial_agent import create_financial_agent
from agent.adapters.factory import AdapterFactory


@pytest.mark.asyncio
@pytest.mark.integration
async def test_financial_agent_creation():
    """Test financial agent creation."""
    adapter = AdapterFactory.create(
        provider="openai",
        model_name="gpt-4",
        temperature=0.0  # Deterministic for financial data
    )
    
    config = create_financial_agent(adapter)
    
    assert config.name == "financial_agent"
    assert len(config.tools) == 2  # FetchMarketData and NormalizeFinancials
