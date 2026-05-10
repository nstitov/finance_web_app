from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, nullable=True, unique=True, index=True)
    username = Column(String, nullable=True)

    telegram_id = Column(String, nullable=True, unique=True, index=True)
    telegram_name = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    categories = relationship("Category", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
