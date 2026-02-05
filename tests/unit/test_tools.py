"""Unit tests for tools."""

import pytest
from agent.tools.email import ReadInboxTool, SendEmailTool


@pytest.mark.asyncio
async def test_read_inbox_tool():
    """Test read inbox tool execution."""
    tool = ReadInboxTool()
    
    result = await tool.execute({"limit": 5, "unread_only": True})
    
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_send_email_tool():
    """Test send email tool execution."""
    tool = SendEmailTool()
    
    result = await tool.execute({
        "to": ["test@example.com"],
        "subject": "Test",
        "body": "Test message"
    })
    
    assert result["success"] is True
