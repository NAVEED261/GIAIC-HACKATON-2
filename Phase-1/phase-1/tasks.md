# Phase-1 Task Breakdown: Console-Based Todo System

**Created**: 2025-12-14
**Feature Branch**: `feature/phase-1-console-todo`
**Plan Reference**: `hafiz-naveed/phase-1/plan.md`

---

## Overview

This document breaks down the Phase-1 implementation into specific, testable tasks. Each task is small enough to be completed and verified independently.

---

## Task Group 1: Project Setup & Structure

### Task 1.1: Create Project Directory Structure

**Description**: Set up the complete folder hierarchy for Phase-1.

**Steps**:
1. Create directory: `src/`
2. Create directory: `tests/`
3. Create directory: `docs/`
4. Create empty files:
   - `src/__init__.py`
   - `src/main.py` (placeholder)
   - `src/cli.py` (placeholder)
   - `src/task_manager.py` (placeholder)
   - `src/models.py` (placeholder)
   - `tests/__init__.py`
   - `tests/test_task_manager.py` (placeholder)
   - `tests/test_cli.py` (placeholder)
5. Create root files:
   - `requirements.txt` (empty or with standard testing frameworks like pytest)
   - `.gitignore` (Python standard patterns)

**Verification**:
- [ ] All directories exist: `src/`, `tests/`, `docs/`
- [ ] All placeholder files exist
- [ ] Run `ls -la` or file explorer to confirm structure
- [ ] `git status` shows all new files ready to commit

**Acceptance**: Directory structure complete and ready for code implementation.

---

### Task 1.2: Create README.md for Phase-1

**Description**: Write the top-level README explaining Phase-1 scope and SDD workflow.

**File**: `hafiz-naveed/README.md`

**Content Requirements**:
- Project title: "Hackathon-2: AI-Native Todo System"
- Use the APP TOPIC verbatim
- Explain Phase-1 scope: Console CLI todo app, in-memory, Python
- Mention the five phases briefly
- Explain SDD workflow: Spec → Plan → Tasks → Implementation → Verification
- Explain agent architecture: HafizNaveed (main) + TodoActionAgent (sub)
- Include quick start command: `python src/main.py`
- Link to specification, plan, and documentation
- Alignment with project constitution

**Verification**:
- [ ] README.md exists at `hafiz-naveed/README.md`
- [ ] Contains all required sections
- [ ] APP TOPIC used verbatim
- [ ] Clear explanation of Phase-1 scope only (no mention of Phases 2-5 functionality)
- [ ] SDD workflow explained
- [ ] Agent architecture mentioned

**Acceptance**: Clear, professional README guides users and developers.

---

## Task Group 2: Task Model & Data Structure

### Task 2.1: Implement Task Model in models.py

**Description**: Create the Task data structure with validation.

**File**: `src/models.py`

**Content Requirements**:
- Define Task class or NamedTuple with attributes:
  - `id: int` (unique identifier)
  - `title: str` (required, non-empty)
  - `status: str` (either "Pending" or "Completed", default "Pending")
- Include validation method or __init__ that:
  - Rejects empty titles (raise ValueError if empty or whitespace-only)
  - Validates status is one of the allowed values
- Include method: `to_dict()` that returns dict representation for display
- Include method: `update_title(new_title: str)` that updates title with validation
- Include method: `mark_complete()` that sets status to "Completed"
- Add docstring explaining each attribute

**Code Quality**:
- Professional, readable code
- Clear error messages in exceptions
- Type hints for all parameters and return values

**Verification**:
- [ ] models.py exists and can be imported
- [ ] Task class/NamedTuple is defined
- [ ] All required attributes present
- [ ] Validation prevents empty titles (test with empty string, spaces-only)
- [ ] Status is validated (test with invalid status)
- [ ] to_dict() returns correct dictionary
- [ ] update_title() works correctly
- [ ] mark_complete() sets status to "Completed"

**Acceptance**: Task model fully functional and ready for TaskManager.

