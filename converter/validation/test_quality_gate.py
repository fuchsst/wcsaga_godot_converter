"""
Test Quality Gate Implementation

This module implements a test quality gate to validate completeness and rigor of generated tests.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
from converter.utils import setup_logging, generate_timestamp

# Configure logging
logger = setup_logging(__name__)


class TestQualityGate:
    """Quality gate for validating test completeness and rigor."""
    
    def __init__(self, min_coverage: float = 85.0, min_test_count: int = 5):
        """
        Initialize the test quality gate.
        
        Args:
            min_coverage: Minimum required code coverage percentage
            min_test_count: Minimum required number of tests
        """
        self.min_coverage = min_coverage
        self.min_test_count = min_test_count
        
        logger.info(f"Test Quality Gate initialized (min_coverage={min_coverage}%, min_test_count={min_test_count})")
    
    def validate_test_quality(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the quality of generated tests.
        
        Args:
            test_results: Results from test execution
            
        Returns:
            Dictionary with validation results
        """
        validation_result = {
            "timestamp": generate_timestamp(),
            "passed": False,
            "score": 0.0,
            "issues": [],
            "metrics": {},
            "recommendations": []
        }
        
        try:
            # Extract metrics
            metrics = self._extract_test_metrics(test_results)
            validation_result["metrics"] = metrics
            
            # Calculate quality score
            score = self._calculate_quality_score(metrics)
            validation_result["score"] = score
            
            # Check for issues
            issues = self._identify_quality_issues(metrics)
            validation_result["issues"] = issues
            
            # Generate recommendations
            recommendations = self._generate_recommendations(metrics, issues)
            validation_result["recommendations"] = recommendations
            
            # Determine if tests pass quality gate
            passed = self._determine_pass_fail(metrics, issues)
            validation_result["passed"] = passed
            
            logger.info(f"Test quality validation completed: {'PASSED' if passed else 'FAILED'} (Score: {score:.1f}%)")
            
        except Exception as e:
            logger.error(f"Error during test quality validation: {str(e)}")
            validation_result["issues"].append({
                "type": "validation_error",
                "message": f"Error during validation: {str(e)}"
            })
            validation_result["passed"] = False
        
        return validation_result
    
    def _extract_test_metrics(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant metrics from test results.
        
        Args:
            test_results: Results from test execution
            
        Returns:
            Dictionary with extracted metrics
        """
        metrics = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "coverage_percentage": 0.0,
            "test_duration": 0.0,
            "assertion_count": 0,
            "unique_functions_tested": 0
        }
        
        # Extract from test results
        if "total" in test_results:
            metrics["total_tests"] = test_results["total"]
        
        if "passed" in test_results:
            metrics["passed_tests"] = test_results["passed"]
        
        if "failed" in test_results:
            metrics["failed_tests"] = test_results["failed"]
        
        if "coverage" in test_results:
            metrics["coverage_percentage"] = float(test_results["coverage"])
        
        if "duration" in test_results:
            metrics["test_duration"] = float(test_results["duration"])
        
        # Calculate derived metrics
        if metrics["total_tests"] > 0:
            metrics["pass_rate"] = (metrics["passed_tests"] / metrics["total_tests"]) * 100
        
        return metrics
    
    def _calculate_quality_score(self, metrics: Dict[str, Any]) -> float:
        """
        Calculate an overall quality score based on metrics.
        
        Args:
            metrics: Test metrics
            
        Returns:
            Quality score (0-100)
        """
        score = 0.0
        max_score = 0.0
        
        # Coverage contribution (40% of score)
        coverage_score = min(metrics.get("coverage_percentage", 0), 100)
        score += coverage_score * 0.4
        max_score += 40.0
        
        # Pass rate contribution (30% of score)
        pass_rate = metrics.get("pass_rate", 0)
        score += pass_rate * 0.3
        max_score += 30.0
        
        # Test count contribution (20% of score)
        test_count = metrics.get("total_tests", 0)
        test_count_score = min(test_count / self.min_test_count * 100, 100) if self.min_test_count > 0 else 0
        score += test_count_score * 0.2
        max_score += 20.0
        
        # Performance contribution (10% of score)
        duration = metrics.get("test_duration", 0)
        # Shorter tests are better, so invert the scale
        if duration > 0:
            duration_score = max(0, 100 - (duration * 10))  # Arbitrary scaling
            score += duration_score * 0.1
            max_score += 10.0
        
        # Normalize score
        if max_score > 0:
            score = (score / max_score) * 100
        
        return score
    
    def _identify_quality_issues(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Identify quality issues based on metrics.
        
        Args:
            metrics: Test metrics
            
        Returns:
            List of quality issues
        """
        issues = []
        
        # Check coverage
        coverage = metrics.get("coverage_percentage", 0)
        if coverage < self.min_coverage:
            issues.append({
                "type": "low_coverage",
                "message": f"Code coverage {coverage:.1f}% is below minimum {self.min_coverage}%",
                "severity": "high" if coverage < self.min_coverage * 0.5 else "medium"
            })
        
        # Check test count
        test_count = metrics.get("total_tests", 0)
        if test_count < self.min_test_count:
            issues.append({
                "type": "low_test_count",
                "message": f"Test count {test_count} is below minimum {self.min_test_count}",
                "severity": "high" if test_count == 0 else "medium"
            })
        
        # Check pass rate
        pass_rate = metrics.get("pass_rate", 0)
        if pass_rate < 90.0:  # Less than 90% pass rate
            issues.append({
                "type": "low_pass_rate",
                "message": f"Pass rate {pass_rate:.1f}% is below recommended 90%",
                "severity": "high" if pass_rate < 50.0 else "medium"
            })
        
        # Check for failed tests
        failed_tests = metrics.get("failed_tests", 0)
        if failed_tests > 0:
            issues.append({
                "type": "failed_tests",
                "message": f"{failed_tests} tests failed",
                "severity": "high" if failed_tests > metrics.get("total_tests", 0) * 0.1 else "medium"
            })
        
        return issues
    
    def _generate_recommendations(self, metrics: Dict[str, Any], 
                                issues: List[Dict[str, Any]]) -> List[str]:
        """
        Generate recommendations for improving test quality.
        
        Args:
            metrics: Test metrics
            issues: List of quality issues
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Check for low coverage
        coverage = metrics.get("coverage_percentage", 0)
        if coverage < self.min_coverage:
            gap = self.min_coverage - coverage
            recommendations.append(f"Increase code coverage by {gap:.1f}% - focus on untested functions")
        
        # Check for low test count
        test_count = metrics.get("total_tests", 0)
        if test_count < self.min_test_count:
            needed = self.min_test_count - test_count
            recommendations.append(f"Add {needed} more tests to meet minimum requirement")
        
        # Check for failed tests
        failed_tests = metrics.get("failed_tests", 0)
        if failed_tests > 0:
            recommendations.append(f"Fix {failed_tests} failed tests")
        
        # General recommendations
        if metrics.get("total_tests", 0) > 0:
            recommendations.append("Consider adding edge case tests for boundary conditions")
            recommendations.append("Add tests for error handling and exception cases")
            recommendations.append("Verify test independence and avoid test interdependencies")
        
        return recommendations
    
    def _determine_pass_fail(self, metrics: Dict[str, Any], 
                           issues: List[Dict[str, Any]]) -> bool:
        """
        Determine if tests pass the quality gate.
        
        Args:
            metrics: Test metrics
            issues: List of quality issues
            
        Returns:
            True if tests pass, False otherwise
        """
        # Check for critical issues
        critical_issues = [issue for issue in issues if issue.get("severity") == "high"]
        if critical_issues:
            logger.warning(f"Critical quality issues found: {len(critical_issues)}")
            return False
        
        # Check minimum requirements
        coverage = metrics.get("coverage_percentage", 0)
        if coverage < self.min_coverage:
            logger.warning(f"Coverage {coverage:.1f}% below minimum {self.min_coverage}%")
            return False
        
        test_count = metrics.get("total_tests", 0)
        if test_count < self.min_test_count:
            logger.warning(f"Test count {test_count} below minimum {self.min_test_count}")
            return False
        
        # Check for any failed tests
        failed_tests = metrics.get("failed_tests", 0)
        if failed_tests > 0:
            logger.warning(f"{failed_tests} tests failed")
            return False
        
        return True


def main():
    """Main function for testing the TestQualityGate."""
    # Create test quality gate
    quality_gate = TestQualityGate(min_coverage=85.0, min_test_count=5)
    
    # Test with good results
    good_results = {
        "total": 10,
        "passed": 10,
        "failed": 0,
        "coverage": 92.5,
        "duration": 2.5
    }
    
    result = quality_gate.validate_test_quality(good_results)
    print("Good test results validation:", result)
    
    # Test with poor results
    poor_results = {
        "total": 3,
        "passed": 2,
        "failed": 1,
        "coverage": 65.0,
        "duration": 1.2
    }
    
    result = quality_gate.validate_test_quality(poor_results)
    print("Poor test results validation:", result)


if __name__ == "__main__":
    main()