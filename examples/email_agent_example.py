"""Example: Email agent usage."""

import asyncio
from agent.core.engine import AgentEngine
from agent.agents.email_agent import create_email_agent
from agent.adapters.factory import AdapterFactory
from agent.models.input import ChatInput
from agent.observability.logger import configure_logging


async def main():
    """Run email agent example."""
    # Configure logging
    configure_logging(level="INFO")
    
    # Create chat model adapter
    adapter = AdapterFactory.create(
        provider="openai",
        model_name="gpt-4",
        temperature=0.7
    )
    
    # Create email agent configuration
    config = create_email_agent(adapter)
    
    # Create agent engine
    engine = AgentEngine(config)
    
    # Create input
    user_input = ChatInput(
        message="Please read my unread emails and summarize them.",
        conversation_id="conv_001"
    )
    
    # Run agent
    print("Running email agent...")
    result = await engine.run(user_input)
    
    print(f"\nAgent Response:")
    print(f"Content: {result.content}")
    print(f"Metadata: {result.metadata}")


if __name__ == "__main__":
    asyncio.run(main())
