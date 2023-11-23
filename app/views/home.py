from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.models import ItemModel, PriceHistoryModel

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
# @login_required
def homepage():
    if current_user.is_authenticated:
        print(f"User {current_user.id} logged in")
    else:
        print("User not logged in")

    items = ItemModel.find_all()
    price_data = {}

    for item in items:
        prices = PriceHistoryModel.price_by_id(str(item._id)) or []  # Ensure this returns a list
        actual_price = prices[-1].price if prices else 'N/A'
        highest_price = max(p.price for p in prices) if prices else 'N/A'
        lowest_price = min(p.price for p in prices) if prices else 'N/A'

        price_data[item.name] = {
            'actual': actual_price,
            'highest': highest_price,
            'lowest': lowest_price,
            'history': [(p.timestamp, p.price) for p in prices]
        }

    return render_template('homepage.html', items=items, price_data=price_data)
