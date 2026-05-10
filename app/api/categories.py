from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.category import CategoryCreate
from app.services import category_service

router = APIRouter(prefix="/categories", tags=["categories"])

TEMP_USER_ID = 1


@router.get("/")
def get_categories(request: Request, db: Session = Depends(get_db)):
    categories = category_service.get_categories_by_user(db, TEMP_USER_ID)
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="categories.html",
        context={"categories": categories, "error": None},
        status_code=status.HTTP_200_OK,
    )


@router.post("/")
def add_category(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    try:
        category_create = CategoryCreate(name=name.capitalize(), user_id=TEMP_USER_ID)
        category_service.create_category(db, category_create)
    except category_service.CategoryForUserAlreadyExist as err:
        categories = category_service.get_categories_by_user(db, TEMP_USER_ID)

        return request.app.state.templates.TemplateResponse(
            request=request,
            name="categories.html",
            context={"categories": categories, "error": str(err)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return RedirectResponse(url="/categories", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/{category_id}/delete")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    deleted = category_service.delete_category_by_id(db, category_id, TEMP_USER_ID)

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    return RedirectResponse("/categories", status_code=status.HTTP_303_SEE_OTHER)
