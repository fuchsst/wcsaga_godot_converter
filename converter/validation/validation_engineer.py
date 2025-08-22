"""
Validation Engineer Implementation

This module implements a validation engineer that incorporates test quality gates
and comprehensive validation checks.
"""

import os
import time
from typing import Any, Dict, List
# For JUnit XML parsing
from xml.etree import ElementTree as ET

from ..tools.qwen_code_execution_tool import QwenCodeExecutionTool
from ..tools.qwen_code_wrapper import QwenCodeWrapper
# Import our validation modules
from .test_quality_gate import TestQualityGate


class ValidationEngineer:
    """Agent responsible for validating GDScript code and running tests with quality gates."""

    def __init__(
        self,
        godot_command: str = "godot",
        qwen_command: str = "qwen-code",
        min_coverage: float = 85.0,
        min_test_count: int = 5,
    ):
        """
        Initialize the ValidationEngineer.

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
            return {"success": False, "error": f"File does not exist: {file_path}"}

        # Use Godot to validate syntax
        # Godot has a --check-only flag that validates scripts without running them
        command = f"{self.godot_command} --check-only --script {file_path}"

        try:
            result = self.execution_tool._run(command, timeout_seconds=30)

            if result.get("return_code") == 0:
                return {
                    "success": True,
                    "file_path": file_path,
                    "message": "Syntax validation passed",
                }
            else:
                return {
                    "success": False,
                    "file_path": file_path,
                    "error": "Syntax validation failed",
                    "stdout": result.get("stdout", ""),
                    "stderr": result.get("stderr", ""),
                }

        except Exception as e:
            return {
                "success": False,
                "file_path": file_path,
                "error": f"Failed to execute syntax validation: {str(e)}",
            }

    def run_unit_tests_with_quality_gate(
        self, test_file: str = None, test_directory: str = None
    ) -> Dict[str, Any]:
        """
        Run unit tests using gdUnit4 with quality gate validation.
        Includes code coverage validation and minimum test requirements.

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

        # Additional validation: check code coverage
        coverage_validation = self._validate_code_coverage(test_results)
        quality_validation["coverage_validation"] = coverage_validation

        # Update overall success to include coverage
        quality_validation_passed = quality_validation.get("passed", False)
        coverage_passed = coverage_validation.get("passed", False)

        combined_results = {
            "test_execution": test_results,
            "quality_validation": quality_validation,
            "overall_success": (
                test_results.get("success", False)
                and quality_validation_passed
                and coverage_passed
            ),
        }

        return combined_results

    def _run_unit_tests_internal(
        self, test_file: str = None, test_directory: str = None
    ) -> Dict[str, Any]:
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
                    "error": f"Test file does not exist: {test_file}",
                }
            test_target = test_file
        elif test_directory:
            if not os.path.exists(test_directory):
                return {
                    "success": False,
                    "error": f"Test directory does not exist: {test_directory}",
                }
            test_target = test_directory
        else:
            return {
                "success": False,
                "error": "Either test_file or test_directory must be specified",
            }

        # Run tests using Godot with JUnit XML output
        # gdUnit4 supports JUnit XML output for better test reporting
        junit_output_file = f"{test_target}_junit_results.xml"
        command = f"{self.godot_command} --path . --quit-after 300 --headless -s {test_target} --junit-xml {junit_output_file}"

        try:
            result = self.execution_tool._run(command, timeout_seconds=300)

            # Parse test results - try JUnit XML first, fallback to stdout parsing
            parsed_test_results = {}

            # Try to parse JUnit XML output
            if os.path.exists(junit_output_file):
                parsed_test_results = self._parse_junit_xml(junit_output_file)
                # Clean up the XML file
                try:
                    os.remove(junit_output_file)
                except:
                    pass

            # If JUnit parsing failed or no XML file, fallback to stdout parsing
            if not parsed_test_results or "error" in parsed_test_results:
                parsed_test_results = self._parse_test_output(
                    result.get("stdout", ""), result.get("stderr", "")
                )

            return {
                "success": result.get("return_code") == 0,
                "test_target": test_target,
                "command_output": result,
                "test_results": parsed_test_results,
            }

        except Exception as e:
            return {
                "success": False,
                "test_target": test_target,
                "error": f"Failed to execute tests: {str(e)}",
            }

    def _parse_test_output(self, stdout: str, stderr: str) -> Dict[str, Any]:
        """
        Parse test output from gdUnit4 with coverage information.

        Args:
            stdout: Standard output from test execution
            stderr: Standard error from test execution

        Returns:
            Dictionary with parsed test results including coverage
        """
        # Parser with coverage extraction
        results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "coverage_percentage": 0.0,
            "duration": 0.0,
            "errors": [],
            "failures": [],
            "test_cases": [],
        }

        # Parse test results with more sophisticated pattern matching
        import re

        # Extract test counts
        passed_match = re.search(r"passed:\s*(\d+)", stdout, re.IGNORECASE)
        failed_match = re.search(r"failed:\s*(\d+)", stdout, re.IGNORECASE)
        total_match = re.search(r"total:\s*(\d+)", stdout, re.IGNORECASE)

        if passed_match:
            results["passed_tests"] = int(passed_match.group(1))
        if failed_match:
            results["failed_tests"] = int(failed_match.group(1))
        if total_match:
            results["total_tests"] = int(total_match.group(1))
        else:
            results["total_tests"] = results["passed_tests"] + results["failed_tests"]

        # Extract coverage percentage with multiple patterns
        coverage_patterns = [
            r"coverage[:\s]*(\d+\.?\d*)%",
            r"line coverage[:\s]*(\d+\.?\d*)%",
            r"code coverage[:\s]*(\d+\.?\d*)%",
        ]

        for pattern in coverage_patterns:
            coverage_match = re.search(pattern, stdout, re.IGNORECASE)
            if coverage_match:
                results["coverage_percentage"] = float(coverage_match.group(1))
                break

        # Extract duration
        duration_match = re.search(r"duration[:\s]*(\d+\.?\d*)s", stdout, re.IGNORECASE)
        if duration_match:
            results["duration"] = float(duration_match.group(1))

        # Collect errors and failures
        if stderr:
            results["errors"].append(stderr)

        # Parse individual test cases for better quality assessment
        test_case_matches = re.findall(
            r"(test_.*?)(?:passed|failed|error)", stdout, re.IGNORECASE
        )
        for match in test_case_matches:
            results["test_cases"].append(match.strip())

        return results

    def _parse_junit_xml(self, xml_file_path: str) -> Dict[str, Any]:
        """
        Parse a JUnit XML report to extract detailed test metrics.

        Args:
            xml_file_path: Path to the JUnit XML file

        Returns:
            Dictionary with parsed test metrics
        """
        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            # Extract test suite information
            testsuite = root if root.tag == "testsuite" else root.find("testsuite")
            if testsuite is None:
                return {}

            # Extract comprehensive test metrics
            metrics = {
                "total_tests": int(testsuite.get("tests", 0)),
                "passed_tests": int(testsuite.get("tests", 0))
                - int(testsuite.get("failures", 0))
                - int(testsuite.get("errors", 0)),
                "failed_tests": int(testsuite.get("failures", 0)),
                "error_tests": int(testsuite.get("errors", 0)),
                "skipped_tests": int(testsuite.get("skipped", 0)),
                "duration": float(testsuite.get("time", 0.0)),
                "test_cases": [],
                "failures": [],
                "errors": [],
            }

            # Extract individual test case details
            for testcase in testsuite.findall(".//testcase"):
                test_case = {
                    "name": testcase.get("name"),
                    "classname": testcase.get("classname"),
                    "time": float(testcase.get("time", 0.0)),
                    "status": "passed",
                }

                # Check for failures or errors
                failure = testcase.find("failure")
                error = testcase.find("error")

                if failure is not None:
                    test_case["status"] = "failed"
                    test_case["failure"] = {
                        "message": failure.get("message"),
                        "type": failure.get("type"),
                        "content": failure.text,
                    }
                    metrics["failures"].append(test_case)
                elif error is not None:
                    test_case["status"] = "error"
                    test_case["error"] = {
                        "message": error.get("message"),
                        "type": error.get("type"),
                        "content": error.text,
                    }
                    metrics["errors"].append(test_case)

                metrics["test_cases"].append(test_case)

            return metrics

        except ET.ParseError as e:
            return {"error": f"XML parsing failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Processing failed: {str(e)}"}

    def _validate_code_coverage(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate code coverage meets minimum requirements.

        Args:
            test_results: Test execution results

        Returns:
            Dictionary with coverage validation results
        """
        coverage = test_results.get("test_results", {}).get("coverage_percentage", 0.0)
        min_coverage = self.test_quality_gate.min_coverage

        passed = coverage >= min_coverage

        return {
            "passed": passed,
            "current_coverage": coverage,
            "min_required_coverage": min_coverage,
            "message": f"Code coverage validation {'passed' if passed else 'failed'}: {coverage}% vs required {min_coverage}%",
        }

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
            return {"success": False, "error": f"File does not exist: {file_path}"}

        results = {"file_path": file_path, "checks": {}}

        # Read the file
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return {"success": False, "error": f"Failed to read file: {str(e)}"}

        # Perform various quality checks
        checks = [
            self._check_line_length(content),
            self._check_naming_conventions(content),
            self._check_documentation(content),
            self._check_code_complexity(content),
            self._check_magic_numbers(content),
            self._check_performance_antipatterns(content),
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
            issues.append(
                "Potential performance issue: _process function contains loops"
            )

        # Check for frequent node lookups
        if ".get_node(" in content and content.count(".get_node(") > 5:
            issues.append("Frequent use of get_node - consider using onready variables")

        return {
            "check_name": "performance_antipatterns",
            "passed": len(issues) == 0,
            "issues": issues,
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
            return {"success": False, "error": f"File does not exist: {file_path}"}

        # Read the file
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return {"success": False, "error": f"Failed to read file: {str(e)}"}

        # Check for potential security issues
        security_issues = []

        # Check for OS command execution
        if "OS.execute" in content:
            security_issues.append(
                "Use of OS.execute detected - potential security risk"
            )

        # Check for file system access
        if "File" in content or "Directory" in content:
            security_issues.append(
                "File system access detected - review for security implications"
            )

        # Check for network access
        if "HTTPClient" in content or "HTTPRequest" in content:
            security_issues.append(
                "Network access detected - review for security implications"
            )

        # Check for eval-like functions
        if "eval" in content.lower() or "execute" in content.lower():
            security_issues.append(
                "Dynamic code execution detected - potential security risk"
            )

        return {
            "success": len(security_issues) == 0,
            "file_path": file_path,
            "security_issues": security_issues,
        }

    def generate_validation_report(
        self, files_to_validate: List[str]
    ) -> Dict[str, Any]:
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
                "failed_files": 0,
                "quality_scores": [],
            },
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

    def validate_tests(
        self, entity_name: str, test_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate the generated tests for an entity using behavior-driven testing.

        Args:
            entity_name: Name of the entity being validated
            test_results: Results from test generation containing test file paths and expected behaviors

        Returns:
            Dictionary with comprehensive validation results including BDD-style test execution
        """
        # Extract test file paths from test results
        test_files = test_results.get("test_files", [])
        expected_behaviors = test_results.get("expected_behaviors", [])
        
        if not test_files:
            return {
                "syntax_valid": False,
                "style_compliant": False,
                "test_results": test_results,
                "entity_name": entity_name,
                "behavior_validation": {
                    "passed": False,
                    "message": "No test files provided for validation"
                }
            }

        # Run comprehensive validation including BDD-style behavior checks
        validation_results = {
            "syntax_validation": [],
            "behavior_validation": {
                "total_scenarios": len(expected_behaviors),
                "passed_scenarios": 0,
                "failed_scenarios": 0,
                "scenario_details": []
            },
            "quality_metrics": {
                "test_coverage": 0.0,
                "edge_cases_covered": 0,
                "boundary_tests": 0,
                "error_handling_tests": 0
            }
        }

        # Validate syntax for each test file
        for test_file in test_files:
            syntax_result = self.validate_gdscript_syntax(test_file)
            validation_results["syntax_validation"].append(syntax_result)

        # Run behavior-driven validation using gdUnit4
        for behavior in expected_behaviors:
            scenario_result = self._validate_behavior_scenario(behavior, test_files)
            validation_results["behavior_validation"]["scenario_details"].append(scenario_result)
            
            if scenario_result["passed"]:
                validation_results["behavior_validation"]["passed_scenarios"] += 1
            else:
                validation_results["behavior_validation"]["failed_scenarios"] += 1

        # Calculate quality metrics
        validation_results["quality_metrics"] = self._calculate_quality_metrics(
            expected_behaviors, validation_results["behavior_validation"]
        )

        # Determine overall validation status
        all_syntax_valid = all(result.get("success", False) 
                              for result in validation_results["syntax_validation"])
        behavior_passed = (validation_results["behavior_validation"]["passed_scenarios"] > 0 and
                          validation_results["behavior_validation"]["failed_scenarios"] == 0)

        return {
            "syntax_valid": all_syntax_valid,
            "behavior_valid": behavior_passed,
            "test_results": test_results,
            "entity_name": entity_name,
            "validation_details": validation_results,
            "overall_valid": all_syntax_valid and behavior_passed
        }

    def _validate_behavior_scenario(self, behavior: Dict[str, Any], test_files: List[str]) -> Dict[str, Any]:
        """
        Validate a specific behavior scenario using BDD-style testing.

        Args:
            behavior: Behavior scenario with Given-When-Then structure
            test_files: List of test files to execute

        Returns:
            Dictionary with scenario validation results
        """
        scenario_name = behavior.get("scenario", "Unknown scenario")
        given = behavior.get("given", "")
        when = behavior.get("when", "")
        then = behavior.get("then", "")
        
        # Create a focused test execution for this specific behavior
        try:
            # Run tests with specific focus on this behavior
            test_result = self.run_unit_tests_with_quality_gate(test_directory=test_files[0])
            
            # Check if the expected behavior is covered by test results
            behavior_covered = self._check_behavior_coverage(test_result, given, when, then)
            
            return {
                "scenario": scenario_name,
                "given": given,
                "when": when,
                "then": then,
                "passed": behavior_covered,
                "test_result": test_result if not behavior_covered else None,
                "message": "Behavior validated successfully" if behavior_covered 
                          else f"Behavior not covered: {scenario_name}"
            }
            
        except Exception as e:
            return {
                "scenario": scenario_name,
                "given": given,
                "when": when,
                "then": then,
                "passed": False,
                "error": str(e),
                "message": f"Error validating behavior: {scenario_name}"
            }

    def _check_behavior_coverage(self, test_result: Dict[str, Any], given: str, when: str, then: str) -> bool:
        """
        Check if the test results cover the specified behavior.

        Args:
            test_result: Test execution results
            given: Given condition from BDD scenario
            when: When action from BDD scenario
            then: Then expected result from BDD scenario

        Returns:
            Boolean indicating if behavior is covered
        """
        # Extract test output for analysis
        test_output = test_result.get("test_execution", {}).get("command_output", {})
        stdout = test_output.get("stdout", "").lower()
        stderr = test_output.get("stderr", "").lower()
        
        # Simple keyword-based behavior coverage check
        # In a real implementation, this would use more sophisticated NLP or pattern matching
        given_covered = given.lower() in stdout or given.lower() in stderr
        when_covered = when.lower() in stdout or when.lower() in stderr
        then_covered = then.lower() in stdout or then.lower() in stderr
        
        return given_covered and when_covered and then_covered

    def _calculate_quality_metrics(self, expected_behaviors: List[Dict[str, Any]], 
                                 behavior_validation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive quality metrics for the test suite.

        Args:
            expected_behaviors: List of expected behaviors
            behavior_validation: Behavior validation results

        Returns:
            Dictionary with quality metrics
        """
        total_scenarios = len(expected_behaviors)
        passed_scenarios = behavior_validation.get("passed_scenarios", 0)
        
        # Calculate test coverage percentage
        test_coverage = (passed_scenarios / total_scenarios * 100) if total_scenarios > 0 else 0
        
        # Count edge cases and boundary tests
        edge_cases = sum(1 for behavior in expected_behaviors 
                        if any(keyword in behavior.get("scenario", "").lower() 
                              for keyword in ["edge", "corner", "extreme"]))
        
        boundary_tests = sum(1 for behavior in expected_behaviors 
                            if any(keyword in behavior.get("scenario", "").lower() 
                                  for keyword in ["boundary", "limit", "max", "min"]))
        
        error_handling_tests = sum(1 for behavior in expected_behaviors 
                                  if any(keyword in behavior.get("scenario", "").lower() 
                                        for keyword in ["error", "exception", "invalid"]))
        
        return {
            "test_coverage": round(test_coverage, 2),
            "edge_cases_covered": edge_cases,
            "boundary_tests": boundary_tests,
            "error_handling_tests": error_handling_tests,
            "total_behaviors": total_scenarios,
            "covered_behaviors": passed_scenarios
        }


def main():
    """Main function for testing the ValidationEngineer."""
    # Example usage (commented out since we don't have actual files to validate)
    # validator = ValidationEngineer(min_coverage=85.0, min_test_count=5)
    # result = validator.validate_gdscript_syntax("target/scripts/player/ship.gd")
    # print("Validation Result:")
    # print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
