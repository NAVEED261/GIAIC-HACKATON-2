# Hackathon-2: AI-Native Todo System
## Specification-Driven Development with Spec-Kit + Claude Code

**Project**: Hackathon-2 - Evolution of a Todo System across 5 phases
**Current Phase**: Phase-2 (Full-Stack Web Application)
**Repository**: https://github.com/NAVEED261/GIAIC-HACKATON-2
**Status**: Phase-1 Complete ✅ | Phase-2 In Specification

---

## Project Vision

This is a reference model for **Specification-Driven Development (SDD)** and **AI-Assisted Software Engineering**. The system evolves continuously across five phases without breaking changes, starting from a console application to a cloud-scale, event-driven system.

### Five Evolutionary Phases

1. **Phase-1**: Console-based Todo (Python, in-memory) ✅ **COMPLETE**
2. **Phase-2**: Full-stack Web Todo (Next.js + FastAPI + PostgreSQL) 🔄 **IN PROGRESS**
3. **Phase-3**: AI Chatbot Todo (Claude AI + MCP integration) 📋 **PLANNED**
4. **Phase-4**: Kubernetes Deployment (Docker, Helm, Minikube) 📋 **PLANNED**
5. **Phase-5**: Cloud-scale System (Kafka, Dapr, advanced features) 📋 **PLANNED**

---

## Spec-Kit Structure

Specifications are organized in `/specs` and managed by Spec-Kit for clarity and consistency:

### Directory Organization
```
specs/
├── phase-2-overview.md              # Phase-2 complete specification
├── features/                         # Feature specifications
│   ├── task-crud-web.md            # Web-based CRUD operations
│   ├── authentication.md             # User auth with Better Auth + JWT
│   └── api-integration.md            # RESTful API design
├── api/                              # API documentation
│   └── rest-endpoints.md             # Endpoint specifications
├── database/                         # Database design
│   └── schema.md                     # PostgreSQL schema
└── ui/                               # UI/UX specifications
    └── components.md                 # React component specs
```

### How to Use Specs
1. **Always read relevant spec before implementing**
   - Feature spec: `@specs/features/[feature-name].md`
   - API spec: `@specs/api/rest-endpoints.md`
   - Database spec: `@specs/database/schema.md`

2. **Reference specs in code comments**:
   ```python
   # Implements @specs/features/authentication.md - User signup
   @app.post("/api/auth/signup")
   ```

3. **Update specs if requirements change**
   - All specs are living documents
   - Changes must be reflected back to specs
   - Maintain specification-first philosophy

---

## Monorepo Organization

### Root Structure
```
hackathon-2/
├── Phase-1/                           # Phase-1 Console App (Complete ✅)
│   ├── hafiz-naveed/
│   │   ├── src/                       # Source code (402 lines)
│   │   ├── tests/                     # Tests (621 lines, 53 tests)
│   │   ├── docs/                      # Documentation
│   │   ├── phase-1/                   # Specification
│   │   └── README.md                  # Phase-1 quick start
│   └── README.md                      # Phase-1 overview
│
├── Phase-2/                           # Phase-2 Full-Stack Web (In Progress 🔄)
│   ├── .spec-kit/                     # Spec-Kit configuration
│   ├── specs/                         # Specifications
│   │   ├── phase-2-overview.md       # Main spec (639 lines)
│   │   ├── features/                  # Feature specs
│   │   ├── api/                       # API specs
│   │   ├── database/                  # Database specs
│   │   └── ui/                        # UI specs
│   ├── frontend/                      # Next.js 16+ (to be created)
│   ├── backend/                       # FastAPI (to be created)
│   ├── docker-compose.yml             # Local development
│   └── README.md                      # Phase-2 quick start
│
├── Phase-3/                           # Phase-3 AI Chatbot (Planned 📋)
│   └── README.md                      # Phase-3 placeholder
│
├── Phase-4/                           # Phase-4 Kubernetes (Planned 📋)
│   └── README.md                      # Phase-4 placeholder
│
├── Phase-5/                           # Phase-5 Cloud-Scale (Planned 📋)
│   └── README.md                      # Phase-5 placeholder
│
├── history/prompts/                   # Prompt History Records (PHRs)
│   ├── phase-1/                       # Phase-1 PHRs
│   └── phase-2/                       # Phase-2 PHRs
│
├── CLAUDE.md                          # This file (root instructions)
├── README.md                          # Project overview
└── .gitignore                         # Git ignore patterns
```

