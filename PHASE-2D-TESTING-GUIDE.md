# Phase 2D: Comprehensive Testing Guide

**Phase:** 2D Testing
**Status:** Ready to implement
**Overall Progress:** Ready for testing (100% code complete)
**Estimated Coverage Target:** 80%+

---

## 📋 Table of Contents

1. [Testing Overview](#testing-overview)
2. [Backend Testing Guide](#backend-testing-guide)
3. [Frontend Testing Guide](#frontend-testing-guide)
4. [Testing Tools & Setup](#testing-tools--setup)
5. [How to Run Tests](#how-to-run-tests)
6. [Expected Test Results](#expected-test-results)

---

## 🎯 Testing Overview

### Types of Testing

**1. Unit Tests**
- Test individual functions/components in isolation
- Mock external dependencies
- Focus on business logic

**2. Integration Tests**
- Test multiple components working together
- Test API endpoints with database
- Test full workflows

**3. E2E Tests (End-to-End)**
- Test complete user flows
- Test from UI to database
- Simulate real user interactions

### Testing Coverage Target
```
Backend: 80%+ coverage
Frontend: 70%+ coverage
Overall: 75%+ coverage
```

---

## 🔧 Backend Testing Guide

### Unit Test Structure

#### 1. Password & Authentication Tests

**File to create:** `Phase-2/backend/tests/test_auth_logic.py`

```python
import pytest
from dependencies.auth import hash_password, verify_password, create_access_token, create_refresh_token
import jwt
from config import get_jwt_config

class TestPasswordHashing:
    """Test password hashing and verification"""

    def test_hash_password_creates_hash(self):
        """Test that password gets hashed"""
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert hashed != password
        assert len(hashed) > len(password)

    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert verify_password(password, hashed) == True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "TestPassword123!"
        hashed = hash_password(password)

        assert verify_password("WrongPassword", hashed) == False

    def test_different_hashes_same_password(self):
        """Test that same password creates different hashes (due to salt)"""
        password = "TestPassword123!"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        assert hash1 != hash2  # Different due to salt
        assert verify_password(password, hash1) == True
        assert verify_password(password, hash2) == True

class TestJWTTokens:
    """Test JWT token generation and validation"""

    def test_access_token_created(self):
        """Test that access token is created"""
        user_id = "test-user-123"
        token = create_access_token(user_id)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_access_token_contains_user_id(self):
        """Test that access token contains user_id in payload"""
        user_id = "test-user-123"
        token = create_access_token(user_id)

        config = get_jwt_config()
        payload = jwt.decode(
            token,
            config["SECRET_KEY"],
            algorithms=[config["ALGORITHM"]]
        )

        assert payload["user_id"] == user_id
        assert payload["type"] == "access"

    def test_refresh_token_created(self):
        """Test that refresh token is created"""
        user_id = "test-user-123"
        token = create_refresh_token(user_id)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_refresh_token_contains_user_id(self):
        """Test that refresh token contains user_id"""
        user_id = "test-user-123"
        token = create_refresh_token(user_id)

        config = get_jwt_config()
        payload = jwt.decode(
            token,
            config["SECRET_KEY"],
            algorithms=[config["ALGORITHM"]]
        )

        assert payload["user_id"] == user_id
        assert payload["type"] == "refresh"

    def test_invalid_token_raises_error(self):
        """Test that invalid token raises JWTError"""
        invalid_token = "invalid.token.here"

        config = get_jwt_config()
        with pytest.raises(jwt.JWTError):
            jwt.decode(
                invalid_token,
                config["SECRET_KEY"],
                algorithms=[config["ALGORITHM"]]
            )
```

#### 2. Model Validation Tests

**File to create:** `Phase-2/backend/tests/test_models.py`

```python
import pytest
from models.user import User
from models.task import Task
from datetime import datetime

class TestUserModel:
    """Test User model validation"""

    def test_user_creation(self):
        """Test creating a user"""
        user = User(
            id="test-id",
            email="test@example.com",
            name="Test User",
            password_hash="hashed_pwd",
            is_active=True,
            created_at=datetime.utcnow()
        )

        assert user.id == "test-id"
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.is_active == True

    def test_user_email_unique(self):
        """Test that user email is unique constraint"""
        # This would be tested in integration tests with database
        pass

class TestTaskModel:
    """Test Task model validation"""

    def test_task_creation(self):
        """Test creating a task"""
        task = Task(
            user_id="user-123",
            title="Test Task",
            description="Test Description",
            priority="high",
            status="pending",
            created_at=datetime.utcnow()
        )

        assert task.user_id == "user-123"
        assert task.title == "Test Task"
        assert task.priority == "high"
        assert task.status == "pending"

    def test_task_default_priority(self):
        """Test that default priority is medium"""
        task = Task(
            user_id="user-123",
            title="Test Task",
            created_at=datetime.utcnow()
        )

        assert task.priority == "medium"

    def test_task_default_status(self):
        """Test that default status is pending"""
        task = Task(
            user_id="user-123",
            title="Test Task",
            created_at=datetime.utcnow()
        )

        assert task.status == "pending"
```

### Integration Test Structure

#### 1. Authentication Flow Tests

**File to create:** `Phase-2/backend/tests/test_auth_integration.py`

```python
import pytest
from fastapi.testclient import TestClient
from main import app
from db.connection import Base, engine
from sqlalchemy.orm import Session

# Setup test database
@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

class TestAuthFlow:
    """Test complete authentication flow"""

    def test_signup_flow(self, client, test_db):
        """Test complete signup flow"""
        # Step 1: Signup
        response = client.post("/api/auth/signup", json={
            "email": "test@example.com",
            "password": "SecurePassword123!",
            "name": "Test User"
        })

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
        user_id = data["id"]

        # Step 2: Verify user can login
        login_response = client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "SecurePassword123!"
        })

        assert login_response.status_code == 200
        login_data = login_response.json()
        assert "access_token" in login_data
        assert "refresh_token" in login_data
        assert login_data["user"]["id"] == user_id

    def test_duplicate_email_signup(self, client, test_db):
        """Test that duplicate email is rejected"""
        # First signup
        client.post("/api/auth/signup", json={
            "email": "test@example.com",
            "password": "SecurePassword123!",
            "name": "Test User"
        })

        # Second signup with same email
        response = client.post("/api/auth/signup", json={
            "email": "test@example.com",
            "password": "DifferentPassword123!",
            "name": "Another User"
        })

        assert response.status_code == 409
        assert "already registered" in response.json()["detail"]

    def test_login_wrong_password(self, client, test_db):
        """Test login with wrong password"""
        # Create user
        client.post("/api/auth/signup", json={
            "email": "test@example.com",
            "password": "SecurePassword123!",
            "name": "Test User"
        })

        # Try to login with wrong password
        response = client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "WrongPassword123!"
        })

        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    def test_token_refresh(self, client, test_db):
        """Test token refresh flow"""
        # Signup and login
        client.post("/api/auth/signup", json={
            "email": "test@example.com",
            "password": "SecurePassword123!",
            "name": "Test User"
        })

        login_response = client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "SecurePassword123!"
        })

        refresh_token = login_response.json()["refresh_token"]

        # Use refresh token
        response = client.post("/api/auth/refresh", json={
            "refresh_token": refresh_token
        })

        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_get_current_user_authorized(self, client, test_db):
        """Test getting current user with valid token"""
        # Signup and login
        client.post("/api/auth/signup", json={
            "email": "test@example.com",
            "password": "SecurePassword123!",
            "name": "Test User"
        })

        login_response = client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "SecurePassword123!"
        })

        access_token = login_response.json()["access_token"]

        # Get current user
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "password_hash" not in data  # Password should not be returned

    def test_get_current_user_unauthorized(self, client, test_db):
        """Test getting current user without token"""
        response = client.get("/api/auth/me")

        assert response.status_code == 403
```

#### 2. Task CRUD Tests

**File to create:** `Phase-2/backend/tests/test_tasks_integration.py`

```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def authenticated_client(client):
    """Create authenticated client with user"""
    # Signup
    client.post("/api/auth/signup", json={
        "email": "test@example.com",
        "password": "SecurePassword123!",
        "name": "Test User"
    })

    # Login
    login_response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "SecurePassword123!"
    })

    access_token = login_response.json()["access_token"]
    client.headers = {"Authorization": f"Bearer {access_token}"}

    return client

class TestTaskCRUD:
    """Test task CRUD operations"""

    def test_create_task(self, authenticated_client):
        """Test creating a task"""
        response = authenticated_client.post("/api/tasks", json={
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high"
        })

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["priority"] == "high"
        assert data["status"] == "pending"
        task_id = data["id"]

        return task_id

    def test_list_tasks(self, authenticated_client):
        """Test listing tasks"""
        # Create a task
        authenticated_client.post("/api/tasks", json={
            "title": "Task 1",
            "priority": "high"
        })

        authenticated_client.post("/api/tasks", json={
            "title": "Task 2",
            "priority": "medium"
        })

        # List tasks
        response = authenticated_client.get("/api/tasks")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    def test_list_tasks_with_filtering(self, authenticated_client):
        """Test listing tasks with status filter"""
        # Create tasks
        authenticated_client.post("/api/tasks", json={
            "title": "Task 1",
            "priority": "high"
        })

        # List with filter
        response = authenticated_client.get("/api/tasks?status=pending")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["status"] == "pending"

    def test_update_task(self, authenticated_client):
        """Test updating a task"""
        # Create task
        create_response = authenticated_client.post("/api/tasks", json={
            "title": "Original Title",
            "priority": "low"
        })
        task_id = create_response.json()["id"]

        # Update task
        response = authenticated_client.put(f"/api/tasks/{task_id}", json={
            "title": "Updated Title",
            "priority": "high"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["priority"] == "high"

    def test_delete_task(self, authenticated_client):
        """Test deleting a task"""
        # Create task
        create_response = authenticated_client.post("/api/tasks", json={
            "title": "Task to Delete"
        })
        task_id = create_response.json()["id"]

        # Delete task
        response = authenticated_client.delete(f"/api/tasks/{task_id}")

        assert response.status_code == 204

        # Verify deletion
        get_response = authenticated_client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_complete_task(self, authenticated_client):
        """Test marking task as complete"""
        # Create task
        create_response = authenticated_client.post("/api/tasks", json={
            "title": "Task to Complete"
        })
        task_id = create_response.json()["id"]

        # Complete task
        response = authenticated_client.patch(f"/api/tasks/{task_id}/complete")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["completed_at"] is not None

class TestMultiUserIsolation:
    """Test that users can only access their own tasks"""

    def test_user_cannot_access_other_users_task(self, client):
        """Test that user cannot access other user's task"""
        # Create user 1 and task
        client.post("/api/auth/signup", json={
            "email": "user1@example.com",
            "password": "Password123!",
            "name": "User 1"
        })

        login1 = client.post("/api/auth/login", json={
            "email": "user1@example.com",
            "password": "Password123!"
        })
        token1 = login1.json()["access_token"]

        # Create task as user 1
        task_response = client.post(
            "/api/tasks",
            json={"title": "User 1 Task"},
            headers={"Authorization": f"Bearer {token1}"}
        )
        task_id = task_response.json()["id"]

        # Create user 2
        client.post("/api/auth/signup", json={
            "email": "user2@example.com",
            "password": "Password123!",
            "name": "User 2"
        })

        login2 = client.post("/api/auth/login", json={
            "email": "user2@example.com",
            "password": "Password123!"
        })
        token2 = login2.json()["access_token"]

        # User 2 tries to access user 1's task
        response = client.get(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token2}"}
        )

        assert response.status_code == 403
        assert "Access denied" in response.json()["detail"]
```

---

## 🎨 Frontend Testing Guide

### Unit Test Structure

#### 1. Component Tests

**File to create:** `Phase-2/frontend/__tests__/components/AuthForm.test.tsx`

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import AuthForm from '@/components/AuthForm'

describe('AuthForm Component', () => {
  it('renders email and password fields', () => {
    const mockSubmit = jest.fn()
    render(
      <AuthForm
        onSubmit={mockSubmit}
        isLoading={false}
        submitLabel="Sign In"
      />
    )

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
  })

  it('renders name field when requested', () => {
    const mockSubmit = jest.fn()
    render(
      <AuthForm
        onSubmit={mockSubmit}
        isLoading={false}
        submitLabel="Sign Up"
        includeNameField={true}
      />
    )

    expect(screen.getByLabelText(/full name/i)).toBeInTheDocument()
  })

  it('validates email format', () => {
    const mockSubmit = jest.fn()
    render(
      <AuthForm
        onSubmit={mockSubmit}
        isLoading={false}
        submitLabel="Sign In"
      />
    )

    const form = screen.getByRole('form')
    fireEvent.submit(form)

    expect(screen.getByText(/please enter a valid email/i)).toBeInTheDocument()
  })

  it('validates password length', () => {
    const mockSubmit = jest.fn()
    render(
      <AuthForm
        onSubmit={mockSubmit}
        isLoading={false}
        submitLabel="Sign In"
      />
    )

    const emailInput = screen.getByLabelText(/email/i)
    const passwordInput = screen.getByLabelText(/password/i)

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } })
    fireEvent.change(passwordInput, { target: { value: '123' } })

    const form = screen.getByRole('form')
    fireEvent.submit(form)

    expect(screen.getByText(/password must be at least 6 characters/i)).toBeInTheDocument()
  })

  it('disables submit button when loading', () => {
    const mockSubmit = jest.fn()
    render(
      <AuthForm
        onSubmit={mockSubmit}
        isLoading={true}
        submitLabel="Sign In"
      />
    )

    const submitButton = screen.getByRole('button', { name: /sign in/i })
    expect(submitButton).toBeDisabled()
  })

  it('displays error message', () => {
    const mockSubmit = jest.fn()
    render(
      <AuthForm
        onSubmit={mockSubmit}
        isLoading={false}
        submitLabel="Sign In"
        error="Invalid credentials"
      />
    )

    expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument()
  })

  it('calls onSubmit with form data', async () => {
    const mockSubmit = jest.fn()
    render(
      <AuthForm
        onSubmit={mockSubmit}
        isLoading={false}
        submitLabel="Sign In"
      />
    )

    const emailInput = screen.getByLabelText(/email/i)
    const passwordInput = screen.getByLabelText(/password/i)

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } })
    fireEvent.change(passwordInput, { target: { value: 'password123' } })

    const form = screen.getByRole('form')
    fireEvent.submit(form)

    expect(mockSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    })
  })
})
```

**File to create:** `Phase-2/frontend/__tests__/components/TaskCard.test.tsx`

```typescript
import { render, screen } from '@testing-library/react'
import TaskCard from '@/components/TaskCard'
import { Task } from '@/types/task'

