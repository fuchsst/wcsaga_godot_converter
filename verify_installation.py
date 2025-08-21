#!/usr/bin/env python3
"""
Final Verification Script for Wing Commander Saga to Godot Converter

This script verifies that the project has been properly restructured
with modern Python development practices.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_file_exists(filepath):
    """Check if a file exists and print status."""
    if Path(filepath).exists():
        print(f"✅ Found: {filepath}")
        return True
    else:
        print(f"❌ Missing: {filepath}")
        return False


def run_command(command, description):
    """Run a command and print status."""
    try:
        print(f"🔍 {description}...")
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"   Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"❌ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {str(e)}")
        return False


def main():
    """Main verification function."""
    print("🚀 Wing Commander Saga to Godot Converter - Final Verification")
    print("=" * 70)
    
    # Check project structure
    print("\n📂 Checking project structure...")
    required_files = [
        "pyproject.toml",
        "README.md",
        "QWEN.md",
        "Makefile",
        "requirements.txt",
        "converter/__init__.py",
        "converter/README.md"
    ]
    
    all_good = True
    for filepath in required_files:
        if not check_file_exists(filepath):
            all_good = False
    
    # Check virtual environment
    print("\n🔧 Checking virtual environment...")
    venv_activated = "VIRTUAL_ENV" in os.environ
    if venv_activated:
        print(f"✅ Virtual environment activated: {os.environ['VIRTUAL_ENV']}")
    else:
        print("⚠️  Virtual environment not activated (this is OK for verification)")
    
    # Run basic import test
    print("\n🧪 Running basic import test...")
    try:
        import converter
        print("✅ Converter package imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import converter package: {str(e)}")
        all_good = False
    
    # Check dependencies
    print("\n📦 Checking key dependencies...")
    try:
        import crewai
        print("✅ CrewAI imported successfully")
        
        import pydantic
        print("✅ Pydantic imported successfully")
        
        import yaml
        print("✅ PyYAML imported successfully")
        
    except ImportError as e:
        print(f"❌ Failed to import dependencies: {str(e)}")
        all_good = False
    
    # Run a simple test
    print("\n🏁 Running simple functionality test...")
    test_result = run_command(
        f"{sys.executable} -m pytest converter/tests/test_example.py::test_example -v",
        "Basic test execution"
    )
    if not test_result:
        all_good = False
    
    # Summary
    print("\n" + "=" * 70)
    if all_good:
        print("🎉 VERIFICATION COMPLETE - All checks passed!")
        print("\n✨ The Wing Commander Saga to Godot Converter project has been")
        print("   successfully enhanced with modern Python development practices.")
        print("\n🚀 Ready for professional development and production use!")
        return 0
    else:
        print("⚠️  VERIFICATION COMPLETE - Some checks failed")
        print("\n📝 Please review the output above to address any issues.")
        return 1


if __name__ == "__main__":
    sys.exit(main())