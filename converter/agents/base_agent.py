"""
Base Agent Implementation

This module provides a base class for agents that load their configurations from YAML files.
"""

import os
import yaml
from crewai import Agent
from typing import Dict, Any, Optional, List


class ConfigurableAgent(Agent):
    """Base class for agents that load configurations from YAML files."""
    
    def __init__(self, config_file: str, **kwargs):
        """
        Initialize the agent with a YAML configuration file.
        
        Args:
            config_file: Path to the YAML configuration file
            **kwargs: Additional arguments to pass to the Agent constructor
        """
        # Load the configuration from the YAML file
        config = self._load_config(config_file)
        
        # Extract agent attributes from the configuration
        role = config.get('role', '')
        goal = config.get('goal', '')
        backstory = config.get('backstory', '')
        tool_names = config.get('tools', [])
        
        # Convert tool names to actual tool instances (for now, we'll leave them as None)
        # In a real implementation, we would map tool names to actual tool instances
        tools = self._load_tools(tool_names)
        
        # Initialize the parent Agent class with the configuration
        super().__init__(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools,
            **kwargs
        )
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """
        Load agent configuration from a YAML file.
        
        Args:
            config_file: Path to the YAML configuration file
            
        Returns:
            Dictionary with agent configuration
        """
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def _load_tools(self, tool_names: List[str]) -> List[Any]:
        """
        Load tools based on their names.
        
        Args:
            tool_names: List of tool names
            
        Returns:
            List of tool instances
        """
        # For now, we'll return an empty list and add tools separately
        # In a real implementation, we would map tool names to actual tool instances
        return []


# Specific agent implementations
class MigrationArchitect(ConfigurableAgent):
    """Lead Systems Architect agent."""
    
    def __init__(self, **kwargs):
        """Initialize the MigrationArchitect agent."""
        config_file = os.path.join(os.path.dirname(__file__), 'migration_architect.yaml')
        super().__init__(config_file, **kwargs)


class CodebaseAnalyst(ConfigurableAgent):
    """Senior Software Analyst agent."""
    
    def __init__(self, **kwargs):
        """Initialize the CodebaseAnalyst agent."""
        config_file = os.path.join(os.path.dirname(__file__), 'codebase_analyst.yaml')
        super().__init__(config_file, **kwargs)


class TaskDecompositionSpecialist(ConfigurableAgent):
    """Technical Project Manager agent."""
    
    def __init__(self, **kwargs):
        """Initialize the TaskDecompositionSpecialist agent."""
        config_file = os.path.join(os.path.dirname(__file__), 'task_decomposition_specialist.yaml')
        super().__init__(config_file, **kwargs)


class PromptEngineeringAgent(ConfigurableAgent):
    """AI Communications Specialist agent."""
    
    def __init__(self, **kwargs):
        """Initialize the PromptEngineeringAgent agent."""
        config_file = os.path.join(os.path.dirname(__file__), 'prompt_engineering_agent.yaml')
        super().__init__(config_file, **kwargs)


class QualityAssuranceAgent(ConfigurableAgent):
    """QA Automation Engineer agent."""
    
    def __init__(self, **kwargs):
        """Initialize the QualityAssuranceAgent agent."""
        config_file = os.path.join(os.path.dirname(__file__), 'quality_assurance_agent.yaml')
        super().__init__(config_file, **kwargs)