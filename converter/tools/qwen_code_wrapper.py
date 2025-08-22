"""
Qwen Code Wrapper

This module provides a high-level wrapper for the qwen-code CLI agent,
specifically designed for high-context generation tasks.
"""

import os
from typing import Any, Dict, List, Optional

from .qwen_code_execution_tool import QwenCodeInteractiveTool


class QwenCodeWrapper:
    """Wrapper for high-context generation tasks with qwen-code."""

    def __init__(self, qwen_command: str = "qwen-code", timeout: int = 300):
        """
        Initialize the QwenCodeWrapper.

        Args:
            qwen_command: The command to invoke qwen-code
            timeout: Default timeout for commands in seconds
        """
        self.qwen_command = qwen_command
        self.timeout = timeout
        self.interactive_tool = QwenCodeInteractiveTool()

    def generate_code(
        self, prompt: str, context_files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate code using qwen-code with high-context input.

        Args:
            prompt: The prompt for code generation
            context_files: Optional list of file paths to include as context

        Returns:
            Dictionary with generation results
        """
        # Build the full prompt with context if provided
        full_prompt = prompt
        if context_files:
            full_prompt = self._build_contextual_prompt(prompt, context_files)

        # Execute qwen-code with the prompt
        result = self.interactive_tool._run(
            command=self.qwen_command, prompt=full_prompt, timeout_seconds=self.timeout
        )

        return self._process_generation_result(result)

    def refactor_code(
        self, file_path: str, refactoring_instructions: str
    ) -> Dict[str, Any]:
        """
        Refactor existing code using qwen-code.

        Args:
            file_path: Path to the file to refactor
            refactoring_instructions: Instructions for the refactoring

        Returns:
            Dictionary with refactoring results
        """
        # Read the existing file content
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read file {file_path}: {str(e)}",
            }

        # Create a refactoring prompt
        prompt = f"""
You are an expert GDScript programmer. Your task is to refactor the provided code according to the instructions.
Return ONLY the refactored code without any additional text or explanations.

<FILE_PATH>{file_path}</FILE_PATH>
<FILE_CONTENT>
{file_content}
</FILE_CONTENT>
<REFACTORING_INSTRUCTIONS>
{refactoring_instructions}
</REFACTORING_INSTRUCTIONS>
"""

        # Execute qwen-code with the refactoring prompt
        result = self.interactive_tool._run(
            command=self.qwen_command, prompt=prompt, timeout_seconds=self.timeout
        )

        return self._process_refactoring_result(result, file_path)

    def fix_bugs(self, file_path: str, error_message: str) -> Dict[str, Any]:
        """
        Fix bugs in code using qwen-code.

        Args:
            file_path: Path to the file with bugs
            error_message: Error message describing the bug

        Returns:
            Dictionary with bug fixing results
        """
        # Read the existing file content
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read file {file_path}: {str(e)}",
            }

        # Create a bug fixing prompt
        prompt = f"""
You are an expert debugger. Your task is to fix the bug described in the error message.
Analyze the provided code and error, identify the root cause, and apply the necessary correction.
Return ONLY the fixed code without any additional text or explanations.

<FILE_PATH>{file_path}</FILE_PATH>
<FILE_CONTENT>
{file_content}
</FILE_CONTENT>
<ERROR_MESSAGE>
{error_message}
</ERROR_MESSAGE>
"""

        # Execute qwen-code with the bug fixing prompt
        result = self.interactive_tool._run(
            command=self.qwen_command, prompt=prompt, timeout_seconds=self.timeout
        )

        return self._process_bugfix_result(result, file_path)

    def _build_contextual_prompt(self, prompt: str, context_files: List[str]) -> str:
        """
        Build a prompt with contextual information from files.

        Args:
            prompt: The base prompt
            context_files: List of file paths to include as context

        Returns:
            Prompt with contextual information
        """
        context_sections = []
        for file_path in context_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    context_sections.append(
                        f"<CONTEXT_FILE path='{file_path}'>\n{content}\n</CONTEXT_FILE>"
                    )
                except Exception:
                    # If we can't read a file, just skip it
                    pass

        if context_sections:
            context_str = "\n".join(context_sections)
            return f"{prompt}\n\n<CONTEXT>\n{context_str}\n</CONTEXT>"

        return prompt

    def _process_generation_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the result of a code generation task.

        Args:
            result: Raw result from qwen-code execution

        Returns:
            Processed result dictionary
        """
        if result.get("return_code") == 0:
            # Extract code from stdout (assuming it's the only content)
            generated_code = result.get("stdout", "").strip()

            return {
                "success": True,
                "generated_code": generated_code,
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", ""),
            }
        else:
            return {
                "success": False,
                "error": result.get("stderr", "Unknown error"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", ""),
            }

    def _process_refactoring_result(
        self, result: Dict[str, Any], original_file_path: str
    ) -> Dict[str, Any]:
        """
        Process the result of a code refactoring task.

        Args:
            result: Raw result from qwen-code execution
            original_file_path: Path to the original file

        Returns:
            Processed result dictionary
        """
        if result.get("return_code") == 0:
            # Extract refactored code from stdout
            refactored_code = result.get("stdout", "").strip()

            return {
                "success": True,
                "refactored_code": refactored_code,
                "original_file": original_file_path,
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", ""),
            }
        else:
            return {
                "success": False,
                "error": result.get("stderr", "Unknown error"),
                "original_file": original_file_path,
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", ""),
            }

    def _process_bugfix_result(
        self, result: Dict[str, Any], original_file_path: str
    ) -> Dict[str, Any]:
        """
        Process the result of a bug fixing task.

        Args:
            result: Raw result from qwen-code execution
            original_file_path: Path to the original file

        Returns:
            Processed result dictionary
        """
        if result.get("return_code") == 0:
            # Extract fixed code from stdout
            fixed_code = result.get("stdout", "").strip()

            return {
                "success": True,
                "fixed_code": fixed_code,
                "original_file": original_file_path,
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", ""),
            }
        else:
            return {
                "success": False,
                "error": result.get("stderr", "Unknown error"),
                "original_file": original_file_path,
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", ""),
            }
