# Configuration Files

This directory contains configuration files for the migration system.

- `crewai_config.yaml` - Main CrewAI configuration with DeepSeek V3.1 settings (legacy)
- `agent_config.yaml` - Agent-specific configurations
- `tool_config.yaml` - Tool-specific configurations
- `project_settings.yaml` - Project-specific settings

## Key Components

- `config_manager.py` - Configuration manager for secure loading of settings
- `crewai_config.yaml` - Legacy CrewAI configuration (to be deprecated)
- `langgraph_config.yaml` - New LangGraph configuration
- `agent_config.yaml` - Agent-specific configurations
- `tool_config.yaml` - Tool-specific configurations
- `project_settings.yaml` - Project-specific settings

## Security

All sensitive configuration values are loaded from environment variables rather than being stored in configuration files:

1. **API Keys**: The DeepSeek API key is loaded from the `DEEPSEEK_API_KEY` environment variable
2. **Base URLs**: The DeepSeek base URL is loaded from the `DEEPSEEK_BASE_URL` environment variable