---

## Task Group 3: TodoActionAgent (Task Management Logic)

### Task 3.1: Implement TodoActionAgent in task_manager.py

**Description**: Create the TodoActionAgent class that manages all task operations.

**File**: `src/task_manager.py`

**Content Requirements**:
- Define TodoActionAgent class with:
  - Constructor `__init__()` that initializes empty task list and ID counter
  - Private variable: `_tasks: List[Task]` to store tasks
  - Private variable: `_next_id: int = 1` for auto-incrementing IDs
- Implement method: `add_task(title: str) -> Task`
  - Validate title (non-empty)
  - Create Task with next available ID
  - Add to task list
  - Return the created Task
  - Raise ValueError if title is empty
- Implement method: `list_tasks() -> List[Task]`
  - Return copy of task list in order
- Implement method: `get_task(task_id: int) -> Task | None`
  - Return task matching ID or None if not found
- Implement method: `update_task(task_id: int, new_title: str) -> bool`
  - Find task by ID
  - Update title if task found
  - Return True if successful, False if task not found
  - Raise ValueError if new_title is empty
- Implement method: `delete_task(task_id: int) -> bool`
  - Find task by ID
  - Remove from list if found
  - Return True if successful, False if task not found
- Implement method: `mark_complete(task_id: int) -> bool`
  - Find task by ID
  - Call task.mark_complete() if found
  - Return True if successful, False if task not found

**Code Quality**:
- Professional, readable code with clear logic
- Type hints on all methods
- Comprehensive docstrings
- No external dependencies

**Verification**:
- [ ] task_manager.py exists and can be imported
- [ ] TodoActionAgent class is defined
- [ ] add_task() creates tasks with sequential IDs starting at 1
- [ ] add_task() rejects empty titles
- [ ] list_tasks() returns all tasks in order
- [ ] get_task() finds tasks by ID
- [ ] update_task() modifies task titles correctly
- [ ] update_task() returns False for invalid IDs
- [ ] delete_task() removes tasks from list
- [ ] delete_task() returns False for invalid IDs
- [ ] mark_complete() changes status to "Completed"
- [ ] mark_complete() returns False for invalid IDs

**Acceptance**: TodoActionAgent fully implements all task operations.

---

### Task 3.2: Write Unit Tests for TodoActionAgent

**Description**: Create comprehensive unit tests for task operations.

**File**: `tests/test_task_manager.py`

**Test Cases Required**:
1. **test_add_task_success**: Create task, verify ID, title, default status
2. **test_add_task_sequential_ids**: Add multiple tasks, verify IDs are sequential
3. **test_add_task_empty_title**: Verify ValueError raised for empty title
4. **test_add_task_whitespace_title**: Verify ValueError raised for whitespace-only title
5. **test_list_tasks_empty**: Verify empty list when no tasks
6. **test_list_tasks_multiple**: Add tasks, verify list returns all in order
7. **test_get_task_found**: Get existing task by ID
8. **test_get_task_not_found**: Get non-existent task returns None
9. **test_update_task_success**: Update task title, verify change
10. **test_update_task_invalid_id**: Update non-existent task returns False
11. **test_update_task_empty_title**: Update with empty title raises ValueError
12. **test_delete_task_success**: Delete task, verify removal
13. **test_delete_task_invalid_id**: Delete non-existent task returns False
14. **test_delete_task_list_updated**: Delete task, verify list updated
15. **test_mark_complete_success**: Mark task complete, verify status
16. **test_mark_complete_invalid_id**: Mark non-existent task returns False
17. **test_mark_complete_idempotent**: Mark complete twice, verify still completed

**Test Framework**: pytest

**Code Quality**:
- Each test is small and focused
- Clear test names describing what is tested
- Proper assertions with helpful messages
- Setup/teardown as needed

**Verification**:
- [ ] test_task_manager.py exists
- [ ] All test cases listed above are implemented
- [ ] All tests pass: `pytest tests/test_task_manager.py -v`
- [ ] Test coverage includes success and error paths
- [ ] No external API calls in tests

