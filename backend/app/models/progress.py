from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey
from app.db.base import Base


class Progress(Base):
    __tablename__ = "progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    workout_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("workoutplan.id"), nullable=True)
    date: Mapped[str] = mapped_column(String)
    exercises_completed: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    sets: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    reps: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    weights: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    calories_burned: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)



