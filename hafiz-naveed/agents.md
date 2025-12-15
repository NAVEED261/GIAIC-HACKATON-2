# Agent Architecture: Phase-1 Todo System

**Created**: 2025-12-14
**Project**: Hackathon-2 Todo System
**Phase**: Phase-1 (Console-Based)

---

## Overview

Phase-1 implements a two-tier agent architecture:

1. **HafizNaveed** (Main Agent): Orchestrator and CLI handler
2. **TodoActionAgent** (Sub-Agent): Task operations executor

This design separates concerns: HafizNaveed handles user interaction; TodoActionAgent handles business logic.

---

## Agent 1: HafizNaveed (Main/Supervisor)

### Purpose

HafizNaveed is the **primary orchestrator** responsible for:
- Managing the command-line interface (CLI)
- Displaying the main menu
- Capturing and validating user input
- Routing requests to TodoActionAgent
- Displaying results and error messages
- Controlling application flow (loop until exit)

### Responsibilities

| Responsibility | Details |
|---|---|
| **Menu Management** | Display formatted menu with 6 options; handle user selection |
| **Input Processing** | Capture user input; validate format and range |
| **Request Routing** | Route menu selections to appropriate TodoActionAgent methods |
| **Response Formatting** | Format task data for display; show confirmation/error messages |
| **Flow Control** | Maintain application loop; handle exit condition |
| **Error Presentation** | Display user-friendly error messages for invalid input or operations |

### Input/Output Format

#### Input

```
User Selection: [1-6 or any input]
Task ID (if needed): [integer]
Task Title (if needed): [string]
```

#### Output

```
Menu display with options
Task list (formatted table/list)
Confirmation messages
Error messages
```

### Delegation Rules

**HafizNaveed delegated to TodoActionAgent**:
- **User selects "Add Task" (1)**: Delegate to `TodoActionAgent.add_task(title)`
- **User selects "List Tasks" (2)**: Delegate to `TodoActionAgent.list_tasks()`
- **User selects "Update Task" (3)**: Delegate to `TodoActionAgent.update_task(task_id, new_title)`
- **User selects "Delete Task" (4)**: Delegate to `TodoActionAgent.delete_task(task_id)`
- **User selects "Mark Complete" (5)**: Delegate to `TodoActionAgent.mark_complete(task_id)`
- **User selects "Exit" (6)**: Terminate application (no delegation)

**Guardrails**:
- HafizNaveed MUST NOT manipulate task data directly
- HafizNaveed MUST NOT store tasks in memory (that's TodoActionAgent's job)
- HafizNaveed MUST validate input BEFORE delegating to TodoActionAgent
- HafizNaveed MUST catch and handle all exceptions from TodoActionAgent

### Communication Protocol

```
HafizNaveed (CLI)
    ↓ (menu selection + optional parameters)
TodoActionAgent (Business Logic)
    ↓ (result or exception)
HafizNaveed (Display result to user)
```

### Implementation Location

**File**: `src/cli.py`

**Class**: `HafizNaveed`

**Methods**:
- `__init__()`: Initialize with TodoActionAgent instance
- `run()`: Main application loop
- `_display_menu()`: Show menu options
- `_get_user_input()`: Capture user input
- `_handle_add_task()`: Route and display add result
- `_handle_list_tasks()`: Route and display task list
- `_handle_update_task()`: Route and display update result
- `_handle_delete_task()`: Route and display delete result
- `_handle_mark_complete()`: Route and display completion result

---

## Agent 2: TodoActionAgent (Sub-Agent)

### Purpose

TodoActionAgent is the **execution engine** responsible for:
- Managing the in-memory task store
- Executing all task operations (CRUD)
- Validating task data
- Maintaining task state and ID generation

### Responsibilities

| Responsibility | Details |
|---|---|
| **Task Storage** | Maintain in-memory list of Task objects |
| **Task Creation** | Add new tasks with auto-generated unique IDs |
| **Task Retrieval** | Retrieve all tasks or find task by ID |
| **Task Updates** | Modify task titles with validation |
| **Task Deletion** | Remove tasks from store |
| **Status Management** | Update task status (Pending → Completed) |
| **Validation** | Validate titles, IDs, and operations |
| **ID Generation** | Auto-increment task IDs starting from 1 |

### Input/Output Format

#### Input (from HafizNaveed)

```python
add_task(title: str) -> Task

list_tasks() -> List[Task]

get_task(task_id: int) -> Task | None

update_task(task_id: int, new_title: str) -> bool

delete_task(task_id: int) -> bool

mark_complete(task_id: int) -> bool
```

#### Output (to HafizNaveed)

```python
# Successful operations
Task object (with id, title, status)
List[Task] (all tasks)
True/False (operation success)

# Failures
Raise ValueError (invalid input)
Return None (task not found)
Return False (operation failed)
```

### Method Specifications

#### Method: `add_task(title: str) -> Task`

**Input**: Task title string

**Process**:
1. Validate title is not empty (raise ValueError if empty)
2. Generate next ID (increment counter)
3. Create Task object with ID, title, status="Pending"
4. Add to task list
5. Return Task object

**Output**: Task object

**Exceptions**: ValueError if title is invalid

---

#### Method: `list_tasks() -> List[Task]`

**Input**: None

**Process**:
1. Return copy of task list (all tasks in order)

**Output**: List[Task] (may be empty)

**Exceptions**: None

---

#### Method: `get_task(task_id: int) -> Task | None`

**Input**: Task ID (integer)

**Process**:
1. Search task list for matching ID
2. Return task if found, None otherwise

**Output**: Task object or None

**Exceptions**: None

---

#### Method: `update_task(task_id: int, new_title: str) -> bool`

