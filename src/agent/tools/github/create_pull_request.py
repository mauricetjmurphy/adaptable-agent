"""Create pull request tool for GitHub agents."""

from typing import Any, Optional
from pydantic import BaseModel, Field
from agent.tools.base import BaseTool


class CreatePullRequestInput(BaseModel):
    """Input schema for creating a pull request."""
    repo: str = Field(description="Repository name (e.g. 'org/repo')")
    title: str = Field(description="Pull request title")
    body: str = Field(description="Pull request description")
    head_branch: str = Field(description="Source branch containing the changes")
    base_branch: str = Field(default="main", description="Target branch to merge into")
    draft: bool = Field(default=False, description="Create as a draft pull request")
    labels: Optional[list[str]] = Field(default=None, description="Labels to apply to the pull request")


class CreatePullRequestTool(BaseTool):
    """
    Tool for creating a pull request on GitHub.

    WRITE operation — this tool MUST be used behind an approval gate.
    The ToolExecutor's approval mechanism should be enabled for this tool
    in production deployments.

    Uses langchain_community.utilities.github.GitHubAPIWrapper under the hood.
    """

    def __init__(self):
        super().__init__(
            name="create_pull_request",
            description="Create a pull request in a GitHub repository (requires approval)",
            input_schema=CreatePullRequestInput
        )

    async def _execute(self, input_data: CreatePullRequestInput) -> dict[str, Any]:
        """Execute pull request creation."""
        # TODO: Integrate with langchain_community.utilities.github.GitHubAPIWrapper
        # Example:
        #   from langchain_community.utilities.github import GitHubAPIWrapper
        #   github = GitHubAPIWrapper(github_repo=input_data.repo)
        #   pr = github.create_pull_request(
        #       title=input_data.title,
        #       body=input_data.body,
        #       head=input_data.head_branch,
        #       base=input_data.base_branch,
        #   )

        return {
            "success": True,
            "number": 99,
            "url": f"https://github.com/{input_data.repo}/pull/99",
            "title": input_data.title,
            "head_branch": input_data.head_branch,
            "base_branch": input_data.base_branch,
            "draft": input_data.draft,
            "created_at": "2026-02-04T10:00:00Z"
        }