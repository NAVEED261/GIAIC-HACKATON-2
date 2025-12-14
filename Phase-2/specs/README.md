# Hackathon-2 Specifications

**Phase-2**: Full-Stack Web Application Specification

This directory contains all specifications for Phase-2 of the Hackathon-2 project, organized using Spec-Kit.

---

## Quick Start

### Read the Phase-2 Specification
```bash
cat phase-2-overview.md
```

### Structure

```
specs/
├── README.md                          # This file
├── phase-2-overview.md                # Main Phase-2 specification (Read this first!)
├── features/                          # Feature specifications
│   ├── task-crud-web.md              # Web-based CRUD operations
│   ├── authentication.md               # User authentication with Better Auth + JWT
│   └── api-integration.md              # API integration patterns
├── api/                                # API documentation
│   └── rest-endpoints.md               # RESTful API specifications
├── database/                           # Database design
│   └── schema.md                       # PostgreSQL schema and relationships
└── ui/                                 # UI/UX specifications
    └── components.md                   # React component specifications
```

---

## How to Use Specs

### 1. Before Implementing Any Feature

**Read the specification**:
```bash
cat specs/phase-2-overview.md
```

### 2. For Specific Features

**Task CRUD Web**:
```bash
cat specs/features/task-crud-web.md
```

**Authentication**:
```bash
cat specs/features/authentication.md
```

### 3. Reference Specs in Code

When implementing, reference the spec:
```python
# Implements @specs/features/authentication.md - User signup
@app.post("/api/auth/signup")
def signup(user: UserSignup):
    ...
```

### 4. If Specs Are Unclear

Use the `/sp.clarify` command:
```bash
/sp.clarify
```

---

## Phase-2 Overview

### What is Phase-2?

Convert the Phase-1 console-based Todo application into a production-ready **full-stack web application**.

### Key Features

✅ Responsive web frontend (Next.js 16+)
✅ RESTful API backend (Python FastAPI)
✅ Persistent database (Neon Serverless PostgreSQL)
✅ User authentication (Better Auth + JWT)
✅ Multi-user task isolation
✅ All Phase-1 features (Task CRUD)

### Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 16+ (App Router) |
| **Backend** | Python FastAPI |
| **Database** | Neon Serverless PostgreSQL |
| **ORM** | SQLModel |
| **Authentication** | Better Auth + JWT |
| **Styling** | Tailwind CSS |

---

## Implementation Status

### Specifications
- ✅ Phase-2 overview complete
- ⏳ Feature specs (coming)
- ⏳ API specs (coming)
- ⏳ Database specs (coming)
- ⏳ UI specs (coming)

### Implementation
- ⏳ Backend setup
- ⏳ Frontend setup
- ⏳ Authentication
- ⏳ API endpoints
- ⏳ UI components
- ⏳ Testing

---

## Key Decisions

### 1. Monorepo Structure
**Decision**: Single repository with `frontend/` and `backend/` separation
**Why**: Shared specs, coordinated releases, easier to maintain

### 2. JWT Authentication
**Decision**: Use JWT tokens issued by Better Auth
**Why**: Stateless, scalable, works across services

### 3. SQLModel ORM
**Decision**: Use SQLModel (Pydantic + SQLAlchemy)
**Why**: Type-safe, modern Python, API validation

---

## Next Steps

1. **Read** `phase-2-overview.md` (main specification)
2. **Review** technology stack and architecture
3. **Create** detailed feature specs in `features/`
4. **Document** API design in `api/`
5. **Define** database schema in `database/`
6. **Specify** UI components in `ui/`
7. **Use `/sp.plan`** to generate implementation plan
8. **Use `/sp.tasks`** to create action items

---

## Spec-Kit Configuration

Spec-Kit is configured in `.spec-kit/config.yaml`:

```yaml
name: hackathon-2-phase-2
version: "2.0"
structure:
  specs_dir: specs
  features_dir: specs/features
  api_dir: specs/api
  database_dir: specs/database
  ui_dir: specs/ui
```

This ensures:
- Organized specs by type
- Clear separation of concerns
- Easy reference from code comments
- Scalable for future phases

---

## Useful Commands

### View Specs
```bash
cat specs/phase-2-overview.md          # Main spec
cat specs/features/[feature].md        # Feature spec
cat specs/api/rest-endpoints.md        # API spec
```

### Create/Update Specs
```bash
/sp.specify "Feature description"      # Create/update spec
/sp.clarify                            # Clarify unclear requirements
```

### Plan Implementation
```bash
/sp.plan                               # Generate implementation plan
/sp.tasks                              # Generate action tasks
```

### Record Decisions
```bash
/sp.adr "Decision Title"               # Create architecture decision record
```

---

## Important Notes

### ⚠️ Specifications are Authoritative
- Always implement **from specs**, not from assumptions
- If specs are unclear, use `/sp.clarify` to refine them
- Update specs if requirements change
- Specs are living documents

### 🔒 No Implementation Details
- Specs describe **WHAT** not **HOW**
- No framework-specific code in specs
- No database implementation details
- Focus on user value and behavior

### 📝 Reference Specs in Code
```python
# ✅ Good
# Implements @specs/features/authentication.md - User signup

# ❌ Bad
# FastAPI route for user signup
```

---

## Questions?

1. **Read the spec first** - most answers are there
2. **Check related specs** - features, API, database often explain context
3. **Use `/sp.clarify`** - for ambiguous requirements
4. **Check CLAUDE.md** - for development workflow

---

**Phase-2 Status**: 🔄 **In Specification** → Planning → Implementation

Next: Read `phase-2-overview.md` and use `/sp.plan` to start!

🤖 Specification-Driven Development with Spec-Kit + Claude Code
