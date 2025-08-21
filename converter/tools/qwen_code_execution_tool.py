"""
Qwen Code Execution Tool

This tool provides a wrapper for executing qwen-code CLI commands.
It uses subprocess.Popen for interactive control of the qwen-code process.
"""

import subprocess
import time
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class QwenCodeExecutionInput(BaseModel):
    """Input schema for the QwenCodeExecutionTool."""
    command: str = Field(..., description="The full shell command to be executed.")
    timeout_seconds: int = Field(default=300, description="Timeout for the command in seconds.")
    working_directory: Optional[str] = Field(default=None, description="Working directory for command execution.")


class QwenCodeExecutionTool(BaseTool):
    """Tool for executing qwen-code CLI commands with interactive control."""
    
    name: str = "Qwen Code CLI Execution Tool"
    description: str = "Executes qwen-code shell commands non-interactively, captures output, and returns results."
    args_schema: type[BaseModel] = QwenCodeExecutionInput
    
    def _run(self, command: str, timeout_seconds: int = 300, working_directory: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute the shell command and return a structured report of the outcome.
        
        Args:
            command: The full shell command to execute
            timeout_seconds: Timeout for the command in seconds
            working_directory: Working directory for command execution
            
        Returns:
            Dictionary with execution results including return code, stdout, stderr
        """
        try:
            # Start the process with pipes for stdin, stdout, and stderr
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                cwd=working_directory
            )
            
            # Wait for the process to complete or timeout
            stdout, stderr = process.communicate(timeout=timeout_seconds)
            
            # Structure the output for the QualityAssuranceAgent
            result = {
                "command": command,
                "return_code": process.returncode,
                "stdout": stdout,
                "stderr": stderr,
                "execution_time": time.time()
            }
            
            return result
            
        except subprocess.TimeoutExpired as e:
            # Handle timeout
            return {
                "command": command,
                "return_code": -1,
                "stdout": getattr(e, 'stdout', ''),
                "stderr": f"Command timed out after {timeout_seconds} seconds",
                "error": "timeout",
                "execution_time": time.time()
            }
        except Exception as e:
            # Handle other exceptions
            return {
                "command": command,
                "return_code": -1,
                "stdout": "",
                "stderr": str(e),
                "error": "exception",
                "execution_time": time.time()
            }


class QwenCodeInteractiveTool(BaseTool):
    """Tool for interactive communication with qwen-code."""
    
    name: str = "Qwen Code Interactive Tool"
    description: str = "Interactively communicates with qwen-code, sending prompts and receiving responses."
    args_schema: type[BaseModel] = QwenCodeExecutionInput
    
    def _run(self, command: str, prompt: str, timeout_seconds: int = 300, working_directory: Optional[str] = None) -> Dict[str, Any]:
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
        try:
            # Start the process with pipes for stdin, stdout, and stderr
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                cwd=working_directory
            )
            
            # Send the prompt to stdin
            stdout, stderr = process.communicate(input=prompt, timeout=timeout_seconds)
            
            # Structure the output
            result = {
                "command": command,
                "prompt": prompt,
                "return_code": process.returncode,
                "stdout": stdout,
                "stderr": stderr,
                "execution_time": time.time()
            }
            
            return result
            
        except subprocess.TimeoutExpired as e:
            return {
                "command": command,
                "prompt": prompt,
                "return_code": -1,
                "stdout": getattr(e, 'stdout', ''),
                "stderr": f"Command timed out after {timeout_seconds} seconds",
                "error": "timeout",
                "execution_time": time.time()
            }
        except Exception as e:
            return {
                "command": command,
                "prompt": prompt,
                "return_code": -1,
                "stdout": "",
                "stderr": str(e),
                "error": "exception",
                "execution_time": time.time()
            }
