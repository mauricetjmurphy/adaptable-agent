"""GitHub agent configuration."""

from agent.core.config import AgentConfig
from agent.core.contracts import ChatModelAdapter, MemoryProvider
from agent.models.input import TaskInput
from agent.memory.buffer import BufferMemory
from agent.tools.github import (
    ListReposTool,
    GetFileContentsTool,
    ListPullRequestsTool,
    CreatePullRequestTool,
)


def create_github_agent(
    chat_model: ChatModelAdapter,
    memory: MemoryProvider = None
) -> AgentConfig:
    """
    Create a GitHub agent configuration.

    GitHub agents are task-based with:
    - Task input (repo names, file paths, PR details)
    - Buffer memory for maintaining context across a review session
    - Read-only tools for repo and file exploration
    - A write tool (CreatePullRequestTool) that must be approval-gated

    Args:
        chat_model: Chat model adapter to use
        memory: Optional custom memory provider

    Returns:
        AgentConfig for GitHub agent
    """
    if memory is None:
        memory = BufferMemory(max_messages=30)

    tools = [
        ListReposTool(),
        GetFileContentsTool(),
        ListPullRequestsTool(),
        CreatePullRequestTool(),
    ]

    return AgentConfig(
        name="github_agent",
        description="Agent for reviewing GitHub repositories and creating pull requests",
        input_schema=TaskInput,
        chat_model=chat_model,
        memory=memory,
        tools=tools,
        max_iterations=20,
        metadata={
            "agent_type": "github",
            "capabilities": [
                "repo_listing",
                "file_reading",
                "pr_listing",
                "pr_creation",
            ],
            "write_tools": ["create_pull_request"],
        }
    )