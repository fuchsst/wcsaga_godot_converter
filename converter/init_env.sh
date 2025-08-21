#!/bin/bash

# Script to initialize the virtual environment and install dependencies using uv

set -e  # Exit on any error

echo "Initializing virtual environment with uv..."

# Create virtual environment
uv venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
uv pip install -r requirements.txt

echo "Virtual environment setup complete!"
echo "To activate the environment, run: source .venv/bin/activate"
