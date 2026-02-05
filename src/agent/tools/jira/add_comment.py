"""Add comment tool for Jira agents."""

from typing import Any
from pydantic import BaseModel, Field
from agent.tools.base import BaseTool


class AddCommentInput(BaseModel):
    """Input schema for adding a comment to a Jira ticket."""
    ticket_id: str = Field(description="Jira ticket identifier (e.g. 'PROJ-123')")
    comment: str = Field(description="Comment text to add to the ticket")


class AddCommentTool(BaseTool):
    """
    Tool for adding a comment to a Jira ticket.

    WRITE operation — this tool MUST be used behind an approval gate
    when running in production.

    Uses langchain_community.utilities.jira.JiraAPIWrapper under the hood.
    """

    def __init__(self):
        super().__init__(
            name="add_comment",
            description="Add a comment to a Jira ticket (requires approval)",
            input_schema=AddCommentInput
        )

    async def _execute(self, input_data: AddCommentInput) -> dict[str, Any]:
        """Execute comment addition."""
        # TODO: Integrate with langchain_community.utilities.jira.JiraAPIWrapper
        # Example:
        #   from langchain_community.utilities.jira import JiraAPIWrapper
        #   jira = JiraAPIWrapper()
        #   jira.add_comment(input_data.ticket_id, input_data.comment)

        return {
            "success": True,
            "ticket_id": input_data.ticket_id,
            "comment": input_data.comment,
            "added_at": "2026-02-04T10:00:00Z"
        }