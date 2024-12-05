"""
b. Підтримувати HTTP Basic аутентифікацію. Користувацькі дані (тобто username password) повинні зберігатися:
i. [Easy] у dictionary в середині програми
"""
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

the_catalog = {
    1: {"name": "Laptop", "price": 1000, "quantity": 5},
    2: {"name": "Phone", "price": 500, "quantity": 10},
    3: {"name": "Tablet", "price": 300, "quantity": 7}
}

users = {
    "admin": "password",
    "user1": "password1"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    return None

@app.route('/items', methods=['GET'])
@auth.login_required
def get_all_items():
    return jsonify(the_catalog), 200

@app.route('/items/<int:item_id>', methods=['GET'])
@auth.login_required
def get_item_by_id(item_id):
    item = the_catalog.get(item_id)
    if item:
        return jsonify(item), 200
    else:
        return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
