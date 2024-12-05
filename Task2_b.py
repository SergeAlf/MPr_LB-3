"""
b.	[medium] З використанням бібліотеки requests написати клієнт для веб-сервісу, за допомогою якого можна зчитувати каталог товарів, додавати, оновлювати та видаляти товари з каталогу
"""
import requests
import sys
from requests.auth import HTTPBasicAuth

BASE_URL = "http://127.0.0.1:8000"
USERNAME = "admin"
PASSWORD = "password"

def get_all_items():
    response = requests.get(f"{BASE_URL}/items", auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200:
        print("Каталог товарів:")
        for item in response.json():
            print(item)
    else:
        print(f"Помилка: {response.status_code}")

def add_item(name, price, quantity):
    new_item = {
        "name": name,
        "price": price,
        "quantity": quantity
    }
    response = requests.post(f"{BASE_URL}/items", json=new_item, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 201:
        print("Товар успішно додано:", response.json())
    else:
        print(f"Помилка: {response.status_code}", response.json())

def update_item(item_id, name, price, quantity):
    updated_item = {
        "name": name,
        "price": price,
        "quantity": quantity
    }
    response = requests.put(f"{BASE_URL}/items/{item_id}", json=updated_item, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200:
        print("Товар успішно оновлено:", response.json())
    else:
        print(f"Помилка: {response.status_code}", response.json())

def delete_item(item_id):
    response = requests.delete(f"{BASE_URL}/items/{item_id}", auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if response.status_code == 200:
        print("Товар успішно видалено:", response.json())
    else:
        print(f"Помилка: {response.status_code}", response.json())

def main():
    while True:
        print("\nОберіть дію:")
        print("1. Отримати всі товари")
        print("2. Додати новий товар")
        print("3. Оновити існуючий товар")
        print("4. Видалити товар")
        print("5. Вийти")

        choice = input("Ваш вибір: ")

        if choice == "1":
            get_all_items()
        elif choice == "2":
            name = input("Введіть назву товару: ")
            price = float(input("Введіть ціну товару: "))
            quantity = int(input("Введіть кількість товару: "))
            add_item(name, price, quantity)
        elif choice == "3":
            item_id = int(input("Введіть ID товару для оновлення: "))
            name = input("Введіть нову назву товару: ")
            price = float(input("Введіть нову ціну товару: "))
            quantity = int(input("Введіть нову кількість товару: "))
            update_item(item_id, name, price, quantity)
        elif choice == "4":
            item_id = int(input("Введіть ID товару для видалення: "))
            delete_item(item_id)
        elif choice == "5":
            print("Вихід...")
            sys.exit()
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()