### Phase Isolation (Spec-Kit SDD Approach)
- **Phase-1** in `Phase-1/` folder (complete, separate environment)
- **Phase-2** in `Phase-2/` folder (in progress, separate environment)
- **Phases 3-5** follow same pattern: each phase is separate folder
- **Shared**: Git repository, specifications philosophy, architecture patterns
- **Benefits**: Clear organization, local visibility, easy multi-phase work

---

## Development Workflow

### 1. Before Implementing Any Feature

**Step 1**: Read the specification
```bash
cat specs/[feature-area]/[feature-name].md
```

**Step 2**: Check related specs
- API spec: `specs/api/rest-endpoints.md`
- Database spec: `specs/database/schema.md`
- If unclear, use `/sp.clarify` command

---

### 2. Implementation Branches

Create feature branches per spec:
```bash
git checkout -b feature/[feature-name]
```

Example:
```bash
git checkout -b feature/task-crud-web
git checkout -b feature/better-auth-integration
```

---

### 3. Backend Implementation

Navigate to backend and read `backend/CLAUDE.md`:
```bash
cd backend
# Read implementation guidelines
cat CLAUDE.md
```

**What you'll implement**:
- `models.py` - SQLModel data models (User, Task)
- `routes/tasks.py` - Task CRUD endpoints
- `routes/auth.py` - Authentication endpoints
- `db.py` - Database connection and setup
- `main.py` - FastAPI application setup
- `tests/` - Unit and integration tests

---

### 4. Frontend Implementation

Navigate to frontend and read `frontend/CLAUDE.md`:
```bash
cd ../frontend
# Read implementation guidelines
cat CLAUDE.md
```

**What you'll implement**:
- `app/` - Next.js pages (dashboard, login, etc.)
- `components/` - React components (TaskList, TaskForm, etc.)
- `lib/` - API client, utilities
- `styles/` - Tailwind CSS
- `tests/` - Component and integration tests

---

### 5. Testing & Validation

**Backend**:
```bash
cd backend
pytest tests/ -v --cov
```

**Frontend**:
```bash
cd frontend
npm test
npm run build
```

---

## Spec-Kit Commands for Claude Code

### Create or Update Specs
```bash
/sp.specify "Feature description"
```

Creates/updates specs and generates a specification plan.

### Plan Implementation
```bash
/sp.plan
```

Generates step-by-step implementation tasks based on specs.

### Generate Tasks
```bash
/sp.tasks
```

Creates actionable, dependency-ordered tasks.

### Record Decisions (ADRs)
```bash
/sp.adr "Architecture Decision Title"
```

Documents significant architectural decisions.

### Create Prompt History Record
```bash
/sp.phr
```

Records conversations for learning and traceability.

---

## Tech Stack Rationale

| Layer | Technology | Why? |
|-------|-----------|------|
| **Frontend** | Next.js 16+ | React-based, SSR, modern DX, built-in routing |
| **Backend** | FastAPI | Async Python, modern, perfect for ML (Phase-3) |
| **Database** | Neon Serverless PostgreSQL | Serverless scaling, zero-maintenance |
| **ORM** | SQLModel | Python type hints + SQL Alchemy |
| **Auth** | Better Auth + JWT | Type-safe, stateless, scalable |
| **Styling** | Tailwind CSS | Utility-first, responsive |
| **Specs** | Spec-Kit + Claude Code | Specification-first development |

---

## Key Architectural Decisions

### 1. Monorepo Organization
**Decision**: Single repository with frontend/backend separation
**Reasoning**: Shared specs, coordinated releases, easier to maintain
**Alternative**: Separate repos (rejected - harder coordination)

### 2. JWT for API Authentication
**Decision**: Use JWT tokens issued by Better Auth
**Reasoning**: Stateless, scalable, works across services
**Alternative**: Session-based auth (rejected - not scalable)

### 3. SQLModel for ORM
**Decision**: Use SQLModel (Pydantic + SQLAlchemy)
**Reasoning**: Type-safe, modern Python, API validation
**Alternative**: Raw SQL (rejected - less maintainable)

---

## Environment Setup