**Input**: Task ID, new title string

**Process**:
1. Validate new_title is not empty (raise ValueError if empty)
2. Find task by ID
3. If found, update title and return True
4. If not found, return False

**Output**: True (success) or False (not found)

**Exceptions**: ValueError if new_title is invalid

---

#### Method: `delete_task(task_id: int) -> bool`

**Input**: Task ID (integer)

**Process**:
1. Find task by ID
2. If found, remove from list and return True
3. If not found, return False

**Output**: True (success) or False (not found)

**Exceptions**: None

---

#### Method: `mark_complete(task_id: int) -> bool`

**Input**: Task ID (integer)

**Process**:
1. Find task by ID
2. If found, set status to "Completed" and return True
3. If not found, return False

**Output**: True (success) or False (not found)

**Exceptions**: None

---

### Data Store

**Structure**:
```python
_tasks: List[Task] = []
_next_id: int = 1
```

**Lifecycle**:
- Initialized empty on application start
- Persists during application session
- Lost on application exit (in-memory only)

### Guardrails

**What TodoActionAgent MUST do**:
- Validate all inputs
- Manage IDs without gaps
- Maintain data consistency
- Handle edge cases (empty list, invalid IDs, etc.)

**What TodoActionAgent MUST NOT do**:
- Display information to user (that's HafizNaveed's job)
- Accept invalid data
- Make assumptions about user intent
- Directly interact with CLI or input/output

### Implementation Location

**File**: `src/task_manager.py`

**Class**: `TodoActionAgent`

**Data Model**: `src/models.py` (Task class)

---

## Agent Interaction Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Start                        │
│                  python src/main.py                         │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                HafizNaveed Agent Starts                      │
│           Initialize TodoActionAgent Instance               │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ↓
                    ┌────────────────┐
                    │  Display Menu  │
                    └────────┬───────┘
                             │
                    ┌────────▼────────┐
                    │ Get User Input  │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
      ┌───▼──┐          ┌───▼──┐          ┌───▼──┐
      │ Add  │          │List  │          │Exit  │
      │ Task │          │Tasks │          │      │
      └───┬──┘          └───┬──┘          └──┬───┘
          │                  │              │
    ┌─────▼──────┐    ┌──────▼──┐     ┌────▼─────┐
    │ Prompt for │    │ Delegate │    │ Terminate│
    │ title      │    │ to .list │    │Application
    └─────┬──────┘    └──────┬───┘    └──────────┘
          │                  │
    ┌─────▼──────────────────▼──────┐
    │ Delegate to TodoActionAgent    │
    │ (execute operation)            │
    └──────────┬────────────────────┘
               │
    ┌──────────▼─────────────┐
    │ Return Result/Error    │
    └──────────┬─────────────┘
               │
    ┌──────────▼──────────────┐
    │ Format & Display Result │
    │ (HafizNaveed)           │
    └──────────┬──────────────┘
               │
         ┌─────▼─────┐
         │ Loop Again │
         │ (unless    │
         │  Exit)     │
         └────────────┘
```

---

## Error Handling

### Error Sources & Handling

| Error | Source | Handler | User Message |
|-------|--------|---------|--------------|
| Empty title | HafizNaveed validation OR TodoActionAgent | HafizNaveed | "Task title cannot be empty." |
| Invalid ID format | HafizNaveed validation | HafizNaveed | "Please enter a valid task ID (number)." |
| Task not found | TodoActionAgent search | HafizNaveed | "Task not found. Please check the ID and try again." |
| Invalid menu option | HafizNaveed validation | HafizNaveed | "Invalid option. Please enter 1-6." |
| Unhandled exception | Any | HafizNaveed (catch-all) | "An error occurred. Please try again." |

### Exception Propagation

```
TodoActionAgent raises ValueError
    ↓
HafizNaveed catches exception
    ↓
HafizNaveed displays user-friendly message
    ↓
Application continues (no crash)
```

---

## Agent Responsibilities Matrix

| Task | HafizNaveed | TodoActionAgent |
|------|-------------|-----------------|
| Display menu | ✅ | ❌ |
| Get user input | ✅ | ❌ |
| Validate input format | ✅ | ❌ |
| Validate business logic | ❌ | ✅ |
| Store tasks in memory | ❌ | ✅ |
| Create/Update/Delete tasks | ❌ | ✅ |
| Display results to user | ✅ | ❌ |
| Control application loop | ✅ | ❌ |
| Handle exceptions | ✅ | ⚠️ (raise to HafizNaveed) |

---

## Phase-2 Compatibility

This two-agent architecture is designed to scale:

**Phase-2 (Full-stack Web)**:
- TodoActionAgent remains unchanged (same logic)
- HafizNaveed is replaced with REST API handler
- New agents added for database, authentication, etc.
- Business logic fully reusable

**Phase-3+ (AI Chatbot, K8s, Cloud)**:
- TodoActionAgent continues as core service
- Replaced at boundaries, reused at core

---

## Summary

| Aspect | HafizNaveed | TodoActionAgent |
|--------|-------------|-----------------|
| **Type** | Orchestrator | Executor |
| **Scope** | CLI interface + flow | Task operations + state |
| **File** | src/cli.py | src/task_manager.py |
| **Key Method** | run() | add_task(), list_tasks(), etc. |
| **Responsibility** | User interaction | Business logic |
| **State Management** | None (stateless) | Task store + ID counter |
| **Dependencies** | TodoActionAgent | models.py (Task class) |

This architecture ensures clear separation of concerns and makes Phase-1 a solid foundation for all future phases.

---

**Status**: Complete
**Next**: Implementation begins with this architecture as guide
