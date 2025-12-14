"""
Integration Tests for HafizNaveed CLI

Tests end-to-end CLI workflows including user input/output,
menu navigation, and error handling.
"""

import io
import sys
from unittest.mock import patch
import pytest
from src.cli import HafizNaveed
from src.task_manager import TodoActionAgent


class TestHafizNaveedBasics:
    """Test basic HafizNaveed functionality."""

    def test_init(self):
        """Test HafizNaveed initialization."""
        app = HafizNaveed()
        assert app._agent is not None

    def test_display_menu(self, capsys):
        """Test menu display."""
        app = HafizNaveed()
        app._display_menu()
        captured = capsys.readouterr()
        assert "===== Todo Menu =====" in captured.out
        assert "1. Add Task" in captured.out
        assert "6. Exit" in captured.out

    def test_get_user_input(self):
        """Test user input capture."""
        with patch("builtins.input", return_value="test input"):
            app = HafizNaveed()
            result = app._get_user_input("prompt: ")
            assert result == "test input"

    def test_get_user_input_strips_whitespace(self):
        """Test that user input is stripped."""
        with patch("builtins.input", return_value="  test  "):
            app = HafizNaveed()
            result = app._get_user_input()
            assert result == "test"


class TestAddTaskFlow:
    """Test add task workflow."""

    def test_add_task_success(self, capsys):
        """Test successful task addition."""
        with patch("builtins.input", side_effect=["Buy groceries"]):
            app = HafizNaveed()
            app._handle_add_task()
            captured = capsys.readouterr()
            assert " Task added with ID: 1" in captured.out

    def test_add_task_empty_title(self, capsys):
        """Test that empty title shows error."""
        with patch("builtins.input", side_effect=[""]):
            app = HafizNaveed()
            app._handle_add_task()
            captured = capsys.readouterr()
            assert " Error:" in captured.out
            assert "empty" in captured.out

    def test_add_multiple_tasks(self, capsys):
        """Test adding multiple tasks."""
        app = HafizNaveed()
        with patch("builtins.input", side_effect=["Task 1"]):
            app._handle_add_task()
        with patch("builtins.input", side_effect=["Task 2"]):
            app._handle_add_task()
        captured = capsys.readouterr()
        assert "ID: 1" in captured.out
        assert "ID: 2" in captured.out


class TestListTasksFlow:
    """Test list tasks workflow."""

    def test_list_tasks_empty(self, capsys):
        """Test listing when no tasks exist."""
        app = HafizNaveed()
        app._handle_list_tasks()
        captured = capsys.readouterr()
        assert "No tasks yet" in captured.out

    def test_list_tasks_with_data(self, capsys):
        """Test listing tasks with data."""
        app = HafizNaveed()
        app._agent.add_task("Buy groceries")
        app._agent.add_task("Do homework")
        app._handle_list_tasks()
        captured = capsys.readouterr()
        assert "Buy groceries" in captured.out
        assert "Do homework" in captured.out
        assert "Pending" in captured.out

    def test_list_tasks_with_completed(self, capsys):
        """Test listing with completed tasks."""
        app = HafizNaveed()
        app._agent.add_task("Task 1")
        app._agent.add_task("Task 2")
        app._agent.mark_complete(1)
        app._handle_list_tasks()
        captured = capsys.readouterr()
        assert "Completed" in captured.out
        assert "Pending" in captured.out

    def test_list_tasks_formatting(self, capsys):
        """Test that list format is correct."""
        app = HafizNaveed()
        app._agent.add_task("Test Task")
        app._handle_list_tasks()
        captured = capsys.readouterr()
        assert "ID" in captured.out
        assert "Title" in captured.out
        assert "Status" in captured.out


class TestUpdateTaskFlow:
    """Test update task workflow."""

    def test_update_task_success(self, capsys):
        """Test successful task update."""
        app = HafizNaveed()
        app._agent.add_task("Old Title")
        with patch("builtins.input", side_effect=["1", "New Title"]):
            app._handle_update_task()
        captured = capsys.readouterr()
        assert " Task updated successfully" in captured.out

    def test_update_task_invalid_id_format(self, capsys):
        """Test invalid ID format."""
        app = HafizNaveed()
        with patch("builtins.input", side_effect=["abc", "New Title"]):
            app._handle_update_task()
        captured = capsys.readouterr()
        assert "valid task ID" in captured.out

    def test_update_task_not_found(self, capsys):
        """Test updating non-existent task."""
        app = HafizNaveed()
        app._agent.add_task("Task")
        with patch("builtins.input", side_effect=["999", "New Title"]):
            app._handle_update_task()
        captured = capsys.readouterr()
        assert "Task not found" in captured.out

    def test_update_task_empty_title(self, capsys):
        """Test updating with empty title."""
        app = HafizNaveed()
        app._agent.add_task("Task")
        with patch("builtins.input", side_effect=["1", ""]):
            app._handle_update_task()
        captured = capsys.readouterr()
        assert "Error:" in captured.out


