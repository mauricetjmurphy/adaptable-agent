"""Jira agent configuration."""

from agent.core.config import AgentConfig
from agent.core.contracts import ChatModelAdapter, MemoryProvider
from agent.models.input import TaskInput
from agent.memory.buffer import BufferMemory
from agent.tools.jira import GetTicketTool, ListTicketsTool, AddCommentTool


def create_jira_agent(
    chat_model: ChatModelAdapter,
    memory: MemoryProvider = None
) -> AgentConfig:
    """
    Create a Jira ticket processing agent configuration.

    Jira agents are task-based with:
    - Task input (ticket IDs, project keys)
    - Buffer memory for accumulating ticket context
    - Read tools for fetching and listing tickets
    - A write tool (AddCommentTool) that must be approval-gated

    Args:
        chat_model: Chat model adapter to use
        memory: Optional custom memory provider

    Returns:
        AgentConfig for Jira agent
    """
    if memory is None:
        memory = BufferMemory(max_messages=30)

    tools = [
        GetTicketTool(),
        ListTicketsTool(),
        AddCommentTool(),
    ]

    return AgentConfig(
        name="jira_agent",
        description="Agent for reading and processing Jira tickets",
        input_schema=TaskInput,
        chat_model=chat_model,
        memory=memory,
        tools=tools,
        max_iterations=15,
        metadata={
            "agent_type": "jira",
            "capabilities": [
                "ticket_retrieval",
                "ticket_listing",
                "ticket_commenting",
            ],
            "write_tools": ["add_comment"],
        }
    )