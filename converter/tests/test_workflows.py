"""
Tests for Workflows

This module contains tests for the SequentialWorkflow and HierarchicalWorkflow components.
"""

import unittest
import time
from unittest.mock import MagicMock

# Import the workflow components to test
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from workflows.sequential_workflow import SequentialWorkflow, Task, TaskStatus, example_task_executor
from workflows.hierarchical_workflow import HierarchicalWorkflow, SubWorkflow, create_migration_phase_workflow


class TestSequentialWorkflow(unittest.TestCase):
    """Test cases for SequentialWorkflow."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.workflow = SequentialWorkflow("Test Workflow")
    
    def test_initialization(self):
        """Test that the workflow initializes correctly."""
        self.assertEqual(self.workflow.name, "Test Workflow")
        self.assertEqual(self.workflow.status, TaskStatus.PENDING)
        self.assertEqual(len(self.workflow.tasks), 0)
    
    def test_add_task(self):
        """Test adding a task to the workflow."""
        task = Task(
            id="test_task",
            name="Test Task",
            description="A test task",
            agent="TestAgent",
            expected_output="Test output"
        )
        
        self.workflow.add_task(task)
        self.assertEqual(len(self.workflow.tasks), 1)
        self.assertEqual(self.workflow.tasks[0], task)
    
    def test_add_tasks(self):
        """Test adding multiple tasks to the workflow."""
        tasks = [
            Task(
                id="task_1",
                name="Task 1",
                description="First task",
                agent="TestAgent",
                expected_output="Output 1"
            ),
            Task(
                id="task_2",
                name="Task 2",
                description="Second task",
                agent="TestAgent",
                expected_output="Output 2"
            )
        ]
        
        self.workflow.add_tasks(tasks)
        self.assertEqual(len(self.workflow.tasks), 2)
        self.assertEqual(self.workflow.tasks[0].id, "task_1")
        self.assertEqual(self.workflow.tasks[1].id, "task_2")
    
    def test_can_execute_task_no_dependencies(self):
        """Test checking if a task with no dependencies can be executed."""
        task = Task(
            id="test_task",
            name="Test Task",
            description="A test task",
            agent="TestAgent",
            expected_output="Test output"
        )
        
        self.assertTrue(self.workflow.can_execute_task(task))
    
    def test_can_execute_task_with_dependencies(self):
        """Test checking if a task with dependencies can be executed."""
        # Create tasks with dependencies
        task1 = Task(
            id="task_1",
            name="Task 1",
            description="First task",
            agent="TestAgent",
            expected_output="Output 1"
        )
        
        task2 = Task(
            id="task_2",
            name="Task 2",
            description="Second task",
            agent="TestAgent",
            expected_output="Output 2",
            dependencies=["task_1"]
        )
        
        self.workflow.add_tasks([task1, task2])
        
        # task2 cannot be executed because task1 is not completed
        self.assertFalse(self.workflow.can_execute_task(task2))
        
        # Complete task1
        task1.status = TaskStatus.COMPLETED
        
        # Now task2 can be executed
        self.assertTrue(self.workflow.can_execute_task(task2))
    
    def test_execute_task_success(self):
        """Test executing a task successfully."""
        task = Task(
            id="test_task",
            name="Test Task",
            description="A test task",
            agent="TestAgent",
            expected_output="Test output"
        )
        
        self.workflow.add_task(task)
        success = self.workflow.execute_task(task, example_task_executor)
        
        self.assertTrue(success)
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertIsNotNone(task.start_time)
        self.assertIsNotNone(task.end_time)
        self.assertIsNotNone(task.result)
    
    def test_execute_task_failure(self):
        """Test executing a task that fails."""
        task = Task(
            id="test_task",
            name="Test Task",
            description="A test task",
            agent="TestAgent",
            expected_output="Test output"
        )
        
        # Create a failing executor
        def failing_executor(task):
            raise Exception("Task execution failed")
        
        self.workflow.add_task(task)
        success = self.workflow.execute_task(task, failing_executor)
        
        self.assertFalse(success)
        self.assertEqual(task.status, TaskStatus.FAILED)
        self.assertIsNotNone(task.start_time)
        self.assertIsNotNone(task.end_time)
        self.assertIsNotNone(task.error)
    
    def test_execute_all(self):
        """Test executing all tasks in the workflow."""
        tasks = [
            Task(
                id="task_1",
                name="Task 1",
                description="First task",
                agent="TestAgent",
                expected_output="Output 1"
            ),
            Task(
                id="task_2",
                name="Task 2",
                description="Second task",
                agent="TestAgent",
                expected_output="Output 2"
            )
        ]
        
        self.workflow.add_tasks(tasks)
        results = self.workflow.execute_all(example_task_executor)
        
        self.assertEqual(results["status"], "completed")
        self.assertEqual(results["total_tasks"], 2)
        self.assertEqual(results["completed_tasks"], 2)
        self.assertEqual(results["failed_tasks"], 0)
        self.assertIsNotNone(results["duration"])
    
    def test_get_task_by_id(self):
        """Test getting a task by its ID."""
        task = Task(
            id="test_task",
            name="Test Task",
            description="A test task",
            agent="TestAgent",
            expected_output="Test output"
        )
        
        self.workflow.add_task(task)
        retrieved_task = self.workflow.get_task_by_id("test_task")
        
        self.assertEqual(retrieved_task, task)
        
        # Test getting non-existent task
        retrieved_task = self.workflow.get_task_by_id("nonexistent_task")
        self.assertIsNone(retrieved_task)
    
    def test_get_tasks_by_status(self):
        """Test getting tasks by status."""
        tasks = [
            Task(
                id="task_1",
                name="Task 1",
                description="First task",
                agent="TestAgent",
                expected_output="Output 1"
            ),
            Task(
                id="task_2",
                name="Task 2",
                description="Second task",
                agent="TestAgent",
                expected_output="Output 2"
            ),
            Task(
                id="task_3",
                name="Task 3",
                description="Third task",
                agent="TestAgent",
                expected_output="Output 3"
            )
        ]
        
        self.workflow.add_tasks(tasks)
        
        # Execute first task
        self.workflow.execute_task(tasks[0], example_task_executor)
        
        # Fail second task
        def failing_executor(task):
            raise Exception("Task execution failed")
        
        self.workflow.execute_task(tasks[1], failing_executor)
        
        pending_tasks = self.workflow.get_pending_tasks()
        completed_tasks = self.workflow.get_completed_tasks()
        failed_tasks = self.workflow.get_failed_tasks()
        
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(pending_tasks[0].id, "task_3")
        
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0].id, "task_1")
        
        self.assertEqual(len(failed_tasks), 1)
        self.assertEqual(failed_tasks[0].id, "task_2")


class TestHierarchicalWorkflow(unittest.TestCase):
    """Test cases for HierarchicalWorkflow."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.workflow = HierarchicalWorkflow("Test Hierarchical Workflow", "TestManager")
    
    def test_initialization(self):
        """Test that the hierarchical workflow initializes correctly."""
        self.assertEqual(self.workflow.name, "Test Hierarchical Workflow")
        self.assertEqual(self.workflow.manager_agent, "TestManager")
        self.assertEqual(self.workflow.status, TaskStatus.PENDING)
        self.assertEqual(len(self.workflow.sub_workflows), 0)
    
    def test_add_sub_workflow(self):
        """Test adding a sub-workflow to the hierarchical workflow."""
        # Create a sequential workflow for the sub-workflow
        sequential_workflow = SequentialWorkflow("Sub Workflow")
        sub_workflow = SubWorkflow(
            id="sub_workflow_1",
            name="Sub Workflow 1",
            workflow=sequential_workflow
        )
        
        self.workflow.add_sub_workflow(sub_workflow)
        self.assertEqual(len(self.workflow.sub_workflows), 1)
        self.assertEqual(self.workflow.sub_workflows[0], sub_workflow)
    
    def test_can_execute_sub_workflow_no_dependencies(self):
        """Test checking if a sub-workflow with no dependencies can be executed."""
        sequential_workflow = SequentialWorkflow("Sub Workflow")
        sub_workflow = SubWorkflow(
            id="sub_workflow_1",
            name="Sub Workflow 1",
            workflow=sequential_workflow
        )
        
        self.assertTrue(self.workflow.can_execute_sub_workflow(sub_workflow))
    
    def test_can_execute_sub_workflow_with_dependencies(self):
        """Test checking if a sub-workflow with dependencies can be executed."""
        # Create sub-workflows with dependencies
        sequential_workflow1 = SequentialWorkflow("Sub Workflow 1")
        sequential_workflow2 = SequentialWorkflow("Sub Workflow 2")
        
        sub_workflow1 = SubWorkflow(
            id="sub_workflow_1",
            name="Sub Workflow 1",
            workflow=sequential_workflow1
        )
        
        sub_workflow2 = SubWorkflow(
            id="sub_workflow_2",
            name="Sub Workflow 2",
            workflow=sequential_workflow2,
            dependencies=["sub_workflow_1"]
        )
        
        self.workflow.add_sub_workflows([sub_workflow1, sub_workflow2])
        
        # sub_workflow2 cannot be executed because sub_workflow1 is not completed
        self.assertFalse(self.workflow.can_execute_sub_workflow(sub_workflow2))
        
        # Complete sub_workflow1
        sub_workflow1.status = TaskStatus.COMPLETED
        
        # Now sub_workflow2 can be executed
        self.assertTrue(self.workflow.can_execute_sub_workflow(sub_workflow2))
    
    def test_create_migration_phase_workflow(self):
        """Test creating a migration phase workflow."""
        tasks = [
            Task(
                id="task_1",
                name="Task 1",
                description="First task",
                agent="TestAgent",
                expected_output="Output 1"
            )
        ]
        
        sub_workflow = create_migration_phase_workflow("Test Phase", tasks, "TestManager")
        
        self.assertEqual(sub_workflow.id, "phase_test_phase")
        self.assertEqual(sub_workflow.name, "Test Phase")
        self.assertEqual(sub_workflow.manager_agent, "TestManager")
        self.assertIsInstance(sub_workflow.workflow, SequentialWorkflow)
        self.assertEqual(len(sub_workflow.workflow.tasks), 1)


if __name__ == "__main__":
    unittest.main()