const mockTask: Task = {
  id: 1,
  user_id: 'user-123',
  title: 'Test Task',
  description: 'Test Description',
  status: 'pending',
  priority: 'high',
  due_date: '2025-12-25T00:00:00Z',
  created_at: '2025-12-14T10:00:00Z',
  updated_at: '2025-12-14T10:00:00Z',
  completed_at: null
}

describe('TaskCard Component', () => {
  it('renders task title', () => {
    render(<TaskCard task={mockTask} />)
    expect(screen.getByText('Test Task')).toBeInTheDocument()
  })

  it('renders task description', () => {
    render(<TaskCard task={mockTask} />)
    expect(screen.getByText('Test Description')).toBeInTheDocument()
  })

  it('renders status badge', () => {
    render(<TaskCard task={mockTask} />)
    expect(screen.getByText(/pending/i)).toBeInTheDocument()
  })

  it('renders priority badge', () => {
    render(<TaskCard task={mockTask} />)
    expect(screen.getByText(/high/i)).toBeInTheDocument()
  })

  it('displays edit button', () => {
    render(<TaskCard task={mockTask} />)
    expect(screen.getByRole('link', { name: /edit/i })).toBeInTheDocument()
  })

  it('displays delete button', () => {
    const mockDelete = jest.fn()
    render(<TaskCard task={mockTask} onDelete={mockDelete} />)
    expect(screen.getByRole('button', { name: /delete/i })).toBeInTheDocument()
  })

  it('displays complete button for pending task', () => {
    const mockComplete = jest.fn()
    render(<TaskCard task={mockTask} onComplete={mockComplete} />)
    expect(screen.getByRole('button', { name: /complete/i })).toBeInTheDocument()
  })

  it('does not show complete button for completed task', () => {
    const completedTask = { ...mockTask, status: 'completed' as const }
    render(<TaskCard task={completedTask} />)
    expect(screen.queryByRole('button', { name: /complete/i })).not.toBeInTheDocument()
  })
})
```

#### 2. Hook Tests

**File to create:** `Phase-2/frontend/__tests__/hooks/useAuth.test.ts`

```typescript
import { renderHook, act } from '@testing-library/react'
import { useAuth } from '@/hooks/useAuth'
import * as api from '@/lib/api-client'

