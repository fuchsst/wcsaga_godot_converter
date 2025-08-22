# CLI Agent Tools

This directory contains wrappers for the CLI coding agents.

The system standardizes on a single, powerful CLI coding agent: **qwen-code**.

qwen-code is built upon Alibaba's state-of-the-art Qwen3-Coder models, which are distinguished by their massive context windows and strong performance in complex, agentic coding tasks.

The tools in this directory are designed to work specifically with the qwen-code CLI agent:

- `qwen_code_wrapper.py` - Wrapper for the qwen-code CLI agent
- `qwen_code_execution_tool.py` - Base tool for executing qwen-code commands

## Integration with Other Systems

The CLI Agent Tools integrate with several systems:

- **Prompt Engineering**: Receive precisely formatted prompts from the Prompt Engineering component
- **Validation System**: Provide execution results to the Validation Engineer
- **Refactoring Specialist**: Execute code generation tasks for the Refactoring Specialist
- **Test Generator**: Execute test generation tasks for the Test Generator