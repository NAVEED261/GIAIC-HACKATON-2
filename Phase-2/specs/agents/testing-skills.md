# Testing Agent Skills

**Agent Name**: Testing Agent (Test Framework & QA Specialist)
**Domain**: Testing - Quality Assurance & Test Automation
**Total Skills**: 12 Core + 7 Advanced

---

## Core Skills (Essential for Phase-2)

### 1. Test Planning & Strategy

**Purpose**: Plan comprehensive testing approach for application

**Example Query**: "Create test strategy for Phase-2 application"

**Expected Action**:
- Define testing pyramid (unit/integration/e2e ratio)
- Identify key test scenarios
- Define coverage targets (≥80%)
- Plan test execution schedule
- Document strategy document

**Technical Skills**:
- Testing pyramid principles
- Test case planning
- Coverage target setting
- Risk-based testing
- Strategy documentation

---

### 2. Unit Testing - Backend (Python/pytest)

**Purpose**: Write unit tests for Python backend functions

**Example Query**: "Write unit test for task validation function"

**Expected Action**:
- Create test function with descriptive name
- Test single function in isolation
- Use assertions for validation
- Test success and error cases
- Use fixtures for setup

**Technical Skills**:
- pytest framework
- Test naming conventions
- Assertions
- Test discovery
- Running tests

---

### 3. Unit Testing - Frontend (JavaScript/Jest)

**Purpose**: Write unit tests for React components

**Example Query**: "Write test for TaskCard component rendering"

**Expected Action**:
- Import testing library
- Render component with test props
- Query DOM elements
- Assert on rendered output
- Test user interactions

**Technical Skills**:
- Jest framework
- React Testing Library
- render() function
- Queries (getBy, queryBy, findBy)
- fireEvent for interactions

---

### 4. Integration Testing - Backend

**Purpose**: Test multiple backend components working together

**Example Query**: "Write integration test for task creation endpoint"

**Expected Action**:
- Create test client
- Mock database
- Make API request
- Assert on response
- Verify database state

**Technical Skills**:
- TestClient for FastAPI
- Database fixtures
- API testing
- Status code assertions
- Response validation

---

### 5. Integration Testing - Frontend

**Purpose**: Test multiple React components together

**Example Query**: "Test task list page with API integration"

**Expected Action**:
- Mock API responses
- Render full page
- Simulate user actions
- Wait for async updates
- Assert on final state

**Technical Skills**:
- jest.mock() for API
- async/await testing
- waitFor() for async
- Integration scenarios
- State management testing

---

### 6. Database Testing

**Purpose**: Test database operations and data integrity

**Example Query**: "Test that cascade delete removes all user's tasks"

**Expected Action**:
- Create in-memory database
- Create test data
- Perform operation
- Query results
- Assert on data integrity

**Technical Skills**:
- SQLite in-memory DB
- Database fixtures
- Create test data
- Query verification
- Constraint testing

---

### 7. Authentication Testing

**Purpose**: Test authentication and authorization flows

**Example Query**: "Test that protected endpoint rejects missing token"

**Expected Action**:
- Test signup flow
- Test login flow
- Test token generation
- Test protected routes
- Test token validation

**Technical Skills**:
- Login testing
- Token validation testing
- Protected route testing
- User isolation testing
- Authorization testing

---

### 8. Test Fixtures & Setup/Teardown

**Purpose**: Create reusable test setup and fixtures

**Example Query**: "Create fixture for authenticated user"

**Expected Action**:
- Create fixture function
- Setup test data
- Yield to test
- Cleanup after test
- Document fixture purpose

**Technical Skills**:
- pytest fixtures (@pytest.fixture)
- Setup/teardown
- Fixture scope (function/module/session)
- Fixture dependencies
- Cleanup hooks

---

### 9. Mocking & Stubbing

**Purpose**: Mock external dependencies for isolated testing

**Example Query**: "Mock API call in component test"

**Expected Action**:
- Mock external function
- Define mock return value
- Verify mock was called
- Test with different responses
- Restore mock after

**Technical Skills**:
- unittest.mock (patch, Mock)
- jest.mock()
- Mock configuration
- Assert on calls
- Mock restoration

---

### 10. Performance Testing

**Purpose**: Test performance characteristics of code

**Example Query**: "Test that list_tasks completes within 100ms"