**Acceptance**: Unit tests provide confidence in task operations.

---

## Task Group 4: HafizNaveed Agent (CLI Handler)

### Task 4.1: Implement HafizNaveed CLI Handler in cli.py

**Description**: Create the HafizNaveed agent that orchestrates CLI flow.

**File**: `src/cli.py`

**Content Requirements**:
- Define HafizNaveed class with:
  - Constructor `__init__()` that creates TodoActionAgent instance
  - Private variable: `_agent: TodoActionAgent`
  - Method: `_display_menu()` that prints formatted menu with options:
    ```
    ===== Todo Menu =====
    1. Add Task
    2. List Tasks
    3. Update Task
    4. Delete Task
    5. Mark Task Complete
    6. Exit
    Choose an option (1-6):
    ```
  - Method: `_get_user_input() -> str` that reads user input and returns it
  - Method: `_handle_add_task()` that:
    - Prompts for task title
    - Calls agent.add_task()
    - Displays success message with task ID
    - Catches ValueError and displays error
  - Method: `_handle_list_tasks()` that:
    - Gets task list from agent
    - Displays all tasks with ID, title, status in table format
    - Shows "No tasks" message if empty
  - Method: `_handle_update_task()` that:
    - Prompts for task ID
    - Validates ID is numeric
    - Prompts for new title
    - Calls agent.update_task()
    - Displays success or "Task not found" message
  - Method: `_handle_delete_task()` that:
    - Prompts for task ID
    - Validates ID is numeric
    - Calls agent.delete_task()
    - Displays success or "Task not found" message
  - Method: `_handle_mark_complete()` that:
    - Prompts for task ID
    - Validates ID is numeric
    - Calls agent.mark_complete()
    - Displays success or "Task not found" message
  - Method: `run()` that:
    - Main application loop
    - Display menu
    - Get user choice
    - Route to appropriate handler based on choice
    - Catch any unhandled exceptions and display error
    - Continue until user selects "Exit" (option 6)

**Error Handling**:
- Invalid menu input: "Invalid option. Please enter 1-6."
- Invalid task ID format: "Please enter a valid task ID (number)."
- Invalid ID not found: "Task not found. Please check the ID and try again."
- Empty title: "Task title cannot be empty."
- Any other exception: "An error occurred. Please try again."

**User Experience**:
- Clear, friendly messages
- Consistent menu format
- Task display formatted readably (tabular if possible)
- Confirmation messages after each action

**Code Quality**:
- Professional, readable code
- Clear method names
- Comprehensive docstrings
- No hardcoded magic strings (use constants for menu options)

**Verification**:
- [ ] cli.py exists and can be imported
- [ ] HafizNaveed class is defined
- [ ] Menu displays correctly with all 6 options
- [ ] User input is captured and processed
- [ ] add_task() handler works and displays confirmation
- [ ] list_tasks() handler displays all tasks clearly
- [ ] update_task() handler updates and confirms
- [ ] delete_task() handler removes and confirms
- [ ] mark_complete() handler changes status and confirms
- [ ] Invalid menu input is rejected with error message
- [ ] Invalid task IDs are rejected with friendly error
- [ ] Exit option (6) terminates the application
- [ ] Application loops until Exit is selected

**Acceptance**: HafizNaveed agent fully orchestrates CLI interactions.

---

### Task 4.2: Write Integration Tests for CLI

**Description**: Create tests that verify end-to-end CLI workflows.

**File**: `tests/test_cli.py`

