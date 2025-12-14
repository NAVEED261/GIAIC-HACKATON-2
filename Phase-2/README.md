# Phase-2: Full-Stack Web Application

**Status**: 🔄 **IN SPECIFICATION** → Planning → Implementation

This folder contains Phase-2 of the Hackathon-2 project - converting Phase-1 console app into a production-ready full-stack web application.

## Quick Start

See `specs/phase-2-overview.md` for complete specification.

```bash
# Read specification
cat specs/phase-2-overview.md

# View Spec-Kit config
cat .spec-kit/config.yaml

# Navigate specs
cat specs/README.md
```

## What's Inside

```
Phase-2/
├── .spec-kit/                         # Spec-Kit configuration
│   └── config.yaml                    # Phase-2 structure definition
│
├── specs/                             # Specifications (Spec-Kit managed)
│   ├── phase-2-overview.md           # Main Phase-2 spec (639 lines)
│   ├── README.md                      # Specs navigation guide
│   ├── features/                      # Feature specifications
│   │   ├── task-crud-web.md          # Web-based CRUD operations
│   │   ├── authentication.md          # User auth with Better Auth + JWT
│   │   └── api-integration.md         # API integration patterns
│   ├── api/                           # API documentation
│   │   └── rest-endpoints.md          # RESTful API specs
│   ├── database/                      # Database design
│   │   └── schema.md                  # PostgreSQL schema
│   └── ui/                            # UI specifications
│       └── components.md              # React component specs
│
├── frontend/                          # Next.js 16+ (coming soon)
│   └── README.md                      # Frontend setup guide
│
├── backend/                           # FastAPI (coming soon)
│   └── README.md                      # Backend setup guide
│
├── docker-compose.yml                 # Local development (coming soon)
├── .env.example                       # Environment variables template
└── README.md                          # This file
```

## Phase-2 Vision

Convert Phase-1 CLI todo system into a **production-ready full-stack web application** with:
- ✅ Responsive web frontend (Next.js)
- ✅ RESTful API backend (FastAPI)
- ✅ Persistent database (PostgreSQL)
- ✅ User authentication (Better Auth + JWT)
- ✅ Multi-user isolation
- ✅ Professional UI/UX
- ✅ Comprehensive testing
- ✅ Specification-Driven Development

## Technology Stack

| Layer | Technology | Why? |
|-------|-----------|------|
| **Frontend** | Next.js 16+ (App Router) | SSR, modern DX, built-in routing |
| **Backend** | Python FastAPI | Async, modern, ML-ready for Phase-3 |
| **Database** | Neon Serverless PostgreSQL | Serverless, zero-maintenance |
| **ORM** | SQLModel | Type-safe, hybrid ORM |
| **Authentication** | Better Auth + JWT | Stateless, scalable |
| **Styling** | Tailwind CSS | Utility-first, responsive |

## Phase-2 Features

### FR-1: User Authentication
- Sign up with email/password
- Login/logout
- JWT token management
- 7-day token expiry
- Secure httpOnly cookies

### FR-2: Task CRUD Operations
- Create tasks (title + description)
- List user's tasks
- Update task details
- Delete tasks
- Mark tasks complete

### FR-3: Task Persistence
- PostgreSQL storage
- Auto-increment IDs
- Automatic timestamps
- Foreign key relationships

### FR-4: Multi-User Isolation
- JWT contains user_id
- All queries filtered by user
- No cross-user access
- 403 Forbidden on violation

### FR-5: Responsive Web UI
- Mobile/tablet/desktop responsive
- Task dashboard
- Create/edit forms
- Filter and search
- Loading states and errors

### FR-6: RESTful API
- GET /api/tasks (list)
- POST /api/tasks (create)
- GET /api/tasks/{id} (detail)
- PUT /api/tasks/{id} (update)
- DELETE /api/tasks/{id} (delete)
- PATCH /api/tasks/{id}/complete (toggle)

## Success Criteria

| SC | Criterion |
|----|-----------|
| SC-1 | Feature parity with Phase-1 ✅ |
| SC-2 | Authentication & security ✅ |
| SC-3 | Data persistence ✅ |
| SC-4 | User experience ✅ |
| SC-5 | Code quality ✅ |
| SC-6 | Specification compliance ✅ |

## Development Status

