"""Agent Engine - Stateless execution engine for all agents."""

from typing import Any, Dict, Optional
from pydantic import BaseModel

from agent.core.config import AgentConfig
from agent.core.contracts import ChatModelAdapter, MemoryProvider
from agent.models.output import BaseOutput
from agent.observability.logger import get_logger

logger = get_logger(__name__)


class AgentEngine:
    """
    Stateless agent execution engine.
    
    Responsibilities:
    - Prompt assembly
    - Chat model invocation
    - Tool call detection and execution
    - Memory loading and persistence
    - Loop control and stop conditions
    - Observability and logging
    
    Contains no domain logic - all behavior is configured via AgentConfig.
    """
    
    def __init__(self, config: AgentConfig):
        """Initialize the agent engine with configuration."""
        self.config = config
        self.chat_model: ChatModelAdapter = config.chat_model
        self.memory: MemoryProvider = config.memory
        self.tools = {tool.name: tool for tool in config.tools}
        self.max_iterations = config.max_iterations
        
    async def run(self, input_data: BaseModel) -> BaseOutput:
        """
        Execute the agent with the given input.
        
        Args:
            input_data: Validated Pydantic input model
            
        Returns:
            Agent output as BaseOutput
        """
        logger.info(f"Starting agent execution with input: {input_data}")
        
        # Load memory context
        memory_context = await self.memory.load()
        logger.debug(f"Loaded memory context: {len(memory_context)} items")
        
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            logger.debug(f"Iteration {iteration}/{self.max_iterations}")
            
            # Build prompt
            prompt = self._build_prompt(input_data, memory_context)
            
            # Call chat model
            response = await self.chat_model.generate(prompt)
            
            # Check for tool calls
            if response.tool_calls:
                # Execute tools and continue loop
                tool_results = await self._execute_tools(response.tool_calls)
                await self.memory.persist(tool_results)
                memory_context.extend(tool_results)
                continue
            
            # Final response
            await self.memory.persist([response])
            logger.info("Agent execution completed successfully")
            return BaseOutput(content=response.content, metadata={"iterations": iteration})
        
        logger.warning(f"Max iterations ({self.max_iterations}) reached")
        return BaseOutput(
            content="Maximum iterations reached without final response",
            metadata={"iterations": iteration, "max_iterations_reached": True}
        )
    
    def _build_prompt(self, input_data: BaseModel, memory_context: list) -> str:
        """Assemble prompt from input, memory, and tool descriptions."""
        # TODO: Implement sophisticated prompt building
        prompt_parts = [
            f"Input: {input_data.model_dump_json()}",
            f"Context: {memory_context}",
            f"Available tools: {list(self.tools.keys())}"
        ]
        return "\n\n".join(prompt_parts)
    
    async def _execute_tools(self, tool_calls: list) -> list[Dict[str, Any]]:
        """Execute tool calls and return results."""
        results = []
        for tool_call in tool_calls:
            tool = self.tools.get(tool_call.name)
            if tool:
                logger.info(f"Executing tool: {tool_call.name}")
                result = await tool.execute(tool_call.arguments)
                results.append({"tool": tool_call.name, "result": result})
            else:
                logger.error(f"Unknown tool requested: {tool_call.name}")
                results.append({"tool": tool_call.name, "error": "Tool not found"})
        return results
