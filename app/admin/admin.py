from dotenv import load_dotenv
load_dotenv()
from app.db import get_mongo
from pymongo.errors import PyMongoError


# TODO: implement password hashing


def create_save_admin(username, password, is_superuser=True):
    """Save admin to database."""
    try:
        client = get_mongo()
        if client is None:
            print("MongoDB client is not available.")
            return
        db = client.mydb

        admin = {
            'username': username,
            'password': password,
            'is_superuser': is_superuser
        }

        collection = db.Users
        result = collection.insert_one(admin)
        print(f"Admin created with ID: {result.inserted_id}")
    except PyMongoError as e:
        print(f"Error creating admin: {e}")


if __name__ == "__main__":
    print("Creating admin...")
    create_save_admin("admin", "admin")  # credentials for admin
