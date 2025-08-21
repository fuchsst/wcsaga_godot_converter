"""
Unit tests for the task configurations.
"""

import os
import sys
import tempfile
import yaml
from pathlib import Path
import pytest

# Add the converter directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from orchestrator.main import MigrationOrchestrator


class TestTaskConfigurations:
    """Test cases for task configurations."""
    
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
    
    def test_analysis_task_loading(self):
        """Test that analysis task configuration loads correctly."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        
        # Check that tasks were loaded
        assert len(orchestrator.tasks) > 0
        
        # Check for specific task configurations
        assert "codebase_analysis_task" in orchestrator.tasks
        analysis_task = orchestrator.tasks["codebase_analysis_task"]
        
        assert "name" in analysis_task
        assert "description" in analysis_task
        assert "expected_output" in analysis_task
        assert "agent" in analysis_task
    
    def test_planning_task_loading(self):
        """Test that planning task configuration loads correctly."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        
        # Check for specific task configurations
        assert "migration_planning_task" in orchestrator.tasks
        planning_task = orchestrator.tasks["migration_planning_task"]
        
        assert "name" in planning_task
        assert "description" in planning_task
        assert "expected_output" in planning_task
        assert "agent" in planning_task
        assert "context" in planning_task
    
    def test_decomposition_task_loading(self):
        """Test that decomposition task configuration loads correctly."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        
        # Check for specific task configurations
        assert "task_decomposition_task" in orchestrator.tasks
        decomposition_task = orchestrator.tasks["task_decomposition_task"]
        
        assert "name" in decomposition_task
        assert "description" in decomposition_task
        assert "expected_output" in decomposition_task
        assert "agent" in decomposition_task
        assert "context" in decomposition_task
    
    def test_refactoring_task_loading(self):
        """Test that refactoring task configuration loads correctly."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        
        # Check for specific task configurations
        assert "code_refactoring_task" in orchestrator.tasks
        refactoring_task = orchestrator.tasks["code_refactoring_task"]
        
        assert "name" in refactoring_task
        assert "description" in refactoring_task
        assert "expected_output" in refactoring_task
        assert "agent" in refactoring_task
        assert "context" in refactoring_task
    
    def test_testing_task_loading(self):
        """Test that testing task configuration loads correctly."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        
        # Check for specific task configurations
        assert "unit_test_generation_task" in orchestrator.tasks
        unit_test_task = orchestrator.tasks["unit_test_generation_task"]
        
        assert "name" in unit_test_task
        assert "description" in unit_test_task
        assert "expected_output" in unit_test_task
        assert "agent" in unit_test_task
        assert "context" in unit_test_task
    
    def test_validation_task_loading(self):
        """Test that validation task configuration loads correctly."""
        orchestrator = MigrationOrchestrator(str(self.source_dir), str(self.target_dir))
        
        # Check for specific task configurations
        assert "code_validation_task" in orchestrator.tasks
        validation_task = orchestrator.tasks["code_validation_task"]
        
        assert "name" in validation_task
        assert "description" in validation_task
        assert "expected_output" in validation_task
        assert "agent" in validation_task
        assert "context" in validation_task