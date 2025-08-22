# CLI Agent Tools and Generic Tool Framework

This directory contains wrappers for the CLI coding agents as part of the Unified Tool Framework, implementing the Generic Tool-Wrapping Pattern recommended in the architectural document.

The system standardizes on a single, powerful CLI coding agent: **qwen-code**.

qwen-code is built upon Alibaba's state-of-the-art Qwen3-Coder models, which are distinguished by their massive context windows and strong performance in complex, agentic coding tasks.

## Key Components

- `qwen_code_wrapper.py` - Wrapper for the qwen-code CLI agent with high-context generation capabilities
- `qwen_code_execution_tool.py` - Base tool for executing qwen-code commands with structured I/O interface
- `command_line_tool.py` - Generic tool framework implementing the standardized CommandLineTool wrapper pattern

## Unified Tool Framework

The system implements a Generic Tool-Wrapping Pattern using a reusable Python wrapper class that serves as a standardized interface for all command-line interactions. It leverages the subprocess.Popen interface to gain fine-grained control over the tool's lifecycle, allowing it to programmatically write to stdin, capture and buffer stdout and stderr streams, enforce configurable timeouts, and interpret process exit codes.

The output of this wrapper is a structured data object defined using a Pydantic model, containing the return code, the complete stdout and stderr logs, and a flag indicating if the process timed out.

### Standardized Tool I/O Interface

Following the recommendations in the architectural document, we implement a standardized I/O interface:

| Interface | Model Name | Fields | Description |
| :---- | :---- | :---- | :---- |
| Input | ToolInput | command: List[str], stdin_data: Optional[str], timeout_seconds: int | The standardized input passed to the generic tool wrapper. |
| Output | ToolOutput | return_code: int, stdout: str, stderr: str, timed_out: bool | The structured result returned by the wrapper, ready for state update and analysis by subsequent nodes. |

## Specific Tool Implementations

The framework includes specific implementations for key tools in the migration process:

1. **GodotTool** - For headless Godot operations including compilation checks and scene execution
2. **GdUnit4Tool** - For executing tests and generating JUnit XML reports
3. **QwenCodeTool** - Specialized wrapper for the qwen-code CLI agent

## Integration with Other Systems

The CLI Agent Tools integrate with several systems:

- **Prompt Engineering**: Receive precisely formatted prompts from the Prompt Engineering component
- **Validation System**: Provide execution results to the Validation Engineer with structured outputs
- **Refactoring Specialist**: Execute code generation tasks for the Refactoring Specialist
- **Test Generator**: Execute test generation tasks for the Test Generator
- **Orchestrator**: Serve as callable tools within the LangGraph state machine workflow