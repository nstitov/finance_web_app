from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from app.models.transaction import Transaction


def get_month_transactions(db: Session, user_id: int, month_year: str) -> list[Transaction]:
    year, month = map(int, month_year.split("-"))
    start_dt = datetime(year=year, month=month, day=1)
    finish_dt = datetime(year=year, month=month + 1, day=1)
    return (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id, Transaction.spent_at >= start_dt, Transaction.spent_at < finish_dt)
        .options(joinedload(Transaction.category))
        .all()
    )


@dataclass
class CategoryStatistic:
    name: str
    transactions_count: int
    total_spent: int
    share_percent: float


@dataclass
class MonthStatistic:
    total_spent: float
    transactions_count: int
    average_trasnsaction: float
    top_category: str
    categories_statistic: list[CategoryStatistic]
    recent_transactions: list[Transaction]


def calculate_month_statistic(transactions: list[Transaction]) -> MonthStatistic:
    total_spent = 0
    transaction_prices = []
    transactions_by_category = {}

    for tr in transactions:
        transaction_price = tr.amount * tr.unit_price
        transaction_prices.append(transaction_price)
        total_spent += transaction_price

        transactions_by_category.setdefault(tr.category.name, [])
        transactions_by_category[tr.category.name].append(transaction_price)

    categories_statistic = []
    for name, trs in transactions_by_category.items():
        category_spent = sum(trs)
        statistic = CategoryStatistic(
            name=name,
            transactions_count=len(trs),
            total_spent=category_spent,
            share_percent=category_spent / total_spent * 100,
        )
        categories_statistic.append(statistic)

    statistic = MonthStatistic(
        total_spent=total_spent,
        transactions_count=len(transactions),
        average_trasnsaction=sum(transaction_prices) / len(transaction_prices) if transaction_prices else 0,
        top_category=max(categories_statistic, key=lambda stat: stat.total_spent) if categories_statistic else None,
        categories_statistic=categories_statistic,
        recent_transactions=transactions,
    )

    return statistic
