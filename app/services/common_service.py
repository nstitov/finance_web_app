from typing import Any

from app.models.transaction import Transaction
from app.models.category import Category
from app.models.user import User


def category_to_json(category: Category) -> dict[str, Any]:
    if not category:
        return {}

    return {
        "id": category.id,
        "name": category.name,
        "created_at": category.created_at.isoformat(),
    }


def transaction_to_json(transaction: Transaction) -> dict[str, Any]:
    return {
        "id": transaction.id,
        "user_id": transaction.user_id,
        "category_id": transaction.category_id,
        "category": category_to_json(transaction.category),
        "title": transaction.title,
        "amount": transaction.amount,
        "unit_price": transaction.unit_price,
        "currency": transaction.currency,
        "comment": transaction.comment,
        "spent_at": transaction.spent_at.isoformat(),
        "created_at": transaction.created_at.isoformat(),
        "updated_at": transaction.updated_at.isoformat(),
    }
