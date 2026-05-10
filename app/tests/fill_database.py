import os.path
import pathlib
import random
import sys

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(pathlib.Path(__file__) / "../../.."))

from app.db.base import SessionLocal
from app.services.category_service import CategoryForUserAlreadyExist, create_category
from app.services.transaction_service import create_transaction
from app.services.user_service import add_user, get_all_users

users_raw = [
    {"username": "Nikita", "email": "nstitov00@gmail.com"},
    {"username": "Nastya", "email": "nastya@gmail.com"},
]
categories_raw = ["Products", "Car", "Home", "Presents", "Cafe", "Entertainments"]
transactions_raw = [
    {"title": "Milk", "unit_price": 100},
    {"title": "Eggs", "unit_price": 200},
    {"title": "Biscuits", "unit_price": 300},
    {"title": "Coffe", "unit_price": 1000},
    {"title": "Bread", "unit_price": 50},
    {"title": "Cheese", "unit_price": 1000},
    {"title": "Cream", "unit_price": 500},
    {"title": "Cinema", "unit_price": 3000},
    {"title": "Book", "unit_price": 5000},
    {"title": "Chocolate bar", "unit_price": 500},
    {"title": "Money", "unit_price": 5000},
    {"title": "Gas", "unit_price": 3000},
    {"title": "Service", "unit_price": 10000},
    {"title": "Packets", "unit_price": 200},
    {"title": "Bucket", "unit_price": 1000},
    {"title": "Forks", "unit_price": 300},
    {"title": "Soap", "unit_price": 200},
    {"title": "MacDonalds", "unit_price": 2000},
    {"title": "KFC", "unit_price": 1500},
    {"title": "DrinkIt", "unit_price": 1000},
    {"title": "Walk in park", "unit_price": 500},
]

categories_transactions = {
    "Products": ["Milk", "Eggs", "Biscuits", "Coffe", "Bread", "Cheese", "Cream"],
    "Car": ["Gas", "Service"],
    "Home": ["Packets", "Bucket", "Forks", "Soap"],
    "Presents": ["Book", "Chocolate bar", "Money"],
    "Cafe": ["MacDonalds", "KFC", "DrinkIt"],
    "Entertainments": ["Cinema", "Walk in park"],
}

if __name__ == "__main__":
    db = SessionLocal()

    try:
        existing_users = get_all_users(db)
        for user in users_raw:
            for existing_user in existing_users:
                if user["email"] == existing_user.email:
                    break
            else:
                add_user(db, user)

        for category_name in categories_raw:
            for user in users_raw:
                try:
                    category = create_category(db, category_name, user["email"])
                except CategoryForUserAlreadyExist:
                    pass

        for transaction in transactions_raw:
            for category, category_transactions in categories_transactions.items():
                if transaction["title"] in category_transactions:
                    user = random.choice(users_raw)
                    create_transaction(db, transaction, user["email"], category)
                    break

    finally:
        db.close()
