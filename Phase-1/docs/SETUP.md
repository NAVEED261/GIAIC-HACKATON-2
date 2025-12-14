# Phase-1 Setup Guide

**Project**: Hackathon-2 Todo System - Phase 1
**Created**: 2025-12-14

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**: [Download Python](https://www.python.org/downloads/)
- **pip** (Python package manager): Usually installed with Python
- **git** (version control): [Download Git](https://git-scm.com/)

### Verify Prerequisites

```bash
# Check Python version
python --version
# Should output: Python 3.8 or higher

# Check pip version
pip --version
# Should output: pip X.X.X from ...

# Check git version
git --version
# Should output: git version X.X.X
```

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/NAVEED261/GIAIC-HACKATON-2.git
cd GIAIC-HACKATON-2/hafiz-naveed
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
# Check installed packages
pip list

# Run a quick test
pytest tests/ -v
```

---

## Running the Application

### Start the Application

```bash
python src/main.py
```

### Expected Output

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

## Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
# Unit tests only
pytest tests/test_task_manager.py -v

# Integration tests only
pytest tests/test_cli.py -v
```

### Run Tests with Coverage

```bash
pytest tests/ -v --cov=src --cov-report=html
```

---

## Troubleshooting

### Python Not Found

**Problem**: `python: command not found` or `'python' is not recognized`

**Solution**:
- Ensure Python is installed from [python.org](https://www.python.org/)
- On Windows, check "Add Python to PATH" during installation
- Try `python3` instead of `python` on macOS/Linux

### Module Not Found Error

**Problem**: `ModuleNotFoundError: No module named 'pytest'`

**Solution**:
```bash
# Ensure virtual environment is activated
# Then reinstall requirements
pip install -r requirements.txt
```

### Permission Denied (macOS/Linux)

**Problem**: `Permission denied: './main.py'`

**Solution**:
```bash
chmod +x src/main.py
python src/main.py
```

### Virtual Environment Issues

**Problem**: Virtual environment not activating properly

**Solution**:
```bash
# Delete old venv
rm -rf venv

# Create new venv
python -m venv venv

# Activate it
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install requirements again
pip install -r requirements.txt
```

---

## Environment Configuration

### Optional: Create .env File

For future phases, you might need a `.env` file for configuration:

```bash
# .env (not needed for Phase-1, but good practice)
DEBUG=True
LOG_LEVEL=INFO
```

**Important**: Never commit `.env` files to version control. It's already in `.gitignore`.

---

## Next Steps

1. **Learn the basics**: Read `USAGE.md` for user guide
2. **Understand architecture**: Review `../agents.md` for agent design
3. **Check specifications**: Review `../phase-1/spec.md` for requirements
4. **Start using**: Run `python src/main.py` and try adding a task

---

## Getting Help

- **User Guide**: See `USAGE.md`
- **Architecture**: See `../agents.md`
- **Specification**: See `../phase-1/spec.md`
- **Implementation Plan**: See `../phase-1/plan.md`
- **Tasks**: See `../phase-1/tasks.md`

---

**Status**: ✅ Setup Complete - Ready to Use
