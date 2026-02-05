"""Get ticket tool for Jira agents."""

from typing import Any
from pydantic import BaseModel, Field
from agent.tools.base import BaseTool


class GetTicketInput(BaseModel):
    """Input schema for retrieving a Jira ticket."""
    ticket_id: str = Field(description="Jira ticket identifier (e.g. 'PROJ-123')")


class GetTicketTool(BaseTool):
    """
    Tool for fetching a single Jira ticket by its ID.

    Returns the full ticket payload including summary, description,
    status, assignee, labels, and acceptance criteria.
    Uses langchain_community.utilities.jira.JiraAPIWrapper under the hood.
    """

    def __init__(self):
        super().__init__(
            name="get_ticket",
            description="Retrieve a Jira ticket by its ID",
            input_schema=GetTicketInput
        )

    async def _execute(self, input_data: GetTicketInput) -> dict[str, Any]:
        """Execute ticket retrieval."""
        # TODO: Integrate with langchain_community.utilities.jira.JiraAPIWrapper
        # Example:
        #   from langchain_community.utilities.jira import JiraAPIWrapper
        #   jira = JiraAPIWrapper()
        #   ticket = jira.get_issue(input_data.ticket_id)

        return {
            "id": input_data.ticket_id,
            "summary": "Example ticket summary",
            "description": "Detailed description of the task.",
            "status": "To Do",
            "assignee": "example-user",
            "labels": ["backend"],
            "created_at": "2026-02-04T10:00:00Z",
            "updated_at": "2026-02-04T12:00:00Z"
        }