"""Health check endpoints tests"""


class TestHealth:
    """Test health check endpoints"""

    def test_health_endpoint(self, client):
        """Test basic health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print(f"✅ Health check passed")

    def test_health_db_endpoint(self, client):
        """Test database health check"""
        response = client.get("/health/db")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "database" in data
        print(f"✅ Database health check passed")
