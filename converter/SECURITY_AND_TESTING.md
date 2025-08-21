# Security and Testing Guide

This document explains how to use the security features and run tests for the Wing Commander Saga to Godot migration system.

## Security Features

The migration system implements several security best practices to protect sensitive information:

### Environment Variables for Secrets

All sensitive configuration values are loaded from environment variables rather than being stored in configuration files:

1. **API Keys**: The DeepSeek API key is loaded from the `DEEPSEEK_API_KEY` environment variable
2. **Base URLs**: The DeepSeek base URL is loaded from the `DEEPSEEK_BASE_URL` environment variable

### Configuration Manager

The `ConfigManager` class in `config/config_manager.py` handles the secure loading of configuration:

```python
# Load API key from environment variable
api_key = config_manager.get_secret("DEEPSEEK_API_KEY")

# Load base URL from environment variable  
base_url = config_manager.get_secret("DEEPSEEK_BASE_URL")
```

### Setting Environment Variables

To set the required environment variables, you can:

1. **Export directly in your shell**:
   ```bash
   export DEEPSEEK_API_KEY="your-api-key-here"
   export DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"
   ```

2. **Use a .env file**:
   Create a `.env` file in the converter directory:
   ```
   DEEPSEEK_API_KEY=your-api-key-here
   DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
   ```

3. **Set in your system environment**:
   Add the variables to your system's environment configuration

## Running Tests

The system includes unit tests for all major components:

### Test Files

- `tests/test_config_manager.py` - Tests for the configuration manager
- `tests/test_agents.py` - Tests for the agent implementations
- `tests/test_orchestrator.py` - Tests for the migration orchestrator
- `tests/test_tools.py` - Tests for the Qwen Code tools
- `tests/test_tasks.py` - Tests for the task configurations

### Running Tests

1. **Run all tests**:
   ```bash
   cd converter
   python -m pytest tests/ -v
   ```

2. **Run a specific test file**:
   ```bash
   cd converter
   python -m pytest tests/test_config_manager.py -v
   ```

3. **Run the quick test script**:
   ```bash
   cd converter
   ./run_tests.sh
   ```

### Test Coverage

The tests cover:

- Configuration loading and validation
- Agent initialization and configuration
- Orchestrator setup and operation
- Tool functionality
- Task configuration loading
- Security features (environment variable loading)

## Best Practices

1. **Never commit secrets**: Never store API keys or other secrets in configuration files that are committed to version control
2. **Use environment variables**: Always load sensitive information from environment variables
3. **Validate configuration**: Use the configuration manager's validation methods to ensure all required settings are present
4. **Run tests regularly**: Run tests after making changes to ensure the system continues to work correctly
5. **Update tests**: Add new tests when adding new functionality

## Troubleshooting

If you encounter issues:

1. **Missing environment variables**: Ensure all required environment variables are set
2. **Configuration loading errors**: Check that configuration files are properly formatted YAML
3. **Import errors**: Ensure the Python path includes the converter directory
4. **Test failures**: Check the specific error messages and ensure all dependencies are installed