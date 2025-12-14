Step 1: Navigate to Phase-1

  cd Phase-1

  Step 2: Install Dependencies

  pip install -r requirements.txt

  Step 3: Run the App

  cd src
  python main.py

  Step 4: Use the Menu

  ===== Todo Menu =====
  1. Add Task
  2. List Tasks
  3. Update Task
  4. Delete Task
  5. Mark Task Complete
  6. Exit
  Choose an option (1-6):

  Example:

  1. Select "1" → Enter "Buy groceries" → Task added ✓
  2. Select "2" → See all tasks
  3. Select "5" → Enter task ID → Mark complete
  4. Select "6" → Exit app

  Run Tests

  cd ..
  pytest tests/ -v
  # Result: 53/53 PASSED ✅

  Documentation

  - Setup: Phase-1/docs/SETUP.md
  - Usage: Phase-1/docs/USAGE.md
  - Quick Ref: Phase-1/PHASE-1-USE.md

  ---
  Bas itna! Phase-1 ready to use! 🚀
