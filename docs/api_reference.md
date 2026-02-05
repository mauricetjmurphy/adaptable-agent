# API Reference

## Core Components

### AgentEngine

The stateless execution engine that runs agents.

```python
from agent.core.engine import AgentEngine

engine = AgentEngine(config: AgentConfig)
result = await engine.run(input_data: BaseModel)
```

**Methods:**
- `run(input_data: BaseModel) -> BaseOutput` - Execute the agent

### AgentConfig

Configuration for an agent instance.

```python
from agent.core.config import AgentConfig

config = AgentConfig(
    name: str,
    description: str,
    input_schema: Type[BaseModel],
    chat_model: ChatModelAdapter,
    memory: MemoryProvider,
    tools: List[Tool],
    max_iterations: int = 10,
    stop_conditions: List[str] = [],
    metadata: dict = {}
)
```

## Adapters

### AdapterFactory

Factory for creating chat model adapters.

```python
from agent.adapters.factory import AdapterFactory

adapter = AdapterFactory.create(
    provider: str,           # "openai" or "anthropic"
    model_name: str,
    api_key: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None
)
```

## Memory Providers

### BufferMemory

Conversation buffer with sliding window.

```python
from agent.memory.buffer import BufferMemory

memory = BufferMemory(
    max_messages: int = 50,
    max_tokens: int = 2000
)
```

### EphemeralMemory

No-op memory for stateless agents.

```python
from agent.memory.ephemeral import EphemeralMemory

memory = EphemeralMemory()
```

### ContextualMemory

Read-only contextual data.

```python
from agent.memory.contextual import ContextualMemory

memory = ContextualMemory(
    context_data: List[Dict[str, Any]]
)
```

## Tools

### BaseTool

Base class for creating tools.

```python
from agent.tools.base import BaseTool
from pydantic import BaseModel

class MyTool(BaseTool):
    def __init__(self):
        super().__init__(
            name: str,
            description: str,
            input_schema: Type[BaseModel]
        )
    
    async def _execute(self, input_data: BaseModel) -> Any:
        # Implement tool logic
        pass
```

### ToolRegistry

Registry for managing tools.

```python
from agent.tools.registry import get_global_registry

registry = get_global_registry()
registry.register(tool: Tool)
registry.get(tool_name: str) -> Optional[Tool]
registry.list_tools() -> List[str]
```

## Input/Output Models

### BaseInput

Base class for agent inputs.

```python
from agent.models.input import BaseInput

class ChatInput(BaseInput):
    message: str
    conversation_id: Optional[str]
```

### BaseOutput

Standard agent output format.

```python
from agent.models.output import BaseOutput

output = BaseOutput(
    content: str,
    metadata: Dict[str, Any],
    timestamp: datetime,
    success: bool,
    error: Optional[str]
)
```

## Observability

### Logger

Structured logging.

```python
from agent.observability.logger import get_logger, configure_logging

configure_logging(level="INFO", log_file="agent.log")
logger = get_logger(__name__)
```

### MetricsCollector

Track execution metrics.

```python
from agent.observability.metrics import get_global_metrics

metrics = get_global_metrics()
metrics.record_execution_time(agent_name, duration)
metrics.record_tool_call(tool_name, success)
```

### ExecutionTracer

Trace execution for debugging.

```python
from agent.observability.tracer import get_global_tracer

tracer = get_global_tracer()
tracer.trace(event_type, agent_name, details, iteration)
traces = tracer.get_traces(agent_name="my_agent")
```

## Safety

### PermissionManager

Manage tool permissions.

```python
from agent.safety.permissions import get_global_permissions, Permission

permissions = get_global_permissions()
permissions.register_tool_permissions(tool_name, [Permission.EXECUTE])
permissions.mark_sensitive(tool_name)
```

### AuditLogger

Audit logging for compliance.

```python
from agent.safety.audit import get_global_audit_logger

audit = get_global_audit_logger()
audit.log_agent_run(agent_name, input_data, output, success)
audit.log_tool_call(agent_name, tool_name, arguments, result, success)
```

## Utilities

### PromptBuilder

Build prompts from components.

```python
from agent.utils.prompt_builder import PromptBuilder

builder = PromptBuilder(template="...")
prompt = builder.build(input_data, memory_context, tools)
```

### RateLimiter

Rate limiting for API calls.

```python
from agent.utils.rate_limiter import RateLimiter

limiter = RateLimiter(max_requests=60, time_window=60.0)
await limiter.acquire()
```

### retry_with_backoff

Decorator for retrying with exponential backoff.

```python
from agent.utils.retry import retry_with_backoff

@retry_with_backoff(max_retries=3, base_delay=1.0)
async def my_function():
    # Will retry up to 3 times with exponential backoff
    pass
```

## Pre-built Agents

### Email Agent

```python
from agent.agents.email_agent import create_email_agent

config = create_email_agent(chat_model)
```

### Financial Agent

```python
from agent.agents.financial_agent import create_financial_agent

config = create_financial_agent(chat_model)
```

### Document Agent

```python
from agent.agents.document_agent import create_document_agent

config = create_document_agent(chat_model)
```