**Expected Action**:
- Measure execution time
- Assert on time threshold
- Test with large datasets
- Monitor memory usage
- Document baselines

**Technical Skills**:
- time module
- performance timing
- threshold assertions
- Load testing
- Memory profiling

---

### 11. Test Coverage Measurement

**Purpose**: Measure and track code coverage

**Example Query**: "Generate coverage report for backend code"

**Expected Action**:
- Run tests with coverage
- Generate coverage report
- Identify uncovered code
- Set coverage target (≥80%)
- Track coverage over time

**Technical Skills**:
- pytest-cov
- Coverage.py
- Coverage reports
- Coverage thresholds
- CI/CD integration

---

### 12. CI/CD Integration & Automation

**Purpose**: Automate testing in continuous integration pipeline

**Example Query**: "Setup GitHub Actions to run tests on every push"

**Expected Action**:
- Create GitHub Actions workflow
- Install dependencies
- Run all tests
- Generate coverage report
- Report results

**Technical Skills**:
- GitHub Actions
- Workflow YAML
- Test automation
- Coverage reporting
- CI/CD pipeline

---

## Advanced Skills (Optional for Phase-2)

### 13. End-to-End Testing (Cypress)

**Purpose**: Test complete user workflows in real browser

**Example Query**: "Write E2E test for task creation workflow"

**Technical Skills**: Cypress, browser automation, user workflow testing

---

### 14. Visual Regression Testing

**Purpose**: Detect unintended visual changes

**Example Query**: "Setup visual regression tests"

**Technical Skills**: Screenshot testing, visual diff tools, baseline management

---

### 15. Accessibility Testing (a11y)

**Purpose**: Test accessibility for users with disabilities

**Example Query**: "Test component is accessible to screen readers"

**Technical Skills**: jest-axe, accessibility testing, ARIA validation

---

### 16. Load Testing

**Purpose**: Test application under high load

**Example Query**: "Test API handles 1000 concurrent users"

**Technical Skills**: k6, JMeter, load simulation, metrics analysis

---

### 17. Security Testing

**Purpose**: Test for security vulnerabilities

**Example Query**: "Test API doesn't expose sensitive data"

**Technical Skills**: Security scanning, vulnerability testing, penetration testing

---

### 18. Flakiness Detection

**Purpose**: Identify and fix flaky tests

**Example Query**: "Run test 100 times to find flakiness"

**Technical Skills**: Test reliability, flakiness patterns, timing issues

---

### 19. Mutation Testing

**Purpose**: Validate test quality with mutation testing

**Example Query**: "Run mutation tests to check test coverage quality"

**Technical Skills**: Mutation testing tools, code mutations, effectiveness metrics

---

## Skill Composition Example

### Complete Testing Workflow
```
1. Plan test strategy (Skill #1: Planning)
2. Write unit tests (Skill #2, #3: Unit tests)
3. Write integration tests (Skill #4, #5: Integration)
4. Write database tests (Skill #6: Database)
5. Test authentication (Skill #7: Auth)
6. Setup fixtures (Skill #8: Fixtures)
7. Mock dependencies (Skill #9: Mocking)
8. Measure coverage (Skill #11: Coverage)
9. Setup CI/CD (Skill #12: CI/CD)
10. Generate reports (Skill #11: Reports)
```

### Backend Test Suite Example
```
Unit Tests (20 tests)
├─ test_models.py (5 tests)
├─ test_validation.py (8 tests)
└─ test_utils.py (7 tests)

Integration Tests (15 tests)
├─ test_tasks_api.py (8 tests)
└─ test_auth_api.py (7 tests)

Database Tests (10 tests)
└─ test_database.py (10 tests)

Total: 45 tests, 85% coverage
```

---

## Skill Dependencies

