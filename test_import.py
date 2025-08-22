#!/usr/bin/env python3
"""
Simple test script to check if converter package can be imported
"""

try:
    import sys
    import os
    # Add the project root to the path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # Try to import the converter package
    import converter
    print("Successfully imported converter package")
    print(f"Converter version: {converter.__version__}")
    
except Exception as e:
    print(f"Error importing converter package: {e}")
    import traceback
    traceback.print_exc()