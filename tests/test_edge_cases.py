import pytest
from fastapi.testclient import TestClient
from src.app import app


def test_signup_full_activity(client):
    """Test that cannot signup when activity is full"""
    activity_name = "Baloncesto"
    
    # Fill up the activity (max 15, currently has 2)
    for i in range(13):
        client.post(f"/activities/{activity_name}/signup?email=user{i}@test.com")
    
    # Try to add one more
    response = client.post(
        f"/activities/{activity_name}/signup?email=overflow@test.com"
    )
    assert response.status_code == 400
    assert "full" in response.json()["detail"].lower()


def test_remove_from_nonexistent_activity(client):
    """Test removing from nonexistent activity returns 404"""
    response = client.delete(
        "/activities/Actividad Inexistente/signup?email=test@example.com"
    )
    assert response.status_code == 404


def test_activity_data_integrity(client):
    """Test that activity data is correctly structured"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)
        assert len(activity_data["participants"]) <= activity_data["max_participants"]