### Specifications
- ✅ Phase-2 overview complete (639 lines)
- ⏳ Feature specs (coming)
- ⏳ API specs (coming)
- ⏳ Database specs (coming)
- ⏳ UI specs (coming)

### Implementation
- ⏳ Backend setup
- ⏳ Frontend setup
- ⏳ Authentication integration
- ⏳ API endpoints
- ⏳ Database schema
- ⏳ UI components
- ⏳ Testing

## How to Use Specs

### 1. Read Main Specification
```bash
cat specs/phase-2-overview.md
```

### 2. Understand Project Organization
```bash
cat specs/README.md
```

### 3. For Specific Features
```bash
cat specs/features/task-crud-web.md
cat specs/features/authentication.md
```

### 4. For API Design
```bash
cat specs/api/rest-endpoints.md
```

### 5. For Database Schema
```bash
cat specs/database/schema.md
```

### 6. For UI Components
```bash
cat specs/ui/components.md
```

## Key Specifications

### Monorepo Organization
- Single repository with `frontend/` and `backend/`
- Shared `/specs` with Spec-Kit
- Clear separation of concerns
- Coordinated releases

### JWT Authentication
- Better Auth issues JWT tokens
- Frontend attaches token to API requests
- Backend verifies JWT signature
- Stateless and scalable

### SQLModel ORM
- Type-safe database models
- Pydantic integration
- SQLAlchemy power
- Clean Python code

## Development Workflow

### 1. Read Spec First
Always start with `specs/phase-2-overview.md`

### 2. Create Feature Branch
```bash
git checkout -b feature/phase-2-task-crud
```

### 3. Implement Backend
```bash
cd backend
# Read backend/CLAUDE.md for guidelines
# Implement routes, models, tests
```

### 4. Implement Frontend
```bash
cd ../frontend
# Read frontend/CLAUDE.md for guidelines
# Implement components, pages, tests
```

### 5. Test & Validate
```bash
# Backend tests
pytest tests/ -v

# Frontend tests
npm test
```

### 6. Commit & Push
```bash
git add .
git commit -m "feat(phase-2): implement task CRUD operations"
git push origin feature/phase-2-task-crud
```

### 7. Create PR & Review
Pull request on GitHub for code review

## Next Steps

1. **Now**: Read `specs/phase-2-overview.md`
2. **Then**: Use `/sp.plan` to generate implementation plan
3. **Then**: Use `/sp.tasks` to create action tasks
4. **Then**: Create feature branches for implementation
5. **Then**: Implement backend and frontend
6. **Then**: Testing and validation
7. **Then**: Merge to master
8. **Finally**: Start Phase-3

## Specification Compliance

Phase-2 is designed following **Specification-Driven Development (SDD)** principles:
- ✅ Complete specification before implementation
- ✅ No implementation details in specs
- ✅ Technology-agnostic requirements
- ✅ Clear success criteria
- ✅ Testable acceptance criteria
- ✅ Living specifications (update if requirements change)

## Important Notes

### ⚠️ Specifications are Authoritative
- Always implement **from specs**, not assumptions
- If unclear, use `/sp.clarify` to refine
- Update specs if requirements change
- Specs are living documents

### 🔒 Security Practices
- Never commit `.env` files
- Use environment variables for secrets
- Validate all user input
- Use SQLModel to prevent SQL injection
- JWT tokens in httpOnly cookies

### 📝 Documentation
- Code comments reference specs: `# @specs/features/...`
- API endpoints have docstrings
- Database schema in specs
- Deployment in README

### 🧪 Testing
- New code requires tests
- Aim for ≥80% coverage
- Integration tests for APIs
- Component tests for UI

## Quick Links

- **Main Spec**: `specs/phase-2-overview.md`
- **Specs Guide**: `specs/README.md`
- **Root Guide**: `../CLAUDE.md`
- **Phase-1**: `../Phase-1/README.md`

## Git Information

- **Branch**: `feature/phase-2-web-app`
- **Repository**: https://github.com/NAVEED261/GIAIC-HACKATON-2
- **Status**: In Specification

---

**Phase-2 Status**: 🔄 In Specification → Planning → Implementation

**Next**: Read `specs/phase-2-overview.md` and use `/sp.plan` or `/sp.clarify`!

🤖 Specification-Driven Development with Spec-Kit + Claude Code
