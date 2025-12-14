"""
HafizNaveed: CLI Handler and Application Orchestrator

This module implements the HafizNaveed main/orchestrator agent that handles
menu display, user input, and request routing to TodoActionAgent.
"""

from typing import Optional
from task_manager import TodoActionAgent


class HafizNaveed:
    """
    Main/Orchestrator agent responsible for CLI interaction.

    Responsibilities:
    - Display menu and handle user interaction
    - Capture and validate user input
    - Route requests to TodoActionAgent
    - Display results and error messages
    - Control application flow
    """

    def __init__(self) -> None:
        """Initialize HafizNaveed with TodoActionAgent instance."""
        self._agent = TodoActionAgent()

    def _display_menu(self) -> None:
        """Display the main menu with all options."""
        print("\n===== Todo Menu =====")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Exit")

    def _get_user_input(self, prompt: str = "Choose an option (1-6): ") -> str:
        """
        Get user input from command line.

        Args:
            prompt: Input prompt to display

        Returns:
            User input as string
        """
        return input(prompt).strip()

    def _handle_add_task(self) -> None:
        """Handle "Add Task" menu option."""
        try:
            title = self._get_user_input("Enter task title: ")
            task = self._agent.add_task(title)
            print(f" Task added with ID: {task.id}")
        except ValueError as e:
            print(f" Error: {e}")

    def _handle_list_tasks(self) -> None:
        """Handle "List Tasks" menu option."""
        tasks = self._agent.list_tasks()
        if not tasks:
            print("\nNo tasks yet. Add one with option 1!")
            return

        print()
        print("ID | Title              | Status")
        print("---|--------------------|-----------")
        for task in tasks:
            # Format title to fit in 18 chars
            title = task.title[:18].ljust(18)
            status = task.status
            print(f"{task.id:<2} | {title} | {status}")

    def _handle_update_task(self) -> None:
        """Handle "Update Task" menu option."""
        try:
            task_id_str = self._get_user_input("Enter task ID: ")
            try:
                task_id = int(task_id_str)
            except ValueError:
                print(" Please enter a valid task ID (number).")
                return

            new_title = self._get_user_input("Enter new title: ")
            if self._agent.update_task(task_id, new_title):
                print(" Task updated successfully")
            else:
                print(" Task not found. Please check the ID and try again.")
        except ValueError as e:
            print(f" Error: {e}")

    def _handle_delete_task(self) -> None:
        """Handle "Delete Task" menu option."""
        try:
            task_id_str = self._get_user_input("Enter task ID: ")
            try:
                task_id = int(task_id_str)
            except ValueError:
                print(" Please enter a valid task ID (number).")
                return

            if self._agent.delete_task(task_id):
                print(" Task deleted successfully")
            else:
                print(" Task not found. Please check the ID and try again.")
        except ValueError as e:
            print(f" Error: {e}")

    def _handle_mark_complete(self) -> None:
        """Handle "Mark Task Complete" menu option."""
        try:
            task_id_str = self._get_user_input("Enter task ID: ")
            try:
                task_id = int(task_id_str)
            except ValueError:
                print(" Please enter a valid task ID (number).")
                return

            if self._agent.mark_complete(task_id):
                print(" Task marked as completed")
            else:
                print(" Task not found. Please check the ID and try again.")
        except ValueError as e:
            print(f" Error: {e}")

    def run(self) -> None:
        """
        Main application loop.

        Continuously displays menu and processes user selections until Exit is chosen.
        """
        print("Welcome to Todo System!")

        while True:
            try:
                self._display_menu()
                choice = self._get_user_input()

                if choice == "1":
                    self._handle_add_task()
                elif choice == "2":
                    self._handle_list_tasks()
                elif choice == "3":
                    self._handle_update_task()
                elif choice == "4":
                    self._handle_delete_task()
                elif choice == "5":
                    self._handle_mark_complete()
                elif choice == "6":
                    print("\nThank you for using Todo System. Goodbye!")
                    break
                else:
                    print(" Invalid option. Please enter 1-6.")

            except KeyboardInterrupt:
                print("\n\nApplication interrupted. Goodbye!")
                break
            except Exception as e:
                print(f" An error occurred: {e}")