jest.mock('@/lib/api-client')

describe('useAuth Hook', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('initializes with null user and no error', () => {
    const { result } = renderHook(() => useAuth())

    expect(result.current.user).toBeNull()
    expect(result.current.error).toBeNull()
    expect(result.current.isLoading).toBe(false)
  })

  it('handles signup success', async () => {
    const mockResponse = {
      data: {
        id: 'user-123',
        email: 'test@example.com',
        name: 'Test User'
      }
    }

    ;(api.apiClient.getClient().post as jest.Mock).mockResolvedValue(mockResponse)

    const { result } = renderHook(() => useAuth())

    await act(async () => {
      await result.current.signup({
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User'
      })
    })

    // Signup doesn't set user, just returns
    expect(result.current.error).toBeNull()
  })

  it('handles signup error', async () => {
    const mockError = {
      response: {
        data: { detail: 'Email already registered' },
        status: 409
      }
    }

    ;(api.apiClient.getClient().post as jest.Mock).mockRejectedValue(mockError)

    const { result } = renderHook(() => useAuth())

    await act(async () => {
      try {
        await result.current.signup({
          email: 'test@example.com',
          password: 'password123',
          name: 'Test User'
        })
      } catch (e) {
        // Expected
      }
    })

    expect(result.current.error).not.toBeNull()
    expect(result.current.error?.detail).toBe('Email already registered')
  })

  it('handles login success', async () => {
    const mockResponse = {
      data: {
        access_token: 'token-123',
        refresh_token: 'refresh-123',
        user: {
          id: 'user-123',
          email: 'test@example.com',
          name: 'Test User',
          created_at: '2025-12-14T10:00:00Z',
          updated_at: '2025-12-14T10:00:00Z',
          is_active: true
        }
      }
    }

    ;(api.apiClient.getClient().post as jest.Mock).mockResolvedValue(mockResponse)

    const { result } = renderHook(() => useAuth())

    await act(async () => {
      await result.current.login({
        email: 'test@example.com',
        password: 'password123'
      })
    })

    expect(result.current.user).not.toBeNull()
    expect(result.current.user?.email).toBe('test@example.com')
    expect(result.current.error).toBeNull()
  })

  it('handles logout', async () => {
    const { result } = renderHook(() => useAuth())

    // First login
    const mockLoginResponse = {
      data: {
        access_token: 'token-123',
        refresh_token: 'refresh-123',
        user: {
          id: 'user-123',
          email: 'test@example.com',
          name: 'Test User',
          created_at: '2025-12-14T10:00:00Z',
          updated_at: '2025-12-14T10:00:00Z',
          is_active: true
        }
      }
    }

    ;(api.apiClient.getClient().post as jest.Mock).mockResolvedValue(mockLoginResponse)

    await act(async () => {
      await result.current.login({
        email: 'test@example.com',
        password: 'password123'
      })
    })

    expect(result.current.user).not.toBeNull()

    // Then logout
    await act(async () => {
      await result.current.logout()
    })

    expect(result.current.user).toBeNull()
  })
})
```

### E2E Test Structure

**File to create:** `Phase-2/frontend/__tests__/e2e/auth-flow.e2e.ts`

```typescript
import { test, expect } from '@playwright/test'

