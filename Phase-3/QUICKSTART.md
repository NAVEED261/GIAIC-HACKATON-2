# Phase-3 Quick Start Guide

AI-Powered Todo Chatbot - Get Started in 5 Minutes

---

## Prerequisites

- Python 3.8+ (backend)
- Node.js 18+ (frontend)
- PostgreSQL 13+ or SQLite (database)
- OpenAI API key

---

## 1. Setup Environment

### Backend

```bash
cd Phase-3/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=sqlite:///./test.db
OPENAI_API_KEY=your_openai_key_here
JWT_SECRET=your-secret-key-min-32-chars-long
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
LOG_LEVEL=info
EOF
```

### Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env.local file
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
```

---

## 2. Start Services

### Backend

```bash
cd Phase-3/backend
python -m uvicorn main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Frontend (new terminal)

```bash
cd Phase-3/frontend
npm run dev
```

Expected output:
```
> ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

---

## 3. Quick Test

### Health Check

```bash
curl http://localhost:8000/health
# Response: {"status": "healthy"}
```

### Send Chat Message

First, create a JWT token:

```bash
python3 << 'EOF'
import jwt
from datetime import datetime, timedelta

user_id = 1
secret = "your-secret-key-min-32-chars-long"
payload = {
    'user_id': user_id,
    'exp': datetime.utcnow() + timedelta(days=7)
}
token = jwt.encode(payload, secret, algorithm='HS256')
print(token)
EOF
```

Then send a message:

```bash
curl -X POST http://localhost:8000/api/1/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": null,
    "message": "Add task: Buy groceries"
  }'
```

Expected response:
```json
{
  "conversation_id": 1,
  "response": "Task 'Buy groceries' has been added to your todo list.",
  "tool_calls": ["add_task"],
  "status": "success"
}
```

---

## 4. Web Interface

Open browser and go to: **http://localhost:3000/chat**

You should see:
- Chat interface with welcome message
- Message input field
- Send button

Try these commands:
1. "Add task: Buy milk"
2. "Show my tasks"
3. "Mark task 1 complete"

---

## 5. Typical Workflow

### Adding Tasks

```
User: "Add task: Buy groceries"
Assistant: "Task 'Buy groceries' has been added."
```

### Listing Tasks

```
User: "Show my tasks"
Assistant: "You have 3 tasks: 1. Buy groceries, 2. Call doctor, 3. Review report"
```

### Completing Tasks

```
User: "Mark task 1 complete"
Assistant: "Task 'Buy groceries' marked as complete."
```

### Updating Tasks

```
User: "Update task 2 to call the dentist"
Assistant: "Task updated successfully."
```

### Deleting Tasks

```
User: "Delete task 3"
Assistant: "Task 'Review report' has been deleted."
```

---

## 6. Testing

### Backend Tests

```bash
cd Phase-3/backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd Phase-3/frontend
npm test
```

---

## 7. Debugging

### Backend Logs

Enable debug logging:

```bash
# In .env file
LOG_LEVEL=debug
```

Then restart backend.

### Check Database

```bash
# For SQLite
sqlite3 test.db "SELECT * FROM conversation;"
sqlite3 test.db "SELECT * FROM message;"

# For PostgreSQL
psql your_db_name
\dt  -- List tables
SELECT * FROM conversation;
SELECT * FROM message;
```

### API Documentation

Visit: **http://localhost:8000/docs**

Interactive API docs with try-it-out functionality.

---

## 8. Troubleshooting

### Port Already in Use

```bash
# Kill process on port 8000
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Kill process on port 3000
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Database Connection Error

```bash
# For SQLite, ensure DB file exists
cd Phase-3/backend
ls -la test.db

# For PostgreSQL, check connection
psql -U postgres -h localhost -d phase3 -c "SELECT 1;"
```

### Token Validation Error

```bash
# Regenerate token with correct secret
echo "Check your JWT_SECRET in .env matches code"
python3 -c "import jwt; print(jwt.decode('YOUR_TOKEN', 'your-secret-key-min-32-chars-long', algorithms=['HS256']))"
```

### CORS Errors

```bash
# Ensure CORS_ORIGINS includes your frontend URL
# In backend/.env:
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

---

## 9. Common Commands

### Frontend

```bash
npm run dev          # Start dev server
npm run build        # Build for production
npm run start        # Start production server
npm test             # Run tests
npm run lint         # Lint code
npm run type-check   # Check TypeScript types
```

### Backend

```bash
# Start development server
python -m uvicorn main:app --reload

# Run tests
pytest tests/ -v

# Check code style
black backend/
mypy backend/

# Format code
isort backend/
```

---

## 10. Next Steps

### Local Development

1. Make changes to code
2. Backend auto-reloads on file change
3. Frontend auto-reloads on file change
4. Test in browser at http://localhost:3000/chat

### Deployment

See `Phase-3/SETUP.md` for Docker and Kubernetes deployment.

### API Integration

Frontend already integrated with backend via:
- `src/lib/chat-client.ts` - API client
- `src/hooks/useChat.ts` - React hook for chat
- `src/components/Chat.tsx` - Main chat component

---

## 11. Project Structure

```
Phase-3/
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment template
│   ├── models/                  # Database models
│   ├── agents/                  # Domain agents
│   ├── routes/                  # API routes
│   ├── mcp/                     # MCP tools
│   ├── db/                      # Database setup
│   └── tests/                   # Test suite
│
├── frontend/
│   ├── package.json             # Node dependencies
│   ├── .env.local               # Environment
│   ├── src/
│   │   ├── app/                 # Next.js pages
│   │   ├── components/          # React components
│   │   ├── hooks/               # Custom hooks
│   │   ├── lib/                 # Utilities
│   │   └── styles/              # Global styles
│   ├── __tests__/               # Test suite
│   └── next.config.js           # Next.js config
│
├── SETUP.md                     # Detailed setup guide
├── QUICKSTART.md                # This file
└── specs/                       # Specifications
```

---

## 12. Support

### Documentation
- API Docs: `backend/API.md`
- Tools Docs: `backend/MCP_TOOLS.md`
- Specs: `specs/phase-3-overview.md`

### Logs

Check logs for errors:
```bash
# Backend logs (shown in terminal)
# Frontend logs (F12 developer console)
```

### Getting Help

1. Check error message
2. Review relevant documentation
3. Check logs for stack trace
4. Review GitHub issues
5. Contact team

---

**Ready to go! Start building your todo chatbot! 🚀**

Open http://localhost:3000/chat in your browser and start chatting!
