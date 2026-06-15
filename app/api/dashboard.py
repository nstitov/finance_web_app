from datetime import datetime

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

import app.services.common_service as coms
import app.services.dashboard_service as das
import app.services.user_service as uss
from app.db.base import get_db

router = APIRouter(prefix="/dashboard")


@router.get("/")
def get_dashboard(
    request: Request,
    month: str | None = None,
    db: Session = Depends(get_db),
):
    if not month:
        month = datetime.utcnow().strftime("%Y-%m")

    current_user = uss.get_current_user(db)
    transactions = das.get_month_transactions(db, current_user.id, month)
    month_statistic = das.calculate_month_statistic(transactions)

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "selected_month": month,
            "total_spent": month_statistic.total_spent,
            "transactions_count": month_statistic.transactions_count,
            "average_transaction": month_statistic.average_transaction,
            "top_category": month_statistic.top_category.name if month_statistic.top_category else None,
            "category_stats": month_statistic.categories_statistic,
            "recent_transactions": [coms.transaction_to_json(tr) for tr in month_statistic.recent_transactions],
            "error": None,
        },
        status_code=status.HTTP_200_OK,
    )
