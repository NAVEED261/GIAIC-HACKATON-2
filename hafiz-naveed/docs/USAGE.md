# Phase-1 Usage Guide

**Project**: Hackathon-2 Todo System - Phase 1
**Created**: 2025-12-14

---

## Quick Start

```bash
# Navigate to project directory
cd hafiz-naveed

# Run the application
python src/main.py
```

You'll see the main menu:

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

## Menu Options Reference

### Option 1: Add Task

**What it does**: Create a new task with a title

**Steps**:
1. Select `1` from the menu
2. Enter a task title (e.g., "Buy groceries")
3. System confirms with task ID

**Example**:
```
Choose an option (1-6): 1
Enter task title: Buy groceries
✓ Task added with ID: 1

===== Todo Menu =====
1. Add Task
2. List Tasks
...
```

**Tips**:
- Task title cannot be empty
- Titles can be any length
- Tasks are automatically assigned unique IDs

---

### Option 2: List Tasks

**What it does**: Display all tasks in your list

**Steps**:
1. Select `2` from the menu
2. See all tasks with ID, title, and status

**Example**:
```
Choose an option (1-6): 2

ID | Title              | Status
---|--------------------|-----------
1  | Buy groceries      | Pending
2  | Complete homework  | Completed
3  | Call dentist       | Pending

===== Todo Menu =====
...
```

**Status Values**:
- **Pending**: Task not yet completed
- **Completed**: Task is done

**When empty**:
```
No tasks yet. Add one with option 1!
```

---

### Option 3: Update Task

**What it does**: Change the title of an existing task

**Steps**:
1. Select `3` from the menu
2. Enter the task ID you want to update
3. Enter the new title
4. System confirms the update

**Example**:
```
Choose an option (1-6): 3
Enter task ID: 1
Enter new title: Buy organic groceries
✓ Task updated successfully

===== Todo Menu =====
...
```

**Error Handling**:
- Invalid ID format: "Please enter a valid task ID (number)."
- Non-existent ID: "Task not found. Please check the ID and try again."
- Empty new title: "Task title cannot be empty."

---

### Option 4: Delete Task

**What it does**: Remove a task from your list

**Steps**:
1. Select `4` from the menu
2. Enter the task ID you want to delete
3. System confirms deletion

**Example**:
```
Choose an option (1-6): 4
Enter task ID: 3
✓ Task deleted successfully

===== Todo Menu =====
...
```

**Error Handling**:
- Invalid ID format: "Please enter a valid task ID (number)."
- Non-existent ID: "Task not found. Please check the ID and try again."

---

### Option 5: Mark Task Complete

**What it does**: Mark a task as completed

**Steps**:
1. Select `5` from the menu
2. Enter the task ID you want to mark complete
3. System confirms the status change

**Example**:
```
Choose an option (1-6): 5
Enter task ID: 1
✓ Task marked as completed

===== Todo Menu =====
...
```

**After Completion**:
```
Choose an option (1-6): 2

ID | Title              | Status
---|--------------------|-----------
1  | Buy groceries      | Completed
2  | Complete homework  | Completed
3  | Call dentist       | Pending
```

**Error Handling**:
- Invalid ID format: "Please enter a valid task ID (number)."
- Non-existent ID: "Task not found. Please check the ID and try again."

---

### Option 6: Exit

**What it does**: Close the application

**Steps**:
1. Select `6` from the menu
2. Application terminates

**Example**:
```
Choose an option (1-6): 6
Thank you for using Todo System. Goodbye!
```

---

## Common Workflows

### Workflow 1: Create and Complete a Task

```
===== Todo Menu =====
1. Add Task
2. List Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Exit
Choose an option (1-6): 1
Enter task title: Study for exam
✓ Task added with ID: 1

Choose an option (1-6): 2

ID | Title          | Status
---|----------------|---------
1  | Study for exam | Pending

Choose an option (1-6): 5
Enter task ID: 1
✓ Task marked as completed

Choose an option (1-6): 2

ID | Title          | Status
---|----------------|---------
1  | Study for exam | Completed

Choose an option (1-6): 6
```

---

### Workflow 2: Update Multiple Tasks

