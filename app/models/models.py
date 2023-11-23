from dotenv import load_dotenv

load_dotenv()

from datetime import datetime
from bson import ObjectId
from pymongo.errors import PyMongoError
from app.db import mongo_client


# TODO: hash passwords
# TODO: tests for Price data
# TODO: tests fod Items


# USERS
class UserModel:
    def __init__(self, username, password, _id=None):
        self.username = username
        self.password = password
        self._id = ObjectId(_id) if _id else None

    @mongo_client
    def save(self, db=None):
        try:
            new_user = {
                'username': self.username,
                'password': self.password,
                'is_superuser': False
            }

            collection = db.users
            result = collection.insert_one(new_user)
            print(f"User {self.username} created with ID: {result.inserted_id}")
        except PyMongoError as e:
            print(f"Error creating admin: {e}")

    @mongo_client
    def update(self, update_data, db=None):
        try:
            collection = db.users
            result = collection.update_one({'_id': self._id}, {'$set': update_data})

            if result.modified_count > 0:
                print(f"User {self.username} updated successfully.")
                return True
            else:
                print("No changes were made.")
                return False

        except PyMongoError as e:
            print(f"Error updating user: {e}")
            return False

    @mongo_client
    def delete(self, db=None):
        try:
            collection = db.users
            result = collection.delete_one({'_id': self._id})

            if result.deleted_count > 0:
                print(f"User {self.username} deleted successfully.")
                return True
            else:
                print("No user was deleted.")
                return False

        except PyMongoError as e:
            print(f"Error deleting user: {e}")
            return False


# ITEMS
class ItemModel:
    def __init__(self, name, url, user_id, _id=None):
        self.name = name
        self.url = url
        self.user_id = ObjectId(user_id)
        self._id = ObjectId(_id) if _id else None

    @mongo_client
    def save(self, db=None):
        try:
            new_item = {
                'name': self.name,
                'url': self.url,
                'user_id': self.user_id

            }

            collection = db.items
            result = collection.insert_one(new_item)
            self._id = result.inserted_id
            print(f"Item saved.")
        except PyMongoError as e:
            print(f"Error creating admin: {e}")

    @mongo_client
    def update(self, update_data, db=None):
        try:
            collection = db.items
            result = collection.update_one({'_id': self._id}, {'$set': update_data})

            if result.modified_count > 0:
                print(f"Item updated successfully.")
                return True
            else:
                print("No changes were made.")
                return False

        except Exception as e:
            print(f"Error updating item: {e}")
            return False

    @mongo_client
    def delete(self, db=None):
        try:
            collection = db.items
            result = collection.delete_one({'_id': self._id})

            if result.deleted_count > 0:
                print(f"Item deleted successfully.")
                return True
            else:
                print("No changes were made")
                return False

        except Exception as e:
            print(f"Error deleting item: {e}")
            return False


# PRICE
class PriceHistoryModel:
    def __init__(self, price, item_id, timestamp=None, _id=None):
        self.price = price
        self.item_id = ObjectId(item_id)
        self.timestamp = timestamp if timestamp else datetime.now()
        self._id = ObjectId(_id) if _id else None

    @mongo_client
    def save(self, db=None):
        try:
            collection = db.price_history

            new_price_entry = {
                'price': self.price,
                'item_id': self.item_id,
                'timestamp': self.timestamp
            }

            result = collection.insert_one(new_price_entry)
            self._id = result.inserted_id
            print(f"New entry created with ID: {self._id}")

            return True

        except Exception as e:
            print(f"Error saving price history entry: {e}")
            return False
