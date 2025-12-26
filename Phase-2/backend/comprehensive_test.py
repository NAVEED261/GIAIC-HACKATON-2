#!/usr/bin/env python3
"""
Comprehensive test suite for Phase-2 Task Management System
Tests backend API and validates all endpoints work correctly
"""

import httpx
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"
client = httpx.Client(timeout=10)

# Test data
TEST_USER_EMAIL = f"comprehensive_test_{int(time.time())}@example.com"
TEST_USER_PASSWORD = "SecurePassword123"
TEST_USER_NAME = "Comprehensive Test User"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_test(name, passed, message=""):
    status = f"{bcolors.OKGREEN}PASS{bcolors.ENDC}" if passed else f"{bcolors.FAIL}FAIL{bcolors.ENDC}"
    print(f"  [{status}] {name}")
    if message:
        print(f"       {message}")

def print_section(title):
    print(f"\n{bcolors.BOLD}{bcolors.HEADER}{'='*60}{bcolors.ENDC}")
    print(f"{bcolors.BOLD}{bcolors.HEADER}{title}{bcolors.ENDC}")
    print(f"{bcolors.BOLD}{bcolors.HEADER}{'='*60}{bcolors.ENDC}")

# ============================================================================
# 1. HEALTH CHECK TESTS
# ============================================================================
print_section("1. HEALTH CHECK TESTS")

try:
    response = client.get(f"{BASE_URL}/health")
    print_test("Health endpoint", response.status_code == 200, f"Status: {response.status_code}")
except Exception as e:
    print_test("Health endpoint", False, str(e))

try:
    response = client.get(f"{BASE_URL}/health/db")
    print_test("Database health", response.status_code == 200, f"Status: {response.status_code}")
except Exception as e:
    print_test("Database health", False, str(e))

# ============================================================================
# 2. AUTHENTICATION TESTS
# ============================================================================
print_section("2. AUTHENTICATION TESTS")

access_token = None
refresh_token = None

# Test signup
try:
    response = client.post(
        f"{BASE_URL}/api/auth/signup",
        json={
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD,
            "name": TEST_USER_NAME
        }
    )
    print_test("User signup", response.status_code == 201, f"Status: {response.status_code}")
except Exception as e:
    print_test("User signup", False, str(e))

# Test login
try:
    response = client.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        }
    )
    success = response.status_code == 200
    print_test("User login", success, f"Status: {response.status_code}")

    if success:
        data = response.json()
        access_token = data.get("access_token")
        refresh_token = data.get("refresh_token")
        user = data.get("user")
        print_test("Login returns access token", access_token is not None)
        print_test("Login returns user data", user is not None and user.get("email") == TEST_USER_EMAIL)
except Exception as e:
    print_test("User login", False, str(e))

# Test get current user
if access_token:
    try:
        response = client.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        success = response.status_code == 200
        print_test("Get current user", success, f"Status: {response.status_code}")
        if success:
            user = response.json()
            print_test("Current user has email", user.get("email") == TEST_USER_EMAIL)
    except Exception as e:
        print_test("Get current user", False, str(e))

# ============================================================================
# 3. TASK MANAGEMENT TESTS
# ============================================================================
print_section("3. TASK MANAGEMENT TESTS")

task_id = None

if access_token:
    headers = {"Authorization": f"Bearer {access_token}"}

    # Create task
    try:
        response = client.post(
            f"{BASE_URL}/api/tasks",
            json={
                "title": "Test Task 1",
                "description": "This is a test task",
                "priority": "High",
                "status": "pending"
            },
            headers=headers
        )
        success = response.status_code == 201
        print_test("Create task", success, f"Status: {response.status_code}")

        if success:
            task_data = response.json()
            task_id = task_data.get("id")
            print_test("Task has ID", task_id is not None, f"Task ID: {task_id}")
    except Exception as e:
        print_test("Create task", False, str(e))

    # Get tasks
    try:
        response = client.get(
            f"{BASE_URL}/api/tasks",
            headers=headers
        )
        success = response.status_code == 200
        print_test("Get all tasks", success, f"Status: {response.status_code}")

        if success:
            tasks = response.json()
            print_test("Tasks returned as list", isinstance(tasks, list), f"Found {len(tasks)} task(s)")
    except Exception as e:
        print_test("Get all tasks", False, str(e))

    # Get single task
    if task_id:
        try:
            response = client.get(
                f"{BASE_URL}/api/tasks/{task_id}",
                headers=headers
            )
            success = response.status_code == 200
            print_test("Get single task", success, f"Status: {response.status_code}")
        except Exception as e:
            print_test("Get single task", False, str(e))

    # Update task
    if task_id:
        try:
            response = client.put(
                f"{BASE_URL}/api/tasks/{task_id}",
                json={
                    "title": "Updated Task Title",
                    "description": "Updated description",
                    "priority": "Medium",
                    "status": "in_progress"
                },
                headers=headers
            )
            success = response.status_code == 200
            print_test("Update task", success, f"Status: {response.status_code}")
        except Exception as e:
            print_test("Update task", False, str(e))

    # Complete task
    if task_id:
        try:
            response = client.patch(
                f"{BASE_URL}/api/tasks/{task_id}/complete",
                headers=headers
            )
            success = response.status_code == 200
            print_test("Complete task", success, f"Status: {response.status_code}")
        except Exception as e:
            print_test("Complete task", False, str(e))

    # Delete task
    if task_id:
        try:
            response = client.delete(
                f"{BASE_URL}/api/tasks/{task_id}",
                headers=headers
            )
            success = response.status_code == 204
            print_test("Delete task", success, f"Status: {response.status_code}")
        except Exception as e:
            print_test("Delete task", False, str(e))

# ============================================================================
# 4. SUMMARY
# ============================================================================
print_section("4. TEST SUMMARY")
print(f"\n{bcolors.OKGREEN}All tests completed!{bcolors.ENDC}\n")
print(f"Test User Email: {TEST_USER_EMAIL}")
print(f"Test User Password: {TEST_USER_PASSWORD}")
print(f"\nBackend is running on: {BASE_URL}")
print(f"Frontend is running on: http://localhost:3001")
print(f"\nYou can now test the frontend manually:")
print(f"  1. Navigate to http://localhost:3001")
print(f"  2. Click 'Sign Up'")
print(f"  3. Register with any email and password (8+ characters)")
print(f"  4. Login with the same credentials")
print(f"  5. Create, edit, and delete tasks")