```
Choose an option (1-6): 1
Enter task title: Project task 1
✓ Task added with ID: 1

Choose an option (1-6): 1
Enter task title: Project task 2
✓ Task added with ID: 2

Choose an option (1-6): 3
Enter task ID: 1
Enter new title: Complete project design
✓ Task updated successfully

Choose an option (1-6): 3
Enter task ID: 2
Enter new title: Submit project
✓ Task updated successfully

Choose an option (1-6): 2

ID | Title                  | Status
---|------------------------|----------
1  | Complete project design | Pending
2  | Submit project         | Pending
```

---

### Workflow 3: Manage a Daily Todo List

```
# Morning - Add tasks
Choose an option (1-6): 1
Enter task title: Attend standup
✓ Task added with ID: 1

Choose an option (1-6): 1
Enter task title: Review pull requests
✓ Task added with ID: 2

Choose an option (1-6): 1
Enter task title: Update documentation
✓ Task added with ID: 3

# Noon - Check progress
Choose an option (1-6): 2

ID | Title                  | Status
---|------------------------|----------
1  | Attend standup         | Pending
2  | Review pull requests   | Pending
3  | Update documentation   | Pending

# Complete tasks as you go
Choose an option (1-6): 5
Enter task ID: 1
✓ Task marked as completed

Choose an option (1-6): 5
Enter task ID: 2
✓ Task marked as completed

# Evening - Final review
Choose an option (1-6): 2

ID | Title                  | Status
---|------------------------|----------
1  | Attend standup         | Completed
2  | Review pull requests   | Completed
3  | Update documentation   | Pending
```

---

## Error Messages & Solutions

| Error Message | Meaning | Solution |
|---|---|---|
| `Invalid option. Please enter 1-6.` | Menu selection not recognized | Enter a number between 1 and 6 |
| `Please enter a valid task ID (number).` | Task ID is not a number | Enter only digits (e.g., 1, 2, 3) |
| `Task not found. Please check the ID and try again.` | Task ID doesn't exist | Check task IDs with "List Tasks" option |
| `Task title cannot be empty.` | Title is blank or spaces-only | Enter a meaningful task title |

---

## Tips & Best Practices

### 1. Use Descriptive Titles

**Good titles**:
- "Buy groceries for dinner"
- "Send project report to manager"
- "Call dentist to schedule appointment"

**Vague titles**:
- "Do stuff"
- "Remember"
- "Task"

---

### 2. Review Your List Regularly

Press option 2 (List Tasks) often to:
- See what you've accomplished
- Identify what's still pending
- Stay motivated by completed tasks

---

### 3. Update Task Titles if Plans Change

If a task changes:
```
Choose an option (1-6): 3
Enter task ID: 5
Enter new title: Updated task description
✓ Task updated successfully
```

---

### 4. Delete Tasks You No Longer Need

Remove tasks that are no longer relevant:
```
Choose an option (1-6): 4
Enter task ID: 3
✓ Task deleted successfully
```

---

### 5. Important: Data is Temporary

**Phase-1 Note**: Tasks are stored in memory only. When you exit the application, all tasks are lost. This is by design for Phase-1. Phase-2 will add persistent database storage.

If you need to save your tasks, take a screenshot before exiting!

---

## Keyboard Shortcuts & Efficiency

### Faster Navigation

- Type menu option and press Enter
- Type task ID and press Enter
- Type new title and press Enter

### Backtracking

- Made a mistake? The menu reappears after each action
- Just select the correct option and try again

---

## What's NOT Supported in Phase-1

These features will be added in later phases:

- ❌ Saving tasks to a file or database
- ❌ Task priorities or due dates
- ❌ Task categories or tags
- ❌ Searching or filtering tasks
- ❌ Multiple users or accounts
- ❌ Web interface or mobile app
- ❌ Recurring tasks
- ❌ Collaborative editing

---

## Getting Help

### Issues?

1. Check SETUP.md for installation help
2. Review this guide for usage examples
3. Check menu options - they guide you through each operation

### Questions about the system?

- Read `../agents.md` for architecture details
- Read `../phase-1/spec.md` for detailed requirements
- Read `../README.md` for project overview

---

## Feedback & Improvements

As you use the system, think about:
- What features would make tasks easier?
- What's confusing or unclear?
- What would you add in future phases?

These ideas will shape Phase-2 and beyond!

---

**Version**: Phase-1 Console-Based Todo
**Last Updated**: 2025-12-14
**Status**: ✅ Ready to Use
