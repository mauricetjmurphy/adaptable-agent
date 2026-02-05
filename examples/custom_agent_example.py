"""Example: Creating a custom agent."""

import asyncio
from agent.core.engine import AgentEngine
from agent.core.config import AgentConfig
from agent.adapters.factory import AdapterFactory
from agent.memory.buffer import BufferMemory
from agent.models.input import TaskInput
from agent.tools.base import BaseTool
from pydantic import BaseModel, Field
from agent.observability.logger import configure_logging


# Define a custom tool
class CustomToolInput(BaseModel):
    """Input for custom tool."""
    action: str = Field(description="Action to perform")


class CustomTool(BaseTool):
    """A custom tool for demonstration."""
    
    def __init__(self):
        super().__init__(
            name="custom_action",
            description="Performs a custom action",
            input_schema=CustomToolInput
        )
    
    async def _execute(self, input_data: CustomToolInput):
        """Execute the custom action."""
        return {
            "success": True,
            "action": input_data.action,
            "result": f"Executed custom action: {input_data.action}"
        }


async def main():
    """Run custom agent example."""
    # Configure logging
    configure_logging(level="INFO")
    
    # Create components
    adapter = AdapterFactory.create(
        provider="openai",
        model_name="gpt-4",
        temperature=0.7
    )
    memory = BufferMemory(max_messages=20)
    tools = [CustomTool()]
    
    # Create custom agent configuration
    config = AgentConfig(
        name="custom_agent",
        description="A custom agent with custom tools",
        input_schema=TaskInput,
        chat_model=adapter,
        memory=memory,
        tools=tools,
        max_iterations=10
    )
    
    # Create agent engine
    engine = AgentEngine(config)
    
    # Create input
    user_input = TaskInput(
        task="Perform a custom action",
        parameters={"action": "process_data"}
    )
    
    # Run agent
    print("Running custom agent...")
    result = await engine.run(user_input)
    
    print(f"\nAgent Response:")
    print(f"Content: {result.content}")
    print(f"Metadata: {result.metadata}")


if __name__ == "__main__":
    asyncio.run(main())
