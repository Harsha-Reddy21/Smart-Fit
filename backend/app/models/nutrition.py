from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey
from app.db.base import Base


class Nutrition(Base):
    __tablename__ = "nutrition"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    date: Mapped[str] = mapped_column(String)
    meals: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    calories: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    macronutrients: Mapped[Optional[str]] = mapped_column(String, nullable=True)



