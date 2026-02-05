"""Example: Orchestrating multiple agents."""

import asyncio
from typing import List, Dict, Any
from agent.core.engine import AgentEngine
from agent.agents.email_agent import create_email_agent
from agent.agents.financial_agent import create_financial_agent
from agent.adapters.factory import AdapterFactory
from agent.models.input import ChatInput, QueryInput
from agent.observability.logger import configure_logging


class AgentOrchestrator:
    """Orchestrates multiple agents to complete complex tasks."""
    
    def __init__(self):
        self.agents: Dict[str, AgentEngine] = {}
    
    def register_agent(self, name: str, engine: AgentEngine) -> None:
        """Register an agent with the orchestrator."""
        self.agents[name] = engine
    
    async def execute_workflow(
        self,
        workflow: List[Dict[str, Any]]
    ) -> List[Any]:
        """Execute a workflow of agent tasks."""
        results = []
        
        for step in workflow:
            agent_name = step["agent"]
            input_data = step["input"]
            
            if agent_name not in self.agents:
                raise ValueError(f"Unknown agent: {agent_name}")
            
            print(f"\nExecuting step with {agent_name}...")
            result = await self.agents[agent_name].run(input_data)
            results.append(result)
        
        return results


async def main():
    """Run orchestrator example."""
    # Configure logging
    configure_logging(level="INFO")
    
    # Create adapters
    openai_adapter = AdapterFactory.create(
        provider="openai",
        model_name="gpt-4"
    )
    
    # Create orchestrator
    orchestrator = AgentOrchestrator()
    
    # Register agents
    orchestrator.register_agent(
        "email",
        AgentEngine(create_email_agent(openai_adapter))
    )
    orchestrator.register_agent(
        "financial",
        AgentEngine(create_financial_agent(openai_adapter))
    )
    
    # Define workflow
    workflow = [
        {
            "agent": "email",
            "input": ChatInput(
                message="Check my emails for any financial updates",
                conversation_id="orch_001"
            )
        },
        {
            "agent": "financial",
            "input": QueryInput(
                query="Get latest market data for mentioned stocks"
            )
        }
    ]
    
    # Execute workflow
    print("Executing multi-agent workflow...")
    results = await orchestrator.execute_workflow(workflow)
    
    print("\n=== Workflow Results ===")
    for i, result in enumerate(results, 1):
        print(f"\nStep {i}:")
        print(f"Content: {result.content}")
        print(f"Metadata: {result.metadata}")


if __name__ == "__main__":
    asyncio.run(main())
