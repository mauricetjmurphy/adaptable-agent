"""List tickets tool for Jira agents."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from agent.tools.base import BaseTool


class ListTicketsInput(BaseModel):
    """Input schema for listing Jira tickets."""
    project: str = Field(description="Jira project key (e.g. 'PROJ')")
    status: Optional[str] = Field(default=None, description="Filter by status (e.g. 'To Do', 'In Progress')")
    assignee: Optional[str] = Field(default=None, description="Filter by assignee")
    limit: int = Field(default=10, description="Maximum number of tickets to return")


class ListTicketsTool(BaseTool):
    """
    Tool for listing Jira tickets within a project.

    Supports filtering by status and assignee.
    Uses langchain_community.utilities.jira.JiraAPIWrapper under the hood.
    """

    def __init__(self):
        super().__init__(
            name="list_tickets",
            description="List Jira tickets in a project with optional filters",
            input_schema=ListTicketsInput
        )

    async def _execute(self, input_data: ListTicketsInput) -> List[dict[str, Any]]:
        """Execute ticket listing."""
        # TODO: Integrate with langchain_community.utilities.jira.JiraAPIWrapper
        # Example:
        #   from langchain_community.utilities.jira import JiraAPIWrapper
        #   jira = JiraAPIWrapper()
        #   jql = f"project = {input_data.project}"
        #   if input_data.status:
        #       jql += f" AND status = '{input_data.status}'"
        #   tickets = jira.search_issues(jql)

        return [
            {
                "id": f"{input_data.project}-1",
                "summary": "Example ticket",
                "status": "To Do",
                "assignee": "example-user",
                "created_at": "2026-02-04T10:00:00Z"
            }
        ]