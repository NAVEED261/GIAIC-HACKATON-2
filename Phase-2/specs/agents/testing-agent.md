# Testing Agent Specification

**Agent Name**: Testing Agent (Test Framework & QA Specialist)
**Domain**: Testing - Quality Assurance & Test Automation
**Technology**: pytest, Jest, React Testing Library, Cypress, Coverage Tools
**Responsibility**: Design and implement comprehensive testing strategies and test suites
**Created**: 2025-12-14

---

## Agent Overview

The Testing Agent is responsible for designing comprehensive testing strategies, implementing test suites, establishing quality gates, and ensuring code quality and reliability across the Phase-2 full-stack application.

### Primary Responsibilities

1. **Test Strategy & Planning**
   - Define testing pyramid (unit, integration, e2e)
   - Test coverage targets
   - Test execution strategy
   - Continuous testing in CI/CD
   - Risk-based testing approach

2. **Backend Testing**
   - Unit tests for business logic
   - Integration tests for API endpoints
   - Database tests
   - Authentication tests
   - Error handling tests
   - Performance tests

3. **Frontend Testing**
   - Component unit tests
   - Integration tests
   - End-to-end tests
   - Visual regression tests
   - Accessibility tests
   - Performance tests

4. **Test Infrastructure**
   - Test fixtures and setup
   - Mock and stub utilities
   - Test database setup/teardown
   - Continuous integration configuration
   - Test reporting
   - Coverage measurement

5. **Quality Metrics**
   - Code coverage (≥80%)
   - Test pass rate (100%)
   - Performance baselines
   - Bug tracking
   - Defect metrics
   - Test execution time

6. **Test Maintenance**
   - Test code quality
   - Test flakiness prevention
   - Test documentation
   - Regression test suite
   - Test deprecation

---

## Technical Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend Testing** | pytest | Python test framework |
| **Frontend Testing** | Jest + React Testing Library | Component testing |
| **E2E Testing** | Cypress | End-to-end testing |
| **Coverage** | pytest-cov, nyc | Coverage measurement |
| **Mocking** | pytest-mock, jest.mock | Test mocking |
| **CI/CD** | GitHub Actions | Automated testing |
| **Reporting** | pytest-html, Coverage.py | Test reports |

---

## Deliverables

### Backend Tests (tests/)
- `tests/test_models.py` - Data model tests
- `tests/test_routes.py` - API endpoint tests
- `tests/test_auth.py` - Authentication tests
- `tests/test_db.py` - Database tests
- `tests/test_validation.py` - Input validation tests
- `tests/test_security.py` - Security tests
- `tests/test_performance.py` - Performance tests
- `tests/conftest.py` - Test fixtures
- `tests/integration/` - Integration test suites
- `tests/fixtures/` - Test data fixtures

### Frontend Tests (tests/)
- `tests/components/` - Component unit tests
- `tests/pages/` - Page tests
- `tests/integration/` - Integration tests
- `tests/e2e/` - End-to-end tests
- `tests/__mocks__/` - Mock definitions
- `tests/fixtures/` - Test data fixtures
- `tests/setup.js` - Test environment setup

### Test Configuration
- `pytest.ini` - pytest configuration
- `jest.config.js` - Jest configuration
- `cypress.config.js` - Cypress configuration
- `.github/workflows/test.yml` - CI/CD pipeline
- `coverage.json` - Coverage thresholds

### Test Documentation
- `tests/README.md` - Testing guide
- `tests/FIXTURES.md` - Fixture documentation
- `tests/MOCKING.md` - Mocking strategy
- `tests/CI_CD.md` - CI/CD setup

---

## Testing Pyramid

```
        /\
       /  \  E2E Tests (10%)
      /    \
     /------\
    /        \  Integration Tests (30%)
   /          \
  /------------\
 /              \  Unit Tests (60%)
/______________\
```

### Distribution
- **Unit Tests** (60%): Fast, isolated, single component
- **Integration Tests** (30%): Multiple components, test interactions
- **E2E Tests** (10%): Full user workflows, real browser

---

## Backend Testing Strategy

### Unit Tests

#### Model Tests
```python
def test_task_creation():
    """Test creating a task with valid input"""
    task = Task(title="Test task", description="A test")
    assert task.title == "Test task"
    assert task.status == "Pending"

def test_task_validation():
    """Test task validation rejects empty title"""
    with pytest.raises(ValueError):
        Task(title="", description="A test")
```

