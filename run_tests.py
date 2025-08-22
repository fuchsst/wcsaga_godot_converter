#!/usr/bin/env python3
"""
Test Runner for Wing Commander Saga to Godot Converter

This script runs the test suite for the converter system.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_tests(test_module=None, verbose=False, coverage=False):
    """
    Run the test suite.

    Args:
        test_module: Specific test module to run (optional)
        verbose: Whether to run tests in verbose mode
        coverage: Whether to run tests with coverage

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    # Change to project root directory
    project_root = Path(__file__).parent.resolve()
    os.chdir(project_root)

    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]

    # Add converter tests directory
    if test_module:
        cmd.extend([f"converter/tests/test_{test_module}.py"])
    else:
        cmd.append("converter/tests/")

    # Add options
    if verbose:
        cmd.append("-v")

    if coverage:
        cmd.extend(["--cov=converter", "--cov-report=term-missing"])

    # Run tests
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        return e.returncode


def list_test_modules():
    """List all available test modules."""
    project_root = Path(__file__).parent.resolve()
    tests_dir = project_root / "converter" / "tests"

    if not tests_dir.exists():
        print("Tests directory not found")
        return

    print("Available test modules:")
    for test_file in tests_dir.glob("test_*.py"):
        module_name = test_file.stem.replace("test_", "")
        print(f"  {module_name}")


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(
        description="Test Runner for Wing Commander Saga to Godot Converter"
    )
    parser.add_argument(
        "module", nargs="?", help="Specific test module to run (without 'test_' prefix)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Run tests in verbose mode"
    )
    parser.add_argument(
        "--coverage", "-c", action="store_true", help="Run tests with coverage"
    )
    parser.add_argument(
        "--list", "-l", action="store_true", help="List available test modules"
    )

    args = parser.parse_args()

    # Handle list option
    if args.list:
        list_test_modules()
        return 0

    # Run tests
    return run_tests(args.module, args.verbose, args.coverage)


if __name__ == "__main__":
    sys.exit(main())