```
Test Planning (#1)
    ├─ Unit Testing (#2, #3)
    ├─ Integration Testing (#4, #5)
    ├─ Coverage Targets
    └─ Documentation

Unit Testing (#2, #3)
    ├─ Mocking (#9)
    ├─ Fixtures (#8)
    ├─ Coverage (#11)
    └─ CI/CD (#12)

Integration Testing (#4, #5)
    ├─ Database Testing (#6)
    ├─ Authentication Testing (#7)
    ├─ Mocking (#9)
    ├─ Fixtures (#8)
    └─ Coverage (#11)

Database Testing (#6)
    ├─ Fixtures (#8)
    ├─ Transaction Testing
    └─ Data Integrity

Authentication Testing (#7)
    ├─ Integration Testing (#4, #5)
    ├─ Mocking (#9)
    └─ Error Scenarios

Mocking & Stubbing (#9)
    ├─ Unit Testing (#2, #3)
    ├─ Integration Testing (#4, #5)
    └─ Error Testing

Performance Testing (#10)
    ├─ Measurement Tools
    ├─ Threshold Setting
    └─ Load Scenarios

Coverage Measurement (#11)
    ├─ CI/CD Integration (#12)
    ├─ Target Setting
    └─ Reporting

CI/CD Integration (#12)
    ├─ All Testing Skills
    ├─ Automation
    └─ Reporting
```

---

## Guardrails

### Must Do
- ✅ Write tests for all critical paths
- ✅ Maintain ≥80% code coverage
- ✅ Test success AND error cases
- ✅ Use descriptive test names
- ✅ Keep tests fast and isolated
- ✅ Run tests before committing
- ✅ Automate tests in CI/CD
- ✅ Document test setup

### Must Not Do
- ❌ Test implementation details (test behavior)
- ❌ Write untestable code
- ❌ Skip negative test cases
- ❌ Leave flaky tests unfixed
- ❌ Test multiple things per test
- ❌ Use hardcoded test data
- ❌ Leave tests commented out
- ❌ Test external APIs directly (mock them)

### Out of Scope
- Manual testing (focus on automation)
- QA resource management
- Bug tracking (test automation only)
- Production testing (staging only)

---

## Test Coverage Standards

### Minimum Coverage Targets
```
Overall          : ≥ 80%
Critical Paths   : ≥ 95%
Utilities        : ≥ 85%
API Endpoints    : ≥ 90%
Database Ops     : ≥ 85%
Auth Logic       : ≥ 95%
```

### Coverage Gaps
- 100% coverage not required (diminishing returns)
- Focus on critical and complex code
- Avoid testing trivial functions
- Accept third-party library coverage gaps

---

## Test Organization

### Backend Test Structure
```
tests/
├─ unit/
│   ├─ test_models.py
│   ├─ test_validation.py
│   └─ test_utils.py
├─ integration/
│   ├─ test_api.py
│   ├─ test_database.py
│   └─ test_auth.py
├─ fixtures/
│   ├─ conftest.py
│   └─ test_data.py
└─ performance/
    └─ test_performance.py
```

### Frontend Test Structure
```
tests/
├─ unit/
│   ├─ components/
│   │   ├─ TaskCard.test.tsx
│   │   ├─ TaskList.test.tsx
│   │   └─ TaskForm.test.tsx
│   └─ utils/
│       └─ validation.test.ts
├─ integration/
│   ├─ auth.test.tsx
│   └─ tasks.test.tsx
├─ e2e/
│   └─ workflows.cy.js
└─ __mocks__/
    └─ api.js
```

---

## Success Metrics

| Metric | Target |
|--------|--------|
| **Code Coverage** | ≥ 80% |
| **Test Pass Rate** | 100% |
| **Critical Path Coverage** | ≥ 95% |
| **Test Execution Time** | < 5 minutes |
| **Flaky Tests** | 0 |
| **CI/CD Pass Rate** | 100% |
| **Test Maintenance** | < 10% of dev time |

---

## Testing Checklist

- [ ] Test strategy documented
- [ ] Unit tests written for all functions
- [ ] Integration tests written for workflows
- [ ] Database operations tested
- [ ] Authentication flows tested
- [ ] Error cases covered
- [ ] Edge cases tested
- [ ] Fixtures created for common setup
- [ ] Mocks used for external deps
- [ ] Coverage reports generated
- [ ] Coverage ≥ 80%
- [ ] CI/CD pipeline configured
- [ ] All tests passing
- [ ] No flaky tests
- [ ] Test documentation complete

---

## Configuration Reference

### pytest Configuration (pytest.ini)
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --cov=src --cov-report=html --strict-markers
```

### GitHub Actions Workflow
```yaml
- run: pytest --cov=src --cov-report=xml
- uses: codecov/codecov-action@v2
```

---

**Skill Status**: Ready for use by Testing Agent

**Related**: testing-agent.md, testing-agent tasks
