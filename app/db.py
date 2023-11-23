from dotenv import load_dotenv
from flask_pymongo import PyMongo

load_dotenv()

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from functools import wraps
import os

mongo = PyMongo()

def get_mongo():
    """Connecting to MongoDB. Core function used by other functions."""

    mongo_uri = os.environ.get('MONGO_URI')
    try:
        client = MongoClient(mongo_uri, server_api=ServerApi('1'))
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)


def mongo_client(func):
    """Wrapper for CRUD functions in models.py."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        client = get_mongo()
        if client is None:
            print("MongoDB client is not available.")
            return False
        db = client.mydb

        return func(*args, db=db, **kwargs)

    return wrapper