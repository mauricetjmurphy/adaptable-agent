"""List pull requests tool for GitHub agents."""

from typing import Any, List
from pydantic import BaseModel, Field
from agent.tools.base import BaseTool


class ListPullRequestsInput(BaseModel):
    """Input schema for listing pull requests."""
    repo: str = Field(description="Repository name (e.g. 'org/repo')")
    state: str = Field(default="open", description="Filter by state: open, closed, all")
    limit: int = Field(default=10, description="Maximum number of pull requests to return")


class ListPullRequestsTool(BaseTool):
    """
    Tool for listing pull requests in a GitHub repository.

    Read-only.  Uses langchain_community.utilities.github.GitHubAPIWrapper
    under the hood.
    """

    def __init__(self):
        super().__init__(
            name="list_pull_requests",
            description="List pull requests for a GitHub repository",
            input_schema=ListPullRequestsInput
        )

    async def _execute(self, input_data: ListPullRequestsInput) -> List[dict[str, Any]]:
        """Execute pull request listing."""
        # TODO: Integrate with langchain_community.utilities.github.GitHubAPIWrapper
        # Example:
        #   from langchain_community.utilities.github import GitHubAPIWrapper
        #   github = GitHubAPIWrapper(github_repo=input_data.repo)
        #   prs = github.list_pull_requests()

        return [
            {
                "number": 42,
                "title": "Example pull request",
                "state": "open",
                "head_branch": "feature/example",
                "base_branch": "main",
                "created_at": "2026-02-04T10:00:00Z",
                "author": "example-user"
            }
        ]