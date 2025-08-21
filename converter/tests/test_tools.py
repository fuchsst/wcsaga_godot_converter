"""
Unit tests for the Qwen Code tools.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Add the converter directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.qwen_code_execution_tool import (
    QwenCodeExecutionTool, QwenCodeInteractiveTool
)


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
    
    @patch("tools.qwen_code_execution_tool.subprocess.Popen")
    def test_successful_execution(self, mock_popen):
        """Test successful command execution."""
        # Mock the subprocess
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("output", "")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        
        result = self.tool._run("echo 'test'")
        
        assert result is not None
        assert result["return_code"] == 0
        assert result["stdout"] == "output"
        assert result["stderr"] == ""
        
        mock_popen.assert_called_once()
    
    @patch("tools.qwen_code_execution_tool.subprocess.Popen")
    def test_execution_with_timeout(self, mock_popen):
        """Test command execution with timeout."""
        # Mock the subprocess to raise a timeout
        mock_popen.side_effect = TimeoutError("Command timed out")
        
        result = self.tool._run("sleep 10", timeout_seconds=1)
        
        assert result is not None
        assert result["return_code"] == -1
        assert "timeout" in result.get("error", "")
    
    @patch("tools.qwen_code_execution_tool.subprocess.Popen")
    def test_execution_with_exception(self, mock_popen):
        """Test command execution with exception."""
        # Mock the subprocess to raise an exception
        mock_popen.side_effect = Exception("Test exception")
        
        result = self.tool._run("invalid_command")
        
        assert result is not None
        assert result["return_code"] == -1
        assert "exception" in result.get("error", "")


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
    
    @patch("tools.qwen_code_execution_tool.subprocess.Popen")
    def test_successful_interactive_execution(self, mock_popen):
        """Test successful interactive command execution."""
        # Mock the subprocess
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("response", "")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        
        result = self.tool._run("qwen-code", "Generate a test script")
        
        assert result is not None
        assert result["return_code"] == 0
        assert result["stdout"] == "response"
        assert result["stderr"] == ""
        assert result["prompt"] == "Generate a test script"
        
        mock_popen.assert_called_once()
    
    @patch("tools.qwen_code_execution_tool.subprocess.Popen")
    def test_interactive_execution_with_timeout(self, mock_popen):
        """Test interactive command execution with timeout."""
        # Mock the subprocess to raise a timeout
        mock_popen.side_effect = TimeoutError("Command timed out")
        
        result = self.tool._run("qwen-code", "Generate a test script", timeout_seconds=1)
        
        assert result is not None
        assert result["return_code"] == -1
        assert "timeout" in result.get("error", "")
    
    @patch("tools.qwen_code_execution_tool.subprocess.Popen")
    def test_interactive_execution_with_exception(self, mock_popen):
        """Test interactive command execution with exception."""
        # Mock the subprocess to raise an exception
        mock_popen.side_effect = Exception("Test exception")
        
        result = self.tool._run("qwen-code", "Generate a test script")
        
        assert result is not None
        assert result["return_code"] == -1
        assert "exception" in result.get("error", "")