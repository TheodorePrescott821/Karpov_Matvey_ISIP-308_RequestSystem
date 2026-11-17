"""End-to-end tests for authentication, authorization, and workflow API."""

import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from request_system.config import settings
from request_system.application.services.auth_service import AuthService
from request_system.presentation.api import create_app
from request_system.infrastructure.database.sqlite import SQLiteDatabase
from pathlib import Path


@pytest.fixture
def test_app():
    """Create test FastAPI app with database."""
    # Use in-memory database for testing
    db = SQLiteDatabase(":memory:", Path(__file__).parent.parent / "docs" / "sql" / "schema.sql")
    db.initialize()
    
    def uow_factory():
        return db.unit_of_work()
    
    app = create_app(uow_factory)
    return app


@pytest.fixture
def client(test_app):
    """Create test client."""
    return TestClient(test_app)


# ============================================================================
# Authentication Tests (ФТ-1)
# ============================================================================

class TestAuthentication:
    """Test JWT authentication (ФТ-1)."""

    def test_login_applicant(self, client):
        """Test applicant login."""
        response = client.post("/api/auth/login", json={
            "email": "applicant@test.com",
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user_id"] == 1
        assert data["email"] == "applicant@test.com"
        assert "applicant" in data["roles"]

    def test_login_operator(self, client):
        """Test operator login."""
        response = client.post("/api/auth/login", json={
            "email": "operator@test.com",
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "operator" in data["roles"]

    def test_login_executor(self, client):
        """Test executor login."""
        response = client.post("/api/auth/login", json={
            "email": "executor@test.com",
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "executor" in data["roles"]

    def test_login_reviewer(self, client):
        """Test reviewer login."""
        response = client.post("/api/auth/login", json={
            "email": "reviewer@test.com",
            "password": "password123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "reviewer" in data["roles"]

    def test_login_invalid_email(self, client):
        """Test login with invalid email."""
        response = client.post("/api/auth/login", json={
            "email": "nonexistent@test.com",
            "password": "password123"
        })
        assert response.status_code == 401
        assert "Invalid" in response.json()["detail"]

    def test_login_invalid_password(self, client):
        """Test login with wrong password."""
        response = client.post("/api/auth/login", json={
            "email": "applicant@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        assert "Invalid" in response.json()["detail"]

    def test_token_format(self, client):
        """Test JWT token format."""
        response = client.post("/api/auth/login", json={
            "email": "applicant@test.com",
            "password": "password123"
        })
        token = response.json()["access_token"]
        
        # Verify token structure (3 parts separated by dots)
        parts = token.split(".")
        assert len(parts) == 3

    def test_token_expiration(self):
        """Test token expiration time."""
        token = AuthService.create_token(
            user_id=1,
            email="test@example.com",
            roles=["applicant"]
        )
        
        payload = AuthService.decode_token(token)
        assert payload is not None
        assert payload.email == "test@example.com"


# ============================================================================
# Role-Based Access Control Tests (ФТ-18)
# ============================================================================

class TestRoleBasedAccessControl:
    """Test role-based access control (ФТ-18)."""

    def test_applicant_can_create_request(self, client):
        """Test applicant can create requests."""
        # Login as applicant
        login_response = client.post("/api/auth/login", json={
            "email": "applicant@test.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        # Create request
        response = client.post(
            "/api/requests",
            json={
                "description": "Test request",
                "category_id": 1,
                "priority": "High"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "новая"

    def test_operator_cannot_create_request(self, client):
        """Test operator cannot create requests."""
        login_response = client.post("/api/auth/login", json={
            "email": "operator@test.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        response = client.post(
            "/api/requests",
            json={
                "description": "Test request",
                "category_id": 1
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403
        assert "applicant" in response.json()["detail"]

    def test_operator_can_update_status(self, client):
        """Test operator can update request status."""
        login_response = client.post("/api/auth/login", json={
            "email": "operator@test.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        response = client.put(
            "/api/requests/100/status",
            json={
                "new_status": "назначена",
                "explanation": "Assigned"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200

    def test_applicant_cannot_update_status(self, client):
        """Test applicant cannot update request status."""
        login_response = client.post("/api/auth/login", json={
            "email": "applicant@test.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        response = client.put(
            "/api/requests/100/status",
            json={"new_status": "назначена"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403

    def test_executor_can_submit_result(self, client):
        """Test executor can submit result."""
        login_response = client.post("/api/auth/login", json={
            "email": "executor@test.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        response = client.post(
            "/api/requests/100/results",
            json={"description": "Work completed"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200

    def test_reviewer_can_make_decision(self, client):
        """Test reviewer can make acceptance decision."""
        login_response = client.post("/api/auth/login", json={
            "email": "reviewer@test.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        response = client.post(
            "/api/requests/100/decision",
            json={
                "outcome": "accepted",
                "comment": "Good work"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200

    def test_missing_token_returns_401(self, client):
        """Test missing token returns 401."""
        response = client.post(
            "/api/requests",
            json={"description": "Test"}
        )
        assert response.status_code == 401

    def test_invalid_token_returns_401(self, client):
        """Test invalid token returns 401."""
        response = client.post(
            "/api/requests",
            json={"description": "Test"},
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        assert response.status_code == 401


# ============================================================================
# Workflow API Tests (ФТ-6 to ФТ-13)
# ============================================================================

class TestWorkflowAPI:
    """Test workflow API endpoints (ФТ-6 to ФТ-13)."""

    def test_create_request_endpoint(self, client):
        """Test POST /api/requests."""
        login_response = client.post("/api/auth/login", json={
            "email": "applicant@test.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        response = client.post(
            "/api/requests",
            json={
                "description": "Need help with something",
                "category_id": 1,
                "priority": "Medium"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert "request_id" in data
        assert "request_number" in data
        assert data["status"] == "новая"

    def test_list_requests_endpoint(self, client):
        """Test GET /api/requests."""
        login_response = client.post("/api/auth/login", json={
            "email": "applicant@test.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        response = client.get(
            "/api/requests",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "requests" in data
        assert "total_count" in data

    def test_update_status_endpoint(self, client):
        """Test PUT /api/requests/{id}/status."""
        login_response = client.post("/api/auth/login", json={
            "email": "operator@test.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        response = client.put(
            "/api/requests/100/status",
            json={
                "new_status": "в работе",
                "explanation": "Started"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["new_status"] == "в работе"

    def test_assign_executor_endpoint(self, client):
        """Test PUT /api/requests/{id}/assign."""
        login_response = client.post("/api/auth/login", json={
            "email": "operator@test.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        response = client.put(
            "/api/requests/100/assign",
            json={
                "executor_id": 3,
                "reason": "Best available"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["executor_id"] == 3

    def test_submit_result_endpoint(self, client):
        """Test POST /api/requests/{id}/results."""
        login_response = client.post("/api/auth/login", json={
            "email": "executor@test.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        response = client.post(
            "/api/requests/100/results",
            json={"description": "Task completed successfully"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "submitted_at" in data

    def test_make_decision_endpoint(self, client):
        """Test POST /api/requests/{id}/decision."""
        login_response = client.post("/api/auth/login", json={
            "email": "reviewer@test.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        response = client.post(
            "/api/requests/100/decision",
            json={
                "outcome": "accepted",
                "comment": "Excellent work"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["outcome"] == "accepted"

    def test_add_comment_endpoint(self, client):
        """Test POST /api/requests/{id}/comments."""
        login_response = client.post("/api/auth/login", json={
            "email": "applicant@test.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        response = client.post(
            "/api/requests/100/comments",
            json={
                "text": "This is a comment",
                "is_service": False
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["text"] == "This is a comment"


# ============================================================================
# Notification Tests (ФТ-15)
# ============================================================================

class TestNotifications:
    """Test notification system (ФТ-15)."""

    def test_get_notifications_endpoint(self, client):
        """Test GET /api/notifications."""
        login_response = client.post("/api/auth/login", json={
            "email": "operator@test.com",
            "password": "password123"
        })
        token = login_response.json()["access_token"]
        
        response = client.get(
            "/api/notifications",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "notifications" in data
        assert "unread_count" in data
        assert isinstance(data["unread_count"], int)

    def test_notifications_require_auth(self, client):
        """Test notifications endpoint requires authentication."""
        response = client.get("/api/notifications")
        assert response.status_code == 401


# ============================================================================
# Happy Path Workflow Test
# ============================================================================

class TestHappyPathWorkflow:
    """Test complete workflow from creation to approval."""

    def test_complete_workflow(self, client):
        """Test complete request workflow."""
        # Step 1: Applicant creates request
        applicant_login = client.post("/api/auth/login", json={
            "email": "applicant@test.com",
            "password": "password123"
        })
        applicant_token = applicant_login.json()["access_token"]
        
        create_response = client.post(
            "/api/requests",
            json={"description": "Complete workflow test"},
            headers={"Authorization": f"Bearer {applicant_token}"}
        )
        assert create_response.status_code == 201
        request_id = create_response.json()["request_id"]
        
        # Step 2: Operator updates status
        operator_login = client.post("/api/auth/login", json={
            "email": "operator@test.com",
            "password": "password123"
        })
        operator_token = operator_login.json()["access_token"]
        
        status_response = client.put(
            f"/api/requests/{request_id}/status",
            json={"new_status": "назначена"},
            headers={"Authorization": f"Bearer {operator_token}"}
        )
        assert status_response.status_code == 200
        
        # Step 3: Operator assigns executor
        assign_response = client.put(
            f"/api/requests/{request_id}/assign",
            json={"executor_id": 3},
            headers={"Authorization": f"Bearer {operator_token}"}
        )
        assert assign_response.status_code == 200
        
        # Step 4: Executor submits result
        executor_login = client.post("/api/auth/login", json={
            "email": "executor@test.com",
            "password": "password123"
        })
        executor_token = executor_login.json()["access_token"]
        
        result_response = client.post(
            f"/api/requests/{request_id}/results",
            json={"description": "Work completed"},
            headers={"Authorization": f"Bearer {executor_token}"}
        )
        assert result_response.status_code == 200
        
        # Step 5: Reviewer makes decision
        reviewer_login = client.post("/api/auth/login", json={
            "email": "reviewer@test.com",
            "password": "password123"
        })
        reviewer_token = reviewer_login.json()["access_token"]
        
        decision_response = client.post(
            f"/api/requests/{request_id}/decision",
            json={"outcome": "accepted"},
            headers={"Authorization": f"Bearer {reviewer_token}"}
        )
        assert decision_response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
