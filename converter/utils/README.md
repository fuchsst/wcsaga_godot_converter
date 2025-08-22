# Utilities

This directory contains shared utility functions used across the converter system.

## Key Components

- `__init__.py` - Exports utility functions for easy access

## Utility Functions

The utilities module provides:

1. **Logging Setup** - Standardized logging configuration
2. **Time Execution** - Decorator for measuring function execution time
3. **Command Execution** - Standardized command execution with timeouts and error handling
4. **Graceful Error Handling** - Decorator for graceful error handling
5. **Timestamp Generation** - Functions for generating timestamps and request IDs
6. **Duration Calculation** - Functions for calculating time durations

## Usage

The utilities are imported and used throughout the system:

```python
from converter.utils import setup_logging, time_execution

logger = setup_logging(__name__)

@time_execution
def my_function():
    # Function implementation
    pass
```