#### Business Logic Tests
```python
def test_add_task():
    """Test adding task to task manager"""
    agent = TodoActionAgent()
    task_id = agent.add_task("Buy groceries")
    assert task_id == 1
    assert len(agent.list_tasks()) == 1
```

### Integration Tests

#### API Endpoint Tests
```python
def test_create_task_endpoint(client, auth_headers):
    """Test POST /api/tasks endpoint"""
    response = client.post(
        "/api/tasks",
        json={"title": "Test task"},
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test task"

def test_list_tasks_endpoint(client, auth_headers, sample_tasks):
    """Test GET /api/tasks endpoint"""
    response = client.get("/api/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()["data"]) == len(sample_tasks)
```

#### Database Tests
```python
def test_task_persistence(db_session):
    """Test task is persisted to database"""
    task = Task(title="Test", user_id="user_1")
    db_session.add(task)
    db_session.commit()

    retrieved = db_session.query(Task).first()
    assert retrieved.title == "Test"
```

#### Authentication Tests
```python
def test_login_success(client):
    """Test successful login returns token"""
    response = client.post(
        "/api/auth/login",
        json={"email": "user@test.com", "password": "Pass123!"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_route_requires_token(client):
    """Test protected route rejects missing token"""
    response = client.get("/api/tasks")
    assert response.status_code == 401
```

### Test Fixtures

#### Database Fixture
```python
@pytest.fixture
def db_session():
    """Create test database session"""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
```

#### Authentication Fixture
```python
@pytest.fixture
def auth_headers(client):
    """Create authenticated headers"""
    response = client.post(
        "/api/auth/login",
        json={"email": "user@test.com", "password": "Pass123!"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

#### Sample Data Fixture
```python
@pytest.fixture
def sample_tasks(db_session):
    """Create sample tasks for testing"""
    tasks = [
        Task(title="Task 1", user_id="user_1"),
        Task(title="Task 2", user_id="user_1"),
        Task(title="Task 3", user_id="user_2"),
    ]
    for task in tasks:
        db_session.add(task)
    db_session.commit()
    return tasks
```

---

## Frontend Testing Strategy

### Component Unit Tests

#### Basic Render Test
```javascript
test('TaskList renders task items', () => {
  const tasks = [
    { id: 1, title: 'Task 1', status: 'Pending' }
  ];
  render(<TaskList tasks={tasks} />);
  expect(screen.getByText('Task 1')).toBeInTheDocument();
});
```

#### User Interaction Test
```javascript
test('clicking delete button calls onDelete', () => {
  const mockDelete = jest.fn();
  render(<TaskItem task={task} onDelete={mockDelete} />);

  const deleteButton = screen.getByRole('button', { name: /delete/i });
  fireEvent.click(deleteButton);

  expect(mockDelete).toHaveBeenCalledWith(task.id);
});
```

#### Form Validation Test
```javascript
test('form shows error for empty title', async () => {
  render(<TaskForm />);

  const submitButton = screen.getByRole('button', { name: /submit/i });
  fireEvent.click(submitButton);

  await waitFor(() => {
    expect(screen.getByText(/title is required/i)).toBeInTheDocument();
  });
});
```

### Integration Tests

#### Authentication Flow
```javascript
describe('Authentication Flow', () => {
  test('user can signup and login', async () => {
    render(<App />);

    // Signup
    const signupButton = screen.getByRole('button', { name: /signup/i });
    fireEvent.click(signupButton);

    // Fill form and submit
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'user@test.com' }
    });
    fireEvent.click(screen.getByRole('button', { name: /register/i }));

    // Verify user is logged in
    await waitFor(() => {
      expect(screen.getByText(/welcome/i)).toBeInTheDocument();
    });
  });
});
```

#### API Integration
```javascript
test('TaskList fetches and displays tasks', async () => {
  const mockFetch = jest.fn().mockResolvedValue({
    json: async () => ({ data: [{ id: 1, title: 'Task' }] })
  });
  global.fetch = mockFetch;

  render(<TaskList />);

  await waitFor(() => {
    expect(screen.getByText('Task')).toBeInTheDocument();
  });
});
```

### End-to-End Tests (Cypress)

```javascript
describe('Task Management Workflow', () => {
  it('user can create and complete a task', () => {
    cy.visit('http://localhost:3000');

    // Login
    cy.get('[data-testid="email-input"]').type('user@test.com');
    cy.get('[data-testid="password-input"]').type('Pass123!');
    cy.get('[data-testid="login-button"]').click();

    // Create task
    cy.get('[data-testid="add-task-input"]').type('Buy groceries');
    cy.get('[data-testid="add-task-button"]').click();
    cy.contains('Buy groceries').should('exist');

    // Complete task
    cy.get('[data-testid="complete-checkbox-1"]').click();
    cy.get('[data-testid="task-1"]').should('have.class', 'completed');
  });
});
```

---

## Coverage Standards

### Coverage Targets
```
Statements   : ≥ 80%
Branches     : ≥ 75%
Functions    : ≥ 80%
Lines        : ≥ 80%
```

### Measuring Coverage

#### Python (Backend)
```bash
pytest --cov=src --cov-report=html --cov-report=term
```

#### JavaScript (Frontend)
```bash
jest --coverage --collectCoverageFrom="src/**/*.{js,jsx}"
```

### Coverage Report
```
File           | Stmts | Branches | Funcs | Lines
----------------------------------------------------
models.py      |  87   |   92     |  95   |  90
task_manager.py|  85   |  88      |  92   |  87
cli.py         |  82   |  85      |  88   |  84
----------------------------------------------------
Total          |  85   |  88      |  91   |  87
```

---

## CI/CD Pipeline Configuration

### GitHub Actions Workflow
```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v2

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: npm install
      - run: npm run test -- --coverage
      - uses: codecov/codecov-action@v2
