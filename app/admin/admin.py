from dotenv import load_dotenv
from flask import Blueprint, request, jsonify

from app.models.models import UserModel
from app.views.operations import api

load_dotenv()
from app.db import get_mongo
from pymongo.errors import PyMongoError


# TODO: implement password hashing

def create_save_admin(username, password, is_superuser):
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

        collection = db.admin
        result = collection.insert_one(admin)
        print(f"Admin created with ID: {result.inserted_id}")
    except PyMongoError as e:
        print(f"Error creating admin: {e}")

@api.route('/user/admin', methods=['POST'])
def create_admin():
    data = request.json
    user = UserModel(username=data['username'], password=data['password'], is_superuser=data['is_superuser'])
    user.save()
    return jsonify({"message": "Admin created", "user_id": str(user._id)}), 201

if __name__ == "__main__":
    print("Creating admin...")
    create_save_admin("admin", "admin", is_superuser=True)  # credentials for admin
