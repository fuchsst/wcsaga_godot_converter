"""
Refactoring Specialist Agent Implementation

This agent is responsible for refactoring existing C++ code to GDScript
using the qwen-code CLI tool.
"""

import os
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

# Import tools
from tools.qwen_code_wrapper import QwenCodeWrapper
from prompt_engineering.prompt_engineering_agent import PromptEngineeringAgent


class RefactoringSpecialist:
    """Agent responsible for refactoring C++ code to GDScript."""
    
    def __init__(self, qwen_command: str = "qwen-code"):
        """
        Initialize the RefactoringSpecialist.
        
        Args:
            qwen_command: Command to invoke qwen-code
        """
        self.qwen_wrapper = QwenCodeWrapper(qwen_command)
        self.prompt_engine = PromptEngineeringAgent()
    
    def refactor_file(self, source_file: str, target_file: str, 
                     refactoring_instructions: str) -> Dict[str, Any]:
        """
        Refactor a single file from C++ to GDScript.
        
        Args:
            source_file: Path to the source C++ file
            target_file: Path where the GDScript file should be created
            refactoring_instructions: Specific instructions for the refactoring
            
        Returns:
            Dictionary with refactoring results
        """
        # Check if source file exists
        if not os.path.exists(source_file):
            return {
                "success": False,
                "error": f"Source file does not exist: {source_file}"
            }
        
        # Read the source file
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                source_content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read source file: {str(e)}"
            }
        
        # Create a detailed specification for the refactoring
        specification = f"""Refactor the following C++ code to GDScript, following the project's STYLE_GUIDE.md and RULES.md:

<SOURCE_FILE_PATH>{source_file}</SOURCE_FILE_PATH>
<TARGET_FILE_PATH>{target_file}</TARGET_FILE_PATH>
<SOURCE_CODE>
{source_content}
</SOURCE_CODE>
<REFACTORING_INSTRUCTIONS>
{refactoring_instructions}
</REFACTORING_INSTRUCTIONS>"""
        
        # Generate the prompt
        prompt = self.prompt_engine.create_generation_prompt(
            target_file_path=target_file,
            specification=specification
        )
        
        # Execute the refactoring using qwen-code
        result = self.qwen_wrapper.generate_code(prompt)
        
        # If successful, save the result to the target file
        if result.get("success"):
            try:
                # Create target directory if it doesn't exist
                target_path = Path(target_file)
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save the refactored code
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(result.get("generated_code", ""))
                
                return {
                    "success": True,
                    "target_file": target_file,
                    "message": "File refactored successfully"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to save refactored code: {str(e)}",
                    "generated_code": result.get("generated_code")
                }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error during refactoring"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }
    
    def refactor_class(self, cpp_header: str, cpp_implementation: str, 
                      gdscript_target: str, class_mapping: Dict[str, str]) -> Dict[str, Any]:
        """
        Refactor a C++ class to GDScript.
        
        Args:
            cpp_header: Path to the C++ header file
            cpp_implementation: Path to the C++ implementation file
            gdscript_target: Path where the GDScript file should be created
            class_mapping: Mapping of C++ class names to GDScript class names
            
        Returns:
            Dictionary with refactoring results
        """
        # Check if files exist
        missing_files = []
        for file_path in [cpp_header, cpp_implementation]:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            return {
                "success": False,
                "error": f"Missing files: {', '.join(missing_files)}"
            }
        
        # Read the source files
        try:
            with open(cpp_header, 'r', encoding='utf-8') as f:
                header_content = f.read()
            
            with open(cpp_implementation, 'r', encoding='utf-8') as f:
                impl_content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read source files: {str(e)}"
            }
        
        # Create a detailed specification for the class refactoring
        specification = f"""Refactor the following C++ class to GDScript, following the project's STYLE_GUIDE.md and RULES.md.
Pay special attention to the class mapping and Godot-specific patterns.

<CPP_HEADER_FILE>{cpp_header}</CPP_HEADER_FILE>
<CPP_IMPLEMENTATION_FILE>{cpp_implementation}</CPP_IMPLEMENTATION_FILE>
<GDSCRIPT_TARGET>{gdscript_target}</GDSCRIPT_TARGET>
<CLASS_MAPPING>
{json.dumps(class_mapping, indent=2)}
</CLASS_MAPPING>
<CPP_HEADER_CONTENT>
{header_content}
</CPP_HEADER_CONTENT>
<CPP_IMPLEMENTATION_CONTENT>
{impl_content}
</CPP_IMPLEMENTATION_CONTENT>"""
        
        # Generate the prompt
        prompt = self.prompt_engine.create_generation_prompt(
            target_file_path=gdscript_target,
            specification=specification
        )
        
        # Execute the refactoring using qwen-code
        result = self.qwen_wrapper.generate_code(prompt)
        
        # If successful, save the result to the target file
        if result.get("success"):
            try:
                # Create target directory if it doesn't exist
                target_path = Path(gdscript_target)
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save the refactored code
                with open(gdscript_target, 'w', encoding='utf-8') as f:
                    f.write(result.get("generated_code", ""))
                
                return {
                    "success": True,
                    "target_file": gdscript_target,
                    "message": "Class refactored successfully"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to save refactored code: {str(e)}",
                    "generated_code": result.get("generated_code")
                }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error during class refactoring"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }
    
    def refactor_with_context(self, source_file: str, target_file: str,
                            refactoring_instructions: str, context_files: List[str]) -> Dict[str, Any]:
        """
        Refactor a file with additional context from other files.
        
        Args:
            source_file: Path to the source file
            target_file: Path where the refactored file should be created
            refactoring_instructions: Specific instructions for the refactoring
            context_files: List of additional files to provide as context
            
        Returns:
            Dictionary with refactoring results
        """
        # Generate the base prompt
        prompt = self.prompt_engine.create_refactoring_prompt(
            file_path=source_file,
            task_description=refactoring_instructions
        )
        
        # Add context to the prompt
        prompt_with_context = self.prompt_engine.add_context_to_prompt(
            prompt, context_files
        )
        
        # Execute the refactoring using qwen-code
        result = self.qwen_wrapper.refactor_code(source_file, prompt_with_context)
        
        # If successful, save the result to the target file
        if result.get("success"):
            try:
                # Create target directory if it doesn't exist
                target_path = Path(target_file)
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save the refactored code
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(result.get("refactored_code", ""))
                
                return {
                    "success": True,
                    "target_file": target_file,
                    "message": "File refactored successfully with context"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to save refactored code: {str(e)}",
                    "refactored_code": result.get("refactored_code")
                }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error during refactoring with context"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }
    
    def fix_refactoring_errors(self, file_path: str, error_message: str) -> Dict[str, Any]:
        """
        Fix errors in previously refactored code.
        
        Args:
            file_path: Path to the file with errors
            error_message: Error message describing the problem
            
        Returns:
            Dictionary with error fixing results
        """
        # Check if file exists
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File does not exist: {file_path}"
            }
        
        # Read the file with errors
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read file: {str(e)}"
            }
        
        # Use qwen-code to fix the errors
        result = self.qwen_wrapper.fix_bugs(file_path, error_message)
        
        # If successful, save the fixed code
        if result.get("success"):
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(result.get("fixed_code", ""))
                
                return {
                    "success": True,
                    "file_path": file_path,
                    "message": "Errors fixed successfully"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to save fixed code: {str(e)}",
                    "fixed_code": result.get("fixed_code")
                }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error during error fixing"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", "")
            }


def main():
    """Main function for testing the RefactoringSpecialist."""
    specialist = RefactoringSpecialist()
    
    # Example usage (commented out since we don't have actual files to refactor)
    # result = specialist.refactor_file(
    #     source_file="source/code/ship.h",
    #     target_file="target/scripts/ship.gd",
    #     refactoring_instructions="Convert C++ class to GDScript Node with proper Godot patterns"
    # )
    # 
    # print("Refactoring Result:")
    # print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
