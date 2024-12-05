"""
e. Організувати зберігання каталогу товарів:
ii. [Medium] у файлі
"""
import json
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": "password",
    "user1": "password1"
}

catalog_file = 'catalog.json'

def load_catalog():
    try:
        with open(catalog_file, 'r') as file:
            catalog = json.load(file)
            return {int(k): v for k, v in catalog.items()}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_catalog(catalog):
    with open(catalog_file, 'w') as file:
        json.dump(catalog, file)

the_catalog = load_catalog()

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    return None

@app.route('/items', methods=['GET', 'POST'])
@auth.login_required
def handle_items():
    if request.method == 'GET':
        return jsonify(the_catalog), 200
    elif request.method == 'POST':
        new_item = request.get_json()
        if new_item and "name" in new_item and "price" in new_item and "quantity" in new_item:
            new_id = max(the_catalog.keys(), default=0) + 1
            the_catalog[new_id] = new_item
            save_catalog(the_catalog)
            return jsonify({"message": "Item added", "item": new_item}), 201
        else:
            return jsonify({"error": "Invalid item data"}), 400

@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def handle_item_by_id(item_id):
    if request.method == 'GET':
        item = the_catalog.get(item_id)
        if item:
            return jsonify(item), 200
        else:
            return jsonify({"error": "Item not found"}), 404
    elif request.method == 'PUT':
        updated_data = request.get_json()
        if item_id in the_catalog:
            if updated_data and "name" in updated_data and "price" in updated_data and "quantity" in updated_data:
                the_catalog[item_id].update(updated_data)
                save_catalog(the_catalog)
                return jsonify({"message": "Item updated", "item": the_catalog[item_id]}), 200
            else:
                return jsonify({"error": "Invalid item data"}), 400
        else:
            return jsonify({"error": "Item not found"}), 404
    elif request.method == 'DELETE':
        if item_id in the_catalog:
            deleted_item = the_catalog.pop(item_id)
            save_catalog(the_catalog)
            return jsonify({"message": "Item deleted", "item": deleted_item}), 200
        else:
            return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
