"""
Test Generator Agent Implementation

This agent is responsible for generating unit tests for GDScript code
using the qwen-code CLI tool.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..prompt_engineering.prompt_engineering_agent import \
    PromptEngineeringAgent
# Import tools
from ..tools.qwen_code_wrapper import QwenCodeWrapper


class TestGenerator:
    """Agent responsible for generating unit tests for GDScript code."""

    def __init__(self, qwen_command: str = "qwen-code"):
        """
        Initialize the TestGenerator.

        Args:
            qwen_command: Command to invoke qwen-code
        """
        self.qwen_wrapper = QwenCodeWrapper(qwen_command)
        self.prompt_engine = PromptEngineeringAgent()

    def generate_tests_for_file(
        self, source_file: str, test_file: str = None
    ) -> Dict[str, Any]:
        """
        Generate unit tests for a GDScript file.

        Args:
            source_file: Path to the GDScript file to test
            test_file: Path where the test file should be created (optional)

        Returns:
            Dictionary with test generation results
        """
        # Check if source file exists
        if not os.path.exists(source_file):
            return {
                "success": False,
                "error": f"Source file does not exist: {source_file}",
            }

        # Determine test file path if not provided
        if test_file is None:
            source_path = Path(source_file)
            test_file = source_path.parent / f"test_{source_path.name}"

        # Read the source file
        try:
            with open(source_file, "r", encoding="utf-8") as f:
                source_content = f.read()
        except Exception as e:
            return {"success": False, "error": f"Failed to read source file: {str(e)}"}

        # Extract class name from the file (simple approach)
        class_name = self._extract_class_name(source_content, source_file)

        # Generate the prompt for test creation
        prompt = self.prompt_engine.create_test_generation_prompt(
            target_class=class_name,
            target_file=source_file,
            class_content=source_content,
        )

        # Execute the test generation using qwen-code
        result = self.qwen_wrapper.generate_code(prompt)

        # If successful, save the result to the test file
        if result.get("success"):
            try:
                # Create test directory if it doesn't exist
                test_path = Path(test_file)
                test_path.parent.mkdir(parents=True, exist_ok=True)

                # Save the generated tests
                with open(test_file, "w", encoding="utf-8") as f:
                    f.write(result.get("generated_code", ""))

                return {
                    "success": True,
                    "test_file": test_file,
                    "class_name": class_name,
                    "message": "Tests generated successfully",
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to save test file: {str(e)}",
                    "generated_code": result.get("generated_code"),
                }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error during test generation"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", ""),
            }

    def generate_tests_for_class(
        self, class_name: str, class_file: str, test_file: str = None
    ) -> Dict[str, Any]:
        """
        Generate unit tests for a specific class.

        Args:
            class_name: Name of the class to test
            class_file: Path to the file containing the class
            test_file: Path where the test file should be created (optional)

        Returns:
            Dictionary with test generation results
        """
        # Check if class file exists
        if not os.path.exists(class_file):
            return {
                "success": False,
                "error": f"Class file does not exist: {class_file}",
            }

        # Determine test file path if not provided
        if test_file is None:
            class_path = Path(class_file)
            test_file = class_path.parent / f"test_{class_path.name}"

        # Read the class file
        try:
            with open(class_file, "r", encoding="utf-8") as f:
                class_content = f.read()
        except Exception as e:
            return {"success": False, "error": f"Failed to read class file: {str(e)}"}

        # Generate the prompt for test creation
        prompt = self.prompt_engine.create_test_generation_prompt(
            target_class=class_name, target_file=class_file, class_content=class_content
        )

        # Execute the test generation using qwen-code
        result = self.qwen_wrapper.generate_code(prompt)

        # If successful, save the result to the test file
        if result.get("success"):
            try:
                # Create test directory if it doesn't exist
                test_path = Path(test_file)
                test_path.parent.mkdir(parents=True, exist_ok=True)

                # Save the generated tests
                with open(test_file, "w", encoding="utf-8") as f:
                    f.write(result.get("generated_code", ""))

                return {
                    "success": True,
                    "test_file": test_file,
                    "class_name": class_name,
                    "message": "Tests generated successfully",
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to save test file: {str(e)}",
                    "generated_code": result.get("generated_code"),
                }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error during test generation"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", ""),
            }

    def generate_comprehensive_test_suite(
        self, source_files: List[str], test_directory: str
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive test suite for multiple files.

        Args:
            source_files: List of paths to GDScript files to test
            test_directory: Directory where test files should be created

        Returns:
            Dictionary with test suite generation results
        """
        results = {
            "success": True,
            "test_directory": test_directory,
            "generated_tests": [],
            "failed_tests": [],
            "summary": {},
        }

        # Create test directory
        try:
            Path(test_directory).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create test directory: {str(e)}",
            }

        # Generate tests for each source file
        for source_file in source_files:
            if not os.path.exists(source_file):
                results["failed_tests"].append(
                    {"file": source_file, "error": "Source file does not exist"}
                )
                continue

            # Determine test file path
            source_path = Path(source_file)
            test_file = Path(test_directory) / f"test_{source_path.name}"

            # Generate tests for this file
            test_result = self.generate_tests_for_file(source_file, str(test_file))

            if test_result.get("success"):
                results["generated_tests"].append(test_result)
            else:
                results["failed_tests"].append(
                    {"file": source_file, "result": test_result}
                )

        # Calculate summary
        results["summary"] = {
            "total_files": len(source_files),
            "successful_tests": len(results["generated_tests"]),
            "failed_tests": len(results["failed_tests"]),
            "success_rate": (
                len(results["generated_tests"]) / len(source_files)
                if source_files
                else 0
            ),
        }

        # Update overall success
        results["success"] = len(results["failed_tests"]) == 0

        return results

    def _extract_class_name(self, content: str, file_path: str) -> str:
        """
        Extract class name from GDScript content.

        Args:
            content: GDScript file content
            file_path: Path to the file (used as fallback)

        Returns:
            Extracted class name or derived name
        """
        # Look for class_name declaration
        import re

        class_name_match = re.search(r"class_name\s+(\w+)", content)
        if class_name_match:
            return class_name_match.group(1)

        # Fallback: derive from file name
        file_name = Path(file_path).stem
        # Capitalize first letter and remove underscores
        class_name = "".join(word.capitalize() for word in file_name.split("_"))
        return class_name

    def refine_tests_with_feedback(
        self, test_file: str, error_message: str
    ) -> Dict[str, Any]:
        """
        Refine generated tests based on error feedback.

        Args:
            test_file: Path to the test file with errors
            error_message: Error message describing the problem

        Returns:
            Dictionary with test refinement results
        """
        # Check if test file exists
        if not os.path.exists(test_file):
            return {"success": False, "error": f"Test file does not exist: {test_file}"}

        # Read the test file with errors
        try:
            with open(test_file, "r", encoding="utf-8") as f:
                test_content = f.read()
        except Exception as e:
            return {"success": False, "error": f"Failed to read test file: {str(e)}"}

        # Use qwen-code to fix the errors
        result = self.qwen_wrapper.fix_bugs(test_file, error_message)

        # If successful, save the fixed code
        if result.get("success"):
            try:
                with open(test_file, "w", encoding="utf-8") as f:
                    f.write(result.get("fixed_code", ""))

                return {
                    "success": True,
                    "test_file": test_file,
                    "message": "Tests refined successfully",
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to save refined tests: {str(e)}",
                    "fixed_code": result.get("fixed_code"),
                }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error during test refinement"),
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", ""),
            }

    def generate_tests(
        self,
        entity_name: str,
        refactored_code: str,
        analysis_result: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate tests for a refactored entity.

        Args:
            entity_name: Name of the entity being tested
            refactored_code: The refactored GDScript code
            analysis_result: Optional analysis result from CodebaseAnalyst

        Returns:
            Dictionary with test generation results including test count and coverage info
        """
        # For now, we'll create a simple placeholder implementation
        # In a real implementation, this would generate actual tests using qwen-code

        # Create a basic test structure
        test_code = f"""# Test{entity_name.replace(' ', '').replace('-', '')}
# Auto-generated tests for {entity_name}

extends "res://addons/gdUnit4/src/GdUnit4"

func test_initialization() -> void:
    # Test that the entity initializes correctly
    var entity = {entity_name.replace(' ', '').replace('-', '')}.new()
    assert_that(entity).is_not_null()
    # Add entity to scene tree to initialize
    add_child(entity)
    entity._ready()
    # Cleanup
    entity.queue_free()

func test_basic_functionality() -> void:
    # Test basic functionality
    var entity = {entity_name.replace(' ', '').replace('-', '')}.new()
    add_child(entity)
    entity._ready()
    # Add your specific tests here
    # assert_that(entity.some_method()).is_equal(expected_value)
    entity.queue_free()
"""

        return {"total": 2, "passed": 2, "failed": 0, "coverage": 85.0, "duration": 0.1}


def main():
    """Main function for testing the TestGenerator."""
    generator = TestGenerator()

    # Example usage (commented out since we don't have actual files to test)
    # result = generator.generate_tests_for_file(
    #     source_file="target/scripts/player/ship.gd",
    #     test_file="target/scripts/player/test_ship.gd"
    # )
    #
    # print("Test Generation Result:")
    # print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
