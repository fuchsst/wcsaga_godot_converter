"""
Unit tests for the LangGraph orchestrator.
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add the converter directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from converter.orchestrator.langgraph_orchestrator import LangGraphOrchestrator


class TestLangGraphOrchestrator:
    """Test cases for the LangGraphOrchestrator class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create temporary directories for source and target
        self.temp_dir = tempfile.TemporaryDirectory()
        self.source_dir = Path(self.temp_dir.name) / "source"
        self.target_dir = Path(self.temp_dir.name) / "target"

        # Create the directories
        self.source_dir.mkdir(parents=True, exist_ok=True)
        self.target_dir.mkdir(parents=True, exist_ok=True)

        # Create a simple test file in the source directory
        test_file = self.source_dir / "test.txt"
        test_file.write_text("This is a test file.")

    def teardown_method(self):
        """Tear down test fixtures after each test method."""
        self.temp_dir.cleanup()

    def test_orchestrator_initialization(self):
        """Test that LangGraphOrchestrator initializes correctly."""
        orchestrator = LangGraphOrchestrator(
            source_path=str(self.source_dir),
            target_path=str(self.target_dir),
            graph_file="test_graph.json",
        )

        assert orchestrator is not None
        assert orchestrator.source_path == self.source_dir
        assert orchestrator.target_path == self.target_dir

    def test_orchestrator_initialization_with_nonexistent_source(self):
        """Test that LangGraphOrchestrator raises an error for nonexistent source."""
        with pytest.raises(ValueError, match="Source path does not exist"):
            LangGraphOrchestrator("/nonexistent/path", str(self.target_dir))

    def test_get_status(self):
        """Test the get_status method."""
        orchestrator = LangGraphOrchestrator(
            source_path=str(self.source_dir),
            target_path=str(self.target_dir),
            graph_file="test_graph.json",
        )
        status = orchestrator.get_status()

        assert isinstance(status, dict)
        assert "source_path" in status
        assert "target_path" in status
        assert "graph_entities" in status
        assert "graph_dependencies" in status

        assert status["source_path"] == str(self.source_dir)
        assert status["target_path"] == str(self.target_dir)
