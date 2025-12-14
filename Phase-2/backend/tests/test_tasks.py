"""Task management endpoints tests"""
import pytest
from datetime import datetime, timedelta


class TestTaskCreate:
    """Test task creation endpoint"""

    def test_create_task_success(self, client, test_user):
        """Test successful task creation"""
        # Signup
        signup_response = client.post("/api/auth/signup", json=test_user)
        access_token = signup_response.json()["access_token"]

        # Create task
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "high",
            "due_date": (datetime.now() + timedelta(days=1)).date().isoformat()
        }
        response = client.post(
            "/api/tasks",
            json=task_data,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["priority"] == task_data["priority"]
        assert data["status"] == "pending"
        print(f"✅ Task created successfully")

    def test_create_task_no_token(self, client):
        """Test create task without authentication"""
        response = client.post(
            "/api/tasks",
            json={"title": "Test"}
        )
        assert response.status_code == 403
        print(f"✅ Missing token rejected on task creation")

    def test_create_task_missing_title(self, client, test_user):
        """Test create task without title"""
        # Signup
        signup_response = client.post("/api/auth/signup", json=test_user)
        access_token = signup_response.json()["access_token"]

        # Try create without title
        response = client.post(
            "/api/tasks",
            json={"description": "No title"},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 422
        print(f"✅ Missing title rejected")


class TestTaskList:
    """Test task listing endpoint"""

    def test_get_tasks_empty(self, client, test_user):
        """Test getting empty task list"""
        # Signup
        signup_response = client.post("/api/auth/signup", json=test_user)
        access_token = signup_response.json()["access_token"]

        # Get tasks
        response = client.get(
            "/api/tasks",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
        print(f"✅ Empty task list retrieved")

    def test_get_tasks_with_data(self, client, test_user):
        """Test getting task list with tasks"""
        # Signup
        signup_response = client.post("/api/auth/signup", json=test_user)
        access_token = signup_response.json()["access_token"]

        # Create task
        client.post(
            "/api/tasks",
            json={"title": "Task 1"},
            headers={"Authorization": f"Bearer {access_token}"}
        )

        # Get tasks
        response = client.get(
            "/api/tasks",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Task 1"
        print(f"✅ Task list with data retrieved")

    def test_get_tasks_filter_by_status(self, client, test_user):
        """Test filtering tasks by status"""
        # Signup
        signup_response = client.post("/api/auth/signup", json=test_user)
        access_token = signup_response.json()["access_token"]

        # Create pending task
        response1 = client.post(
            "/api/tasks",
            json={"title": "Pending Task", "status": "pending"},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        task_id = response1.json()["id"]

        # Get pending tasks
        response = client.get(
            "/api/tasks?status=pending",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        print(f"✅ Task filtering by status works")

    def test_get_tasks_no_token(self, client):
        """Test getting tasks without token"""
        response = client.get("/api/tasks")
        assert response.status_code == 403
        print(f"✅ Missing token rejected on task listing")

    def test_multi_user_isolation(self, client, test_user, test_user_2):
        """Test that users only see their own tasks"""
        # User 1 signup and create task
        signup1 = client.post("/api/auth/signup", json=test_user)
        token1 = signup1.json()["access_token"]

        client.post(
            "/api/tasks",
            json={"title": "User 1 Task"},
            headers={"Authorization": f"Bearer {token1}"}
        )

        # User 2 signup and create task
        signup2 = client.post("/api/auth/signup", json=test_user_2)
        token2 = signup2.json()["access_token"]

        client.post(
            "/api/tasks",
            json={"title": "User 2 Task"},
            headers={"Authorization": f"Bearer {token2}"}
        )

        # User 1 gets their tasks (should only see 1)
        response1 = client.get(
            "/api/tasks",
            headers={"Authorization": f"Bearer {token1}"}
        )
        assert len(response1.json()) == 1
        assert response1.json()[0]["title"] == "User 1 Task"

        # User 2 gets their tasks (should only see 1)
        response2 = client.get(
            "/api/tasks",
            headers={"Authorization": f"Bearer {token2}"}
        )
        assert len(response2.json()) == 1
        assert response2.json()[0]["title"] == "User 2 Task"
        print(f"✅ Multi-user isolation verified")


class TestTaskUpdate:
    """Test task update endpoint"""

    def test_update_task_success(self, client, test_user):
        """Test successful task update"""
        # Signup
        signup_response = client.post("/api/auth/signup", json=test_user)
        access_token = signup_response.json()["access_token"]

        # Create task
        create_response = client.post(
            "/api/tasks",
            json={"title": "Original Title"},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        task_id = create_response.json()["id"]

        # Update task
        response = client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Updated Title", "priority": "high"},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["priority"] == "high"
        print(f"✅ Task updated successfully")

    def test_update_task_not_found(self, client, test_user):
        """Test updating non-existent task"""
        # Signup
        signup_response = client.post("/api/auth/signup", json=test_user)
        access_token = signup_response.json()["access_token"]

        # Try update non-existent task
        response = client.put(
            "/api/tasks/99999",
            json={"title": "Updated"},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 404
        print(f"✅ Non-existent task update rejected")

    def test_update_task_unauthorized(self, client, test_user, test_user_2):
        """Test updating another user's task"""
        # User 1 signup and create task
        signup1 = client.post("/api/auth/signup", json=test_user)
        token1 = signup1.json()["access_token"]

        create_response = client.post(
            "/api/tasks",
            json={"title": "User 1 Task"},
            headers={"Authorization": f"Bearer {token1}"}
        )
        task_id = create_response.json()["id"]

        # User 2 signup
        signup2 = client.post("/api/auth/signup", json=test_user_2)
        token2 = signup2.json()["access_token"]

        # User 2 tries to update User 1's task
        response = client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Hacked"},
            headers={"Authorization": f"Bearer {token2}"}
        )
        assert response.status_code == 403
        print(f"✅ Unauthorized task update rejected")


class TestTaskDelete:
    """Test task deletion endpoint"""

    def test_delete_task_success(self, client, test_user):
        """Test successful task deletion"""
        # Signup
        signup_response = client.post("/api/auth/signup", json=test_user)
        access_token = signup_response.json()["access_token"]

        # Create task
        create_response = client.post(
            "/api/tasks",
            json={"title": "Delete Me"},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        task_id = create_response.json()["id"]

        # Delete task
        response = client.delete(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200

        # Verify deleted
        get_response = client.get(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert get_response.status_code == 404
        print(f"✅ Task deleted successfully")

    def test_delete_task_unauthorized(self, client, test_user, test_user_2):
        """Test deleting another user's task"""
        # User 1 signup and create task
        signup1 = client.post("/api/auth/signup", json=test_user)
        token1 = signup1.json()["access_token"]

        create_response = client.post(
            "/api/tasks",
            json={"title": "User 1 Task"},
            headers={"Authorization": f"Bearer {token1}"}
        )
        task_id = create_response.json()["id"]

        # User 2 signup
        signup2 = client.post("/api/auth/signup", json=test_user_2)
        token2 = signup2.json()["access_token"]

        # User 2 tries to delete User 1's task
        response = client.delete(
            f"/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {token2}"}
        )
        assert response.status_code == 403
        print(f"✅ Unauthorized task deletion rejected")


class TestTaskComplete:
    """Test task completion endpoint"""

    def test_complete_task_success(self, client, test_user):
        """Test marking task as complete"""
        # Signup
        signup_response = client.post("/api/auth/signup", json=test_user)
        access_token = signup_response.json()["access_token"]

        # Create task
        create_response = client.post(
            "/api/tasks",
            json={"title": "Complete Me"},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        task_id = create_response.json()["id"]

        # Complete task
        response = client.patch(
            f"/api/tasks/{task_id}/complete",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        print(f"✅ Task marked as complete")

    def test_complete_already_completed_task(self, client, test_user):
        """Test completing an already completed task"""
        # Signup
        signup_response = client.post("/api/auth/signup", json=test_user)
        access_token = signup_response.json()["access_token"]

        # Create and complete task
        create_response = client.post(
            "/api/tasks",
            json={"title": "Complete Me"},
            headers={"Authorization": f"Bearer {access_token}"}
        )
        task_id = create_response.json()["id"]

        client.patch(
            f"/api/tasks/{task_id}/complete",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        # Try to complete again
        response = client.patch(
            f"/api/tasks/{task_id}/complete",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        print(f"✅ Already completed task handled correctly")
