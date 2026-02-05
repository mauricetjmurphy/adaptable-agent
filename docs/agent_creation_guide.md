# Agent Creation Guide

## Overview

This guide walks you through creating custom agents using the adaptable agent architecture.

## Core Concepts

Every agent requires exactly four components:

1. **Input Schema** - Pydantic model defining what the agent accepts
2. **Chat Model** - LLM adapter for generating responses
3. **Memory** - Context management strategy
4. **Tools** - Capabilities the agent can use

## Step 1: Define Input Schema

```python
from pydantic import BaseModel, Field
from agent.models.input import BaseInput

class MyAgentInput(BaseInput):
    """Custom input for my agent."""
    query: str = Field(description="User query")
    context: dict = Field(default_factory=dict)
```

## Step 2: Create Custom Tools

```python
from agent.tools.base import BaseTool
from pydantic import BaseModel, Field

class MyToolInput(BaseModel):
    parameter: str = Field(description="Tool parameter")

class MyCustomTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="Does something useful",
            input_schema=MyToolInput
        )
    
    async def _execute(self, input_data: MyToolInput):
        # Implement tool logic
        return {"result": f"Processed: {input_data.parameter}"}
```

## Step 3: Configure the Agent

```python
from agent.core.config import AgentConfig
from agent.adapters.factory import AdapterFactory
from agent.memory.buffer import BufferMemory

def create_my_agent(api_key: str):
    # Create adapter
    adapter = AdapterFactory.create(
        provider="openai",
        model_name="gpt-4",
        temperature=0.7,
        api_key=api_key
    )
    
    # Create memory
    memory = BufferMemory(max_messages=30)
    
    # Create tools
    tools = [MyCustomTool()]
    
    # Create configuration
    config = AgentConfig(
        name="my_agent",
        description="My custom agent",
        input_schema=MyAgentInput,
        chat_model=adapter,
        memory=memory,
        tools=tools,
        max_iterations=15
    )
    
    return config
```

## Step 4: Run the Agent

```python
from agent.core.engine import AgentEngine

async def run_my_agent():
    config = create_my_agent(api_key="your_key")
    engine = AgentEngine(config)
    
    input_data = MyAgentInput(
        query="Do something interesting"
    )
    
    result = await engine.run(input_data)
    print(result.content)
```

## Memory Options

### Buffer Memory (Chat History)
```python
from agent.memory.buffer import BufferMemory
memory = BufferMemory(max_messages=50, max_tokens=2000)
```

### Ephemeral Memory (Stateless)
```python
from agent.memory.ephemeral import EphemeralMemory
memory = EphemeralMemory()
```

### Contextual Memory (Read-only)
```python
from agent.memory.contextual import ContextualMemory
memory = ContextualMemory(context_data=[...])
```

## Best Practices

1. **Keep tools focused** - Each tool should do one thing well
2. **Validate inputs** - Use Pydantic for all input validation
3. **Handle errors** - Tools should catch and report errors gracefully
4. **Use appropriate memory** - Match memory to agent purpose
5. **Set reasonable iteration limits** - Prevent infinite loops
6. **Add observability** - Use logging and metrics

## Advanced: Tool Permissions

```python
from agent.safety.permissions import get_global_permissions, Permission

permissions = get_global_permissions()
permissions.register_tool_permissions(
    "my_sensitive_tool",
    [Permission.EXECUTE, Permission.ADMIN]
)
permissions.mark_sensitive("my_sensitive_tool")
```

## Advanced: Approval Gates

```python
from agent.tools.executor import ToolExecutor

executor = ToolExecutor(enable_approval_gates=True)
result = await executor.execute(
    tool=my_tool,
    arguments={"param": "value"},
    require_approval=True
)
```

## Example: Complete Custom Agent

See [examples/custom_agent_example.py](../examples/custom_agent_example.py) for a complete working example.
