"""
Centralized utilities for the WCSAGA Godot Converter.

This module provides shared utilities to eliminate code duplication across the codebase.
"""

import functools
import logging
import os
import subprocess
import time
from typing import Any, Callable, Dict, Optional


def setup_logging(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Configure and return a logger with standardized setup.

    Args:
        name: Logger name (typically __name__)
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(name)


def time_execution(func: Callable) -> Callable:
    """
    Decorator to measure and log function execution time.

    Args:
        func: Function to decorate

    Returns:
        Decorated function with timing
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time

        logger = logging.getLogger(func.__module__)
        logger.debug(f"{func.__name__} executed in {duration:.4f} seconds")

        return result

    return wrapper


class CommandExecutor:
    """Standardized command execution with timeouts and error handling."""

    @staticmethod
    def execute_command(
        command: str,
        timeout_seconds: int = 300,
        working_directory: Optional[str] = None,
        input_data: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute a shell command with standardized error handling.

        Args:
            command: Shell command to execute
            timeout_seconds: Command timeout in seconds
            working_directory: Working directory for execution
            input_data: Input data to send to stdin

        Returns:
            Dictionary with execution results
        """
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE if input_data else None,
                text=True,
                cwd=working_directory,
            )

            stdout, stderr = process.communicate(
                input=input_data, timeout=timeout_seconds
            )

            return {
                "command": command,
                "return_code": process.returncode,
                "stdout": stdout,
                "stderr": stderr,
                "execution_time": time.time(),
            }

        except subprocess.TimeoutExpired as e:
            return {
                "command": command,
                "return_code": -1,
                "stdout": getattr(e, "stdout", ""),
                "stderr": f"Command timed out after {timeout_seconds} seconds",
                "error": "timeout",
                "execution_time": time.time(),
            }
        except Exception as e:
            return {
                "command": command,
                "return_code": -1,
                "stdout": "",
                "stderr": str(e),
                "error": "exception",
                "execution_time": time.time(),
            }


def handle_graceful(func: Callable) -> Callable:
    """
    Decorator for graceful error handling that catches and logs exceptions.

    Args:
        func: Function to decorate

    Returns:
        Decorated function with error handling
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = logging.getLogger(func.__module__)
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            raise

    return wrapper


def generate_timestamp() -> float:
    """
    Generate a standardized timestamp.

    Returns:
        Current timestamp as float
    """
    return time.time()


def generate_request_id(entity_id: str, prefix: str = "req") -> str:
    """
    Generate a standardized request ID with timestamp.

    Args:
        entity_id: Entity identifier
        prefix: Request ID prefix

    Returns:
        Standardized request ID
    """
    return f"{prefix}_{entity_id}_{int(time.time())}"


def calculate_duration(start_time: float, end_time: Optional[float] = None) -> float:
    """
    Calculate duration between start and end times.

    Args:
        start_time: Start timestamp
        end_time: End timestamp (defaults to current time)

    Returns:
        Duration in seconds
    """
    if end_time is None:
        end_time = time.time()
    return end_time - start_time
