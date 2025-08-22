"""
Qwen Code Execution Tool

This tool provides a wrapper for executing qwen-code CLI commands.
It uses subprocess.Popen for interactive control of the qwen-code process.
"""

from typing import Any, Callable, Dict, Optional

from pydantic import BaseModel, Field

from converter.utils import CommandExecutor


class BaseTool:
    """Base class for tools."""

    name: str = "Base Tool"
    description: str = "A base tool implementation"
    args_schema: type[BaseModel] = BaseModel

    def _run(self, **kwargs) -> Dict[str, Any]:
        """Run the tool with the given arguments."""
        raise NotImplementedError("Subclasses must implement _run method")

    def run(self, **kwargs) -> Dict[str, Any]:
        """Run the tool with validation."""
        return self._run(**kwargs)


class QwenCodeExecutionInput(BaseModel):
    """Input schema for the QwenCodeExecutionTool."""

    command: str = Field(..., description="The full shell command to be executed.")
    timeout_seconds: int = Field(
        default=300, description="Timeout for the command in seconds."
    )
    working_directory: Optional[str] = Field(
        default=None, description="Working directory for command execution."
    )


class QwenCodeInteractiveInput(BaseModel):
    """Input schema for the QwenCodeInteractiveTool."""

    command: str = Field(..., description="The qwen-code command to execute.")
    prompt: str = Field(..., description="The prompt to send to qwen-code.")
    timeout_seconds: int = Field(
        default=300, description="Timeout for the command in seconds."
    )
    working_directory: Optional[str] = Field(
        default=None, description="Working directory for command execution."
    )


class QwenCodeExecutionTool(BaseTool):
    """Tool for executing qwen-code CLI commands with interactive control."""

    name: str = "Qwen Code CLI Execution Tool"
    description: str = (
        "Executes qwen-code shell commands non-interactively, captures output, and returns results."
    )
    args_schema: type[BaseModel] = QwenCodeExecutionInput

    def _run(
        self,
        command: str,
        timeout_seconds: int = 300,
        working_directory: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute the shell command and return a structured report of the outcome.

        Args:
            command: The full shell command to execute
            timeout_seconds: Timeout for the command in seconds
            working_directory: Working directory for command execution

        Returns:
            Dictionary with execution results including return code, stdout, stderr
        """
        return CommandExecutor.execute_command(
            command=command,
            timeout_seconds=timeout_seconds,
            working_directory=working_directory,
        )


class QwenCodeInteractiveTool(BaseTool):
    """Tool for interactive communication with qwen-code."""

    name: str = "Qwen Code Interactive Tool"
    description: str = (
        "Interactively communicates with qwen-code, sending prompts and receiving responses."
    )
    args_schema: type[BaseModel] = QwenCodeInteractiveInput

    def _run(
        self,
        command: str,
        prompt: str,
        timeout_seconds: int = 300,
        working_directory: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute qwen-code interactively by sending a prompt.

        Args:
            command: The qwen-code command to execute
            prompt: The prompt to send to qwen-code
            timeout_seconds: Timeout for the command in seconds
            working_directory: Working directory for command execution

        Returns:
            Dictionary with execution results
        """
        result = CommandExecutor.execute_command(
            command=command,
            timeout_seconds=timeout_seconds,
            working_directory=working_directory,
            input_data=prompt,
        )
        result["prompt"] = prompt
        return result
