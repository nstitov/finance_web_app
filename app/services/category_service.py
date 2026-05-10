from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate
from app.services.user_service import get_user_by_email


class CategoryForUserAlreadyExist(Exception):
    pass


def get_categories(db: Session) -> list[Category]:
    return db.query(Category).all()


def get_categories_by_user(db: Session, user_id: int) -> list[Category]:
    return db.query(Category).filter(Category.user_id == user_id).order_by(Category.name).all()


def get_user_category(db: Session, user: User, category: str) -> Category:
    return db.query(Category).filter(Category.user_id == user.id, Category.name == category).one()


def create_category(db: Session, category_create: CategoryCreate) -> Category:
    existing_category = (
        db.query(Category)
        .filter(Category.user_id == category_create.user_id, Category.name == category_create.name)
        .first()
    )

    if existing_category:
        raise CategoryForUserAlreadyExist

    category = Category(name=category_create.name, user_id=category_create.user_id)
    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def delete_category_by_id(db: Session, category_id: int, user_id: int) -> None:
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()

    if category is None:
        return False

    db.delete(category)
    db.commit()

    return True
