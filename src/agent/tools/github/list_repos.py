"""List repositories tool for GitHub agents."""

from typing import Any, List, Optional
from pydantic import BaseModel, Field
from agent.tools.base import BaseTool


class ListReposInput(BaseModel):
    """Input schema for listing repositories."""
    org: Optional[str] = Field(default=None, description="GitHub organization or user to list repos for")
    limit: int = Field(default=10, description="Maximum number of repositories to return")
    sort: str = Field(default="updated", description="Sort order: updated, created, pushed, fullname")


class ListReposTool(BaseTool):
    """
    Tool for listing GitHub repositories.

    Returns repository metadata for an organization or authenticated user.
    Uses langchain_community.utilities.github.GitHubAPIWrapper under the hood.
    """

    def __init__(self):
        super().__init__(
            name="list_repos",
            description="List GitHub repositories for an organization or the authenticated user",
            input_schema=ListReposInput
        )

    async def _execute(self, input_data: ListReposInput) -> List[dict[str, Any]]:
        """Execute repository listing."""
        # TODO: Integrate with langchain_community.utilities.github.GitHubAPIWrapper
        # Example:
        #   from langchain_community.utilities.github import GitHubAPIWrapper
        #   github = GitHubAPIWrapper(github_repo=input_data.org)
        #   repos = github.list_repos()

        return [
            {
                "name": "example-repo",
                "full_name": "example-org/example-repo",
                "description": "An example repository",
                "private": False,
                "default_branch": "main",
                "updated_at": "2026-02-04T10:00:00Z"
            }
        ]