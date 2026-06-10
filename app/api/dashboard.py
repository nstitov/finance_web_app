from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, Request, status
from sqlalchemy.orm import Session

import app.services.common_service as cs
import app.services.dashboard_service as ds
from app.db.base import get_db

router = APIRouter(prefix="/dashboard")

TEMP_USER_ID = 1


@router.get("/")
def get_dashboard(
    request: Request,
    month: str | None = None,
    db: Session = Depends(get_db),
):
    if month is None:
        month = datetime.utcnow().strftime("%Y-%m")

    transactions = ds.get_month_transactions(db, TEMP_USER_ID, month)
    month_statistic = ds.calculate_month_statistic(transactions)

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "selected_month": month,
            "total_spent": month_statistic.total_spent,
            "transactions_count": month_statistic.transactions_count,
            "average_transaction": month_statistic.average_trasnsaction,
            "top_category": month_statistic.top_category.name,
            "category_stats": month_statistic.categories_statistic,
            "recent_transactions": [cs.transaction_to_json(tr) for tr in month_statistic.recent_transactions],
            "error": None,
        },
        status_code=status.HTTP_200_OK,
    )
