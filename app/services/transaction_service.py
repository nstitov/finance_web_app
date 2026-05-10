from sqlalchemy.orm import Session, joinedload

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionDelete


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
