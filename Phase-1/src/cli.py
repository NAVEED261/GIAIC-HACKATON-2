"""
HafizNaveed: CLI Handler and Application Orchestrator

This module implements the HafizNaveed main/orchestrator agent that handles
menu display, user input, and request routing to TodoActionAgent.
"""

from typing import Optional
from task_manager import TodoActionAgent
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box


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
        self.console = Console()

    def _display_menu(self) -> None:
        """Display the main menu with all options."""
        menu_text = Text()
        menu_text.append("\n")

        # Create a beautiful menu panel
        menu_content = """[bold cyan]1.[/bold cyan] [green]Add Task[/green]
[bold cyan]2.[/bold cyan] [blue]List Tasks[/blue]
[bold cyan]3.[/bold cyan] [yellow]Update Task[/yellow]
[bold cyan]4.[/bold cyan] [red]Delete Task[/red]
[bold cyan]5.[/bold cyan] [magenta]Mark Task Complete[/magenta]
[bold cyan]6.[/bold cyan] [white]Exit[/white]"""

        self.console.print(Panel(
            menu_content,
            title="[bold magenta]Todo Menu[/bold magenta]",
            border_style="bright_blue",
            box=box.DOUBLE_EDGE
        ))

    def _get_user_input(self, prompt: str = "Choose an option (1-6): ") -> str:
        """
        Get user input from command line.

        Args:
            prompt: Input prompt to display

        Returns:
            User input as string
        """
        return self.console.input(f"[bold yellow]{prompt}[/bold yellow]").strip()

    def _handle_add_task(self) -> None:
        """Handle "Add Task" menu option."""
        try:
            title = self._get_user_input("[green]Enter task title:[/green] ")
            task = self._agent.add_task(title)
            self.console.print(f"[bold green]Task added with ID: {task.id}[/bold green]")
        except ValueError as e:
            self.console.print(f"[bold red]Error: {e}[/bold red]")

    def _handle_list_tasks(self) -> None:
        """Handle "List Tasks" menu option."""
        tasks = self._agent.list_tasks()
        if not tasks:
            self.console.print("\n[yellow]No tasks yet. Add one with option 1![/yellow]")
            return

        # Create a beautiful table
        table = Table(
            title="[bold cyan]Your Tasks[/bold cyan]",
            box=box.ROUNDED,
            header_style="bold magenta",
            border_style="bright_blue"
        )

        table.add_column("ID", style="cyan", justify="center", width=6)
        table.add_column("Title", style="white", width=30)
        table.add_column("Status", justify="center", width=12)

        for task in tasks:
            # Color status based on completion
            if task.status == "Completed":
                status_style = "[bold green]completed[/bold green]"
            else:
                status_style = "[bold yellow]pending[/bold yellow]"

            table.add_row(str(task.id), task.title, status_style)

        self.console.print()
        self.console.print(table)

    def _handle_update_task(self) -> None:
        """Handle "Update Task" menu option."""
        try:
            task_id_str = self._get_user_input("[yellow]Enter task ID:[/yellow] ")
            try:
                task_id = int(task_id_str)
            except ValueError:
                self.console.print("[bold red]Please enter a valid task ID (number).[/bold red]")
                return

            new_title = self._get_user_input("[yellow]Enter new title:[/yellow] ")
            if self._agent.update_task(task_id, new_title):
                self.console.print("[bold green]Task updated successfully[/bold green]")
            else:
                self.console.print("[bold red]Task not found. Please check the ID and try again.[/bold red]")
        except ValueError as e:
            self.console.print(f"[bold red]Error: {e}[/bold red]")

    def _handle_delete_task(self) -> None:
        """Handle "Delete Task" menu option."""
        try:
            task_id_str = self._get_user_input("[red]Enter task ID:[/red] ")
            try:
                task_id = int(task_id_str)
            except ValueError:
                self.console.print("[bold red]Please enter a valid task ID (number).[/bold red]")
                return

            if self._agent.delete_task(task_id):
                self.console.print("[bold green]Task deleted successfully[/bold green]")
            else:
                self.console.print("[bold red]Task not found. Please check the ID and try again.[/bold red]")
        except ValueError as e:
            self.console.print(f"[bold red]Error: {e}[/bold red]")

    def _handle_mark_complete(self) -> None:
        """Handle "Mark Task Complete" menu option."""
        try:
            task_id_str = self._get_user_input("[magenta]Enter task ID:[/magenta] ")
            try:
                task_id = int(task_id_str)
            except ValueError:
                self.console.print("[bold red]Please enter a valid task ID (number).[/bold red]")
                return

            if self._agent.mark_complete(task_id):
                self.console.print("[bold green]Task marked as completed[/bold green]")
            else:
                self.console.print("[bold red]Task not found. Please check the ID and try again.[/bold red]")
        except ValueError as e:
            self.console.print(f"[bold red]Error: {e}[/bold red]")

    def run(self) -> None:
        """
        Main application loop.

        Continuously displays menu and processes user selections until Exit is chosen.
        """
        # Welcome banner
        welcome_text = Text()
        welcome_text.append("Welcome to ", style="bold white")
        welcome_text.append("Todo System", style="bold cyan")
        welcome_text.append("!", style="bold white")

        self.console.print(Panel(
            welcome_text,
            title="[bold green]GIAIC Hackathon-2[/bold green]",
            subtitle="[dim]By Hafiz Naveed Uddin[/dim]",
            border_style="bright_magenta",
            box=box.DOUBLE
        ))

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
                    self.console.print("\n[bold cyan]Thank you for using Todo System. Goodbye![/bold cyan]")
                    break
                else:
                    self.console.print("[bold red]Invalid option. Please enter 1-6.[/bold red]")

            except KeyboardInterrupt:
                self.console.print("\n\n[bold yellow]Application interrupted. Goodbye![/bold yellow]")
                break
            except Exception as e:
                self.console.print(f"[bold red]An error occurred: {e}[/bold red]")
