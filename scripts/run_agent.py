#!/usr/bin/env python3
"""CLI tool for running agents."""

import argparse
import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent.core.engine import AgentEngine
from agent.agents.email_agent import create_email_agent
from agent.agents.financial_agent import create_financial_agent
from agent.agents.document_agent import create_document_agent
from agent.adapters.factory import AdapterFactory
from agent.models.input import ChatInput, QueryInput, TaskInput
from agent.observability.logger import configure_logging
from dotenv import load_dotenv


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run an agent")
    parser.add_argument(
        "agent",
        choices=["email", "financial", "document"],
        help="Agent type to run"
    )
    parser.add_argument(
        "--message",
        "-m",
        help="Message/query/task for the agent",
        required=True
    )
    parser.add_argument(
        "--provider",
        default="openai",
        choices=["openai", "anthropic"],
        help="LLM provider"
    )
    parser.add_argument(
        "--model",
        default="gpt-4",
        help="Model name"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Model temperature"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level"
    )
    
    return parser.parse_args()


async def run_agent(args):
    """Run the specified agent."""
    # Load environment variables
    load_dotenv()
    
    # Configure logging
    configure_logging(level=args.log_level)
    
    # Create adapter
    api_key_env = f"{args.provider.upper()}_API_KEY"
    api_key = os.getenv(api_key_env)
    
    if not api_key:
        print(f"Error: {api_key_env} not found in environment")
        sys.exit(1)
    
    adapter = AdapterFactory.create(
        provider=args.provider,
        model_name=args.model,
        temperature=args.temperature,
        api_key=api_key
    )
    
    # Create agent configuration
    if args.agent == "email":
        config = create_email_agent(adapter)
        input_data = ChatInput(message=args.message)
    elif args.agent == "financial":
        config = create_financial_agent(adapter)
        input_data = QueryInput(query=args.message)
    elif args.agent == "document":
        config = create_document_agent(adapter)
        input_data = TaskInput(task=args.message)
    else:
        print(f"Error: Unknown agent type: {args.agent}")
        sys.exit(1)
    
    # Create engine and run
    engine = AgentEngine(config)
    
    print(f"\n{'='*60}")
    print(f"Running {args.agent} agent with {args.provider}/{args.model}")
    print(f"{'='*60}\n")
    
    try:
        result = await engine.run(input_data)
        
        print(f"\n{'='*60}")
        print("Agent Response:")
        print(f"{'='*60}")
        print(f"\n{result.content}\n")
        
        if result.metadata:
            print(f"\nMetadata: {result.metadata}")
        
        print(f"\nSuccess: {result.success}")
        
        if result.error:
            print(f"Error: {result.error}")
            
    except Exception as e:
        print(f"\nError running agent: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    args = parse_args()
    asyncio.run(run_agent(args))


if __name__ == "__main__":
    main()
