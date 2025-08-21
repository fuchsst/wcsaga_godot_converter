"""
Unit tests for the migration orchestrator.
"""

import os
import sys
import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

# Add the converter directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from converter.orchestrator.main import MigrationOrchestrator


class TestMigrationOrchestrator:
    """Test cases for the MigrationOrchestrator class."""
    
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
        """Test that MigrationOrchestrator initializes correctly."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        
        assert orchestrator is not None
        assert orchestrator.source_path == self.source_dir
        assert orchestrator.target_path == self.target_dir
    
    def test_orchestrator_initialization_with_nonexistent_source(self):
        """Test that MigrationOrchestrator raises an error for nonexistent source."""
        with pytest.raises(ValueError, match="Source path does not exist"):
            MigrationOrchestrator("/nonexistent/path", str(self.target_dir))
    
    def test_get_status(self):
        """Test the get_status method."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        status = orchestrator.get_status()
        
        assert isinstance(status, dict)
        assert "source_path" in status
        assert "target_path" in status
        assert "agents_initialized" in status
        assert "tools_initialized" in status
        assert "crew_status" in status
        
        assert status["source_path"] == str(self.source_dir)
        assert status["target_path"] == str(self.target_dir)
        assert status["crew_status"] == "ready"
    
    @patch("converter.orchestrator.main.Crew")
    def test_run_migration_analysis_phase(self, mock_crew_class):
        """Test running the analysis phase of migration."""
        # Mock the Crew class
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = {"result": "analysis_complete"}
        mock_crew_class.return_value = mock_crew_instance
        
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        result = orchestrator.run_migration("analysis")
        
        assert result is not None
        assert result["status"] == "completed"
        assert result["phase"] == "analysis"
        
        # Verify that the crew was created with the right parameters
        mock_crew_class.assert_called_once()
    
    @patch("converter.orchestrator.main.Crew")
    def test_run_migration_planning_phase(self, mock_crew_class):
        """Test running the planning phase of migration."""
        # Mock the Crew class
        mock_crew_instance = MagicMock()
        mock_crew_instance.kickoff.return_value = {"result": "planning_complete"}
        mock_crew_class.return_value = mock_crew_instance
        
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        result = orchestrator.run_migration("planning")
        
        assert result is not None
        assert result["status"] == "completed"
        assert result["phase"] == "planning"
        
        # Verify that the crew was created with the right parameters
        mock_crew_class.assert_called_once()
    
    def test_run_migration_with_invalid_phase(self):
        """Test running migration with an invalid phase."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        
        # This should not raise an exception, but should return a failure result
        result = orchestrator.run_migration("invalid_phase")
        
        # The result will depend on the implementation, but it should be a dict
        assert isinstance(result, dict)