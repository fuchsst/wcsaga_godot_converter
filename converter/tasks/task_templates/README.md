# Task Templates

This directory contains structured prompt templates specifically designed for qwen-code tasks.

## Key Components

- `qwen_prompt_templates.py` - Specific templates for different qwen-code task types

## Template Types

The templates include:

1. **Code Generation Templates** - For creating new GDScript files
2. **Refactoring Templates** - For modifying existing code
3. **Bug Fixing Templates** - For correcting errors in code
4. **Test Generation Templates** - For creating unit tests
5. **Code Optimization Templates** - For improving performance
6. **Documentation Templates** - For adding code documentation

## Usage

The templates are used by the Prompt Engineering component to create precisely formatted prompts for qwen-code:

```python
from tasks.task_templates.qwen_prompt_templates import generate_qwen_generate_prompt

prompt = generate_qwen_generate_prompt(
    target_file_path="scripts/player/ship.gd",
    specification="Create a PlayerShip class that handles movement, weapons, and health"
)
```