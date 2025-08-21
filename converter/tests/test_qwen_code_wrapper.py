"""
Tests for QwenCodeWrapper

This module contains tests for the QwenCodeWrapper component.
"""

import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the wrapper to test
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from converter.tools.qwen_code_wrapper import QwenCodeWrapper


class TestQwenCodeWrapper(unittest.TestCase):
    """Test cases for QwenCodeWrapper."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.wrapper = QwenCodeWrapper()
    
    def test_initialization(self):
        """Test that the wrapper initializes correctly."""
        self.assertEqual(self.wrapper.qwen_command, "qwen-code")
        self.assertEqual(self.wrapper.timeout, 300)
    
    def test_initialization_with_custom_params(self):
        """Test initialization with custom parameters."""
        wrapper = QwenCodeWrapper(qwen_command="custom-qwen", timeout=600)
        self.assertEqual(wrapper.qwen_command, "custom-qwen")
        self.assertEqual(wrapper.timeout, 600)
    
    @patch('converter.tools.qwen_code_wrapper.QwenCodeInteractiveTool')
    def test_generate_code(self, mock_interactive_tool):
        """Test generating code with the wrapper."""
        # Mock the interactive tool response
        mock_result = {
            "return_code": 0,
            "stdout": "print('Hello, World!')",
            "stderr": ""
        }
        mock_interactive_tool.return_value._run.return_value = mock_result
        
        # Create wrapper with mocked tool
        wrapper = QwenCodeWrapper()
        wrapper.interactive_tool = mock_interactive_tool.return_value
        
        # Test code generation
        result = wrapper.generate_code("Create a simple Python script that prints 'Hello, World!'")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["generated_code"], "print('Hello, World!')")
        mock_interactive_tool.return_value._run.assert_called_once()
    
    @patch('converter.tools.qwen_code_wrapper.QwenCodeInteractiveTool')
    def test_generate_code_with_context(self, mock_interactive_tool):
        """Test generating code with context files."""
        # Mock the interactive tool response
        mock_result = {
            "return_code": 0,
            "stdout": "class MyClass:\n    pass",
            "stderr": ""
        }
        mock_interactive_tool.return_value._run.return_value = mock_result
        
        # Create wrapper with mocked tool
        wrapper = QwenCodeWrapper()
        wrapper.interactive_tool = mock_interactive_tool.return_value
        
        # Create temporary context file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("# This is a context file\nCONSTANT = 42\n")
            context_file_path = f.name
        
        try:
            # Test code generation with context
            result = wrapper.generate_code(
                "Create a class that uses the CONSTANT from context",
                context_files=[context_file_path]
            )
            
            self.assertTrue(result["success"])
            self.assertIn("class MyClass", result["generated_code"])
            mock_interactive_tool.return_value._run.assert_called_once()
        finally:
            # Clean up temporary file
            os.unlink(context_file_path)
    
    @patch('converter.tools.qwen_code_wrapper.QwenCodeInteractiveTool')
    def test_refactor_code(self, mock_interactive_tool):
        """Test refactoring code with the wrapper."""
        # Mock the interactive tool response
        mock_result = {
            "return_code": 0,
            "stdout": "refactored_code = True",
            "stderr": ""
        }
        mock_interactive_tool.return_value._run.return_value = mock_result
        
        # Create wrapper with mocked tool
        wrapper = QwenCodeWrapper()
        wrapper.interactive_tool = mock_interactive_tool.return_value
        
        # Create temporary file to refactor
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("old_code = False\n")
            file_path = f.name
        
        try:
            # Test code refactoring
            result = wrapper.refactor_code(file_path, "Refactor the code to set old_code to True")
            
            self.assertTrue(result["success"])
            self.assertEqual(result["refactored_code"], "refactored_code = True")
            mock_interactive_tool.return_value._run.assert_called_once()
        finally:
            # Clean up temporary file
            os.unlink(file_path)
    
    @patch('converter.tools.qwen_code_wrapper.QwenCodeInteractiveTool')
    def test_fix_bugs(self, mock_interactive_tool):
        """Test fixing bugs with the wrapper."""
        # Mock the interactive tool response
        mock_result = {
            "return_code": 0,
            "stdout": "fixed_code = 'No more bugs'",
            "stderr": ""
        }
        mock_interactive_tool.return_value._run.return_value = mock_result
        
        # Create wrapper with mocked tool
        wrapper = QwenCodeWrapper()
        wrapper.interactive_tool = mock_interactive_tool.return_value
        
        # Create temporary file with bugs
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("buggy_code = 'Has bugs'\n")
            file_path = f.name
        
        try:
            # Test bug fixing
            result = wrapper.fix_bugs(file_path, "SyntaxError: invalid syntax")
            
            self.assertTrue(result["success"])
            self.assertEqual(result["fixed_code"], "fixed_code = 'No more bugs'")
            mock_interactive_tool.return_value._run.assert_called_once()
        finally:
            # Clean up temporary file
            os.unlink(file_path)
    
    @patch('converter.tools.qwen_code_wrapper.QwenCodeInteractiveTool')
    def test_generate_code_failure(self, mock_interactive_tool):
        """Test handling of code generation failure."""
        # Mock the interactive tool response with failure
        mock_result = {
            "return_code": 1,
            "stdout": "",
            "stderr": "Error: Failed to generate code"
        }
        mock_interactive_tool.return_value._run.return_value = mock_result
        
        # Create wrapper with mocked tool
        wrapper = QwenCodeWrapper()
        wrapper.interactive_tool = mock_interactive_tool.return_value
        
        # Test code generation failure
        result = wrapper.generate_code("Create a simple script")
        
        self.assertFalse(result["success"])
        self.assertIn("Error: Failed to generate code", result["error"])
    
    def test_build_contextual_prompt(self):
        """Test building contextual prompts."""
        # Create temporary context files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f1, \
             tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f2:
            f1.write("# Context file 1\nCONSTANT1 = 1\n")
            f2.write("# Context file 2\nCONSTANT2 = 2\n")
            context_file_1 = f1.name
            context_file_2 = f2.name
        
        try:
            # Test building contextual prompt
            prompt = self.wrapper._build_contextual_prompt(
                "Create a script using context constants",
                [context_file_1, context_file_2]
            )
            
            self.assertIn("Create a script using context constants", prompt)
            self.assertIn("CONSTANT1 = 1", prompt)
            self.assertIn("CONSTANT2 = 2", prompt)
        finally:
            # Clean up temporary files
            os.unlink(context_file_1)
            os.unlink(context_file_2)
    
    def test_process_generation_result(self):
        """Test processing generation results."""
        # Test successful result
        success_result = {
            "return_code": 0,
            "stdout": "generated_code = True",
            "stderr": ""
        }
        
        processed = self.wrapper._process_generation_result(success_result)
        self.assertTrue(processed["success"])
        self.assertEqual(processed["generated_code"], "generated_code = True")
        
        # Test failed result
        failure_result = {
            "return_code": 1,
            "stdout": "",
            "stderr": "Error occurred"
        }
        
        processed = self.wrapper._process_generation_result(failure_result)
        self.assertFalse(processed["success"])
        self.assertIn("Error occurred", processed["error"])


if __name__ == "__main__":
    unittest.main()