class TestDeleteTaskFlow:
    """Test delete task workflow."""

    def test_delete_task_success(self, capsys):
        """Test successful task deletion."""
        app = HafizNaveed()
        app._agent.add_task("Task to Delete")
        with patch("builtins.input", side_effect=["1"]):
            app._handle_delete_task()
        captured = capsys.readouterr()
        assert " Task deleted successfully" in captured.out

    def test_delete_task_invalid_id_format(self, capsys):
        """Test invalid ID format."""
        app = HafizNaveed()
        with patch("builtins.input", side_effect=["abc"]):
            app._handle_delete_task()
        captured = capsys.readouterr()
        assert "valid task ID" in captured.out

    def test_delete_task_not_found(self, capsys):
        """Test deleting non-existent task."""
        app = HafizNaveed()
        app._agent.add_task("Task")
        with patch("builtins.input", side_effect=["999"]):
            app._handle_delete_task()
        captured = capsys.readouterr()
        assert "Task not found" in captured.out


class TestMarkCompleteFlow:
    """Test mark complete workflow."""

    def test_mark_complete_success(self, capsys):
        """Test successful task completion."""
        app = HafizNaveed()
        app._agent.add_task("Task to Complete")
        with patch("builtins.input", side_effect=["1"]):
            app._handle_mark_complete()
        captured = capsys.readouterr()
        assert " Task marked as completed" in captured.out

    def test_mark_complete_invalid_id_format(self, capsys):
        """Test invalid ID format."""
        app = HafizNaveed()
        with patch("builtins.input", side_effect=["abc"]):
            app._handle_mark_complete()
        captured = capsys.readouterr()
        assert "valid task ID" in captured.out

    def test_mark_complete_not_found(self, capsys):
        """Test completing non-existent task."""
        app = HafizNaveed()
        app._agent.add_task("Task")
        with patch("builtins.input", side_effect=["999"]):
            app._handle_mark_complete()
        captured = capsys.readouterr()
        assert "Task not found" in captured.out


class TestCompleteWorkflows:
    """Test complete end-to-end workflows."""

    def test_full_workflow(self, capsys):
        """Test complete workflow: add, list, update, complete, delete."""
        app = HafizNaveed()

        # Add task
        with patch("builtins.input", side_effect=["Buy groceries"]):
            app._handle_add_task()

        # List tasks
        app._handle_list_tasks()

        # Update task
        with patch("builtins.input", side_effect=["1", "Buy organic groceries"]):
            app._handle_update_task()

        # Mark complete
        with patch("builtins.input", side_effect=["1"]):
            app._handle_mark_complete()

        # Delete task
        with patch("builtins.input", side_effect=["1"]):
            app._handle_delete_task()

        captured = capsys.readouterr()
        assert "Task added with ID: 1" in captured.out
        assert "Task updated successfully" in captured.out
        assert "Task marked as completed" in captured.out
        assert "Task deleted successfully" in captured.out

    def test_multiple_tasks_workflow(self, capsys):
        """Test workflow with multiple tasks."""
        app = HafizNaveed()

        # Add multiple tasks
        with patch("builtins.input", side_effect=["Task 1"]):
            app._handle_add_task()
        with patch("builtins.input", side_effect=["Task 2"]):
            app._handle_add_task()
        with patch("builtins.input", side_effect=["Task 3"]):
            app._handle_add_task()

        # List all
        app._handle_list_tasks()

        # Mark first complete
        with patch("builtins.input", side_effect=["1"]):
            app._handle_mark_complete()

        # Update second
        with patch("builtins.input", side_effect=["2", "Updated Task 2"]):
            app._handle_update_task()

        # Delete third
        with patch("builtins.input", side_effect=["3"]):
            app._handle_delete_task()

        # List after operations
        app._handle_list_tasks()

        captured = capsys.readouterr()
        assert "Task 1" in captured.out
        assert "Task 2" in captured.out
        assert "Task 3" in captured.out
        assert "Completed" in captured.out

    def test_error_recovery_workflow(self, capsys):
        """Test that application recovers from errors."""
        app = HafizNaveed()

        # Try invalid input
        with patch("builtins.input", side_effect=[""]):
            app._handle_add_task()

        # Still able to add task after error
        with patch("builtins.input", side_effect=["Valid Task"]):
            app._handle_add_task()

        captured = capsys.readouterr()
        assert "Error:" in captured.out
        assert "Task added with ID: 1" in captured.out


class TestApplicationLoop:
    """Test application main loop."""

    def test_menu_display_on_each_iteration(self, capsys):
        """Test that menu displays on each iteration."""
        with patch("builtins.input", side_effect=["1", "Test", "6"]):
            app = HafizNaveed()
            app.run()
        captured = capsys.readouterr()
        # Menu should display at least twice (before option 1, before option 6)
        menu_count = captured.out.count("===== Todo Menu =====")
        assert menu_count >= 2

    def test_exit_option(self, capsys):
        """Test that exit option works."""
        with patch("builtins.input", side_effect=["6"]):
            app = HafizNaveed()
            app.run()
        captured = capsys.readouterr()
        assert "Goodbye!" in captured.out

    def test_invalid_menu_option(self, capsys):
        """Test invalid menu option handling."""
        with patch("builtins.input", side_effect=["9", "6"]):
            app = HafizNaveed()
            app.run()
        captured = capsys.readouterr()
        assert "Invalid option" in captured.out
        assert "Goodbye!" in captured.out