**Test Cases Required**:
1. **test_menu_display**: Verify menu displays all options
2. **test_add_task_flow**: Simulate adding task via CLI, verify result
3. **test_add_empty_task_flow**: Attempt to add empty task, verify error
4. **test_list_tasks_flow**: Add task and list, verify display
5. **test_list_empty_tasks**: List when no tasks, verify message
6. **test_update_task_flow**: Add task, update title, verify change
7. **test_update_invalid_id**: Update non-existent task, verify error
8. **test_delete_task_flow**: Add task, delete, verify removal
9. **test_delete_invalid_id**: Delete non-existent task, verify error
10. **test_mark_complete_flow**: Add task, mark complete, verify status
11. **test_mark_complete_invalid_id**: Mark non-existent task, verify error
12. **test_invalid_menu_option**: Enter invalid option, verify error and menu redisplay
13. **test_non_numeric_task_id**: Enter non-numeric ID, verify error
14. **test_full_workflow**: Simulate complete user session with multiple operations

**Test Framework**: pytest with mocking for user input (mock input, capture output)

**Code Quality**:
- Use unittest.mock or pytest fixtures for input/output simulation
- Each test is focused on one workflow
- Clear test names and docstrings
- Proper assertions on output

**Verification**:
- [ ] test_cli.py exists
- [ ] All test cases listed above are implemented
- [ ] All tests pass: `pytest tests/test_cli.py -v`
- [ ] Integration tests verify end-to-end workflows
- [ ] Mock input/output used appropriately

**Acceptance**: Integration tests verify CLI workflows work correctly.

---

## Task Group 5: Application Entry Point

### Task 5.1: Implement Application Entry Point in main.py

**Description**: Create the application startup script.

**File**: `src/main.py`

**Content Requirements**:
- Import HafizNaveed from cli module
- Define main() function that:
  - Creates HafizNaveed instance
  - Calls run() method
  - Handles any top-level exceptions
- Include `if __name__ == "__main__":` block that calls main()
- Add module-level docstring explaining the application:
  ```
  """
  Hackathon-2 Phase-1: Console-Based Todo System

  An AI-native, specification-driven Task Management System
  designed to manage personal and professional work across
  scalable cloud architectures.

  This module serves as the application entry point for the
  Phase-1 console CLI implementation.
  """
  ```

**Verification**:
- [ ] main.py exists at `src/main.py`
- [ ] File can be executed: `python src/main.py`
- [ ] Application starts and displays menu
- [ ] Application can be exited cleanly
- [ ] No import errors

**Acceptance**: Application can be started with `python src/main.py`.

---

## Task Group 6: Documentation

### Task 6.1: Create SETUP.md

**Description**: Write installation and setup guide.

**File**: `docs/SETUP.md`

**Content Requirements**:
- Title: "Phase-1 Setup Guide"
- Prerequisites section:
  - Python 3.8 or higher
  - pip (Python package manager)
  - git (for version control)
- Installation steps:
  - Clone repository (provide command)
  - Navigate to project directory
  - Install dependencies: `pip install -r requirements.txt`
- Running the application:
  - Command: `python src/main.py`
  - What to expect on startup (menu display)
- Troubleshooting:
  - Python not found (how to verify installation)
  - Module not found errors (how to check PYTHONPATH)
  - Permission issues (if applicable)
- Next steps (link to USAGE.md)

**Verification**:
- [ ] SETUP.md exists at `docs/SETUP.md`
- [ ] Contains all required sections
- [ ] Instructions are clear and complete
- [ ] Troubleshooting helps with common issues

**Acceptance**: Users can set up and run the application following the guide.

---

### Task 6.2: Create USAGE.md

**Description**: Write user guide for operating the application.

**File**: `docs/USAGE.md`

**Content Requirements**:
- Title: "Phase-1 Usage Guide"
- Quick start section:
  - How to run: `python src/main.py`
  - Menu will display
- Menu options reference:
  - Option 1 (Add Task): Description, example, what happens next
  - Option 2 (List Tasks): Description, example output, column explanations
  - Option 3 (Update Task): Description, steps, example
  - Option 4 (Delete Task): Description, steps, example
  - Option 5 (Mark Complete): Description, steps, example
  - Option 6 (Exit): Description
- Common workflows:
  - "Create and complete a task": Step-by-step example
  - "Update multiple tasks": Step-by-step example
  - "View and organize tasks": Step-by-step example
