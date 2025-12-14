# Phase-2: Full-Stack Web Application Specification

**Project**: Hackathon-2 AI-Native Todo System
**Phase**: Phase-2 - Full-Stack Web Application
**Created**: 2025-12-14
**Status**: Specification in Progress
**Version**: 2.0

---

## Executive Summary

Convert the Phase-1 console-based Todo application into a production-ready **full-stack web application**. This phase introduces a persistent database, RESTful API, responsive frontend interface, and user authentication—establishing the foundation for scalability and multi-user collaboration.

**App Topic**:
> An AI-native, specification-driven Task Management System designed to manage personal and professional work across scalable cloud architectures.

---

## Vision & Goals

### Strategic Goals
- Transition from console to production web platform
- Enable multi-user task management with authentication
- Establish API foundation for Phase-3 (AI Chatbot) and Phase-4 (Kubernetes)
- Maintain all Phase-1 features while adding web capabilities
- Set architectural patterns for future cloud-scale evolution

### User Value
- Users can access tasks from any device via web browser
- Secure authentication protects user data
- Real-time task synchronization across devices
- Professional UI/UX experience matching modern web standards

---

## Scope Definition

### In Scope - Phase-2 Delivers
✅ Responsive web frontend (Next.js)
✅ RESTful API backend (FastAPI)
✅ Persistent PostgreSQL database (Neon Serverless)
✅ User authentication (Better Auth + JWT)
✅ All Phase-1 features (Task CRUD) as web interface
✅ Task ownership and multi-user isolation
✅ Specification-Driven Development workflow
✅ Monorepo organization with separate frontend/backend
✅ Docker support for local development
✅ Environment-based configuration (.env)

### Out of Scope - Phase-2 Does NOT Include
❌ AI chatbot functionality (Phase-3)
❌ Kubernetes deployment (Phase-4)
❌ Cloud-scale event streaming (Phase-5)
❌ Real-time WebSocket updates
❌ Advanced analytics or reporting
❌ Mobile native applications
❌ Third-party OAuth providers (only JWT)
❌ Task collaboration/sharing features
❌ File attachments or multimedia

---

## Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Frontend** | Next.js 16+ (App Router) | React-based SSR, modern DX, built-in routing |
| **Backend** | Python FastAPI | Async, modern, Perfect for ML integration (Phase-3) |
| **Database** | Neon Serverless PostgreSQL | Serverless scaling, zero-maintenance |
| **ORM** | SQLModel | Python dataclasses + SQL alchemy hybrid |
| **Authentication** | Better Auth + JWT | Type-safe auth, JWT for stateless API |
| **Styling** | Tailwind CSS | Utility-first, responsive design |
| **Package Manager** | npm (frontend), pip (backend) | Industry standard |
| **Version Control** | Git + GitHub | Existing workflow |
| **Specs** | Spec-Kit + Claude Code | Specification-Driven Development |

---

## User Stories & Scenarios

### User Personas

**1. Working Professional**
- Manages daily tasks and project work
- Accesses tasks from office, home, mobile device
- Needs quick task creation and completion tracking
- Uses email for authentication

**2. Team Lead** (Future - Phase-3)
- Delegates tasks to team members
- Monitors task completion
- Generates reports on productivity

---

### Primary User Scenarios

#### Scenario 1: Signup and Task Creation
```
As a New User:
1. Navigate to todo.app
2. Click "Sign Up"
3. Enter email and password
4. Click "Create Account"
5. Redirected to dashboard
6. See "Create Task" button
7. Enter task title: "Buy groceries"
8. Click "Add Task"
9. Task appears in list with "Pending" status
10. Task persists after page refresh
```

**Acceptance**: User can signup, create task, and see it persisted across sessions

---

#### Scenario 2: Task Management Workflow
```
As an Existing User:
1. Login with email/password
2. See all my tasks (only mine, filtered by user_id)
3. Click "Edit" on task
4. Change title to "Buy organic groceries"
5. Click "Save"
6. Click "Mark Complete" on first task
7. See status change to "Completed"
8. Filter view to show only "Pending" tasks
9. Delete a task
10. Confirm deletion
```

**Acceptance**: All CRUD operations work, data persists, multi-user isolation enforced

---

