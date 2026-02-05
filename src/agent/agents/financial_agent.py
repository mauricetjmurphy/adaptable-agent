"""Financial data agent configuration."""

from agent.core.config import AgentConfig
from agent.core.contracts import ChatModelAdapter, MemoryProvider
from agent.models.input import QueryInput
from agent.memory.ephemeral import EphemeralMemory
from agent.tools.financial import FetchMarketDataTool, NormalizeFinancialsTool


def create_financial_agent(
    chat_model: ChatModelAdapter,
    memory: MemoryProvider = None
) -> AgentConfig:
    """
    Create a financial data agent configuration.
    
    Financial agents are query-based with:
    - Structured query input
    - Deterministic chat model (low temperature)
    - Financial data tools
    - Ephemeral memory (stateless queries)
    
    Args:
        chat_model: Chat model adapter to use
        memory: Optional custom memory provider
        
    Returns:
        AgentConfig for financial agent
    """
    if memory is None:
        memory = EphemeralMemory()
    
    tools = [
        FetchMarketDataTool(),
        NormalizeFinancialsTool()
    ]
    
    return AgentConfig(
        name="financial_agent",
        description="Agent for fetching and analyzing financial data",
        input_schema=QueryInput,
        chat_model=chat_model,
        memory=memory,
        tools=tools,
        max_iterations=10,
        metadata={
            "agent_type": "financial",
            "capabilities": ["market_data", "financial_analysis", "data_normalization"]
        }
    )
