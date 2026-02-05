"""Agent configuration definitions."""

from agent.agents.base import create_agent_config
from agent.agents.email_agent import create_email_agent
from agent.agents.financial_agent import create_financial_agent
from agent.agents.document_agent import create_document_agent
from agent.agents.github_agent import create_github_agent
from agent.agents.jira_agent import create_jira_agent

__all__ = [
    "create_agent_config",
    "create_email_agent",
    "create_financial_agent",
    "create_document_agent",
    "create_github_agent",
    "create_jira_agent",
]
