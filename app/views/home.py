from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.db import get_mongo

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
@login_required
def homepage():
    client = get_mongo()
    db = client['mydb']

    item_collection = db.items
    price_history_collection = db.price_history

    items = list(item_collection.find({"user_id": current_user._id}))

    price_data = {}
    for item in items:
        prices = list(price_history_collection.find({"item_id": item["_id"]}))
        if prices:
            latest_price = prices[-1]['price']
            highest_price = max(p['price'] for p in prices)
            lowest_price = min(p['price'] for p in prices)

            processed_price_data = {
                'name': item['name'],
                'latest': latest_price,
                'highest': highest_price,
                'lowest': lowest_price,
                'history': [(p['timestamp'], p['price']) for p in prices]
            }
        else:
            processed_price_data = {
                'name': item['name'],
                'latest': 'N/A',
                'highest': 'N/A',
                'lowest': 'N/A',
                'history': []
            }

        price_data[item["_id"]] = processed_price_data

    return render_template('homepage2.html', items=items, price_data=price_data)
