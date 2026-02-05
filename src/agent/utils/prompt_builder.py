"""Prompt assembly utilities."""

from typing import Any, Dict, List
from pydantic import BaseModel


class PromptBuilder:
    """
    Builds prompts from input, memory, and tool descriptions.
    
    Provides flexible prompt assembly with templates.
    """
    
    def __init__(self, template: str = None):
        self.template = template or self._default_template()
    
    @staticmethod
    def _default_template() -> str:
        """Default prompt template."""
        return """You are an AI agent with the following capabilities:

{tools}

Current context:
{memory}

User request:
{input}

Please respond with either:
1. A tool call to execute an action
2. A final response to the user

Your response:"""
    
    def build(
        self,
        input_data: BaseModel,
        memory_context: List[Dict[str, Any]],
        tools: List[Dict[str, Any]]
    ) -> str:
        """Build a prompt from components."""
        # Format tools
        tools_str = self._format_tools(tools)
        
        # Format memory
        memory_str = self._format_memory(memory_context)
        
        # Format input
        input_str = input_data.model_dump_json(indent=2)
        
        # Apply template
        prompt = self.template.format(
            tools=tools_str,
            memory=memory_str,
            input=input_str
        )
        
        return prompt
    
    def _format_tools(self, tools: List[Dict[str, Any]]) -> str:
        """Format tools for prompt."""
        if not tools:
            return "No tools available."
        
        tool_descriptions = []
        for tool in tools:
            tool_descriptions.append(
                f"- {tool.get('name', 'unknown')}: {tool.get('description', '')}"
            )
        
        return "\n".join(tool_descriptions)
    
    def _format_memory(self, memory: List[Dict[str, Any]]) -> str:
        """Format memory for prompt."""
        if not memory:
            return "No previous context."
        
        # Format last N items
        max_items = 5
        recent_memory = memory[-max_items:]
        
        memory_str = []
        for item in recent_memory:
            memory_str.append(str(item))
        
        return "\n".join(memory_str)