test.describe('Authentication Flow E2E', () => {
  test('Complete signup and login flow', async ({ page }) => {
    // Navigate to home
    await page.goto('http://localhost:3000')

    // Click signup button
    await page.click('text=Sign Up')
    await expect(page).toHaveURL('http://localhost:3000/auth/signup')

    // Fill signup form
    await page.fill('input[placeholder="John Doe"]', 'Test User')
    await page.fill('input[placeholder="you@example.com"]', 'testuser@example.com')
    await page.fill('input[placeholder="••••••••"]', 'TestPassword123!')

    // Submit
    await page.click('button:has-text("Sign Up")')

    // Should redirect to login
    await expect(page).toHaveURL('http://localhost:3000/auth/login')

    // Fill login form
    await page.fill('input[placeholder="you@example.com"]', 'testuser@example.com')
    await page.fill('input[placeholder="••••••••"]', 'TestPassword123!')

    // Submit
    await page.click('button:has-text("Sign In")')

    // Should redirect to dashboard
    await expect(page).toHaveURL('http://localhost:3000/dashboard')

    // Check welcome message
    await expect(page).toContainText('Welcome, Test User')
  })

  test('Task creation flow', async ({ page }) => {
    // Login first
    await page.goto('http://localhost:3000/auth/login')
    await page.fill('input[placeholder="you@example.com"]', 'testuser@example.com')
    await page.fill('input[placeholder="••••••••"]', 'TestPassword123!')
    await page.click('button:has-text("Sign In")')

    // Wait for dashboard
    await expect(page).toHaveURL('http://localhost:3000/dashboard')

    // Click create task
    await page.click('text=Create New Task')
    await expect(page).toHaveURL('http://localhost:3000/dashboard/tasks/create')

    // Fill task form
    await page.fill('input[placeholder="Enter task title..."]', 'Test Task')
    await page.fill('textarea[placeholder="Enter task description..."]', 'Test Description')
    await page.selectOption('select', 'high')

    // Submit
    await page.click('button:has-text("Create Task")')

    // Should redirect to tasks list
    await expect(page).toHaveURL('http://localhost:3000/dashboard/tasks')

    // Check task appears in list
    await expect(page).toContainText('Test Task')
  })

  test('Responsive design on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })

    // Navigate to home
    await page.goto('http://localhost:3000')

    // Check layout is mobile-friendly
    const buttons = page.locator('button')
    const button = buttons.first()

    const box = await button.boundingBox()
    expect(box?.height).toBeGreaterThanOrEqual(48) // Minimum touch target
  })
})
```

---

## 🛠 Testing Tools & Setup

### Backend Testing Setup

**1. Install Testing Dependencies**
```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

