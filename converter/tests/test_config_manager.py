"""
Unit tests for the configuration manager.
"""

import os
import sys
import tempfile
import yaml
from pathlib import Path
import pytest

# Add the converter directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestConfigManager:
    """Test cases for the ConfigManager class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a temporary directory for test configuration files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.temp_dir.name)
        
        # Create test configuration files
        self._create_test_configs()
    
    def teardown_method(self):
        """Tear down test fixtures after each test method."""
        self.temp_dir.cleanup()
    
    def _create_test_configs(self):
        """Create test configuration files."""
        # Create llm_config.yaml
        llm_config = {
            "model": "deepseek-ai/DeepSeek-V3.1",
            "temperature": 0.7,
            "max_tokens": 4096,
            "base_url": "https://api.deepseek.com/v1",
            "api_key_env_var": "DEEPSEEK_API_KEY"
        }
        
        with open(self.config_dir / "llm.yaml", "w") as f:
            yaml.dump(llm_config, f)
        
        # Create agent_config.yaml
        agent_config = {
            "default": {
                "verbose": True,
                "allow_delegation": True,
                "max_rpm": 60,
                "cache": True
            },
            "migration_architect": {
                "role": "Lead Systems Architect",
                "goal": "Decompose the overall migration into a high-level, phased project plan"
            },
            "codebase_analyst": {
                "role": "Senior Software Analyst",
                "goal": "Analyze the legacy codebase to identify dependencies, modules, and architectural patterns"
            }
        }
        
        with open(self.config_dir / "agents.yaml", "w") as f:
            yaml.dump(agent_config, f)
        
        # Create process_config.yaml
        process_config = {
            "sequential": {
                "timeout": 300
            },
            "hierarchical": {
                "manager_llm": "deepseek-ai/DeepSeek-V3.1",
                "timeout": 600
            }
        }
        
        with open(self.config_dir / "process.yaml", "w") as f:
            yaml.dump(process_config, f)
    
    def test_config_manager_initialization(self):
        """Test that ConfigManager initializes correctly."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        assert config_manager is not None
        assert hasattr(config_manager, "_config")
    
    def test_load_yaml_config(self):
        """Test loading configuration from YAML files."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        # Check that configurations were loaded
        llm_config = config_manager._config.get("llm", {})
        assert llm_config is not None
        assert "model" in llm_config
        
        agent_config = config_manager._config.get("agents", {})
        assert agent_config is not None
    
    def test_get_config(self):
        """Test getting configuration values."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        # Test getting a simple configuration value
        model = config_manager.get_config("llm", "model", "default_model")
        assert model == "deepseek-ai/DeepSeek-V3.1"
        
        # Test getting a non-existent configuration with default
        default_value = config_manager.get_config("nonexistent", "key", "default")
        assert default_value == "default"
    
    def test_get_nested_config(self):
        """Test getting nested configuration values."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        # Test getting a nested configuration value
        temperature = config_manager.get_nested_config("llm", "temperature")
        assert temperature == 0.7
        
        # Test getting a nested configuration with default
        default_value = config_manager.get_nested_config("llm", "nonexistent", default="default")
        assert default_value == "default"
    
    def test_get_secret(self):
        """Test getting secrets from environment variables."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        # Test getting a secret that doesn't exist
        secret = config_manager.get_secret("NONEXISTENT_SECRET", "default_secret")
        assert secret == "default_secret"
        
        # Test getting a secret that exists
        os.environ["TEST_SECRET"] = "test_value"
        secret = config_manager.get_secret("TEST_SECRET")
        assert secret == "test_value"
        del os.environ["TEST_SECRET"]
    
    def test_get_llm_config(self):
        """Test getting LLM configuration with secrets."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        # Test without environment variable set
        llm_config = config_manager.get_llm_config()
        assert "model" in llm_config
        assert llm_config["model"] == "deepseek-ai/DeepSeek-V3.1"
        assert "api_key" not in llm_config  # Should not be present without env var
        
        # Test with environment variable set
        os.environ["DEEPSEEK_API_KEY"] = "test_api_key"
        llm_config = config_manager.get_llm_config()
        assert "api_key" in llm_config
        assert llm_config["api_key"] == "test_api_key"
        del os.environ["DEEPSEEK_API_KEY"]
    
    def test_get_agent_config(self):
        """Test getting agent configuration."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        # Test getting default agent configuration
        default_agent_config = config_manager.get_agent_config("default")
        assert default_agent_config is not None
        assert default_agent_config.get("verbose") is True
        
        # Test getting specific agent configuration
        architect_config = config_manager.get_agent_config("migration_architect")
        assert architect_config is not None
        assert architect_config.get("role") == "Lead Systems Architect"
    
    def test_get_process_config(self):
        """Test getting process configuration."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        # Test getting sequential process configuration
        sequential_config = config_manager.get_process_config("sequential")
        assert sequential_config is not None
        assert sequential_config.get("timeout") == 300
        
        # Test getting hierarchical process configuration
        hierarchical_config = config_manager.get_process_config("hierarchical")
        assert hierarchical_config is not None
        assert hierarchical_config.get("timeout") == 600
    
    def test_validate_config(self):
        """Test configuration validation."""
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager(str(self.config_dir))
        
        # Test with valid configuration
        is_valid = config_manager.validate_config()
        assert is_valid is True