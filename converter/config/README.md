# Configuration Files

This directory contains configuration files for the migration system.

## Key Components

- `config_manager.py` - Configuration manager for secure loading of settings

## Configuration Approach

The system uses a centralized configuration approach rather than separate YAML files for each component. The ConfigManager handles loading configuration from both files and environment variables.

## Security

All sensitive configuration values are loaded from environment variables rather than being stored in configuration files:

1. **API Keys**: Loaded from environment variables as needed
2. **Base URLs**: Loaded from environment variables as needed

## Usage

The configuration manager is used throughout the system to access settings:

```python
from config.config_manager import get_config_manager

config_manager = get_config_manager()
llm_config = config_manager.get_llm_config()
```