#### Scenario 3: Secure API Access
```
As Frontend Application:
1. User logs in → Better Auth issues JWT token
2. Store token in secure httpOnly cookie
3. Make API call: GET /api/tasks
4. Include Authorization header: Bearer <jwt_token>
5. Backend verifies JWT signature
6. Backend decodes user_id from token
7. Return only tasks owned by this user_id
8. Token expires after 7 days
9. User must re-login
```

**Acceptance**: JWT authentication prevents cross-user access, stateless and scalable

---

## Functional Requirements

### FR-1: User Authentication
**Description**: Users can signup, login, and logout with email/password credentials.
**Requirements**:
- Sign up with email and password (min 8 characters)
- Login with registered email/password
- Session persists across page refreshes
- Logout clears session and authentication token
- Password reset via email (optional for Phase-2)
- JWT tokens issued by Better Auth
- Tokens stored in secure httpOnly cookies
- Token expiry: 7 days

**Acceptance Criteria**:
- [ ] User can create account with valid email
- [ ] User can login with correct credentials
- [ ] Login fails with incorrect password
- [ ] User stays logged in after page refresh
- [ ] JWT token in Authorization header on API calls
- [ ] Unauthorized requests return 401 status

---

### FR-2: Task CRUD Operations
**Description**: All Phase-1 operations (Add, List, Update, Delete, Mark Complete) available via web UI and API.

**Requirements**:
- Create task with title (required) and description (optional)
- List all tasks for authenticated user
- Update task title/description
- Delete task permanently
- Mark task complete/incomplete (toggle)
- Tasks display: ID, Title, Description, Status, CreatedAt, UpdatedAt
- Each task owned by single user
- Only task owner can modify their tasks

**Acceptance Criteria**:
- [ ] Create task: POST /api/tasks → 201 Created
- [ ] List tasks: GET /api/tasks → 200 OK, filtered by user_id
- [ ] Update task: PUT /api/tasks/{id} → 200 OK
- [ ] Delete task: DELETE /api/tasks/{id} → 204 No Content
- [ ] Toggle complete: PATCH /api/tasks/{id}/complete → 200 OK
- [ ] Attempt to modify other user's task → 403 Forbidden

---

### FR-3: Task Persistence
**Description**: All task data persists in PostgreSQL database.

**Requirements**:
- Tasks stored in `tasks` table with user_id foreign key
- Each task has unique auto-incrementing ID
- Timestamps: created_at, updated_at (auto-managed)
- Status values: "Pending" or "Completed"
- Database connection via SQLModel ORM
- Connection pooling for performance

**Acceptance Criteria**:
- [ ] Task created via API stored in database
- [ ] Task exists after app restart
- [ ] Timestamps automatically set and updated
- [ ] Database indexes on user_id for fast queries
- [ ] No orphaned tasks without user_id

---

### FR-4: Multi-User Isolation
**Description**: Each user sees and modifies only their own tasks.

**Requirements**:
- JWT token contains user_id
- All API queries filtered by user_id
- No way to access other user's tasks via API
- Frontend cannot display tasks from other users
- Database queries use user_id in WHERE clause

**Acceptance Criteria**:
- [ ] User A cannot see User B's tasks
- [ ] API enforces user_id on every operation
- [ ] Attempting to modify other user's task returns 403
- [ ] No data leakage between users

---

### FR-5: Responsive Web Interface
**Description**: Professional, mobile-friendly UI using Next.js and Tailwind CSS.

**Requirements**:
- Dashboard displays task list
- Create task form
- Edit task modal
- Delete confirmation dialog
- Task status toggle
- Filter tasks by status (All/Pending/Completed)
- Search tasks by title
- Mobile responsive (works on phone, tablet, desktop)
- Loading states and error messages
- Clean, modern design

**Acceptance Criteria**:
- [ ] UI renders correctly on mobile (320px), tablet (768px), desktop (1024px+)
- [ ] All operations have feedback (loading spinners, success messages)
- [ ] Error messages are user-friendly
- [ ] Page loads in under 3 seconds
- [ ] No horizontal scrolling on mobile

---

### FR-6: RESTful API Endpoints
**Description**: Backend exposes standard REST API for all task operations.

