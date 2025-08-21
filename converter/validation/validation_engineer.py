"""
Validation Engineer Agent Implementation

This agent is responsible for validating generated GDScript code,
running tests, and ensuring code quality standards.
"""

import os
import json
import subprocess
import time
from typing import Dict, Any, List, Optional
from pathlib import Path

# Import tools
from tools.qwen_code_execution_tool import QwenCodeExecutionTool
from tools.qwen_code_wrapper import QwenCodeWrapper


class ValidationEngineer:
    """Agent responsible for validating GDScript code and running tests."""
    
    def __init__(self, godot_command: str = "godot", qwen_command: str = "qwen-code"):
        """
        Initialize the ValidationEngineer.
        
        Args:
            godot_command: Command to invoke Godot
            qwen_command: Command to invoke qwen-code
        """
        self.godot_command = godot_command
        self.qwen_wrapper = QwenCodeWrapper(qwen_command)
        self.execution_tool = QwenCodeExecutionTool()
    
    def validate_gdscript_syntax(self, file_path: str) -> Dict[str, Any]:
        """
        Validate GDScript syntax for a file.
        
        Args:
            file_path: Path to the GDScript file to validate
            
        Returns:
            Dictionary with validation results
        """
        # Check if file exists
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File does not exist: {file_path}"
            }
        
        # Use Godot to validate syntax
        # Godot has a --check-only flag that validates scripts without running them
        command = f"{self.godot_command} --check-only --script {file_path}"
        
        try:
            result = self.execution_tool._run(command, timeout_seconds=30)
            
            if result.get("return_code") == 0:
                return {
                    "success": True,
                    "file_path": file_path,
                    "message": "Syntax validation passed"
                }
            else:
                return {
                    "success": False,
                    "file_path": file_path,
                    "error": "Syntax validation failed",
                    "stdout": result.get("stdout", ""),
                    "stderr": result.get("stderr", "")
                }
                
        except Exception as e:
            return {
                "success": False,
                "file_path": file_path,
                "error": f"Failed to execute syntax validation: {str(e)}"
            }
    
    def run_unit_tests(self, test_file: str = None, test_directory: str = None) -> Dict[str, Any]:
        """
        Run unit tests using gdUnit4.
        
        Args:
            test_file: Specific test file to run (optional)
            test_directory: Directory containing test files (optional)
            
        Returns:
            Dictionary with test results
        """
        # Determine what to test
        if test_file:
            if not os.path.exists(test_file):
                return {
                    "success": False,
                    "error": f"Test file does not exist: {test_file}"
                }
            test_target = test_file
        elif test_directory:
            if not os.path.exists(test_directory):
                return {
                    "success": False,
                    "error": f"Test directory does not exist: {test_directory}"
                }
            test_target = test_directory
        else:
            return {
                "success": False,
                "error": "Either test_file or test_directory must be specified"
            }
        
        # Run tests using Godot
        # gdUnit4 typically runs with a specific scene or through the Godot editor
        # For command line, we might need to use a test runner scene
        command = f"{self.godot_command} --path . --quit-after 300 --headless -s {test_target}"
        
        try:
            result = self.execution_tool._run(command, timeout_seconds=300)
            
            # Parse test results (this would depend on gdUnit4 output format)
            test_results = self._parse_test_output(result.get("stdout", ""), result.get("stderr", ""))
            
            return {
                "success": result.get("return_code") == 0,
                "test_target": test_target,
                "command_output": result,
                "test_results": test_results
            }
            
        except Exception as e:
            return {
                "success": False,
                "test_target": test_target,
                "error": f"Failed to execute tests: {str(e)}"
            }
    
    def _parse_test_output(self, stdout: str, stderr: str) -> Dict[str, Any]:
        """
        Parse test output from gdUnit4.
        
        Args:
            stdout: Standard output from test execution
            stderr: Standard error from test execution
            
        Returns:
            Dictionary with parsed test results
        """
        # This is a simplified parser - in reality, this would need to parse
        # the specific output format of gdUnit4
        results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "errors": [],
            "failures": []
        }
        
        # Look for test summary patterns
        # This is a placeholder implementation
        if "passed" in stdout.lower():
            results["passed_tests"] = stdout.lower().count("passed")
        if "failed" in stdout.lower():
            results["failed_tests"] = stdout.lower().count("failed")
        
        results["total_tests"] = results["passed_tests"] + results["failed_tests"]
        
        # Collect errors and failures
        if stderr:
            results["errors"].append(stderr)
        
        return results
    
    def validate_code_quality(self, file_path: str) -> Dict[str, Any]:
        """
        Validate code quality and adherence to style guidelines.
        
        Args:
            file_path: Path to the GDScript file to validate
            
        Returns:
            Dictionary with code quality results
        """
        # Check if file exists
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File does not exist: {file_path}"
            }
        
        results = {
            "file_path": file_path,
            "checks": {}
        }
        
        # Read the file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read file: {str(e)}"
            }
        
        # Perform various quality checks
        checks = [
            self._check_line_length(content),
            self._check_naming_conventions(content),
            self._check_documentation(content),
            self._check_code_complexity(content),
            self._check_magic_numbers(content)
        ]
        
        # Aggregate results
        all_passed = True
        for check in checks:
            check_name = check.get("check_name", "unknown")
            results["checks"][check_name] = check
            if not check.get("passed", False):
                all_passed = False
        
        results["success"] = all_passed
        return results
    
    def _check_line_length(self, content: str) -> Dict[str, Any]:
        """Check if lines exceed maximum length."""
        max_length = 100
        long_lines = []
        
        for i, line in enumerate(content.split('\n'), 1):
            if len(line) > max_length:
                long_lines.append({
                    "line_number": i,
                    "length": len(line),
                    "content": line[:50] + "..." if len(line) > 50 else line
                })
        
        return {
            "check_name": "line_length",
            "passed": len(long_lines) == 0,
            "max_length": max_length,
            "violations": long_lines
        }
    
    def _check_naming_conventions(self, content: str) -> Dict[str, Any]:
        """Check if naming conventions are followed."""
        import re
        
        # Check for PascalCase class names
        class_pattern = r'class_name\s+(\w+)'
        class_matches = re.findall(class_pattern, content)
        
        # Check for snake_case function names
        func_pattern = r'func\s+(\w+)'
        func_matches = re.findall(func_pattern, content)
        
        # Check for CONSTANT_CASE constants
        const_pattern = r'const\s+(\w+)'
        const_matches = re.findall(const_pattern, content)
        
        # Simple validation (in a real implementation, this would be more thorough)
        issues = []
        for class_name in class_matches:
            if not class_name[0].isupper():
                issues.append(f"Class {class_name} should use PascalCase")
        
        # For now, we'll just return a basic result
        return {
            "check_name": "naming_conventions",
            "passed": len(issues) == 0,
            "issues": issues
        }
    
    def _check_documentation(self, content: str) -> Dict[str, Any]:
        """Check if functions and classes are documented."""
        import re
        
        # Look for functions without docstrings
        func_pattern = r'func\s+(\w+)\s*\('
        func_matches = re.findall(func_pattern, content)
        
        # Simple check - in reality, this would be more sophisticated
        return {
            "check_name": "documentation",
            "passed": True,  # Placeholder
            "undocumented_functions": len(func_matches)
        }
    
    def _check_code_complexity(self, content: str) -> Dict[str, Any]:
        """Check for overly complex code."""
        # Simple check for nested conditions
        nested_if_count = content.count("if ") + content.count("elif ")
        
        return {
            "check_name": "code_complexity",
            "passed": nested_if_count < 10,  # Arbitrary threshold
            "nested_conditions": nested_if_count
        }
    
    def _check_magic_numbers(self, content: str) -> Dict[str, Any]:
        """Check for magic numbers in the code."""
        import re
        
        # Look for numeric literals that aren't 0, 1, or simple cases
        number_pattern = r'[^a-zA-Z_](\d+\.\d+|\d+)[^a-zA-Z_]'
        matches = re.findall(number_pattern, content)
        
        # Filter out common acceptable numbers
        magic_numbers = [num for num in matches if num not in ['0', '1', '2', '10', '100']]
        
        return {
            "check_name": "magic_numbers",
            "passed": len(magic_numbers) == 0,
            "magic_numbers_found": len(magic_numbers)
        }
    
    def run_security_scan(self, file_path: str) -> Dict[str, Any]:
        """
        Run a basic security scan on GDScript code.
        
        Args:
            file_path: Path to the GDScript file to scan
            
        Returns:
            Dictionary with security scan results
        """
        # Check if file exists
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"File does not exist: {file_path}"
            }
        
        # Read the file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to read file: {str(e)}"
            }
        
        # Check for potential security issues
        security_issues = []
        
        # Check for OS command execution
        if "OS.execute" in content:
            security_issues.append("Use of OS.execute detected - potential security risk")
        
        # Check for file system access
        if "File" in content or "Directory" in content:
            security_issues.append("File system access detected - review for security implications")
        
        # Check for network access
        if "HTTPClient" in content or "HTTPRequest" in content:
            security_issues.append("Network access detected - review for security implications")
        
        return {
            "success": len(security_issues) == 0,
            "file_path": file_path,
            "security_issues": security_issues
        }
    
    def generate_validation_report(self, files_to_validate: List[str]) -> Dict[str, Any]:
        """
        Generate a comprehensive validation report for multiple files.
        
        Args:
            files_to_validate: List of file paths to validate
            
        Returns:
            Dictionary with comprehensive validation report
        """
        report = {
            "timestamp": time.time(),
            "files_processed": 0,
            "syntax_validation": [],
            "code_quality": [],
            "security_scans": [],
            "test_results": [],
            "summary": {
                "total_files": len(files_to_validate),
                "passed_syntax": 0,
                "passed_quality": 0,
                "passed_security": 0,
                "failed_files": 0
            }
        }
        
        for file_path in files_to_validate:
            if not os.path.exists(file_path):
                report["summary"]["failed_files"] += 1
                continue
            
            # Syntax validation
            syntax_result = self.validate_gdscript_syntax(file_path)
            report["syntax_validation"].append(syntax_result)
            if syntax_result.get("success"):
                report["summary"]["passed_syntax"] += 1
            
            # Code quality validation
            quality_result = self.validate_code_quality(file_path)
            report["code_quality"].append(quality_result)
            if quality_result.get("success"):
                report["summary"]["passed_quality"] += 1
            
            # Security scan
            security_result = self.run_security_scan(file_path)
            report["security_scans"].append(security_result)
            if security_result.get("success"):
                report["summary"]["passed_security"] += 1
            
            report["files_processed"] += 1
        
        return report


def main():
    """Main function for testing the ValidationEngineer."""
    validator = ValidationEngineer()
    
    # Example usage (commented out since we don't have actual files to validate)
    # result = validator.validate_gdscript_syntax("target/scripts/player/ship.gd")
    # print("Validation Result:")
    # print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
