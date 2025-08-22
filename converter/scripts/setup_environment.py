#!/usr/bin/env python3
"""
Environment Setup Script for Wing Commander Saga to Godot Migration

This script helps set up the development environment for the migration project,
including installing dependencies and configuring tools.
"""

import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class EnvironmentSetup:
    """Class to handle environment setup for the migration project."""

    def __init__(self, project_root: str = "."):
        """
        Initialize the environment setup.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root).resolve()
        self.converter_dir = self.project_root / "converter"

    def install_python_dependencies(self) -> bool:
        """
        Install Python dependencies from requirements.txt.

        Returns:
            True if successful, False otherwise
        """
        logger.info("Installing Python dependencies...")

        requirements_file = self.converter_dir / "requirements.txt"
        if not requirements_file.exists():
            logger.error(f"Requirements file not found: {requirements_file}")
            return False

        try:
            # Install dependencies
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                check=True,
                capture_output=True,
                text=True,
            )

            logger.info("Python dependencies installed successfully")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install Python dependencies: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during dependency installation: {str(e)}")
            return False

    def check_qwen_code_installation(self) -> bool:
        """
        Check if qwen-code is installed and accessible.

        Returns:
            True if installed, False otherwise
        """
        logger.info("Checking qwen-code installation...")

        try:
            # Try to run qwen-code with --help to check if it's installed
            result = subprocess.run(
                ["qwen-code", "--help"], capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                logger.info("qwen-code is installed and accessible")
                return True
            else:
                logger.warning("qwen-code is installed but returned an error")
                return False

        except subprocess.TimeoutExpired:
            logger.error("qwen-code command timed out")
            return False
        except FileNotFoundError:
            logger.warning("qwen-code is not installed or not in PATH")
            return False
        except Exception as e:
            logger.error(f"Error checking qwen-code installation: {str(e)}")
            return False

    def install_qwen_code(self) -> bool:
        """
        Install qwen-code (this would typically be done manually).

        Returns:
            True if successful, False otherwise
        """
        logger.info(
            "Please install qwen-code manually following the official documentation"
        )
        logger.info(
            "Visit: https://github.com/QwenLM/qwen-code for installation instructions"
        )
        return False

    def setup_directory_structure(self) -> bool:
        """
        Set up the required directory structure for the migration.

        Returns:
            True if successful, False otherwise
        """
        logger.info("Setting up directory structure...")

        # Define required directories
        required_dirs = [
            "source",  # Source C++ codebase
            "target",  # Target Godot project
            "logs",  # Log files
            "backups",  # Backup files
            "temp",  # Temporary files
        ]

        try:
            for dir_name in required_dirs:
                dir_path = self.project_root / dir_name
                dir_path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {dir_path}")

            logger.info("Directory structure set up successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to set up directory structure: {str(e)}")
            return False

    def create_env_file(self) -> bool:
        """
        Create a .env file with default environment variables.

        Returns:
            True if successful, False otherwise
        """
        logger.info("Creating .env file...")

        env_file = self.project_root / ".env"

        # Default environment variables
        env_content = """# Environment variables for Wing Commander Saga to Godot Migration

# DeepSeek API configuration
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# qwen-code configuration
QWEN_CODE_COMMAND=qwen-code
QWEN_CODE_TIMEOUT=300

# Project paths
SOURCE_PATH=./source
TARGET_PATH=./target
LOG_PATH=./logs

# Migration settings
MAX_WORKERS=4
DEBUG_MODE=False
"""

        try:
            with open(env_file, "w", encoding="utf-8") as f:
                f.write(env_content)

            logger.info(f"Created .env file: {env_file}")
            logger.info(
                "Please update the .env file with your actual API keys and settings"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to create .env file: {str(e)}")
            return False

    def validate_setup(self) -> dict:
        """
        Validate the current setup and report status.

        Returns:
            Dictionary with validation results
        """
        logger.info("Validating setup...")

        results = {
            "python_dependencies": self.install_python_dependencies(),
            "qwen_code": self.check_qwen_code_installation(),
            "directories": self.setup_directory_structure(),
            "env_file": self.create_env_file(),
        }

        # Calculate overall status
        success_count = sum(1 for result in results.values() if result)
        total_count = len(results)

        logger.info(
            f"Setup validation complete: {success_count}/{total_count} checks passed"
        )

        return results

    def run_full_setup(self) -> bool:
        """
        Run the complete setup process.

        Returns:
            True if successful, False otherwise
        """
        logger.info("Running full environment setup...")

        # Run all setup steps
        steps = [
            ("Installing Python dependencies", self.install_python_dependencies),
            ("Setting up directory structure", self.setup_directory_structure),
            ("Creating .env file", self.create_env_file),
            ("Checking qwen-code installation", self.check_qwen_code_installation),
        ]

        success = True
        for step_name, step_func in steps:
            logger.info(f"Executing: {step_name}")
            try:
                result = step_func()
                if not result:
                    logger.warning(f"Step failed: {step_name}")
                    success = False
            except Exception as e:
                logger.error(f"Step failed with exception: {step_name} - {str(e)}")
                success = False

        if success:
            logger.info("Full environment setup completed successfully!")
            logger.info("Please remember to:")
            logger.info("1. Install qwen-code if not already installed")
            logger.info("2. Update the .env file with your actual API keys")
            logger.info("3. Verify all paths are correct")
        else:
            logger.error("Full environment setup completed with some errors")

        return success


def main():
    """Main entry point for the setup script."""
    parser = argparse.ArgumentParser(
        description="Environment Setup for Wing Commander Saga to Godot Migration"
    )
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--full", action="store_true", help="Run full setup")
    parser.add_argument(
        "--dependencies", action="store_true", help="Install Python dependencies only"
    )
    parser.add_argument(
        "--directories", action="store_true", help="Set up directory structure only"
    )
    parser.add_argument("--env", action="store_true", help="Create .env file only")
    parser.add_argument(
        "--validate", action="store_true", help="Validate current setup"
    )

    args = parser.parse_args()

    # Create setup instance
    setup = EnvironmentSetup(args.project_root)

    # Execute requested actions
    if args.full:
        setup.run_full_setup()
    elif args.dependencies:
        setup.install_python_dependencies()
    elif args.directories:
        setup.setup_directory_structure()
    elif args.env:
        setup.create_env_file()
    elif args.validate:
        results = setup.validate_setup()
        print("\nSetup Validation Results:")
        for check, result in results.items():
            status = "✓" if result else "✗"
            print(f"  {status} {check}")
    else:
        # Default action: show help
        parser.print_help()


if __name__ == "__main__":
    main()
