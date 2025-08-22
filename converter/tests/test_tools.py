"""
Unit tests for the Qwen Code tools.
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Add the converter directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tools.qwen_code_execution_tool import (QwenCodeExecutionTool,
                                            QwenCodeInteractiveTool)

from converter.utils import CommandExecutor


class TestQwenCodeExecutionTool:
    """Test cases for the QwenCodeExecutionTool class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.tool = QwenCodeExecutionTool()

    def test_tool_initialization(self):
        """Test that QwenCodeExecutionTool initializes correctly."""
        assert self.tool is not None
        assert self.tool.name == "Qwen Code CLI Execution Tool"
        assert self.tool.description is not None
        assert self.tool.args_schema is not None

    @patch("converter.utils.CommandExecutor.execute_command")
    def test_successful_execution(self, mock_execute):
        """Test successful command execution."""
        # Mock the command execution
        mock_execute.return_value = {
            "command": "echo 'test'",
            "return_code": 0,
            "stdout": "output",
            "stderr": "",
            "execution_time": 1234567890.0,
        }

        result = self.tool._run("echo 'test'")

        assert result is not None
        assert result["return_code"] == 0
        assert result["stdout"] == "output"
        assert result["stderr"] == ""

        mock_execute.assert_called_once_with(
            command="echo 'test'", timeout_seconds=300, working_directory=None
        )

    @patch("converter.utils.CommandExecutor.execute_command")
    def test_execution_with_timeout(self, mock_execute):
        """Test command execution with timeout."""
        # Mock the command execution to return timeout result
        mock_execute.return_value = {
            "command": "sleep 10",
            "return_code": -1,
            "stdout": "",
            "stderr": "Command timed out after 1 seconds",
            "error": "timeout",
            "execution_time": 1234567890.0,
        }

        result = self.tool._run("sleep 10", timeout_seconds=1)

        assert result is not None
        assert result["return_code"] == -1
        assert "timeout" in result.get("error", "")

        mock_execute.assert_called_once_with(
            command="sleep 10", timeout_seconds=1, working_directory=None
        )

    @patch("converter.utils.CommandExecutor.execute_command")
    def test_execution_with_exception(self, mock_execute):
        """Test command execution with exception."""
        # Mock the command execution to return exception result
        mock_execute.return_value = {
            "command": "invalid_command",
            "return_code": -1,
            "stdout": "",
            "stderr": "Test exception",
            "error": "exception",
            "execution_time": 1234567890.0,
        }

        result = self.tool._run("invalid_command")

        assert result is not None
        assert result["return_code"] == -1
        assert "exception" in result.get("error", "")

        mock_execute.assert_called_once_with(
            command="invalid_command", timeout_seconds=300, working_directory=None
        )


class TestQwenCodeInteractiveTool:
    """Test cases for the QwenCodeInteractiveTool class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.tool = QwenCodeInteractiveTool()

    def test_tool_initialization(self):
        """Test that QwenCodeInteractiveTool initializes correctly."""
        assert self.tool is not None
        assert self.tool.name == "Qwen Code Interactive Tool"
        assert self.tool.description is not None
        assert self.tool.args_schema is not None

    @patch("converter.utils.CommandExecutor.execute_command")
    def test_successful_interactive_execution(self, mock_execute):
        """Test successful interactive command execution."""
        # Mock the command execution
        mock_execute.return_value = {
            "command": "qwen-code",
            "return_code": 0,
            "stdout": "response",
            "stderr": "",
            "execution_time": 1234567890.0,
        }

        result = self.tool._run("qwen-code", "Generate a test script")

        assert result is not None
        assert result["return_code"] == 0
        assert result["stdout"] == "response"
        assert result["stderr"] == ""
        assert result["prompt"] == "Generate a test script"

        mock_execute.assert_called_once_with(
            command="qwen-code",
            timeout_seconds=300,
            working_directory=None,
            input_data="Generate a test script",
        )

    @patch("converter.utils.CommandExecutor.execute_command")
    def test_interactive_execution_with_timeout(self, mock_execute):
        """Test interactive command execution with timeout."""
        # Mock the command execution to return timeout result
        mock_execute.return_value = {
            "command": "qwen-code",
            "return_code": -1,
            "stdout": "",
            "stderr": "Command timed out after 1 seconds",
            "error": "timeout",
            "execution_time": 1234567890.0,
        }

        result = self.tool._run(
            "qwen-code", "Generate a test script", timeout_seconds=1
        )

        assert result is not None
        assert result["return_code"] == -1
        assert "timeout" in result.get("error", "")
        assert result["prompt"] == "Generate a test script"

        mock_execute.assert_called_once_with(
            command="qwen-code",
            timeout_seconds=1,
            working_directory=None,
            input_data="Generate a test script",
        )

    @patch("converter.utils.CommandExecutor.execute_command")
    def test_interactive_execution_with_exception(self, mock_execute):
        """Test interactive command execution with exception."""
        # Mock the command execution to return exception result
        mock_execute.return_value = {
            "command": "qwen-code",
            "return_code": -1,
            "stdout": "",
            "stderr": "Test exception",
            "error": "exception",
            "execution_time": 1234567890.0,
        }

        result = self.tool._run("qwen-code", "Generate a test script")

        assert result is not None
        assert result["return_code"] == -1
        assert "exception" in result.get("error", "")
        assert result["prompt"] == "Generate a test script"

        mock_execute.assert_called_once_with(
            command="qwen-code",
            timeout_seconds=300,
            working_directory=None,
            input_data="Generate a test script",
        )
