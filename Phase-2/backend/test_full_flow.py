#!/usr/bin/env python
"""Complete API flow testing"""
import httpx
import json
import sys
import time

def test_flow():
    print("=" * 60)
    print("COMPLETE FRONTEND-BACKEND FLOW TEST")
    print("=" * 60)

    base_url = "http://127.0.0.1:8000"
    unique_id = int(time.time() * 1000) % 1000000

    # Test 1: Health Check
    print("\n1. Testing Health Endpoint...")
    try:
        response = httpx.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("   [PASS] Health Check: 200 OK")
            print(f"   Response: {response.json()}")
        else:
            print(f"   [FAIL] Health Check Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   [FAIL] Health Check Error: {e}")
        return False

    # Test 2: Signup
    print("\n2. Testing Signup...")
    try:
        signup_data = {
            "email": f"test_{unique_id}@example.com",
            "password": "FrontendTest123!",
            "name": "Frontend Test User"
        }
        response = httpx.post(f"{base_url}/api/auth/signup", json=signup_data, timeout=5)
        if response.status_code == 201:
            print("   [OK] Signup: 201 Created")
            user_data = response.json()
            print(f"   User ID: {user_data.get('id')}")
            print(f"   Email: {user_data.get('email')}")
            print(f"   Name: {user_data.get('name')}")
        elif response.status_code == 400:
            print("   ⚠ User already exists (400)")
        else:
            print(f"   [FAIL] Signup Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   [FAIL] Signup Error: {e}")
        return False

    # Test 3: Login
    print("\n3. Testing Login...")
    try:
        login_data = {
            "email": f"test_{unique_id}@example.com",
            "password": "FrontendTest123!"
        }
        response = httpx.post(f"{base_url}/api/auth/login", json=login_data, timeout=5)
        if response.status_code == 200:
            print("   [OK] Login: 200 OK")
            auth_data = response.json()
            access_token = auth_data.get('access_token')
            print(f"   Access Token: {access_token[:20]}...")
            print(f"   User: {auth_data.get('user', {}).get('name')}")
        else:
            print(f"   [FAIL] Login Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   [FAIL] Login Error: {e}")
        return False

    # Test 4: Create Task
    print("\n4. Testing Create Task...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        task_data = {
            "title": "Frontend Test Task",
            "description": "Task created to test frontend-backend integration",
            "priority": "high"
        }
        response = httpx.post(f"{base_url}/api/tasks", json=task_data, headers=headers, timeout=5)
        if response.status_code == 201:
            print("   [OK] Create Task: 201 Created")
            task = response.json()
            print(f"   Task ID: {task.get('id')}")
            print(f"   Title: {task.get('title')}")
            print(f"   Status: {task.get('status')}")
            task_id = task.get('id')
        else:
            print(f"   [FAIL] Create Task Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   [FAIL] Create Task Error: {e}")
        return False

    # Test 5: Get Tasks
    print("\n5. Testing Get Tasks...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = httpx.get(f"{base_url}/api/tasks", headers=headers, timeout=5)
        if response.status_code == 200:
            print("   [OK] Get Tasks: 200 OK")
            tasks_data = response.json()
            if isinstance(tasks_data, list):
                print(f"   Tasks Count: {len(tasks_data)}")
                if tasks_data:
                    print(f"   First Task ID: {tasks_data[0].get('id')}")
            else:
                print(f"   Total Tasks: {tasks_data.get('total')}")
                print(f"   Tasks Count: {len(tasks_data.get('items', []))}")
        else:
            print(f"   [FAIL] Get Tasks Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   [FAIL] Get Tasks Error: {e}")
        return False

    # Test 6: Update Task
    if task_id:
        print("\n6. Testing Update Task...")
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            update_data = {
                "title": "Updated Frontend Test Task",
                "description": "Updated description",
                "priority": "low"
            }
            response = httpx.put(f"{base_url}/api/tasks/{task_id}", json=update_data, headers=headers, timeout=5)
            if response.status_code == 200:
                print("   [OK] Update Task: 200 OK")
                task = response.json()
                print(f"   Updated Title: {task.get('title')}")
            else:
                print(f"   [FAIL] Update Task Failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   [FAIL] Update Task Error: {e}")
            return False

    # Test 7: Complete Task
    if task_id:
        print("\n7. Testing Complete Task...")
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = httpx.patch(f"{base_url}/api/tasks/{task_id}/complete", headers=headers, timeout=5)
            if response.status_code == 200:
                print("   [OK] Complete Task: 200 OK")
                task = response.json()
                print(f"   Status: {task.get('status')}")
            else:
                print(f"   [FAIL] Complete Task Failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   [FAIL] Complete Task Error: {e}")
            return False

    # Test 8: Delete Task
    if task_id:
        print("\n8. Testing Delete Task...")
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = httpx.delete(f"{base_url}/api/tasks/{task_id}", headers=headers, timeout=5)
            if response.status_code == 204:
                print("   [OK] Delete Task: 204 No Content")
            elif response.status_code == 200:
                print("   [OK] Delete Task: 200 OK")
            else:
                print(f"   [FAIL] Delete Task Failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   [FAIL] Delete Task Error: {e}")
            return False

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED [OK]")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_flow()
    sys.exit(0 if success else 1)
