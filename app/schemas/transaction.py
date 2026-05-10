from typing import Optional

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    user_id: int
    category_id: int

    title: str
    amount: float
    unit_price: float

    currency: Optional[str] = None
    spent_at: Optional[str] = None
    comment: Optional[str] = None


class TransactionDelete(BaseModel):
    id: int
    user_id: int
