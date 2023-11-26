from dotenv import load_dotenv
from flask_login import UserMixin
from datetime import datetime
from bson import ObjectId
from pymongo.errors import PyMongoError
from app.db import mongo_client

load_dotenv()


# TODO: hash passwords
# TODO: tests for Price data
# TODO: tests fod Items


# USERS
class UserModel(UserMixin):
    def __init__(self, username, password, is_superuser, _id=None):
        self.username = username
        self.password = password
        self.is_superuser = is_superuser
        self._id = ObjectId(_id) if _id else None

    def to_dict(self):
        return {
            "username": self.username,
            "_id": str(self._id)
        }

    # @property
    # def is_active(self):
    #     return True
    #
    # @property
    # def is_anonymous(self):
    #     return False

    def get_id(self):
        return str(self._id)

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

    @classmethod
    @mongo_client
    def user_by_id(cls, user_id: str, db=None):
        collection = db.users

        try:
            if not ObjectId.is_valid(user_id):
                print("Invalid ID.")
                return None

            user_data = collection.find_one({"_id": ObjectId(user_id)})
            if user_data:
                return cls(**user_data)
            else:
                return None

        except PyMongoError as e:
            print(f"Error finding user by ID: {e}")
            return None

    @classmethod
    @mongo_client
    def find_by_username(cls, username, db=None):
        collection = db.users
        user_data = collection.find_one({"username": username})
        if user_data:
            return cls(**user_data)
        else:
            return None

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
    def __init__(self, name, url, _id=None):
        self.name = name
        self.url = url
        self._id = ObjectId(_id) if _id else None

    def to_dict(self):
        return {
            '_id': str(self._id),
            'name': self.name,
            'url': self.url
        }

    @mongo_client
    def save(self, db=None):
        try:
            new_item = {
                'name': self.name,
                'url': self.url
            }

            collection = db.items
            result = collection.insert_one(new_item)
            self._id = result.inserted_id
            print(f"Item saved.")
        except PyMongoError as e:
            print(f"Error creating admin: {e}")

    @classmethod
    @mongo_client
    def find_all(cls, db=None):
        collection = db.items
        items = collection.find()
        return [cls(**item) for item in items]

    @classmethod
    @mongo_client
    def item_by_id(cls, item_id, db=None):

        try:
            collection = db.items
            if not ObjectId.is_valid(item_id):
                print("Invalid ID")
                return None

            item_data = collection.find_one({"_id": ObjectId(item_id)})
            if item_data:
                return cls(**item_data)
            else:
                return None

        except PyMongoError as e:
            print(f"Error finding Item: {e}")
            return None

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

    @property
    def id(self):
        """Return the ID of the item."""
        return self._id


# PRICE
class PriceHistoryModel:
    def __init__(self, price, item_id, timestamp=None, _id=None):
        self.price = price
        self.item_id = ObjectId(item_id)
        self.timestamp = timestamp if timestamp else datetime.now()
        self._id = ObjectId(_id) if _id else None

    def to_dict(self):
        return {
            '_id': str(self._id),
            'price': self.price,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
        }

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

    @classmethod
    @mongo_client
    def find_all(cls, db=None):
        collection = db.price_history
        data = collection.find()
        return [cls(**data) for data in data]

    @classmethod
    @mongo_client
    def price_by_id(cls, item_id, db=None):

        try:
            collection = db.price_history
            if not ObjectId.is_valid(item_id):
                print("Invalid ID")
                return None

            price_data = collection.find({"item_id": ObjectId(item_id)})
            print("searching for price data associated with item_id:", item_id)
            price_histories = []
            for data in price_data:
                print("price data found for item_id:", item_id)
                price_histories.append(cls(**data))

            return price_histories
        except Exception as e:
            print(f"Error in price_by_id: {e}")
            return None