- Error messages and solutions:
  - "Invalid option" - what it means and how to fix
  - "Task not found" - why it happens and how to verify ID
  - "Task title cannot be empty" - explanation and retry
- Tips and best practices:
  - Task titles should be descriptive
  - Use task completion to track progress
  - Note that data is in-memory (lost on exit)

**Verification**:
- [ ] USAGE.md exists at `docs/USAGE.md`
- [ ] Contains all required sections
- [ ] Examples are clear and practical
- [ ] Error messages explained
- [ ] Professional and user-friendly tone

**Acceptance**: Users understand how to use the application effectively.

---

## Task Group 7: Verification & Testing

### Task 7.1: Run All Unit Tests

**Description**: Execute all unit tests and verify passage.

**Steps**:
1. Ensure tests directory exists: `tests/`
2. Ensure test files exist: `test_task_manager.py`, `test_cli.py`
3. Run command: `pytest tests/test_task_manager.py -v`
4. Verify all tests pass (green check marks)
5. Run command: `pytest tests/test_cli.py -v`
6. Verify all tests pass

**Verification**:
- [ ] `pytest tests/test_task_manager.py -v` shows all tests PASSED
- [ ] `pytest tests/test_cli.py -v` shows all tests PASSED
- [ ] No failed tests or errors
- [ ] Test output is clean and readable

**Acceptance**: All unit and integration tests pass.

---

### Task 7.2: Manual End-to-End Testing

**Description**: Perform manual verification of all features.

**Test Scenario 1: Add and List Tasks**
- [ ] Start application: `python src/main.py`
- [ ] Select option 1 (Add Task)
- [ ] Enter title: "Buy groceries"
- [ ] Verify confirmation message with task ID
- [ ] Select option 2 (List Tasks)
- [ ] Verify task appears with ID, title, and "Pending" status

**Test Scenario 2: Update Task**
- [ ] From list, note a task ID
- [ ] Select option 3 (Update Task)
- [ ] Enter task ID
- [ ] Enter new title: "Buy organic groceries"
- [ ] Select option 2 (List Tasks)
- [ ] Verify title is updated

**Test Scenario 3: Mark Task Complete**
- [ ] Note a task ID from the list
- [ ] Select option 5 (Mark Task Complete)
- [ ] Enter task ID
- [ ] Verify confirmation message
- [ ] Select option 2 (List Tasks)
- [ ] Verify task status is now "Completed"

**Test Scenario 4: Delete Task**
- [ ] Note a task ID
- [ ] Select option 4 (Delete Task)
- [ ] Enter task ID
- [ ] Verify confirmation message
- [ ] Select option 2 (List Tasks)
- [ ] Verify task no longer appears

**Test Scenario 5: Error Handling**
- [ ] Select option 1 (Add Task)
- [ ] Press Enter without entering title (empty input)
- [ ] Verify error message: "Task title cannot be empty"
- [ ] Select option 3 (Update Task)
- [ ] Enter invalid ID (e.g., 999)
- [ ] Verify error message: "Task not found"
- [ ] Select invalid menu option (e.g., 9)
- [ ] Verify error message: "Invalid option"

**Test Scenario 6: Exit Application**
- [ ] Select option 6 (Exit)
- [ ] Verify application terminates cleanly
- [ ] Verify no error messages on exit

**Verification Checklist**:
- [ ] All five task operations work (add, list, update, delete, complete)
- [ ] Task IDs are unique and sequential
- [ ] Status displays correctly ("Pending" or "Completed")
- [ ] Error messages are friendly and helpful
- [ ] Menu displays correctly after each operation
- [ ] Application exits cleanly
- [ ] No crashes or unhandled exceptions
- [ ] All success criteria from specification are met

**Acceptance**: Application meets all specification requirements and success criteria.

---

### Task 7.3: Specification Alignment Review

**Description**: Verify implementation meets all specification requirements.

