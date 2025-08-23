#!/bin/bash

# This script runs pytest within the 'data_converter' directory,
# using uv to handle the virtual environment from the project root.

# Determine the script's directory and the project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)" # Moves up one level from data_converter to project root

# Default to running all tests if no specific test is provided
TEST_PATH=${1:-"tests/"}
shift # Remove the test path from arguments if provided

echo "Running uv run pytest $TEST_PATH $@"
# Execute pytest using uv from the project root directory
(cd "$PROJECT_ROOT_DIR" && uv run pytest "$TEST_PATH" "$@" -v)
