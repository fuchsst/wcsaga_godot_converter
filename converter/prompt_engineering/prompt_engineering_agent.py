"""
Prompt Engineering Agent Implementation

This agent is responsible for converting atomic tasks and code context into
precise, effective prompts for the CLI coding agents.
"""

import json
from typing import Dict, Any, List, Optional
from pathlib import Path


class PromptEngineeringAgent:
    """AI Communications Specialist for creating precise prompts."""
    
    def __init__(self):
        """Initialize the PromptEngineeringAgent."""
        self.template_library = self._load_template_library()
    
    def _load_template_library(self) -> Dict[str, str]:
        """
        Load the library of prompt templates.
        
        Returns:
            Dictionary mapping template IDs to template strings
        """
        # In a real implementation, this would load from files
        # For now, we'll define the templates directly
        return {
            "QWEN_GENERATE_01": """You are an expert GDScript programmer. Your task is to generate a new script file based on the provided specification.
Your response must contain ONLY the complete GDScript code for the new file.
Do not include any explanatory text, markdown formatting, or conversational filler.

<TARGET_FILE_PATH>{target_file_path}</TARGET_FILE_PATH>
<SPECIFICATION>{specification}</SPECIFICATION>
<CONTEXT_CODE>{context_code}</CONTEXT_CODE>""",
            
            "QWEN_REFACTOR_01": """You are an expert GDScript programmer. Your task is to perform a specific refactoring on an existing file.
Do not propose a plan; implement the change directly. Do not modify any other files.

<FILE_PATH>{file_path}</FILE_PATH>
<TASK_DESCRIPTION>{task_description}</TASK_DESCRIPTION>
<CONSTRAINTS>{constraints}</CONSTRAINTS>""",
            
            "QWEN_BUGFIX_01": """You are an expert debugger. A bug has been identified in the following file.
Your task is to fix it. Analyze the provided error message and code, identify the root cause, and apply the necessary correction.
Implement the fix directly.

<FILE_PATH>{file_path}</FILE_PATH>
<CODE_SNIPPET>{code_snippet}</CODE_SNIPPET>
<ERROR_MESSAGE>{error_message}</ERROR_MESSAGE>""",
            
            "QWEN_TEST_GENERATE_01": """You are an expert QA engineer. Your task is to generate unit tests for the provided GDScript class.
Create comprehensive tests that cover all public methods and edge cases.
Use the gdUnit4 framework for test implementation.

<TARGET_CLASS>{target_class}</TARGET_CLASS>
<TARGET_FILE>{target_file}</TARGET_FILE>
<CLASS_CONTENT>{class_content}</CLASS_CONTENT>
<TEST_FRAMEWORK>gdUnit4</TEST_FRAMEWORK>"""
        }
    
    def generate_prompt(self, task_type: str, **kwargs) -> str:
        """
        Generate a prompt for a specific task type.
        
        Args:
            task_type: Type of task (e.g., "QWEN_GENERATE_01")
            **kwargs: Parameters for the template
            
        Returns:
            Formatted prompt string
        """
        if task_type not in self.template_library:
            raise ValueError(f"Unknown task type: {task_type}")
        
        template = self.template_library[task_type]
        return template.format(**kwargs)
    
    def create_generation_prompt(self, target_file_path: str, specification: str, 
                               context_code: str = "") -> str:
        """
        Create a prompt for generating a new file.
        
        Args:
            target_file_path: Path where the new file should be created
            specification: Detailed specification for the new file
            context_code: Optional context code to reference
            
        Returns:
            Formatted prompt string
        """
        return self.generate_prompt(
            "QWEN_GENERATE_01",
            target_file_path=target_file_path,
            specification=specification,
            context_code=context_code
        )
    
    def create_refactoring_prompt(self, file_path: str, task_description: str, 
                                constraints: str = "") -> str:
        """
        Create a prompt for refactoring an existing file.
        
        Args:
            file_path: Path to the file to refactor
            task_description: Description of the refactoring task
            constraints: Additional constraints for the task
            
        Returns:
            Formatted prompt string
        """
        return self.generate_prompt(
            "QWEN_REFACTOR_01",
            file_path=file_path,
            task_description=task_description,
            constraints=constraints
        )
    
    def create_bugfix_prompt(self, file_path: str, code_snippet: str, 
                           error_message: str) -> str:
        """
        Create a prompt for fixing a bug.
        
        Args:
            file_path: Path to the file with the bug
            code_snippet: Code snippet with the bug
            error_message: Error message describing the bug
            
        Returns:
            Formatted prompt string
        """
        return self.generate_prompt(
            "QWEN_BUGFIX_01",
            file_path=file_path,
            code_snippet=code_snippet,
            error_message=error_message
        )
    
    def create_test_generation_prompt(self, target_class: str, target_file: str, 
                                    class_content: str) -> str:
        """
        Create a prompt for generating unit tests.
        
        Args:
            target_class: Name of the class to test
            target_file: Path to the file containing the class
            class_content: Content of the class to test
            
        Returns:
            Formatted prompt string
        """
        return self.generate_prompt(
            "QWEN_TEST_GENERATE_01",
            target_class=target_class,
            target_file=target_file,
            class_content=class_content
        )
    
    def refine_prompt_with_feedback(self, original_prompt: str, error_message: str, 
                                  previous_output: str = "") -> str:
        """
        Refine a prompt based on error feedback.
        
        Args:
            original_prompt: The original prompt that failed
            error_message: Error message from the failed execution
            previous_output: Output from the failed execution (if any)
            
        Returns:
            Refined prompt string
        """
        refinement_prompt = f"""{original_prompt}

The previous attempt to execute this task failed with the following error:
<ERROR_MESSAGE>{error_message}</ERROR_MESSAGE>

Please revise the prompt to address this error. Consider:
1. Making the instructions more specific
2. Adding additional constraints or context
3. Clarifying the expected output format
4. Ensuring all required information is included

<REFINEMENT_INSTRUCTIONS>
Please provide a corrected version of the code that addresses the error above.
</REFINEMENT_INSTRUCTIONS>"""
        
        return refinement_prompt
    
    def add_context_to_prompt(self, prompt: str, context_files: List[str]) -> str:
        """
        Add context from files to an existing prompt.
        
        Args:
            prompt: The base prompt
            context_files: List of file paths to include as context
            
        Returns:
            Prompt with added context
        """
        context_sections = []
        for file_path in context_files:
            path = Path(file_path)
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    context_sections.append(f"<CONTEXT_FILE path='{file_path}'>\n{content}\n</CONTEXT_FILE>")
                except Exception:
                    # If we can't read a file, just skip it
                    pass
        
        if context_sections:
            context_str = "\n".join(context_sections)
            return f"{prompt}\n\n<ADDITIONAL_CONTEXT>\n{context_str}\n</ADDITIONAL_CONTEXT>"
        
        return prompt


def main():
    """Main function for testing the PromptEngineeringAgent."""
    agent = PromptEngineeringAgent()
    
    # Example usage
    prompt = agent.create_generation_prompt(
        target_file_path="scripts/player/ship.gd",
        specification="Create a PlayerShip class that handles movement, weapons, and health",
        context_code="# This class represents a player-controlled spacecraft"
    )
    
    print("Generated Prompt:")
    print(prompt)
    print("\n" + "="*50 + "\n")
    
    # Example of refinement
    refined_prompt = agent.refine_prompt_with_feedback(
        original_prompt=prompt,
        error_message="SyntaxError: Unexpected token 'class'"
    )
    
    print("Refined Prompt:")
    print(refined_prompt)


if __name__ == "__main__":
    main()
