import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Fixture that provides a TestClient with fresh app state"""
    # Store original state
    original_activities = deepcopy(activities)
    
    # Create client
    test_client = TestClient(app)
    
    yield test_client
    
    # Restore original state after test
    activities.clear()
    activities.update(original_activities)
