"""
Tests for the centralized utilities module.
"""

import os
import sys
import time
import logging
import subprocess
from unittest.mock import patch, MagicMock

# Add converter to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from converter.utils import (
    setup_logging, 
    time_execution, 
    CommandExecutor, 
    handle_graceful,
    generate_timestamp,
    generate_request_id,
    calculate_duration
)


def test_setup_logging():
    """Test that setup_logging creates a properly configured logger."""
    # Clear any existing handlers to avoid interference
    for handler in logging.getLogger().handlers[:]:
        logging.getLogger().removeHandler(handler)
    
    logger = setup_logging("test_logger", logging.DEBUG)
    
    assert logger.name == "test_logger"
    # The root logger level might be different, but our logger should be accessible
    assert logger.getEffectiveLevel() <= logging.DEBUG
    # The handler is on the root logger, not the specific logger
    assert len(logging.getLogger().handlers) > 0


def test_time_execution():
    """Test the time_execution decorator."""
    
    @time_execution
    def test_function():
        time.sleep(0.01)
        return "success"
    
    result = test_function()
    assert result == "success"


def test_command_executor_success():
    """Test CommandExecutor with successful command."""
    with patch('subprocess.Popen') as mock_popen:
        # Mock successful process
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = ("stdout output", "")
        mock_popen.return_value = mock_process
        
        result = CommandExecutor.execute_command("echo test")
        
        assert result["return_code"] == 0
        assert result["stdout"] == "stdout output"
        assert result["stderr"] == ""
        assert "execution_time" in result


def test_command_executor_timeout():
    """Test CommandExecutor with timeout."""
    with patch('subprocess.Popen') as mock_popen:
        mock_process = MagicMock()
        mock_process.communicate.side_effect = subprocess.TimeoutExpired("echo test", 1)
        mock_popen.return_value = mock_process
        
        result = CommandExecutor.execute_command("echo test", timeout_seconds=1)
        
        assert result["return_code"] == -1
        assert result["error"] == "timeout"
        assert "timed out" in result["stderr"]


def test_handle_graceful():
    """Test the handle_graceful decorator."""
    
    @handle_graceful
    def failing_function():
        raise ValueError("Test error")
    
    # Should re-raise the exception but log it
    with patch('converter.utils.setup_logging') as mock_logging:
        mock_logger = MagicMock()
        mock_logging.return_value = mock_logger
        
        try:
            failing_function()
            assert False, "Should have raised an exception"
        except ValueError as e:
            assert str(e) == "Test error"


def test_generate_timestamp():
    """Test timestamp generation."""
    timestamp = generate_timestamp()
    assert isinstance(timestamp, float)
    assert timestamp > 0


def test_generate_request_id():
    """Test request ID generation."""
    request_id = generate_request_id("test_entity", "test")
    assert request_id.startswith("test_test_entity_")
    # Should have prefix, entity, and timestamp (3 parts)
    parts = request_id.split("_")
    assert len(parts) >= 3  # At least prefix, entity, timestamp
    assert parts[0] == "test"
    assert parts[1] == "test"
    assert parts[2] == "entity"


def test_calculate_duration():
    """Test duration calculation."""
    start_time = time.time()
    time.sleep(0.01)
    end_time = time.time()
    
    duration = calculate_duration(start_time, end_time)
    assert isinstance(duration, float)
    assert duration > 0
    assert duration < 1.0
    
    # Test with default end time
    duration_default = calculate_duration(start_time)
    assert duration_default > duration


def test_command_executor_with_input():
    """Test CommandExecutor with input data."""
    with patch('subprocess.Popen') as mock_popen:
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.communicate.return_value = ("processed output", "")
        mock_popen.return_value = mock_process
        
        result = CommandExecutor.execute_command(
            "cat", 
            input_data="test input"
        )
        
        assert result["return_code"] == 0
        assert result["stdout"] == "processed output"
        
        # Verify communicate was called with input
        mock_process.communicate.assert_called_with(
            input="test input", 
            timeout=300
        )