import mongomock
import pytest
from app.models.models import UserModel
from app.db import get_mongo


@pytest.fixture
def mock_mongo_client(monkeypatch):
    mock_client = mongomock.MongoClient()
    monkeypatch.setattr("app.db.MongoClient", lambda *args, **kwargs: mock_client)
    return mock_client


def test_save_user(mock_mongo_client):
    # Use the mock client for the test
    db = mock_mongo_client.mydb
    users_collection = db.users

    user = UserModel("test_user", "password123")
    user.save()

    # Verify if the user is inserted
    inserted_user = users_collection.find_one({"username": "test_user"})
    assert inserted_user is not None
    assert inserted_user["username"] == "test_user"
