# Agent Skills: Phase-1 Todo System

**Created**: 2025-12-14
**Project**: Hackathon-2 Todo System
**Phase**: Phase-1 (Console-Based)

---

## Overview

This document defines the **skills** (capabilities) of both agents in Phase-1:

- **HafizNaveed** (Main Agent): CLI orchestration and user interaction skills
- **TodoActionAgent** (Sub-Agent): Task management and data operation skills

Each skill is defined with purpose, example usage, and expected outcome.

---

## HafizNaveed Agent Skills

### Skill 1: Display Menu

**Skill Name**: `display_menu`

**Purpose**: Present the main menu with all available options in a formatted, user-friendly manner.

**Example User Query**: User starts the application

**Expected Action/Output**:
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

---

### Skill 2: Capture User Input

**Skill Name**: `capture_input`

**Purpose**: Read and return user input from the command line.

**Example User Query**: User enters a menu option (e.g., "1" or "add")

**Expected Action/Output**: Input is captured as string, returned to menu handler for processing.

---

### Skill 3: Validate Menu Selection

**Skill Name**: `validate_menu_input`

**Purpose**: Verify that user input is a valid menu option (1-6) and reject invalid inputs with a friendly error message.

**Example User Query**: User enters "9" or "abc"

**Expected Action/Output**: "Invalid option. Please enter 1-6." (Display and loop back to menu)

---

### Skill 4: Route to Add Task

**Skill Name**: `route_add_task`

**Purpose**: Handle the "Add Task" menu selection by prompting for a title and delegating to TodoActionAgent.

**Example User Query**: User selects "1" (Add Task)

**Expected Action/Output**:
```
Enter task title: Buy groceries
✓ Task added with ID: 1
Back to menu...
```

---

### Skill 5: Route to List Tasks

**Skill Name**: `route_list_tasks`

**Purpose**: Retrieve all tasks from TodoActionAgent and display them in a clear, formatted manner.

**Example User Query**: User selects "2" (List Tasks)

**Expected Action/Output**:
```
ID | Title              | Status
---|--------------------|-----------
1  | Buy groceries      | Pending
2  | Complete homework  | Completed
3  | Call dentist       | Pending
```

---

### Skill 6: Route to Update Task

**Skill Name**: `route_update_task`

**Purpose**: Handle the "Update Task" menu selection by prompting for task ID and new title, then delegating to TodoActionAgent.

**Example User Query**: User selects "3" (Update Task)

**Expected Action/Output**:
```
Enter task ID: 1
Enter new title: Buy organic groceries
✓ Task updated successfully
```

---

### Skill 7: Route to Delete Task

**Skill Name**: `route_delete_task`

**Purpose**: Handle the "Delete Task" menu selection by prompting for task ID and delegating to TodoActionAgent.

**Example User Query**: User selects "4" (Delete Task)

**Expected Action/Output**:
```
Enter task ID: 2
✓ Task deleted successfully
```

---

### Skill 8: Route to Mark Complete

**Skill Name**: `route_mark_complete`

**Purpose**: Handle the "Mark Task Complete" menu selection by prompting for task ID and delegating to TodoActionAgent.

**Example User Query**: User selects "5" (Mark Task Complete)

**Expected Action/Output**:
```
Enter task ID: 1
✓ Task marked as completed
```

---

### Skill 9: Handle Invalid Task ID

**Skill Name**: `handle_invalid_id`

**Purpose**: Display a friendly error message when user provides a non-existent task ID or invalid format.

**Example User Query**: User enters task ID "999" or "abc"

**Expected Action/Output**: "Task not found. Please check the ID and try again." (or) "Please enter a valid task ID (number)."

---

### Skill 10: Control Application Loop

**Skill Name**: `control_loop`

**Purpose**: Maintain the continuous menu loop, handling the Exit condition to terminate the application cleanly.

**Example User Query**: User selects "6" (Exit)

**Expected Action/Output**: Application terminates without errors; user is returned to command prompt.

---

## TodoActionAgent Skills

### Skill 1: Create Task

**Skill Name**: `create_task`

**Purpose**: Add a new task with a title, assigning a unique auto-incremented ID and default "Pending" status.

**Example User Query**: "Add task: Buy groceries" (routed from HafizNaveed)

**Expected Action/Output**:
```
Task Created:
{
  "id": 1,
  "title": "Buy groceries",
  "status": "Pending"
}
```

---

### Skill 2: Retrieve All Tasks

**Skill Name**: `retrieve_all_tasks`

**Purpose**: Return a list of all tasks currently in the system, maintaining their order and complete information.

**Example User Query**: "List all tasks" (routed from HafizNaveed)

**Expected Action/Output**:
```
[
  {"id": 1, "title": "Buy groceries", "status": "Pending"},
  {"id": 2, "title": "Complete homework", "status": "Completed"},
  {"id": 3, "title": "Call dentist", "status": "Pending"}
]
```

---

### Skill 3: Find Task by ID

**Skill Name**: `find_task`

**Purpose**: Search for a specific task by its ID and return it, or indicate not found.

**Example User Query**: "Get task with ID 2" (internal operation)

**Expected Action/Output**:
```
Task Found:
{
  "id": 2,
  "title": "Complete homework",
  "status": "Completed"
}
```
or
```
Task Not Found (returns None)
```

---

