"""Mock LLM responses for testing."""

MOCK_CHAT_RESPONSE = {
    "role": "assistant",
    "content": "This is a mock response from the LLM."
}

MOCK_TOOL_CALL_RESPONSE = {
    "role": "assistant",
    "content": "",
    "tool_calls": [
        {
            "name": "read_inbox",
            "arguments": {"limit": 10, "unread_only": True}
        }
    ]
}

MOCK_FINAL_RESPONSE = {
    "role": "assistant",
    "content": "I have completed the task successfully."
}
