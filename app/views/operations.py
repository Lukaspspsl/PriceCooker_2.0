from flask import Blueprint, request, jsonify
from app.models.models import UserModel, ItemModel, PriceHistoryModel

api = Blueprint('api', __name__)

# USER OPERATIONS
#CREATE
@api.route('/user', methods=['POST'])
def create_user():
    data = request.json
    user = UserModel(username=data['username'], password=data['password'])
    user.save()
    return jsonify({"message": "User created", "user_id": str(user._id)}), 201

#UPDATE
@api.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = UserModel.user_by_id(user_id)
    if user:
        user.update(data)
        return jsonify({"message": "User updated"}), 200
    return jsonify({"error": "User not found"}), 404

#DELETE
@api.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = UserModel.user_by_id(user_id)
    if user:
        user.delete()
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404

# ITEM OPERATION
#CREATE
@api.route('/item', methods=['POST'])
def create_item():
    data = request.json
    item = ItemModel(name=data['name'], url=data['url'], user_id=data['user_id'])
    item.save()
    return jsonify({"message": "Item created", "item_id": str(item._id)}), 201

#DISPLAY_BY_ID
@api.route("item/<item_id>", methods=["GET"])
def item_by_id(item_id):
    data = request.json
    item = ItemModel.item_by_id(item_id)
    if item:
        return jsonify(item.to_dict()), 200
    return jsonify({"error": "Item not found"}), 404

#DISPLAY_ALL
@api.route('/item', methods=['GET'])
def display_all_items():
    items = ItemModel.find_all()
    return jsonify([item.to_dict() for item in items]), 200

#DELETE
@api.route('/item/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    result = ItemModel.delete(item_id)
    if result:
        return jsonify({"message": "Item deleted"}), 200
    return jsonify({"error": "Item not found or could not be deleted"}), 404


#PRICE DATA OPERATION
#CREATE ENTRY
@api.route('/price_history', methods=['POST'])
def create_price_history():
    data = request.json
    price_entry = PriceHistoryModel(price=data['price'], item_id=data['item_id'])
    price_entry.save()
    return jsonify({"message": "Price history entry created"}), 201

#DISPLAY PRICE BY ID
@api.route('/price_history/<item_id>', methods=['GET'])
def display_price_history_by_id(item_id):
    price_histories = PriceHistoryModel.price_by_id(item_id)
    if price_histories:
        return jsonify([ph.to_dict() for ph in price_histories]), 200
    return jsonify({"error": "Price history not found"}), 404

#DISPLAY ALL
@api.route('/price_history', methods=['GET'])
def display_all_price_histories():
    price_histories = PriceHistoryModel.find_all()
    return jsonify([ph.to_dict() for ph in price_histories]), 200