### Skill 4: Update Task Title

**Skill Name**: `update_task_title`

**Purpose**: Modify the title of an existing task by its ID, validating the new title is not empty.

**Example User Query**: "Update task 1 title to 'Buy organic groceries'" (routed from HafizNaveed)

**Expected Action/Output**:
```
Task Updated:
{
  "id": 1,
  "title": "Buy organic groceries",
  "status": "Pending"
}
```

---

### Skill 5: Delete Task

**Skill Name**: `delete_task`

**Purpose**: Remove a task from the system by its ID, returning success or failure status.

**Example User Query**: "Delete task with ID 3" (routed from HafizNaveed)

**Expected Action/Output**:
```
Deletion Status: Success (True)
Task removed from list
```
or
```
Deletion Status: Failed - Task not found (False)
```

---

### Skill 6: Mark Task Complete

**Skill Name**: `mark_task_complete`

**Purpose**: Change a task's status from "Pending" to "Completed" by its ID.

**Example User Query**: "Mark task 1 as completed" (routed from HafizNaveed)

**Expected Action/Output**:
```
Task Updated:
{
  "id": 1,
  "title": "Buy groceries",
  "status": "Completed"
}
```

---

### Skill 7: Validate Task Title

**Skill Name**: `validate_title`

**Purpose**: Check that a task title is not empty or whitespace-only, raising an error if invalid.

**Example User Query**: Title validation during add or update operations

**Expected Action/Output**:
```
Valid: Returns True (or proceeds silently)
Invalid: Raises ValueError("Task title cannot be empty")
```

---

### Skill 8: Generate Unique ID

**Skill Name**: `generate_unique_id`

**Purpose**: Create sequential, unique task IDs starting from 1 and incrementing with each new task.

**Example User Query**: Task creation triggers ID generation

**Expected Action/Output**:
```
Task 1 created → ID = 1
Task 2 created → ID = 2
Task 3 created → ID = 3
(Sequential without gaps)
```

---

### Skill 9: Maintain Data Integrity

**Skill Name**: `maintain_integrity`

**Purpose**: Ensure data consistency—prevent duplicate IDs, maintain task order, and validate operations.

**Example User Query**: All operations implicitly use this skill

**Expected Action/Output**:
```
No duplicate IDs
Tasks remain in creation order
Operations are atomic (succeed or fail completely)
No data corruption
```

---

## Skill Mapping to Phase-1 Requirements

| Phase-1 Action | HafizNaveed Skills | TodoActionAgent Skills |
|---|---|---|
| **Add Task** | route_add_task, capture_input, validate_menu_input | create_task, validate_title, generate_unique_id |
| **List Tasks** | route_list_tasks, capture_input, validate_menu_input | retrieve_all_tasks |
| **Update Task** | route_update_task, capture_input, validate_menu_input, handle_invalid_id | update_task_title, find_task, validate_title |
| **Delete Task** | route_delete_task, capture_input, validate_menu_input, handle_invalid_id | delete_task, find_task |
| **Mark Complete** | route_mark_complete, capture_input, validate_menu_input, handle_invalid_id | mark_task_complete, find_task |
| **Exit** | control_loop, capture_input, validate_menu_input | (N/A) |

---

## Skill Composition Example: "Add Task" Workflow

**User Action**: Selects menu option 1 and enters "Buy groceries"

**Skill Chain**:

```
HafizNaveed.display_menu()
    ↓
HafizNaveed.capture_input() → "1"
    ↓
HafizNaveed.validate_menu_input() → Valid
    ↓
HafizNaveed.route_add_task()
    ↓
HafizNaveed.capture_input() → "Buy groceries"
    ↓
TodoActionAgent.validate_title() → Valid
    ↓
TodoActionAgent.generate_unique_id() → 1
    ↓
TodoActionAgent.create_task() → Task(id=1, title="Buy groceries", status="Pending")
    ↓
HafizNaveed displays success message
    ↓
HafizNaveed.control_loop() → back to menu
```

---

## Skills Not Included (Out of Phase-1 Scope)

The following skills are **explicitly NOT included** in Phase-1:

- Search/filter tasks
- Sort tasks by title or status
- Assign priority or due dates
- Recurring tasks
- Task categories or tags
- Data persistence (files, database)
- Multi-user support
- Authentication
- REST API endpoints
- Web interface
- Real-time updates
- Cloud storage

These will be introduced in Phase-2 and beyond.

---

## Guardrails for All Skills

**All HafizNaveed Skills MUST**:
- Validate input before using it
- Display user-friendly messages
- Never crash on invalid input
- Delegate to TodoActionAgent for business logic
- Handle exceptions gracefully

**All TodoActionAgent Skills MUST**:
- Validate business logic
- Never accept invalid data
- Return meaningful success/failure indicators
- Maintain data consistency
- Never directly interact with CLI or user

---

## Summary

| Dimension | HafizNaveed | TodoActionAgent |
|---|---|---|
| **Number of Skills** | 10 | 9 |
| **Scope** | User Interaction | Data Operations |
| **Primary Role** | Orchestration | Execution |
| **Error Handling** | Input validation & user feedback | Business logic validation |
| **State Management** | None | Task store |
| **External Dependencies** | TodoActionAgent | models.py (Task class) |

---

**Status**: Complete
**Next**: Implementation begins using these skills as specifications
