from app.models.models import ItemModel, PriceHistoryModel
from app.db import get_mongo, mongo_client
from datetime import datetime

@mongo_client
def store_price(price, item_id, db=None):

    collection = db.price_history

    if price is not None and isinstance(price, float):
        new_price_entry = {"price": price, "item_id": item_id, "timestamp": datetime.now()}
        collection.insert_one(new_price_entry)
        print(f"Price entry for item {item_id} added.")


@mongo_client
def store_name(name, item_id, db=None):
    collection = db.items

    result = collection.update_one({"_id": item_id}, {"$set": {"name": name}})
    if result.modified_count > 0:
        print(f"Item name updated for item {item_id}.")
    else:
        print(f"No update made.")


@mongo_client
def store_in_db(name, price, url, db=None):
    item_collection = db.items  # Replace with your actual collection name
    price_history_collection = db.price_history  # Replace with your actual collection name

    item = item_collection.find_one({"url": url})
    if not item:
        item = {"name": name, "url": url}
        result = item_collection.insert_one(item)
        item_id = result.inserted_id
    else:
        item_id = item["_id"]

    if isinstance(price, float):
        new_price_entry = {"price": price, "item_id": item_id, "timestamp": datetime.now()}
        price_history_collection.insert_one(new_price_entry)
        print(f"Price  entry for item {item_id} added.")