```

---

## Test Execution Strategy

### Local Testing
```bash
# Backend tests
pytest tests/ -v --cov=src

# Frontend tests
npm test -- --coverage

# E2E tests
npm run test:e2e
```

### Pre-commit Checks
```bash
# Run before committing
pytest tests/
npm test

# Code quality
pylint src/
eslint src/
```

### Continuous Integration
- Run on every push
- Run on every PR
- Publish coverage reports
- Block merge on failures
- Generate test reports

---

## Test Quality Standards

### Test Code Quality
- Clear, descriptive test names
- One assertion per test (when possible)
- DRY principle - use fixtures
- No hardcoded values
- Good test organization

### Test Reliability
- No flaky tests
- Proper setup/teardown
- Test isolation (no cross-test dependencies)
- Deterministic results
- Fast execution

### Test Documentation
- Clear docstrings
- Example usage comments
- Fixture documentation
- Known limitations noted

---

## Performance Testing

### Backend Performance Tests
```python
def test_list_tasks_performance():
    """Test list_tasks completes within 100ms"""
    agent = TodoActionAgent()

    # Add 1000 tasks
    for i in range(1000):
        agent.add_task(f"Task {i}")

    start = time.time()
    tasks = agent.list_tasks()
    duration = time.time() - start

    assert duration < 0.1  # 100ms target
```

### Frontend Performance Tests
```javascript
test('TaskList renders 100 items in under 1 second', () => {
  const tasks = Array.from({ length: 100 }, (_, i) => ({
    id: i,
    title: `Task ${i}`,
    status: 'Pending'
  }));

  const start = performance.now();
  render(<TaskList tasks={tasks} />);
  const duration = performance.now() - start;

  expect(duration).toBeLessThan(1000);
});
```

---

## Acceptance Criteria

- [ ] Test pyramid implemented (60/30/10 ratio)
- [ ] Backend unit tests (≥26 tests)
- [ ] Backend integration tests (≥27 tests)
- [ ] Frontend component tests (≥20 tests)
- [ ] Frontend integration tests (≥15 tests)
- [ ] E2E tests for critical workflows
- [ ] Code coverage ≥80%
- [ ] All tests passing
- [ ] Test fixtures implemented
- [ ] CI/CD pipeline configured
- [ ] Performance tests included
- [ ] Test documentation complete

---

## Related Specifications

- `@specs/agents/backend-agent.md` - Backend to test
- `@specs/agents/frontend-agent.md` - Frontend to test
- `@specs/features/task-crud-web.md` - Feature requirements
- `@specs/features/authentication.md` - Auth requirements

---

**Agent Status**: 🔄 Ready for Implementation

**Next Step**: Follow `testing-skills.md` for detailed capabilities
