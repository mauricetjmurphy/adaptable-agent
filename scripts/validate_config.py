#!/usr/bin/env python3
"""Config validation tool."""

import sys
import yaml
from pathlib import Path
from typing import Dict, Any


def validate_agent_config(config: Dict[str, Any], config_file: Path) -> bool:
    """Validate agent configuration."""
    errors = []
    
    # Required fields
    required_fields = ["name", "description", "chat_model", "memory", "tools"]
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")
    
    # Validate chat_model
    if "chat_model" in config:
        cm = config["chat_model"]
        if "provider" not in cm:
            errors.append("chat_model missing 'provider'")
        if "model_name" not in cm:
            errors.append("chat_model missing 'model_name'")
    
    # Validate memory
    if "memory" in config:
        mem = config["memory"]
        if "type" not in mem:
            errors.append("memory missing 'type'")
    
    # Validate tools
    if "tools" in config:
        if not isinstance(config["tools"], list):
            errors.append("tools must be a list")
    
    if errors:
        print(f"\n✗ {config_file.name} has errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print(f"✓ {config_file.name} is valid")
    return True


def validate_model_config(config: Dict[str, Any], config_file: Path) -> bool:
    """Validate model configuration."""
    errors = []
    
    # Required fields
    if "provider" not in config:
        errors.append("Missing required field: provider")
    
    if "models" not in config:
        errors.append("Missing required field: models")
    elif not isinstance(config["models"], dict):
        errors.append("models must be a dictionary")
    
    if errors:
        print(f"\n✗ {config_file.name} has errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print(f"✓ {config_file.name} is valid")
    return True


def main():
    """Validate all configuration files."""
    root_dir = Path(__file__).parent.parent
    configs_dir = root_dir / "configs"
    
    if not configs_dir.exists():
        print(f"✗ configs directory not found at {configs_dir}")
        sys.exit(1)
    
    print("Validating configuration files...\n")
    
    all_valid = True
    
    # Validate agent configs
    agent_configs_dir = configs_dir / "agents"
    if agent_configs_dir.exists():
        print("Agent Configurations:")
        for config_file in agent_configs_dir.glob("*.yaml"):
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            if not validate_agent_config(config, config_file):
                all_valid = False
    
    # Validate model configs
    model_configs_dir = configs_dir / "models"
    if model_configs_dir.exists():
        print("\nModel Configurations:")
        for config_file in model_configs_dir.glob("*.yaml"):
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            if not validate_model_config(config, config_file):
                all_valid = False
    
    print("\n" + "="*60)
    if all_valid:
        print("✓ All configurations are valid!")
        sys.exit(0)
    else:
        print("✗ Some configurations have errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
