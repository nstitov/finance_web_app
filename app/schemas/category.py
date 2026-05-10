from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    user_id: int
