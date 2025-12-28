@echo off
echo Starting Phase-5 Backend...
set DATABASE_URL=postgresql://todouser:todopass@localhost:5432/tododb
set JWT_SECRET=phase5-secret-key-minimum-32-characters
set PYTHONIOENCODING=utf-8
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
