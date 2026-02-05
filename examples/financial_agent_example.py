"""Example: Financial agent usage."""

import asyncio
from agent.core.engine import AgentEngine
from agent.agents.financial_agent import create_financial_agent
from agent.adapters.factory import AdapterFactory
from agent.models.input import QueryInput
from agent.observability.logger import configure_logging


async def main():
    """Run financial agent example."""
    # Configure logging
    configure_logging(level="INFO")
    
    # Create chat model adapter with low temperature for deterministic responses
    adapter = AdapterFactory.create(
        provider="openai",
        model_name="gpt-4",
        temperature=0.0
    )
    
    # Create financial agent configuration
    config = create_financial_agent(adapter)
    
    # Create agent engine
    engine = AgentEngine(config)
    
    # Create input
    user_input = QueryInput(
        query="Get the current stock price for AAPL",
        filters={"period": "1d", "interval": "1h"}
    )
    
    # Run agent
    print("Running financial agent...")
    result = await engine.run(user_input)
    
    print(f"\nAgent Response:")
    print(f"Content: {result.content}")
    print(f"Metadata: {result.metadata}")


if __name__ == "__main__":
    asyncio.run(main())
