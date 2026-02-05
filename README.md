# Adaptable Agent Architecture

A flexible, LLM-agnostic agent framework built with Pydantic and LangChain.

## Overview

This system provides a single reusable agent engine that powers multiple domain-specific agents through configuration rather than code changes.

## Features

- **Single Engine, Multiple Agents**: Shared execution engine with agent-specific configurations
- **LLM-Agnostic**: Chat model adapter layer supporting multiple LLM providers
- **Stateless Execution**: Horizontal scaling and async execution support
- **Capability-Based**: Agents constrained by input schema, memory, and tools
- **Safe & Observable**: Built-in logging, auditing, and permission controls

## Quick Start

```bash
# Install dependencies
pip install -e .

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run an example agent
python examples/email_agent_example.py
```

## Documentation

- [Architecture Overview](docs/adaptable_agent_architecture.md)
- [Quick Start Guide](docs/quickstart.md)
- [Agent Creation Guide](docs/agent_creation_guide.md)
- [API Reference](docs/api_reference.md)

## Project Structure

- `src/agent/core/` - Core agent engine and execution logic
- `src/agent/adapters/` - LLM provider adapters
- `src/agent/memory/` - Memory implementations
- `src/agent/tools/` - Tool definitions and implementations
- `src/agent/agents/` - Agent configurations
- `examples/` - Usage examples
- `configs/` - YAML configuration files

## License

MIT
