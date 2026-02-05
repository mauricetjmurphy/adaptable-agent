# Quick Start Guide

## Installation

1. **Clone or set up the repository**

2. **Install dependencies**
   ```bash
   pip install -e .
   ```

3. **Set up environment**
   ```bash
   python scripts/setup_env.py
   ```
   
   This will create necessary directories and a `.env` file.

4. **Configure API keys**
   
   Edit `.env` and add your LLM provider API keys:
   ```bash
   OPENAI_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   ```

## Running Your First Agent

### Using the CLI

```bash
# Email agent
python scripts/run_agent.py email -m "Check my unread emails"

# Financial agent
python scripts/run_agent.py financial -m "Get AAPL stock price"

# Document agent
python scripts/run_agent.py document -m "Parse the quarterly report"
```

### Using Python

```python
import asyncio
from agent.core.engine import AgentEngine
from agent.agents.email_agent import create_email_agent
from agent.adapters.factory import AdapterFactory
from agent.models.input import ChatInput

async def main():
    # Create chat model adapter
    adapter = AdapterFactory.create(
        provider="openai",
        model_name="gpt-4"
    )
    
    # Create agent
    config = create_email_agent(adapter)
    engine = AgentEngine(config)
    
    # Run agent
    result = await engine.run(
        ChatInput(message="Read my emails")
    )
    
    print(result.content)

asyncio.run(main())
```

## Creating a Custom Agent

```python
from agent.core.config import AgentConfig
from agent.adapters.factory import AdapterFactory
from agent.memory.buffer import BufferMemory
from agent.models.input import TaskInput

# Create adapter
adapter = AdapterFactory.create(
    provider="openai",
    model_name="gpt-4"
)

# Create custom agent
config = AgentConfig(
    name="my_agent",
    description="My custom agent",
    input_schema=TaskInput,
    chat_model=adapter,
    memory=BufferMemory(),
    tools=[],  # Add your tools here
    max_iterations=10
)
```

## Next Steps

- Read the [Agent Creation Guide](agent_creation_guide.md)
- Check out the [examples/](../examples/) directory
- Review the [Architecture Documentation](adaptable_agent_architecture.md)
