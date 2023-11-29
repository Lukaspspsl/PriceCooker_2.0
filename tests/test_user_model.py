from app.models.models import UserModel


def test_save_user(mock_mongo_client):
    db = mock_mongo_client.mydb
    users_collection = db.users

    user = UserModel("test_user", "password123", is_superuser=False)
    user.save()

    inserted_user = users_collection.find_one({"username": "test_user"})
    assert inserted_user is not None
    assert inserted_user["username"] == "test_user"