**2. Create pytest configuration**

Create `Phase-2/backend/pytest.ini`:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
```

**3. Create conftest.py**

Create `Phase-2/backend/tests/conftest.py`:
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.connection import Base
from db.session import get_db
from main import app
from fastapi.testclient import TestClient

# Use in-memory SQLite for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)(session)

    yield session

    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

### Frontend Testing Setup

**1. Install Testing Dependencies**
```bash
npm install --save-dev jest @testing-library/react @testing-library/jest-dom @testing-library/user-event @types/jest ts-jest jest-environment-jsdom playwright @playwright/test
```

**2. Create Jest config**

Create `Phase-2/frontend/jest.config.js`:
```javascript
const nextJest = require('next/jest')

const createJestConfig = nextJest({
  dir: './',
})

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  testMatch: [
    '**/__tests__/**/*.[jt]s?(x)',
    '**/?(*.)+(spec|test).[jt]s?(x)',
  ],
}

module.exports = createJestConfig(customJestConfig)
```

**3. Create Playwright config**

Create `Phase-2/frontend/playwright.config.ts`:
```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
})
```

---

## 🚀 How to Run Tests

### Backend Tests

```bash
# Run all backend tests
cd Phase-2/backend
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_auth_logic.py

# Run specific test class
pytest tests/test_auth_logic.py::TestPasswordHashing

