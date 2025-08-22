"""
Enhanced Validation Engineer Implementation

This module implements an enhanced validation engineer that incorporates test quality gates
and more comprehensive validation checks.
"""

import os
import json
import time
from typing import Dict, Any, List, Optional
from pathlib import Path

# Import our enhanced modules
from .validation.test_quality_gate import TestQualityGate
from tools.qwen_code_execution_tool import QwenCodeExecutionTool
from tools.qwen_code_wrapper import QwenCodeWrapper


class EnhancedValidationEngineer:
    """Enhanced agent responsible for validating GDScript code and running tests with quality gates."""
    
    def __init__(self, godot_command: str = "godot", qwen_command: str = "qwen-code",
                 min_coverage: float = 85.0, min_test_count: int = 5):
        """
        Initialize the EnhancedValidationEngineer.
        
        Args:
            godot_command: Command to invoke Godot
            qwen_command: Command to invoke qwen-code
            min_coverage: Minimum required code coverage percentage
            min_test_count: Minimum required number of tests
        """
        self.godot_command = godot_command
        self.qwen_wrapper = QwenCodeWrapper(qwen_command)
        self.execution_tool = QwenCodeExecutionTool()
        self.test_quality_gate = TestQualityGate(min_coverage, min_test_count)
    
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
    
    def run_unit_tests_with_quality_gate(self, test_file: str = None, 
                                        test_directory: str = None) -> Dict[str, Any]:
        """
        Run unit tests using gdUnit4 with quality gate validation.
        
        Args:
            test_file: Specific test file to run (optional)
            test_directory: Directory containing test files (optional)
            
        Returns:
            Dictionary with comprehensive test results including quality gate validation
        """
        # Run tests first
        test_results = self._run_unit_tests_internal(test_file, test_directory)
        
        # Apply quality gate validation
        quality_validation = self.test_quality_gate.validate_test_quality(
            test_results.get("test_results", {})
        )
        
        # Combine results
        combined_results = {
            "test_execution": test_results,
            "quality_validation": quality_validation,
            "overall_success": test_results.get("success", False) and quality_validation.get("passed", False)
        }
        
        return combined_results
    
    def _run_unit_tests_internal(self, test_file: str = None, 
                                test_directory: str = None) -> Dict[str, Any]:
        """
        Internal method to run unit tests using gdUnit4.
        
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
            parsed_test_results = self._parse_enhanced_test_output(
                result.get("stdout", ""), 
                result.get("stderr", "")
            )
            
            return {
                "success": result.get("return_code") == 0,
                "test_target": test_target,
                "command_output": result,
                "test_results": parsed_test_results
            }
            
        except Exception as e:
            return {
                "success": False,
                "test_target": test_target,
                "error": f"Failed to execute tests: {str(e)}"
            }
    
    def _parse_enhanced_test_output(self, stdout: str, stderr: str) -> Dict[str, Any]:
        """
        Parse enhanced test output from gdUnit4 with coverage information.
        
        Args:
            stdout: Standard output from test execution
            stderr: Standard error from test execution
            
        Returns:
            Dictionary with parsed test results including coverage
        """
        # This is a more sophisticated parser that attempts to extract
        # test results and coverage information
        results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "coverage_percentage": 0.0,
            "duration": 0.0,
            "errors": [],
            "failures": []
        }
        
        # Look for test summary patterns
        # This is a placeholder implementation that would need to be
        # customized based on the actual gdUnit4 output format
        
        # Simple parsing for demonstration
        if "passed" in stdout.lower():
            results["passed_tests"] = stdout.lower().count("passed")
        if "failed" in stdout.lower():
            results["failed_tests"] = stdout.lower().count("failed")
        
        results["total_tests"] = results["passed_tests"] + results["failed_tests"]
        
        # Look for coverage information
        if "coverage" in stdout.lower():
            # Try to extract coverage percentage
            import re
            coverage_match = re.search(r'coverage[:\s]*(\d+\.?\d*)%', stdout, re.IGNORECASE)
            if coverage_match:
                results["coverage_percentage"] = float(coverage_match.group(1))
        
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
            self._check_magic_numbers(content),
            self._check_performance_antipatterns(content)
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
    
    def _check_performance_antipatterns(self, content: str) -> Dict[str, Any]:
        """Check for performance-related anti-patterns."""
        issues = []
        
        # Check for _process in loops
        if "_process" in content and "for " in content:
            issues.append("Potential performance issue: _process function contains loops")
        
        # Check for frequent node lookups
        if ".get_node(" in content and content.count(".get_node(") > 5:
            issues.append("Frequent use of get_node - consider using onready variables")
        
        return {
            "check_name": "performance_antipatterns",
            "passed": len(issues) == 0,
            "issues": issues
        }
    
    def run_security_scan(self, file_path: str) -> Dict[str, Any]:
        """
        Run a comprehensive security scan on GDScript code.
        
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
        
        # Check for eval-like functions
        if "eval" in content.lower() or "execute" in content.lower():
            security_issues.append("Dynamic code execution detected - potential security risk")
        
        return {
            "success": len(security_issues) == 0,
            "file_path": file_path,
            "security_issues": security_issues
        }
    
    def generate_enhanced_validation_report(self, files_to_validate: List[str]) -> Dict[str, Any]:
        """
        Generate an enhanced comprehensive validation report for multiple files.
        
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
                "failed_files": 0,
                "quality_scores": []
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
    """Main function for testing the EnhancedValidationEngineer."""
    # Create enhanced validation engineer
    validator = EnhancedValidationEngineer(min_coverage=85.0, min_test_count=5)
    
    # Example usage (commented out since we don't have actual files to validate)
    # result = validator.validate_gdscript_syntax("target/scripts/player/ship.gd")
    # print("Validation Result:")
    # print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()