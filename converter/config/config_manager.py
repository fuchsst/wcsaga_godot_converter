"""
Configuration Manager for the Migration System

This module handles loading configuration from YAML files and environment variables,
ensuring that sensitive information is properly secured.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class ConfigManager:
    """Manages configuration loading from files and environment variables."""

    def __init__(self, config_dir: str = "config"):
        """
        Initialize the configuration manager.

        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir)
        self._config = {}
        self._load_all_configurations()

    def _load_all_configurations(self):
        """Load all configuration files."""
        # Load all YAML configuration files
        for config_file in self.config_dir.glob("*.yaml"):
            config_name = config_file.stem
            self._config[config_name] = self._load_yaml_config(config_file)

    def _load_yaml_config(self, config_path: Path) -> Dict[str, Any]:
        """
        Load configuration from a YAML file.

        Args:
            config_path: Path to the YAML configuration file

        Returns:
            Dictionary with configuration data
        """
        try:
            with open(config_path, "r") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            raise ValueError(
                f"Failed to load configuration from {config_path}: {str(e)}"
            )

    def get_config(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            section: Configuration section name
            key: Configuration key
            default: Default value if not found

        Returns:
            Configuration value
        """
        section_config = self._config.get(section, {})
        return section_config.get(key, default)

    def get_nested_config(self, section: str, *keys: str, default: Any = None) -> Any:
        """
        Get a nested configuration value.

        Args:
            section: Configuration section name
            keys: Nested keys to traverse
            default: Default value if not found

        Returns:
            Configuration value
        """
        section_config = self._config.get(section, {})
        current = section_config

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default

        return current

    def get_secret(self, env_var: str, default: str = None) -> str:
        """
        Get a secret from environment variables.

        Args:
            env_var: Environment variable name
            default: Default value if not found

        Returns:
            Secret value from environment variable
        """
        return os.environ.get(env_var, default)

    def get_llm_config(self) -> Dict[str, Any]:
        """
        Get LLM configuration with secrets loaded from environment variables.

        Returns:
            Dictionary with LLM configuration
        """
        llm_config = self._config.get("llm", {})

        # Load API key from environment variable
        api_key_env_var = llm_config.get("api_key_env_var", "DEEPSEEK_API_KEY")
        api_key = self.get_secret(api_key_env_var)

        # Load base URL from environment variable
        base_url_env_var = llm_config.get("base_url_env_var", "DEEPSEEK_BASE_URL")
        base_url = self.get_secret(base_url_env_var)

        # Remove the environment variable names from the config
        llm_config_copy = llm_config.copy()
        llm_config_copy.pop("api_key_env_var", None)
        llm_config_copy.pop("base_url_env_var", None)

        # Remove any existing api_key from the config
        llm_config_copy.pop("api_key", None)

        # Add the actual values only if they exist
        if api_key:
            llm_config_copy["api_key"] = api_key
        if base_url:
            llm_config_copy["base_url"] = base_url

        return llm_config_copy

    def get_agent_config(self, agent_type: str = "default") -> Dict[str, Any]:
        """
        Get agent configuration.

        Args:
            agent_type: Type of agent configuration to get

        Returns:
            Dictionary with agent configuration
        """
        if agent_type == "default":
            return self._config.get("agents", {}).get("default", {})
        else:
            return self._config.get("agents", {}).get(agent_type, {})

    def get_process_config(self, process_type: str) -> Dict[str, Any]:
        """
        Get process configuration.

        Args:
            process_type: Type of process configuration to get

        Returns:
            Dictionary with process configuration
        """
        return self._config.get("process", {}).get(process_type, {})

    def get_memory_config(self) -> Dict[str, Any]:
        """
        Get memory configuration.

        Returns:
            Dictionary with memory configuration
        """
        return self._config.get("memory", {})

    def validate_config(self) -> bool:
        """
        Validate that all required configuration is present.

        Returns:
            True if configuration is valid, False otherwise
        """
        # Check that we have LLM configuration
        llm_config = self._config.get("llm", {})
        if not llm_config.get("model"):
            return False

        # Check that required environment variables are set
        api_key_env_var = llm_config.get("api_key_env_var", "DEEPSEEK_API_KEY")
        if not os.environ.get(api_key_env_var):
            # This is a warning, not an error, as the system might work in some cases without API key
            pass

        return True

    def get_graph_config(self) -> Dict[str, Any]:
        """
        Get graph configuration for LangGraph orchestrator.

        Returns:
            Dictionary with graph configuration
        """
        return self._config.get("graph", {})


# Global configuration manager instance
config_manager = ConfigManager()


def get_config_manager() -> ConfigManager:
    """
    Get the global configuration manager instance.

    Returns:
        ConfigManager instance
    """
    return config_manager
