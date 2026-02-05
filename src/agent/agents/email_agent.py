"""Email agent configuration."""

from agent.core.config import AgentConfig
from agent.core.contracts import ChatModelAdapter, MemoryProvider
from agent.models.input import ChatInput
from agent.memory.buffer import BufferMemory
from agent.tools.email import ReadInboxTool, SendEmailTool


def create_email_agent(
    chat_model: ChatModelAdapter,
    memory: MemoryProvider = None
) -> AgentConfig:
    """
    Create an email agent configuration.
    
    Email agents are chat-based with:
    - Chat input
    - Conversation buffer memory
    - Email reading and sending tools
    
    Args:
        chat_model: Chat model adapter to use
        memory: Optional custom memory provider
        
    Returns:
        AgentConfig for email agent
    """
    if memory is None:
        memory = BufferMemory(max_messages=50)
    
    tools = [
        ReadInboxTool(),
        SendEmailTool()
    ]
    
    return AgentConfig(
        name="email_agent",
        description="Agent for reading and managing emails",
        input_schema=ChatInput,
        chat_model=chat_model,
        memory=memory,
        tools=tools,
        max_iterations=15,
        metadata={
            "agent_type": "email",
            "capabilities": ["read_inbox", "send_email", "chat"]
        }
    )
