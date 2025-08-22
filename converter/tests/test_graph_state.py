"""
Unit tests for the GraphState Pydantic models.
"""

import pytest
from pydantic import ValidationError

from converter.graph_system.graph_state import CenturionGraphState, Task


class TestCenturionGraphState:
    """Test cases for the CenturionGraphState Pydantic model."""

    def test_graph_state_initialization(self):
        """Test that CenturionGraphState can be initialized with valid data."""
        # Test with minimal valid data
        state_data = {
            "task_queue": [],
            "active_task": None,
            "source_code_content": {},
            "status": "pending",
        }

        state = CenturionGraphState(**state_data)
        assert state is not None
        assert state.status == "pending"
        assert state.task_queue == []
        assert state.source_code_content == {}

    def test_graph_state_with_task_queue(self):
        """Test that CenturionGraphState can be initialized with a task queue."""
        task_queue = [
            Task(
                task_id="SHIP-GTC_FENRIS",
                entity_name="GTC Fenris",
                source_files=["source/tables/ships.tbl", "source/models/fenris.pof"],
                status="pending",
            )
        ]

        state_data = {
            "task_queue": task_queue,
            "active_task": None,
            "source_code_content": {},
            "status": "pending",
        }

        state = CenturionGraphState(**state_data)
        assert state is not None
        assert len(state.task_queue) == 1
        assert state.task_queue[0].task_id == "SHIP-GTC_FENRIS"

    def test_graph_state_with_active_task(self):
        """Test that CenturionGraphState can be initialized with an active task."""
        active_task = Task(
            task_id="SHIP-GTC_FENRIS",
            entity_name="GTC Fenris",
            source_files=["source/tables/ships.tbl", "source/models/fenris.pof"],
            status="in_progress",
        )

        state_data = {
            "task_queue": [],
            "active_task": active_task,
            "source_code_content": {},
            "status": "in_progress",
        }

        state = CenturionGraphState(**state_data)
        assert state is not None
        assert state.active_task.task_id == "SHIP-GTC_FENRIS"
        assert state.status == "in_progress"

    def test_graph_state_with_source_code_content(self):
        """Test that CenturionGraphState can be initialized with source code content."""
        source_code_content = {
            "source/tables/ships.tbl": "# Ship definitions\n$Name: GTC Fenris\n",
            "source/models/fenris.pof": "# Model data\n# Binary content",
        }

        state_data = {
            "task_queue": [],
            "active_task": None,
            "source_code_content": source_code_content,
            "status": "pending",
        }

        state = CenturionGraphState(**state_data)
        assert state is not None
        assert "source/tables/ships.tbl" in state.source_code_content
        assert "source/models/fenris.pof" in state.source_code_content
