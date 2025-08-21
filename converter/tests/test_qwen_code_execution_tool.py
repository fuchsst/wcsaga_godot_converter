"""
Tests for QwenCodeExecutionTool

This module contains tests for the QwenCodeExecutionTool and related components.
"""

import unittest
import tempfile
import os
from pathlib import Path

# Import the tools to test
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from tools.qwen_code_execution_tool import QwenCodeExecutionTool, QwenCodeInteractiveTool


class TestQwenCodeExecutionTool(unittest.TestCase):
    """Test cases for QwenCodeExecutionTool."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tool = QwenCodeExecutionTool()
    
    def test_initialization(self):
        """Test that the tool initializes correctly."""
        self.assertEqual(self.tool.name, "Qwen Code CLI Execution Tool")
        self.assertEqual(self.tool.description, "Executes qwen-code shell commands non-interactively, captures output, and returns results.")
    
    def test_run_successful_command(self):
        """Test running a successful command."""
        result = self.tool._run("echo 'Hello, World!'")
        
        self.assertEqual(result["return_code"], 0)
        self.assertIn("Hello, World!", result["stdout"])
        self.assertEqual(result["stderr"], "")
    
    def test_run_failing_command(self):
        """Test running a command that fails."""
        result = self.tool._run("exit 1")
        
        self.assertNotEqual(result["return_code"], 0)
        self.assertEqual(result["stdout"], "")
    
    def test_run_with_timeout(self):
        """Test running a command with a timeout."""
        result = self.tool._run("sleep 1", timeout_seconds=2)
        
        self.assertEqual(result["return_code"], 0)
    
    def test_run_timeout_exceeded(self):
        """Test that a command times out when it exceeds the timeout."""
        result = self.tool._run("sleep 3", timeout_seconds=1)
        
        self.assertEqual(result["return_code"], -1)
        self.assertIn("timed out", result["stderr"])


class TestQwenCodeInteractiveTool(unittest.TestCase):
    """Test cases for QwenCodeInteractiveTool."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tool = QwenCodeInteractiveTool()
    
    def test_initialization(self):
        """Test that the tool initializes correctly."""
        self.assertEqual(self.tool.name, "Qwen Code Interactive Tool")
        self.assertEqual(self.tool.description, "Interactively communicates with qwen-code, sending prompts and receiving responses.")
    
    def test_run_interactive_command(self):
        """Test running an interactive command."""
        # This is a basic test - in reality, we'd need to mock qwen-code
        result = self.tool._run("cat", "Hello, World!")
        
        # For the cat command, the input should be echoed to stdout
        self.assertIn("Hello, World!", result["stdout"])


if __name__ == "__main__":
    unittest.main()