# Run specific test
pytest tests/test_auth_logic.py::TestPasswordHashing::test_hash_password_creates_hash

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

### Frontend Tests

```bash
# Run all unit tests
cd Phase-2/frontend
npm test

# Run unit tests with coverage
npm test -- --coverage

# Run specific test file
npm test AuthForm.test.tsx

# Run E2E tests
npx playwright test

# Run E2E tests in headed mode (see browser)
npx playwright test --headed

# Run E2E tests for specific browser
npx playwright test --project=chromium
```

---

## ✅ Expected Test Results

### Backend Expected Coverage

```
File                Coverage
──────────────────────────
models/user.py      85%
models/task.py      80%
routes/auth.py      90%
routes/tasks.py     85%
dependencies/auth.py 95%
──────────────────────────
Total               86%
```

### Frontend Expected Coverage

```
File                    Coverage
─────────────────────────────────
components/AuthForm     85%
components/TaskForm     80%
components/TaskCard     85%
hooks/useAuth           90%
hooks/useTasks          85%
─────────────────────────────────
Total                   85%
```

---

## 📝 Testing Checklist

- [ ] Backend unit tests passing (80%+ coverage)
- [ ] Backend integration tests passing
- [ ] Frontend component tests passing (70%+ coverage)
- [ ] Frontend hook tests passing
- [ ] Frontend E2E tests passing
- [ ] All API endpoints tested
- [ ] Authentication flow tested
- [ ] Task CRUD tested
- [ ] Multi-user isolation tested
- [ ] Error handling tested
- [ ] Form validation tested
- [ ] Responsive design tested
- [ ] Security measures tested

---

**Status:** Ready to implement Phase 2D Testing
**Estimated Time:** 2-3 weeks for comprehensive testing
**Target Coverage:** 80%+

