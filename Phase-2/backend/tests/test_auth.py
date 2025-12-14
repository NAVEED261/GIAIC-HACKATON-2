"""Authentication endpoints tests"""
import pytest
from fastapi.testclient import TestClient


class TestAuthSignup:
    """Test user registration endpoint"""

    def test_signup_success(self, client, test_user):
        """Test successful user registration"""
        response = client.post(
            "/api/auth/signup",
            json=test_user
        )
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["user"]["email"] == test_user["email"]
        print(f"✅ Signup successful: {test_user['email']}")

    def test_signup_duplicate_email(self, client, test_user):
        """Test signup with duplicate email"""
        # First signup
        response1 = client.post("/api/auth/signup", json=test_user)
        assert response1.status_code == 201

        # Second signup with same email
        response2 = client.post("/api/auth/signup", json=test_user)
        assert response2.status_code == 400
        assert "already exists" in response2.json()["detail"].lower()
        print(f"✅ Duplicate email prevented")

    def test_signup_invalid_email(self, client):
        """Test signup with invalid email"""
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "invalid-email",
                "password": "TestPassword123!@#"
            }
        )
        assert response.status_code == 422
        print(f"✅ Invalid email rejected")

    def test_signup_weak_password(self, client):
        """Test signup with weak password"""
        response = client.post(
            "/api/auth/signup",
            json={
                "email": "weakpwd@example.com",
                "password": "123"  # Too weak
            }
        )
        assert response.status_code == 422
        print(f"✅ Weak password rejected")


class TestAuthLogin:
    """Test user login endpoint"""

    def test_login_success(self, client, test_user):
        """Test successful login"""
        # First signup
        client.post("/api/auth/signup", json=test_user)

        # Then login
        response = client.post(
            "/api/auth/login",
            json={
                "email": test_user["email"],
                "password": test_user["password"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        print(f"✅ Login successful: {test_user['email']}")

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "AnyPassword123!@#"
            }
        )
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()
        print(f"✅ Non-existent user rejected")

    def test_login_wrong_password(self, client, test_user):
        """Test login with wrong password"""
        # Signup first
        client.post("/api/auth/signup", json=test_user)

        # Try login with wrong password
        response = client.post(
            "/api/auth/login",
            json={
                "email": test_user["email"],
                "password": "WrongPassword123!@#"
            }
        )
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()
        print(f"✅ Wrong password rejected")


class TestAuthRefresh:
    """Test token refresh endpoint"""

    def test_refresh_token_success(self, client, test_user):
        """Test successful token refresh"""
        # Signup
        signup_response = client.post("/api/auth/signup", json=test_user)
        refresh_token = signup_response.json()["refresh_token"]

        # Refresh
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        print(f"✅ Token refresh successful")

    def test_refresh_invalid_token(self, client):
        """Test refresh with invalid token"""
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": "invalid.token.here"}
        )
        assert response.status_code == 401
        print(f"✅ Invalid token rejected")


class TestAuthMe:
    """Test get current user endpoint"""

    def test_get_current_user(self, client, test_user):
        """Test getting current user info"""
        # Signup
        signup_response = client.post("/api/auth/signup", json=test_user)
        access_token = signup_response.json()["access_token"]

        # Get current user
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user["email"]
        print(f"✅ Get current user successful")

    def test_get_current_user_no_token(self, client):
        """Test getting current user without token"""
        response = client.get("/api/auth/me")
        assert response.status_code == 403
        print(f"✅ Missing token rejected")

    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        assert response.status_code == 403
        print(f"✅ Invalid token rejected")


class TestAuthLogout:
    """Test logout endpoint"""

    def test_logout_success(self, client, test_user):
        """Test successful logout"""
        # Signup
        signup_response = client.post("/api/auth/signup", json=test_user)
        access_token = signup_response.json()["access_token"]

        # Logout
        response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 200
        print(f"✅ Logout successful")

    def test_logout_no_token(self, client):
        """Test logout without token"""
        response = client.post("/api/auth/logout")
        assert response.status_code == 403
        print(f"✅ Missing token rejected on logout")