### Prerequisites
- Node.js 18+ (frontend)
- Python 3.8+ (backend)
- PostgreSQL 13+ (or Neon Serverless)
- Docker & Docker Compose (optional)
- Git

### Local Development

**1. Clone Repository**:
```bash
git clone https://github.com/NAVEED261/GIAIC-HACKATON-2.git
cd GIAIC-HACKATON-2
```

**2. Create Environment Files**:

**frontend/.env.local**:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
```

**backend/.env**:
```
DATABASE_URL=postgresql://user:password@localhost:5432/hackathon2
BETTER_AUTH_SECRET=your_dev_secret_key_min_32_chars
JWT_EXPIRY_DAYS=7
```

**3. Start with Docker Compose**:
```bash
docker-compose up
```

Or manually:

**Backend**:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

---

## Testing Strategy

### Backend Tests
```bash
cd backend

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test
pytest tests/test_auth.py -v
```

### Frontend Tests
```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Build for production
npm run build
```

---

## Code Review Checklist

Before committing, verify:

- ✅ Implementation matches spec
- ✅ No implementation details in specs
- ✅ Tests pass (100% for new code)
- ✅ No hardcoded secrets (use .env)
- ✅ Code follows project patterns
- ✅ Database migrations applied
- ✅ API documented (docstrings/OpenAPI)
- ✅ Commit message is semantic (feat:, fix:, docs:, etc.)

---

## Useful Commands

### Git
```bash
# Create feature branch
git checkout -b feature/[name]

# Push branch and create PR
git push origin feature/[name]

# Merge PR (GitHub)
gh pr merge [number] --squash
```

### Backend
```bash
# Format code
black backend/

# Check types
mypy backend/

# Run migrations
alembic upgrade head

# Start dev server
uvicorn main:app --reload
```

### Frontend
```bash
# Format code
npm run format

# Check types
npm run type-check

# Start dev server
npm run dev

# Build for production
npm run build
```

### Spec-Kit
```bash
# View spec
cat specs/phase-2-overview.md

# Create new feature spec
/sp.specify "Feature description"

# Generate implementation plan
/sp.plan
```

---

## Important Notes

### ⚠️ Keep Specs Authoritative
- Always implement from specs
- If unclear, clarify specs first (don't invent solutions)
- Update specs if requirements change
- Specs are living documents

### 🔒 Security Practices
- Never commit `.env` files
- Use environment variables for secrets
- Validate all user input
- Use SQLModel to prevent SQL injection
- JWT tokens in httpOnly cookies (XSS protection)

### 📝 Documentation
- Code comments reference specs: `# @specs/features/...`
- API endpoints have docstrings
- Database schema documented in `specs/database/schema.md`
- Deployment guide in README.md

### 🧪 Testing
- New code requires tests
- Aim for ≥80% coverage
- Integration tests for API endpoints
- Component tests for UI

---

## Phase-2 Checklist

- [ ] Spec complete and reviewed
- [ ] Monorepo structure created
- [ ] `.spec-kit/config.yaml` set up
- [ ] `frontend/CLAUDE.md` created
- [ ] `backend/CLAUDE.md` created
- [ ] Backend implementation started
- [ ] Frontend implementation started
- [ ] Authentication working
- [ ] Database persistence confirmed
- [ ] Multi-user isolation tested
- [ ] API documentation complete
- [ ] 100% test coverage
- [ ] PR merged to master
- [ ] Phase-2 complete!

---

## Getting Help

### Documentation
- **Specs**: `/specs` directory
- **Phase-1**: `hafiz-naveed/README.md`
- **Phase-2 Plan**: Use `/sp.plan` command
- **Architecture**: `/sp.adr` decisions

### Commands
- **Understanding features**: `/sp.clarify`
- **Planning implementation**: `/sp.plan`
- **Recording decisions**: `/sp.adr`
- **Creating tasks**: `/sp.tasks`

### Questions
- Refer to spec first
- Check existing code patterns
- Use `/sp.clarify` if spec is ambiguous
- Ask in commit messages if needed

---

**Status**: ✅ Phase-1 Complete | 🔄 Phase-2 In Progress

Next: Read `specs/phase-2-overview.md` and use `/sp.plan` to start implementation!

🤖 **Specification-Driven Development** with **Claude Code** + **Spec-Kit**
