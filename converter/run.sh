#!/bin/bash

# Script to run the Wing Commander Saga to Godot migration

set -e  # Exit on any error

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Virtual environment not activated. Please run 'source .venv/bin/activate' first."
    exit 1
fi

# Check if source and target directories are provided
if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <source_directory> <target_directory> [additional_args...]"
    echo "Example: $0 ../source ../target --verbose"
    exit 1
fi

SOURCE_DIR="$1"
TARGET_DIR="$2"
shift 2  # Remove the first two arguments, leaving any additional args

# Check if source directory exists
if [[ ! -d "$SOURCE_DIR" ]]; then
    echo "Error: Source directory '$SOURCE_DIR' does not exist."
    exit 1
fi

# Create target directory if it doesn't exist
mkdir -p "$TARGET_DIR"

echo "Running Wing Commander Saga to Godot migration..."
echo "Source directory: $SOURCE_DIR"
echo "Target directory: $TARGET_DIR"

# Run the migration
python orchestrator/main.py --source "$SOURCE_DIR" --target "$TARGET_DIR" "$@"

echo "Migration completed!"
