import pytest
import mongomock

@pytest.fixture(scope="session")
def mock_mongo_client(monkeypatch):
    mock_client = mongomock.MongoClient()
    monkeypatch.setattr("app.db.MongoClient", lambda *args, **kwargs: mock_client)
    yield mock_client