import mongomock
import pytest
from app.admin.admin import create_save_admin


@pytest.fixture
def mock_mongo_client(monkeypatch):
    mock_client = mongomock.MongoClient()
    monkeypatch.setattr("app.admin.admin.MongoClient", lambda *args, **kwargs: mock_client)
    return mock_client


def test_save_admin(mock_mongo_client):
    # Use the mock client for the test
    db = mock_mongo_client.mydb
    users_collection = db.Users

    create_save_admin("test_admin", "password123", True)

    # Verify if the user is inserted
    assert users_collection.find_one({"username": "test_admin"}) is not None
