from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from app.db.base import Base


class Exercise(Base):
    __tablename__ = "exercise"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    exercise_name: Mapped[str] = mapped_column(String)
    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    equipment_needed: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    difficulty: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    instructions: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    target_muscles: Mapped[Optional[str]] = mapped_column(String, nullable=True)



