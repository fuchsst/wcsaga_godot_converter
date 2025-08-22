"""
Generic Command Line Tool Wrapper

This module implements a standardized, reusable pattern for integrating all external
command-line tools as reliable, agent-callable functions within the LangGraph state machine.
"""

import os
import signal
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ToolInput(BaseModel):
    """
    Standardized input for the generic tool wrapper.

    This follows the interface defined in Table 3 of the architectural document.
    """

    command: List[str] = Field(
        ..., description="The command to execute as a list of arguments"
    )
    stdin_data: Optional[str] = Field(default=None, description="Data to send to stdin")
    timeout_seconds: int = Field(
        default=300, description="Timeout for the command in seconds"
    )
    working_directory: Optional[str] = Field(
        default=None, description="Working directory for command execution"
    )


class ToolOutput(BaseModel):
    """
    Standardized output from the generic tool wrapper.

    This follows the interface defined in Table 3 of the architectural document.
    """

    return_code: int = Field(..., description="Return code from the process")
    stdout: str = Field(..., description="Standard output from the process")
    stderr: str = Field(..., description="Standard error from the process")
    timed_out: bool = Field(..., description="Whether the process timed out")
    execution_time: float = Field(
        ..., description="Time taken to execute the command in seconds"
    )


class CommandLineTool:
    """
    Standardized wrapper for all command-line tools.

    This class serves as a standardized interface for all command-line interactions,
    leveraging subprocess.Popen for fine-grained control over the tool's lifecycle.
    """

    def __init__(self, name: str = "CommandLineTool"):
        """
        Initialize the CommandLineTool wrapper.

        Args:
            name: Name of the tool for logging purposes
        """
        self.name = name

    def execute(self, tool_input: ToolInput) -> ToolOutput:
        """
        Execute a command-line tool with standardized input/output.

        Args:
            tool_input: ToolInput object with command and parameters

        Returns:
            ToolOutput object with structured results
        """
        import time

        start_time = time.time()

        try:
            # Create the process
            process = subprocess.Popen(
                tool_input.command,
                stdin=subprocess.PIPE if tool_input.stdin_data else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=tool_input.working_directory or os.getcwd(),
            )

            # Communicate with the process
            stdout, stderr = process.communicate(
                input=tool_input.stdin_data, timeout=tool_input.timeout_seconds
            )

            execution_time = time.time() - start_time

            return ToolOutput(
                return_code=process.returncode,
                stdout=stdout,
                stderr=stderr,
                timed_out=False,
                execution_time=execution_time,
            )

        except subprocess.TimeoutExpired as e:
            # Handle timeout
            execution_time = time.time() - start_time

            # Try to terminate the process
            try:
                process.kill()
                process.wait(timeout=5)
            except:
                pass  # If we can't kill it, not much we can do

            return ToolOutput(
                return_code=-1,
                stdout=getattr(e, "stdout", ""),
                stderr=f"Command timed out after {tool_input.timeout_seconds} seconds",
                timed_out=True,
                execution_time=execution_time,
            )

        except Exception as e:
            # Handle other exceptions
            execution_time = time.time() - start_time

            return ToolOutput(
                return_code=-1,
                stdout="",
                stderr=str(e),
                timed_out=False,
                execution_time=execution_time,
            )


# Specific tool implementations using the generic wrapper


class GodotTool:
    """
    Wrapper for the Godot engine command-line interface.

    This tool can be used for compilation checks and scene execution.
    """

    def __init__(self, godot_command: str = "godot"):
        """
        Initialize the GodotTool.

        Args:
            godot_command: Command to invoke Godot (e.g., "godot", "/path/to/godot")
        """
        self.godot_command = godot_command
        self.generic_tool = CommandLineTool("GodotTool")

    def check_syntax(self, script_path: str, timeout_seconds: int = 30) -> ToolOutput:
        """
        Check the syntax of a GDScript file.

        Args:
            script_path: Path to the GDScript file to check
            timeout_seconds: Timeout for the command

        Returns:
            ToolOutput with syntax check results
        """
        tool_input = ToolInput(
            command=[self.godot_command, "--check-only", "--script", script_path],
            timeout_seconds=timeout_seconds,
        )
        return self.generic_tool.execute(tool_input)

    def run_scene(
        self, scene_path: str, headless: bool = True, timeout_seconds: int = 300
    ) -> ToolOutput:
        """
        Run a Godot scene.

        Args:
            scene_path: Path to the scene file to run
            headless: Whether to run in headless mode
            timeout_seconds: Timeout for the command

        Returns:
            ToolOutput with scene execution results
        """
        command = [self.godot_command]
        if headless:
            command.append("--headless")
        command.extend(["--path", ".", "-s", scene_path])

        tool_input = ToolInput(command=command, timeout_seconds=timeout_seconds)
        return self.generic_tool.execute(tool_input)


class GdUnit4Tool:
    """
    Wrapper for the gdUnit4 testing framework command-line interface.

    This tool can execute test suites and generate JUnit XML reports.
    """

    def __init__(self, godot_command: str = "godot"):
        """
        Initialize the GdUnit4Tool.

        Args:
            godot_command: Command to invoke Godot (e.g., "godot", "/path/to/godot")
        """
        self.godot_command = godot_command
        self.generic_tool = CommandLineTool("GdUnit4Tool")

    def run_tests(
        self,
        test_path: str,
        generate_xml: bool = True,
        output_file: str = "results.xml",
        timeout_seconds: int = 600,
    ) -> ToolOutput:
        """
        Run gdUnit4 tests.

        Args:
            test_path: Path to test file or directory
            generate_xml: Whether to generate JUnit XML report
            output_file: Path for XML output file
            timeout_seconds: Timeout for the command

        Returns:
            ToolOutput with test execution results
        """
        command = [self.godot_command, "--headless", "--path", ".", "-s", test_path]

        if generate_xml:
            # Note: This assumes gdUnit4 supports JUnit XML output via command line
            # The actual implementation might vary based on gdUnit4's CLI interface
            command.extend(["--junit-xml", output_file])

        tool_input = ToolInput(command=command, timeout_seconds=timeout_seconds)
        return self.generic_tool.execute(tool_input)


def main():
    """Main function for testing the CommandLineTool implementations."""
    # Test the generic tool
    generic_tool = CommandLineTool()
    tool_input = ToolInput(command=["echo", "Hello, World!"], timeout_seconds=10)
    result = generic_tool.execute(tool_input)
    print("Generic tool result:", result)

    # Test GodotTool (if Godot is available)
    godot_tool = GodotTool()
    # result = godot_tool.check_syntax("test.gd")  # Only run if you have a test file
    # print("Godot syntax check result:", result)

    # Test GdUnit4Tool (if Godot and gdUnit4 are available)
    gdunit4_tool = GdUnit4Tool()
    # result = gdunit4_tool.run_tests("test_script.gd")  # Only run if you have tests
    # print("GdUnit4 test result:", result)


if __name__ == "__main__":
    main()
