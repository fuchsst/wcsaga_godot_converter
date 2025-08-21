"""
Unit tests for the base agent implementation.
"""

import os
import sys
import tempfile
import yaml
from pathlib import Path
import pytest

# Add the converter directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from agents.base_agent import (
    ConfigurableAgent, MigrationArchitect, CodebaseAnalyst, 
    TaskDecompositionSpecialist, PromptEngineeringAgent, QualityAssuranceAgent
)


class TestBaseAgent:
    """Test cases for the base agent implementation."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a temporary directory for test configuration files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.temp_dir.name)
        
        # Create test configuration files
        self._create_test_agent_configs()
    
    def teardown_method(self):
        """Tear down test fixtures after each test method."""
        self.temp_dir.cleanup()
    
    def _create_test_agent_configs(self):
        """Create test agent configuration files."""
        # Create migration_architect.yaml
        migration_architect_config = {
            "name": "MigrationArchitect",
            "role": "Lead Systems Architect",
            "goal": "Decompose the overall migration into a high-level, phased project plan",
            "backstory": "You are the project lead for the Wing Commander Saga to Godot migration.",
            "tools": []
        }
        
        with open(self.config_dir / "migration_architect.yaml", "w") as f:
            yaml.dump(migration_architect_config, f)
        
        # Create codebase_analyst.yaml
        codebase_analyst_config = {
            "name": "CodebaseAnalyst",
            "role": "Senior Software Analyst",
            "goal": "Analyze the legacy codebase to identify dependencies, modules, and architectural patterns",
            "backstory": "You are an expert in legacy game engine architecture with deep knowledge of C++ codebases.",
            "tools": ["FileReadTool"]
        }
        
        with open(self.config_dir / "codebase_analyst.yaml", "w") as f:
            yaml.dump(codebase_analyst_config, f)
        
        # Create task_decomposition_specialist.yaml
        task_decomposition_config = {
            "name": "TaskDecompositionSpecialist",
            "role": "Technical Project Manager",
            "goal": "Break down high-level migration phases into a sequence of atomic, executable coding tasks",
            "backstory": "You are a middle manager in the AI crew, acting as a bridge between high-level strategy and low-level execution.",
            "tools": []
        }
        
        with open(self.config_dir / "task_decomposition_specialist.yaml", "w") as f:
            yaml.dump(task_decomposition_config, f)
        
        # Create prompt_engineering_agent.yaml
        prompt_engineering_config = {
            "name": "PromptEngineeringAgent",
            "role": "AI Communications Specialist",
            "goal": "Convert atomic tasks and code context into precise, effective prompts for the CLI agent",
            "backstory": "You are a critical meta-agent that functions as the communication officer between the command crew and the execution layer.",
            "tools": []
        }
        
        with open(self.config_dir / "prompt_engineering_agent.yaml", "w") as f:
            yaml.dump(prompt_engineering_config, f)
        
        # Create quality_assurance_agent.yaml
        quality_assurance_config = {
            "name": "QualityAssuranceAgent",
            "role": "QA Automation Engineer",
            "goal": "Verify the output of CLI agent tasks, diagnose failures, and initiate corrective actions",
            "backstory": "You are responsible for verification and quality control in the AI crew.",
            "tools": ["QwenCodeExecutionTool"]
        }
        
        with open(self.config_dir / "quality_assurance_agent.yaml", "w") as f:
            yaml.dump(quality_assurance_config, f)
    
    def test_configurable_agent_initialization(self):
        """Test that ConfigurableAgent initializes correctly."""
        # Test with a valid configuration file
        config_file = self.config_dir / "migration_architect.yaml"
        agent = ConfigurableAgent(str(config_file))
        
        assert agent is not None
        assert hasattr(agent, "role")
        assert agent.role == "Lead Systems Architect"
    
    def test_migration_architect_initialization(self):
        """Test that MigrationArchitect initializes correctly."""
        # Change current working directory to the temp directory to make the relative paths work
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        
        try:
            agent = MigrationArchitect()
            
            assert agent is not None
            assert hasattr(agent, "role")
            assert agent.role == "Lead Systems Architect"
        finally:
            os.chdir(original_cwd)
    
    def test_codebase_analyst_initialization(self):
        """Test that CodebaseAnalyst initializes correctly."""
        # Change current working directory to the temp directory to make the relative paths work
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        
        try:
            agent = CodebaseAnalyst()
            
            assert agent is not None
            assert hasattr(agent, "role")
            assert agent.role == "Senior Software Analyst"
        finally:
            os.chdir(original_cwd)
    
    def test_task_decomposition_specialist_initialization(self):
        """Test that TaskDecompositionSpecialist initializes correctly."""
        # Change current working directory to the temp directory to make the relative paths work
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        
        try:
            agent = TaskDecompositionSpecialist()
            
            assert agent is not None
            assert hasattr(agent, "role")
            assert agent.role == "Technical Project Manager"
        finally:
            os.chdir(original_cwd)
    
    def test_prompt_engineering_agent_initialization(self):
        """Test that PromptEngineeringAgent initializes correctly."""
        # Change current working directory to the temp directory to make the relative paths work
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        
        try:
            agent = PromptEngineeringAgent()
            
            assert agent is not None
            assert hasattr(agent, "role")
            assert agent.role == "AI Communications Specialist"
        finally:
            os.chdir(original_cwd)
    
    def test_quality_assurance_agent_initialization(self):
        """Test that QualityAssuranceAgent initializes correctly."""
        # Change current working directory to the temp directory to make the relative paths work
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        
        try:
            agent = QualityAssuranceAgent()
            
            assert agent is not None
            assert hasattr(agent, "role")
            assert agent.role == "QA Automation Engineer"
        finally:
            os.chdir(original_cwd)