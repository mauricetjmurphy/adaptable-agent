"""LangChain wrapper utilities."""

from typing import Any, Dict, List
from agent.core.contracts import Tool


class LangChainToolWrapper:
    """
    Wraps our Tool interface for LangChain compatibility.
    
    LangChain is used internally but not exposed at system boundaries.
    """
    
    @staticmethod
    def to_langchain_tool(tool: Tool) -> Dict[str, Any]:
        """Convert our Tool to LangChain tool format."""
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema.model_json_schema()
            }
        }
    
    @staticmethod
    def from_langchain_response(response: Any) -> Dict[str, Any]:
        """Convert LangChain response to our format."""
        # TODO: Implement conversion logic
        return {
            "content": str(response),
            "tool_calls": []
        }
