from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import app.services.category_service as cats
import app.services.user_service as uss
from app.db.base import get_db
from app.schemas.category import CategoryCreate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/")
def get_categories(request: Request, db: Session = Depends(get_db)):
    current_user = uss.get_current_user(db)
    categories = cats.get_categories_by_user(db, current_user.id)
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="categories.html",
        context={"categories": categories, "error": None},
        status_code=status.HTTP_200_OK,
    )


@router.post("/")
def add_category(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    current_user = uss.get_current_user(db)
    try:
        category_create = CategoryCreate(name=name.capitalize(), user_id=current_user.id)
        cats.create_category(db, category_create)
    except cats.CategoryForUserAlreadyExist as err:
        categories = cats.get_categories_by_user(db, current_user.id)

        return request.app.state.templates.TemplateResponse(
            request=request,
            name="categories.html",
            context={"categories": categories, "error": str(err)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return RedirectResponse(url="/categories", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/{category_id}/delete")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    current_user = uss.get_current_user(db)
    deleted = cats.delete_category_by_id(db, category_id, current_user.id)

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    return RedirectResponse("/categories", status_code=status.HTTP_303_SEE_OTHER)