**Checklist**:
- [ ] FR-001: Menu-driven CLI with all options present
- [ ] FR-002: Add task creates with unique ID and default "Pending" status
- [ ] FR-003: List shows ID, title, status for all tasks
- [ ] FR-004: Update task title by ID works correctly
- [ ] FR-005: Mark complete changes status to "Completed"
- [ ] FR-006: Delete removes task from list
- [ ] FR-007: Invalid inputs produce friendly error messages
- [ ] FR-008: In-memory state maintained during session
- [ ] FR-009: Application loops until Exit selected
- [ ] FR-010: Status defaults to "Pending"
- [ ] SC-001: Task addition takes under 30 seconds
- [ ] SC-002: Task list displays clearly with all fields
- [ ] SC-003: No crashes from invalid input (100% validation)
- [ ] SC-004: Invalid IDs produce error within 1 second
- [ ] SC-005: All five operations work independently
- [ ] SC-006: Application exits cleanly

**Verification**:
- [ ] All 16 functional and success criteria met
- [ ] No implementation details leaked into spec
- [ ] No features added beyond Phase-1 scope
- [ ] Phase-1 foundation ready for Phase-2

**Acceptance**: Implementation fully satisfies specification.

---

## Task Group 8: Code Quality & Final Checks

### Task 8.1: Code Review Checklist

**Description**: Review code for quality, readability, and standards.

**Checklist**:
- [ ] All files have module-level docstrings
- [ ] All functions have docstrings with parameters and return types
- [ ] Type hints present on all function signatures
- [ ] Variable names are clear and descriptive
- [ ] No magic numbers or strings (use constants)
- [ ] Error handling is explicit (try/except with informative messages)
- [ ] No print debugging (all output intentional)
- [ ] Code is DRY (no repeated logic)
- [ ] No commented-out code left behind
- [ ] Professional formatting (consistent indentation, spacing)

**Verification**:
- [ ] All code review items checked
- [ ] Code is professional-grade and maintainable
- [ ] New developer can understand the code

**Acceptance**: Code meets quality standards.

---

### Task 8.2: Git Commit & Documentation Final Check

**Description**: Prepare for commit and verify all files are in place.

**Checklist**:
- [ ] All source files present: `src/main.py`, `src/cli.py`, `src/task_manager.py`, `src/models.py`
- [ ] All test files present: `tests/test_task_manager.py`, `tests/test_cli.py`
- [ ] All documentation present: `docs/SETUP.md`, `docs/USAGE.md`, `hafiz-naveed/README.md`
- [ ] All specification/plan files present: `hafiz-naveed/phase-1/spec.md`, `hafiz-naveed/phase-1/plan.md`
- [ ] `.gitignore` configured for Python
- [ ] `requirements.txt` includes all dependencies
- [ ] All tests passing
- [ ] No uncommitted changes
- [ ] Ready to commit and push

**Verification**:
- [ ] `git status` shows clean working tree
- [ ] All required files exist
- [ ] All tests pass

**Acceptance**: Ready for commit and PR creation.

---

## Summary

**Total Tasks**: 13 (organized into 8 groups)

**Estimated Completion Order**:
1. Task Group 1: Project Setup (Tasks 1.1, 1.2)
2. Task Group 2: Task Model (Task 2.1)
3. Task Group 3: TodoActionAgent (Tasks 3.1, 3.2)
4. Task Group 4: HafizNaveed Agent (Tasks 4.1, 4.2)
5. Task Group 5: Entry Point (Task 5.1)
6. Task Group 6: Documentation (Tasks 6.1, 6.2)
7. Task Group 7: Verification (Tasks 7.1, 7.2, 7.3)
8. Task Group 8: Final Checks (Tasks 8.1, 8.2)

**Success Condition**: All tasks completed with all verification checkmarks passing.

**Next Phase**: After Task 8.2 passes, commit to feature branch, create PR to master, and proceed with Phase-2 specification.

---

**Status**: Ready for Implementation
**Next Action**: `/sp.implement` to begin code generation
