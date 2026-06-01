from sqlalchemy.orm import Session, joinedload

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionDelete, TransactionUpdate


def get_all_transactions_by_user(db: Session, user_id: int) -> list[Transaction]:
    return db.query(Transaction).filter(Transaction.user_id == user_id).options(joinedload(Transaction.category)).all()


def create_transaction(db: Session, transaction_create: TransactionCreate) -> Transaction:
    transaction = Transaction(
        user_id=transaction_create.user_id,
        category_id=transaction_create.category_id,
        title=transaction_create.title,
        amount=transaction_create.amount,
        unit_price=transaction_create.unit_price,
    )

    if transaction_create.currency:
        transaction.currency = transaction_create.currency
    if transaction_create.spent_at:
        transaction.spent_at = transaction_create.spent_at
    if transaction_create.comment:
        transaction.comment = transaction_create.comment

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


def update_transaction(db: Session, transaction_update: TransactionUpdate) -> Transaction | None:
    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_update.id, Transaction.user_id == transaction_update.user_id)
        .first()
    )

    if transaction is None:
        return None

    transaction.category_id = transaction_update.category_id
    transaction.title = transaction_update.title
    transaction.amount = transaction_update.amount
    transaction.unit_price = transaction_update.unit_price
    transaction.comment = transaction_update.comment

    if transaction_update.currency is not None:
        transaction.currency = transaction_update.currency
    if transaction_update.spent_at is not None:
        transaction.spent_at = transaction_update.spent_at

    db.commit()
    db.refresh(transaction)

    return transaction


def delete_transaction(db: Session, transaction_delete: TransactionDelete):
    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_delete.id, Transaction.user_id == transaction_delete.user_id)
        .first()
    )

    if transaction is None:
        return False

    db.delete(transaction)
    db.commit()

    return True
