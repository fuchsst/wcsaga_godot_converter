#!/bin/bash

# Script to run the converter tests

set -e  # Exit on any error

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Virtual environment not activated. Please run 'source .venv/bin/activate' first."
    exit 1
fi

# Default to running all tests
TEST_MODULE=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --list)
            echo "Available test modules:"
            ls tests/test_*.py | sed 's/tests\/test_//' | sed 's/\.py$//' | sort
            exit 0
            ;;
        --verbose|-v)
            PYTEST_ARGS="$PYTEST_ARGS -v"
            shift
            ;;
        *)
            TEST_MODULE="$1"
            shift
            ;;
    esac
done

# Run tests
if [[ -n "$TEST_MODULE" ]]; then
    echo "Running tests for module: $TEST_MODULE"
    pytest tests/test_${TEST_MODULE}.py $PYTEST_ARGS
else
    echo "Running all tests"
    pytest tests/ $PYTEST_ARGS
fi
