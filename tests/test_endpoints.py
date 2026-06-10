import pytest
from fastapi.testclient import TestClient
from src.app import app


def test_get_activities(client):
    """Test GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert "Club de Ajedrez" in data


def test_signup_success(client):
    """Test successful signup"""
    response = client.post(
        "/activities/Club de Ajedrez/signup?email=test@example.com"
    )
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]


def test_signup_duplicate_email(client):
    """Test signup with duplicate email returns 400"""
    client.post("/activities/Club de Ajedrez/signup?email=dup@test.com")
    response = client.post(
        "/activities/Club de Ajedrez/signup?email=dup@test.com"
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_signup_nonexistent_activity(client):
    """Test signup to nonexistent activity returns 404"""
    response = client.post(
        "/activities/Actividad Falsa/signup?email=test@example.com"
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_remove_participant_success(client):
    """Test successful removal of participant"""
    client.post("/activities/Club de Ajedrez/signup?email=remove@test.com")
    response = client.delete(
        "/activities/Club de Ajedrez/signup?email=remove@test.com"
    )
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]


def test_remove_nonexistent_participant(client):
    """Test removing nonexistent participant returns 404"""
    response = client.delete(
        "/activities/Club de Ajedrez/signup?email=notinlist@test.com"
    )
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]
