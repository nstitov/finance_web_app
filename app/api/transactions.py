from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.transaction import (
    TransactionCreate,
    TransactionDelete,
    TransactionUpdate,
)
from app.services import category_service, common_service, transaction_service

router = APIRouter(prefix="/transactions")

TEMP_USER_ID = 1
CURRENCIES = ["EUR", "AMD", "RUB", "USD"]


@router.get("/")
def get_transactions(request: Request, db: Session = Depends(get_db)):
    transactions = [
        common_service.transaction_to_json(transaction)
        for transaction in transaction_service.get_all_transactions_by_user(db, TEMP_USER_ID)
    ]
    categories = category_service.get_categories_by_user(db, TEMP_USER_ID)

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="transactions.html",
        context={
            "transactions": transactions,
            "categories": categories,
            "currencies": CURRENCIES,
            "error": None,
        },
        status_code=status.HTTP_200_OK,
    )


@router.post("/create")
def create_transaction(
    title: Annotated[str, Form()],
    amount: Annotated[float, Form()],
    unit_price: Annotated[float, Form()],
    category_id: Annotated[int, Form()],
    currency: Annotated[str, Form()] = None,
    spent_at: Annotated[str, Form()] = None,
    comment: Annotated[str, Form()] = None,
    db: Session = Depends(get_db),
) -> RedirectResponse:
    transaction_create = TransactionCreate(
        user_id=TEMP_USER_ID,
        category_id=category_id,
        title=title,
        amount=amount,
        unit_price=unit_price,
        currency=currency,
        spent_at=datetime.strptime(spent_at, "%Y-%m-%d"),
        comment=comment,
    )
    transaction_service.create_transaction(db, transaction_create)

    return RedirectResponse(url="/transactions", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/{transaction_id}/update")
def update_transaction(
    transaction_id: int,
    title: Annotated[str, Form()],
    amount: Annotated[float, Form()],
    unit_price: Annotated[float, Form()],
    category_id: Annotated[int, Form()],
    currency: Annotated[str, Form()] = None,
    spent_at: Annotated[str, Form()] = None,
    comment: Annotated[str, Form()] = None,
    db: Session = Depends(get_db),
):
    transaction_update = TransactionUpdate(
        id=transaction_id,
        user_id=TEMP_USER_ID,
        category_id=category_id,
        title=title,
        amount=amount,
        unit_price=unit_price,
        currency=currency,
        spent_at=datetime.strptime(spent_at, "%Y-%m-%d"),
        comment=comment,
    )
    updated = transaction_service.update_transaction(db, transaction_update)

    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    return RedirectResponse(url="/transactions", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/{transaction_id}/delete")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction_delete = TransactionDelete(id=transaction_id, user_id=TEMP_USER_ID)
    deleted = transaction_service.delete_transaction(db, transaction_delete)

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    return RedirectResponse("/transactions", status_code=status.HTTP_303_SEE_OTHER)
