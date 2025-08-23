#!/bin/bash

# This script runs a Python module located within the 'data_converter' directory or its subdirectories,
# using uv to handle the virtual environment from the project root.

# Determine the script's directory and the project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)" # Moves up one level from data_converter to project root

# Check if a Python module name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <python_module_to_run> [args...]"
  echo "Example: $0 pof_parser.cli --input my_file.pof"
  exit 1
fi

PYTHON_MODULE=$1
shift # Remove the module name from the arguments list, so $@ contains only args for the python script

# Convert relative --source and --output to absolute paths
args=()
while (( "$#" )); do
  case "$1" in
    --source|--output)
      args+=("$1")
      shift
      # Use realpath to resolve the path
      args+=("$(realpath "$1")")
      shift
      ;;
    *)
      args+=("$1")
      shift
      ;;
  esac
done

echo "Running uv run python -m $PYTHON_MODULE ${args[*]}"
# Execute the Python module using uv from the project root directory
(cd "$PROJECT_ROOT_DIR" && uv run python -m "$PYTHON_MODULE" "${args[@]}")
