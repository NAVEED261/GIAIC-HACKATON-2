"""
Unit Tests for TodoActionAgent

Tests all task operations including creation, retrieval, updating,
deletion, and completion marking.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from task_manager import TodoActionAgent
from models import Task


class TestTodoActionAgentBasics:
    """Test basic TodoActionAgent initialization and task creation."""

    def test_init(self):
        """Test TodoActionAgent initialization."""
        agent = TodoActionAgent()
        assert agent.list_tasks() == []

    def test_add_task_success(self):
        """Test successful task addition."""
        agent = TodoActionAgent()
        task = agent.add_task("Buy groceries")
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.status == "Pending"

    def test_add_task_sequential_ids(self):
        """Test that IDs are sequential."""
        agent = TodoActionAgent()
        task1 = agent.add_task("Task 1")
        task2 = agent.add_task("Task 2")
        task3 = agent.add_task("Task 3")
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_empty_title(self):
        """Test that empty title raises ValueError."""
        agent = TodoActionAgent()
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            agent.add_task("")

    def test_add_task_whitespace_title(self):
        """Test that whitespace-only title raises ValueError."""
        agent = TodoActionAgent()
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            agent.add_task("   ")

    def test_add_task_strips_whitespace(self):
        """Test that leading/trailing whitespace is stripped."""
        agent = TodoActionAgent()
        task = agent.add_task("  Buy milk  ")
        assert task.title == "Buy milk"


class TestListTasks:
    """Test list_tasks operation."""

    def test_list_tasks_empty(self):
        """Test listing when no tasks exist."""
        agent = TodoActionAgent()
        assert agent.list_tasks() == []

    def test_list_tasks_multiple(self):
        """Test listing multiple tasks."""
        agent = TodoActionAgent()
        agent.add_task("Task 1")
        agent.add_task("Task 2")
        agent.add_task("Task 3")
        tasks = agent.list_tasks()
        assert len(tasks) == 3
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"
        assert tasks[2].title == "Task 3"

    def test_list_tasks_returns_copy(self):
        """Test that list_tasks returns a copy, not the original."""
        agent = TodoActionAgent()
        agent.add_task("Original Task")
        tasks = agent.list_tasks()
        tasks.clear()
        # Original should still have the task
        assert len(agent.list_tasks()) == 1


class TestGetTask:
    """Test get_task operation."""

    def test_get_task_found(self):
        """Test retrieving an existing task."""
        agent = TodoActionAgent()
        agent.add_task("Task 1")
        task = agent.get_task(1)
        assert task is not None
        assert task.title == "Task 1"

    def test_get_task_not_found(self):
        """Test retrieving a non-existent task."""
        agent = TodoActionAgent()
        agent.add_task("Task 1")
        task = agent.get_task(999)
        assert task is None


class TestUpdateTask:
    """Test update_task operation."""

    def test_update_task_success(self):
        """Test successful task title update."""
        agent = TodoActionAgent()
        agent.add_task("Old Title")
        success = agent.update_task(1, "New Title")
        assert success is True
        task = agent.get_task(1)
        assert task.title == "New Title"

    def test_update_task_invalid_id(self):
        """Test updating non-existent task returns False."""
        agent = TodoActionAgent()
        agent.add_task("Task")
        success = agent.update_task(999, "New Title")
        assert success is False

    def test_update_task_empty_title(self):
        """Test that empty new title raises ValueError."""
        agent = TodoActionAgent()
        agent.add_task("Task")
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            agent.update_task(1, "")

    def test_update_task_whitespace_title(self):
        """Test that whitespace-only new title raises ValueError."""
        agent = TodoActionAgent()
        agent.add_task("Task")
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            agent.update_task(1, "   ")

    def test_update_task_multiple(self):
        """Test updating multiple tasks."""
        agent = TodoActionAgent()
        agent.add_task("Task 1")
        agent.add_task("Task 2")
        agent.update_task(1, "Updated 1")
        agent.update_task(2, "Updated 2")
        assert agent.get_task(1).title == "Updated 1"
        assert agent.get_task(2).title == "Updated 2"


class TestDeleteTask:
    """Test delete_task operation."""

    def test_delete_task_success(self):
        """Test successful task deletion."""
        agent = TodoActionAgent()
        agent.add_task("Task to Delete")
        success = agent.delete_task(1)
        assert success is True
        assert agent.list_tasks() == []

    def test_delete_task_invalid_id(self):
        """Test deleting non-existent task returns False."""
        agent = TodoActionAgent()
        agent.add_task("Task")
        success = agent.delete_task(999)
        assert success is False
        assert len(agent.list_tasks()) == 1

    def test_delete_task_list_updated(self):
        """Test that list is updated after deletion."""
        agent = TodoActionAgent()
        agent.add_task("Task 1")
        agent.add_task("Task 2")
        agent.add_task("Task 3")
        agent.delete_task(2)
        tasks = agent.list_tasks()
        assert len(tasks) == 2
        assert tasks[0].id == 1
        assert tasks[1].id == 3

    def test_delete_task_multiple(self):
        """Test deleting multiple tasks."""
        agent = TodoActionAgent()
        agent.add_task("Task 1")
        agent.add_task("Task 2")
        agent.add_task("Task 3")
        agent.delete_task(1)
        agent.delete_task(3)
        tasks = agent.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 2


class TestMarkComplete:
    """Test mark_complete operation."""

    def test_mark_complete_success(self):
        """Test successfully marking task as complete."""
        agent = TodoActionAgent()
        agent.add_task("Task to Complete")
        success = agent.mark_complete(1)
        assert success is True
        task = agent.get_task(1)
        assert task.status == "Completed"

    def test_mark_complete_invalid_id(self):
        """Test marking non-existent task returns False."""
        agent = TodoActionAgent()
        agent.add_task("Task")
        success = agent.mark_complete(999)
        assert success is False
        assert agent.get_task(1).status == "Pending"

    def test_mark_complete_idempotent(self):
        """Test that marking complete twice is safe."""
        agent = TodoActionAgent()
        agent.add_task("Task")
        agent.mark_complete(1)
        agent.mark_complete(1)
        task = agent.get_task(1)
        assert task.status == "Completed"

    def test_mark_complete_multiple(self):
        """Test marking multiple tasks complete."""
        agent = TodoActionAgent()
        agent.add_task("Task 1")
        agent.add_task("Task 2")
        agent.add_task("Task 3")
        agent.mark_complete(1)
        agent.mark_complete(3)
        tasks = agent.list_tasks()
        assert tasks[0].status == "Completed"
        assert tasks[1].status == "Pending"
        assert tasks[2].status == "Completed"


class TestComplexScenarios:
    """Test complex multi-operation scenarios."""

    def test_full_workflow(self):
        """Test complete workflow: add, list, update, complete, delete."""
        agent = TodoActionAgent()

        # Add tasks
        agent.add_task("Buy groceries")
        agent.add_task("Do homework")
        agent.add_task("Call mom")
        assert len(agent.list_tasks()) == 3

        # Update a task
        agent.update_task(2, "Complete homework")
        assert agent.get_task(2).title == "Complete homework"

        # Mark complete
        agent.mark_complete(1)
        assert agent.get_task(1).status == "Completed"

        # Delete a task
        agent.delete_task(3)
        assert len(agent.list_tasks()) == 2

        # Verify final state
        tasks = agent.list_tasks()
        assert tasks[0].status == "Completed"
        assert tasks[1].status == "Pending"

    def test_multiple_agents(self):
        """Test that multiple agents maintain separate state."""
        agent1 = TodoActionAgent()
        agent2 = TodoActionAgent()

        agent1.add_task("Agent 1 Task")
        agent2.add_task("Agent 2 Task")

        assert len(agent1.list_tasks()) == 1
        assert len(agent2.list_tasks()) == 1
        assert agent1.get_task(1).title == "Agent 1 Task"
        assert agent2.get_task(1).title == "Agent 2 Task"
