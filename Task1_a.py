"""
1. Розробити REST API веб-сервісу з використанням будь-якого фреймворку python (flask, bottle, etc.). Веб-сервіс повинен:
a. Реалізовувати 2 API endpoints:
i. /items - за цим ендпоінтом проводяться операції з усіма товарами в каталозі, наприклад можливо вивести те, що зберігається у каталозі
ii. /items/<id> - інформація про конкретний товар за його атрибутом <id>
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

the_catalog = {
    1: {"name": "Laptop", "price": 1000, "quantity": 5},
    2: {"name": "Phone", "price": 500, "quantity": 10},
    3: {"name": "Tablet", "price": 300, "quantity": 7}
}

@app.route('/items', methods=['GET'])
def get_all_items():
    return jsonify(the_catalog), 200

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item_by_id(item_id):
    item = the_catalog.get(item_id)
    if item:
        return jsonify(item), 200
    else:
        return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)