**Endpoints**:
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | /api/tasks | List all user's tasks | JWT |
| POST | /api/tasks | Create new task | JWT |
| GET | /api/tasks/{id} | Get task details | JWT |
| PUT | /api/tasks/{id} | Update task | JWT |
| DELETE | /api/tasks/{id} | Delete task | JWT |
| PATCH | /api/tasks/{id}/complete | Toggle task completion | JWT |

**Acceptance Criteria**:
- [ ] All endpoints require valid JWT in Authorization header
- [ ] Requests without token return 401 Unauthorized
- [ ] All responses return appropriate HTTP status codes
- [ ] API returns JSON with consistent structure
- [ ] Error responses include error message and error_code

---

## Success Criteria

### SC-1: Full Feature Parity
✅ All Phase-1 features (Add/List/Update/Delete/Mark Complete) work in web UI
✅ API endpoints match Phase-1 functionality

---

### SC-2: Authentication & Security
✅ User registration and login working
✅ JWT tokens issued and verified
✅ Users cannot access other users' tasks
✅ All API endpoints require authentication
✅ Tokens expire after 7 days

---

### SC-3: Data Persistence
✅ All tasks stored in PostgreSQL
✅ Tasks survive application restart
✅ Database integrity maintained (no orphaned tasks)
✅ Timestamps automatically managed

---

### SC-4: User Experience
✅ Frontend loads in under 3 seconds
✅ UI is responsive on all device sizes
✅ Users receive clear feedback (success/error messages)
✅ Signup-to-first-task flow completes in under 2 minutes

---

### SC-5: Code Quality
✅ 100% of Phase-2 requirements tested
✅ Code follows established patterns (separate frontend/backend)
✅ API documentation complete (OpenAPI/Swagger)
✅ Database schema documented

---

### SC-6: Specification Compliance
✅ Implementation matches this specification
✅ No unplanned features added
✅ All edge cases handled gracefully

---

## Key Entities & Data Models

### User (Managed by Better Auth)
```
id: string (primary key, managed by Better Auth)
email: string (unique, required)
name: string (optional)
created_at: timestamp
updated_at: timestamp
```

### Task
```
id: integer (auto-increment primary key)
user_id: string (foreign key → User.id)
title: string (required, 1-200 characters)
description: text (optional, max 1000 characters)
status: enum ("Pending" | "Completed") - default "Pending"
created_at: timestamp (auto-set)
updated_at: timestamp (auto-update)
```

**Relationships**:
- One User → Many Tasks
- Delete User → Cascade delete all Tasks

---

## API Request/Response Formats

### Authentication
**Request**:
```json
POST /api/auth/signup
{
  "email": "user@example.com",
  "password": "securepass123"
}
```

**Response** (201 Created):
```json
{
  "user_id": "user_123",
  "email": "user@example.com",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 604800
}
```

---

### Create Task
**Request**:
```json
POST /api/tasks
Authorization: Bearer <jwt_token>

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "user_id": "user_123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "Pending",
  "created_at": "2025-12-14T10:00:00Z",
  "updated_at": "2025-12-14T10:00:00Z"
}
```

---

