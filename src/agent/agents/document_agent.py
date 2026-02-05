"""Document processing agent configuration."""

from agent.core.config import AgentConfig
from agent.core.contracts import ChatModelAdapter, MemoryProvider
from agent.models.input import TaskInput
from agent.memory.buffer import BufferMemory
from agent.tools.document import ParsePDFTool, ExtractTextTool


def create_document_agent(
    chat_model: ChatModelAdapter,
    memory: MemoryProvider = None
) -> AgentConfig:
    """
    Create a document processing agent configuration.
    
    Document agents are task-based with:
    - Task input
    - Buffer memory for processing context
    - Document parsing and text extraction tools
    
    Args:
        chat_model: Chat model adapter to use
        memory: Optional custom memory provider
        
    Returns:
        AgentConfig for document agent
    """
    if memory is None:
        memory = BufferMemory(max_messages=30)
    
    tools = [
        ParsePDFTool(),
        ExtractTextTool()
    ]
    
    return AgentConfig(
        name="document_agent",
        description="Agent for processing and analyzing documents",
        input_schema=TaskInput,
        chat_model=chat_model,
        memory=memory,
        tools=tools,
        max_iterations=20,
        metadata={
            "agent_type": "document",
            "capabilities": ["pdf_parsing", "text_extraction", "document_analysis"]
        }
    )
