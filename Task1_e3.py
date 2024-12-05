"""
e. Організувати зберігання каталогу товарів:
iii.	[Hard] у sqlite БД
"""
import sqlite3
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": "password",
    "user1": "password1"
}

def init_db():
    conn = sqlite3.connect('catalog.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    return None

@app.route('/items', methods=['GET', 'POST'])
@auth.login_required
def handle_items():
    conn = sqlite3.connect('catalog.db')
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute('SELECT * FROM items')
        items = [
            {"id": row[0], "name": row[1], "price": row[2], "quantity": row[3]}
            for row in cursor.fetchall()
        ]
        conn.close()
        return jsonify(items), 200
    elif request.method == 'POST':
        new_item = request.get_json()
        if new_item and "name" in new_item and "price" in new_item and "quantity" in new_item:
            cursor.execute(
                'INSERT INTO items (name, price, quantity) VALUES (?, ?, ?)',
                (new_item['name'], new_item['price'], new_item['quantity'])
            )
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()
            return jsonify({"message": "Item added", "item": {"id": new_id, **new_item}}), 201
        else:
            conn.close()
            return jsonify({"error": "Invalid item data"}), 400

@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def handle_item_by_id(item_id):
    conn = sqlite3.connect('catalog.db')
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            item = {"id": row[0], "name": row[1], "price": row[2], "quantity": row[3]}
            return jsonify(item), 200
        else:
            return jsonify({"error": "Item not found"}), 404
    elif request.method == 'PUT':
        updated_data = request.get_json()
        if updated_data and "name" in updated_data and "price" in updated_data and "quantity" in updated_data:
            cursor.execute(
                'UPDATE items SET name = ?, price = ?, quantity = ? WHERE id = ?',
                (updated_data['name'], updated_data['price'], updated_data['quantity'], item_id)
            )
            if cursor.rowcount == 0:
                conn.close()
                return jsonify({"error": "Item not found"}), 404
            conn.commit()
            conn.close()
            return jsonify({"message": "Item updated", "item": {"id": item_id, **updated_data}}), 200
        else:
            conn.close()
            return jsonify({"error": "Invalid item data"}), 400
    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Item not found"}), 404
        conn.commit()
        conn.close()
        return jsonify({"message": "Item deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