### List Tasks
**Request**:
```
GET /api/tasks?status=pending&sort=created
Authorization: Bearer <jwt_token>
```

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": 1,
      "title": "Buy groceries",
      "status": "Pending",
      "created_at": "2025-12-14T10:00:00Z"
    }
  ],
  "count": 1,
  "total": 1
}
```

---

### Error Response
**Status**: 400/401/403/500

```json
{
  "error_code": "UNAUTHORIZED",
  "message": "Invalid or expired token",
  "details": {}
}
```

---

## Technical Architecture

### Monorepo Structure
```
hackathon-2/
├── .spec-kit/
│   └── config.yaml                 # Spec-Kit configuration
├── specs/                           # Specifications (Spec-Kit managed)
│   ├── phase-2-overview.md         # This file
│   ├── features/
│   │   ├── task-crud-web.md
│   │   └── authentication.md
│   ├── api/
│   │   └── rest-endpoints.md
│   ├── database/
│   │   └── schema.md
│   └── ui/
│       └── components.md
├── history/prompts/phase-2/        # Prompt history records
├── frontend/                        # Next.js application
│   ├── CLAUDE.md
│   ├── app/                        # Next.js 13+ App Router
│   ├── components/
│   ├── lib/
│   └── package.json
├── backend/                         # FastAPI application
│   ├── CLAUDE.md
│   ├── main.py
│   ├── models.py
│   ├── routes/
│   ├── db.py
│   └── requirements.txt
├── hafiz-naveed/                   # Phase-1 (preserved)
├── docker-compose.yml              # Local development
├── CLAUDE.md                        # Root instructions
└── README.md
```

---

## Assumptions & Dependencies

### Assumptions
- Users have valid email addresses
- Passwords are at least 8 characters (validated on signup)
- PostgreSQL connection via environment variable DATABASE_URL
- Better Auth secret key shared between frontend/backend via BETTER_AUTH_SECRET
- Development environment uses localhost:3000 (frontend), localhost:8000 (backend)
- Users understand basic web application workflows

### External Dependencies
- Neon Serverless PostgreSQL (cloud database)
- Better Auth library (authentication provider)
- Next.js ecosystem (React, Node.js)
- FastAPI ecosystem (Python 3.8+)
- Docker (optional, for local development)

### Internal Dependencies
- Phase-1 specification and architecture patterns
- Project constitution and governance
- Existing Git workflow and repository

---

## Non-Functional Requirements

### Performance
- Page load time: < 3 seconds (initial)
- API response time: < 500ms (p95)
- List tasks: < 100ms for 10,000 tasks
- Authentication: < 1 second (JWT validation)

### Reliability
- 99.5% uptime SLO (during beta)
- Graceful error handling with user-friendly messages
- Database transaction rollback on failures
- Automatic token refresh before expiration

### Security
- HTTPS only (in production)
- JWT tokens in httpOnly cookies (XSS protection)
- CORS properly configured
- SQL injection prevention (via ORM)
- Password hashing (handled by Better Auth)
- Input validation on all endpoints

### Scalability
- Support 1,000 concurrent users (Phase-2 target)
- Scale to 10,000 tasks per user
- Horizontal scaling via stateless API

---

## Testing Strategy

### Unit Tests
- Authentication logic
- JWT validation
- Task model validators
- API route handlers

### Integration Tests
- Signup → Create Task → List Tasks workflow
- Multi-user isolation
- Database persistence
- API endpoint behavior

### End-to-End Tests
- Complete user journey (signup to task completion)
- Cross-browser compatibility
- Mobile responsiveness

---

## Deployment & Release

### Local Development
```bash
docker-compose up
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Database: postgresql://localhost:5432
```

### Environment Variables
```
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth

# Backend (.env)
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your_secret_key
JWT_EXPIRY_DAYS=7
```

---

## Risks & Mitigations

### Risk 1: JWT Token Management Complexity
**Impact**: Authentication failures, security vulnerabilities
**Mitigation**: Use Better Auth library (battle-tested), document token flow clearly

### Risk 2: Cross-User Data Leakage
**Impact**: Privacy breach, data violation
**Mitigation**: Enforce user_id filtering on every query, add integration tests

### Risk 3: Database Connection Pool Exhaustion
**Impact**: Performance degradation, connection timeouts
**Mitigation**: Configure connection pooling, monitor metrics, implement retry logic

---

## Success Measurement

| Metric | Target | Measurement |
|--------|--------|-------------|
| Feature Completeness | 100% | All FRs implemented and tested |
| Code Coverage | ≥ 80% | Unit + Integration tests |
| Performance | < 3s page load | Lighthouse/WebPageTest |
| Security | 0 Critical CVEs | Dependency scanning |
| User Satisfaction | ≥ 4/5 | Manual testing feedback |

---

## Next Steps (Phase-3 Preview)

Phase-3 will enhance Phase-2 with:
- AI Chatbot integration (Claude API)
- Natural language task creation
- Smart task suggestions
- Chat-based task management

Phase-2 must provide:
- Stable, well-documented API
- User-agnostic backend (ready for new features)
- Strong authentication foundation

---

**Status**: ✅ Specification Complete - Ready for Planning Phase

**Document Metadata**:
- Created: 2025-12-14
- Last Updated: 2025-12-14
- Version: 2.0
- Phase: Phase-2 (Full-Stack Web Application)
- Next: `/sp.plan` or `/sp.clarify`
