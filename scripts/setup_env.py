#!/usr/bin/env python3
"""Setup script for environment configuration."""

import os
import sys
from pathlib import Path


def create_env_file():
    """Create .env file from .env.example if it doesn't exist."""
    root_dir = Path(__file__).parent.parent
    env_file = root_dir / ".env"
    env_example = root_dir / ".env.example"
    
    if env_file.exists():
        print(f"✓ .env file already exists at {env_file}")
        return
    
    if not env_example.exists():
        print(f"✗ .env.example not found at {env_example}")
        sys.exit(1)
    
    # Copy .env.example to .env
    with open(env_example, 'r') as f:
        content = f.read()
    
    with open(env_file, 'w') as f:
        f.write(content)
    
    print(f"✓ Created .env file at {env_file}")
    print("  Please edit .env and add your API keys")


def check_python_version():
    """Check Python version."""
    if sys.version_info < (3, 10):
        print("✗ Python 3.10 or higher is required")
        print(f"  Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python version {sys.version_info.major}.{sys.version_info.minor} is supported")


def create_directories():
    """Create necessary directories."""
    root_dir = Path(__file__).parent.parent
    
    dirs = [
        root_dir / "logs",
        root_dir / "data" / "vector_store",
    ]
    
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")


def main():
    """Run environment setup."""
    print("Setting up agent environment...\n")
    
    # Check Python version
    check_python_version()
    
    # Create .env file
    create_env_file()
    
    # Create directories
    create_directories()
    
    print("\n" + "="*60)
    print("Environment setup complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Edit .env and add your API keys")
    print("2. Install dependencies: pip install -e .")
    print("3. Run an example: python examples/email_agent_example.py")
    print("4. Or use the CLI: python scripts/run_agent.py email -m 'Check my emails'")


if __name__ == "__main__":
    main()
